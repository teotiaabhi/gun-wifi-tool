#!/usr/bin/env python3
"""
WiFi Interface Auto-Detection Test
Verify that the auto-detection works properly
"""

import subprocess
import sys
from pathlib import Path

def test_interface_detection():
    """Test WiFi interface auto-detection"""
    print("🔍 Testing WiFi Interface Auto-Detection...")
    print("=" * 50)
    
    # Method 1: iwconfig
    print("\n1. Testing iwconfig method:")
    try:
        result = subprocess.run(['iwconfig'], capture_output=True, text=True, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            interfaces = []
            for line in result.stdout.split('\n'):
                if 'IEEE 802.11' in line or ('no wireless extensions' not in line and line.strip()):
                    interface = line.split()[0] if line.strip() else None
                    if interface and interface != 'lo' and not interface.endswith(':'):
                        interfaces.append(interface)
            
            if interfaces:
                print(f"   ✅ Found interfaces: {', '.join(interfaces)}")
            else:
                print("   ❌ No wireless interfaces found")
        else:
            print("   ❌ iwconfig not available")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Method 2: /sys/class/net
    print("\n2. Testing /sys/class/net method:")
    try:
        net_path = Path("/sys/class/net")
        if net_path.exists():
            wireless_interfaces = []
            for interface_path in net_path.iterdir():
                interface = interface_path.name
                wireless_path = interface_path / "wireless"
                if wireless_path.exists() and interface not in ['lo']:
                    wireless_interfaces.append(interface)
            
            if wireless_interfaces:
                print(f"   ✅ Found wireless interfaces: {', '.join(wireless_interfaces)}")
            else:
                print("   ❌ No wireless interfaces found in /sys/class/net")
        else:
            print("   ❌ /sys/class/net not available")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Method 3: ip link
    print("\n3. Testing ip link method:")
    try:
        result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
        if result.returncode == 0:
            interfaces = []
            for line in result.stdout.split('\n'):
                if ': ' in line and ('wlan' in line or 'wlp' in line or 'wlo' in line):
                    interface = line.split(':')[1].strip().split('@')[0]
                    interfaces.append(interface)
            
            if interfaces:
                print(f"   ✅ Found potential interfaces: {', '.join(interfaces)}")
            else:
                print("   ❌ No WiFi-like interfaces found")
        else:
            print("   ❌ ip command failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Auto-detection should pick the first available wireless interface")
    print("💡 If no interface found, tool will show error and exit gracefully")

if __name__ == "__main__":
    test_interface_detection()
