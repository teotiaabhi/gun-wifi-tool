#!/bin/bash
# =================================================================
# GUN WiFi Tool - Automated Installer Script
# Professional WiFi Penetration Testing Suite
# Author: GUN Community
# Version: 3.0 - Enhanced Auto Installation
# =================================================================

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Banner
print_banner() {
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗"
    echo -e "║              🔫 GUN WiFi Tool Auto Installer                     ║"
    echo -e "║                Professional Installation Script                   ║"
    echo -e "╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo
}

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "Running as root. This is not recommended for pip installations."
        log_info "Consider running without sudo and using virtual environment."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Detect Linux distribution
detect_distro() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        DISTRO=$ID
        VERSION=$VERSION_ID
    else
        log_error "Cannot detect Linux distribution"
        exit 1
    fi
    
    log_info "Detected distribution: $DISTRO $VERSION"
}

# Update system packages
update_system() {
    log_info "Updating system packages..."
    
    case $DISTRO in
        "ubuntu"|"debian"|"kali")
            sudo apt update && sudo apt upgrade -y
            ;;
        "centos"|"rhel"|"fedora")
            if command -v dnf &> /dev/null; then
                sudo dnf update -y
            else
                sudo yum update -y
            fi
            ;;
        "arch"|"manjaro")
            sudo pacman -Syu --noconfirm
            ;;
        "opensuse"|"sles")
            sudo zypper update -y
            ;;
        *)
            log_warning "Unknown distribution. Skipping system update."
            ;;
    esac
    
    log_success "System packages updated"
}

# Install system dependencies
install_system_deps() {
    log_info "Installing system dependencies..."
    
    case $DISTRO in
        "ubuntu"|"debian"|"kali")
            sudo apt install -y \
                aircrack-ng \
                hostapd \
                dnsmasq \
                iptables \
                wireless-tools \
                iw \
                net-tools \
                python3 \
                python3-pip \
                python3-venv \
                python3-dev \
                python3-setuptools \
                build-essential \
                libffi-dev \
                libssl-dev \
                python3-qrcode \
                python3-pil \
                macchanger \
                tcpdump
            ;;
        "centos"|"rhel"|"fedora")
            if command -v dnf &> /dev/null; then
                sudo dnf install -y \
                    aircrack-ng \
                    hostapd \
                    dnsmasq \
                    iptables \
                    wireless-tools \
                    iw \
                    python3 \
                    python3-pip \
                    python3-devel \
                    gcc \
                    openssl-devel \
                    libffi-devel
            else
                sudo yum install -y \
                    aircrack-ng \
                    hostapd \
                    dnsmasq \
                    iptables \
                    wireless-tools \
                    iw \
                    python3 \
                    python3-pip \
                    python3-devel \
                    gcc \
                    openssl-devel \
                    libffi-devel
            fi
            ;;
        "arch"|"manjaro")
            sudo pacman -S --noconfirm \
                aircrack-ng \
                hostapd \
                dnsmasq \
                iptables \
                wireless_tools \
                iw \
                python \
                python-pip \
                base-devel
            ;;
        "opensuse"|"sles")
            sudo zypper install -y \
                aircrack-ng \
                hostapd \
                dnsmasq \
                iptables \
                wireless-tools \
                iw \
                python3 \
                python3-pip \
                python3-devel \
                gcc
            ;;
        *)
            log_error "Unsupported distribution: $DISTRO"
            exit 1
            ;;
    esac
    
    log_success "System dependencies installed"
}

# Setup Python environment
setup_python_env() {
    log_info "Setting up Python environment..."
    
    # Check if we should use virtual environment
    read -p "Use virtual environment? (Recommended) (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        log_info "Creating virtual environment..."
        python3 -m venv gun_wifi_env
        source gun_wifi_env/bin/activate
        log_success "Virtual environment created and activated"
        
        # Create activation script
        cat > activate_env.sh << 'EOF'
#!/bin/bash
source gun_wifi_env/bin/activate
echo "GUN WiFi Tool environment activated"
echo "To deactivate, run: deactivate"
EOF
        chmod +x activate_env.sh
        log_info "Created activation script: ./activate_env.sh"
    fi
    
    # Upgrade pip
    log_info "Upgrading pip..."
    python3 -m pip install --upgrade pip setuptools wheel
    log_success "Pip upgraded"
}

