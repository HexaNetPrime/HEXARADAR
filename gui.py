#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HEXARADAR v3.0 - COMPLETE EDITION
8 पेज: MAIN + OUTPUT + AI + NETWORK + OSINT + ANALYTICS + EVASION + ML
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
from datetime import datetime
import queue
import re
import os
import time
import json
import webbrowser

from nmap_commands import NmapCommands
from ai_features_manager import AIFeaturesManager


class NmapGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚡ HEXARADAR v3.0 - Network Scanner ⚡")
        self.root.geometry("1550x970")
        self.root.configure(bg='#0a0a0f')
        
        # ========== NEO CYBER थीम ==========
        self.colors = {
            'bg_primary': '#0a0a0f',
            'bg_secondary': '#0f0f1a',
            'bg_card': '#141420',
            'bg_input': '#1a1a2e',
            'bg_hover': '#1f1f3a',
            'bg_nav': '#0a0a15',
            'neon_gold': '#ffd700',
            'neon_cyan': '#00e5ff',
            'neon_purple': '#9b59ff',
            'neon_pink': '#ff2d95',
            'neon_green': '#00ff88',
            'neon_orange': '#ff6b35',
            'neon_red': '#ff1744',
            'neon_blue': '#4488ff',
            'white': '#e8e8f0',
            'gray': '#7a7a9a',
            'dark_gray': '#3a3a5a',
        }
        
        self.current_process = None
        self.is_scanning = False
        self.output_queue = queue.Queue()
        self.last_scan_output = ""
        self.scan_history = []
        self.cmd_vars = {}
        self.cmd_entries = {}
        self.current_page_index = 0
        self.manual_command = ""
        self.ai_manager = None
        
        # ========== 8 पेज ==========
        self.page_names = [
            "🏠 MAIN",
            "📊 OUTPUT",
            "🤖 AI",
            "🌐 NETWORK",
            "🔍 OSINT",
            "📊 ANALYTICS",
            "🛡 EVASION",
            "🧠 ML"
        ]
        self.total_pages = 8
        
        # ========== Nmap Commands ==========
        self.nmap_cmds = NmapCommands()
        self.all_commands = self.nmap_cmds.get_all_commands()
        self.categories = self.nmap_cmds.get_categories()
        
        print(f"[*] Loaded {len(self.all_commands)} commands")
        
        self.category_tab_map = {
            'target': '🎯 TARGET',
            'host_discovery': '🔍 HOST',
            'scan_techniques': '⚡ SCAN',
            'port_spec': '🔌 PORT',
            'service_version': '🛠 SERVICE',
            'script_scan': '📜 SCRIPT',
            'os_detection': '💻 OS',
            'timing_performance': '⏱ TIMING',
            'firewall_evasion': '🛡 FIREWALL',
            'output_options': '📄 OUTPUT',
            'misc': '🔧 MISC'
        }
        
        self.setup_ui()
        self.update_output_queue()
        self.animate_status()
    
    # ========== SETUP UI ==========
    def setup_ui(self):
        """Main UI Setup - 8 Pages"""
        self.main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # ========== TOP NAVIGATION BAR ==========
        self.create_navigation_bar()
        
        # ========== PAGE CONTAINER ==========
        self.page_container = tk.Frame(self.main_container, bg=self.colors['bg_primary'])
        self.page_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # ========== CREATE 8 PAGES ==========
        self.pages = []
        
        # Page 0: Main
        self.main_page = tk.Frame(self.page_container, bg=self.colors['bg_primary'])
        self.pages.append(self.main_page)
        
        # Page 1: Output
        self.output_page = tk.Frame(self.page_container, bg=self.colors['bg_primary'])
        self.pages.append(self.output_page)
        
        # Page 2: AI
        self.ai_page = tk.Frame(self.page_container, bg=self.colors['bg_primary'])
        self.pages.append(self.ai_page)
        
        # Page 3: Network Mapping
        self.network_page = tk.Frame(self.page_container, bg=self.colors['bg_primary'])
        self.pages.append(self.network_page)
        
        # Page 4: Advanced Discovery (OSINT)
        self.discovery_page = tk.Frame(self.page_container, bg=self.colors['bg_primary'])
        self.pages.append(self.discovery_page)
        
        # Page 5: Data Analytics
        self.analytics_page = tk.Frame(self.page_container, bg=self.colors['bg_primary'])
        self.pages.append(self.analytics_page)
        
        # Page 6: Evasion Techniques
        self.evasion_page = tk.Frame(self.page_container, bg=self.colors['bg_primary'])
        self.pages.append(self.evasion_page)
        
        # Page 7: ML Vulnerability Prediction (NEW)
        self.ml_page = tk.Frame(self.page_container, bg=self.colors['bg_primary'])
        self.pages.append(self.ml_page)
        
        # ========== CREATE CONTENT ==========
        self.create_main_page()
        self.create_output_page()
        self.create_ai_page()
        self.create_network_page()
        self.create_discovery_page()
        self.create_analytics_page()
        self.create_evasion_page()
        self.create_ml_page()
        
        # Show first page
        self.show_page(0)
    
    # ========== TOP NAVIGATION BAR ==========
    def create_navigation_bar(self):
        """Navigation Bar - 8 Pages"""
        nav_frame = tk.Frame(self.main_container, bg=self.colors['bg_nav'], height=45)
        nav_frame.pack(fill=tk.X, pady=(0, 2))
        nav_frame.pack_propagate(False)
        
        # Left: Logo
        logo_frame = tk.Frame(nav_frame, bg=self.colors['bg_nav'])
        logo_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            logo_frame,
            text="⚡ HEXARADAR",
            bg=self.colors['bg_nav'],
            fg=self.colors['neon_gold'],
            font=('Courier', 14, 'bold')
        ).pack(side=tk.LEFT)
        
        tk.Label(
            logo_frame,
            text="v3.0",
            bg=self.colors['bg_nav'],
            fg=self.colors['gray'],
            font=('Courier', 8)
        ).pack(side=tk.LEFT, padx=5)
        
        # Center: Page Navigation Buttons
        nav_center = tk.Frame(nav_frame, bg=self.colors['bg_nav'])
        nav_center.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
        
        self.nav_buttons = []
        self.nav_frames = []
        
        for i, name in enumerate(self.page_names):
            btn_frame = tk.Frame(nav_center, bg=self.colors['bg_nav'])
            btn_frame.pack(side=tk.LEFT, padx=5)
            
            btn = tk.Button(
                btn_frame,
                text=name,
                command=lambda idx=i: self.show_page(idx),
                bg=self.colors['bg_card'] if i == 0 else self.colors['bg_nav'],
                fg=self.colors['neon_gold'] if i == 0 else self.colors['gray'],
                font=('Courier', 10, 'bold'),
                padx=20, pady=5,
                cursor='hand2',
                relief=tk.FLAT, bd=0
            )
            btn.pack()
            self.nav_buttons.append(btn)
            
            indicator = tk.Frame(
                btn_frame,
                bg=self.colors['neon_gold'] if i == 0 else self.colors['bg_nav'],
                height=3
            )
            indicator.pack(fill=tk.X, padx=5)
            self.nav_frames.append(indicator)
        
        # Right: Stats
        stats_frame = tk.Frame(nav_frame, bg=self.colors['bg_nav'])
        stats_frame.pack(side=tk.RIGHT, padx=10)
        
        stats = [
            ("📊", "0", self.colors['neon_cyan']),
            ("🔓", "0", self.colors['neon_green']),
            ("⚠️", "0", self.colors['neon_red']),
        ]
        
        self.stats_labels = {}
        for icon, value, color in stats:
            frame = tk.Frame(stats_frame, bg=self.colors['bg_nav'])
            frame.pack(side=tk.LEFT, padx=5)
            
            lbl = tk.Label(
                frame,
                text=f"{icon} {value}",
                bg=self.colors['bg_nav'],
                fg=color,
                font=('Courier', 9, 'bold')
            )
            lbl.pack()
            self.stats_labels[icon] = lbl
    
    # ========== PAGE NAVIGATION ==========
    def show_page(self, index):
        if index < 0 or index >= len(self.pages):
            return
        
        for page in self.pages:
            page.pack_forget()
        
        self.pages[index].pack(fill=tk.BOTH, expand=True)
        self.current_page_index = index
        
        # Update navigation
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.config(bg=self.colors['bg_card'], fg=self.colors['neon_gold'])
                self.nav_frames[i].config(bg=self.colors['neon_gold'])
            else:
                btn.config(bg=self.colors['bg_nav'], fg=self.colors['gray'])
                self.nav_frames[i].config(bg=self.colors['bg_nav'])
        
        # Update AI data when AI page is shown
        if index == 2 and self.ai_manager and self.last_scan_output:
            self.ai_manager.update_scan_data(self.last_scan_output)
    
    # ========== ANIMATED STATUS ==========
    def animate_status(self):
        try:
            if hasattr(self, 'status_indicator'):
                current = self.status_indicator.cget('fg')
                new_color = self.colors['neon_red'] if current == self.colors['neon_gold'] else self.colors['neon_gold']
                self.status_indicator.config(fg=new_color)
            self.root.after(500, self.animate_status)
        except:
            pass
    
    # ========== PAGE 0: MAIN PAGE ==========
    def create_main_page(self):
        parent = self.pages[0]
        
        content_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Quick Actions
        self.create_quick_actions(content_frame)
        
        # Target Section
        self.create_target_section(content_frame)
        
        # Scan Options
        self.create_scan_options(content_frame)
        
        # Status Bar
        self.create_status_bar(parent)
    
    def create_quick_actions(self, parent):
        frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=50)
        frame.pack(fill=tk.X, pady=(0, 8))
        frame.pack_propagate(False)
        
        tk.Label(
            frame,
            text="⚡ QUICK ACTIONS",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_gold'],
            font=('Courier', 10, 'bold')
        ).pack(side=tk.LEFT, padx=15)
        
        actions = [
            ("🚀 ULTRA", self.ultra_fast_scan, self.colors['neon_cyan']),
            ("⚡ FAST", self.fast_scan, self.colors['neon_green']),
            ("📋 LIST", self.list_scan, self.colors['neon_purple']),
            ("🛡 STEALTH", self.stealth_scan, self.colors['neon_pink']),
            ("🔍 FULL", self.full_scan, self.colors['neon_orange']),
        ]
        
        for text, cmd, color in actions:
            btn = tk.Button(
                frame,
                text=text,
                command=cmd,
                bg=self.colors['bg_card'],
                fg=color,
                font=('Courier', 9, 'bold'),
                padx=15, pady=5,
                cursor='hand2',
                relief=tk.FLAT, bd=0
            )
            btn.pack(side=tk.LEFT, padx=3)
            self._add_hover(btn, color)
    
    def _add_hover(self, button, color):
        def on_enter(e):
            button.config(bg=self.colors['bg_hover'], fg='white')
        def on_leave(e):
            button.config(bg=self.colors['bg_card'], fg=color)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def create_target_section(self, parent):
        frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=55)
        frame.pack(fill=tk.X, pady=(0, 8))
        frame.pack_propagate(False)
        
        tk.Label(
            frame,
            text="🎯 TARGET",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_gold'],
            font=('Courier', 11, 'bold')
        ).pack(side=tk.LEFT, padx=15)
        
        self.target_entry = tk.Entry(
            frame,
            width=35,
            bg=self.colors['bg_input'],
            fg=self.colors['white'],
            font=('Courier', 11),
            insertbackground=self.colors['neon_gold'],
            relief=tk.FLAT, bd=0
        )
        self.target_entry.pack(side=tk.LEFT, padx=10)
        self.target_entry.insert(0, "192.168.159.128")
        
        buttons = [
            ("▶ RUN", self.run_scan, self.colors['neon_green']),
            ("⏹ STOP", self.stop_scan, self.colors['neon_red']),
            ("🗑 CLEAR", self.clear_output, self.colors['neon_gold']),
            ("💾 SAVE", self.save_output_file, self.colors['neon_purple']),
        ]
        
        for text, cmd, color in buttons:
            btn = tk.Button(
                frame,
                text=text,
                command=cmd,
                bg=self.colors['bg_card'],
                fg=color,
                font=('Courier', 9, 'bold'),
                padx=12, pady=5,
                cursor='hand2',
                relief=tk.FLAT, bd=0
            )
            btn.pack(side=tk.LEFT, padx=3)
            self._add_hover(btn, color)
            
            if text == "⏹ STOP":
                self.stop_btn = btn
                btn.config(state=tk.DISABLED)
            elif text == "▶ RUN":
                self.run_btn = btn
    
    def create_scan_options(self, parent):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure(
            'Neon.TNotebook',
            background=self.colors['bg_secondary'],
            borderwidth=0
        )
        style.configure(
            'Neon.TNotebook.Tab',
            background=self.colors['bg_card'],
            foreground=self.colors['gray'],
            padding=[12, 6],
            font=('Courier', 9, 'bold')
        )
        style.map(
            'Neon.TNotebook.Tab',
            background=[('selected', self.colors['neon_gold']), ('active', self.colors['bg_hover'])],
            foreground=[('selected', '#0a0a0f'), ('active', 'white')]
        )
        
        self.notebook = ttk.Notebook(parent, style='Neon.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for category in self.categories:
            tab_name = self.category_tab_map.get(category, category.upper())
            commands = self.nmap_cmds.get_category(category)
            if commands:
                self.create_command_tab(tab_name, commands, category)
    
    def create_command_tab(self, title, commands, tab_name):
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg_secondary'])
        self.notebook.add(tab_frame, text=title)
        
        canvas = tk.Canvas(tab_frame, bg=self.colors['bg_secondary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_secondary'])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        if tab_name not in self.cmd_vars:
            self.cmd_vars[tab_name] = {}
        if tab_name not in self.cmd_entries:
            self.cmd_entries[tab_name] = {}
        
        row = 0
        for cmd, info in commands.items():
            cmd_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], relief=tk.FLAT)
            cmd_frame.grid(row=row, column=0, sticky=tk.W+tk.E, pady=2, padx=3, ipadx=4, ipady=2)
            cmd_frame.grid_columnconfigure(0, weight=1)
            
            var = tk.BooleanVar()
            chk = tk.Checkbutton(
                cmd_frame,
                text=cmd,
                variable=var,
                bg=self.colors['bg_card'],
                fg=self.colors['neon_cyan'],
                selectcolor=self.colors['bg_card'],
                font=('Courier', 8, 'bold')
            )
            chk.pack(side=tk.LEFT, padx=4)
            
            desc = info.get('desc', info.get('what', ''))
            short_desc = desc[:35] + "..." if len(desc) > 35 else desc
            tk.Label(
                cmd_frame,
                text=f"- {short_desc}",
                bg=self.colors['bg_card'],
                fg=self.colors['gray'],
                font=('Courier', 7)
            ).pack(side=tk.LEFT, padx=4)
            
            entry_widget = None
            syntax = info.get('syntax', '')
            needs_value = any(x in syntax for x in ['<', '>', 'port', 'file', 'time', 'number'])
            
            if needs_value or cmd in ['-p', '--script', '--min-rate', '--max-retries', 
                                       '--host-timeout', '--top-ports', '--mtu', '-D', 
                                       '-g', '--ttl', '--spoof-mac', '-oN', '-oX', '-oG', 
                                       '-oA', '-iL', '--exclude', '--excludefile']:
                entry = tk.Entry(
                    cmd_frame,
                    width=10,
                    bg=self.colors['bg_input'],
                    fg=self.colors['neon_gold'],
                    font=('Courier', 7),
                    relief=tk.FLAT, bd=0
                )
                entry.pack(side=tk.RIGHT, padx=4)
                
                defaults = {
                    '-p': '1-1000', '--min-rate': '5000', '--max-retries': '1',
                    '--top-ports': '100', '-D': 'RND:10', '-g': '53',
                    '--mtu': '8', '--ttl': '128', '--spoof-mac': '0',
                    '-oN': 'scan.txt', '-oX': 'scan.xml', '-oG': 'scan.gnmap',
                    '-oA': 'scan', '-iL': 'targets.txt', '--exclude': '192.168.1.5',
                    '--version-intensity': '7', '--host-timeout': '5m'
                }
                if cmd in defaults:
                    entry.insert(0, defaults[cmd])
                entry_widget = entry
            
            self.cmd_vars[tab_name][cmd] = var
            self.cmd_entries[tab_name][cmd] = entry_widget
            row += 1
        
        tk.Label(
            scrollable_frame,
            text=f"📊 {len(commands)} commands",
            bg=self.colors['bg_secondary'],
            fg=self.colors['gray'],
            font=('Courier', 8)
        ).grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
    
    def create_status_bar(self, parent):
        frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=30)
        frame.pack(fill=tk.X, pady=(8, 0))
        frame.pack_propagate(False)
        
        self.status_indicator = tk.Label(
            frame,
            text="●",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_gold'],
            font=('Courier', 14)
        )
        self.status_indicator.pack(side=tk.LEFT, padx=12)
        
        self.status_bar = tk.Label(
            frame,
            text="HEXARADAR v3.0 READY ⚡",
            bg=self.colors['bg_secondary'],
            fg=self.colors['white'],
            font=('Courier', 10, 'bold')
        )
        self.status_bar.pack(side=tk.LEFT, padx=8)
        
        self.progress = ttk.Progressbar(
            frame,
            mode='indeterminate',
            length=150,
            style='Neon.Horizontal.TProgressbar'
        )
        self.progress.pack(side=tk.RIGHT, padx=15)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'Neon.Horizontal.TProgressbar',
            background=self.colors['neon_gold'],
            troughcolor=self.colors['bg_input'],
            borderwidth=0
        )
    
    # ========== PAGE 1: OUTPUT PAGE ==========
    def create_output_page(self):
        parent = self.pages[1]
        
        content_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(content_frame, bg=self.colors['bg_secondary'], height=40)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📊 OUTPUT CONSOLE",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_gold'],
            font=('Courier', 13, 'bold')
        ).pack(side=tk.LEFT, padx=15)
        
        self.scan_status = tk.Label(
            header_frame,
            text="🟢 READY",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_green'],
            font=('Courier', 10, 'bold')
        )
        self.scan_status.pack(side=tk.RIGHT, padx=15)
        
        # Manual Command
        manual_frame = tk.Frame(content_frame, bg=self.colors['bg_card'])
        manual_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        tk.Label(
            manual_frame,
            text="📝 MANUAL COMMAND",
            bg=self.colors['bg_card'],
            fg=self.colors['neon_gold'],
            font=('Courier', 10, 'bold')
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        cmd_input_frame = tk.Frame(manual_frame, bg=self.colors['bg_card'])
        cmd_input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.manual_command_entry = tk.Entry(
            cmd_input_frame,
            bg=self.colors['bg_input'],
            fg=self.colors['neon_cyan'],
            font=('Courier', 11),
            insertbackground=self.colors['neon_gold'],
            relief=tk.FLAT, bd=0
        )
        self.manual_command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.manual_command_entry.insert(0, "nmap -p- -sV -sC 192.168.159.128")
        
        self.manual_run_btn = tk.Button(
            cmd_input_frame,
            text="▶ RUN",
            command=self.run_manual_command,
            bg=self.colors['neon_green'],
            fg='#0a0a0f',
            font=('Courier', 10, 'bold'),
            padx=20, pady=5,
            cursor='hand2',
            relief=tk.FLAT, bd=0
        )
        self.manual_run_btn.pack(side=tk.RIGHT)
        
        # Command Display
        cmd_frame = tk.Frame(content_frame, bg=self.colors['bg_card'])
        cmd_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        tk.Label(
            cmd_frame,
            text="📝 CURRENT COMMAND",
            bg=self.colors['bg_card'],
            fg=self.colors['neon_gold'],
            font=('Courier', 10, 'bold')
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        self.command_text_widget = tk.Text(
            cmd_frame,
            height=2,
            bg=self.colors['bg_input'],
            fg=self.colors['neon_gold'],
            font=('Courier', 10),
            relief=tk.FLAT, bd=0,
            wrap=tk.WORD
        )
        self.command_text_widget.pack(fill=tk.X, padx=10, pady=5)
        
        # Output Display
        output_frame = tk.Frame(content_frame, bg=self.colors['bg_card'])
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))
        
        tk.Label(
            output_frame,
            text="📊 SCAN OUTPUT",
            bg=self.colors['bg_card'],
            fg=self.colors['neon_cyan'],
            font=('Courier', 10, 'bold')
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        self.output_text_widget = scrolledtext.ScrolledText(
            output_frame,
            bg=self.colors['bg_input'],
            fg=self.colors['white'],
            font=('Courier', 10),
            relief=tk.FLAT, bd=0,
            wrap=tk.WORD,
            insertbackground=self.colors['neon_gold']
        )
        self.output_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.output_text_widget.tag_config('info', foreground=self.colors['neon_cyan'])
        self.output_text_widget.tag_config('output', foreground=self.colors['white'])
        self.output_text_widget.tag_config('error', foreground=self.colors['neon_red'])
        self.output_text_widget.tag_config('warning', foreground=self.colors['neon_gold'])
        self.output_text_widget.tag_config('success', foreground=self.colors['neon_green'])
        
        btn_frame = tk.Frame(output_frame, bg=self.colors['bg_card'])
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        for text, cmd, color in [
            ("🗑 CLEAR", self.clear_output_display, self.colors['neon_gold']),
            ("📋 COPY", self.copy_output, self.colors['neon_cyan']),
            ("💾 SAVE", self.save_output_file, self.colors['neon_purple']),
        ]:
            btn = tk.Button(
                btn_frame,
                text=text,
                command=cmd,
                bg=self.colors['bg_card'],
                fg=color,
                font=('Courier', 9, 'bold'),
                padx=10, pady=4,
                cursor='hand2',
                relief=tk.FLAT, bd=0
            )
            btn.pack(side=tk.LEFT, padx=3)
            self._add_hover(btn, color)
    
    # ========== PAGE 2: AI PAGE ==========
    def create_ai_page(self):
        parent = self.pages[2]
        
        content_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(content_frame, bg=self.colors['bg_secondary'], height=40)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🤖 AI & NETWORK FEATURES",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_gold'],
            font=('Courier', 14, 'bold')
        ).pack(side=tk.LEFT, padx=15)
        
        # Create AI Manager - 5 features handle करेगा (ML removed from AI)
        self.ai_manager = AIFeaturesManager(content_frame, self.output_text_widget)
        if self.last_scan_output:
            self.ai_manager.update_scan_data(self.last_scan_output)
    
    # ========== PAGE 3: NETWORK MAPPING ==========
    def create_network_page(self):
        parent = self.pages[3]
        
        content_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(content_frame, bg=self.colors['bg_secondary'], height=40)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🌐 NETWORK MAPPING",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_gold'],
            font=('Courier', 14, 'bold')
        ).pack(side=tk.LEFT, padx=15)
        
        # Network Mapping Feature Direct Load
        try:
            from features.network_mapping import NetworkMappingFeature
            
            self.network_mapping = NetworkMappingFeature(
                content_frame,
                self.colors,
                self.output_text_widget
            )
            
            if self.last_scan_output:
                self.network_mapping.update_scan_data(self.last_scan_output)
            
            self.network_mapping.show()
        except ImportError as e:
            self._show_network_placeholder(f"Module not found: {e}")
        except Exception as e:
            self._show_network_placeholder(f"Error: {e}")
    
    def _show_network_placeholder(self, error_msg=""):
        frame = tk.Frame(self.pages[3], bg=self.colors['bg_primary'])
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="🌐 NETWORK MAPPING", bg=self.colors['bg_primary'], fg=self.colors['neon_gold'], font=('Courier', 16, 'bold')).pack(pady=50)
        tk.Label(frame, text="⏳ Loading Network Mapping Module...", bg=self.colors['bg_primary'], fg=self.colors['gray'], font=('Courier', 12)).pack(pady=10)
        if error_msg:
            tk.Label(frame, text=f"Note: {error_msg}", bg=self.colors['bg_primary'], fg=self.colors['neon_red'], font=('Courier', 10)).pack(pady=10)
    
    # ========== PAGE 4: ADVANCED DISCOVERY (OSINT) ==========
    def create_discovery_page(self):
        parent = self.pages[4]
        
        content_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(content_frame, bg=self.colors['bg_secondary'], height=40)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🔍 ADVANCED DISCOVERY (OSINT)",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_gold'],
            font=('Courier', 14, 'bold')
        ).pack(side=tk.LEFT, padx=15)
        
        try:
            from features.advanced_discovery import AdvancedDiscoveryFeature
            
            self.discovery_feature = AdvancedDiscoveryFeature(
                content_frame,
                self.colors,
                self.output_text_widget
            )
            self.discovery_feature.show()
        except ImportError as e:
            self._show_discovery_placeholder(f"Module not found: {e}")
        except Exception as e:
            self._show_discovery_placeholder(f"Error: {e}")
    
    def _show_discovery_placeholder(self, error_msg=""):
        frame = tk.Frame(self.pages[4], bg=self.colors['bg_primary'])
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="🔍 ADVANCED DISCOVERY (OSINT)", bg=self.colors['bg_primary'], fg=self.colors['neon_gold'], font=('Courier', 16, 'bold')).pack(pady=50)
        tk.Label(frame, text="⏳ Loading Advanced Discovery Module...", bg=self.colors['bg_primary'], fg=self.colors['gray'], font=('Courier', 12)).pack(pady=10)
        if error_msg:
            tk.Label(frame, text=f"Note: {error_msg}", bg=self.colors['bg_primary'], fg=self.colors['neon_red'], font=('Courier', 10)).pack(pady=10)
    
    # ========== PAGE 5: DATA ANALYTICS ==========
    def create_analytics_page(self):
        parent = self.pages[5]
        
        content_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(content_frame, bg=self.colors['bg_secondary'], height=40)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📊 DATA ANALYTICS",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_gold'],
            font=('Courier', 14, 'bold')
        ).pack(side=tk.LEFT, padx=15)
        
        try:
            from features.data_analytics import DataAnalyticsFeature
            
            self.analytics_feature = DataAnalyticsFeature(
                content_frame,
                self.colors,
                self.output_text_widget
            )
            self.analytics_feature.show()
        except ImportError as e:
            self._show_analytics_placeholder(f"Module not found: {e}")
        except Exception as e:
            self._show_analytics_placeholder(f"Error: {e}")
    
    def _show_analytics_placeholder(self, error_msg=""):
        frame = tk.Frame(self.pages[5], bg=self.colors['bg_primary'])
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="📊 DATA ANALYTICS", bg=self.colors['bg_primary'], fg=self.colors['neon_gold'], font=('Courier', 16, 'bold')).pack(pady=50)
        tk.Label(frame, text="⏳ Loading Data Analytics Module...", bg=self.colors['bg_primary'], fg=self.colors['gray'], font=('Courier', 12)).pack(pady=10)
        if error_msg:
            tk.Label(frame, text=f"Note: {error_msg}", bg=self.colors['bg_primary'], fg=self.colors['neon_red'], font=('Courier', 10)).pack(pady=10)
    
    # ========== PAGE 6: EVASION TECHNIQUES ==========
    def create_evasion_page(self):
        parent = self.pages[6]
        
        content_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(content_frame, bg=self.colors['bg_secondary'], height=40)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🛡 EVASION TECHNIQUES",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_gold'],
            font=('Courier', 14, 'bold')
        ).pack(side=tk.LEFT, padx=15)
        
        try:
            from features.evasion_techniques import EvasionTechniquesFeature
            
            self.evasion_feature = EvasionTechniquesFeature(
                content_frame,
                self.colors,
                self.output_text_widget
            )
            self.evasion_feature.show()
        except ImportError as e:
            self._show_evasion_placeholder(f"Module not found: {e}")
        except Exception as e:
            self._show_evasion_placeholder(f"Error: {e}")
    
    def _show_evasion_placeholder(self, error_msg=""):
        frame = tk.Frame(self.pages[6], bg=self.colors['bg_primary'])
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="🛡 EVASION TECHNIQUES", bg=self.colors['bg_primary'], fg=self.colors['neon_gold'], font=('Courier', 16, 'bold')).pack(pady=50)
        tk.Label(frame, text="⏳ Loading Evasion Techniques Module...", bg=self.colors['bg_primary'], fg=self.colors['gray'], font=('Courier', 12)).pack(pady=10)
        if error_msg:
            tk.Label(frame, text=f"Note: {error_msg}", bg=self.colors['bg_primary'], fg=self.colors['neon_red'], font=('Courier', 10)).pack(pady=10)
    
    # ========== PAGE 7: ML VULNERABILITY PREDICTION ==========
    def create_ml_page(self):
        """Page 7: ML Vulnerability Prediction"""
        parent = self.pages[7]
        
        content_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(content_frame, bg=self.colors['bg_secondary'], height=40)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🧠 DEEP LEARNING VULNERABILITY PREDICTION",
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_gold'],
            font=('Courier', 14, 'bold')
        ).pack(side=tk.LEFT, padx=15)
        
        # Load ML Feature Directly
        try:
            from features.ml_vuln_prediction import MLVulnPredictionFeature
            
            self.ml_feature = MLVulnPredictionFeature(
                content_frame,
                self.colors,
                self.output_text_widget
            )
            if self.last_scan_output:
                self.ml_feature.update_scan_data(self.last_scan_output)
            self.ml_feature.show()
            
        except ImportError as e:
            self._show_ml_placeholder(f"Module not found: {e}")
        except Exception as e:
            self._show_ml_placeholder(f"Error: {e}")
    
    def _show_ml_placeholder(self, error_msg=""):
        """Placeholder for ML feature if not available"""
        frame = tk.Frame(self.pages[7], bg=self.colors['bg_primary'])
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            frame,
            text="🧠 DEEP LEARNING VULNERABILITY PREDICTION",
            bg=self.colors['bg_primary'],
            fg=self.colors['neon_gold'],
            font=('Courier', 16, 'bold')
        ).pack(pady=50)
        
        tk.Label(
            frame,
            text="⏳ Loading ML Module...",
            bg=self.colors['bg_primary'],
            fg=self.colors['gray'],
            font=('Courier', 12)
        ).pack(pady=10)
        
        if error_msg:
            tk.Label(
                frame,
                text=f"Note: {error_msg}",
                bg=self.colors['bg_primary'],
                fg=self.colors['neon_red'],
                font=('Courier', 10)
            ).pack(pady=10)
        
        tk.Label(
            frame,
            text="💡 Make sure features/ml_vuln_prediction.py exists",
            bg=self.colors['bg_primary'],
            fg=self.colors['neon_cyan'],
            font=('Courier', 10)
        ).pack(pady=20)
    
    # ========== SCAN FUNCTIONS ==========
    def _set_option(self, tab, cmd, value, entry_val=None):
        if tab in self.cmd_vars and cmd in self.cmd_vars[tab]:
            self.cmd_vars[tab][cmd].set(value)
            if entry_val is not None and tab in self.cmd_entries and cmd in self.cmd_entries[tab]:
                entry = self.cmd_entries[tab][cmd]
                if entry:
                    entry.delete(0, tk.END)
                    entry.insert(0, entry_val)
    
    def clear_all_selections(self):
        for tab in self.cmd_vars:
            for cmd in self.cmd_vars[tab]:
                self.cmd_vars[tab][cmd].set(False)
        for tab in self.cmd_entries:
            for entry in self.cmd_entries[tab].values():
                if entry:
                    try:
                        entry.delete(0, tk.END)
                    except:
                        pass
    
    def ultra_fast_scan(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("No Target", "Enter target first!")
            return
        self.clear_all_selections()
        self._set_option('⏱ TIMING', '-T5', True)
        self._set_option('⏱ TIMING', '--min-rate', True, "10000")
        self._set_option('⏱ TIMING', '--max-retries', True, "0")
        self._set_option('🔌 PORT', '-F', True)
        self._set_option('🔧 MISC', '-n', True)
        self.show_page(1)
        self.log_output("🚀 ULTRA FAST SCAN STARTED\n", 'info')
        self.run_scan()
    
    def fast_scan(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("No Target", "Enter target first!")
            return
        self.clear_all_selections()
        self._set_option('⏱ TIMING', '-T4', True)
        self._set_option('⏱ TIMING', '--min-rate', True, "5000")
        self._set_option('⏱ TIMING', '--max-retries', True, "1")
        self._set_option('🔌 PORT', '-F', True)
        self._set_option('🔧 MISC', '-n', True)
        self.show_page(1)
        self.log_output("⚡ FAST SCAN STARTED\n", 'info')
        self.run_scan()
    
    def list_scan(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("No Target", "Enter target first!")
            return
        self.clear_all_selections()
        self._set_option('🔍 HOST', '-sL', True)
        self._set_option('🔧 MISC', '-n', True)
        self.show_page(1)
        self.log_output("📋 LIST SCAN STARTED\n", 'info')
        self.run_scan()
    
    def stealth_scan(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("No Target", "Enter target first!")
            return
        self.clear_all_selections()
        self._set_option('⏱ TIMING', '-T2', True)
        self._set_option('⏱ TIMING', '--min-rate', True, "100")
        self._set_option('🔌 PORT', '-p', True, "22,80,443,445,3389")
        self._set_option('🛡 FIREWALL', '-f', True)
        self._set_option('🛡 FIREWALL', '--mtu', True, "8")
        self.show_page(1)
        self.log_output("🛡 STEALTH SCAN STARTED\n", 'info')
        self.run_scan()
    
    def full_scan(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("No Target", "Enter target first!")
            return
        self.clear_all_selections()
        self._set_option('⚡ SCAN', '-sS', True)
        self._set_option('⚡ SCAN', '-sV', True)
        self._set_option('⚡ SCAN', '-sC', True)
        self._set_option('🔌 PORT', '-p-', True)
        self._set_option('⏱ TIMING', '-T4', True)
        self._set_option('🛡 FIREWALL', '-Pn', True)
        self.show_page(1)
        self.log_output("🔍 FULL SCAN STARTED\n", 'info')
        self.run_scan()
    
    # ========== RUN SCAN ==========
    def run_scan(self):
        if self.is_scanning:
            return
        cmd = self.build_command()
        if hasattr(self, 'command_text_widget') and self.command_text_widget:
            self.command_text_widget.delete(1.0, tk.END)
            self.command_text_widget.insert(1.0, cmd)
        if self.output_text_widget:
            self.output_text_widget.delete(1.0, tk.END)
        self.log_output("="*70 + "\n", 'info')
        self.log_output(f"[*] SCAN: {datetime.now().strftime('%H:%M:%S')}\n", 'info')
        self.log_output(f"[*] {cmd}\n", 'info')
        self.log_output("="*70 + "\n\n", 'info')
        
        def scan():
            process = None
            try:
                start_time = time.time()
                self.is_scanning = True
                self.run_btn.config(state=tk.DISABLED)
                self.manual_run_btn.config(state=tk.DISABLED, bg=self.colors['gray'])
                self.stop_btn.config(state=tk.NORMAL)
                self.status_bar.config(text="🔥 SCANNING...", fg=self.colors['neon_red'])
                self.scan_status.config(text="🔄 SCANNING...", fg=self.colors['neon_gold'])
                self.progress.start()
                
                process = subprocess.Popen(
                    cmd, shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                self.current_process = process
                
                if process is None:
                    self.log_output("\n[✗] ERROR: Failed to start process\n", 'error')
                    return
                
                lines = []
                while True:
                    if process.poll() is not None:
                        break
                    try:
                        line = process.stdout.readline()
                        if not line:
                            break
                        self.log_output(line, 'output')
                        lines.append(line)
                    except Exception as e:
                        self.log_output(f"\n[!] Read error: {e}\n", 'warning')
                        break
                
                try:
                    stdout, stderr = process.communicate(timeout=5)
                    if stdout:
                        self.log_output(stdout, 'output')
                        lines.append(stdout)
                    if stderr:
                        self.log_output(f"\n[!] {stderr}\n", 'error')
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate()
                    if stdout:
                        self.log_output(stdout, 'output')
                
                self.last_scan_output = ''.join(lines)
                elapsed = time.time() - start_time
                self.progress.stop()
                self.log_output("\n" + "="*70 + "\n", 'info')
                self.log_output(f"[✓] COMPLETED: {elapsed:.2f}s\n", 'success')
                self.status_bar.config(text="✅ READY", fg=self.colors['neon_green'])
                self.scan_status.config(text="✅ COMPLETED", fg=self.colors['neon_green'])
                self.update_stats()
                
                if self.ai_manager and self.last_scan_output:
                    self.ai_manager.update_scan_data(self.last_scan_output)
                    
            except subprocess.TimeoutExpired:
                self.progress.stop()
                self.log_output("\n[✗] ERROR: Scan timed out\n", 'error')
                self.status_bar.config(text="❌ TIMEOUT", fg=self.colors['neon_red'])
                self.scan_status.config(text="❌ TIMEOUT", fg=self.colors['neon_red'])
            except Exception as e:
                self.progress.stop()
                self.log_output(f"\n[✗] ERROR: {str(e)}\n", 'error')
                self.status_bar.config(text="❌ FAILED", fg=self.colors['neon_red'])
                self.scan_status.config(text="❌ FAILED", fg=self.colors['neon_red'])
            finally:
                self.is_scanning = False
                self.run_btn.config(state=tk.NORMAL)
                self.manual_run_btn.config(state=tk.NORMAL, bg=self.colors['neon_green'])
                self.stop_btn.config(state=tk.DISABLED)
                self.current_process = None
                if process and process.poll() is None:
                    try:
                        process.kill()
                    except:
                        pass
        
        threading.Thread(target=scan, daemon=True).start()
    
    def build_command(self):
        cmd = ["nmap"]
        target = self.target_entry.get().strip()
        is_list_scan = False
        for tab, vars_dict in self.cmd_vars.items():
            for c, var in vars_dict.items():
                if c == '-sL' and var.get():
                    is_list_scan = True
        for tab, vars_dict in self.cmd_vars.items():
            entries_dict = self.cmd_entries.get(tab, {})
            for c, var in vars_dict.items():
                if var.get():
                    if is_list_scan and c in ['-p', '-F', '--top-ports', '-T0', '-T1', '-T2', '-T3', '-T4', '-T5']:
                        continue
                    entry = entries_dict.get(c)
                    if entry and entry.get():
                        cmd.append(f"{c} {entry.get()}")
                    else:
                        cmd.append(c)
        if target:
            cmd.append(target)
        else:
            cmd.append("scanme.nmap.org")
        return " ".join(cmd)
    
    def stop_scan(self):
        if self.current_process and self.is_scanning:
            try:
                self.current_process.terminate()
                time.sleep(0.5)
                if self.current_process.poll() is None:
                    self.current_process.kill()
                self.log_output("\n[!] STOPPED\n", 'warning')
                self.status_bar.config(text="⏹ STOPPED", fg=self.colors['neon_gold'])
                self.scan_status.config(text="⏹ STOPPED", fg=self.colors['neon_gold'])
                self.progress.stop()
                self.is_scanning = False
                self.run_btn.config(state=tk.NORMAL)
                self.manual_run_btn.config(state=tk.NORMAL, bg=self.colors['neon_green'])
                self.stop_btn.config(state=tk.DISABLED)
            except Exception as e:
                self.log_output(f"\n[!] Stop error: {e}\n", 'warning')
    
    def update_stats(self):
        if self.last_scan_output:
            ports = re.findall(r'(\d+)/tcp\s+open', self.last_scan_output)
            vulns = len(re.findall(r'VULNERABLE|CVE-', self.last_scan_output))
            self.stats_labels['📊'].config(text=f"📊 {len(self.scan_history) + 1}")
            self.stats_labels['🔓'].config(text=f"🔓 {len(ports)}")
            self.stats_labels['⚠️'].config(text=f"⚠️ {vulns}")
    
    def log_output(self, text, tag='info'):
        if hasattr(self, 'output_text_widget') and self.output_text_widget:
            self.output_text_widget.insert(tk.END, text, tag)
            self.output_text_widget.see(tk.END)
    
    def run_manual_command(self):
        command = self.manual_command_entry.get().strip()
        if not command:
            messagebox.showwarning("No Command", "Please enter a command!")
            return
        if not command.startswith('nmap'):
            messagebox.showwarning("Invalid Command", "Only Nmap commands are supported!")
            return
        if self.output_text_widget:
            self.output_text_widget.delete(1.0, tk.END)
        self.log_output("="*70 + "\n", 'info')
        self.log_output(f"[*] MANUAL SCAN: {datetime.now().strftime('%H:%M:%S')}\n", 'info')
        self.log_output(f"[*] {command}\n", 'info')
        self.log_output("="*70 + "\n\n", 'info')
        if self.command_text_widget:
            self.command_text_widget.delete(1.0, tk.END)
            self.command_text_widget.insert(1.0, command)
        
        def scan():
            process = None
            try:
                start_time = time.time()
                self.is_scanning = True
                self.manual_run_btn.config(state=tk.DISABLED, bg=self.colors['gray'])
                self.run_btn.config(state=tk.DISABLED)
                self.stop_btn.config(state=tk.NORMAL)
                self.status_bar.config(text="🔥 SCANNING...", fg=self.colors['neon_red'])
                self.scan_status.config(text="🔄 SCANNING...", fg=self.colors['neon_gold'])
                self.progress.start()
                
                process = subprocess.Popen(
                    command, shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                self.current_process = process
                
                if process is None:
                    self.log_output("\n[✗] ERROR: Failed to start process\n", 'error')
                    return
                
                lines = []
                while True:
                    if process.poll() is not None:
                        break
                    try:
                        line = process.stdout.readline()
                        if not line:
                            break
                        self.log_output(line, 'output')
                        lines.append(line)
                    except Exception as e:
                        self.log_output(f"\n[!] Read error: {e}\n", 'warning')
                        break
                
                try:
                    stdout, stderr = process.communicate(timeout=5)
                    if stdout:
                        self.log_output(stdout, 'output')
                        lines.append(stdout)
                    if stderr:
                        self.log_output(f"\n[!] {stderr}\n", 'error')
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate()
                    if stdout:
                        self.log_output(stdout, 'output')
                
                self.last_scan_output = ''.join(lines)
                elapsed = time.time() - start_time
                self.progress.stop()
                self.log_output("\n" + "="*70 + "\n", 'info')
                self.log_output(f"[✓] COMPLETED: {elapsed:.2f}s\n", 'success')
                self.status_bar.config(text="✅ READY", fg=self.colors['neon_green'])
                self.scan_status.config(text="✅ COMPLETED", fg=self.colors['neon_green'])
                self.update_stats()
                
                if self.ai_manager and self.last_scan_output:
                    self.ai_manager.update_scan_data(self.last_scan_output)
                    
            except subprocess.TimeoutExpired:
                self.progress.stop()
                self.log_output("\n[✗] ERROR: Scan timed out\n", 'error')
                self.status_bar.config(text="❌ TIMEOUT", fg=self.colors['neon_red'])
                self.scan_status.config(text="❌ TIMEOUT", fg=self.colors['neon_red'])
            except Exception as e:
                self.progress.stop()
                self.log_output(f"\n[✗] ERROR: {str(e)}\n", 'error')
                self.status_bar.config(text="❌ FAILED", fg=self.colors['neon_red'])
                self.scan_status.config(text="❌ FAILED", fg=self.colors['neon_red'])
            finally:
                self.is_scanning = False
                self.manual_run_btn.config(state=tk.NORMAL, bg=self.colors['neon_green'])
                self.run_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                self.current_process = None
                if process and process.poll() is None:
                    try:
                        process.kill()
                    except:
                        pass
        
        threading.Thread(target=scan, daemon=True).start()
    
    def clear_output(self):
        if hasattr(self, 'output_text_widget') and self.output_text_widget:
            self.output_text_widget.delete(1.0, tk.END)
        if hasattr(self, 'command_text_widget') and self.command_text_widget:
            self.command_text_widget.delete(1.0, tk.END)
        self.last_scan_output = ""
        self.status_bar.config(text="✅ CLEARED", fg=self.colors['neon_green'])
        self.scan_status.config(text="🟢 READY", fg=self.colors['neon_green'])
    
    def clear_output_display(self):
        if self.output_text_widget:
            self.output_text_widget.delete(1.0, tk.END)
    
    def copy_output(self):
        if self.output_text_widget:
            text = self.output_text_widget.get(1.0, tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
    
    def save_output_file(self):
        if not self.last_scan_output and not self.output_text_widget:
            messagebox.showwarning("No Data", "Run a scan first!")
            return
        scan_output = self.last_scan_output
        if not scan_output and self.output_text_widget:
            try:
                scan_output = self.output_text_widget.get(1.0, tk.END)
            except:
                pass
        if not scan_output or len(scan_output.strip()) < 10:
            messagebox.showwarning("No Data", "No scan results to save!")
            return
        format_choice = messagebox.askquestion(
            "Save Format",
            "Save as HTML report?\n\nYes = HTML Report\nNo = JSON Report"
        )
        if format_choice == 'yes':
            self._save_as_html(scan_output)
        else:
            self._save_as_json(scan_output)
    
    def _save_as_html(self, scan_output):
        data = self._parse_scan_data(scan_output)
        html = self._create_html_report(data)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_filename = f"hexaradar_report_{timestamp}.html"
        filename = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            initialfile=default_filename
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            webbrowser.open(filename)
            self.log_output(f"\n✅ HTML Report saved: {filename}\n", 'success')
            messagebox.showinfo("Saved", f"HTML Report saved:\n{filename}")
    
    def _save_as_json(self, scan_output):
        data = self._parse_scan_data(scan_output)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_filename = f"hexaradar_report_{timestamp}.json"
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=default_filename
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            self.log_output(f"\n✅ JSON Report saved: {filename}\n", 'success')
            messagebox.showinfo("Saved", f"JSON Report saved:\n{filename}")
    
    def _parse_scan_data(self, text):
        data = {
            'target': 'Unknown',
            'open_ports': [],
            'services': [],
            'critical_count': 0,
            'high_count': 0,
            'medium_count': 0,
            'risk_score': 0,
            'vulnerabilities': [],
            'scan_time': 'Unknown',
            'timestamp': datetime.now().isoformat()
        }
        target_match = re.search(r'Nmap scan report for ([^\s]+)', text)
        if target_match:
            data['target'] = target_match.group(1)
        pattern = r'(\d+)/tcp\s+open\s+(\S+)\s*(.*?)(?:\n|$)'
        matches = re.findall(pattern, text, re.IGNORECASE)
        critical_ports = [445, 3389, 23, 21, 512, 513, 514, 1524, 6667]
        high_ports = [22, 3306, 5432, 5900, 139]
        for port, service, version in matches:
            port_num = int(port)
            version = version.strip()
            if version:
                version_parts = version.split()
                version = version_parts[0] if version_parts else version
            data['open_ports'].append({'port': port_num, 'service': service, 'version': version})
            data['services'].append(service)
            if port_num in critical_ports:
                data['critical_count'] += 1
            elif port_num in high_ports:
                data['high_count'] += 1
            else:
                data['medium_count'] += 1
        data['risk_score'] = min(100, (data['critical_count'] * 15) + (data['high_count'] * 10) + (data['medium_count'] * 5))
        time_match = re.search(r'Nmap done:.*?(\d+\.\d+)\s+seconds', text)
        if time_match:
            data['scan_time'] = f"{time_match.group(1)} seconds"
        vuln_pattern = r'VULNERABLE|CVE-\d{4}-\d{4,}'
        vulns = re.findall(vuln_pattern, text, re.IGNORECASE)
        data['vulnerabilities'] = list(set(vulns))
        return data
    
    def _create_html_report(self, data):
        risk_level = "LOW"
        risk_color = "#00ff88"
        if data['risk_score'] >= 70:
            risk_level = "CRITICAL"
            risk_color = "#ff1744"
        elif data['risk_score'] >= 50:
            risk_level = "HIGH"
            risk_color = "#ff6b35"
        elif data['risk_score'] >= 30:
            risk_level = "MEDIUM"
            risk_color = "#ffd700"
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HEXARADAR - Security Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Courier New', monospace;
            background: #0a0a0f;
            color: #00e5ff;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: #0f0f1a;
            border: 1px solid #ffd700;
            border-radius: 10px;
            padding: 25px;
        }}
        .header {{
            text-align: center;
            padding: 20px;
            border-bottom: 2px solid #ffd700;
            margin-bottom: 20px;
        }}
        .header h1 {{
            font-size: 2.5em;
            color: #ffd700;
            text-shadow: 0 0 20px rgba(255,215,0,0.3);
        }}
        .section {{
            background: #141420;
            padding: 15px 20px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #ffd700;
        }}
        .section h2 {{ color: #ffd700; margin-bottom: 10px; }}
        .risk-box {{
            background: {risk_color};
            color: #0a0a0f;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            font-size: 1.2em;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }}
        .stat-card {{
            background: #0a0a0f;
            border: 1px solid #ffd700;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }}
        .stat-card .number {{ font-size: 2em; font-weight: bold; }}
        .stat-card .label {{ color: #7a7a9a; font-size: 0.8em; }}
        .port-list {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
            margin: 10px 0;
        }}
        .port-item {{
            background: #0a0a0f;
            padding: 8px 12px;
            border-radius: 4px;
            border-left: 3px solid #ffd700;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            border-top: 1px solid #ffd700;
            margin-top: 20px;
            font-size: 0.8em;
            color: #7a7a9a;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ HEXARADAR</h1>
            <div style="margin-top:10px;color:#7a7a9a;font-size:0.9em;">
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        <div class="risk-box">
            Risk Score: {data['risk_score']}/100 - {risk_level}
        </div>
        <div class="section">
            <h2>🎯 Target</h2>
            <p><strong>Target:</strong> {data['target']}</p>
            <p><strong>Scan Time:</strong> {data['scan_time']}</p>
        </div>
        <div class="section">
            <h2>📊 Summary</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="number">{len(data['open_ports'])}</div>
                    <div class="label">Open Ports</div>
                </div>
                <div class="stat-card">
                    <div class="number" style="color:#ff1744;">{data['critical_count']}</div>
                    <div class="label">🔴 Critical</div>
                </div>
                <div class="stat-card">
                    <div class="number" style="color:#ff6b35;">{data['high_count']}</div>
                    <div class="label">🟠 High</div>
                </div>
                <div class="stat-card">
                    <div class="number" style="color:#ffd700;">{data['medium_count']}</div>
                    <div class="label">🟡 Medium</div>
                </div>
            </div>
        </div>
        <div class="section">
            <h2>🔌 Open Ports</h2>
            <div class="port-list">
                {''.join([f'<div class="port-item">{p["port"]}/{p["service"]}</div>' for p in data['open_ports'][:30]])}
            </div>
        </div>
        <div class="footer">
            HEXARADAR v3.0 - Security Report
        </div>
    </div>
</body>
</html>"""
        return html
    
    # ========== UPDATE OUTPUT QUEUE ==========
    def update_output_queue(self):
        self.root.after(100, self.update_output_queue)
    
    # ========== RUN ==========
    def run(self):
        self.root.mainloop()
