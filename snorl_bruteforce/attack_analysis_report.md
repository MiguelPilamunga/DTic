# Reporte de Análisis de Ataques - Laboratorio Snort

## Resumen Ejecutivo
Análisis completo de diferentes tipos de ataques ejecutados contra el laboratorio de Snort para evaluar capacidades de detección y monitoreo.

---

## 🎯 Infraestructura de Pruebas

### Componentes del Laboratorio
- **Target Ubuntu**: 172.18.0.2 (Servidor vulnerable)
- **Kali Attacker**: 172.18.0.3 (Plataforma de ataque)
- **Snort IDS**: Host network (Monitor de seguridad)

### Servicios Expuestos en Target
- **SSH**: Puerto 22 (OpenSSH 8.9p1)
- **FTP**: Puerto 21 (vsftpd 2.0.8)
- **HTTP**: Puerto 80 (Apache 2.4.52)

---

## 🔍 Pruebas de Ataque Realizadas

### 1. Test de Conectividad (ICMP)
**Comando Ejecutado:**
```bash
ping -c 5 target-ubuntu
```

**Resultados:**
- ✅ **Conectividad exitosa**: 5 packets transmitidos, 5 recibidos
- ✅ **Latencia**: 0.037-0.110ms (muy baja, típico de contenedores)
- ✅ **Sin pérdida de paquetes**: 0% packet loss

**Análisis de Seguridad:**
- Permite verificar que el target está accesible
- ICMP puede ser usado para reconnaissance
- Snort debería detectar patrones de ping flood

---

### 2. Escaneo de Puertos (Nmap SYN Scan)
**Comando Ejecutado:**
```bash
nmap -sS target-ubuntu
```

**Resultados Detectados:**
```
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh  
80/tcp open  http
```

**Análisis de Seguridad:**
- ⚠️ **Fingerprinting exitoso**: Identificó servicios exactos
- ⚠️ **Surface de ataque expuesta**: 3 servicios vulnerables
- 🔴 **Indicador de reconocimiento**: Patrón típico de pre-ataque

**Tiempo de Ejecución:** 0.12 segundos (muy rápido)

---

### 3. Escaneo Agresivo (Nmap Aggressive)
**Comando Ejecutado:**
```bash
nmap -A -T4 target-ubuntu
```

**Información Recopilada:**
- **Sistema Operativo**: Ubuntu Linux (kernel 4.15-5.19)
- **Servicios Detallados**:
  - SSH: OpenSSH 8.9p1 Ubuntu 3ubuntu0.13
  - FTP: vsftpd 2.0.8 (con error de configuración)
  - HTTP: Apache httpd 2.4.52
- **Host Keys SSH**: ECDSA y ED25519 identificadas
- **Headers HTTP**: Apache/2.4.52 (Ubuntu)

**Análisis de Seguridad:**
- 🔴 **Información crítica expuesta**: Versiones exactas de software
- 🔴 **Vulnerabilidades identificables**: Versiones específicas permiten buscar CVEs
- 🔴 **Error FTP detectado**: "OOPS: vsftpd: refusing to run with writable root"
- ⚠️ **Fingerprinting completo**: Suficiente información para ataques dirigidos

**Tiempo de Ejecución:** 12.73 segundos

---

### 4. Ataque de Fuerza Bruta SSH
**Comando Ejecutado:**
```bash
hydra -L /tmp/users.txt -P /tmp/pass.txt ssh://target-ubuntu:22 -t 8 -V
```

**Credenciales Probadas:**
- **Usuarios**: admin, root, test, guest  
- **Contraseñas**: admin, password, 123456, test, toor
- **Total de intentos**: 20 combinaciones
- **Threads concurrentes**: 8

**Resultados del Ataque:**
- ✅ **Credenciales encontradas**:
  - `admin:admin` ✅
  - `root:toor` ✅
- **Tiempo de ejecución**: < 1 segundo
- **Éxito del ataque**: 100% (credenciales débiles)

