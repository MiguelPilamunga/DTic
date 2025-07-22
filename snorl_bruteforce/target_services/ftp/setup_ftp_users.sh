#!/bin/bash
# Script to set up FTP service for brute force research
# WARNING: Creates intentionally vulnerable FTP setup for research only

echo "Setting up FTP service for brute force research..."

# Install vsftpd if not present
if ! command -v vsftpd &> /dev/null; then
    echo "Installing vsftpd..."
    apt-get update
    apt-get install -y vsftpd
fi

# Create FTP directories
mkdir -p /var/ftp/pub
mkdir -p /var/ftp/upload
mkdir -p /var/ftp/download

# Set permissions for anonymous access
chmod 755 /var/ftp
chmod 777 /var/ftp/pub
chmod 777 /var/ftp/upload
chmod 755 /var/ftp/download

# Create test files
echo "This is a test file for FTP research" > /var/ftp/pub/test.txt
echo "Anonymous FTP access enabled for research" > /var/ftp/pub/readme.txt

# Create FTP users with weak passwords
ftp_users=("ftpuser1" "ftpuser2" "ftpadmin" "anonymous" "ftp")
ftp_passwords=("ftp123" "password" "admin" "" "ftp")

for i in "${!ftp_users[@]}"; do
    username="${ftp_users[$i]}"
    password="${ftp_passwords[$i]}"
    
    if [[ "$username" != "anonymous" && "$username" != "ftp" ]]; then
        # Create user if doesn't exist
        if ! id "$username" &>/dev/null; then
            useradd -m -s /bin/bash "$username"
            echo "$username:$password" | chpasswd
            echo "Created FTP user: $username with password: $password"
        else
            echo "FTP user $username already exists"
            echo "$username:$password" | chpasswd
            echo "Updated password for $username"
        fi
        
        # Create user's FTP directory
        mkdir -p "/home/$username/ftp"
        chown "$username:$username" "/home/$username/ftp"
        chmod 755 "/home/$username/ftp"
    fi
done

# Set up anonymous FTP user
if ! id "ftp" &>/dev/null; then
    useradd -d /var/ftp -s /bin/false ftp
fi

# Create welcome message
cat > /var/ftp/.message << 'EOF'
Welcome to Research Lab FTP Server
==================================

This FTP server is configured for academic security research.
All connections are logged and monitored for analysis.

Available directories:
- /pub     - Public files for download
- /upload  - Upload directory
- /download - Download directory

WARNING: This is a research environment with intentionally
vulnerable configurations. Do not use in production.
EOF

# Create directory-specific messages
echo "Public file sharing directory" > /var/ftp/pub/.message
echo "Upload your test files here" > /var/ftp/upload/.message
echo "Download test files from here" > /var/ftp/download/.message

# Set ownership
chown -R ftp:ftp /var/ftp
chown root:root /var/ftp

# Create vulnerable configuration backup
cp vsftpd_vulnerable.conf /etc/vsftpd.conf.research

echo "FTP service setup complete!"
echo ""
echo "Created FTP users for brute force testing:"
echo "  ftpuser1:ftp123"
echo "  ftpuser2:password"
echo "  ftpadmin:admin"
echo "  anonymous:(no password - anonymous access enabled)"
echo ""
echo "FTP directories created:"
echo "  /var/ftp/pub - Public access"
echo "  /var/ftp/upload - Upload directory"
echo "  /var/ftp/download - Download directory"
echo ""
echo "To start FTP service with vulnerable config:"
echo "  sudo cp /etc/vsftpd.conf.research /etc/vsftpd.conf"
echo "  sudo systemctl restart vsftpd"
echo ""
echo "WARNING: This FTP setup is intentionally vulnerable for research only!"