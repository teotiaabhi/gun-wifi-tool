# 🔫 GUN WiFi Tool - Complete Step-by-Step User Guide

## 📋 **Pre-Installation Requirements**

### System Check
```bash
# Check if you have Linux
uname -a

# Check Python version (should be 3.8+)
python3 --version

# Check if you have WiFi adapter
iwconfig
```

### Required Hardware
- **WiFi Adapter**: USB WiFi adapter with monitor mode support
- **Recommended Adapters**:
  - Alfa AWUS036ACS
  - Panda PAU09
  - TP-Link AC600T2U Plus

---

## 🚀 **Method 1: One-Line Installation (Easiest)**

### Step 1: Download and Run Installer
```bash
# Download and run installer automatically
curl -fsSL https://raw.githubusercontent.com/teotiaabhi/gun-wifi-tool/main/install.sh | bash
```

### Step 2: Follow Prompts
- Installer will ask for sudo password
- Choose **Y** for virtual environment (recommended)
- Wait for installation to complete

### Step 3: Verify Installation
```bash
# Test if tool works
python3 gun_wifi_tool.py --help
```

---

## 📦 **Method 2: Manual Installation**

### Step 1: Clone Repository
```bash
# Download the tool
git clone https://github.com/teotiaabhi/gun-wifi-tool.git
cd gun-wifi-tool
```

### Step 2: Run Installer
```bash
# Make installer executable
chmod +x install.sh

# Run installer
./install.sh
```

### Step 3: Manual Dependencies (if installer fails)
```bash
# System packages
sudo apt update
sudo apt install -y aircrack-ng hostapd dnsmasq iptables wireless-tools iw python3-qrcode

# Python packages
pip install -r requirements.txt
```

---

## 🐳 **Method 3: Docker Installation**

### Step 1: Install Docker
```bash
# Install Docker (Ubuntu/Debian)
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER
```

### Step 2: Build and Run
```bash
# Clone repository
git clone https://github.com/teotiaabhi/gun-wifi-tool.git
cd gun-wifi-tool

# Build Docker image
docker build -t gun-wifi-tool .

# Run with network access
docker run -it --privileged --net=host gun-wifi-tool
```

---

## 🎯 **First Time Setup**

### Step 1: Activate Environment (if using virtual env)
```bash
# If you used virtual environment during installation
source gun_wifi_env/bin/activate

# OR use the activation script
./activate_env.sh
```

### Step 2: Check WiFi Adapter
```bash
# List network interfaces
iwconfig

# Should see something like:
# wlan0     IEEE 802.11  ESSID:off/any  
# lo        no wireless extensions.
```

### Step 3: Test Monitor Mode Support
```bash
# Test if your adapter supports monitor mode
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up

# If no errors, your adapter supports monitor mode
# Switch back to managed mode
sudo iw dev wlan0 set type managed
```

---

## 🔧 **Basic Usage - Step by Step**

### Step 1: Interactive Mode (Recommended for Beginners)
```bash
# Start interactive mode
sudo python3 gun_wifi_tool.py --interactive
```

**What happens:**
1. Tool will show a menu
2. Choose option 1 for network scan
3. Choose option 2 for monitor mode setup
4. Choose option 3 for attack options

### Step 2: Manual Network Scan
```bash
# Scan for available networks
sudo python3 gun_wifi_tool.py --scan
```

**Output will show:**
```
[SCAN] Found networks:
[1] SSID: "MyWiFi" | BSSID: AA:BB:CC:DD:EE:FF | Channel: 6 | Security: WPA2
[2] SSID: "Neighbor" | BSSID: 11:22:33:44:55:66 | Channel: 11 | Security: WPA
```

### Step 3: Setup Monitor Mode
```bash
# Setup monitor mode on your WiFi adapter
sudo python3 gun_wifi_tool.py --monitor --interface wlan0
```

**What happens:**
1. Tool switches your WiFi adapter to monitor mode
2. You can now capture WiFi traffic
3. Your internet connection will be disabled during this

---

## ⚔️ **Attack Operations**

### 🚨 **IMPORTANT: Legal Authorization Required**
```
⚠️ ONLY USE ON NETWORKS YOU OWN OR HAVE WRITTEN PERMISSION TO TEST!
⚠️ UNAUTHORIZED ACCESS IS ILLEGAL!
⚠️ FOLLOW LOCAL LAWS AND REGULATIONS!
```

### Attack 1: Deauthentication Attack
```bash
# Basic deauth attack
sudo python3 gun_wifi_tool.py --deauth --target AA:BB:CC:DD:EE:FF

# Deauth with specific client
sudo python3 gun_wifi_tool.py --deauth --target AA:BB:CC:DD:EE:FF --client 11:22:33:44:55:66

# Deauth for specific duration
sudo python3 gun_wifi_tool.py --deauth --target AA:BB:CC:DD:EE:FF --duration 60
```

### Attack 2: Evil Twin Attack
```bash
# Create fake access point
sudo python3 gun_wifi_tool.py --evil-twin --ssid "FreeWiFi" --interface wlan0

# Evil twin with specific channel
sudo python3 gun_wifi_tool.py --evil-twin --ssid "FreeWiFi" --channel 6
```

