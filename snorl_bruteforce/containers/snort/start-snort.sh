#!/bin/bash

echo "Starting Snort IDS for Brute Force Research Lab..."

# Esperar a que la red esté lista
sleep 5

# Verificar conectividad con el objetivo
TARGET_IP=${TARGET_IP:-192.168.100.10}
echo "Testing connectivity to target: $TARGET_IP"
ping -c 3 $TARGET_IP || echo "Warning: Cannot reach target IP"

# Crear directorios de logs si no existen
mkdir -p /var/log/snort
chown snort:snort /var/log/snort

# Configurar interfaz de red
INTERFACE=${MONITOR_INTERFACE:-eth0}
echo "Monitoring interface: $INTERFACE"

# Verificar que existe la configuración
if [[ ! -f /etc/snort/snort.conf ]]; then
    echo "Snort configuration not found. Using default basic config."
    
    # Crear configuración básica
    cat > /etc/snort/snort.conf << 'EOF'
# Basic Snort configuration for research lab
var HOME_NET 192.168.100.0/24
var EXTERNAL_NET !$HOME_NET
var SSH_SERVERS $HOME_NET
var FTP_SERVERS $HOME_NET

# Rule paths
var RULE_PATH /etc/snort/rules
var SO_RULE_PATH /etc/snort/so_rules
var PREPROC_RULE_PATH /etc/snort/preproc_rules

# Output plugins
output alert_fast: /var/log/snort/alert
output log_tcpdump: /var/log/snort/snort.log

# Include configs
include classification.config
include reference.config

# Include preprocessor rules (empty files to avoid errors)
include $PREPROC_RULE_PATH/preprocessor.rules
include $PREPROC_RULE_PATH/decoder.rules
include $PREPROC_RULE_PATH/sensitive-data.rules

# Include rule files
include $RULE_PATH/local.rules
include $RULE_PATH/brute-force.rules
include $RULE_PATH/ssh.rules
include $RULE_PATH/ftp.rules

# Basic preprocessors
preprocessor frag3_global: max_frags 65536
preprocessor frag3_engine: policy first detect_anomalies

preprocessor stream5_global: track_tcp yes, track_udp yes
preprocessor stream5_tcp: policy first, use_static_footprint_sizes

# Performance
config detection: search-method ac-split search-optimize max-pattern-len 20
EOF
fi

# Probar configuración
echo "Testing Snort configuration..."
snort -T -c /etc/snort/snort.conf -i $INTERFACE

if [[ $? -ne 0 ]]; then
    echo "Configuration test failed. Starting with basic mode..."
    # Modo básico sin reglas complejas
    snort -v -i $INTERFACE -l /var/log/snort &
else
    echo "Configuration test passed. Starting full IDS mode..."
    # Modo completo con reglas
    snort -A fast -c /etc/snort/snort.conf -i $INTERFACE -l /var/log/snort -D
fi

echo "Snort IDS started successfully"
echo "Logs location: /var/log/snort/"
echo "Monitoring network: $TARGET_NETWORK"
echo "Target server: $TARGET_IP"

# Monitor de logs en tiempo real
echo "Starting log monitoring..."
tail -f /var/log/snort/alert 2>/dev/null &

# Mantener el contenedor activo
while true; do
    sleep 60
    if ! pgrep snort > /dev/null; then
        echo "Snort stopped. Restarting..."
        snort -A fast -c /etc/snort/snort.conf -i $INTERFACE -l /var/log/snort -D 2>/dev/null || \
        snort -v -i $INTERFACE -l /var/log/snort &
    fi
done