# Laboratorio de Investigación: Snort vs Ataques de Fuerza Bruta

## Descripción

Este repositorio contiene la infraestructura completa para realizar investigación académica sobre el comportamiento del sistema de detección de intrusos Snort ante ataques de fuerza bruta tradicionales.

## Estructura del Proyecto

```
snorl_bruteforce/
├── snort_config/           # Configuraciones de Snort IDS/IPS
│   ├── etc/               # Archivos de configuración principal
│   ├── rules/             # Reglas personalizadas de detección
│   ├── logs/              # Directorio para logs de Snort
│   └── scripts/           # Scripts para gestión de Snort
├── target_services/        # Servicios vulnerables objetivo
│   ├── ssh/               # Configuración SSH vulnerable
│   └── ftp/               # Configuración FTP vulnerable
├── attack_tools/           # Herramientas de ataque para testing
├── documentation/          # Documentación del laboratorio
└── README.md              # Este archivo
```

## Configuración Rápida (Docker)

### 1. Iniciar Laboratorio

```bash
# Construir e iniciar contenedores
docker-compose up -d --build

# Verificar estado
docker ps
```

### 2. Ejecutar Ataques SSH

```bash
# Ataque básico
docker exec kali-attacker hydra -l admin -p admin ssh://target-ubuntu:22

# Ataque con múltiples credenciales
docker exec kali-attacker hydra -L /tmp/users.txt -P /tmp/pass.txt ssh://target-ubuntu:22 -t 8
```

### 3. Monitorear con Snort

```bash
# Ver logs de Snort
docker logs snort-monitor

# Analizar tráfico capturado
docker exec snort-monitor tcpdump -r /var/log/snort/snort.log.* -c 20

# Detener laboratorio
docker-compose down
```

## Casos de Uso

### Ataques SSH
- Fuerza bruta con diccionarios
- Ataques lentos para evasión
- Conexiones masivas simultáneas

### Ataques FTP
- Brute force contra usuarios
- Ataques a acceso anónimo
- Enumeración de cuentas

### Análisis de Detección
- Tiempo de respuesta de Snort
- Precisión de alertas
- Efectividad de reglas

## Reglas de Snort Incluidas

- Detección de múltiples intentos fallidos
- Patrones de conexión sospechosos  
- Identificación de herramientas automatizadas
- Correlación de eventos de seguridad

## Consideraciones Éticas

⚠️ **IMPORTANTE**: Este laboratorio está diseñado exclusivamente para:
- Investigación académica autorizada
- Entornos controlados y aislados
- Fines educativos en ciberseguridad

**NO utilizar** en sistemas de producción o sin autorización explícita.

## Resultados Esperados

- Análisis de efectividad de Snort
- Documentación de patrones de ataque
- Recomendaciones de configuración
- Contribuciones a la investigación en IDS

## Requisitos del Sistema

- Ubuntu Server 20.04+ (objetivo)
- Kali Linux 2023+ (atacante)
- Snort 2.9+ o 3.x (IDS)
- Red aislada 192.168.1.0/24
- Mínimo 4GB RAM por servidor

## Licencia

Este proyecto es para uso académico y de investigación únicamente.

---
*Proyecto de investigación en ciberseguridad defensiva*