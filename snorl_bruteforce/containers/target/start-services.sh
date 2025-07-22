#!/bin/bash

echo "Starting vulnerable services for research lab..."

# Iniciar SSH
service ssh start
echo "SSH started on port 22"

# Iniciar FTP
service vsftpd start
echo "FTP started on port 21"

# Iniciar Apache
service apache2 start
echo "Apache started on port 80"

# Configurar logging detallado
echo "Configuring detailed logging..."

# SSH logging
sed -i 's/#LogLevel INFO/LogLevel VERBOSE/' /etc/ssh/sshd_config

# Reiniciar SSH con nueva configuración
service ssh restart

# Mostrar servicios activos
echo "Active services:"
netstat -tlnp | grep -E ':(22|21|80|23) '

# Mantener el contenedor corriendo
echo "Services started. Container ready for testing."
echo "Target services:"
echo "  SSH: port 22 (users: testuser1/password, testuser2/123456, admin/admin, guest/guest, root/toor)"
echo "  FTP: port 21 (same users + anonymous access)"
echo "  HTTP: port 80 (basic auth: admin/admin, test/password)"

# Log monitoring loop
tail -f /var/log/auth.log /var/log/vsftpd.log /var/log/apache2/access.log 2>/dev/null &

# Mantener contenedor activo
while true; do
    sleep 60
    # Verificar que los servicios sigan corriendo
    if ! pgrep sshd > /dev/null; then
        echo "Restarting SSH service"
        service ssh start
    fi
    if ! pgrep vsftpd > /dev/null; then
        echo "Restarting FTP service"
        service vsftpd start
    fi
    if ! pgrep apache2 > /dev/null; then
        echo "Restarting Apache service"
        service apache2 start
    fi
done