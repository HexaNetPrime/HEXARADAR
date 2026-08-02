#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧠 LIGHTWEIGHT NEURAL NETWORK (No TensorFlow Required)
Pure NumPy implementation for vulnerability prediction
✅ बिना किसी API के - पूरी तरह से ऑफलाइन
✅ No TensorFlow Required - Uses NumPy only
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
import re
import random
import math
import numpy as np
import threading
from datetime import datetime

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_features_manager import AIFeatureBase

# ========== No TensorFlow Required ==========
TENSORFLOW_AVAILABLE = False
print("[CNN] Using lightweight NumPy-based neural network")


class SimpleNeuralNetwork:
    """Simple Neural Network - No TensorFlow Required"""
    
    def __init__(self, input_size=8, hidden_size=20, output_size=1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Initialize weights with Xavier initialization
        self.w1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.w2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        self.b2 = np.zeros((1, output_size))
        
        self.trained = False
        self.training_loss = []
    
    def sigmoid(self, x):
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-np.clip(x, -10, 10)))
    
    def sigmoid_derivative(self, x):
        """Derivative of sigmoid"""
        return x * (1 - x)
    
    def relu(self, x):
        """ReLU activation function"""
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        """Derivative of ReLU"""
        return (x > 0).astype(float)
    
    def forward(self, X):
        """Forward pass"""
        self.z1 = np.dot(X, self.w1) + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = np.dot(self.a1, self.w2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2
    
    def train(self, X, y, epochs=200, lr=0.01, verbose=False):
        """Train the neural network"""
        X = np.array(X)
        y = np.array(y).reshape(-1, 1)
        
        self.training_loss = []
        
        for epoch in range(epochs):
            # Forward pass
            output = self.forward(X)
            
            # Calculate loss (binary cross-entropy)
            loss = -np.mean(y * np.log(output + 1e-8) + (1 - y) * np.log(1 - output + 1e-8))
            self.training_loss.append(loss)
            
            # Backward pass
            d_output = output - y
            
            # Hidden to output gradients
            d_w2 = np.dot(self.a1.T, d_output)
            d_b2 = np.sum(d_output, axis=0, keepdims=True)
            
            # Input to hidden gradients
            d_hidden = np.dot(d_output, self.w2.T) * self.relu_derivative(self.a1)
            d_w1 = np.dot(X.T, d_hidden)
            d_b1 = np.sum(d_hidden, axis=0, keepdims=True)
            
            # Update weights with gradient clipping
            self.w2 -= lr * np.clip(d_w2, -5, 5)
            self.b2 -= lr * np.clip(d_b2, -5, 5)
            self.w1 -= lr * np.clip(d_w1, -5, 5)
            self.b1 -= lr * np.clip(d_b1, -5, 5)
            
            if verbose and epoch % 50 == 0:
                print(f"[CNN] Epoch {epoch}/{epochs}, Loss: {loss:.4f}")
        
        self.trained = True
        print(f"[CNN] Training complete! Final loss: {self.training_loss[-1]:.4f}")
    
    def predict(self, X):
        """Predict probabilities"""
        X = np.array(X)
        output = self.forward(X)
        return output.flatten()
    
    def predict_proba(self, X):
        """Predict probabilities (alias)"""
        return self.predict(X)
    
    def get_accuracy(self, X_test, y_test):
        """Calculate accuracy on test data"""
        predictions = self.predict(X_test)
        predicted_classes = (predictions > 0.5).astype(int)
        accuracy = np.mean(predicted_classes == y_test)
        return accuracy


class CNNVulnPredictionFeature(AIFeatureBase):
    """CNN Feature - Lightweight Neural Network Version"""
    
    def __init__(self, parent, colors, output_text_widget=None):
        super().__init__(parent, colors, output_text_widget)
        
        self.root = parent.winfo_toplevel() if parent else None
        
        # Model variables
        self.model = None
        self.is_trained = False
        self.training_data = []
        self.predictions = []
        self.scan_output_text = ""
        self.training_samples = 0
        
        # Port risk mapping
        self.port_risk = {
            21: 8, 22: 7, 23: 9, 25: 6, 53: 6, 80: 7, 111: 5,
            139: 8, 443: 6, 445: 10, 512: 9, 513: 9, 514: 9,
            1099: 7, 1433: 8, 1521: 8, 1524: 10, 2049: 6,
            3306: 7, 3389: 9, 5432: 7, 5900: 7, 6000: 7,
            6379: 7, 6667: 9, 8080: 6, 8443: 6, 9200: 7,
            27017: 7, 3632: 8
        }
        
        self.service_risk = {
            'ftp': 7, 'ssh': 7, 'telnet': 9, 'smtp': 6, 'dns': 6,
            'http': 7, 'https': 6, 'rpcbind': 5, 'netbios-ssn': 8,
            'smb': 10, 'exec': 9, 'login': 9, 'shell': 9,
            'java-rmi': 7, 'mysql': 7, 'postgresql': 7,
            'vnc': 7, 'x11': 7, 'irc': 9, 'redis': 7,
            'mongodb': 7, 'elasticsearch': 7, 'distccd': 8,
            'bindshell': 10, 'nfs': 6
        }
        
        # CVE Database
        self.cve_db = self._build_cve_db()
        
        # Load or train model
        self.load_model()
        
        print("[CNN] Lightweight Neural Network loaded successfully")
        print(f"[CNN] Training samples: {self.training_samples}")
    
    def _build_cve_db(self):
        """Build CVE database for training"""
        return {
            'CVE-2017-0144': {'port': 445, 'service': 'smb', 'cvss': 9.8, 'exploit': 1, 'year': 2017},
            'CVE-2020-0796': {'port': 445, 'service': 'smb', 'cvss': 10.0, 'exploit': 1, 'year': 2020},
            'CVE-2019-0708': {'port': 3389, 'service': 'rdp', 'cvss': 9.8, 'exploit': 1, 'year': 2019},
            'CVE-2014-0160': {'port': 443, 'service': 'ssl', 'cvss': 7.5, 'exploit': 1, 'year': 2014},
            'CVE-2011-2523': {'port': 21, 'service': 'ftp', 'cvss': 10.0, 'exploit': 1, 'year': 2011},
            'CVE-2016-6210': {'port': 22, 'service': 'ssh', 'cvss': 7.5, 'exploit': 1, 'year': 2016},
            'CVE-2012-2122': {'port': 3306, 'service': 'mysql', 'cvss': 7.5, 'exploit': 1, 'year': 2012},
            'CVE-2019-9193': {'port': 5432, 'service': 'postgresql', 'cvss': 7.5, 'exploit': 1, 'year': 2019},
            'CVE-2021-41773': {'port': 80, 'service': 'http', 'cvss': 7.5, 'exploit': 1, 'year': 2021},
            'CVE-2007-2447': {'port': 139, 'service': 'smb', 'cvss': 9.8, 'exploit': 1, 'year': 2007},
            'CVE-2010-2075': {'port': 6667, 'service': 'irc', 'cvss': 10.0, 'exploit': 1, 'year': 2010},
            'CVE-2006-2369': {'port': 5900, 'service': 'vnc', 'cvss': 7.5, 'exploit': 1, 'year': 2006},
            'CVE-2004-2687': {'port': 3632, 'service': 'distccd', 'cvss': 9.3, 'exploit': 1, 'year': 2004},
        }
    
    def load_model(self):
        """Load or train the model"""
        # Check if saved model exists
        model_file = "data/nn_model.npy"
        data_file = "data/cnn_training_data.json"
        
        try:
            if os.path.exists(model_file) and os.path.exists(data_file):
                # Load training data
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    self.training_data = data.get('training_data', [])
                    self.training_samples = len(self.training_data)
                
                # Load model weights
                weights = np.load(model_file, allow_pickle=True).item()
                self.model = SimpleNeuralNetwork()
                self.model.w1 = weights['w1']
                self.model.b1 = weights['b1']
                self.model.w2 = weights['w2']
                self.model.b2 = weights['b2']
                self.model.trained = True
                self.is_trained = True
                print(f"[CNN] Model loaded from {model_file}")
                return
        except Exception as e:
            print(f"[CNN] Could not load saved model: {e}")
        
        # Generate training data and train
        self._generate_training_data()
        self._train_model()
    
    def _generate_training_data(self):
        """Generate synthetic training data"""
        self.training_data = []
        
        # Positive samples (Vulnerable)
        for cve_id, info in self.cve_db.items():
            for _ in range(10):
                port = info['port'] + random.randint(-3, 3)
                port = max(1, min(65535, port))
                
                service_risk = self.service_risk.get(info['service'], 5) + random.uniform(-0.5, 0.5)
                port_risk = self.port_risk.get(info['port'], 5) + random.uniform(-0.5, 0.5)
                
                features = [
                    max(0, min(10, port_risk)),
                    max(0, min(10, service_risk)),
                    info['cvss'] / 10,
                    info['exploit'],
                    info['year'] / 2025,
                    len(str(info['port'])) / 5,
                    1 if info['port'] in self.port_risk else 0,
                    random.uniform(0.5, 0.9)
                ]
                
                self.training_data.append({
                    'features': features,
                    'label': 1,
                    'cve': cve_id,
                    'port': info['port'],
                    'service': info['service']
                })
        
        # Negative samples (Safe)
        safe_ports = [22, 80, 443, 53, 25, 110, 143, 993, 995, 8080, 8443]
        safe_services = ['ssh', 'http', 'https', 'dns', 'smtp', 'pop3', 'imap', 'imaps', 'pop3s']
        
        for _ in range(50):
            port = random.choice(safe_ports) + random.randint(-2, 2)
            port = max(1, min(65535, port))
            service = random.choice(safe_services)
            
            features = [
                max(0, min(10, self.port_risk.get(port, 3) + random.uniform(-0.3, 0.3))),
                max(0, min(10, self.service_risk.get(service, 3) + random.uniform(-0.3, 0.3))),
                random.uniform(0.1, 0.3),
                0,
                random.uniform(0.8, 1.0),
                len(str(port)) / 5,
                1 if port in self.port_risk else 0,
                random.uniform(0.1, 0.4)
            ]
            
            self.training_data.append({
                'features': features,
                'label': 0,
                'cve': None,
                'port': port,
                'service': service
            })
        
        self.training_samples = len(self.training_data)
        
        # Save training data
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/cnn_training_data.json", 'w') as f:
                json.dump({'training_data': self.training_data}, f, indent=2)
            print(f"[CNN] Generated {self.training_samples} training samples")
        except Exception as e:
            print(f"[CNN] Could not save training data: {e}")
    
    def _train_model(self):
        """Train the neural network"""
        if not self.training_data:
            print("[CNN] No training data available!")
            return
        
        try:
            X = [d['features'] for d in self.training_data]
            y = [d['label'] for d in self.training_data]
            
            # Normalize features
            X = np.array(X)
            X_mean = X.mean(axis=0)
            X_std = X.std(axis=0) + 1e-8
            X = (X - X_mean) / X_std
            
            # Create and train model
            self.model = SimpleNeuralNetwork(input_size=8, hidden_size=20)
            self.model.train(X, y, epochs=300, lr=0.005, verbose=True)
            self.is_trained = True
            
            # Save model
            try:
                weights = {
                    'w1': self.model.w1,
                    'b1': self.model.b1,
                    'w2': self.model.w2,
                    'b2': self.model.b2
                }
                np.save("data/nn_model.npy", weights)
                print("[CNN] Model saved to data/nn_model.npy")
            except Exception as e:
                print(f"[CNN] Could not save model: {e}")
            
        except Exception as e:
            print(f"[CNN] Training error: {e}")
            self.is_trained = False
    
    def predict_vulnerability(self, services):
        """Predict vulnerabilities using the neural network"""
        predictions = []
        
        for svc in services:
            port = svc['port']
            service = svc['service'].lower()
            
            port_risk = self.port_risk.get(port, 5)
            service_risk = self.service_risk.get(service, 5)
            
            # Extract features
            features = np.array([[
                max(0, min(10, port_risk + random.uniform(-0.2, 0.2))),
                max(0, min(10, service_risk + random.uniform(-0.2, 0.2))),
                random.uniform(0.2, 0.6),
                1 if port in self.port_risk else 0,
                2026 / 2025,
                len(str(port)) / 5,
                1 if port in self.port_risk else 0,
                random.uniform(0.4, 0.8)
            ]])
            
            # Normalize features
            if self.is_trained:
                X_mean = np.mean([d['features'] for d in self.training_data], axis=0)
                X_std = np.std([d['features'] for d in self.training_data], axis=0) + 1e-8
                features = (features - X_mean) / X_std
            
            # Predict
            if self.is_trained and self.model:
                prob = float(self.model.predict(features)[0])
                prob = max(0.05, min(0.95, prob))
            else:
                # Fallback prediction
                prob = min(0.95, (port_risk + service_risk) / 25)
            
            # Find matching CVEs
            matched_cves = []
            for cve_id, info in self.cve_db.items():
                if info['service'] == service or info['port'] == port:
                    matched_cves.append({
                        'id': cve_id,
                        'cvss': info['cvss'],
                        'exploit': info['exploit']
                    })
            
            # Calculate risk score
            risk_score = min(100, int(prob * 70 + (port_risk + service_risk) * 2.5))
            risk_score = max(0, min(100, risk_score))
            
            predictions.append({
                'port': port,
                'service': service,
                'vulnerable': prob > 0.45,
                'probability': prob,
                'cves': matched_cves,
                'risk_score': risk_score,
                'model': 'Lightweight NN (NumPy)'
            })
        
        return predictions
    
    def parse_services(self, text):
        """Parse services from scan output"""
        services = []
        pattern = r'(\d+)/tcp\s+open\s+(\S+)\s*(.*?)(?:\n|$)'
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        for port, service, version in matches:
            version = version.strip()
            if version:
                version_parts = version.split()
                version = version_parts[0] if version_parts else version
            
            services.append({
                'port': int(port),
                'service': service.lower(),
                'version': version
            })
        
        return services
    
    def get_scan_output(self):
        """Get scan output from main GUI"""
        if self.output_text_widget:
            try:
                text = self.output_text_widget.get(1.0, tk.END)
                if text and len(text.strip()) > 10:
                    return text
            except:
                pass
        if self.scan_data and isinstance(self.scan_data, str):
            return self.scan_data
        return ""
    
    # ========== UI BUILD ==========
    def build_ui(self):
        self.frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        
        # Header
        header_frame = tk.Frame(self.frame, bg=self.colors['bg_secondary'], height=50)
        header_frame.pack(fill=tk.X, pady=(0, 8))
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🧠 LIGHTWEIGHT NEURAL NETWORK",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_gold'],
            font=('Courier', 13, 'bold')
        ).pack(side=tk.LEFT, padx=15, pady=10)
        
        status_text = "✅ READY (NumPy)" if self.is_trained else "⏳ NOT TRAINED"
        status_color = self.colors['neon_green'] if self.is_trained else self.colors['neon_red']
        
        self.status_label = tk.Label(
            header_frame,
            text=status_text,
            bg=self.colors['bg_secondary'],
            fg=status_color,
            font=('Courier', 9, 'bold')
        )
        self.status_label.pack(side=tk.RIGHT, padx=15, pady=10)
        
        # Info Bar
        info_frame = tk.Frame(self.frame, bg=self.colors['bg_card'])
        info_frame.pack(fill=tk.X, padx=10, pady=(0, 8))
        
        tk.Label(
            info_frame,
            text=f"🧠 Model: 8→20→1 | Samples: {self.training_samples} | No TensorFlow Required | 100% Pure NumPy",
            bg=self.colors['bg_card'],
            fg=self.colors['gray'],
            font=('Courier', 9)
        ).pack(anchor=tk.W, padx=15, pady=6)
        
        # Buttons
        btn_frame = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 8))
        
        self.predict_btn = tk.Button(
            btn_frame,
            text="🧠 PREDICT (NN)",
            command=self.run_prediction,
            bg=self.colors['bg_card'],
            fg=self.colors['neon_purple'],
            font=('Courier', 10, 'bold'),
            padx=20, pady=6,
            cursor='hand2',
            relief=tk.FLAT, bd=1
        )
        self.predict_btn.pack(side=tk.LEFT, padx=3)
        self._add_hover(self.predict_btn, self.colors['neon_purple'])
        
        self.train_btn = tk.Button(
            btn_frame,
            text="🔄 RETRAIN NN",
            command=self.retrain_model,
            bg=self.colors['bg_card'],
            fg=self.colors['neon_cyan'],
            font=('Courier', 9, 'bold'),
            padx=15, pady=6,
            cursor='hand2',
            relief=tk.FLAT, bd=1
        )
        self.train_btn.pack(side=tk.LEFT, padx=3)
        self._add_hover(self.train_btn, self.colors['neon_cyan'])
        
        self.info_btn = tk.Button(
            btn_frame,
            text="📊 MODEL INFO",
            command=self.show_model_info,
            bg=self.colors['bg_card'],
            fg=self.colors['neon_green'],
            font=('Courier', 9, 'bold'),
            padx=15, pady=6,
            cursor='hand2',
            relief=tk.FLAT, bd=1
        )
        self.info_btn.pack(side=tk.LEFT, padx=3)
        self._add_hover(self.info_btn, self.colors['neon_green'])
        
        self.export_btn = tk.Button(
            btn_frame,
            text="💾 EXPORT",
            command=self.export_predictions,
            bg=self.colors['bg_card'],
            fg=self.colors['neon_gold'],
            font=('Courier', 8, 'bold'),
            padx=10, pady=6,
            cursor='hand2',
            relief=tk.FLAT, bd=1,
            state=tk.DISABLED
        )
        self.export_btn.pack(side=tk.LEFT, padx=10)
        self._add_hover(self.export_btn, self.colors['neon_gold'])
        
        # Progress
        progress_frame = tk.Frame(self.frame, bg=self.colors['bg_card'])
        progress_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=300,
            style='Neon.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="",
            bg=self.colors['bg_card'],
            fg=self.colors['gray'],
            font=('Courier', 8)
        )
        self.progress_label.pack(side=tk.LEFT, padx=10)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'Neon.Horizontal.TProgressbar',
            background=self.colors['neon_cyan'],
            troughcolor=self.colors['bg_input'],
            borderwidth=0
        )
        
        # Results
        results_frame = tk.LabelFrame(
            self.frame,
            text="📊 NN ANALYSIS RESULTS",
            bg=self.colors['bg_card'],
            fg=self.colors['neon_cyan'],
            font=('Courier', 10, 'bold')
        )
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 8))
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            bg=self.colors['bg_input'],
            fg=self.colors['white'],
            font=('Courier', 10),
            relief=tk.FLAT, bd=0,
            wrap=tk.WORD,
            insertbackground=self.colors['neon_gold']
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
        
        # Tags
        self.results_text.tag_config('info', foreground=self.colors['neon_cyan'])
        self.results_text.tag_config('success', foreground=self.colors['neon_green'])
        self.results_text.tag_config('warning', foreground=self.colors['neon_gold'])
        self.results_text.tag_config('error', foreground=self.colors['neon_red'])
        self.results_text.tag_config('critical', foreground=self.colors['neon_red'], font=('Courier', 10, 'bold'))
        self.results_text.tag_config('header', foreground=self.colors['neon_purple'], font=('Courier', 11, 'bold'))
        self.results_text.tag_config('cve_id', foreground=self.colors['neon_gold'], font=('Courier', 9, 'bold'))
        self.results_text.tag_config('host', foreground=self.colors['neon_cyan'], font=('Courier', 9, 'bold'))
        
        self.show_initial_message()
    
    def _add_hover(self, button, color):
        def on_enter(e):
            button.config(bg=self.colors['bg_hover'], fg='white')
        def on_leave(e):
            button.config(bg=self.colors['bg_card'], fg=color)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def show_initial_message(self):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🧠 LIGHTWEIGHT NEURAL NETWORK\n", 'header')
        self.results_text.insert(tk.END, "="*60 + "\n\n", 'info')
        self.results_text.insert(tk.END, "✅ No TensorFlow Required!\n", 'success')
        self.results_text.insert(tk.END, "📊 Model Architecture: 8 → 20 → 1\n", 'info')
        self.results_text.insert(tk.END, "📊 Training Samples: {}\n".format(self.training_samples), 'info')
        self.results_text.insert(tk.END, "📊 CVEs Used: {}\n\n".format(len(self.cve_db)), 'info')
        self.results_text.insert(tk.END, "📌 How to use:\n", 'info')
        self.results_text.insert(tk.END, "  1️⃣ Run a scan first (MAIN tab)\n", 'info')
        self.results_text.insert(tk.END, "  2️⃣ Click 'PREDICT (NN)' button\n", 'info')
        self.results_text.insert(tk.END, "  3️⃣ Results will appear here\n\n", 'info')
        self.results_text.insert(tk.END, "📌 Features:\n", 'info')
        self.results_text.insert(tk.END, "  🧠 PREDICT (NN) - Neural Network prediction\n", 'info')
        self.results_text.insert(tk.END, "  🔄 RETRAIN NN - Train model with new data\n", 'info')
        self.results_text.insert(tk.END, "  📊 MODEL INFO - View model architecture\n", 'info')
        self.results_text.insert(tk.END, "  💾 EXPORT - Save predictions\n", 'info')
    
    def run_prediction(self):
        """Run NN prediction"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🧠 NEURAL NETWORK PREDICTION\n", 'header')
        self.results_text.insert(tk.END, "="*60 + "\n\n", 'info')
        
        scan_output = self.get_scan_output()
        
        if not scan_output or len(scan_output.strip()) < 10:
            self.results_text.insert(tk.END, "⚠️ No scan results found!\n", 'error')
            self.results_text.insert(tk.END, "   💡 Run a scan first (MAIN tab)\n", 'warning')
            return
        
        self.progress_bar.start(10)
        self.progress_label.config(text="🧠 Neural Network predicting...")
        self.status_label.config(text="🧠 PREDICTING...", fg=self.colors['neon_gold'])
        self.predict_btn.config(state=tk.DISABLED, text="⏳ PREDICTING...")
        
        def predict():
            try:
                services = self.parse_services(scan_output)
                
                if not services:
                    self.root.after(0, lambda: self.results_text.insert(tk.END, "⚠️ No services found!\n", 'warning'))
                    return
                
                self.root.after(0, lambda: self.results_text.insert(tk.END, f"📊 Services Found: {len(services)}\n\n", 'header'))
                
                self.predictions = self.predict_vulnerability(services)
                
                self.root.after(0, lambda: self._display_predictions())
                self.root.after(0, lambda: self.export_btn.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.status_label.config(text="✅ PREDICTION COMPLETE", fg=self.colors['neon_green']))
                
            except Exception as e:
                self.root.after(0, lambda: self.results_text.insert(tk.END, f"\n❌ Error: {str(e)}\n", 'error'))
            finally:
                self.root.after(0, lambda: self.progress_bar.stop())
                self.root.after(0, lambda: self.progress_label.config(text=""))
                self.root.after(0, lambda: self.predict_btn.config(state=tk.NORMAL, text="🧠 PREDICT (NN)"))
        
        threading.Thread(target=predict, daemon=True).start()
    
    def _display_predictions(self):
        """Display predictions in UI"""
        vulnerable_count = sum(1 for p in self.predictions if p['vulnerable'])
        
        self.results_text.insert(tk.END, "📊 PREDICTION SUMMARY\n", 'header')
        self.results_text.insert(tk.END, "-"*60 + "\n\n", 'info')
        self.results_text.insert(tk.END, f"   • Model: Lightweight NN (NumPy)\n", 'info')
        self.results_text.insert(tk.END, f"   • Total Services: {len(self.predictions)}\n", 'info')
        self.results_text.insert(tk.END, f"   • Vulnerable: {vulnerable_count}\n", 'critical' if vulnerable_count > 0 else 'success')
        self.results_text.insert(tk.END, f"   • Status: {'✅ Trained' if self.is_trained else '⚠️ Fallback'}\n", 'info')
        self.results_text.insert(tk.END, "\n" + "="*60 + "\n\n", 'info')
        
        if not self.predictions:
            self.results_text.insert(tk.END, "✅ No services to analyze!\n", 'success')
            return
        
        sorted_preds = sorted(self.predictions, key=lambda x: x['risk_score'], reverse=True)
        
        self.results_text.insert(tk.END, "🔮 PREDICTIONS\n", 'header')
        self.results_text.insert(tk.END, "-"*60 + "\n\n", 'info')
        
        for pred in sorted_preds[:20]:
            risk = pred['risk_score']
            port = pred['port']
            service = pred['service'].upper()
            vulnerable = pred['vulnerable']
            prob = pred['probability']
            
            if vulnerable and risk >= 70:
                icon = "🔴"
                tag = 'critical'
            elif vulnerable and risk >= 50:
                icon = "🟠"
                tag = 'error'
            elif vulnerable:
                icon = "🟡"
                tag = 'warning'
            else:
                icon = "🟢"
                tag = 'success'
            
            self.results_text.insert(tk.END, f"{icon} Port {port} - {service}\n", 'host')
            self.results_text.insert(tk.END, f"   📊 Risk Score: {risk}/100\n", tag)
            self.results_text.insert(tk.END, f"   📈 Probability: {prob:.1%}\n", tag)
            self.results_text.insert(tk.END, f"   🎯 Vulnerable: {'✅ YES' if vulnerable else '❌ NO'}\n", tag)
            
            if pred.get('cves'):
                self.results_text.insert(tk.END, f"   📌 CVEs:\n", 'info')
                for cve in pred['cves'][:3]:
                    self.results_text.insert(tk.END, f"      • {cve.get('id', 'Unknown')} (CVSS: {cve.get('cvss', 'N/A')})\n", 'cve_id')
                    if cve.get('exploit'):
                        self.results_text.insert(tk.END, f"        🚨 EXPLOIT AVAILABLE\n", 'critical')
            
            self.results_text.insert(tk.END, "   " + "-"*40 + "\n", 'info')
        
        if len(sorted_preds) > 20:
            self.results_text.insert(tk.END, f"\n   ... and {len(sorted_preds) - 20} more\n", 'info')
    
    def retrain_model(self):
        """Retrain the neural network"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🔄 RETRAINING NEURAL NETWORK\n", 'header')
        self.results_text.insert(tk.END, "="*60 + "\n\n", 'info')
        
        self.progress_bar.start(10)
        self.progress_label.config(text="🔄 Retraining...")
        self.status_label.config(text="🔄 TRAINING...", fg=self.colors['neon_gold'])
        self.train_btn.config(state=tk.DISABLED, text="⏳ TRAINING...")
        
        def train():
            try:
                self.results_text.insert(tk.END, "📊 Generating training data...\n", 'info')
                self._generate_training_data()
                
                self.results_text.insert(tk.END, "📊 Training neural network...\n", 'info')
                self.results_text.insert(tk.END, "   ⏳ This may take 10-20 seconds...\n", 'info')
                
                self._train_model()
                
                if self.is_trained:
                    self.root.after(0, lambda: self.results_text.insert(tk.END, "\n✅ Neural Network retrained successfully!\n", 'success'))
                    self.root.after(0, lambda: self.results_text.insert(tk.END, f"   📊 Training Samples: {self.training_samples}\n", 'info'))
                    self.root.after(0, lambda: self.results_text.insert(tk.END, f"   📊 CVEs Used: {len(self.cve_db)}\n", 'info'))
                    self.root.after(0, lambda: self.status_label.config(text="✅ TRAINED", fg=self.colors['neon_green']))
                else:
                    self.root.after(0, lambda: self.results_text.insert(tk.END, "\n❌ Training failed!\n", 'error'))
                
            except Exception as e:
                self.root.after(0, lambda: self.results_text.insert(tk.END, f"\n❌ Error: {str(e)}\n", 'error'))
            finally:
                self.root.after(0, lambda: self.progress_bar.stop())
                self.root.after(0, lambda: self.progress_label.config(text=""))
                self.root.after(0, lambda: self.train_btn.config(state=tk.NORMAL, text="🔄 RETRAIN NN"))
        
        threading.Thread(target=train, daemon=True).start()
    
    def show_model_info(self):
        """Show model information"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "📊 NEURAL NETWORK INFO\n", 'header')
        self.results_text.insert(tk.END, "="*60 + "\n\n", 'info')
        
        self.results_text.insert(tk.END, "📊 MODEL ARCHITECTURE\n", 'header')
        self.results_text.insert(tk.END, "-"*60 + "\n\n", 'info')
        self.results_text.insert(tk.END, "   🧠 Type: Feedforward Neural Network\n", 'info')
        self.results_text.insert(tk.END, "   📊 Layers:\n", 'info')
        self.results_text.insert(tk.END, "      • Input Layer (8 features)\n", 'info')
        self.results_text.insert(tk.END, "      • Hidden Layer (20 neurons, ReLU)\n", 'info')
        self.results_text.insert(tk.END, "      • Output Layer (1 neuron, Sigmoid)\n", 'info')
        self.results_text.insert(tk.END, "   🔧 Activation: ReLU (Hidden) + Sigmoid (Output)\n", 'info')
        self.results_text.insert(tk.END, "   📉 Optimizer: Gradient Descent\n", 'info')
        self.results_text.insert(tk.END, "   💻 Framework: Pure NumPy\n", 'info')
        
        self.results_text.insert(tk.END, "\n📊 TRAINING INFO\n", 'header')
        self.results_text.insert(tk.END, "-"*60 + "\n\n", 'info')
        self.results_text.insert(tk.END, f"   • Training Samples: {self.training_samples}\n", 'info')
        self.results_text.insert(tk.END, f"   • CVEs Used: {len(self.cve_db)}\n", 'info')
        self.results_text.insert(tk.END, f"   • Model Status: {'✅ Trained' if self.is_trained else '❌ Not Trained'}\n", 'info')
        self.results_text.insert(tk.END, f"   • TensorFlow: ❌ Not Required\n", 'info')
        self.results_text.insert(tk.END, f"   • Features: 8\n", 'info')
        
        self.results_text.insert(tk.END, "\n📊 FEATURES\n", 'header')
        self.results_text.insert(tk.END, "-"*60 + "\n\n", 'info')
        self.results_text.insert(tk.END, "   1. port_risk - Port risk level (0-10)\n", 'info')
        self.results_text.insert(tk.END, "   2. service_risk - Service risk level (0-10)\n", 'info')
        self.results_text.insert(tk.END, "   3. cvss - CVSS score normalized\n", 'info')
        self.results_text.insert(tk.END, "   4. exploit - Exploit available? (0/1)\n", 'info')
        self.results_text.insert(tk.END, "   5. year - CVE year normalized\n", 'info')
        self.results_text.insert(tk.END, "   6. port_len - Port number length\n", 'info')
        self.results_text.insert(tk.END, "   7. known_port - Known port? (0/1)\n", 'info')
        self.results_text.insert(tk.END, "   8. confidence - Confidence factor\n", 'info')
    
    def export_predictions(self):
        """Export predictions to JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"nn_predictions_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'model': 'Lightweight NN (NumPy)',
                    'trained': self.is_trained,
                    'samples': self.training_samples,
                    'predictions': self.predictions[:50]
                }, f, indent=2)
            
            self.results_text.insert(tk.END, f"\n✅ Exported: {filename}\n", 'success')
            messagebox.showinfo("Success", f"NN predictions exported to:\n{filename}")
            
        except Exception as e:
            self.results_text.insert(tk.END, f"\n❌ Export error: {e}\n", 'error')
    
    def update_scan_data(self, scan_data):
        self.scan_data = scan_data
        if isinstance(scan_data, str):
            self.scan_output_text = scan_data
    
    def show(self):
        if not self.is_loaded:
            self.build_ui()
            self.is_loaded = True
        
        if self.frame:
            self.frame.pack(fill=tk.BOTH, expand=True)
            self.show_initial_message()
