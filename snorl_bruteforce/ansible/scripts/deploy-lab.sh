#!/bin/bash
# Script de Despliegue del Laboratorio de Ataques Distribuidos
# Propósito: Automatizar la configuración completa del laboratorio

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directorios
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ANSIBLE_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_DIR="$(dirname "$ANSIBLE_DIR")"

echo -e "${GREEN}[INFO]${NC} Iniciando despliegue del laboratorio de ataques distribuidos..."

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [opciones]"
    echo ""
    echo "Opciones:"
    echo "  --setup-only     Solo configurar el laboratorio, no ejecutar ataques"
    echo "  --attack-only    Solo ejecutar ataques (requiere laboratorio configurado)"
    echo "  --full          Configurar y ejecutar ataques completos"
    echo "  --clean         Limpiar el laboratorio"
    echo "  --help          Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 --setup-only   # Solo configurar"
    echo "  $0 --full        # Configurar y atacar"
    echo "  $0 --clean       # Limpiar todo"
}

# Función para verificar dependencias
check_dependencies() {
    echo -e "${YELLOW}[CHECK]${NC} Verificando dependencias..."
    
    # Verificar Ansible
    if ! command -v ansible &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} Ansible no está instalado. Instalando..."
        sudo apt-get update
        sudo apt-get install -y ansible
    fi
    
    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} Docker no está instalado. Instalando..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
    fi
    
    # Verificar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} Docker Compose no está instalado. Instalando..."
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
    
    echo -e "${GREEN}[OK]${NC} Todas las dependencias están disponibles"
}

# Función para configurar el laboratorio
setup_lab() {
    echo -e "${YELLOW}[SETUP]${NC} Configurando laboratorio..."
    
    cd "$ANSIBLE_DIR"
    
    # Crear directorios necesarios
    mkdir -p logs/attackers logs/targets logs/monitors reports
    
    # Generar claves SSH si no existen
    if [ ! -f ~/.ssh/lab_key ]; then
        echo -e "${YELLOW}[SETUP]${NC} Generando claves SSH del laboratorio..."
        ssh-keygen -t rsa -b 2048 -f ~/.ssh/lab_key -N ""
    fi
    
    # Verificar conectividad a hosts
    echo -e "${YELLOW}[SETUP]${NC} Verificando conectividad..."
    ansible all -i inventory/hosts -m ping --ask-pass || {
        echo -e "${RED}[ERROR]${NC} No se puede conectar a algunos hosts"
        echo "Asegúrate de que:"
        echo "1. Los hosts están accesibles"
        echo "2. Las credenciales SSH son correctas"
        echo "3. El inventario está configurado correctamente"
        exit 1
    }
    
    # Ejecutar playbook de configuración
    echo -e "${YELLOW}[SETUP]${NC} Ejecutando configuración del laboratorio..."
    ansible-playbook -i inventory/hosts playbooks/setup-distributed-lab.yml --ask-become-pass
    
    echo -e "${GREEN}[OK]${NC} Laboratorio configurado exitosamente"
}

# Función para ejecutar ataques
run_attacks() {
    echo -e "${YELLOW}[ATTACK]${NC} Ejecutando ataques distribuidos..."
    
    cd "$ANSIBLE_DIR"
    
    # Verificar que Snort está ejecutándose
    echo -e "${YELLOW}[CHECK]${NC} Verificando estado de Snort..."
    ansible monitors -i inventory/hosts -m shell -a "systemctl is-active snort-monitor" || {
        echo -e "${YELLOW}[WARN]${NC} Snort no está ejecutándose, iniciando..."
        ansible monitors -i inventory/hosts -m service -a "name=snort-monitor state=started" --become
    }
    
    # Ejecutar ataques distribuidos
    echo -e "${YELLOW}[ATTACK]${NC} Iniciando coordinación de ataques..."
    ansible-playbook -i inventory/hosts playbooks/run-distributed-attack.yml
    
    # Generar reporte consolidado
    echo -e "${YELLOW}[REPORT]${NC} Generando reporte consolidado..."
    generate_report
    
    echo -e "${GREEN}[OK]${NC} Ataques ejecutados exitosamente"
}

