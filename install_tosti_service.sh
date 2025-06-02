#!/bin/bash

set -e

# Configuration
SERVICE_NAME="tosti-fridge"
SERVICE_USER="pi"
APP_DIR="/opt/tosti-fridge-client"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} ⚠️  $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} ❌ $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    print_error "This script should not be run as root. Please run as the pi user."
    exit 1
fi

print_status "🚀 Starting TOSTI Fridge Client installation..."

# Update system packages
print_status "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install required system packages
print_status "🔧 Installing system dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-rpi.gpio \
    git

# Install Poetry
print_status "📝 Installing Poetry..."
if ! command -v poetry &> /dev/null; then
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
else
    print_status "✅ Poetry already installed"
fi

# Create application directory
print_status "📁 Setting up application directory..."
if [ -d "$APP_DIR" ]; then
    print_warning "Application directory already exists. Backing up..."
    sudo mv "$APP_DIR" "${APP_DIR}.backup.$(date +%s)"
fi

sudo mkdir -p "$APP_DIR"
sudo chown "$SERVICE_USER:$SERVICE_USER" "$APP_DIR"

# Copy application files
print_status "📋 Copying application files..."
cp -r client "$APP_DIR/"
cp pyproject.toml "$APP_DIR/"
cp README.md "$APP_DIR/" 2>/dev/null || true

print_status "✅ Using existing production.py configuration"

# Install Python dependencies
print_status "🐍 Installing Python dependencies..."
cd "$APP_DIR"
export PATH="$HOME/.local/bin:$PATH"
poetry install --only=main,production

# Set up serial port permissions
print_status "🔐 Setting up serial port permissions..."
sudo usermod -a -G dialout "$SERVICE_USER"

# Interactive configuration
print_status "⚙️  Configuration Setup"
echo

# Show available serial devices
print_status "🔍 Available serial devices:"
if ls /dev/serial/by-id/* 2>/dev/null; then
    echo
else
    echo "No serial devices found"
    echo
fi

# Prompt for serial device
echo "📱 Enter the path to your QR scanner serial device:"
read -p "Serial device: " SERIAL_DEVICE

if [ -z "$SERIAL_DEVICE" ]; then
    print_error "Serial device path cannot be empty"
    exit 1
fi

# Verify serial device exists
if [ ! -e "$SERIAL_DEVICE" ]; then
    print_warning "Serial device $SERIAL_DEVICE not found!"
    print_warning "Make sure your QR scanner is:"
    print_warning "1. Connected via USB"
    print_warning "2. Configured for serial/UART mode (not HID keyboard mode)"
    print_warning "3. Detected as a serial device"
    echo
    read -p "Continue with this device path anyway? (y/N): " continue_response
    if [[ ! "$continue_response" =~ ^[Yy]$ ]]; then
        print_error "Installation cancelled."
        exit 1
    fi
fi

echo
print_status "🔑 API Configuration"
echo "Enter your TOSTI API credentials:"
echo

read -p "Client ID: " CLIENT_ID
if [ -z "$CLIENT_ID" ]; then
    print_error "Client ID cannot be empty"
    exit 1
fi

read -p "Client Secret: " CLIENT_SECRET
if [ -z "$CLIENT_SECRET" ]; then
    print_error "Client Secret cannot be empty"
    exit 1
fi

DEFAULT_API_URL="https://tosti.science.ru.nl"
read -p "API Base URL [$DEFAULT_API_URL]: " API_BASE_URL
API_BASE_URL=${API_BASE_URL:-$DEFAULT_API_URL}

echo
print_status "📋 Configuration Summary:"
echo "  📱 Serial Device: $SERIAL_DEVICE"
echo "  🆔 Client ID: $CLIENT_ID"
echo "  🔐 Client Secret: ${CLIENT_SECRET:0:8}..."
echo "  🌐 API Base URL: $API_BASE_URL"
echo

read -p "✅ Continue with this configuration? (Y/n): " confirm_response
if [[ "$confirm_response" =~ ^[Nn]$ ]]; then
    print_error "Installation cancelled."
    exit 1
fi

# Create environment file for systemd
print_status "💾 Creating environment configuration..."
sudo tee /etc/tosti-fridge.env > /dev/null << EOF
# TOSTI Configuration
# Generated during installation on $(date)
TOSTI_CLIENT_SECRET=$CLIENT_SECRET
TOSTI_CLIENT_ID=$CLIENT_ID
TOSTI_API_BASE_URL=$API_BASE_URL
TOSTI_SERIAL_DEVICE=$SERIAL_DEVICE
EOF

sudo chown root:pi /etc/tosti-fridge.env
sudo chmod 640 /etc/tosti-fridge.env

# Set proper ownership
sudo chown -R "$SERVICE_USER:$SERVICE_USER" "$APP_DIR"

# Create main application service
print_status "🔧 Creating TOSTI fridge service..."
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null << EOF
[Unit]
Description=TOSTI Fridge Client
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$APP_DIR/client
Environment=PATH=/home/pi/.local/bin:/usr/local/bin:/usr/bin:/bin
EnvironmentFile=/etc/tosti-fridge.env
ExecStart=/home/pi/.local/bin/poetry run python client.py --settings settings.production
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
print_status "🚀 Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}.service

# Start service
sudo systemctl start ${SERVICE_NAME}.service

# Show status
print_status "📊 Installation complete! Service status:"
echo
sudo systemctl status ${SERVICE_NAME}.service --no-pager -l

print_status "📝 Configuration notes:"
echo "1. ✅ API credentials configured: $CLIENT_ID"
echo "2. ✅ Serial port configured: $SERIAL_DEVICE"
echo "3. ✅ Service configured and started"
echo "4. 🔧 Configure your fridge locks in $APP_DIR/client/settings/production.py if needed"
echo
print_status "🎉 Your TOSTI Fridge Client is ready to use!"
echo "🧪 Test QR scanner by scanning a code - the result should appear in logs"
echo
print_status "🛠️  Useful commands:"
echo "  📝 View logs: sudo journalctl -u $SERVICE_NAME -f"
echo "  🧪 Test serial port: ./manage_tosti.sh test"
echo "  🔄 Restart:   sudo systemctl restart $SERVICE_NAME"
echo "  ⏹️  Stop:      sudo systemctl stop $SERVICE_NAME"
echo "  📊 Status:    sudo systemctl status $SERVICE_NAME"
echo "  ⚙️  Edit config: ./manage_tosti.sh env"

print_status "🔄 To restart service after configuration changes:"
echo "  ./manage_tosti.sh restart"

print_status "🎉 Installation completed successfully! 🎉"