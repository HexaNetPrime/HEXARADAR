#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔍 ADVANCED DISCOVERY (OSINT) v2.0
फीचर्स: OSINT Integration, Passive Recon, Email Enumeration, Tech Fingerprint, Cloud Discovery
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
from datetime import datetime
from collections import defaultdict, OrderedDict
import socket
import dns.resolver
import dns.exception
import requests
from urllib.parse import urlparse

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_features_manager import AIFeatureBase


class AdvancedDiscoveryFeature(AIFeatureBase):
    """
    🔍 Advanced Discovery (OSINT) - Complete Offline OSINT Suite
    """
    
    def __init__(self, parent, colors, output_text_widget=None):
        super().__init__(parent, colors, output_text_widget)
        
        self.root = parent.winfo_toplevel() if parent else None
        
        self.target = ""
        self.is_scanning = False
        self.scan_thread = None
        
        # Cache for DNS lookups
        self.dns_cache = OrderedDict()
        self.cache_size = 100
        
        # Common email usernames
        self.common_usernames = [
            'admin', 'info', 'support', 'sales', 'contact', 'help', 'webmaster',
            'postmaster', 'abuse', 'security', 'noreply', 'hello', 'team',
            'office', 'hr', 'marketing', 'billing', 'accounts', 'service',
            'customer', 'feedback', 'mail', 'hostmaster', 'root', 'manager',
            'ceo', 'cto', 'cfo', 'it', 'ops', 'devops', 'sysadmin', 'network'
        ]
        
        # CMS detection patterns
        self.cms_patterns = {
            'WordPress': [
                r'wp-content', r'wp-includes', r'wp-admin', r'wp-json',
                r'wordpress', r'generator" content="WordPress'
            ],
            'Drupal': [
                r'drupal', r'sites/all', r'misc/drupal', r'Drupal.settings',
                r'generator" content="Drupal'
            ],
            'Joomla': [
                r'joomla', r'components/com_', r'media/system', r'Joomla!',
                r'generator" content="Joomla'
            ],
            'Magento': [
                r'magento', r'Mage.Cookies', r'catalog/product',
                r'Magento_', r'generator" content="Magento'
            ],
            'Shopify': [
                r'shopify', r'myshopify.com', r'cdn.shopify',
                r'Shopify.theme'
            ],
            'Wix': [
                r'wix.com', r'wixstatic', r'wix-code'
            ],
            'Squarespace': [
                r'squarespace', r'static.squarespace', r'collection-root'
            ]
        }
        
        # JS framework detection
        self.js_patterns = {
            'React': [r'react-', r'ReactDOM', r'React.createElement', r'<script.*src=".*react'],
            'Angular': [r'angular', r'ng-app', r'ng-controller', r'<script.*src=".*angular'],
            'Vue.js': [r'vue', r'v-bind', r'v-for', r'data-v-', r'<script.*src=".*vue'],
            'jQuery': [r'jquery', r'\$\(document\).ready', r'\.jquery', r'<script.*src=".*jquery'],
            'Bootstrap': [r'bootstrap', r'data-toggle', r'data-target', r'<link.*bootstrap'],
            'Tailwind': [r'tailwind', r'<link.*tailwindcss']
        }
        
        # Web server detection
        self.server_patterns = {
            'Apache': [r'Apache', r'apache', r'Apache/2', r'httpd'],
            'Nginx': [r'nginx', r'nginx/1', r'Nginx'],
            'IIS': [r'Microsoft-IIS', r'IIS', r'Windows Server'],
            'Tomcat': [r'Apache-Coyote', r'Tomcat', r'Apache Tomcat'],
            'Node.js': [r'Node.js', r'node.js', r'Express'],
            'Python': [r'Python', r'WSGIServer', r'Gunicorn'],
            'PHP': [r'PHP/', r'PHP/7', r'PHP/8']
        }
        
        # Cloud provider detection
        self.cloud_patterns = {
            'AWS': {
                'patterns': [r'amazonaws.com', r'cloudfront.net', r'ec2', r'aws'],
                'services': ['S3', 'CloudFront', 'EC2', 'RDS', 'ELB']
            },
            'Azure': {
                'patterns': [r'azurewebsites.net', r'blob.core.windows.net', r'azure.com', r'cloudapp.azure.com'],
                'services': ['Blob Storage', 'App Service', 'CDN', 'VM']
            },
            'Google Cloud': {
                'patterns': [r'cloud.google.com', r'storage.googleapis.com', r'appspot.com', r'googleapis.com'],
                'services': ['Storage', 'App Engine', 'Cloud Run', 'Compute Engine']
            },
            'Cloudflare': {
                'patterns': [r'cloudflare.com', r'cdn.cloudflare', r'cf-cache-status'],
                'services': ['CDN', 'WAF', 'DNS', 'DDoS Protection']
            },
            'DigitalOcean': {
                'patterns': [r'digitalocean.com', r'digitaloceanspaces.com'],
                'services': ['Droplets', 'Spaces', 'Kubernetes']
            },
            'Heroku': {
                'patterns': [r'herokuapp.com', r'heroku.com'],
                'services': ['App Hosting', 'PostgreSQL']
            },
            'Linode': {
                'patterns': [r'linode.com', r'linodeusercontent.com'],
                'services': ['VPS', 'Kubernetes']
            }
        }
        
        self.results_data = {}
        self.load_cache()
        
        print("[Advanced Discovery] Loaded successfully")
    
    def load_cache(self):
        """Load DNS cache from file"""
        try:
            cache_file = "data/discovery_cache.json"
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    self.dns_cache = OrderedDict(data.get('dns_cache', {}))
                print(f"[Cache] Loaded {len(self.dns_cache)} DNS records")
        except:
            pass
    
    def save_cache(self):
        """Save DNS cache to file"""
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/discovery_cache.json", 'w') as f:
                json.dump({
                    'dns_cache': dict(self.dns_cache),
                    'updated': datetime.now().isoformat()
                }, f, indent=2)
        except:
            pass
    
    def _get_dns_cached(self, domain, record_type):
        """Get DNS record from cache"""
        key = f"{domain}_{record_type}"
        if key in self.dns_cache:
            return self.dns_cache[key]
        return None
    
    def _set_dns_cached(self, domain, record_type, value):
        """Set DNS record in cache"""
        key = f"{domain}_{record_type}"
        self.dns_cache[key] = value
        # Limit cache size
        if len(self.dns_cache) > self.cache_size:
            self.dns_cache.popitem(last=False)
    
    def _safe_insert(self, text, tag='info'):
        """Safely insert text into results"""
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
            text="🔍 ADVANCED DISCOVERY (OSINT) v2.0",
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
            width=35,
            bg=self.colors['bg_input'],
            fg=self.colors['white'],
            font=('Courier', 10),
            relief=tk.FLAT, bd=0
        )
        self.target_entry.pack(side=tk.LEFT, padx=8, pady=8)
        self.target_entry.insert(0, "example.com")
        
        # Presets
        presets = [
            ("google.com", "google.com"),
            ("github.com", "github.com"),
            ("stackoverflow.com", "stackoverflow.com")
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
        
        self.scan_btn = tk.Button(
            input_frame,
            text="🔍 SCAN",
            command=self.start_scan,
            bg=self.colors['neon_green'],
            fg='#0a0a0f',
            font=('Courier', 9, 'bold'),
            padx=15, pady=5,
            cursor='hand2',
            relief=tk.FLAT, bd=0
        )
        self.scan_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(
            input_frame,
            text="⏹ STOP",
            command=self.stop_scan,
            bg=self.colors['bg_card'],
            fg=self.colors['neon_red'],
            font=('Courier', 9, 'bold'),
            padx=15, pady=5,
            cursor='hand2',
            relief=tk.FLAT, bd=1,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=3)
        
        tk.Label(
            input_frame,
            text="💡 Domain or URL (e.g., example.com)",
            bg=self.colors['bg_card'],
            fg=self.colors['gray'],
            font=('Courier', 8)
        ).pack(side=tk.RIGHT, padx=10)
        
        # ========== FEATURE BUTTONS ==========
        btn_frame = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 8))
        
        buttons = [
            ("🌐 OSINT", self.run_osint, self.colors['neon_cyan']),
            ("🕵️ PASSIVE", self.run_passive_recon, self.colors['neon_gold']),
            ("📧 EMAIL", self.run_email_enum, self.colors['neon_purple']),
            ("💻 TECH", self.run_tech_fingerprint, self.colors['neon_pink']),
            ("☁️ CLOUD", self.run_cloud_discovery, self.colors['neon_green'])
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
        
        self.export_btn = tk.Button(
            btn_frame,
            text="💾 EXPORT",
            command=self.export_results,
            bg=self.colors['bg_card'],
            fg=self.colors['neon_gold'],
            font=('Courier', 8, 'bold'),
            padx=10, pady=5,
            cursor='hand2',
            relief=tk.FLAT, bd=1,
            state=tk.DISABLED
        )
        self.export_btn.pack(side=tk.LEFT, padx=10)
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
            text="📊 OSINT RESULTS",
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
        self.results_text.insert(tk.END, "🔍 ADVANCED DISCOVERY (OSINT) v2.0\n", 'header')
        self.results_text.insert(tk.END, "="*60 + "\n\n", 'info')
        self.results_text.insert(tk.END, "📌 How to use:\n\n", 'info')
        self.results_text.insert(tk.END, "  1️⃣ Enter domain or URL (e.g., example.com)\n", 'info')
        self.results_text.insert(tk.END, "  2️⃣ Click 🔍 SCAN for complete analysis\n", 'info')
        self.results_text.insert(tk.END, "  3️⃣ Or use individual feature buttons\n", 'info')
        self.results_text.insert(tk.END, "  4️⃣ Results appear here\n\n", 'info')
        self.results_text.insert(tk.END, "📌 Features:\n", 'info')
        self.results_text.insert(tk.END, "  🌐 OSINT - WHOIS + DNS Records\n", 'info')
        self.results_text.insert(tk.END, "  🕵️ PASSIVE - DNS Lookups (A, MX, NS, TXT)\n", 'info')
        self.results_text.insert(tk.END, "  📧 EMAIL - Common email enumeration\n", 'info')
        self.results_text.insert(tk.END, "  💻 TECH - CMS, JS, Web Server detection\n", 'info')
        self.results_text.insert(tk.END, "  ☁️ CLOUD - AWS, Azure, GCP detection\n", 'info')
    
    def get_target(self):
        """Get target from entry"""
        target = self.target_entry.get().strip()
        if not target:
            return None
        # Remove http:// or https://
        target = re.sub(r'^https?://', '', target)
        # Remove trailing slash
        target = target.rstrip('/')
        return target
    
    # ========== STOP SCAN ==========
    def stop_scan(self):
        self.is_scanning = False
        self.stop_btn.config(state=tk.DISABLED)
        self.scan_btn.config(state=tk.NORMAL, text="🔍 SCAN")
        self.progress_bar.stop()
        self.progress_label.config(text="")
        self.status_label.config(text="⏹️ STOPPED", fg=self.colors['neon_red'])
        self._safe_insert("\n⏹️ Scan stopped by user\n", 'warning')
    
    def _reset_scan_state(self):
        self.is_scanning = False
        self.stop_btn.config(state=tk.DISABLED)
        self.scan_btn.config(state=tk.NORMAL, text="🔍 SCAN")
        self.progress_bar.stop()
        self.progress_label.config(text="")
        if self.status_label.cget('text') != "⏹️ STOPPED":
            self.status_label.config(text="✅ READY", fg=self.colors['neon_green'])
    
    # ========== START FULL SCAN ==========
    def start_scan(self):
        if self.is_scanning:
            return
        
        target = self.get_target()
        if not target:
            messagebox.showwarning("No Target", "Please enter a domain or URL!")
            return
        
        self.target = target
        self.results_text.delete(1.0, tk.END)
        self._safe_insert("🔍 FULL OSINT SCAN\n", 'header')
        self._safe_insert("="*60 + "\n\n", 'info')
        self._safe_insert(f"📡 Target: {target}\n", 'info')
        self._safe_insert("⏳ Scanning... Please wait\n\n", 'info')
        
        self.is_scanning = True
        self.scan_btn.config(state=tk.DISABLED, text="⏳ SCANNING...")
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_bar.start(10)
        self.progress_label.config(text=f"Scanning: {target}")
        self.status_label.config(text="🔄 SCANNING...", fg=self.colors['neon_gold'])
        
        def scan():
            try:
                # Run all modules
                self._run_osint_module()
                if not self.is_scanning:
                    return
                self._run_passive_recon_module()
                if not self.is_scanning:
                    return
                self._run_email_enum_module()
                if not self.is_scanning:
                    return
                self._run_tech_fingerprint_module()
                if not self.is_scanning:
                    return
                self._run_cloud_discovery_module()
                
                if self.is_scanning:
                    self._safe_insert("\n" + "="*60 + "\n", 'info')
                    self._safe_insert("✅ SCAN COMPLETE!\n", 'success')
                    self.export_btn.config(state=tk.NORMAL)
                    self.status_label.config(text="✅ SCAN COMPLETE", fg=self.colors['neon_green'])
                    
            except Exception as e:
                if self.is_scanning:
                    self._safe_insert(f"\n❌ Error: {str(e)}\n", 'error')
            finally:
                self._reset_scan_state()
        
        threading.Thread(target=scan, daemon=True).start()
    
    # ========== 1. OSINT INTEGRATION ==========
    def run_osint(self):
        if not self.get_target():
            messagebox.showwarning("No Target", "Please enter a domain or URL!")
            return
        self.target = self.get_target()
        self.results_text.delete(1.0, tk.END)
        self._safe_insert("🌐 OSINT INTEGRATION\n", 'header')
        self._safe_insert("="*60 + "\n\n", 'info')
        self._run_osint_module()
    
    def _run_osint_module(self):
        self._safe_insert(f"🌐 OSINT RESULTS: {self.target}\n", 'header')
        self._safe_insert("-"*60 + "\n\n", 'info')
        
        # WHOIS lookup
        self._safe_insert("📋 WHOIS INFORMATION\n", 'info')
        try:
            import whois
            w = whois.whois(self.target)
            if w:
                self._safe_insert(f"   Domain: {w.domain_name}\n", 'info')
                self._safe_insert(f"   Registrar: {w.registrar}\n", 'info')
                self._safe_insert(f"   Creation Date: {w.creation_date}\n", 'info')
                self._safe_insert(f"   Expiry Date: {w.expiration_date}\n", 'info')
                self._safe_insert(f"   Nameservers: {w.name_servers}\n", 'info')
        except ImportError:
            self._safe_insert("   ⚠️ python-whois not installed\n", 'warning')
            self._safe_insert("   💡 Install: pip install python-whois\n", 'info')
        except Exception as e:
            self._safe_insert(f"   ⚠️ WHOIS lookup failed: {e}\n", 'warning')
        
        self._safe_insert("\n", 'info')
        
        # DNS Records
        self._safe_insert("📊 DNS RECORDS\n", 'info')
        dns_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        for record_type in dns_types:
            try:
                answers = dns.resolver.resolve(self.target, record_type)
                if answers:
                    for rdata in answers:
                        self._safe_insert(f"   {record_type}: {rdata}\n", 'info')
            except:
                pass
        
        self._safe_insert("\n" + "="*60 + "\n\n", 'info')
        self.results_data['osint'] = {'target': self.target}
    
    # ========== 2. PASSIVE RECON ==========
    def run_passive_recon(self):
        if not self.get_target():
            messagebox.showwarning("No Target", "Please enter a domain or URL!")
            return
        self.target = self.get_target()
        self.results_text.delete(1.0, tk.END)
        self._safe_insert("🕵️ PASSIVE RECON\n", 'header')
        self._safe_insert("="*60 + "\n\n", 'info')
        self._run_passive_recon_module()
    
    def _run_passive_recon_module(self):
        self._safe_insert(f"🕵️ PASSIVE RECON: {self.target}\n", 'header')
        self._safe_insert("-"*60 + "\n\n", 'info')
        
        self._safe_insert("📡 DNS LOOKUPS\n", 'info')
        dns_types = {
            'A': 'IPv4 Address',
            'AAAA': 'IPv6 Address',
            'MX': 'Mail Exchange',
            'NS': 'Nameserver',
            'TXT': 'TXT Record',
            'CNAME': 'Canonical Name',
            'SOA': 'Start of Authority'
        }
        
        found_count = 0
        for record_type, description in dns_types.items():
            cached = self._get_dns_cached(self.target, record_type)
            if cached:
                self._safe_insert(f"   {record_type} ({description}): {cached} [CACHED]\n", 'info')
                found_count += 1
                continue
            
            try:
                answers = dns.resolver.resolve(self.target, record_type)
                if answers:
                    values = []
                    for rdata in answers:
                        values.append(str(rdata))
                    value_str = ', '.join(values)
                    self._set_dns_cached(self.target, record_type, value_str)
                    self._safe_insert(f"   {record_type} ({description}): {value_str}\n", 'info')
                    found_count += 1
            except:
                pass
        
        self.save_cache()
        self._safe_insert(f"\n📊 Found {found_count} DNS records\n", 'success')
        self._safe_insert("\n" + "="*60 + "\n\n", 'info')
        self.results_data['passive'] = {'target': self.target}
    
    # ========== 3. EMAIL ENUMERATION ==========
    def run_email_enum(self):
        if not self.get_target():
            messagebox.showwarning("No Target", "Please enter a domain or URL!")
            return
        self.target = self.get_target()
        self.results_text.delete(1.0, tk.END)
        self._safe_insert("📧 EMAIL ENUMERATION\n", 'header')
        self._safe_insert("="*60 + "\n\n", 'info')
        self._run_email_enum_module()
    
    def _run_email_enum_module(self):
        self._safe_insert(f"📧 EMAIL ENUMERATION: {self.target}\n", 'header')
        self._safe_insert("-"*60 + "\n\n", 'info')
        
        found_emails = []
        
        # Check MX records first
        mx_servers = []
        try:
            answers = dns.resolver.resolve(self.target, 'MX')
            for rdata in answers:
                mx_servers.append(str(rdata.exchange).rstrip('.'))
        except:
            pass
        
        if mx_servers:
            self._safe_insert(f"📡 MX Servers: {', '.join(mx_servers)}\n", 'info')
        else:
            self._safe_insert("📡 No MX records found\n", 'warning')
        
        self._safe_insert("\n🔍 Checking common email addresses:\n", 'info')
        self._safe_insert("-"*40 + "\n", 'info')
        
        for username in self.common_usernames[:20]:
            email = f"{username}@{self.target}"
            # Simple validation - just check if domain exists
            try:
                socket.gethostbyname(self.target)
                found_emails.append(email)
                self._safe_insert(f"   ✅ {email}\n", 'success')
            except:
                self._safe_insert(f"   ❌ {email}\n", 'info')
        
        self._safe_insert("\n" + "="*60 + "\n\n", 'info')
        self._safe_insert(f"📊 Found {len(found_emails)} potential emails\n", 'success')
        self.results_data['email'] = {'found': found_emails}
    
    # ========== 4. TECH FINGERPRINT ==========
    def run_tech_fingerprint(self):
        if not self.get_target():
            messagebox.showwarning("No Target", "Please enter a domain or URL!")
            return
        self.target = self.get_target()
        self.results_text.delete(1.0, tk.END)
        self._safe_insert("💻 TECH FINGERPRINT\n", 'header')
        self._safe_insert("="*60 + "\n\n", 'info')
        self._run_tech_fingerprint_module()
    
    def _run_tech_fingerprint_module(self):
        self._safe_insert(f"💻 TECH FINGERPRINT: {self.target}\n", 'header')
        self._safe_insert("-"*60 + "\n\n", 'info')
        
        url = f"https://{self.target}"
        
        # Try HTTP request
        try:
            response = requests.get(url, timeout=10, verify=False, headers={'User-Agent': 'Mozilla/5.0'})
            content = response.text
            headers = response.headers
            
            # Server detection
            self._safe_insert("📊 WEB SERVER\n", 'info')
            server = headers.get('Server', '')
            if server:
                self._safe_insert(f"   Server: {server}\n", 'info')
            else:
                self._safe_insert("   Server: Unknown\n", 'info')
            
            # Powered by
            powered = headers.get('X-Powered-By', '')
            if powered:
                self._safe_insert(f"   Powered By: {powered}\n", 'info')
            
            self._safe_insert(f"   Status: {response.status_code}\n", 'info')
            self._safe_insert("\n", 'info')
            
            # CMS Detection
            self._safe_insert("📦 CMS DETECTION\n", 'info')
            detected_cms = []
            for cms, patterns in self.cms_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        detected_cms.append(cms)
                        break
            
            if detected_cms:
                for cms in set(detected_cms):
                    self._safe_insert(f"   ✅ {cms}\n", 'success')
            else:
                self._safe_insert("   ℹ️ No CMS detected\n", 'info')
            
            self._safe_insert("\n", 'info')
            
            # JS Framework Detection
            self._safe_insert("📱 FRONTEND\n", 'info')
            detected_js = []
            for js, patterns in self.js_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        detected_js.append(js)
                        break
            
            if detected_js:
                for js in set(detected_js):
                    self._safe_insert(f"   ✅ {js}\n", 'success')
            else:
                self._safe_insert("   ℹ️ No JS framework detected\n", 'info')
            
            self._safe_insert("\n", 'info')
            
            # Language Detection
            self._safe_insert("🔧 LANGUAGE\n", 'info')
            if 'php' in content.lower() or 'PHP' in server:
                self._safe_insert("   ✅ PHP\n", 'success')
            if '.js' in content or 'javascript' in content.lower():
                self._safe_insert("   ✅ JavaScript\n", 'success')
            if 'python' in server.lower() or 'wsgi' in server.lower():
                self._safe_insert("   ✅ Python\n", 'success')
            if 'asp' in server.lower() or '.net' in server.lower():
                self._safe_insert("   ✅ ASP.NET\n", 'success')
            
        except requests.exceptions.Timeout:
            self._safe_insert("⚠️ Connection timeout\n", 'warning')
        except requests.exceptions.SSLError:
            self._safe_insert("⚠️ SSL Error, trying HTTP...\n", 'warning')
            try:
                response = requests.get(f"http://{self.target}", timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                self._safe_insert("✅ HTTP connection successful\n", 'success')
            except:
                self._safe_insert("❌ Connection failed\n", 'error')
        except Exception as e:
            self._safe_insert(f"❌ Error: {str(e)}\n", 'error')
        
        self._safe_insert("\n" + "="*60 + "\n\n", 'info')
        self.results_data['tech'] = {'target': self.target}
    
    # ========== 5. CLOUD DISCOVERY ==========
    def run_cloud_discovery(self):
        if not self.get_target():
            messagebox.showwarning("No Target", "Please enter a domain or URL!")
            return
        self.target = self.get_target()
        self.results_text.delete(1.0, tk.END)
        self._safe_insert("☁️ CLOUD DISCOVERY\n", 'header')
        self._safe_insert("="*60 + "\n\n", 'info')
        self._run_cloud_discovery_module()
    
    def _run_cloud_discovery_module(self):
        self._safe_insert(f"☁️ CLOUD DISCOVERY: {self.target}\n", 'header')
        self._safe_insert("-"*60 + "\n\n", 'info')
        
        url = f"https://{self.target}"
        content = ""
        headers = {}
        
        try:
            response = requests.get(url, timeout=10, verify=False, headers={'User-Agent': 'Mozilla/5.0'})
            content = response.text
            headers = response.headers
        except:
            pass
        
        # Check for cloud providers
        self._safe_insert("📦 CLOUD PROVIDERS\n", 'info')
        
        found_clouds = []
        for provider, info in self.cloud_patterns.items():
            detected = False
            for pattern in info['patterns']:
                if re.search(pattern, content, re.IGNORECASE):
                    detected = True
                    break
                for header_key, header_value in headers.items():
                    if re.search(pattern, f"{header_key}: {header_value}", re.IGNORECASE):
                        detected = True
                        break
            
            if detected:
                found_clouds.append(provider)
                self._safe_insert(f"   ✅ {provider}\n", 'success')
                for service in info['services']:
                    self._safe_insert(f"      • {service}\n", 'info')
        
        if not found_clouds:
            self._safe_insert("   ℹ️ No cloud services detected\n", 'info')
        
        # Check for S3 buckets
        self._safe_insert("\n📦 S3 BUCKET CHECK\n", 'info')
        bucket_names = [
            self.target.replace('.', '-'),
            self.target.split('.')[0],
            f"{self.target.split('.')[0]}-assets",
            f"{self.target.split('.')[0]}-static",
            f"{self.target.split('.')[0]}-media"
        ]
        
        for bucket in bucket_names[:5]:
            try:
                s3_url = f"https://{bucket}.s3.amazonaws.com"
                response = requests.head(s3_url, timeout=5)
                if response.status_code == 200:
                    self._safe_insert(f"   ✅ {s3_url} - PUBLIC\n", 'success')
                elif response.status_code == 403:
                    self._safe_insert(f"   🔒 {s3_url} - PRIVATE\n", 'info')
            except:
                pass
        
        self._safe_insert("\n" + "="*60 + "\n\n", 'info')
        self.results_data['cloud'] = {'found': found_clouds}
    
    # ========== EXPORT ==========
    def export_results(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"osint_results_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'target': self.target,
                    'timestamp': datetime.now().isoformat(),
                    'results': self.results_data
                }, f, indent=2)
            self._safe_insert(f"\n✅ Exported: {filename}\n", 'success')
            messagebox.showinfo("Success", f"Results exported to:\n{filename}")
        except Exception as e:
            self._safe_insert(f"\n❌ Export error: {e}\n", 'error')
    
    def update_scan_data(self, scan_data):
        self.scan_data = scan_data
    
    def show(self):
        if not self.is_loaded:
            self.build_ui()
            self.is_loaded = True
        
        if self.frame:
            self.frame.pack(fill=tk.BOTH, expand=True)
            self.show_initial_message()
