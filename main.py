#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HEXARADAR v3.0 - COMPLETE EDITION
✅ CNN Neural Network Integration
✅ TensorFlow Deep Learning
✅ 6 AI Features + ML + CNN
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check all required dependencies"""
    print("\n" + "="*70)
    print("🔍 CHECKING DEPENDENCIES...")
    print("="*70)
    
    missing_deps = []
    optional_deps = []
    
    # ========== Check Python version ==========
    print(f"\n🐍 Python Version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print("   💡 Upgrade: https://www.python.org/downloads/")
        sys.exit(1)
    else:
        print("✅ Python version OK")
    
    # ========== Check Nmap ==========
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
    
    # ========== Check Tkinter ==========
    print("\n🖥️ Checking Tkinter...")
    try:
        import tkinter
        print("✅ Tkinter is installed")
    except ImportError:
        print("❌ Tkinter is not installed!")
        missing_deps.append("tkinter")
    
    # ========== Check scikit-learn (ML) ==========
    print("\n🤖 Checking scikit-learn...")
    try:
        import sklearn
        print(f"✅ scikit-learn is installed (version: {sklearn.__version__})")
    except ImportError:
        print("⚠️ scikit-learn is not installed (ML features will be limited)")
        optional_deps.append("scikit-learn")
    
    # ========== ✅ Check TensorFlow (CNN) ==========
    print("\n🧠 Checking TensorFlow (CNN)...")
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow is installed (version: {tf.__version__})")
        
        # Check if GPU is available
        gpu_available = tf.config.list_physical_devices('GPU')
        if gpu_available:
            print(f"   🚀 GPU Available: {len(gpu_available)} GPU(s) detected")
        else:
            print("   💻 CPU Mode (GPU not detected)")
            
    except ImportError:
        print("⚠️ TensorFlow is not installed (CNN features will be disabled)")
        print("   💡 Install: pip install tensorflow")
        optional_deps.append("tensorflow")
    
    # ========== Check bcrypt (optional) ==========
    print("\n🔐 Checking bcrypt...")
    try:
        import bcrypt
        print("✅ bcrypt is installed")
    except ImportError:
        print("⚠️ bcrypt is not installed (optional, using PBKDF2 fallback)")
        print("   💡 Install: pip install bcrypt")
    
    # ========== Check other modules ==========
    print("\n📦 Checking Python modules...")
    modules = [
        'dns.resolver',      # dnspython
        'cryptography',      # cryptography
        'requests',          # requests
        'whois',             # python-whois
        'numpy',             # numpy (ML)
    ]
    
    for mod in modules:
        try:
            __import__(mod)
            print(f"   ✅ {mod} is installed")
        except ImportError:
            print(f"   ⚠️ {mod} is not installed")
            optional_deps.append(mod)
    
    # ========== Check Numpy (required for ML) ==========
    try:
        import numpy as np
        print(f"   ✅ numpy is installed (version: {np.__version__})")
    except ImportError:
        print("   ⚠️ numpy is not installed (ML features will be limited)")
        optional_deps.append("numpy")
    
    # ========== Summary ==========
    print("\n" + "="*70)
    print("📊 DEPENDENCY SUMMARY")
    print("="*70)
    
    if missing_deps:
        print("\n❌ MISSING DEPENDENCIES (Required):")
        for dep in missing_deps:
            print(f"   • {dep}")
        print("\n💡 Please install missing dependencies and try again.")
        return False
    
    if optional_deps:
        print("\n⚠️ OPTIONAL DEPENDENCIES (Some features may be limited):")
        for dep in optional_deps:
            print(f"   • {dep}")
        print("\n💡 Recommended: pip install -r requirements.txt")
    
    print("\n✅ ALL REQUIRED DEPENDENCIES SATISFIED!")
    
    # ========== Show CNN Status ==========
    try:
        import tensorflow as tf
        print("\n🧠 CNN STATUS: ✅ AVAILABLE")
        print(f"   TensorFlow Version: {tf.__version__}")
        gpu = tf.config.list_physical_devices('GPU')
        if gpu:
            print(f"   🚀 GPU Acceleration: ENABLED ({len(gpu)} GPU)")
        else:
            print(f"   💻 GPU Acceleration: DISABLED (CPU Mode)")
    except:
        print("\n🧠 CNN STATUS: ❌ NOT AVAILABLE")
        print("   💡 Install: pip install tensorflow")
    
    return True

def show_banner():
    """Show HexaRadar banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                               ║
    ║   ██╗  ██╗███████╗██╗  ██╗ █████╗ ██████╗  █████╗ ██████╗  █████╗ ██████╗  ║
    ║   ██║  ██║██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗ ║
    ║   ███████║█████╗   ╚███╔╝ ███████║██████╔╝███████║██║  ██║███████║██████╔╝ ║
    ║   ██╔══██║██╔══╝   ██╔██╗ ██╔══██║██╔══██╗██╔══██║██║  ██║██╔══██║██╔══██╗ ║
    ║   ██║  ██║███████╗██╔╝ ██╗██║  ██║██║  ██║██║  ██║██████╔╝██║  ██║██║  ██║ ║
    ║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ║
    ║                                                                               ║
    ║                     ╔═══════════════════════════════════════════╗              ║
    ║                     ║         H E X A R A D A R                ║              ║
    ║                     ║    ULTIMATE NETWORK SCANNER v3.0        ║              ║
    ║                     ║  [ FAST | STEALTH | PROFESSIONAL ]      ║              ║
    ║                     ╚═══════════════════════════════════════════╝              ║
    ║                                                                               ║
    ║   ⚡ Features:                                                                 ║
    ║   • AI-Powered Vulnerability Detection (ML + CNN)                            ║
    ║   • 6 AI Features with Neural Network (CNN)                                  ║
    ║   • 11 Scan Tabs with 60+ Nmap Options                                       ║
    ║   • Advanced Reporting (HTML/JSON/CSV)                                      ║
    ║   • Offline OSINT (WHOIS, DNS, Email, Cloud)                                ║
    ║   • Data Analytics (Trend, Risk, Compliance, SLA, Predict)                  ║
    ║   • Evasion Techniques (Proxy, VPN, MAC, Traffic Shaping, IDS)              ║
    ║   • Deep Learning (CNN + Random Forest Ensemble)                            ║
    ║                                                                               ║
    ║   💡 Quick Actions:                                                          ║
    ║   • 🚀 ULTRA FAST SCAN - 5-10 seconds                                        ║
    ║   • ⚡ FAST PORT SCAN - 15-30 seconds                                        ║
    ║   • 📋 LIST SCAN - <2 seconds                                                ║
    ║   • 🔍 FULL SCAN - 3-5 minutes                                               ║
    ║                                                                               ║
    ║   🧠 AI Features:                                                            ║
    ║   • 🤖 Advanced AI Engine (Vuln Prediction + CVE DB)                         ║
    ║   • 🌐 Network Mapping (Discover + Topology + Attack Surface)               ║
    ║   • 🔍 OSINT (WHOIS + DNS + Email + Tech + Cloud)                           ║
    ║   • 📊 Data Analytics (Trend + Risk + Compliance + SLA + Predict)           ║
    ║   • 🛡️ Evasion Techniques (Proxy + VPN + MAC + Traffic + IDS)               ║
    ║   • 🧠 CNN Prediction (Deep Learning + Ensemble)                            ║
    ║                                                                               ║
    ║   ⚠️  USE RESPONSIBLY - ONLY ON AUTHORIZED SYSTEMS                         ║
    ║                                                                               ║
    ╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def show_cnn_status():
    """Show CNN/TensorFlow status"""
    print("\n" + "="*70)
    print("🧠 CNN / TENSORFLOW STATUS")
    print("="*70)
    
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow Version: {tf.__version__}")
        
        # Check GPU
        gpu_devices = tf.config.list_physical_devices('GPU')
        if gpu_devices:
            print(f"🚀 GPU Acceleration: ENABLED ({len(gpu_devices)} GPU(s))")
            for i, gpu in enumerate(gpu_devices):
                print(f"   GPU {i}: {gpu.name}")
        else:
            print("💻 GPU Acceleration: DISABLED (Running on CPU)")
            
        # Check if CNN model exists
        cnn_model_path = "data/cnn_model.h5"
        if os.path.exists(cnn_model_path):
            size = os.path.getsize(cnn_model_path)
            print(f"✅ CNN Model: FOUND ({size} bytes)")
        else:
            print("⚠️ CNN Model: NOT FOUND (Will be created on first run)")
            
        # Check training data
        training_data_path = "data/cnn_training_data.json"
        if os.path.exists(training_data_path):
            import json
            with open(training_data_path, 'r') as f:
                data = json.load(f)
                count = len(data.get('training_data', []))
            print(f"✅ Training Data: FOUND ({count} samples)")
        else:
            print("⚠️ Training Data: NOT FOUND (Will be created on first run)")
            
    except ImportError:
        print("❌ TensorFlow: NOT INSTALLED")
        print("   💡 Install: pip install tensorflow")
        print("   ⚠️ CNN features will be disabled")
    
    print("="*70)