### Attack 3: Captive Portal
```bash
# Setup captive portal
sudo python3 gun_wifi_tool.py --captive-portal --template corporate

# Custom captive portal
sudo python3 gun_wifi_tool.py --captive-portal --template custom --html-file mypage.html
```

---

## 🔄 **Daily Usage Workflow**

### Step 1: Start Session
```bash
# Navigate to tool directory
cd gun-wifi-tool

# Activate environment (if using virtual env)
source gun_wifi_env/bin/activate

# OR
./activate_env.sh
```

### Step 2: Check System
```bash
# Verify all tools are working
python3 gun_wifi_tool.py --check-system

# Test WiFi adapter
iwconfig
```

### Step 3: Run Operations
```bash
# Start with interactive mode
sudo python3 gun_wifi_tool.py --interactive

# OR use specific commands
sudo python3 gun_wifi_tool.py --scan
sudo python3 gun_wifi_tool.py --monitor
```

### Step 4: End Session
```bash
# Stop any running attacks
sudo python3 gun_wifi_tool.py --stop-all

# Restore normal WiFi mode
sudo python3 gun_wifi_tool.py --restore

# Deactivate environment
deactivate
```

---

## 🛠️ **Troubleshooting Common Issues**

### Issue 1: "Permission Denied"
```bash
# Solution: Always use sudo for WiFi operations
sudo python3 gun_wifi_tool.py --scan
```

### Issue 2: "No module named 'qrcode'"
```bash
# Solution 1: Use system package
sudo apt install python3-qrcode

# Solution 2: Use virtual environment
python3 -m venv myenv
source myenv/bin/activate
pip install qrcode
```

### Issue 3: "Monitor mode not supported"
```bash
# Check your WiFi adapter
lsusb | grep -i wireless
iwconfig

# Get a compatible adapter:
# - Alfa AWUS036ACS
# - Panda PAU09
# - TP-Link AC600T2U Plus
```

### Issue 4: "Interface busy"
```bash
# Stop NetworkManager
sudo systemctl stop NetworkManager

# Kill conflicting processes
sudo airmon-ng check kill

# Restart after testing
sudo systemctl start NetworkManager
```

### Issue 5: Installation fails
```bash
# Clear pip cache
pip cache purge

# Use virtual environment
python3 -m venv gun_wifi_env
source gun_wifi_env/bin/activate
pip install -r requirements.txt
```

---

## 📊 **Testing Your Installation**

### Step 1: Run Unit Tests
```bash
# Test all functions
python3 test_gun_wifi_tool.py
```

### Step 2: Live Function Testing
```bash
# Test attack functions safely
python3 live_attack_testing.py
```

### Step 3: Interactive Demo
```bash
# Try the demo mode
python3 interactive_attack_demo.py
```

### Step 4: Security Analysis
```bash
# Analyze code security
python3 security_analysis.py
```

---

## 📱 **Mobile Device Testing**

### QR Code Features
```bash
# Generate QR code for mobile testing
sudo python3 gun_wifi_tool.py --qr-code --ssid "TestNetwork"

# Captive portal with QR code
sudo python3 gun_wifi_tool.py --captive-portal --qr-code
```

---

## 🔒 **Security Best Practices**

### Before Testing
1. **Get written authorization** from network owner
2. **Document your testing scope** and objectives
3. **Inform relevant parties** about testing schedule
4. **Have legal counsel review** if commercial testing

### During Testing
1. **Use minimal disruption** techniques
2. **Monitor for unintended impacts**
3. **Keep detailed logs** of all activities
4. **Stop immediately** if issues arise

### After Testing
1. **Restore all systems** to original state
2. **Document all findings** professionally
3. **Report vulnerabilities** responsibly
4. **Secure or delete** captured data

---

## 📞 **Getting Help**

### Documentation
```bash
# Read documentation
cat README.md
cat COMPLETE_GUIDE.md
cat USAGE.md
```

### Support Channels
- 🐛 **Bug Reports**: GitHub Issues
- 💬 **Discussions**: GitHub Discussions
- 📧 **Email**: security@gun-wifi-tool.com
- 📚 **Wiki**: GitHub Wiki

### Community
- Join security testing forums
- Follow ethical hacking guidelines
- Share knowledge responsibly
- Help other security professionals

---

## 🔄 **Updates and Maintenance**

### Check for Updates
```bash
# Check current version
python3 gun_wifi_tool.py --version

# Update from GitHub
git pull origin main
pip install -r requirements.txt --upgrade
```

### Backup Configuration
```bash
# Backup your settings
cp -r ~/.gun-wifi-tool ~/.gun-wifi-tool.backup

# Restore if needed
cp -r ~/.gun-wifi-tool.backup ~/.gun-wifi-tool
```

---

## ⚖️ **Legal Reminder**

```
🚨 IMPORTANT LEGAL NOTICE 🚨

This tool is for AUTHORIZED security testing only!

✅ DO:
- Use on your own networks
- Get written permission before testing
- Follow local laws and regulations
- Use for educational purposes
- Report vulnerabilities responsibly

❌ DON'T:
- Test networks without permission
- Use for malicious purposes
- Violate privacy or laws
- Cause network disruption
- Access unauthorized data

THE USER IS FULLY RESPONSIBLE FOR LEGAL COMPLIANCE!
```

---

**Happy Ethical Hacking! 🔒🔫**
