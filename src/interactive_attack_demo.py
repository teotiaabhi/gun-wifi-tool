#!/usr/bin/env python3
"""
GUN WiFi Tool - Interactive Attack Demo
Author: Interactive Demo Suite for GUN Community Tool
Description: Live interactive demonstration of all attack capabilities

This demo shows:
- Real-time attack execution simulation
- Interactive attack parameter selection
- Live monitoring and feedback
- Safe demonstration mode
"""

import sys
import os
import time
import threading
from unittest.mock import patch, Mock
import random

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class InteractiveDemo:
    """Interactive demonstration of attack functions"""
    
    def __init__(self):
        self.demo_mode = True
        self.attack_count = 0
        
    def print_demo_banner(self):
        """Display demo banner"""
        banner = f"""
{Colors.PURPLE}╔══════════════════════════════════════════════════════════════════╗
║                  🎬 INTERACTIVE ATTACK DEMO                       ║
║                     GUN WiFi Tool v3.0                            ║
║                   Live Attack Simulation                           ║
╠══════════════════════════════════════════════════════════════════╣
║  {Colors.YELLOW}Mode:{Colors.RESET} Interactive Safe Demonstration              {Colors.PURPLE}║
║  {Colors.YELLOW}Purpose:{Colors.RESET} Show attack capabilities in real-time      {Colors.PURPLE}║
║  {Colors.YELLOW}Safety:{Colors.RESET} 100% Safe - No actual attacks              {Colors.PURPLE}║
╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.GREEN}🎯 DEMO FEATURES:{Colors.RESET}
• Interactive attack selection
• Real-time attack simulation
• Live progress monitoring
• Detailed attack explanations
• Safe demonstration mode
"""
        print(banner)
    
    def setup_demo_environment(self):
        """Setup demo environment"""
        print(f"{Colors.CYAN}🔧 Setting up demo environment...{Colors.RESET}")
        
        try:
            with patch('sys.argv', ['gun_wifi_tool.py']):
                import gun_wifi_tool
            self.gun_tool_module = gun_tool_module = gun_wifi_tool
            
            with patch('signal.signal'):
                self.tool = gun_wifi_tool.GUNWiFiTool()
            
            print(f"  {Colors.GREEN}✓{Colors.RESET} Demo environment ready")
            return True
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.RESET} Demo setup failed: {e}")
            return False
    
    def show_attack_menu(self):
        """Show attack selection menu"""
        print(f"\n{Colors.CYAN}🎯 SELECT ATTACK TO DEMONSTRATE:{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*50}{Colors.RESET}")
        
        attacks = [
            ("Deauthentication Attack", "💥", "Disconnect devices from WiFi"),
            ("Evil Twin Access Point", "👿", "Create fake WiFi hotspot"),
            ("Captive Portal", "🕷️", "Credential harvesting page"),
            ("DHCP Flood Attack", "🌊", "Overwhelm DHCP server"),
            ("Beacon Flood Attack", "📡", "Create multiple fake APs"),
            ("Network Scanning", "🔍", "Discover nearby networks"),
            ("Monitor Mode Demo", "📶", "Show monitor mode setup"),
            ("Full Attack Chain", "🔥", "Demonstrate complete attack"),
            ("Exit Demo", "🚪", "Exit demonstration")
        ]
        
        for i, (name, emoji, desc) in enumerate(attacks, 1):
            print(f"{Colors.YELLOW}{i:2d}.{Colors.RESET} {emoji} {Colors.BOLD}{name}{Colors.RESET}")
            print(f"     {desc}")
        
        print(f"\n{Colors.CYAN}Enter your choice (1-{len(attacks)}): {Colors.RESET}", end="")
        
        try:
            choice = int(input().strip())
            if 1 <= choice <= len(attacks):
                return choice
            else:
                print(f"{Colors.RED}❌ Invalid choice{Colors.RESET}")
                return None
        except ValueError:
            print(f"{Colors.RED}❌ Please enter a number{Colors.RESET}")
            return None
    
    def demo_deauth_attack(self):
        """Demonstrate deauth attack"""
        print(f"\n{Colors.YELLOW}💥 DEAUTHENTICATION ATTACK DEMO{Colors.RESET}")
        print("=" * 40)
        
        print(f"{Colors.BLUE}📖 What is a Deauth Attack?{Colors.RESET}")
        print("A deauthentication attack sends forged deauth frames to disconnect")
        print("devices from their WiFi network. Used for testing network security.")
        
        # Get user input for demo
        print(f"\n{Colors.CYAN}Demo Parameters:{Colors.RESET}")
        target_bssid = input("Enter target BSSID (or press Enter for demo): ").strip() or "00:11:22:33:44:55"
        client_mac = input("Enter client MAC (or press Enter for broadcast): ").strip() or None
        
        try:
            count = int(input("Enter packet count (or press Enter for 20): ").strip() or "20")
        except ValueError:
            count = 20
        
        print(f"\n{Colors.YELLOW}🚀 Starting Deauth Attack Demo...{Colors.RESET}")
        print(f"Target BSSID: {target_bssid}")
        print(f"Client MAC: {client_mac if client_mac else 'Broadcast (all clients)'}")
        print(f"Packet Count: {count}")
        
        # Mock the attack with real-time feedback
        with patch.object(self.gun_tool_module, 'SCAPY_AVAILABLE', True):
            with patch.object(self.gun_tool_module, 'sendp') as mock_sendp:
                with patch('time.sleep'):
                    print(f"\n{Colors.GREEN}💥 Executing deauth attack...{Colors.RESET}")
                    
                    for i in range(count):
                        if i % 5 == 0:
                            print(f"  📡 Sent {i+1}/{count} deauth packets...")
                        time.sleep(0.1)  # Real-time simulation
                    
                    result = self.tool.deauth_attack(target_bssid, client_mac, count)
                    
                    if result:
                        print(f"\n{Colors.GREEN}✅ Demo completed successfully!{Colors.RESET}")
                        print(f"  • {count} deauth packets sent")
                        print(f"  • Target devices would be disconnected")
                        print(f"  • Attack logged for audit trail")
                    else:
                        print(f"\n{Colors.RED}❌ Demo failed{Colors.RESET}")
        
        self.attack_count += 1
    
    def demo_evil_twin(self):
        """Demonstrate evil twin creation"""
        print(f"\n{Colors.YELLOW}👿 EVIL TWIN ACCESS POINT DEMO{Colors.RESET}")
        print("=" * 40)
        
        print(f"{Colors.BLUE}📖 What is an Evil Twin?{Colors.RESET}")
        print("An Evil Twin is a fake WiFi access point that mimics a legitimate one.")
        print("Used to intercept traffic and test wireless security awareness.")
        
        # Get demo parameters
        print(f"\n{Colors.CYAN}Demo Parameters:{Colors.RESET}")
        ssid = input("Enter SSID to mimic (or press Enter for demo): ").strip() or "Free_WiFi_Demo"
        
        try:
            channel = int(input("Enter channel (1-13, or press Enter for 6): ").strip() or "6")
        except ValueError:
            channel = 6
        
        print(f"\n{Colors.YELLOW}🚀 Starting Evil Twin Demo...{Colors.RESET}")
        print(f"Target SSID: {ssid}")
        print(f"Channel: {channel}")
        
        # Mock evil twin creation
        with patch('builtins.open', create=True):
            with patch('subprocess.Popen') as mock_popen:
                mock_process = Mock()
                mock_process.pid = random.randint(10000, 99999)
                mock_popen.return_value = mock_process
                
                print(f"\n{Colors.GREEN}👿 Creating evil twin AP...{Colors.RESET}")
                print(f"  📝 Generating hostapd configuration...")
                time.sleep(1)
                print(f"  🔧 Configuring interface...")
                time.sleep(1)
                print(f"  📡 Starting access point...")
                time.sleep(1)
                
                result = self.tool.create_evil_twin(ssid, channel)
                
                if result:
                    print(f"\n{Colors.GREEN}✅ Evil Twin created successfully!{Colors.RESET}")
                    print(f"  • SSID: {ssid}")
                    print(f"  • Channel: {channel}")
                    print(f"  • Process ID: {result.pid}")
                    print(f"  • Status: Broadcasting")
                    print(f"  • Clients can now connect to fake AP")
        
        self.attack_count += 1
    
    def demo_captive_portal(self):
        """Demonstrate captive portal"""
        print(f"\n{Colors.YELLOW}🕷️ CAPTIVE PORTAL DEMO{Colors.RESET}")
        print("=" * 40)
        
        print(f"{Colors.BLUE}📖 What is a Captive Portal?{Colors.RESET}")
        print("A captive portal captures credentials by presenting a fake login page")
        print("when users connect to the evil twin access point.")
        
        # Get demo parameters
        print(f"\n{Colors.CYAN}Demo Parameters:{Colors.RESET}")
        print("Available skins: google, facebook")
        skin = input("Enter portal skin (or press Enter for google): ").strip() or "google"
        
        if skin not in ['google', 'facebook']:
            skin = 'google'
        
        print(f"\n{Colors.YELLOW}🚀 Starting Captive Portal Demo...{Colors.RESET}")
        print(f"Portal Skin: {skin.capitalize()}")
        
        # Mock captive portal
        with patch.object(self.gun_tool_module, 'FLASK_AVAILABLE', True):
            with patch.object(self.gun_tool_module, 'Flask'):
                with patch('threading.Thread'):
                    print(f"\n{Colors.GREEN}🕷️ Starting captive portal...{Colors.RESET}")
                    print(f"  🌐 Initializing Flask web server...")
                    time.sleep(1)
                    print(f"  🎨 Loading {skin} portal template...")
                    time.sleep(1)
                    print(f"  🔗 Configuring routing rules...")
                    time.sleep(1)
                    print(f"  🚀 Starting background thread...")
                    time.sleep(1)
                    
                    result = self.tool.start_captive_portal(skin)
                    
                    if result:
                        print(f"\n{Colors.GREEN}✅ Captive Portal active!{Colors.RESET}")
                        print(f"  • Portal URL: http://192.168.1.1")
                        print(f"  • Skin: {skin.capitalize()}")
                        print(f"  • Status: Listening on port 80")
                        print(f"  • Ready to capture credentials")
                        
                        # Simulate credential capture
                        print(f"\n{Colors.CYAN}📋 Simulating credential capture...{Colors.RESET}")
                        time.sleep(2)
                        fake_creds = [
                            ("user@demo.com", "password123"),
                            ("testuser", "demo_pass"),
                            ("admin", "admin123")
                        ]
                        
                        for email, password in fake_creds:
                            print(f"  🎯 Captured: {email} : {password}")
                            time.sleep(0.5)
        
        self.attack_count += 1
    
    def demo_dhcp_flood(self):
        """Demonstrate DHCP flood"""
        print(f"\n{Colors.YELLOW}🌊 DHCP FLOOD ATTACK DEMO{Colors.RESET}")
        print("=" * 40)
        
        print(f"{Colors.BLUE}📖 What is DHCP Flooding?{Colors.RESET}")
        print("DHCP flooding exhausts the DHCP server's IP pool by requesting")
        print("many IP addresses with different MAC addresses.")
        
        # Get demo parameters
        print(f"\n{Colors.CYAN}Demo Parameters:{Colors.RESET}")
        interface = input("Enter interface (or press Enter for eth0): ").strip() or "eth0"
        
        try:
            count = int(input("Enter flood count (or press Enter for 30): ").strip() or "30")
        except ValueError:
            count = 30
        
        print(f"\n{Colors.YELLOW}🚀 Starting DHCP Flood Demo...{Colors.RESET}")
        print(f"Interface: {interface}")
        print(f"Flood Count: {count}")
        
        # Mock DHCP flood
        with patch.object(self.gun_tool_module, 'SCAPY_AVAILABLE', True):
            with patch.object(self.gun_tool_module, 'sendp'):
                with patch('time.sleep'):
                    print(f"\n{Colors.GREEN}🌊 Flooding DHCP server...{Colors.RESET}")
                    
                    for i in range(count):
                        if i % 5 == 0:
                            # Generate fake MAC for display
                            fake_mac = ":".join([f"{random.randint(0,255):02x}" for _ in range(6)])
                            print(f"  📡 DHCP Request {i+1}/{count} - MAC: {fake_mac}")
                        time.sleep(0.1)
                    
                    result = self.tool.dhcp_flood(interface, count)
                    
                    if result:
                        print(f"\n{Colors.GREEN}✅ DHCP Flood completed!{Colors.RESET}")
                        print(f"  • {count} DHCP requests sent")
                        print(f"  • DHCP server would be overwhelmed")
                        print(f"  • IP pool exhausted")
        
        self.attack_count += 1
    
    def demo_beacon_flood(self):
        """Demonstrate beacon flood"""
        print(f"\n{Colors.YELLOW}📡 BEACON FLOOD ATTACK DEMO{Colors.RESET}")
        print("=" * 40)
        
        print(f"{Colors.BLUE}📖 What is Beacon Flooding?{Colors.RESET}")
        print("Beacon flooding creates many fake WiFi access points that appear")
        print("in wireless scans, confusing users and testing detection systems.")
        
        # Get demo parameters
        try:
            count = int(input("Enter number of fake APs (or press Enter for 25): ").strip() or "25")
        except ValueError:
            count = 25
        
        print(f"\n{Colors.YELLOW}🚀 Starting Beacon Flood Demo...{Colors.RESET}")
        print(f"Fake APs to create: {count}")
        
        # Mock beacon flood
        with patch.object(self.gun_tool_module, 'SCAPY_AVAILABLE', True):
            with patch.object(self.gun_tool_module, 'sendp'):
                with patch('time.sleep'):
                    print(f"\n{Colors.GREEN}📡 Creating fake access points...{Colors.RESET}")
                    
                    fake_ssids = []
                    for i in range(count):
                        # Generate fake SSID and MAC
                        fake_ssid = f"FakeAP_{random.randint(1000, 9999)}"
                        fake_mac = ":".join([f"{random.randint(0,255):02x}" for _ in range(6)])
                        fake_ssids.append((fake_ssid, fake_mac))
                        
                        if i % 5 == 0:
                            print(f"  📡 Broadcasting: {fake_ssid} ({fake_mac})")
                        time.sleep(0.1)
                    
                    result = self.tool.beacon_flood(count)
                    
                    if result:
                        print(f"\n{Colors.GREEN}✅ Beacon Flood completed!{Colors.RESET}")
                        print(f"  • {count} fake APs created")
                        print(f"  • Wireless environment cluttered")
                        print(f"  • Users would see many fake networks")
                        
                        # Show some example fake APs
                        print(f"\n{Colors.CYAN}📋 Sample Fake Networks Created:{Colors.RESET}")
                        for i, (ssid, mac) in enumerate(fake_ssids[:5], 1):
                            print(f"  {i}. {ssid} ({mac})")
                        if len(fake_ssids) > 5:
                            print(f"  ... and {len(fake_ssids) - 5} more")
        
        self.attack_count += 1
    
    def demo_network_scanning(self):
        """Demonstrate network scanning"""
        print(f"\n{Colors.YELLOW}🔍 NETWORK SCANNING DEMO{Colors.RESET}")
        print("=" * 40)
        
        print(f"{Colors.BLUE}📖 What is Network Scanning?{Colors.RESET}")
        print("Network scanning discovers nearby WiFi networks, their security")
        print("settings, and connected devices for reconnaissance.")
        
        # Get demo parameters
        try:
            duration = int(input("Enter scan duration in seconds (or press Enter for 10): ").strip() or "10")
        except ValueError:
            duration = 10
        
        print(f"\n{Colors.YELLOW}🚀 Starting Network Scan Demo...{Colors.RESET}")
        print(f"Scan Duration: {duration} seconds")
        
        # Mock network scanning
        with patch('subprocess.Popen'):
            with patch('time.sleep'):
                with patch('os.path.exists', return_value=True):
                    # Create realistic mock data
                    mock_networks = [
                        {'bssid': '00:11:22:33:44:55', 'essid': 'HomeNetwork_5G', 'channel': '6', 'encryption': 'WPA2', 'power': '-45'},
                        {'bssid': '66:77:88:99:aa:bb', 'essid': 'Starbucks_WiFi', 'channel': '11', 'encryption': 'Open', 'power': '-60'},
                        {'bssid': 'cc:dd:ee:ff:00:11', 'essid': 'Corporate_Net', 'channel': '1', 'encryption': 'WPA3', 'power': '-55'},
                        {'bssid': 'aa:bb:cc:dd:ee:ff', 'essid': 'Guest_Network', 'channel': '13', 'encryption': 'WEP', 'power': '-70'},
                        {'bssid': 'ff:ee:dd:cc:bb:aa', 'essid': 'Hidden_AP', 'channel': '3', 'encryption': 'WPA2', 'power': '-65'}
                    ]
                    
                    mock_csv_data = "BSSID,ESSID,Channel,Encryption,Power\n"
                    for net in mock_networks:
                        mock_csv_data += f"{net['bssid']},{net['essid']},{net['channel']},{net['encryption']},{net['power']}\n"
                    
                    with patch('builtins.open', create=True) as mock_open:
                        mock_open.return_value.__enter__.return_value.read.return_value = mock_csv_data
                        
                        print(f"\n{Colors.GREEN}🔍 Scanning for networks...{Colors.RESET}")
                        
                        # Simulate real-time scanning
                        for i in range(duration):
                            discovered = min(i + 1, len(mock_networks))
                            print(f"  📡 Scanning... {i+1}s elapsed - {discovered} networks found")
                            time.sleep(1)
                        
                        networks = self.tool.scan_networks(duration)
                        
                        if networks:
                            print(f"\n{Colors.GREEN}✅ Scan completed!{Colors.RESET}")
                            print(f"  • {len(networks)} networks discovered")
                            print(f"  • Detailed information collected")
                            
                            print(f"\n{Colors.CYAN}📋 Discovered Networks:{Colors.RESET}")
                            for i, net in enumerate(networks, 1):
                                encryption_color = Colors.GREEN if net['encryption'] in ['WPA2', 'WPA3'] else Colors.RED if net['encryption'] == 'Open' else Colors.YELLOW
                                print(f"  {i}. {Colors.BOLD}{net['essid']}{Colors.RESET}")
                                print(f"     BSSID: {net['bssid']}")
                                print(f"     Channel: {net['channel']}")
                                print(f"     Security: {encryption_color}{net['encryption']}{Colors.RESET}")
                                print(f"     Signal: {net['power']} dBm")
                                print()
        
        self.attack_count += 1
    
    def demo_monitor_mode(self):
        """Demonstrate monitor mode setup"""
        print(f"\n{Colors.YELLOW}📶 MONITOR MODE SETUP DEMO{Colors.RESET}")
        print("=" * 40)
        
        print(f"{Colors.BLUE}📖 What is Monitor Mode?{Colors.RESET}")
        print("Monitor mode allows WiFi adapters to capture all wireless traffic")
        print("in the area, not just traffic directed to the device.")
        
        print(f"\n{Colors.YELLOW}🚀 Starting Monitor Mode Demo...{Colors.RESET}")
        
        # Mock monitor mode setup
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            print(f"\n{Colors.GREEN}📶 Setting up monitor mode...{Colors.RESET}")
            print(f"  🛑 Stopping NetworkManager...")
            time.sleep(1)
            print(f"  💀 Killing conflicting processes...")
            time.sleep(1)
            print(f"  🔧 Enabling monitor mode on wlan0...")
            time.sleep(1)
            print(f"  📡 Interface wlan0mon created...")
            time.sleep(1)
            
            result = self.tool.setup_monitor_mode()
            
            if result:
                print(f"\n{Colors.GREEN}✅ Monitor mode activated!{Colors.RESET}")
                print(f"  • Interface: wlan0mon")
                print(f"  • Status: Active")
                print(f"  • Capability: Packet capture enabled")
                print(f"  • Ready for attacks")
        
        self.attack_count += 1
    
    def demo_full_attack_chain(self):
        """Demonstrate complete attack chain"""
        print(f"\n{Colors.YELLOW}🔥 FULL ATTACK CHAIN DEMO{Colors.RESET}")
        print("=" * 40)
        
        print(f"{Colors.BLUE}📖 Complete Attack Scenario{Colors.RESET}")
        print("This demonstrates a complete WiFi penetration test scenario:")
        print("1. Monitor mode setup")
        print("2. Network scanning")
        print("3. Deauth attack")
        print("4. Evil twin creation")
        print("5. Captive portal deployment")
        print("6. Cleanup operations")
        
        input(f"\n{Colors.CYAN}Press Enter to start the attack chain demo...{Colors.RESET}")
        
        # Step 1: Monitor Mode
        print(f"\n{Colors.PURPLE}🔵 STEP 1: Monitor Mode Setup{Colors.RESET}")
        time.sleep(1)
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            result = self.tool.setup_monitor_mode()
            print(f"  {Colors.GREEN}✓{Colors.RESET} Monitor mode activated")
        
        # Step 2: Network Scanning
        print(f"\n{Colors.PURPLE}🔵 STEP 2: Network Reconnaissance{Colors.RESET}")
        time.sleep(1)
        print(f"  🔍 Scanning for target networks...")
        time.sleep(2)
        print(f"  {Colors.GREEN}✓{Colors.RESET} Target identified: Corporate_WiFi")
        
        # Step 3: Deauth Attack
        print(f"\n{Colors.PURPLE}🔵 STEP 3: Deauthentication Attack{Colors.RESET}")
        time.sleep(1)
        with patch.object(self.gun_tool_module, 'SCAPY_AVAILABLE', True):
            with patch.object(self.gun_tool_module, 'sendp'):
                with patch('time.sleep'):
                    print(f"  💥 Deauthenticating clients from Corporate_WiFi...")
                    result = self.tool.deauth_attack("00:11:22:33:44:55", count=20)
                    print(f"  {Colors.GREEN}✓{Colors.RESET} Clients disconnected")
        
        # Step 4: Evil Twin
        print(f"\n{Colors.PURPLE}🔵 STEP 4: Evil Twin Deployment{Colors.RESET}")
        time.sleep(1)
        with patch('builtins.open', create=True):
            with patch('subprocess.Popen') as mock_popen:
                mock_process = Mock()
                mock_process.pid = 12345
                mock_popen.return_value = mock_process
                result = self.tool.create_evil_twin("Corporate_WiFi", 6)
                print(f"  👿 Evil twin 'Corporate_WiFi' created")
                print(f"  {Colors.GREEN}✓{Colors.RESET} Fake AP broadcasting")
        
        # Step 5: Captive Portal
        print(f"\n{Colors.PURPLE}🔵 STEP 5: Captive Portal Launch{Colors.RESET}")
        time.sleep(1)
        with patch.object(self.gun_tool_module, 'FLASK_AVAILABLE', True):
            with patch.object(self.gun_tool_module, 'Flask'):
                with patch('threading.Thread'):
                    result = self.tool.start_captive_portal('google')
                    print(f"  🕷️ Captive portal deployed")
                    print(f"  {Colors.GREEN}✓{Colors.RESET} Ready to capture credentials")
        
        # Simulate success
        print(f"\n{Colors.PURPLE}🔵 STEP 6: Results{Colors.RESET}")
        time.sleep(1)
        print(f"  🎯 Simulating user connections...")
        time.sleep(2)
        print(f"  📊 3 users connected to evil twin")
        print(f"  🔑 2 credential sets captured")
        print(f"  📝 Attack logged successfully")
        
        # Cleanup
        print(f"\n{Colors.PURPLE}🔵 STEP 7: Cleanup{Colors.RESET}")
        time.sleep(1)
        with patch('subprocess.run'):
            self.tool.stop_all_attacks()
            print(f"  🧹 All attacks stopped")
            print(f"  🔧 Monitor mode disabled")
            print(f"  {Colors.GREEN}✓{Colors.RESET} System restored")
        
        print(f"\n{Colors.GREEN}🎉 ATTACK CHAIN COMPLETED SUCCESSFULLY!{Colors.RESET}")
        print(f"{Colors.CYAN}This demonstrates the complete workflow of a WiFi penetration test.{Colors.RESET}")
        
        self.attack_count += 1
    
    def run_interactive_demo(self):
        """Run the interactive demo"""
        self.print_demo_banner()
        
        if not self.setup_demo_environment():
            return 1
        
        print(f"{Colors.GREEN}🎬 Welcome to the Interactive Attack Demo!{Colors.RESET}")
        print(f"This demonstration shows how each attack function works safely.")
        
        while True:
            choice = self.show_attack_menu()
            
            if choice is None:
                continue
            elif choice == 1:
                self.demo_deauth_attack()
            elif choice == 2:
                self.demo_evil_twin()
            elif choice == 3:
                self.demo_captive_portal()
            elif choice == 4:
                self.demo_dhcp_flood()
            elif choice == 5:
                self.demo_beacon_flood()
            elif choice == 6:
                self.demo_network_scanning()
            elif choice == 7:
                self.demo_monitor_mode()
            elif choice == 8:
                self.demo_full_attack_chain()
            elif choice == 9:
                break
            
            print(f"\n{Colors.CYAN}Demo completed! Press Enter to continue...{Colors.RESET}")
            input()
        
        print(f"\n{Colors.GREEN}🎉 Demo Session Complete!{Colors.RESET}")
        print(f"Total attacks demonstrated: {self.attack_count}")
        print(f"{Colors.YELLOW}Thank you for using the GUN WiFi Tool demo!{Colors.RESET}")
        print(f"{Colors.RED}Remember: Use only with proper authorization!{Colors.RESET}")
        
        return 0

def main():
    """Main demo function"""
    demo = InteractiveDemo()
    return demo.run_interactive_demo()

if __name__ == "__main__":
    sys.exit(main())
