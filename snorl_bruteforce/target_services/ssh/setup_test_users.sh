#!/bin/bash
# Script to create test users for SSH brute force research
# WARNING: Creates intentionally weak accounts for research only

echo "Setting up test users for SSH brute force research..."

# Create test users with weak passwords
users=("testuser1" "testuser2" "admin" "guest" "user")
passwords=("password" "123456" "admin" "guest" "test")

for i in "${!users[@]}"; do
    username="${users[$i]}"
    password="${passwords[$i]}"
    
    # Create user if doesn't exist
    if ! id "$username" &>/dev/null; then
        useradd -m -s /bin/bash "$username"
        echo "$username:$password" | chpasswd
        echo "Created user: $username with password: $password"
    else
        echo "User $username already exists"
        echo "$username:$password" | chpasswd
        echo "Updated password for $username"
    fi
done

# Create a user with no password (for testing)
if ! id "nopassuser" &>/dev/null; then
    useradd -m -s /bin/bash nopassuser
    passwd -d nopassuser
    echo "Created user: nopassuser (no password)"
fi

# Set up some users with common weak passwords
common_users=("root" "administrator" "service")
common_passwords=("toor" "password" "service123")

for i in "${!common_users[@]}"; do
    username="${common_users[$i]}"
    password="${common_passwords[$i]}"
    
    if id "$username" &>/dev/null; then
        echo "$username:$password" | chpasswd
        echo "Set weak password for existing user: $username"
    fi
done

# Create SSH banner
cat > /etc/ssh/banner << 'EOF'
***************************************************************************
                    RESEARCH LAB - AUTHORIZED ACCESS ONLY
    
    This system is configured for academic security research purposes.
    All connections are monitored and logged for analysis.
    
    Unauthorized access is prohibited.
***************************************************************************
EOF

# Set appropriate permissions
chmod 644 /etc/ssh/banner

echo "Test user setup complete!"
echo ""
echo "Created users for brute force testing:"
echo "  testuser1:password"
echo "  testuser2:123456"
echo "  admin:admin"
echo "  guest:guest"
echo "  user:test"
echo "  nopassuser:(no password)"
echo ""
echo "WARNING: These are intentionally weak accounts for research only!"
echo "Do not use in production environments."