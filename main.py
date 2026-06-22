#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import subprocess

def check_dependencies():
    """Check all required dependencies"""
    print("\n" + "="*70)
    print("🔍 CHECKING DEPENDENCIES...")
    print("="*70)
    
    missing_deps = []
    
    # Check Python version
    print(f"\n🐍 Python Version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required!")
        sys.exit(1)
    else:
        print("✅ Python version OK")
    
    # Check nmap
    print("\n📡 Checking Nmap...")
    try:
        result = subprocess.run(['nmap', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ {version_line}")
        else:
            print("❌ Nmap is not installed!")
            missing_deps.append("nmap")
    except FileNotFoundError:
        print("❌ Nmap not found!")
        missing_deps.append("nmap")
    
    # Check tkinter
    print("\n🖥️ Checking Tkinter...")
    try:
        import tkinter
        print("✅ Tkinter is installed")
    except ImportError:
        print("❌ Tkinter is not installed!")
        missing_deps.append("tkinter")
    
    # Check bcrypt (optional)
    print("\n🔐 Checking bcrypt...")
    try:
        import bcrypt
        print("✅ bcrypt is installed")
    except ImportError:
        print("⚠️ bcrypt is not installed (optional, using PBKDF2 fallback)")
        print("   Install: pip install bcrypt")
    
    # Check other modules
    print("\n📦 Checking Python modules...")
    modules = ['dns.resolver', 'cryptography', 'requests']
    for mod in modules:
        try:
            __import__(mod)
            print(f"   ✅ {mod} is installed")
        except ImportError:
            print(f"   ⚠️ {mod} is not installed")
            missing_deps.append(mod)
    
    if missing_deps:
        print("\n⚠️ MISSING DEPENDENCIES:")
        for dep in missing_deps:
            print(f"   • {dep}")
        return False
    
    print("\n✅ ALL DEPENDENCIES SATISFIED!")
    return True

def show_banner():
    """Show HexaRadar banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════════╗
    ║                                                                                  ║
    ║   ██╗  ██╗███████╗██╗  ██╗ █████╗ ██████╗  █████╗ ██████╗                      ║
    ║   ██║  ██║██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗                     ║
    ║   ███████║█████╗   ╚███╔╝ ███████║██████╔╝███████║██║  ██║                     ║
    ║   ██╔══██║██╔══╝   ██╔██╗ ██╔══██║██╔══██╗██╔══██║██║  ██║                     ║
    ║   ██║  ██║███████╗██╔╝ ██╗██║  ██║██║  ██║██║  ██║██████╔╝                     ║
    ║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝                      ║
    ║                                                                                  ║
    ║                     ╔═══════════════════════════════════════╗                     ║
    ║                     ║         H E X A R A D A R            ║                     ║
    ║                     ║    ULTIMATE NETWORK SCANNER v2.0    ║                     ║
    ║                     ║  [ FAST | STEALTH | PROFESSIONAL ]  ║                     ║
    ║                     ╚═══════════════════════════════════════╝                     ║
    ║                                                                                  ║
    ║   ⚡ Features:                                                                   ║
    ║   • AI-Powered Vulnerability Detection                                           ║
    ║   • 11 Scan Tabs with 60+ Nmap Options                                           ║
    ║   • 12 AI Dashboard Tabs                                                         ║
    ║   • Advanced Reporting (HTML/CSV/JSON/XML/TXT)                                   ║
    ║   • Gamification with Achievements & Leaderboard                                 ║
    ║   • Encrypted Storage & Audit Logging                                            ║
    ║   • Bluetooth, WiFi, IPv6, IoT Scanning                                          ║
    ║   • Separate Output Window                                                       ║
    ║                                                                                  ║
    ║   💡 Quick Actions:                                                              ║
    ║   • 🚀 ULTRA FAST SCAN - 1 second                                               ║
    ║   • ⚡ FAST PORT SCAN - 2-3 seconds                                             ║
    ║   • 📋 LIST SCAN - <1 second                                                    ║
    ║                                                                                  ║
    ║   ⚠️  USE RESPONSIBLY - ONLY ON AUTHORIZED SYSTEMS                             ║
    ║                                                                                  ║
    ╚══════════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main entry point"""
    try:
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Show banner
        show_banner()
        
        print("\n🚀 LOADING HEXARADAR v2.0...")
        print("="*70)
        
        # Check dependencies
        if not check_dependencies():
            print("\n❌ Please install missing dependencies and try again.")
            input("\nPress Enter to exit...")
            sys.exit(1)
        
        # Import GUI
        try:
            from gui import NmapGUI
        except ImportError as e:
            print(f"\n❌ IMPORT ERROR: {e}")
            print("\n💡 Make sure all required files are in the same directory:")
            print("   • gui.py")
            print("   • ai_dashboard.py")
            print("   • security_features.py")
            print("   • advanced_scanning.py")
            print("   • gamification.py")
            print("   • advanced_reporting.py")
            print("   • network_mapping.py")
            print("   • advanced_discovery.py")
            print("   • and all other .py files")
            input("\nPress Enter to exit...")
            sys.exit(1)
        
        print("\n✨ INITIALIZING INTERFACE...")
        print("="*70 + "\n")
        
        # Create and run GUI
        app = NmapGUI()
        app.run()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Program interrupted by user!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    # Check for root privileges
    if os.name == 'posix' and os.geteuid() != 0:
        print("\n⚠️ Running without root privileges! Some features may not work.")
        print("   Recommended: sudo python3 main.py\n")
        print("   Press Enter to continue without root, or Ctrl+C to exit...")
        try:
            input()
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
    
    main()
