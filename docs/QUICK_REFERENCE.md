# 🔫 GUN WiFi Tool - Quick Reference Card

## 🚀 **Installation Commands**
```bash
# One-line install
curl -fsSL https://raw.githubusercontent.com/yourusername/gun-wifi-tool/main/install.sh | bash

# Manual install
git clone https://github.com/teotiaabhi/gun-wifi-tool.git
cd gun-wifi-tool && ./install.sh
```

## 🎯 **Basic Commands**
```bash
# Interactive mode (easiest)
sudo python3 gun_wifi_tool.py --interactive

# Scan networks
sudo python3 gun_wifi_tool.py --scan

# Monitor mode
sudo python3 gun_wifi_tool.py --monitor

# Help
python3 gun_wifi_tool.py --help
```

## ⚔️ **Attack Commands**
```bash
# Deauth attack
sudo python3 gun_wifi_tool.py --deauth --target AA:BB:CC:DD:EE:FF

# Evil twin
sudo python3 gun_wifi_tool.py --evil-twin --ssid "FreeWiFi"

# Captive portal
sudo python3 gun_wifi_tool.py --captive-portal --template corporate
```

## 🔧 **Environment Commands**
```bash
# Activate virtual env
source gun_wifi_env/bin/activate

# Deactivate
deactivate

# Check system
python3 gun_wifi_tool.py --check-system
```

## 🛠️ **Troubleshooting**
```bash
# Fix QR code issue
sudo apt install python3-qrcode

# Fix permissions
sudo python3 gun_wifi_tool.py

# Check WiFi adapter
iwconfig

# Stop NetworkManager
sudo systemctl stop NetworkManager
```

## 🧪 **Testing Commands**
```bash
# Unit tests
python3 test_gun_wifi_tool.py

# Live testing
python3 live_attack_testing.py

# Interactive demo
python3 interactive_attack_demo.py

# Security analysis
python3 security_analysis.py
```

## ⚖️ **Legal Reminder**
```
⚠️  ONLY USE WITH PROPER AUTHORIZATION!
⚠️  FOLLOW LOCAL LAWS AND REGULATIONS!
⚠️  ETHICAL HACKING ONLY!
```

## 📞 **Need Help?**
- 📖 Read: `STEP_BY_STEP_GUIDE.md`
- 🐛 Issues: GitHub Issues
- 💬 Discuss: GitHub Discussions
