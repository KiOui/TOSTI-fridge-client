# 🍟 TOSTI Fridge Client - Raspberry Pi Installation

This guide will help you install and configure the TOSTI Fridge Client as a background service on your Raspberry Pi with QR scanner serial port input support.

## ✨ Features

- **🔒 Environment Variable Configuration**: Secure API credential management
- **🚀 Background Service**: Runs automatically on boot  
- **📱 Serial Port QR Scanner**: Direct USB QR scanner integration via serial port
- **🛠️ Service Management**: Easy start/stop/restart commands
- **🔄 Zero Code Changes**: Works with your existing Python code

## 🚀 Quick Installation

### 1. Download and Run Interactive Installer

```bash
# Make scripts executable
chmod +x install_tosti_service.sh manage_tosti.sh setup_env.sh

# Run interactive installation
./install_tosti_service.sh
```

The installer will prompt you for:
- **📱 Serial device path** (for your QR scanner)
- **🔑 TOSTI API credentials** (Client ID, Client Secret, API URL)

### 2. Configure Fridge Locks (Optional)

Only needed if you want to change the default configuration:

```bash
./manage_tosti.sh config
```

### 3. Test Your Setup

```bash
# Test QR scanner
./manage_tosti.sh test

# Check status  
./manage_tosti.sh status

# View logs
./manage_tosti.sh logs
```

## 🎉 Installation Complete!

The installation is fully interactive - no separate configuration steps needed!

## Management Commands

Use the `manage_tosti.sh` script for all service operations:

```bash
./manage_tosti.sh status      # Show service status and configuration
./manage_tosti.sh start       # Start services
./manage_tosti.sh stop        # Stop services
./manage_tosti.sh restart     # Restart services
./manage_tosti.sh logs        # View live logs
./manage_tosti.sh config      # Edit fridge configuration
./manage_tosti.sh env         # Edit API credentials
./manage_tosti.sh test        # Test keyboard input
./manage_tosti.sh uninstall   # Remove services
```

## Configuration Files

### Environment Variables (`/etc/tosti-fridge.env`)
```bash
TOSTI_CLIENT_SECRET=your_secret_here
TOSTI_CLIENT_ID=your_client_id_here
TOSTI_API_BASE_URL=https://tosti.science.ru.nl
TOSTI_SERIAL_DEVICE=/dev/serial/by-id/your-qr-scanner-device
```

### Application Config (`/opt/tosti-fridge-client/client/settings/production.py`)
The production.py file automatically reads configuration from environment variables:
```python
CLIENT_SECRET = os.getenv('TOSTI_CLIENT_SECRET')
CLIENT_ID = os.getenv('TOSTI_CLIENT_ID')
API_BASE_URL = os.getenv('TOSTI_API_BASE_URL', 'https://tosti.science.ru.nl')
SCANNER_INPUT_PARAMETERS = os.getenv("TOSTI_SERIAL_DEVICE")
```

Configure:
- Fridge lock configuration
- GPIO pin assignments  
- Logging settings

## Architecture

### Services Created

1. **tosti-fridge.service**
   - Your main TOSTI application
   - Reads QR scan results directly from serial port
   - Manages fridge locks via GPIO

## Security Features

- **Environment Variables**: API credentials stored securely outside code
- **File Permissions**: Environment file readable only by root
- **Service Isolation**: Each service runs with minimal permissions
- **Input Group**: Proper keyboard access permissions

## Troubleshooting

### Check Service Status
```bash
./manage_tosti.sh status
```

### View Logs
```bash
./manage_tosti.sh logs
```

### Test Serial Port
```bash
./manage_tosti.sh test
```

### Check Serial Device
```bash
ls /dev/serial/by-id/
```

### Manual Serial Port Test
```bash
sudo cat /dev/serial/by-id/your-qr-scanner-device
# Example: sudo cat /dev/serial/by-id/usb-SM_SM-2D_PRODUCT_USB_UART_APP-000000000-if00
```

### Verify Environment Variables
```bash
sudo cat /etc/tosti-fridge.env
```

### Manual Service Commands
```bash
sudo systemctl status tosti-fridge
sudo systemctl status tosti-keyboard-reader
sudo journalctl -u tosti-fridge -f
```

## Common Issues

### QR Scanner Not Detected
- Check USB connection
- Verify device path: `ls /dev/serial/by-id/`
- Update scanner device in `/etc/tosti-fridge.env`
- Ensure scanner is in serial/UART mode (not HID keyboard mode)

### Permission Denied on Serial Port
- Ensure user is in dialout group: `groups pi`
- Add if missing: `sudo usermod -a -G dialout pi`
- Restart service after group change

### API Connection Failed
- Check credentials in `/etc/tosti-fridge.env`
- Verify API base URL
- Check network connectivity

### GPIO Issues
- Ensure running on Raspberry Pi
- Check GPIO pin configuration
- Verify wiring connections

### QR Codes Not Recognized
- Test serial port with: `./manage_tosti.sh test`
- Verify scanner outputs to correct device
- Check scanner configuration for serial output mode
- Some scanners need specific baud rate settings

## File Locations

- **Application**: `/opt/tosti-fridge-client/`
- **Environment**: `/etc/tosti-fridge.env`
- **Services**: `/etc/systemd/system/tosti-*.service`
- **Logs**: `journalctl -u tosti-fridge`
- **Keyboard Script**: `/usr/local/bin/tosti-keyboard-reader`

## Advanced Configuration

### Custom Serial Port Device
Edit `/etc/tosti-fridge.env` and update:
```bash
TOSTI_SERIAL_DEVICE=/dev/serial/by-id/your-qr-scanner-device
```

## Updating

To update the application:
```bash
# Stop services
./manage_tosti.sh stop

# Update application files
# ... copy new files ...

# Restart services
./manage_tosti.sh restart
```

## Uninstallation

To completely remove the TOSTI services:
```bash
./manage_tosti.sh uninstall
```

This preserves the application directory but removes all services and environment files.