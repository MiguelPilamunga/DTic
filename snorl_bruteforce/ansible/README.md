# Laboratorio de Ataques Distribuidos con Ansible

## Descripción

Este módulo implementa la orquestación de ataques distribuidos usando Ansible para investigación defensiva. Simula patrones de botnet para evaluar la efectividad de sistemas de detección como Snort.

## Estructura del Proyecto

```
ansible/
├── inventory/
│   └── hosts                    # Inventario de hosts del laboratorio
├── playbooks/
│   ├── setup-distributed-lab.yml   # Configuración inicial
│   └── run-distributed-attack.yml  # Ejecución de ataques
├── templates/
│   ├── attack_coordinator.py.j2    # Coordinador de ataques
│   ├── distributed-attack.rules.j2 # Reglas de Snort
│   ├── usernames.txt.j2            # Lista de usuarios
│   └── passwords.txt.j2            # Lista de passwords
├── group_vars/
│   ├── attackers.yml               # Variables de atacantes
│   └── monitors.yml                # Variables de monitores
├── scripts/
│   └── deploy-lab.sh               # Script de despliegue
└── README.md                       # Este archivo
```

## Arquitectura del Laboratorio

### Componentes

1. **Nodos Atacantes (5)**: Simulan botnet distribuida
2. **Servidor Objetivo (1)**: Ubuntu con servicios vulnerables
3. **Monitor Snort (1)**: Sistema de detección
4. **Controlador Ansible (1)**: Orquestación central

### Red del Laboratorio

```
192.168.100.0/24
├── 192.168.100.10-14  # Atacantes
├── 192.168.100.100    # Objetivo
├── 192.168.100.200    # Monitor
└── 192.168.100.50     # Controlador
```

## Configuración Inicial

### 1. Preparar Entorno

```bash
# Instalar dependencias
sudo apt-get update
sudo apt-get install ansible docker.io docker-compose

# Configurar inventario
cp inventory/hosts.example inventory/hosts
# Editar IPs según tu entorno
```

### 2. Generar Claves SSH

```bash
# Generar claves para el laboratorio
ssh-keygen -t rsa -b 2048 -f ~/.ssh/lab_key -N ""

# Copiar claves a todos los hosts
ssh-copy-id -i ~/.ssh/lab_key.pub user@192.168.100.10
# Repetir para todos los hosts
```

### 3. Verificar Conectividad

```bash
# Probar conectividad
ansible all -i inventory/hosts -m ping
```

## Uso del Laboratorio

### Despliegue Automático

```bash
# Configurar y ejecutar laboratorio completo
./scripts/deploy-lab.sh --full

# Solo configurar (sin ejecutar ataques)
./scripts/deploy-lab.sh --setup-only

# Solo ejecutar ataques
./scripts/deploy-lab.sh --attack-only

# Limpiar laboratorio
./scripts/deploy-lab.sh --clean
```

### Despliegue Manual

#### 1. Configurar Laboratorio

```bash
# Configurar todos los componentes
ansible-playbook -i inventory/hosts playbooks/setup-distributed-lab.yml
```

#### 2. Ejecutar Ataques

```bash
# Ejecutar simulación de ataque distribuido
ansible-playbook -i inventory/hosts playbooks/run-distributed-attack.yml
```

#### 3. Monitorear Resultados

```bash
# Ver logs de Snort
ansible monitors -i inventory/hosts -m shell -a "tail -f /var/log/snort/alerts.txt"

# Ver logs de atacantes
ansible attackers -i inventory/hosts -m shell -a "tail -f /var/log/distributed-attack/node-*.log"
```

## Tipos de Ataques Implementados

### 1. SSH Distribuido
- **Coordinación**: 5 nodos atacando simultáneamente
- **Evasión**: Delays aleatorios entre intentos
- **Detección**: Correlación por destino

### 2. FTP Distribuido
- **Estrategia**: Rotación de credenciales
- **Timing**: Low-and-slow para evasión
- **Detección**: Patrones de usuario/contraseña

### 3. HTTP Distribuido
- **Objetivo**: Páginas de administración
- **Método**: Fuerza bruta en formularios
- **Detección**: Análisis de User-Agent

