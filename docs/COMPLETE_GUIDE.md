# 🔫 GUN WiFi Tool - Complete Installation & Setup Guide

## 📋 Project Overview

**GUN WiFi Tool v3.0** is a comprehensive WiFi penetration testing suite designed for security professionals and ethical hackers. The tool provides advanced capabilities for network security testing with a focus on professional-grade features and safety.

### 🎯 Key Features
- **Deauthentication Attacks**: Professional WiFi disconnection testing
- **Evil Twin AP**: Rogue access point creation and management
- **Captive Portal**: Custom authentication page deployment
- **Monitor Mode**: Advanced wireless interface management
- **QR Code Integration**: Mobile device testing capabilities
- **Comprehensive Logging**: Detailed attack and security logs
- **Safety Features**: Built-in protections and ethical guidelines

## 🛠️ Installation Methods

### 🚀 Method 1: Automated Installer (Recommended)
```bash
# Download and run the installer
curl -fsSL https://raw.githubusercontent.com/teotiaabhi/gun-wifi-tool/main/install.sh | bash

# Or download locally
wget https://raw.githubusercontent.com/teotiaabhi/gun-wifi-tool/main/install.sh
chmod +x install.sh
./install.sh
```

### 📦 Method 2: Manual Installation
```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install system dependencies
sudo apt install -y aircrack-ng hostapd dnsmasq iptables wireless-tools iw python3-qrcode python3-pil macchanger tcpdump

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Verify installation
python3 gun_wifi_tool.py --help
```

### 🐳 Method 3: Docker Installation
```bash
# Build Docker image
docker build -t gun-wifi-tool .

# Run with network access
docker run -it --privileged --net=host gun-wifi-tool
```

### 🌐 Method 4: Virtual Environment
```bash
# Create virtual environment
python3 -m venv gun_wifi_env
source gun_wifi_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Usage
python3 gun_wifi_tool.py
```

## 🔧 System Requirements

### Minimum Requirements
- **OS**: Linux (Ubuntu 18+, Debian 10+, Kali Linux, Arch Linux)
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 1GB free space
- **Network**: WiFi adapter with monitor mode support

### Recommended Setup
- **OS**: Kali Linux 2024.1+ (optimal compatibility)
- **Python**: 3.13+ (latest features)
- **RAM**: 8GB for optimal performance
- **WiFi Adapter**: External USB adapter with AP mode support
- **CPU**: Multi-core processor for concurrent operations

## 📁 File Structure

```
gun-wifi-tool/
├── gun_wifi_tool.py          # Main application
├── requirements.txt          # Python dependencies
├── install.sh               # Automated installer
├── QUICK_SETUP.md           # Quick start guide
├── USAGE.md                 # Detailed usage instructions
├── test_gun_wifi_tool.py    # Unit tests
├── live_attack_testing.py   # Live function tests
├── interactive_attack_demo.py # Interactive demo
├── security_analysis.py     # Security analysis
├── generate_test_report.py  # Test reporting
└── __pycache__/             # Python cache files
```

## 🎯 Quick Start Commands

### Basic Usage
```bash
# Show help and options
python3 gun_wifi_tool.py --help

# Interactive mode (easiest for beginners)
sudo python3 gun_wifi_tool.py --interactive

# Scan available networks
sudo python3 gun_wifi_tool.py --scan

# Setup monitor mode
sudo python3 gun_wifi_tool.py --monitor
```

### Advanced Operations
```bash
# Deauthentication attack
sudo python3 gun_wifi_tool.py --deauth --target AA:BB:CC:DD:EE:FF

# Evil twin attack
sudo python3 gun_wifi_tool.py --evil-twin --ssid "TestNetwork"

# Captive portal
sudo python3 gun_wifi_tool.py --captive-portal --template corporate
```

## 🔍 Testing & Verification

### Automated Testing Suite
```bash
# Run unit tests
python3 test_gun_wifi_tool.py

# Live function testing
python3 live_attack_testing.py

# Interactive demo
python3 interactive_attack_demo.py
```

### Security Analysis
```bash
# Code security analysis
python3 security_analysis.py

# Generate test report
python3 generate_test_report.py
```

## 🛠️ Troubleshooting

### Common Issues & Solutions

