#!/bin/bash
# Script to start Snort IDS/IPS for brute force research
# Academic research configuration

SNORT_CONFIG="/home/labctrl/Documents/snor/snorl_bruteforce/snort_config/etc/snort.conf"
LOG_DIR="/home/labctrl/Documents/snor/snorl_bruteforce/snort_config/logs"
INTERFACE="eth0"  # Change to your network interface

echo "Starting Snort IDS for Brute Force Research Lab..."

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root for packet capture"
   echo "Usage: sudo ./start_snort.sh"
   exit 1
fi

# Check if Snort is installed
if ! command -v snort &> /dev/null; then
    echo "Snort is not installed. Please install it first:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install snort"
    exit 1
fi

# Check if config file exists
if [[ ! -f "$SNORT_CONFIG" ]]; then
    echo "Snort configuration file not found: $SNORT_CONFIG"
    echo "Please ensure the configuration file exists."
    exit 1
fi

# Test configuration
echo "Testing Snort configuration..."
snort -T -c "$SNORT_CONFIG"

if [[ $? -ne 0 ]]; then
    echo "Snort configuration test failed. Please check the configuration."
    exit 1
fi

echo "Configuration test passed."

# Start Snort in different modes based on parameter
case "${1:-ids}" in
    "ids")
        echo "Starting Snort in IDS mode..."
        snort -A fast -c "$SNORT_CONFIG" -i "$INTERFACE" -l "$LOG_DIR" -D
        ;;
    "ips")
        echo "Starting Snort in IPS mode..."
        echo "Note: IPS mode requires iptables rules for packet forwarding"
        snort -Q -c "$SNORT_CONFIG" -i "$INTERFACE" -l "$LOG_DIR" -D
        ;;
    "console")
        echo "Starting Snort in console mode (no daemon)..."
        snort -A console -c "$SNORT_CONFIG" -i "$INTERFACE" -l "$LOG_DIR"
        ;;
    "test")
        echo "Testing packet capture on interface $INTERFACE..."
        snort -v -i "$INTERFACE"
        ;;
    *)
        echo "Usage: $0 [ids|ips|console|test]"
        echo "  ids     - Start in IDS mode (daemon)"
        echo "  ips     - Start in IPS mode (daemon)"
        echo "  console - Start in console mode (interactive)"
        echo "  test    - Test packet capture"
        exit 1
        ;;
esac

if [[ "${1:-ids}" != "console" && "${1:-ids}" != "test" ]]; then
    echo "Snort started successfully."
    echo "Logs will be written to: $LOG_DIR"
    echo "To stop Snort: sudo pkill snort"
    echo "To view alerts: tail -f $LOG_DIR/alert"
fi