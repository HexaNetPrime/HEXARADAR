# ⚡ HEXARADAR v3.0

### AI-Powered Network Security Scanner | Offline | No API Required

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Nmap](https://img.shields.io/badge/Nmap-7.80+-red.svg)](https://nmap.org/)
[![AI](https://img.shields.io/badge/AI-Powered-purple.svg)]()
[![Offline](https://img.shields.io/badge/Offline-Yes-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20Mac-lightgrey.svg)]()

---

## 📌 Table of Contents

- [🌟 Introduction](#-introduction)
- [🚀 Features](#-features)
- [📸 Screenshots](#-screenshots)
- [🛠️ Installation](#️-installation)
- [📖 Usage Guide](#-usage-guide)
- [📂 Project Structure](#-project-structure)
- [🤖 AI Features Details](#-ai-features-details)
- [📊 ML Module](#-ml-module)
- [🛡️ Evasion Techniques](#️-evasion-techniques)
- [📚 CVE Database](#-cve-database)
- [⚠️ Disclaimer](#️-disclaimer)
- [📝 License](#-license)
- [👨‍💻 Author](#-author)

---

## 🌟 Introduction

**HEXARADAR v3.0** is a **complete AI-Powered Network Security Scanner** built with Python and Tkinter. It combines **Nmap scanning** with **Artificial Intelligence** to provide:

- 🔮 **Vulnerability Prediction** with CVSS scoring
- 🌐 **Network Mapping** and topology discovery
- 🔍 **OSINT** (Open Source Intelligence) gathering
- 📊 **Data Analytics** and compliance checking
- 🛡️ **Evasion Techniques** for IDS/IPS bypass
- 🧠 **Machine Learning** vulnerability prediction

> ✅ **100% Offline** - No Internet connection or API required!
> ✅ **Open Source** - Free to use, modify, and distribute!

---

## 🚀 Features

### 🏠 **MAIN Tab** - Scanning Hub
| Feature | Description |
|---------|-------------|
| 🎯 Target Input | IP, Domain, Subnet (e.g., 192.168.1.0/24) |
| 🚀 ULTRA Scan | Fastest scan - 5-10 seconds |
| ⚡ FAST Scan | Quick port scan - 15-30 seconds |
| 📋 LIST Scan | Host listing - <2 seconds |
| 🛡️ STEALTH Scan | Slow scan to evade IDS |
| 🔍 FULL Scan | Complete scan: -p- -sV -sC |
| 60+ Nmap Commands | 11 categories organized |

### 📊 **OUTPUT Tab** - Console Output
| Feature | Description |
|---------|-------------|
| 📝 Manual Command | Run custom nmap commands |
| 📊 Live Output | Real-time scan results |
| 🗑️ CLEAR | Clear output display |
| 📋 COPY | Copy output to clipboard |
| 💾 SAVE | Save as HTML/JSON report |

### 🤖 **AI Tab** - 5 AI Features

#### 1. 🔮 **Advanced AI Engine**
- Vulnerability Prediction (CVSS-based scoring)
- Smart Scan Optimization (network-aware)
- Anomaly Detection (backdoors, botnets)
- CVE Database Search (90+ CVEs)
- Full AI Security Report

#### 2. 🌐 **Network Mapping**
- Discover Live Hosts
- Topology Mapping (traceroute)
- Service Dependency Analysis
- Attack Surface Detection
- Live Host Tracking

#### 3. 🔍 **Advanced Discovery (OSINT)**
- WHOIS Lookup
- DNS Records (A, MX, NS, TXT)
- Email Enumeration
- Technology Fingerprinting (CMS, JS, Server)
- Cloud Provider Detection (AWS, Azure, GCP)

#### 4. 📊 **Data Analytics**
- 30-Day Trend Analysis
- Auto Risk Scoring (0-100)
- Compliance Checks (PCI-DSS, HIPAA, GDPR, ISO)
- SLA Monitoring
- 7-Day Predictive Analysis

#### 5. 🛡️ **Evasion Techniques**
- Proxy Chains (Tor/SOCKS5/HTTP)
- VPN Rotation
- MAC Randomization
- Traffic Shaping (delay/rate control)
- IDS/IPS Detection

### 🌐 **NETWORK Tab** - Direct Network Mapping
- Discover Hosts
- Topology Map
- Service Dependencies
- Attack Surface
- Live Tracking
- STOP ALL Button

### 🔍 **OSINT Tab** - Direct OSINT
- Full OSINT Scan
- Email Enumeration
- Technology Fingerprinting
- Cloud Discovery
- Export Results

### 📊 **ANALYTICS Tab** - Direct Analytics
- Trend Analysis
- Risk Scoring
- Compliance Check
- SLA Monitoring
- Predictive Analysis

### 🛡️ **EVASION Tab** - Direct Evasion
- Proxy Chains
- VPN Rotation
- MAC Randomization
- Traffic Shaping
- IDS/IPS Detection

### 🧠 **ML Tab** - Deep Learning
- ML Vulnerability Prediction (Random Forest)
- Model Retraining
- Model Accuracy Check
- Export Predictions

---

## 📸 Screenshots

### Main Tab
![Main Tab](screenshots/main.png)

### AI Tab
![AI Tab](screenshots/ai.png)

### ML Tab
![ML Tab](screenshots/ml.png)

### Network Tab
![Network Tab](screenshots/network.png)

---

## 🛠️ Installation

### 📦 **Requirements**

| Requirement | Version |
|-------------|---------|
| Python | 3.6+ |
| Nmap | 7.80+ |
| Tkinter | Built-in |
| OS | Linux/Windows/Mac |

### 🐍 **Python Dependencies**

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install manually
pip install python-whois dnspython requests scikit-learn numpy