## Capacidades Defensivas

### Reglas de Snort Implementadas

1. **Detección de Coordinación**
   - Múltiples fuentes → Un destino
   - Correlación temporal
   - Patrones de sincronización

2. **Análisis de Comportamiento**
   - Rotación de IPs
   - Evasión temporal
   - Volumen distribuido

3. **Correlación Cross-Service**
   - Ataques simultáneos SSH/FTP/HTTP
   - Detección de herramientas automatizadas
   - Análisis de User-Agent

### Métricas de Detección

```bash
# Verificar alertas generadas
ansible monitors -i inventory/hosts -m shell -a "grep 'DISTRIBUTED' /var/log/snort/alerts.txt | wc -l"

# Analizar tipos de alerta
ansible monitors -i inventory/hosts -m shell -a "grep 'DISTRIBUTED' /var/log/snort/alerts.txt | cut -d':' -f2 | sort | uniq -c"
```

## Configuración Avanzada

### Personalizar Ataques

Editar `group_vars/attackers.yml`:

```yaml
# Modificar intensidad del ataque
attack_duration: 600  # segundos
attack_rate: 1.0      # intentos/segundo

# Configurar evasión
evasion:
  min_delay: 10       # delay mínimo
  max_delay: 60       # delay máximo
  use_tor_proxy: true # usar proxy Tor
```

### Personalizar Detección

Editar `templates/distributed-attack.rules.j2`:

```snort
# Ajustar umbrales de detección
detection_filter:track by_dst, count 5, seconds 30
threshold:type both, track by_dst, count 10, seconds 60
```

## Análisis de Resultados

### Generar Reportes

```bash
# Reporte consolidado
./scripts/deploy-lab.sh --report

# Análisis específico
ansible monitors -i inventory/hosts -m fetch -a "src=/var/log/snort/alerts.txt dest=./analysis/"
```

### Métricas Clave

1. **Tasa de Detección**: Alertas generadas vs intentos realizados
2. **Tiempo de Detección**: Latencia entre ataque y alerta
3. **Falsos Positivos**: Alertas sin ataque real
4. **Correlación**: Detección de patrones distribuidos

## Consideraciones de Seguridad

### Uso Ético

⚠️ **IMPORTANTE**: Este laboratorio es para investigación defensiva únicamente:

- Usar solo en entornos controlados
- No apuntar a sistemas externos
- Respetar las políticas de seguridad
- Documentar todos los experimentos

### Aislamiento de Red

```bash
# Configurar red aislada
docker network create --driver bridge --subnet=192.168.100.0/24 lab-network
```

### Limpieza Post-Experimento

```bash
# Limpiar completamente
./scripts/deploy-lab.sh --clean

# Verificar limpieza
ansible all -i inventory/hosts -m shell -a "ps aux | grep attack"
```

## Troubleshooting

### Problemas Comunes

1. **Conectividad SSH**
   ```bash
   # Verificar claves
   ssh-keygen -R 192.168.100.10
   ssh-copy-id -i ~/.ssh/lab_key.pub user@192.168.100.10
   ```

2. **Permisos Ansible**
   ```bash
   # Verificar sudo
   ansible all -i inventory/hosts -m shell -a "whoami" --become
   ```

3. **Snort No Inicia**
   ```bash
   # Verificar configuración
   ansible monitors -i inventory/hosts -m shell -a "snort -T -c /etc/snort/snort.conf"
   ```

### Logs de Debug

```bash
# Ansible verbose
ansible-playbook -i inventory/hosts playbooks/setup-distributed-lab.yml -vvv

# Logs de coordinador
ansible attackers -i inventory/hosts -m shell -a "journalctl -u distributed-attack -f"
```

## Contribución

Para mejorar este laboratorio:

1. Fork el proyecto
2. Crear rama de feature
3. Documentar cambios
4. Probar en entorno aislado
5. Enviar pull request

## Licencia

Este proyecto es para uso académico y de investigación únicamente.

---
*Laboratorio de Investigación en Ciberseguridad Defensiva*