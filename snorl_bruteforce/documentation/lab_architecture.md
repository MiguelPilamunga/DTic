# Laboratorio de Investigación: Análisis de Snort ante Ataques de Fuerza Bruta

## Arquitectura del Laboratorio (Implementada)

### Visión General
Laboratorio académico implementado con contenedores Docker para analizar el comportamiento del sistema de detección de intrusos Snort ante ataques de fuerza bruta SSH.

### Componentes Implementados

#### 1. Target Ubuntu Container
**Propósito**: Servidor vulnerable con servicios SSH expuestos
- **Imagen Base**: Ubuntu 22.04
- **Container**: target-ubuntu
- **Red**: lab-network (Docker bridge)
- **Puertos Expuestos**:
  - 2222:22 (SSH)
  - 2121:21 (FTP)
  - 8080:80 (HTTP)

**Usuarios Vulnerables Configurados**:
- admin:admin
- test:password  
- guest:guest
- root:toor

**Configuración SSH**:
- PermitRootLogin yes
- PasswordAuthentication yes
- Sin restricciones de fuerza bruta

#### 2. Snort IDS Container
**Propósito**: Sistema de monitoreo y captura de tráfico
- **Imagen Base**: Ubuntu 22.04 + Snort 2.9.15.1
- **Container**: snort-monitor
- **Modo**: Host networking (acceso completo a interfaces)
- **Interfaz Monitoreada**: br-e4a61fe26bee (Docker bridge)
- **Logs**: /var/log/snort/

**Capacidades**:
- Captura de paquetes en tiempo real
- Análisis de tráfico SSH
- Detección de patrones de conexión
- Logging de actividad maliciosa

#### 3. Kali Attacker Container  
**Propósito**: Plataforma de ataque automatizado
- **Imagen Base**: Kali Linux Rolling
- **Container**: kali-attacker
- **Red**: lab-network
- **Herramientas Instaladas**:
  - Hydra (ataques SSH)
  - Nmap (reconocimiento)
  - Herramientas de red básicas

**Ataques Implementados**:
- SSH brute force con wordlists
- Múltiples conexiones simultáneas
- Ataques con diferentes velocidades

## Topología de Red Implementada

```
Docker Host (192.168.0.105)
│
├── Docker Bridge (br-e4a61fe26bee) 172.18.0.0/16
    │
    ├── target-ubuntu (172.18.0.2)
    │   ├── SSH:22 → Host:2222
    │   ├── FTP:21 → Host:2121  
    │   └── HTTP:80 → Host:8080
    │
    ├── kali-attacker (172.18.0.3)
    │   └── Hydra SSH attacks → target-ubuntu:22
    │
    └── snort-monitor (Host network)
        └── Monitoring: br-e4a61fe26bee
            └── Captures: All traffic between containers
```

## Resultados de Implementación y Pruebas

### 1. Ataques SSH Exitosos Ejecutados
- **Hydra con múltiples credenciales**: 16 intentos (4 usuarios x 4 contraseñas)
- **Conexiones simultáneas**: Hasta 8 threads concurrentes
- **Credenciales encontradas**: admin:admin, root:toor
- **Tiempo de ataque**: < 1 segundo para encontrar credenciales

### 2. Patrones de Ataque Detectados por Snort
- **626 paquetes capturados** en archivo snort.log
- **Múltiples puertos de origen**: 54050, 54056, 54064, 54072, 54084...
- **Conexiones SSH simultaneas** desde 172.18.0.3 → 172.18.0.2:22
- **Patrón temporal**: Todas las conexiones en el mismo segundo
- **Protocolos identificados**: SSH-2.0-libssh_0.11.2 (Hydra) vs SSH-2.0-OpenSSH_8.9p1

### 3. Indicadores de Fuerza Bruta Identificados
✅ **Múltiples conexiones desde una IP**  
✅ **Diferentes puertos de origen simultáneos**  
✅ **Conexiones SSH rápidas y fallidas**  
✅ **Patrón de conexión no humano (automatizado)**  
✅ **Volumen alto de tráfico SSH en corto tiempo**

### 4. Capacidades de Monitoreo Verificadas
- **Snort captura tráfico**: ✅ Funcional
- **Análisis de protocolos**: ✅ SSH identificado correctamente
- **Logging detallado**: ✅ Todos los paquetes registrados
- **Detección en tiempo real**: ✅ Captura durante el ataque
- **Análisis forense**: ✅ Logs disponibles para análisis post-ataque

## Configuraciones de Snort

### Reglas Principales
- Detección de múltiples intentos de login fallidos
- Identificación de patrones de fuerza bruta
- Alertas por volumen de conexiones
- Detección de herramientas automatizadas

### Configuración de Red
```
var HOME_NET 192.168.1.0/24
var EXTERNAL_NET !$HOME_NET
var SSH_SERVERS $HOME_NET
var FTP_SERVERS $HOME_NET
```

## Procedimiento de Pruebas

### Fase 1: Preparación
1. Configurar los tres servidores
2. Instalar y configurar Snort
3. Verificar conectividad
4. Establecer baseline de tráfico normal

### Fase 2: Ejecución
1. Iniciar monitoreo en Snort
2. Ejecutar ataques desde Kali
3. Documentar respuestas del IDS/IPS
4. Recopilar logs y alertas

### Fase 3: Análisis
1. Revisar efectividad de detección
2. Analizar tiempos de respuesta
3. Evaluar calidad de alertas
4. Documentar hallazgos

## Consideraciones de Seguridad

⚠️ **ADVERTENCIA**: Esta infraestructura está diseñada exclusivamente para investigación académica controlada.

- Aislar la red de laboratorio de redes de producción
- Usar únicamente en ambiente controlado
- No exponer servicios vulnerables a Internet
- Documentar y justificar el uso académico
- Cumplir con políticas institucionales de seguridad

## Herramientas de Análisis

### Monitoreo en Tiempo Real
- Snort console
- Wireshark para análisis de paquetes
- Tail de logs en tiempo real

### Análisis Post-Ataque
- Herramientas de correlación de logs
- Scripts de análisis estadístico
- Generación de reportes automatizados

## Resultados Esperados

### Documentación
- Efectividad de reglas Snort contra diferentes tipos de fuerza bruta
- Comparación de técnicas de detección
- Recomendaciones para mejora de configuraciones
- Análisis de rendimiento bajo carga de ataques

### Publicación Académica
- Paper de investigación sobre efectividad de IDS
- Documentación de metodología de pruebas
- Benchmarks de rendimiento
- Contribuciones a la comunidad de seguridad

---
*Documento creado para fines de investigación académica en ciberseguridad*