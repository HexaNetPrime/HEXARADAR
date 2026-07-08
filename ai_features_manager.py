#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI Features Manager - Updated for 5 Features (ML removed to Tab 8)
"""

import tkinter as tk
from tkinter import ttk
import os
import sys


class AIFeaturesRegistry:
    """AI फीचर्स की रजिस्ट्री"""
    
    def __init__(self):
        self.features = []
        self.current_index = 0
        self.parent_window = None
        self.scan_data = None
        self.feature_frames = {}
        
    def register_feature(self, name, icon, description, module_name, class_name):
        """एक नया AI फीचर register करें"""
        self.features.append({
            'name': name,
            'icon': icon,
            'description': description,
            'module': module_name,
            'class': class_name,
            'enabled': True,
            'frame': None,
            'instance': None
        })
        print(f"[AI Manager] Feature Registered: {icon} {name}")
    
    def get_feature_count(self):
        return len(self.features)
    
    def get_current_feature(self):
        if 0 <= self.current_index < len(self.features):
            return self.features[self.current_index]
        return None
    
    def set_scan_data(self, scan_data):
        self.scan_data = scan_data
        for feature in self.features:
            if feature['instance']:
                try:
                    feature['instance'].update_scan_data(scan_data)
                except:
                    pass


class AIFeaturesManager:
    """AI फीचर्स मैनेजर"""
    
    def __init__(self, parent, output_text_widget=None):
        self.parent = parent
        self.output_text_widget = output_text_widget
        self.registry = AIFeaturesRegistry()
        self.current_frame = None
        self.main_container = None
        
        # Colors
        self.colors = {
            'bg_primary': '#0a0a0f',
            'bg_secondary': '#0f0f1a',
            'bg_card': '#141420',
            'bg_input': '#1a1a2e',
            'bg_hover': '#1f1f3a',
            'neon_gold': '#ffd700',
            'neon_cyan': '#00e5ff',
            'neon_purple': '#9b59ff',
            'neon_pink': '#ff2d95',
            'neon_green': '#00ff88',
            'neon_orange': '#ff6b35',
            'neon_red': '#ff1744',
            'white': '#e8e8f0',
            'gray': '#7a7a9a',
        }
        
        # Register ALL AI Features (5 features - ML removed to Tab 8)
        self._register_features()
        
        # Setup UI
        self.setup_ui()
    
    def _register_features(self):
        """सभी AI फीचर्स register करें"""
        
        # ===== FEATURE 1: Advanced Vuln Prediction =====
        self.registry.register_feature(
            name="Advanced AI Engine",
            icon="🤖",
            description="Vulnerability Prediction + Anomaly Detection + CVE Database + Full AI Report",
            module_name="vuln_prediction",
            class_name="VulnPredictionFeature"
        )
        
        # ===== FEATURE 2: Network Mapping =====
        self.registry.register_feature(
            name="Network Mapping",
            icon="🌐",
            description="Discover Hosts + Topology Map + Dependency Map + Attack Surface + Live Tracking",
            module_name="network_mapping",
            class_name="NetworkMappingFeature"
        )
        
        # ===== FEATURE 3: Advanced Discovery (OSINT) =====
        self.registry.register_feature(
            name="Advanced Discovery",
            icon="🔍",
            description="OSINT Integration + Passive Recon + Email Enumeration + Tech Fingerprint + Cloud Discovery",
            module_name="advanced_discovery",
            class_name="AdvancedDiscoveryFeature"
        )
        
        # ===== FEATURE 4: Data Analytics =====
        self.registry.register_feature(
            name="Data Analytics",
            icon="📊",
            description="Trend Analysis + Risk Scoring + Compliance Check + SLA Monitoring + Predictive Analysis",
            module_name="data_analytics",
            class_name="DataAnalyticsFeature"
        )
        
        # ===== FEATURE 5: Evasion Techniques =====
        self.registry.register_feature(
            name="Evasion Techniques",
            icon="🛡",
            description="Proxy Chains + VPN Rotation + MAC Randomization + Traffic Shaping + IDS/IPS Detection",
            module_name="evasion_techniques",
            class_name="EvasionTechniquesFeature"
        )
        
        # ===== ML Feature REMOVED - Now in Tab 8 =====
        # ML Vulnerability Prediction is now a separate Tab (Tab 8)
        # It is loaded directly in gui.py create_ml_page()
        
        print(f"[AI Manager] Total {self.registry.get_feature_count()} features registered")
    
    def setup_ui(self):
        """Main UI setup"""
        self.main_container = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # ========== FEATURE SELECTION BAR ==========
        self.nav_frame = tk.Frame(self.main_container, bg=self.colors['bg_secondary'], height=40)
        self.nav_frame.pack(fill=tk.X, pady=(0, 5))
        self.nav_frame.pack_propagate(False)
        
        self.feature_buttons = []
        for i, feature in enumerate(self.registry.features):
            btn = tk.Button(
                self.nav_frame,
                text=f"{feature['icon']} {feature['name']}",
                command=lambda idx=i: self.select_feature(idx),
                bg=self.colors['bg_card'] if i == 0 else self.colors['bg_secondary'],
                fg=self.colors['neon_gold'] if i == 0 else self.colors['gray'],
                font=('Courier', 9, 'bold'),
                padx=12, pady=5,
                cursor='hand2',
                relief=tk.FLAT, bd=0
            )
            btn.pack(side=tk.LEFT, padx=3)
            self.feature_buttons.append(btn)
        
        # Content frame
        self.content_frame = tk.Frame(self.main_container, bg=self.colors['bg_primary'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Load first feature
        self.select_feature(0)
    
    def select_feature(self, index):
        """Select and load a feature"""
        if index >= len(self.registry.features):
            return
        
        # Update buttons
        for i, btn in enumerate(self.feature_buttons):
            if i == index:
                btn.config(bg=self.colors['bg_card'], fg=self.colors['neon_gold'])
            else:
                btn.config(bg=self.colors['bg_secondary'], fg=self.colors['gray'])
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Load feature
        feature = self.registry.features[index]
        self.registry.current_index = index
        
        try:
            module_name = f"features.{feature['module']}"
            class_name = feature['class']
            
            module = __import__(module_name, fromlist=[class_name])
            feature_class = getattr(module, class_name)
            
            if feature['instance'] is None:
                feature['instance'] = feature_class(
                    self.content_frame,
                    self.colors,
                    self.output_text_widget
                )
                if self.registry.scan_data:
                    feature['instance'].update_scan_data(self.registry.scan_data)
            
            feature['instance'].show()
            
        except ImportError as e:
            self._show_placeholder(feature, f"Module not found: {e}")
        except Exception as e:
            self._show_placeholder(feature, f"Error: {e}")
    
    def _show_placeholder(self, feature, error_msg=""):
        """Placeholder for missing features"""
        frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            frame,
            text=f"{feature['icon']} {feature['name']}",
            bg=self.colors['bg_primary'],
            fg=self.colors['neon_cyan'],
            font=('Courier', 16, 'bold')
        ).pack(pady=30)
        
        tk.Label(
            frame,
            text="⏳ Coming Soon...",
            bg=self.colors['bg_primary'],
            fg=self.colors['gray'],
            font=('Courier', 12)
        ).pack(pady=10)
        
        if error_msg:
            tk.Label(
                frame,
                text=f"Note: {error_msg}",
                bg=self.colors['bg_primary'],
                fg=self.colors['neon_gold'],
                font=('Courier', 9)
            ).pack(pady=5)
    
    def update_scan_data(self, scan_data):
        """Scan Results को फीचर्स के साथ share करें"""
        self.registry.set_scan_data(scan_data)
        feature = self.registry.get_current_feature()
        if feature and feature['instance']:
            try:
                feature['instance'].update_scan_data(scan_data)
            except:
                pass
    
    def destroy(self):
        """Cleanup"""
        if self.main_container:
            self.main_container.destroy()


class AIFeatureBase:
    """सभी AI फीचर्स के लिए Base Class"""
    
    def __init__(self, parent, colors, output_text_widget=None):
        self.parent = parent
        self.colors = colors
        self.output_text_widget = output_text_widget
        self.scan_data = None
        self.frame = None
        self.is_loaded = False
    
    def show(self):
        if not self.is_loaded:
            self.build_ui()
            self.is_loaded = True
        
        if self.frame:
            self.frame.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        if self.frame:
            self.frame.pack_forget()
    
    def build_ui(self):
        self.frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        tk.Label(
            self.frame,
            text="⚠️ This feature has no UI defined",
            bg=self.colors['bg_primary'],
            fg=self.colors['neon_red'],
            font=('Courier', 12)
        ).pack(pady=50)
    
    def update_scan_data(self, scan_data):
        self.scan_data = scan_data
        self.on_data_updated()
    
    def on_data_updated(self):
        pass
    
    def get_output_text(self):
        if self.output_text_widget:
            return self.output_text_widget.get(1.0, tk.END)
        return ""
