#!/bin/bash
# Setup Environment for Enhanced SSH Brute Force Attack
# Creates Python virtual environment and installs dependencies

echo "Setting up Enhanced SSH Brute Force Attack Environment"
echo "===================================================="

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

# Create virtual environment
VENV_DIR="/home/labctrl/Documents/snor/snorl_bruteforce/attack_tools/venv"

echo "Creating virtual environment..."
python3 -m venv "$VENV_DIR"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install required dependencies
echo "Installing dependencies..."
pip install paramiko==3.4.0
pip install requests==2.31.0
pip install sqlalchemy==2.0.23
pip install numpy==1.24.3
pip install pandas==2.0.3

# Create requirements.txt for reference
cat > "$VENV_DIR/../requirements.txt" << 'EOF'
paramiko==3.4.0
requests==2.31.0
sqlalchemy==2.0.23
numpy==1.24.3
pandas==2.0.3
EOF

# Create activation script
cat > "$VENV_DIR/../activate_env.sh" << 'EOF'
#!/bin/bash
# Activate the virtual environment for enhanced SSH attacks
source /home/labctrl/Documents/snor/snorl_bruteforce/attack_tools/venv/bin/activate
echo "Virtual environment activated"
echo "Available commands:"
echo "  python enhanced_bruteforce_ssh.py"
echo "  deactivate (to exit environment)"
EOF

chmod +x "$VENV_DIR/../activate_env.sh"

# Test imports
echo "Testing imports..."
python3 -c "
import paramiko
import requests
import sqlalchemy
import numpy
import pandas
print('All dependencies installed successfully!')
"

echo ""
echo "Setup completed successfully!"
echo "=========================="
echo "To activate the environment:"
echo "  source activate_env.sh"
echo ""
echo "To run the enhanced attack:"
echo "  python enhanced_bruteforce_ssh.py"
echo ""
echo "Dependencies installed:"
echo "  - paramiko (SSH client)"
echo "  - requests (HTTP requests)"
echo "  - sqlalchemy (Database ORM)"
echo "  - numpy (Numerical computing)"
echo "  - pandas (Data analysis)"
echo ""
echo "Virtual environment: $VENV_DIR"