# Install Python dependencies
install_python_deps() {
    log_info "Installing Python dependencies..."
    
    # Define packages to install
    PACKAGES=(
        "scapy>=2.4.4"
        "flask>=2.0.0"
        "werkzeug>=2.0.0"
        "pillow>=8.3.2"
        "requests>=2.26.0"
        "pycryptodome>=3.15.0"
        "cryptography>=3.4.8"
        "netaddr>=0.8.0"
        "psutil>=5.8.0"
        "netifaces>=0.11.0"
        "colorama>=0.4.4"
        "tqdm>=4.62.0"
        "pyjwt>=2.4.0"
    )
    
    # Install QR code package separately (handles compatibility issues)
    log_info "Installing QR code package..."
    if python3 -c "import qrcode" 2>/dev/null; then
        log_success "QR code package already available (system package)"
    else
        pip install qrcode || {
            log_warning "Failed to install qrcode via pip, trying alternative..."
            pip install qrcode-terminal || log_warning "QR code installation failed"
        }
    fi
    
    # Install main packages
    for package in "${PACKAGES[@]}"; do
        log_info "Installing $package..."
        pip install "$package" || {
            log_warning "Failed to install $package, continuing..."
        }
    done
    
    # Install optional packages
    log_info "Installing optional packages..."
    OPTIONAL_PACKAGES=(
        "matplotlib>=3.5.0"
        "numpy>=1.21.0"
        "pandas>=1.3.0"
        "python-nmap>=0.7.1"
    )
    
    for package in "${OPTIONAL_PACKAGES[@]}"; do
        pip install "$package" 2>/dev/null || log_warning "Optional package $package failed to install"
    done
    
    log_success "Python dependencies installed"
}

# Verify installation
verify_installation() {
    log_info "Verifying installation..."
    
    # Check system tools
    SYSTEM_TOOLS=("aircrack-ng" "hostapd" "dnsmasq" "iptables" "iwconfig")
    
    for tool in "${SYSTEM_TOOLS[@]}"; do
        if command -v "$tool" &> /dev/null; then
            log_success "$tool installed"
        else
            log_error "$tool not found"
        fi
    done
    
    # Check Python packages
    PYTHON_PACKAGES=("scapy" "flask" "requests" "psutil" "colorama")
    
    for package in "${PYTHON_PACKAGES[@]}"; do
        if python3 -c "import $package" 2>/dev/null; then
            log_success "Python package $package installed"
        else
            log_error "Python package $package not found"
        fi
    done
    
    # Test QR code specifically
    if python3 -c "import qrcode; print('QR Code test passed')" 2>/dev/null; then
        log_success "QR code package working"
    else
        log_warning "QR code package may have issues"
    fi
    
    # Test the main tool
    if [[ -f "gun_wifi_tool.py" ]]; then
        log_info "Testing main tool..."
        if python3 gun_wifi_tool.py --help &>/dev/null; then
            log_success "GUN WiFi Tool is working!"
        else
            log_warning "GUN WiFi Tool may have issues"
        fi
    else
        log_warning "gun_wifi_tool.py not found in current directory"
    fi
}

# Setup completion
setup_completion() {
    log_info "Setting up completion..."
    
    # Create desktop shortcut (if in GUI environment)
    if [[ -n "$DISPLAY" ]] && [[ -d "$HOME/Desktop" ]]; then
        cat > "$HOME/Desktop/GUN WiFi Tool.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=GUN WiFi Tool
Comment=Professional WiFi Penetration Testing Suite
Exec=gnome-terminal -- bash -c 'cd "$(dirname "$(readlink -f "%k")")"; python3 gun_wifi_tool.py; exec bash'
Icon=network-wireless
Terminal=true
Categories=Network;Security;
EOF
        chmod +x "$HOME/Desktop/GUN WiFi Tool.desktop"
        log_success "Desktop shortcut created"
    fi
    
    # Create usage instructions
    cat > USAGE.md << 'EOF'
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
EOF
    
    log_success "Usage instructions created (USAGE.md)"
}

# Cleanup function
cleanup() {
    log_info "Installation completed!"
    echo
    echo -e "${BOLD}${GREEN}🎉 GUN WiFi Tool Installation Summary:${NC}"
    echo -e "${GREEN}✅ System dependencies installed${NC}"
    echo -e "${GREEN}✅ Python environment configured${NC}"
    echo -e "${GREEN}✅ Python packages installed${NC}"
    echo -e "${GREEN}✅ Installation verified${NC}"
    echo
    echo -e "${YELLOW}⚠️  Important Reminders:${NC}"
    echo -e "${YELLOW}• Use only with proper authorization${NC}"
    echo -e "${YELLOW}• Follow ethical hacking guidelines${NC}"
    echo -e "${YELLOW}• Respect local laws and regulations${NC}"
    echo
    echo -e "${CYAN}📚 Next Steps:${NC}"
    echo -e "${CYAN}1. Read USAGE.md for instructions${NC}"
    echo -e "${CYAN}2. Run: sudo python3 gun_wifi_tool.py --help${NC}"
    echo -e "${CYAN}3. Start with: sudo python3 gun_wifi_tool.py --interactive${NC}"
    echo
    if [[ -f "gun_wifi_env/bin/activate" ]]; then
        echo -e "${BLUE}💡 To activate virtual environment: source gun_wifi_env/bin/activate${NC}"
    fi
}

# Main installation flow
main() {
    print_banner
    
    log_info "Starting GUN WiFi Tool installation..."
    
    # Run installation steps
    check_root
    detect_distro
    update_system
    install_system_deps
    setup_python_env
    install_python_deps
    verify_installation
    setup_completion
    cleanup
}

# Handle interruption
trap 'log_error "Installation interrupted"; exit 1' INT TERM

# Run main function
main "$@"
