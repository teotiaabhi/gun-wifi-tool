# GUN WiFi Tool Usage Instructions

## Activation
If you used virtual environment:
```bash
source gun_wifi_env/bin/activate
# OR
./activate_env.sh
```

## Basic Usage
```bash
# Show help
python3 gun_wifi_tool.py --help

# Interactive mode
sudo python3 gun_wifi_tool.py --interactive

# Scan networks
sudo python3 gun_wifi_tool.py --scan

# Setup monitor mode
sudo python3 gun_wifi_tool.py --monitor
```

## Important Notes
- Always run with sudo for actual WiFi operations
- Ensure proper authorization before testing
- Use only for ethical security testing
- Follow local laws and regulations

## Troubleshooting
If you encounter issues:
1. Check if all dependencies are installed
2. Verify WiFi adapter supports monitor mode
3. Ensure proper permissions
4. Check system logs for errors

For more help, refer to the tool's documentation.