# Función para generar reporte
generate_report() {
    local report_file="reports/distributed-attack-report-$(date +%Y%m%d-%H%M%S).txt"
    
    echo "=== REPORTE DE ATAQUE DISTRIBUIDO ===" > "$report_file"
    echo "Fecha: $(date)" >> "$report_file"
    echo "Duración: Variable por nodo" >> "$report_file"
    echo "" >> "$report_file"
    
    echo "=== RESUMEN POR NODO ===" >> "$report_file"
    for report in reports/node-*-report.txt; do
        if [ -f "$report" ]; then
            echo "--- $(basename "$report") ---" >> "$report_file"
            cat "$report" >> "$report_file"
            echo "" >> "$report_file"
        fi
    done
    
    echo "=== LOGS DE SNORT ===" >> "$report_file"
    if [ -d "logs/monitors" ]; then
        find logs/monitors -name "*.log" -exec echo "--- {} ---" \; -exec head -20 {} \; >> "$report_file"
    fi
    
    echo -e "${GREEN}[OK]${NC} Reporte generado: $report_file"
}

# Función para limpiar el laboratorio
clean_lab() {
    echo -e "${YELLOW}[CLEAN]${NC} Limpiando laboratorio..."
    
    cd "$ANSIBLE_DIR"
    
    # Detener servicios
    ansible attackers -i inventory/hosts -m service -a "name=distributed-attack state=stopped" --become || true
    ansible monitors -i inventory/hosts -m service -a "name=snort-monitor state=stopped" --become || true
    
    # Limpiar logs
    ansible all -i inventory/hosts -m shell -a "rm -rf /var/log/distributed-attack/*" --become || true
    
    # Limpiar archivos temporales
    rm -rf logs/* reports/*
    
    echo -e "${GREEN}[OK]${NC} Laboratorio limpiado"
}

# Función para monitorear el laboratorio
monitor_lab() {
    echo -e "${YELLOW}[MONITOR]${NC} Iniciando monitoreo del laboratorio..."
    
    cd "$ANSIBLE_DIR"
    
    while true; do
        clear
        echo "=== ESTADO DEL LABORATORIO ==="
        echo "Timestamp: $(date)"
        echo ""
        
        echo "--- Estado de Atacantes ---"
        ansible attackers -i inventory/hosts -m shell -a "ps aux | grep attack_coordinator | grep -v grep | wc -l" 2>/dev/null || echo "Error consultando atacantes"
        echo ""
        
        echo "--- Estado de Snort ---"
        ansible monitors -i inventory/hosts -m shell -a "systemctl is-active snort-monitor" 2>/dev/null || echo "Error consultando Snort"
        echo ""
        
        echo "--- Alertas Recientes ---"
        ansible monitors -i inventory/hosts -m shell -a "tail -5 /var/log/snort/alerts.txt" 2>/dev/null || echo "Sin alertas disponibles"
        echo ""
        
        echo "Presiona Ctrl+C para salir"
        sleep 30
    done
}

# Procesamiento de argumentos
case "${1:-}" in
    --setup-only)
        check_dependencies
        setup_lab
        ;;
    --attack-only)
        run_attacks
        ;;
    --full)
        check_dependencies
        setup_lab
        run_attacks
        ;;
    --clean)
        clean_lab
        ;;
    --monitor)
        monitor_lab
        ;;
    --help)
        show_help
        ;;
    *)
        echo -e "${RED}[ERROR]${NC} Opción no válida: ${1:-}"
        show_help
        exit 1
        ;;
esac

echo -e "${GREEN}[DONE]${NC} Operación completada exitosamente"