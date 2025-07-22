#!/bin/bash

echo "Kali Attacker Container Ready"
echo "============================"

TARGET_IP=${TARGET_IP:-192.168.100.10}

echo "Target IP: $TARGET_IP"
echo "Available attack scripts:"
echo "  - attack-ssh.sh   : SSH brute force"
echo "  - attack-ftp.sh   : FTP brute force"
echo "  - attack-http.sh  : HTTP brute force"
echo ""

# Esperar a que el objetivo esté disponible
echo "Waiting for target to be ready..."
while ! ping -c 1 $TARGET_IP &> /dev/null; do
    echo "Target not ready, waiting..."
    sleep 5
done

echo "Target is ready!"

# Verificar puertos abiertos
echo "Scanning target ports..."
nmap -sT -p 21,22,80 $TARGET_IP

echo ""
echo "Container ready for manual attacks."
echo "Connect with: docker exec -it kali-attacker bash"
echo "Or run automated attacks:"
echo "  docker exec kali-attacker /opt/attacks/attack-ssh.sh"

# Mantener contenedor activo
exec /bin/bash