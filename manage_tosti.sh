#!/bin/bash

# TOSTI Fridge Client Management Script

SERVICE_NAME="tosti-fridge"
APP_DIR="/opt/tosti-fridge-client"
CONFIG_FILE="$APP_DIR/client/settings/production.py"
ENV_FILE="/etc/tosti-fridge.env"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} ❌ $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} ⚠️  $1"
}

show_help() {
    echo "TOSTI Fridge Client Management Script"
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  status      Show service status"
    echo "  start       Start services"
    echo "  stop        Stop services"
    echo "  restart     Restart services"
    echo "  logs        Show live logs"
    echo "  config      Edit fridge configuration"
    echo "  env         Edit environment variables (API credentials)"
    echo "  test        Test serial port input"
    echo "  install     Re-run installation"
    echo "  uninstall   Remove services"
    echo "  help        Show this help"
}

show_status() {
    print_status "📊 Service Status:"
    echo
    echo "🍟 TOSTI Fridge Client:"
    sudo systemctl status $SERVICE_NAME --no-pager -l
    echo
    echo "⚙️  Environment Configuration:"
    if [ -f "$ENV_FILE" ]; then
        echo "  📄 Environment file: $ENV_FILE"
        if sudo grep -q "TOSTI_CLIENT_SECRET=.*[^=]" "$ENV_FILE"; then
            echo "  🔐 CLIENT_SECRET: [SET]"
        else
            echo "  🔐 CLIENT_SECRET: [NOT SET]"
        fi
        if sudo grep -q "TOSTI_CLIENT_ID=.*[^=]" "$ENV_FILE"; then
            echo "  🆔 CLIENT_ID: [SET]"
        else
            echo "  🆔 CLIENT_ID: [NOT SET]"
        fi
        api_url=$(sudo grep "TOSTI_API_BASE_URL=" "$ENV_FILE" | cut -d'=' -f2-)
        echo "  🌐 API_BASE_URL: ${api_url:-[NOT SET]}"
        serial_port=$(sudo grep "TOSTI_SERIAL_INPUT=" "$ENV_FILE" | cut -d'=' -f2-)
        echo "  📱 SERIAL_INPUT: ${serial_port:-[NOT SET]}"

        # Check if serial device exists
        if [ -n "$serial_port" ] && [ -e "$serial_port" ]; then
            echo "  📱 Serial device: [FOUND] ✅"
        elif [ -n "$serial_port" ]; then
            echo "  📱 Serial device: [NOT FOUND] ❌"
        fi
    else
        echo "  📄 Environment file: [NOT FOUND] ❌"
    fi
}

start_services() {
    print_status "▶️  Starting service..."
    sudo systemctl start $SERVICE_NAME
    show_status
}

stop_services() {
    print_status "⏹️  Stopping service..."
    sudo systemctl stop $SERVICE_NAME
    show_status
}

restart_services() {
    print_status "🔄 Restarting service..."
    sudo systemctl restart $SERVICE_NAME
    show_status
}

show_logs() {
    print_status "📝 Showing live logs (Ctrl+C to exit)..."
    sudo journalctl -u $SERVICE_NAME -f
}

edit_config() {
    if [ -f "$CONFIG_FILE" ]; then
        print_status "Opening fridge configuration file..."
        nano "$CONFIG_FILE"
        print_status "Fridge configuration updated. Restart services? (y/n)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            restart_services
        fi
    else
        print_error "Configuration file not found: $CONFIG_FILE"
    fi
}

edit_env() {
    if [ -f "$ENV_FILE" ]; then
        print_status "Opening environment configuration (API credentials)..."
        sudo nano "$ENV_FILE"
        print_status "Environment variables updated. Restart services? (y/n)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            restart_services
        fi
    else
        print_error "Environment file not found: $ENV_FILE"
        print_status "You can create it with:"
        echo "sudo tee $ENV_FILE > /dev/null << EOF"
        echo "TOSTI_CLIENT_SECRET=your_secret_here"
        echo "TOSTI_CLIENT_ID=your_client_id_here"
        echo "TOSTI_API_BASE_URL=https://tosti.science.ru.nl"
        echo "EOF"
    fi
}

test_keyboard() {
    print_status "Testing serial port input (scan a QR code, Ctrl+C to exit)..."

    # Get serial port from environment file
    if [ -f "$ENV_FILE" ]; then
        serial_port=$(sudo grep "TOSTI_SERIAL_INPUT=" "$ENV_FILE" | cut -d'=' -f2-)
        if [ -n "$serial_port" ] && [ -e "$serial_port" ]; then
            print_status "Reading from serial port: $serial_port"
            sudo cat "$serial_port"
        else
            print_error "Serial port not found: $serial_port"
            echo "Available serial devices:"
            ls -la /dev/serial/by-id/ 2>/dev/null || echo "No serial devices found"
        fi
    else
        print_error "Environment file not found: $ENV_FILE"
    fi
}

uninstall_services() {
    print_warning "This will remove the TOSTI service and environment files. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        print_status "🗑️  Uninstalling service..."
        sudo systemctl stop $SERVICE_NAME
        sudo systemctl disable $SERVICE_NAME
        sudo rm -f /etc/systemd/system/${SERVICE_NAME}.service
        sudo rm -f "$ENV_FILE"
        sudo systemctl daemon-reload
        print_status "✅ Service uninstalled. Application directory $APP_DIR preserved."
    else
        print_status "❌ Uninstall cancelled."
    fi
}

# Main script logic
case "$1" in
    "status")
        show_status
        ;;
    "start")
        start_services
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        restart_services
        ;;
    "logs")
        show_logs
        ;;
    "config")
        edit_config
        ;;
    "env")
        edit_env
        ;;
    "test")
        test_keyboard
        ;;
    "uninstall")
        uninstall_services
        ;;
    "install")
        print_status "📦 Re-running installation..."
        bash install_tosti_service.sh
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    "")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo
        show_help
        exit 1
        ;;
esac