**Análisis de Seguridad:**
- 🔴 **Falla crítica de seguridad**: Contraseñas por defecto
- 🔴 **Root access comprometido**: Acceso total al sistema
- 🔴 **Sin protección anti-brute force**: Sin rate limiting
- 🔴 **Múltiples cuentas vulnerables**: Varias entradas de ataque

---

## 📊 Patrones de Ataque Detectados por Snort

### Evidencia de Logs Anteriores (archivo snort.log.1752616559):

**Estadísticas de Fuerza Bruta SSH:**
- **26 puertos de origen diferentes** desde 172.18.0.3
- **626 paquetes capturados** durante el ataque
- **Conexiones simultáneas múltiples** hacia puerto 22
- **Patrón temporal concentrado** (todos en segundos)

**Protocolos Identificados:**
```
SSH-2.0-libssh_0.11.2    (Hydra - Herramienta de ataque)
SSH-2.0-OpenSSH_8.9p1   (Target Ubuntu)
```

**Puertos de Origen Utilizados en Ataque:**
```
54050, 54056, 54064, 54072, 54084, 54088, 54104, 54112,
54122, 54412, 54424, 54426, 54442, 54444, 54462, 54464,
54492, 54506, 54508, 54522, 54526, 54534, 54544, 54546,
54562, 54570
```

---

## 🚨 Indicadores de Compromiso (IOCs)

### 1. Patrones de Red Sospechosos
- ✅ **Múltiples conexiones SSH simultáneas**
- ✅ **Diferentes puertos de origen desde una IP**
- ✅ **Volumen alto de tráfico SSH en poco tiempo**
- ✅ **Conexiones rápidas y fallidas (automatizadas)**

### 2. Comportamiento de Ataque
- ✅ **Escaneo de puertos previo al ataque**
- ✅ **Fingerprinting de servicios**
- ✅ **Ataques de fuerza bruta automatizados**
- ✅ **Múltiples threads concurrentes**

### 3. Vectores de Compromiso
- 🔴 **Credenciales débiles** (admin:admin, root:toor)
- 🔴 **Sin protecciones anti-brute force**
- 🔴 **Servicios con configuraciones inseguras**
- 🔴 **Información excesiva expuesta en servicios**

---

## 📈 Efectividad de Snort

### Capacidades Verificadas ✅
- **Captura de tráfico en tiempo real**
- **Identificación de protocolos SSH**
- **Registro detallado de conexiones**
- **Detección de patrones anómalos**
- **Logging para análisis forense**

### Limitaciones Identificadas ⚠️
- **Sin alertas automáticas configuradas**
- **Falta de reglas específicas para brute force**
- **No hay bloqueo automático de IPs**
- **Configuración básica sin optimizar**

---

## 🔧 Recomendaciones de Seguridad

### Para el Target:
1. **Implementar políticas de contraseñas fuertes**
2. **Configurar fail2ban para SSH**
3. **Deshabilitar root login remoto**
4. **Implementar autenticación por clave pública**
5. **Ocultar versiones de servicios en headers**

### Para Snort:
1. **Configurar reglas específicas de brute force**
2. **Implementar alertas en tiempo real**
3. **Configurar thresholds para detección**
4. **Integrar con sistemas de respuesta automática**
5. **Optimizar reglas para reducir falsos positivos**

### Para la Red:
1. **Implementar VPN para acceso administrativo**
2. **Configurar rate limiting en servicios**
3. **Monitoreo 24/7 de logs de seguridad**
4. **Implementar honeypots para detección temprana**

---

## 📝 Conclusiones

El laboratorio demostró exitosamente:

1. **Vulnerabilidades críticas** en configuraciones por defecto
2. **Efectividad de herramientas de ataque** automatizadas (Hydra, Nmap)
3. **Capacidades de monitoreo** de Snort para captura de tráfico
4. **Necesidad de configuraciones avanzadas** para detección proactiva
5. **Importancia del análisis forense** post-ataque

**El entorno es ideal para:**
- Investigación académica en seguridad
- Entrenamiento en análisis forense
- Desarrollo de reglas de detección
- Pruebas de herramientas de seguridad

---

*Reporte generado para fines académicos y de investigación en ciberseguridad*