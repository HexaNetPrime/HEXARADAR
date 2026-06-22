#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🛡 EVASION TECHNIQUES v2.0
फीचर्स: Proxy Chains, VPN Rotation, MAC Randomization, Traffic Shaping, IDS/IPS Detection
✅ बिना किसी API के - पूरी तरह से ऑफलाइन
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import re
import os
import json
import time
import random
import socket
from datetime import datetime

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_features_manager import AIFeatureBase


class EvasionTechniquesFeature(AIFeatureBase):
    """
    🛡 Evasion Techniques - Complete Offline Evasion Suite
    """
    
    def __init__(self, parent, colors, output_text_widget=None):
        super().__init__(parent, colors, output_text_widget)
        
        self.root = parent.winfo_toplevel() if parent else None
        
        # Config file
        self.config_file = "data/evasion_config.json"
        self.config = self.load_config()
        
        # Status flags
        self.is_running = False
        self.current_proxy = None
        self.current_vpn = None
        
        # MAC Address info
        self.original_mac = None
        self.current_mac = None
        self.interface = "eth0"  # Default
        
        # Traffic shaping settings
        self.scan_delay = 500  # ms
        self.max_rate = 1000   # packets/sec
        self.min_rate = 100    # packets/sec
        
        print("[Evasion Techniques] Loaded successfully")
    
    def load_config(self):
        """Load config from file"""
        default_config = {
            'proxy': {
                'type': 'socks5',
                'host': '127.0.0.1',
                'port': 9050,
                'enabled': False
            },
            'vpn': {
                'interface': 'tun0',
                'provider': 'OpenVPN',
                'enabled': False
            },
            'mac': {
                'interface': 'eth0',
                'enabled': False
            },
            'traffic': {
                'scan_delay': 500,
                'max_rate': 1000,
                'min_rate': 100,
                'enabled': False
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config
            else:
                os.makedirs("data", exist_ok=True)
                with open(self.config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except:
            return default_config
    
    def save_config(self):
        """Save config to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
    
    def _safe_insert(self, text, tag='info'):
        try:
            if self.results_text:
                self.results_text.insert(tk.END, text, tag)
                self.results_text.see(tk.END)
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
            text="🛡 EVASION TECHNIQUES v2.0",
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
        
        # ========== 5 FEATURE SECTIONS ==========
        
        # 1. Proxy Chains
        self._build_proxy_section()
        
        # 2. VPN Rotation
        self._build_vpn_section()
        
        # 3. MAC Randomization
        self._build_mac_section()
        
        # 4. Traffic Shaping
        self._build_traffic_section()
        
        # 5. IDS/IPS Detection
        self._build_ids_section()
        
        # ========== RESULTS ==========
        results_frame = tk.LabelFrame(
            self.frame,
            text="📊 EVASION RESULTS",
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
        
        self.show_initial_message()
    
    def _build_proxy_section(self):
        """Proxy Chains Section"""
        frame = tk.LabelFrame(self.frame, text="🌐 PROXY CHAINS", bg=self.colors['bg_card'],
                              fg=self.colors['neon_cyan'], font=('Courier', 9, 'bold'))
        frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # Proxy Type
        tk.Label(frame, text="Type:", bg=self.colors['bg_card'], fg=self.colors['white'],
                font=('Courier', 8)).pack(side=tk.LEFT, padx=10, pady=5)
        
        self.proxy_type_var = tk.StringVar(value="socks5")
        proxy_types = ['socks5', 'socks4', 'http', 'https']
        for pt in proxy_types:
            rb = tk.Radiobutton(frame, text=pt.upper(), variable=self.proxy_type_var,
                                value=pt, bg=self.colors['bg_card'], fg=self.colors['gray'],
                                selectcolor=self.colors['bg_card'], font=('Courier', 8))
            rb.pack(side=tk.LEFT, padx=3)
        
        # Proxy Host
        tk.Label(frame, text="Host:", bg=self.colors['bg_card'], fg=self.colors['white'],
                font=('Courier', 8)).pack(side=tk.LEFT, padx=10, pady=5)
        self.proxy_host_entry = tk.Entry(frame, width=15, bg=self.colors['bg_input'],
                                         fg=self.colors['white'], font=('Courier', 8))
        self.proxy_host_entry.pack(side=tk.LEFT, padx=3, pady=5)
        self.proxy_host_entry.insert(0, "127.0.0.1")
        
        # Proxy Port
        tk.Label(frame, text="Port:", bg=self.colors['bg_card'], fg=self.colors['white'],
                font=('Courier', 8)).pack(side=tk.LEFT, padx=10, pady=5)
        self.proxy_port_entry = tk.Entry(frame, width=8, bg=self.colors['bg_input'],
                                         fg=self.colors['white'], font=('Courier', 8))
        self.proxy_port_entry.pack(side=tk.LEFT, padx=3, pady=5)
        self.proxy_port_entry.insert(0, "9050")
        
        # Buttons
        self.proxy_enable_btn = tk.Button(frame, text="▶ ENABLE", command=self.enable_proxy,
                                          bg=self.colors['bg_card'], fg=self.colors['neon_green'],
                                          font=('Courier', 7, 'bold'), padx=8, pady=3,
                                          cursor='hand2', relief=tk.FLAT, bd=1)
        self.proxy_enable_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.proxy_disable_btn = tk.Button(frame, text="⏹ DISABLE", command=self.disable_proxy,
                                           bg=self.colors['bg_card'], fg=self.colors['neon_red'],
                                           font=('Courier', 7, 'bold'), padx=8, pady=3,
                                           cursor='hand2', relief=tk.FLAT, bd=1,
                                           state=tk.DISABLED)
        self.proxy_disable_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.proxy_status = tk.Label(frame, text="⭕ Inactive", bg=self.colors['bg_card'],
                                     fg=self.colors['gray'], font=('Courier', 8))
        self.proxy_status.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def _build_vpn_section(self):
        """VPN Rotation Section"""
        frame = tk.LabelFrame(self.frame, text="🔒 VPN ROTATION", bg=self.colors['bg_card'],
                              fg=self.colors['neon_gold'], font=('Courier', 9, 'bold'))
        frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        tk.Label(frame, text="Interface:", bg=self.colors['bg_card'], fg=self.colors['white'],
                font=('Courier', 8)).pack(side=tk.LEFT, padx=10, pady=5)
        self.vpn_interface_entry = tk.Entry(frame, width=10, bg=self.colors['bg_input'],
                                            fg=self.colors['white'], font=('Courier', 8))
        self.vpn_interface_entry.pack(side=tk.LEFT, padx=3, pady=5)
        self.vpn_interface_entry.insert(0, "tun0")
        
        tk.Label(frame, text="Provider:", bg=self.colors['bg_card'], fg=self.colors['white'],
                font=('Courier', 8)).pack(side=tk.LEFT, padx=10, pady=5)
        self.vpn_provider_entry = tk.Entry(frame, width=12, bg=self.colors['bg_input'],
                                           fg=self.colors['white'], font=('Courier', 8))
        self.vpn_provider_entry.pack(side=tk.LEFT, padx=3, pady=5)
        self.vpn_provider_entry.insert(0, "OpenVPN")
        
        self.vpn_check_btn = tk.Button(frame, text="🔍 CHECK STATUS", command=self.check_vpn_status,
                                       bg=self.colors['bg_card'], fg=self.colors['neon_cyan'],
                                       font=('Courier', 7, 'bold'), padx=8, pady=3,
                                       cursor='hand2', relief=tk.FLAT, bd=1)
        self.vpn_check_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.vpn_rotate_btn = tk.Button(frame, text="🔄 ROTATE VPN", command=self.rotate_vpn,
                                        bg=self.colors['bg_card'], fg=self.colors['neon_gold'],
                                        font=('Courier', 7, 'bold'), padx=8, pady=3,
                                        cursor='hand2', relief=tk.FLAT, bd=1)
        self.vpn_rotate_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.vpn_status = tk.Label(frame, text="⭕ Not Connected", bg=self.colors['bg_card'],
                                   fg=self.colors['gray'], font=('Courier', 8))
        self.vpn_status.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def _build_mac_section(self):
        """MAC Randomization Section"""
        frame = tk.LabelFrame(self.frame, text="🔧 MAC RANDOMIZATION", bg=self.colors['bg_card'],
                              fg=self.colors['neon_pink'], font=('Courier', 9, 'bold'))
        frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        tk.Label(frame, text="Interface:", bg=self.colors['bg_card'], fg=self.colors['white'],
                font=('Courier', 8)).pack(side=tk.LEFT, padx=10, pady=5)
        self.mac_interface_entry = tk.Entry(frame, width=10, bg=self.colors['bg_input'],
                                            fg=self.colors['white'], font=('Courier', 8))
        self.mac_interface_entry.pack(side=tk.LEFT, padx=3, pady=5)
        self.mac_interface_entry.insert(0, "eth0")
        
        self.mac_random_btn = tk.Button(frame, text="🔀 RANDOMIZE MAC", command=self.randomize_mac,
                                        bg=self.colors['bg_card'], fg=self.colors['neon_pink'],
                                        font=('Courier', 7, 'bold'), padx=8, pady=3,
                                        cursor='hand2', relief=tk.FLAT, bd=1)
        self.mac_random_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.mac_restore_btn = tk.Button(frame, text="↩️ RESTORE MAC", command=self.restore_mac,
                                         bg=self.colors['bg_card'], fg=self.colors['neon_gold'],
                                         font=('Courier', 7, 'bold'), padx=8, pady=3,
                                         cursor='hand2', relief=tk.FLAT, bd=1,
                                         state=tk.DISABLED)
        self.mac_restore_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.mac_status = tk.Label(frame, text="📌 Original: Not Set", bg=self.colors['bg_card'],
                                   fg=self.colors['gray'], font=('Courier', 8))
        self.mac_status.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def _build_traffic_section(self):
        """Traffic Shaping Section"""
        frame = tk.LabelFrame(self.frame, text="📊 TRAFFIC SHAPING", bg=self.colors['bg_card'],
                              fg=self.colors['neon_green'], font=('Courier', 9, 'bold'))
        frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # Scan Delay
        tk.Label(frame, text="Scan Delay (ms):", bg=self.colors['bg_card'], fg=self.colors['white'],
                font=('Courier', 8)).pack(side=tk.LEFT, padx=10, pady=5)
        self.delay_entry = tk.Entry(frame, width=6, bg=self.colors['bg_input'],
                                    fg=self.colors['white'], font=('Courier', 8))
        self.delay_entry.pack(side=tk.LEFT, padx=3, pady=5)
        self.delay_entry.insert(0, "500")
        
        tk.Label(frame, text="Max Rate (pkts/sec):", bg=self.colors['bg_card'], fg=self.colors['white'],
                font=('Courier', 8)).pack(side=tk.LEFT, padx=10, pady=5)
        self.max_rate_entry = tk.Entry(frame, width=6, bg=self.colors['bg_input'],
                                       fg=self.colors['white'], font=('Courier', 8))
        self.max_rate_entry.pack(side=tk.LEFT, padx=3, pady=5)
        self.max_rate_entry.insert(0, "1000")
        
        self.traffic_apply_btn = tk.Button(frame, text="✅ APPLY SHAPING", command=self.apply_traffic_shaping,
                                           bg=self.colors['bg_card'], fg=self.colors['neon_green'],
                                           font=('Courier', 7, 'bold'), padx=8, pady=3,
                                           cursor='hand2', relief=tk.FLAT, bd=1)
        self.traffic_apply_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.traffic_status = tk.Label(frame, text="⭕ Shaping Off", bg=self.colors['bg_card'],
                                       fg=self.colors['gray'], font=('Courier', 8))
        self.traffic_status.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def _build_ids_section(self):
        """IDS/IPS Detection Section"""
        frame = tk.LabelFrame(self.frame, text="🕵️ IDS/IPS DETECTION", bg=self.colors['bg_card'],
                              fg=self.colors['neon_orange'], font=('Courier', 9, 'bold'))
        frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        tk.Label(frame, text="Target:", bg=self.colors['bg_card'], fg=self.colors['white'],
                font=('Courier', 8)).pack(side=tk.LEFT, padx=10, pady=5)
        self.ids_target_entry = tk.Entry(frame, width=20, bg=self.colors['bg_input'],
                                         fg=self.colors['white'], font=('Courier', 8))
        self.ids_target_entry.pack(side=tk.LEFT, padx=3, pady=5)
        self.ids_target_entry.insert(0, "192.168.159.128")
        
        self.ids_scan_btn = tk.Button(frame, text="🔍 DETECT IDS/IPS", command=self.detect_ids_ips,
                                      bg=self.colors['bg_card'], fg=self.colors['neon_orange'],
                                      font=('Courier', 7, 'bold'), padx=8, pady=3,
                                      cursor='hand2', relief=tk.FLAT, bd=1)
        self.ids_scan_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.ids_status = tk.Label(frame, text="⭕ Not Scanned", bg=self.colors['bg_card'],
                                   fg=self.colors['gray'], font=('Courier', 8))
        self.ids_status.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def show_initial_message(self):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🛡 EVASION TECHNIQUES v2.0\n", 'header')
        self.results_text.insert(tk.END, "="*60 + "\n\n", 'info')
        self.results_text.insert(tk.END, "📌 Features:\n\n", 'info')
        self.results_text.insert(tk.END, "  🌐 PROXY - Use Tor/SOCKS5/HTTP proxy\n", 'info')
        self.results_text.insert(tk.END, "  🔒 VPN - Check and rotate VPN\n", 'info')
        self.results_text.insert(tk.END, "  🔧 MAC - Randomize MAC address\n", 'info')
        self.results_text.insert(tk.END, "  📊 TRAFFIC - Shape packet rate\n", 'info')
        self.results_text.insert(tk.END, "  🕵️ IDS - Detect Firewall/IDS\n\n", 'info')
        self.results_text.insert(tk.END, "💡 Use these techniques to evade detection during scans.\n", 'info')
    
    # ========== 1. PROXY CHAINS ==========
    def enable_proxy(self):
        """Enable proxy"""
        proxy_type = self.proxy_type_var.get()
        host = self.proxy_host_entry.get().strip()
        port = self.proxy_port_entry.get().strip()
        
        if not host or not port:
            messagebox.showwarning("Warning", "Please enter proxy host and port!")
            return
        
        try:
            port = int(port)
        except:
            messagebox.showwarning("Warning", "Invalid port number!")
            return
        
        self.config['proxy']['type'] = proxy_type
        self.config['proxy']['host'] = host
        self.config['proxy']['port'] = port
        self.config['proxy']['enabled'] = True
        self.save_config()
        
        self.current_proxy = f"{proxy_type}://{host}:{port}"
        self.proxy_status.config(text=f"🟢 Active: {self.current_proxy}", fg=self.colors['neon_green'])
        self.proxy_enable_btn.config(state=tk.DISABLED)
        self.proxy_disable_btn.config(state=tk.NORMAL)
        
        self._safe_insert(f"🌐 Proxy Enabled: {self.current_proxy}\n", 'success')
        self._safe_insert(f"   Nmap Flag: --proxies {proxy_type}://{host}:{port}\n", 'info')
        self._safe_insert(f"   Use in Nmap: nmap --proxies {proxy_type}://{host}:{port} <target>\n\n", 'info')
    
    def disable_proxy(self):
        """Disable proxy"""
        self.config['proxy']['enabled'] = False
        self.save_config()
        
        self.current_proxy = None
        self.proxy_status.config(text="⭕ Inactive", fg=self.colors['gray'])
        self.proxy_enable_btn.config(state=tk.NORMAL)
        self.proxy_disable_btn.config(state=tk.DISABLED)
        
        self._safe_insert("🌐 Proxy Disabled\n", 'warning')
    
    # ========== 2. VPN ROTATION ==========
    def check_vpn_status(self):
        """Check VPN status"""
        self._safe_insert("🔒 VPN STATUS CHECK\n", 'header')
        self._safe_insert("-"*40 + "\n", 'info')
        
        interface = self.vpn_interface_entry.get().strip()
        
        try:
            # Check if interface exists
            result = subprocess.run(['ip', 'addr', 'show', interface], capture_output=True, text=True)
            if result.returncode == 0:
                self.vpn_status.config(text="🟢 Connected", fg=self.colors['neon_green'])
                self._safe_insert(f"   ✅ VPN Interface: {interface} - UP\n", 'success')
                
                # Get IP
                ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout)
                if ip_match:
                    ip = ip_match.group(1)
                    self._safe_insert(f"   📍 VPN IP: {ip}\n", 'info')
            else:
                self.vpn_status.config(text="🔴 Not Connected", fg=self.colors['neon_red'])
                self._safe_insert(f"   ❌ VPN Interface: {interface} - DOWN\n", 'error')
        except:
            self.vpn_status.config(text="⚠️ Error", fg=self.colors['neon_red'])
            self._safe_insert(f"   ❌ Failed to check VPN status\n", 'error')
        
        self._safe_insert("\n", 'info')
    
    def rotate_vpn(self):
        """Rotate VPN connection"""
        self._safe_insert("🔄 VPN ROTATION\n", 'header')
        self._safe_insert("-"*40 + "\n", 'info')
        
        interface = self.vpn_interface_entry.get().strip()
        provider = self.vpn_provider_entry.get().strip()
        
        self._safe_insert(f"   🔄 Rotating {provider} VPN on {interface}\n", 'info')
        self._safe_insert("   💡 This will restart the VPN connection\n", 'info')
        
        # Simulate VPN rotation
        self.vpn_status.config(text="🔄 Rotating...", fg=self.colors['neon_gold'])
        self.vpn_rotate_btn.config(state=tk.DISABLED, text="⏳ ROTATING...")
        
        def rotate():
            try:
                # Try to restart VPN (OpenVPN/WireGuard)
                if 'openvpn' in provider.lower():
                    subprocess.run(['sudo', 'systemctl', 'restart', 'openvpn'], capture_output=True)
                elif 'wireguard' in provider.lower():
                    subprocess.run(['sudo', 'wg-quick', 'down', interface], capture_output=True)
                    time.sleep(1)
                    subprocess.run(['sudo', 'wg-quick', 'up', interface], capture_output=True)
                
                time.sleep(2)
                
                # Check new IP
                result = subprocess.run(['curl', '-s', 'ifconfig.me'], capture_output=True, text=True)
                if result.stdout:
                    self.root.after(0, lambda: self._safe_insert(f"   ✅ New IP: {result.stdout.strip()}\n", 'success'))
                
                self.root.after(0, lambda: self.vpn_status.config(text="🟢 Connected (Rotated)", fg=self.colors['neon_green']))
                self.root.after(0, lambda: self._safe_insert("   ✅ VPN Rotated Successfully!\n", 'success'))
                
            except Exception as e:
                self.root.after(0, lambda: self._safe_insert(f"   ❌ Rotation failed: {e}\n", 'error'))
                self.root.after(0, lambda: self.vpn_status.config(text="⚠️ Error", fg=self.colors['neon_red']))
            
            finally:
                self.root.after(0, lambda: self.vpn_rotate_btn.config(state=tk.NORMAL, text="🔄 ROTATE VPN"))
                self.root.after(0, lambda: self._safe_insert("\n", 'info'))
        
        threading.Thread(target=rotate, daemon=True).start()
    
    # ========== 3. MAC RANDOMIZATION ==========
    def randomize_mac(self):
        """Randomize MAC address"""
        self._safe_insert("🔧 MAC RANDOMIZATION\n", 'header')
        self._safe_insert("-"*40 + "\n", 'info')
        
        interface = self.mac_interface_entry.get().strip()
        
        # Get original MAC
        try:
            result = subprocess.run(['ip', 'link', 'show', interface], capture_output=True, text=True)
            mac_match = re.search(r'link/ether ([0-9a-f:]+)', result.stdout)
            if mac_match:
                self.original_mac = mac_match.group(1)
                self._safe_insert(f"   📌 Original MAC: {self.original_mac}\n", 'info')
        except:
            pass
        
        # Generate random MAC
        random_mac = self._generate_random_mac()
        self._safe_insert(f"   🔀 New MAC: {random_mac}\n", 'info')
        
        # Apply MAC change
        try:
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'], capture_output=True)
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'address', random_mac], capture_output=True)
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'], capture_output=True)
            
            self.current_mac = random_mac
            self.mac_status.config(text=f"🔀 New: {random_mac}", fg=self.colors['neon_pink'])
            self.mac_random_btn.config(state=tk.DISABLED)
            self.mac_restore_btn.config(state=tk.NORMAL)
            
            self._safe_insert("   ✅ MAC Randomization Successful!\n", 'success')
        except Exception as e:
            self._safe_insert(f"   ❌ Failed: {e}\n", 'error')
            self._safe_insert("   💡 Requires sudo privileges\n", 'warning')
        
        self._safe_insert("\n", 'info')
    
    def _generate_random_mac(self):
        """Generate random MAC address"""
        mac = [0x02, 0x00, 0x00,
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0xff),
               random.randint(0x00, 0xff)]
        return ':'.join(map(lambda x: "%02x" % x, mac))
    
    def restore_mac(self):
        """Restore original MAC"""
        self._safe_insert("↩️ RESTORE MAC\n", 'header')
        self._safe_insert("-"*40 + "\n", 'info')
        
        if not self.original_mac:
            self._safe_insert("   ❌ No original MAC found!\n", 'error')
            return
        
        interface = self.mac_interface_entry.get().strip()
        
        try:
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'], capture_output=True)
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'address', self.original_mac], capture_output=True)
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'], capture_output=True)
            
            self.current_mac = self.original_mac
            self.mac_status.config(text=f"📌 Restored: {self.original_mac}", fg=self.colors['gray'])
            self.mac_random_btn.config(state=tk.NORMAL)
            self.mac_restore_btn.config(state=tk.DISABLED)
            
            self._safe_insert(f"   ✅ MAC Restored: {self.original_mac}\n", 'success')
        except Exception as e:
            self._safe_insert(f"   ❌ Failed: {e}\n", 'error')
        
        self._safe_insert("\n", 'info')
    
    # ========== 4. TRAFFIC SHAPING ==========
    def apply_traffic_shaping(self):
        """Apply traffic shaping settings"""
        self._safe_insert("📊 TRAFFIC SHAPING\n", 'header')
        self._safe_insert("-"*40 + "\n", 'info')
        
        try:
            delay = int(self.delay_entry.get().strip())
            max_rate = int(self.max_rate_entry.get().strip())
        except:
            self._safe_insert("   ❌ Invalid input! Use numbers only.\n", 'error')
            return
        
        self.scan_delay = delay
        self.max_rate = max_rate
        
        self.config['traffic']['scan_delay'] = delay
        self.config['traffic']['max_rate'] = max_rate
        self.config['traffic']['enabled'] = True
        self.save_config()
        
        self.traffic_status.config(text=f"🟢 Delay: {delay}ms, Max: {max_rate}pkt/s", fg=self.colors['neon_green'])
        
        self._safe_insert(f"   ✅ Traffic Shaping Applied\n", 'success')
        self._safe_insert(f"   📊 Scan Delay: {delay}ms\n", 'info')
        self._safe_insert(f"   📊 Max Rate: {max_rate} packets/sec\n", 'info')
        self._safe_insert(f"   💡 Nmap Flags: --scan-delay {delay}ms --max-rate {max_rate}\n", 'info')
        self._safe_insert(f"   💡 Example: nmap --scan-delay {delay}ms --max-rate {max_rate} <target>\n", 'info')
        self._safe_insert("\n", 'info')
    
    # ========== 5. IDS/IPS DETECTION ==========
    def detect_ids_ips(self):
        """Detect IDS/IPS"""
        target = self.ids_target_entry.get().strip()
        if not target:
            messagebox.showwarning("Warning", "Please enter a target!")
            return
        
        self._safe_insert("🕵️ IDS/IPS DETECTION\n", 'header')
        self._safe_insert("="*60 + "\n\n", 'info')
        
        self.ids_scan_btn.config(state=tk.DISABLED, text="⏳ SCANNING...")
        self.ids_status.config(text="🔄 Scanning...", fg=self.colors['neon_gold'])
        self.status_label.config(text="🕵️ SCANNING...", fg=self.colors['neon_gold'])
        
        self._safe_insert(f"📡 Target: {target}\n", 'info')
        self._safe_insert("⏳ Detecting IDS/IPS...\n\n", 'info')
        
        def scan():
            results = []
            
            # 1. ACK Scan (Detect stateful firewall)
            try:
                self._safe_insert("🔍 ACK Scan (Detect Stateful Firewall)\n", 'header')
                self._safe_insert("-"*40 + "\n", 'info')
                
                cmd = f"nmap -sA -p 22,80,443,445 {target}"
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate(timeout=30)
                
                if 'filtered' in stdout.lower():
                    self._safe_insert("   ⚠️ Filtered ports detected - Stateful firewall present\n", 'warning')
                    results.append("Stateful Firewall Detected")
                else:
                    self._safe_insert("   ✅ No filtering detected - No stateful firewall\n", 'success')
                    results.append("No Stateful Firewall")
                
                # Count filtered ports
                filtered_count = len(re.findall(r'filtered', stdout, re.IGNORECASE))
                if filtered_count > 0:
                    self._safe_insert(f"   📊 Filtered Ports: {filtered_count}\n", 'info')
                
            except Exception as e:
                self._safe_insert(f"   ❌ ACK Scan error: {e}\n", 'error')
            
            # 2. SYN Scan (Detect IDS)
            try:
                self._safe_insert("\n🔍 SYN Scan (Detect IDS)\n", 'header')
                self._safe_insert("-"*40 + "\n", 'info')
                
                cmd = f"nmap -sS -p 22,80,443,445 --max-retries 0 {target}"
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate(timeout=30)
                
                if 'filtered' in stdout.lower():
                    self._safe_insert("   ⚠️ Filtered ports - IDS/IPS may be active\n", 'warning')
                    results.append("IDS/IPS Active")
                else:
                    self._safe_insert("   ✅ No filtering - IDS/IPS likely inactive\n", 'success')
                    results.append("IDS/IPS Inactive")
                
            except Exception as e:
                self._safe_insert(f"   ❌ SYN Scan error: {e}\n", 'error')
            
            # 3. Summary
            self._safe_insert("\n📊 IDS/IPS DETECTION SUMMARY\n", 'header')
            self._safe_insert("="*60 + "\n\n", 'info')
            
            if "Stateful Firewall Detected" in results:
                self._safe_insert("   🔴 Stateful Firewall: PRESENT\n", 'error')
            else:
                self._safe_insert("   🟢 Stateful Firewall: NOT DETECTED\n", 'success')
            
            if "IDS/IPS Active" in results:
                self._safe_insert("   🔴 IDS/IPS: ACTIVE\n", 'error')
                self._safe_insert("\n   💡 Recommendations:\n", 'info')
                self._safe_insert("   • Use --scan-delay to slow down\n", 'info')
                self._safe_insert("   • Use --max-rate to limit packets\n", 'info')
                self._safe_insert("   • Use --proxies to route through Tor\n", 'info')
                self._safe_insert("   • Use -f to fragment packets\n", 'info')
            else:
                self._safe_insert("   🟢 IDS/IPS: NOT DETECTED\n", 'success')
            
            self.root.after(0, lambda: self._ids_done())
        
        threading.Thread(target=scan, daemon=True).start()
    
    def _ids_done(self):
        self.ids_scan_btn.config(state=tk.NORMAL, text="🔍 DETECT IDS/IPS")
        self.ids_status.config(text="✅ Scan Complete", fg=self.colors['neon_green'])
        self.status_label.config(text="🕵️ IDS DETECTION COMPLETE", fg=self.colors['neon_orange'])
        self._safe_insert("\n✅ IDS/IPS Detection Complete\n", 'success')
    
    # ========== UPDATE ==========
    def update_scan_data(self, scan_data):
        self.scan_data = scan_data
    
    def show(self):
        if not self.is_loaded:
            self.build_ui()
            self.is_loaded = True
        
        if self.frame:
            self.frame.pack(fill=tk.BOTH, expand=True)
            self.show_initial_message()