def main():
    """Main entry point"""
    try:
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Show banner
        show_banner()
        
        print("\n🚀 LOADING HEXARADAR v3.0...")
        print("="*70)
        
        # Check dependencies
        if not check_dependencies():
            print("\n❌ Please install missing dependencies and try again.")
            print("\n💡 Installation commands:")
            print("   pip install -r requirements.txt")
            print("   pip install tensorflow  # For CNN features")
            input("\nPress Enter to exit...")
            sys.exit(1)
        
        # Show CNN status
        show_cnn_status()
        
        # Import GUI
        try:
            from gui import NmapGUI
        except ImportError as e:
            print(f"\n❌ IMPORT ERROR: {e}")
            print("\n💡 Make sure all required files are in the same directory:")
            print("   • gui.py")
            print("   • ai_features_manager.py")
            print("   • nmap_commands.py")
            print("   • features/ (folder with all feature files)")
            print("   • data/ (folder with JSON databases)")
            input("\nPress Enter to exit...")
            sys.exit(1)
        
        print("\n✅ INITIALIZING INTERFACE...")
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
        print("   💡 Recommended: sudo python3 main.py")
        print("   ⚠️ MAC Randomization and some evasion techniques require root")
        print("\n   Press Enter to continue without root, or Ctrl+C to exit...")
        try:
            input()
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
    
    main()
