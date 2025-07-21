# 🔫 GUN WiFi Tool - Quick Setup Guide

## 🚀 One-Line Installation

For most Linux distributions (Ubuntu, Debian, Kali):
```bash
curl -fsSL https://raw.githubusercontent.com/gun-wifi/tool/main/install.sh | bash
```

Or download and run locally:
```bash
wget https://raw.githubusercontent.com/gun-wifi/tool/main/install.sh
chmod +x install.sh
./install.sh
```

## 📦 Manual Installation Options

### Option 1: Automated Installer (Recommended)
```bash
./install.sh
```

### Option 2: Package Manager (Debian/Ubuntu/Kali)
```bash
# System packages
sudo apt update
sudo apt install -y aircrack-ng hostapd dnsmasq iptables wireless-tools iw python3-qrcode python3-pil

# Python packages
pip install -r requirements.txt
```

### Option 3: Virtual Environment
```bash
python3 -m venv gun_wifi_env
source gun_wifi_env/bin/activate
pip install -r requirements.txt
```

### Option 4: Docker Installation
```bash
docker build -t gun-wifi-tool .
docker run -it --privileged --net=host gun-wifi-tool
```

## 🔧 Quick Verification

Test if installation worked:
```bash
python3 gun_wifi_tool.py --help
```

## 🆘 Common Issues & Solutions

### Issue 1: `qrcode` package error
```bash
# Solution 1: Use system package
sudo apt install python3-qrcode

# Solution 2: Use virtual environment
python3 -m venv env && source env/bin/activate && pip install qrcode
```

### Issue 2: Permission errors
```bash
# Solution: Run with sudo for WiFi operations
sudo python3 gun_wifi_tool.py
```

### Issue 3: Monitor mode not supported
```bash
# Check WiFi adapter
iwconfig
# Look for monitor mode support in driver
```

## 🎯 Quick Start Commands

```bash
# 1. Scan available networks
sudo python3 gun_wifi_tool.py --scan

# 2. Interactive mode (easiest)
sudo python3 gun_wifi_tool.py --interactive

# 3. Setup monitor mode
sudo python3 gun_wifi_tool.py --monitor

# 4. Help and options
python3 gun_wifi_tool.py --help
```

## ⚖️ Legal Notice

⚠️ **IMPORTANT**: This tool is for authorized security testing only!
- Only use on networks you own or have explicit permission to test
- Follow your local laws and regulations
- Use for educational and ethical purposes only
- The developers are not responsible for misuse

## 🔗 Support

- 📖 Full documentation: `USAGE.md`
- 🐛 Report issues: Create GitHub issue
- 💬 Community: Join our security testing community
- 📧 Contact: security@gun-wifi-tool.com

---
**GUN WiFi Tool v3.0** - Professional WiFi Penetration Testing Suite