#### 1. QR Code Package Error
```bash
# Error: "No module named 'qrcode'"
# Solution 1: Use system package
sudo apt install python3-qrcode

# Solution 2: Use pip in virtual environment
python3 -m venv env
source env/bin/activate
pip install qrcode
```

#### 2. Permission Denied
```bash
# Error: "Operation not permitted"
# Solution: Run with sudo for WiFi operations
sudo python3 gun_wifi_tool.py
```

#### 3. Monitor Mode Not Supported
```bash
# Check WiFi adapter capabilities
iwconfig
lsusb | grep -i wireless

# Recommended adapters:
# - Alfa AWUS036ACS
# - Panda PAU09
# - TP-Link AC600T2U Plus
```

#### 4. Dependencies Installation Failed
```bash
# Error: "externally-managed-environment"
# Solution 1: Use virtual environment
python3 -m venv gun_wifi_env
source gun_wifi_env/bin/activate
pip install -r requirements.txt

# Solution 2: Use system packages
sudo apt install python3-scapy python3-flask python3-requests
```

#### 5. Network Interface Issues
```bash
# Check network interfaces
ip link show
iwconfig

# Restart network manager
sudo systemctl restart NetworkManager

# Manual interface setup
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
```

## 🔒 Security & Legal Guidelines

### ⚖️ Legal Requirements
- ✅ **Only use on networks you own or have explicit written permission to test**
- ✅ **Follow local laws and regulations regarding wireless security testing**
- ✅ **Obtain proper authorization before conducting any security tests**
- ✅ **Use for educational and ethical purposes only**
- ❌ **Never use for unauthorized access or malicious activities**

### 🛡️ Ethical Guidelines
1. **Responsible Disclosure**: Report vulnerabilities to network owners
2. **Minimal Impact**: Conduct tests with minimal disruption
3. **Documentation**: Maintain detailed logs of all testing activities
4. **Professional Use**: Use only in professional security assessments

### 🔐 Security Best Practices
- Keep tool updated to latest version
- Use strong authentication for your testing environment
- Secure your testing data and logs
- Follow industry standard penetration testing methodologies

## 📊 Performance Optimization

### System Optimization
```bash
# Increase system limits
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Optimize network stack
echo "net.core.rmem_max = 134217728" | sudo tee -a /etc/sysctl.conf
echo "net.core.wmem_max = 134217728" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Tool Configuration
```bash
# Enable verbose logging
export GUN_WIFI_DEBUG=1

# Set custom interface
export GUN_WIFI_INTERFACE=wlan0

# Performance mode
export GUN_WIFI_PERFORMANCE=1
```

## 📞 Support & Community

### Getting Help
- 📖 **Documentation**: Read USAGE.md for detailed instructions
- 🐛 **Bug Reports**: Create GitHub issues for problems
- 💬 **Community**: Join security testing forums
- 📧 **Contact**: security@gun-wifi-tool.com

### Contributing
- Fork the repository
- Create feature branches
- Submit pull requests
- Follow coding standards
- Include comprehensive tests

## 📝 Version History

### v3.0 (Current)
- ✅ Comprehensive installation system
- ✅ Enhanced error handling
- ✅ Virtual environment support
- ✅ Docker containerization
- ✅ Automated testing suite
- ✅ Security analysis integration

### v2.x
- Basic WiFi attack capabilities
- Manual installation process
- Limited error handling

## 🔄 Updates & Maintenance

### Checking for Updates
```bash
# Check current version
python3 gun_wifi_tool.py --version

# Download latest version
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade
```

### Backup & Recovery
```bash
# Backup configuration
cp -r ~/.gun-wifi-tool ~/.gun-wifi-tool.backup

# Restore configuration
cp -r ~/.gun-wifi-tool.backup ~/.gun-wifi-tool
```

---

## 📜 License & Disclaimer

**GUN WiFi Tool** is released under the MIT License for educational and professional security testing purposes.

**⚠️ IMPORTANT DISCLAIMER**: This tool is designed for authorized security testing only. Users are responsible for complying with all applicable laws and regulations. The developers are not responsible for any misuse or damage caused by this tool.

**© 2024 GUN WiFi Tool Development Team. All rights reserved.**

---

*For the latest updates and documentation, visit: https://github.com/teotiaabhi/gun-wifi-tool*
