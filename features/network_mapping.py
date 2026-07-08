#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌐 NETWORK MAPPING v2.0 - COMPLETE FIXED VERSION
✅ NameError 'e' fixed
✅ root attribute fixed
✅ Single STOP button for all scans
✅ Fast scan 5-30 seconds
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import re
import os
import json
import time
from datetime import datetime
from collections import defaultdict

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_features_manager import AIFeatureBase


class NetworkMappingFeature(AIFeatureBase):
    
    def __init__(self, parent, colors, output_text_widget=None):
        super().__init__(parent, colors, output_text_widget)
        
        # ========== ROOT REFERENCE ==========
        self.root = parent.winfo_toplevel() if parent else None
        
        self.scan_output_text = ""
        self.discovered_hosts = []
        self.trace_hops = []
        self.dependencies = {}
        self.attack_surface = []
        self.live_hosts = {}
        
        # Status flags
        self.is_discovering = False
        self.is_tracing = False
        self.is_tracking = False
        
        # Processes
        self.discover_process = None
        self.trace_process = None
        self.track_thread = None
        
        self.cache_file = "data/network_cache.json"
        
        # Service dependencies
        self.service_dependencies = {
            'http': ['mysql', 'postgresql', 'redis', 'mongodb'],
            'https': ['mysql', 'postgresql', 'redis', 'mongodb'],
            'mysql': ['dns'],
            'postgresql': ['dns'],
            'dns': [],
            'smtp': ['dns'],
            'ssh': [],
            'ftp': [],
            'smb': ['dns'],
        }
        
        # Attack vectors
        self.attack_vectors = {
            '21': {'service': 'FTP', 'vectors': ['Anonymous Login', 'Bruteforce'], 'risk': 'HIGH'},
            '22': {'service': 'SSH', 'vectors': ['User Enumeration', 'Bruteforce'], 'risk': 'HIGH'},
            '23': {'service': 'Telnet', 'vectors': ['Plain Text Auth'], 'risk': 'CRITICAL'},
            '25': {'service': 'SMTP', 'vectors': ['Open Relay', 'Spam'], 'risk': 'HIGH'},
            '53': {'service': 'DNS', 'vectors': ['Cache Poisoning'], 'risk': 'HIGH'},
            '80': {'service': 'HTTP', 'vectors': ['Directory Traversal', 'SQL Injection'], 'risk': 'HIGH'},
            '139': {'service': 'NetBIOS', 'vectors': ['SMB RCE', 'EternalBlue'], 'risk': 'CRITICAL'},
            '443': {'service': 'HTTPS', 'vectors': ['Heartbleed', 'Weak Ciphers'], 'risk': 'HIGH'},
            '445': {'service': 'SMB', 'vectors': ['EternalBlue', 'SMBGhost'], 'risk': 'CRITICAL'},
            '512': {'service': 'Rexec', 'vectors': ['Unrestricted Execution'], 'risk': 'CRITICAL'},
            '513': {'service': 'Rlogin', 'vectors': ['Unrestricted Login'], 'risk': 'CRITICAL'},
            '514': {'service': 'Rshell', 'vectors': ['Unrestricted Shell'], 'risk': 'CRITICAL'},
            '1524': {'service': 'bindshell', 'vectors': ['BACKDOOR', 'Root Shell'], 'risk': 'CRITICAL'},
            '3306': {'service': 'MySQL', 'vectors': ['Auth Bypass', 'SQL Injection'], 'risk': 'HIGH'},
            '3389': {'service': 'RDP', 'vectors': ['BlueKeep', 'Bruteforce'], 'risk': 'CRITICAL'},
            '5432': {'service': 'PostgreSQL', 'vectors': ['RCE', 'Auth Bypass'], 'risk': 'HIGH'},
            '5900': {'service': 'VNC', 'vectors': ['Weak Auth', 'Bruteforce'], 'risk': 'HIGH'},
            '6000': {'service': 'X11', 'vectors': ['Keylogging', 'Screen Capture'], 'risk': 'HIGH'},
            '6667': {'service': 'IRC', 'vectors': ['Backdoor', 'Botnet C2'], 'risk': 'CRITICAL'},
        }
        
        self.load_cache()
        print("[Network Mapping] Loaded successfully")
    
    def load_cache(self):
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    self.discovered_hosts = data.get('hosts', [])
        except:
            pass
    
    def save_cache(self):
        try:
            os.makedirs("data", exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump({'hosts': self.discovered_hosts, 'updated': datetime.now().isoformat()}, f, indent=2)
        except:
            pass
    
    # ========== BUILD UI ==========
    def build_ui(self):
        self.frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        
        # Header
        header_frame = tk.Frame(self.frame, bg=self.colors['bg_secondary'], height=45)
        header_frame.pack(fill=tk.X, pady=(0, 8))
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🌐 NETWORK MAPPING v2.0",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_gold'],
            font=('Courier', 13, 'bold')
        ).pack(side=tk.LEFT, padx=15, pady=10)
        
        self.status_label = tk.Label(
            header_frame,
            text="🟢 READY",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_green'],
            font=('Courier', 9, 'bold')
        )
        self.status_label.pack(side=tk.RIGHT, padx=15, pady=10)
        
        # ========== INPUT SECTION ==========
        input_frame = tk.Frame(self.frame, bg=self.colors['bg_card'])
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 8))
        
        tk.Label(
            input_frame,
            text="🎯 Target:",
            bg=self.colors['bg_card'],
            fg=self.colors['neon_cyan'],
            font=('Courier', 9, 'bold')
        ).pack(side=tk.LEFT, padx=10, pady=8)
        
        self.target_entry = tk.Entry(
            input_frame,
            width=30,
            bg=self.colors['bg_input'],
            fg=self.colors['white'],
            font=('Courier', 10),
            relief=tk.FLAT, bd=0
        )
        self.target_entry.pack(side=tk.LEFT, padx=8, pady=8)
        self.target_entry.insert(0, "192.168.159.0/24")
        
        # Presets
        presets = [
            ("/24", "192.168.159.0/24"),
            ("/24", "192.168.1.0/24"),
            ("IP", "8.8.8.8"),
        ]
        for label, value in presets:
            btn = tk.Button(
                input_frame,
                text=label,
                command=lambda v=value: self.target_entry.delete(0, tk.END) or self.target_entry.insert(0, v),
                bg=self.colors['bg_hover'],
                fg=self.colors['gray'],
                font=('Courier', 7),
                padx=6, pady=2,
                cursor='hand2',
                relief=tk.FLAT, bd=0
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        tk.Label(
            input_frame,
            text="💡 Examples: 192.168.1.0/24 | 192.168.1.1",
            bg=self.colors['bg_card'],
            fg=self.colors['gray'],
            font=('Courier', 8)
        ).pack(side=tk.RIGHT, padx=10)
        
        # ========== BUTTONS ==========
        btn_frame = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 8))
        
        # Feature Buttons
        buttons = [
            ("🌐 DISCOVER", self.discover_hosts, self.colors['neon_cyan']),
            ("🗺️ TOPOLOGY", self.trace_topology, self.colors['neon_gold']),
            ("🔗 DEPENDENCIES", self.analyze_dependencies, self.colors['neon_purple']),
            ("🎯 ATTACK SURFACE", self.analyze_attack_surface, self.colors['neon_red']),
            ("📡 LIVE TRACK", self.start_live_tracking, self.colors['neon_green']),
        ]
        
        for text, cmd, color in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                command=cmd,
                bg=self.colors['bg_card'],
                fg=color,
                font=('Courier', 9, 'bold'),
                padx=12, pady=5,
                cursor='hand2',
                relief=tk.FLAT, bd=1
            )
            btn.pack(side=tk.LEFT, padx=3)
            self._add_hover(btn, color)
        
        # ========== SINGLE STOP BUTTON ==========
        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹ STOP ALL",
            command=self.stop_all_scans,
            bg=self.colors['bg_card'],
            fg=self.colors['neon_red'],
            font=('Courier', 9, 'bold'),
            padx=15, pady=5,
            cursor='hand2',
            relief=tk.FLAT, bd=1,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        self._add_hover(self.stop_btn, self.colors['neon_red'])
        
        self.export_btn = tk.Button(
            btn_frame,
            text="💾 EXPORT",
            command=self.export_network_data,
            bg=self.colors['bg_card'],
            fg=self.colors['neon_gold'],
            font=('Courier', 8, 'bold'),
            padx=10, pady=5,
            cursor='hand2',
            relief=tk.FLAT, bd=1,
            state=tk.DISABLED
        )
        self.export_btn.pack(side=tk.LEFT, padx=3)
        self._add_hover(self.export_btn, self.colors['neon_gold'])
        
        # ========== PROGRESS ==========
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
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'Neon.Horizontal.TProgressbar',
            background=self.colors['neon_cyan'],
            troughcolor=self.colors['bg_input'],
            borderwidth=0
        )
        
        # ========== RESULTS ==========
        results_frame = tk.LabelFrame(
            self.frame,
            text="📊 RESULTS",
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
        self.results_text.tag_config('host', foreground=self.colors['neon_cyan'], font=('Courier', 9, 'bold'))
        self.results_text.tag_config('hop', foreground=self.colors['neon_gold'], font=('Courier', 9, 'bold'))
        
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
        self.results_text.insert(tk.END, "🌐 NETWORK MAPPING v2.0\n", 'header')
        self.results_text.insert(tk.END, "="*60 + "\n\n", 'info')
        self.results_text.insert(tk.END, "📌 How to use:\n\n", 'info')
        self.results_text.insert(tk.END, "  1️⃣ Enter target IP or Subnet\n", 'info')
        self.results_text.insert(tk.END, "  2️⃣ Click any feature button\n", 'info')
        self.results_text.insert(tk.END, "  3️⃣ Use ⏹ STOP ALL to cancel\n", 'info')
        self.results_text.insert(tk.END, "  4️⃣ Results appear here\n\n", 'info')
        self.results_text.insert(tk.END, "📌 Features:\n", 'info')
        self.results_text.insert(tk.END, "  🌐 DISCOVER - Find live hosts\n", 'info')
        self.results_text.insert(tk.END, "  🗺️ TOPOLOGY - Trace network path\n", 'info')
        self.results_text.insert(tk.END, "  🔗 DEPENDENCIES - Service deps\n", 'info')
        self.results_text.insert(tk.END, "  🎯 ATTACK SURFACE - Attack vectors\n", 'info')
        self.results_text.insert(tk.END, "  📡 LIVE TRACK - Real-time monitor\n", 'info')
    
    def get_scan_output(self):
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
    
    # ========== SINGLE STOP BUTTON ==========
    def stop_all_scans(self):
        """⏹ STOP ALL - एक ही बटन से सब रोके"""
        
        # Stop Discover
        if self.is_discovering:
            self.is_discovering = False
            if self.discover_process:
                try:
                    self.discover_process.terminate()
                    time.sleep(0.3)
                    if self.discover_process.poll() is None:
                        self.discover_process.kill()
                except:
                    pass
            self._safe_insert("⏹️ Discover stopped\n", 'warning')
        
        # Stop Trace
        if self.is_tracing:
            self.is_tracing = False
            if self.trace_process:
                try:
                    self.trace_process.terminate()
                except:
                    pass
            self._safe_insert("⏹️ Topology stopped\n", 'warning')
        
        # Stop Live Track
        if self.is_tracking:
            self.is_tracking = False
            self._safe_insert("⏹️ Live tracking stopped\n", 'warning')
        
        # Cleanup all
        self._reset_ui()
        self.status_label.config(text="⏹️ STOPPED", fg=self.colors['neon_red'])
    
    def _safe_insert(self, text, tag='info'):
        """Safely insert text into results"""
        try:
            if self.results_text:
                self.results_text.insert(tk.END, text, tag)
                self.results_text.see(tk.END)
        except:
            pass
    
    def _reset_ui(self):
        """Reset UI after stop"""
        self.is_discovering = False
        self.is_tracing = False
        self.is_tracking = False
        self.discover_process = None
        self.trace_process = None
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_bar.stop()
        self.progress_label.config(text="")
        
        if self.status_label.cget('text') != "⏹️ STOPPED":
            self.status_label.config(text="✅ READY", fg=self.colors['neon_green'])
    
    # ========== 1. DISCOVER HOSTS ==========
    def discover_hosts(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("No Target", "Please enter IP or Subnet!")
            return
        
        if self.is_discovering:
            return
        
        self.results_text.delete(1.0, tk.END)
        self._safe_insert("🌐 DISCOVER HOSTS\n", 'header')
        self._safe_insert("="*60 + "\n\n", 'info')
        
        self.is_discovering = True
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="🔄 SCANNING...", fg=self.colors['neon_gold'])
        self.progress_bar.start(10)
        self.progress_label.config(text=f"Scanning: {target}")
        
        self._safe_insert(f"📡 Target: {target}\n", 'info')
        self._safe_insert("⏳ Please wait...\n\n", 'info')
        
        def scan():
            try:
                cmd = f"nmap -sn -n --max-rtt-timeout=200ms --min-hostgroup=256 --max-retries=0 --host-timeout=10s {target}"
                self._safe_insert(f"⚡ {cmd}\n\n", 'info')
                
                process = subprocess.Popen(
                    cmd, shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )
                self.discover_process = process
                
                lines = []
                while self.is_discovering:
                    if process.poll() is not None:
                        break
                    try:
                        line = process.stdout.readline()
                        if not line:
                            break
                        if 'Nmap scan report' in line:
                            self._safe_insert(f"   ✅ {line.strip()}\n", 'success')
                        lines.append(line)
                    except:
                        break
                
                stdout, stderr = process.communicate(timeout=5)
                if stdout:
                    lines.append(stdout)
                
                full_output = ''.join(lines)
                hosts = self._parse_hosts(full_output)
                
                if self.is_discovering:
                    self.discovered_hosts = hosts
                    self.save_cache()
                    self._show_discover_results(hosts)
                else:
                    self._safe_insert("\n⏹️ Stopped\n", 'warning')
                
            except Exception as e:
                if self.is_discovering:
                    self._safe_insert(f"\n❌ Error: {str(e)}\n", 'error')
            finally:
                self._discover_done()
        
        threading.Thread(target=scan, daemon=True).start()
    
    def _discover_done(self):
        self.is_discovering = False
        self.discover_process = None
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_bar.stop()
        self.progress_label.config(text="")
        if self.status_label.cget('text') != "⏹️ STOPPED":
            self.status_label.config(text="✅ READY", fg=self.colors['neon_green'])
    
    def _parse_hosts(self, output):
        hosts = []
        ip_pattern = r'Nmap scan report for ([\d.]+)'
        ips = re.findall(ip_pattern, output)
        mac_pattern = r'MAC Address: ([0-9A-F:]+)'
        macs = re.findall(mac_pattern, output, re.IGNORECASE)
        
        for i, ip in enumerate(ips):
            hosts.append({
                'ip': ip,
                'mac': macs[i] if i < len(macs) else 'Unknown',
                'status': 'UP'
            })
        return hosts
    
    def _show_discover_results(self, hosts):
        self._safe_insert("\n" + "="*60 + "\n\n", 'info')
        self._safe_insert("📊 RESULTS\n", 'header')
        self._safe_insert("-"*60 + "\n\n", 'info')
        self._safe_insert(f"   • Total Hosts: {len(hosts)}\n", 'info')
        self._safe_insert("\n" + "="*60 + "\n\n", 'info')
        
        if not hosts:
            self._safe_insert("⚠️ No hosts found!\n", 'warning')
            return
        
        self._safe_insert("🌐 HOST LIST\n", 'header')
        self._safe_insert("-"*60 + "\n\n", 'info')
        
        for host in hosts:
            self._safe_insert(f"   🖥️  {host['ip']}\n", 'host')
            if host['mac'] != 'Unknown':
                self._safe_insert(f"      📍 MAC: {host['mac']}\n", 'info')
            self._safe_insert(f"      ✅ Status: {host['status']}\n\n", 'success')
        
        self.export_btn.config(state=tk.NORMAL)
        self.status_label.config(text="✅ DISCOVER COMPLETE", fg=self.colors['neon_cyan'])
    
    # ========== 2. TOPOLOGY MAP ==========
    def trace_topology(self):
        target = self.target_entry.get().strip()
        if not target:
            target = "8.8.8.8"
        
        if self.is_tracing:
            return
        
        self.results_text.delete(1.0, tk.END)
        self._safe_insert("🗺️ TOPOLOGY MAP\n", 'header')
        self._safe_insert("="*60 + "\n\n", 'info')
        
        self.is_tracing = True
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="🗺️ TRACING...", fg=self.colors['neon_gold'])
        self.progress_bar.start(10)
        self.progress_label.config(text=f"Tracing: {target}")
        
        self._safe_insert(f"📡 Tracing: {target}\n", 'info')
        
        def trace():
            try:
                cmd = f"traceroute -n {target}" if os.name == 'posix' else f"tracert -d {target}"
                
                process = subprocess.Popen(
                    cmd, shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                self.trace_process = process
                stdout, stderr = process.communicate(timeout=30)
                
                if self.is_tracing:
                    self._show_trace_results(stdout)
                else:
                    self._safe_insert("\n⏹️ Stopped\n", 'warning')
                
            except Exception as e:
                self._safe_insert(f"\n❌ Error: {str(e)}\n", 'error')
            finally:
                self._trace_done()
        
        threading.Thread(target=trace, daemon=True).start()
    
    def _trace_done(self):
        self.is_tracing = False
        self.trace_process = None
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_bar.stop()
        self.progress_label.config(text="")
        if self.status_label.cget('text') != "⏹️ STOPPED":
            self.status_label.config(text="🗺️ COMPLETE", fg=self.colors['neon_gold'])
    
    def _show_trace_results(self, output):
        self._safe_insert("\n📊 TRACE RESULTS\n", 'header')
        self._safe_insert("-"*60 + "\n\n", 'info')
        
        lines = output.split('\n')
        found_hops = False
        
        for line in lines:
            if 'ms' in line:
                found_hops = True
                line = line.strip()
                if line:
                    self._safe_insert(f"   {line}\n", 'hop')
        
        if not found_hops:
            self._safe_insert("   No hops found\n", 'warning')
            self._safe_insert("   💡 Try: install traceroute\n", 'info')
        
        self.export_btn.config(state=tk.NORMAL)
    
    # ========== 3. DEPENDENCIES ==========
    def analyze_dependencies(self):
        self.results_text.delete(1.0, tk.END)
        self._safe_insert("🔗 DEPENDENCY MAP\n", 'header')
        self._safe_insert("="*60 + "\n\n", 'info')
        
        scan_output = self.get_scan_output()
        
        if not scan_output or len(scan_output.strip()) < 10:
            self._safe_insert("⚠️ No scan results found!\n", 'error')
            self._safe_insert("   💡 Run a scan first (MAIN tab)\n", 'warning')
            return
        
        services = self.parse_services(scan_output)
        
        if not services:
            self._safe_insert("⚠️ No services found!\n", 'warning')
            return
        
        self.status_label.config(text="🔗 ANALYZING...", fg=self.colors['neon_gold'])
        self.progress_bar.start(10)
        self.progress_label.config(text="Analyzing dependencies...")
        
        self.dependencies = self._build_dependency_graph(services)
        self._show_dependency_results(services)
        
        self.status_label.config(text="🔗 COMPLETE", fg=self.colors['neon_purple'])
        self.progress_bar.stop()
        self.progress_label.config(text="")
        self.export_btn.config(state=tk.NORMAL)
    
    def parse_services(self, text):
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
    
    def _build_dependency_graph(self, services):
        graph = defaultdict(list)
        service_names = [s['service'] for s in services]
        
        for service in services:
            svc = service['service']
            if svc in self.service_dependencies:
                for dep in self.service_dependencies[svc]:
                    if dep in service_names:
                        graph[svc].append(dep)
            else:
                graph[svc] = []
        
        return dict(graph)
    
    def _show_dependency_results(self, services):
        self._safe_insert("📊 SERVICES FOUND\n", 'header')
        self._safe_insert("-"*60 + "\n\n", 'info')
        
        for svc in services:
            self._safe_insert(f"   • Port {svc['port']}: {svc['service']}\n", 'info')
        
        self._safe_insert("\n" + "="*60 + "\n\n", 'info')
        self._safe_insert("🔗 DEPENDENCIES\n", 'header')
        self._safe_insert("-"*60 + "\n\n", 'info')
        
        has_deps = False
        for service, deps in self.dependencies.items():
            if deps:
                has_deps = True
                self._safe_insert(f"   📦 {service.upper()}\n", 'host')
                for dep in deps:
                    self._safe_insert(f"      └──→ {dep.upper()}\n", 'info')
                self._safe_insert("\n", 'info')
        
        if not has_deps:
            self._safe_insert("   ℹ️ No dependencies\n", 'info')
    
    # ========== 4. ATTACK SURFACE ==========
    def analyze_attack_surface(self):
        self.results_text.delete(1.0, tk.END)
        self._safe_insert("🎯 ATTACK SURFACE\n", 'header')
        self._safe_insert("="*60 + "\n\n", 'info')
        
        scan_output = self.get_scan_output()
        
        if not scan_output or len(scan_output.strip()) < 10:
            self._safe_insert("⚠️ No scan results found!\n", 'error')
            self._safe_insert("   💡 Run a scan first (MAIN tab)\n", 'warning')
            return
        
        services = self.parse_services(scan_output)
        
        if not services:
            self._safe_insert("⚠️ No services found!\n", 'warning')
            return
        
        self.status_label.config(text="🎯 ANALYZING...", fg=self.colors['neon_gold'])
        self.progress_bar.start(10)
        self.progress_label.config(text="Analyzing attack surface...")
        
        self.attack_surface = []
        risk_score = 0
        
        for svc in services:
            port_str = str(svc['port'])
            if port_str in self.attack_vectors:
                info = self.attack_vectors[port_str]
                info['port'] = svc['port']
                info['service_actual'] = svc['service']
                self.attack_surface.append(info)
                
                if info['risk'] == 'CRITICAL':
                    risk_score += 10
                elif info['risk'] == 'HIGH':
                    risk_score += 5
                elif info['risk'] == 'MEDIUM':
                    risk_score += 2
        
        risk_score = min(100, risk_score)
        self._show_attack_surface(risk_score)
        
        self.export_btn.config(state=tk.NORMAL)
        self.status_label.config(text="🎯 COMPLETE", fg=self.colors['neon_red'])
        self.progress_bar.stop()
        self.progress_label.config(text="")
    
    def _show_attack_surface(self, risk_score):
        self._safe_insert("📊 SUMMARY\n", 'header')
        self._safe_insert("-"*60 + "\n\n", 'info')
        self._safe_insert(f"   • Attack Vectors: {len(self.attack_surface)}\n", 'info')
        self._safe_insert(f"   • Risk Score: {risk_score}/100\n", 'info')
        
        if risk_score >= 70:
            risk_level = "🔴 CRITICAL"
            risk_tag = 'critical'
        elif risk_score >= 50:
            risk_level = "🟠 HIGH"
            risk_tag = 'error'
        elif risk_score >= 30:
            risk_level = "🟡 MEDIUM"
            risk_tag = 'warning'
        else:
            risk_level = "🟢 LOW"
            risk_tag = 'success'
        
        self._safe_insert(f"   • Risk Level: {risk_level}\n\n", risk_tag)
        self._safe_insert("="*60 + "\n\n", 'info')
        
        if not self.attack_surface:
            self._safe_insert("✅ No attack vectors\n", 'success')
            return
        
        self._safe_insert("🎯 ATTACK VECTORS\n", 'header')
        self._safe_insert("-"*60 + "\n\n", 'info')
        
        risk_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2}
        sorted_vectors = sorted(self.attack_surface, key=lambda x: risk_order.get(x.get('risk', 'LOW'), 3))
        
        for vec in sorted_vectors:
            risk = vec.get('risk', 'UNKNOWN')
            port = vec.get('port', 'Unknown')
            service = vec.get('service', 'Unknown')
            
            icon = '🔴' if risk == 'CRITICAL' else '🟠' if risk == 'HIGH' else '🟡'
            tag = 'critical' if risk == 'CRITICAL' else 'error' if risk == 'HIGH' else 'warning'
            
            self._safe_insert(f"{icon} Port {port} - {service}\n", 'host')
            self._safe_insert(f"   📊 Risk: {risk}\n", tag)
            self._safe_insert("   🎯 Vectors:\n", 'info')
            for v in vec.get('vectors', []):
                self._safe_insert(f"      • {v}\n", 'vector')
            self._safe_insert("\n", 'info')
        
        # Recommendations
        critical_vectors = [v for v in self.attack_surface if v.get('risk') == 'CRITICAL']
        high_vectors = [v for v in self.attack_surface if v.get('risk') == 'HIGH']
        
        self._safe_insert("🎯 RECOMMENDATIONS\n", 'header')
        self._safe_insert("-"*60 + "\n\n", 'info')
        
        if critical_vectors:
            self._safe_insert("🔴 CRITICAL - Fix IMMEDIATELY:\n", 'critical')
            for v in critical_vectors:
                self._safe_insert(f"   • Port {v.get('port')} ({v.get('service')})\n", 'error')
        
        if high_vectors:
            self._safe_insert("\n🟠 HIGH - Fix within 48 hours:\n", 'error')
            for v in high_vectors:
                self._safe_insert(f"   • Port {v.get('port')} ({v.get('service')})\n", 'warning')
    
    # ========== 5. LIVE TRACKING ==========
    def start_live_tracking(self):
        if self.is_tracking:
            self.stop_live_tracking()
            return
        
        default_hosts = ", ".join([h['ip'] for h in self.discovered_hosts[:5]]) if self.discovered_hosts else "8.8.8.8"
        
        import tkinter.simpledialog
        hosts_input = tkinter.simpledialog.askstring(
            "📡 Live Tracking",
            "Enter IPs to track (comma separated):",
            initialvalue=default_hosts
        )
        
        if not hosts_input:
            return
        
        self.results_text.delete(1.0, tk.END)
        self._safe_insert("📡 LIVE TRACKING\n", 'header')
        self._safe_insert("="*60 + "\n\n", 'info')
        
        self.is_tracking = True
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="📡 TRACKING...", fg=self.colors['neon_green'])
        self.progress_bar.start(10)
        self.progress_label.config(text="Tracking...")
        
        self._safe_insert(f"📡 Tracking: {hosts_input}\n", 'info')
        self._safe_insert("⏳ Updates every 5 seconds\n\n", 'info')
        
        def track():
            hosts = [h.strip() for h in hosts_input.split(',') if h.strip()]
            
            while self.is_tracking:
                results = []
                for host in hosts:
                    status = self._ping_host(host)
                    results.append(f"{host}: {'✅ UP' if status else '❌ DOWN'}")
                
                self._update_track_results(results)
                time.sleep(5)
        
        if self.track_thread and self.track_thread.is_alive():
            self.is_tracking = False
            self.track_thread.join(timeout=1)
        
        self.track_thread = threading.Thread(target=track, daemon=True)
        self.track_thread.start()
    
    def stop_live_tracking(self):
        self.is_tracking = False
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="📡 STOPPED", fg=self.colors['neon_gold'])
        self.progress_bar.stop()
        self.progress_label.config(text="")
        self._safe_insert("\n⏹️ Tracking stopped\n", 'warning')
    
    def _ping_host(self, host):
        try:
            param = '-n' if os.name == 'nt' else '-c'
            cmd = ['ping', param, '1', host]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            return result.returncode == 0
        except:
            return False
    
    def _update_track_results(self, results):
        if not self.is_tracking:
            return
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        self._safe_insert(f"🕐 {timestamp}\n", 'header')
        self._safe_insert("-"*40 + "\n", 'info')
        
        for line in results:
            if '✅ UP' in line:
                tag = 'success'
                icon = '🟢'
            else:
                tag = 'error'
                icon = '🔴'
            host = line.split(':')[0].strip()
            self._safe_insert(f"   {icon} {host}\n", tag)
        
        self._safe_insert("\n", 'info')
        self.results_text.see(tk.END)
    
    # ========== EXPORT ==========
    def export_network_data(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"network_mapping_{timestamp}.csv"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Type,IP/Port,Service,Risk,Details\n")
                
                if self.discovered_hosts:
                    for host in self.discovered_hosts:
                        f.write(f"HOST,{host['ip']},,,MAC: {host['mac']}\n")
                
                if self.attack_surface:
                    for vec in self.attack_surface:
                        vectors = ' | '.join(vec.get('vectors', []))
                        f.write(f"ATTACK_VECTOR,Port {vec.get('port')},{vec.get('service')},{vec.get('risk')},{vectors}\n")
            
            self._safe_insert(f"\n✅ Exported: {filename}\n", 'success')
            
        except Exception as e:
            self._safe_insert(f"\n❌ Export error: {str(e)}\n", 'error')
    
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
