 FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar Snort y dependencias
RUN apt-get update && apt-get install -y \
    snort \
    tcpdump \
    net-tools \
    iputils-ping \
    curl \
    wget \
    nano \
    rsyslog \
    && rm -rf /var/lib/apt/lists/*

# Crear directorios necesarios
RUN mkdir -p /etc/snort/rules \
    && mkdir -p /var/log/snort \
    && mkdir -p /etc/snort/so_rules \
    && mkdir -p /etc/snort/preproc_rules

# Copiar archivos de configuración base de Snort
RUN snort -V || true

# Crear archivos de configuración básicos si no existen
RUN touch /etc/snort/classification.config
RUN touch /etc/snort/reference.config
RUN touch /etc/snort/threshold.config

# Configuración básica de classification.config
RUN echo 'config classification: not-suspicious,Not Suspicious Traffic,3' > /etc/snort/classification.config
RUN echo 'config classification: unknown,Unknown Traffic,3' >> /etc/snort/classification.config
RUN echo 'config classification: bad-unknown,Potentially Bad Traffic,2' >> /etc/snort/classification.config
RUN echo 'config classification: attempted-recon,Attempted Information Leak,2' >> /etc/snort/classification.config
RUN echo 'config classification: successful-recon-limited,Information Leak,2' >> /etc/snort/classification.config
RUN echo 'config classification: successful-recon-largescale,Large Scale Information Leak,2' >> /etc/snort/classification.config
RUN echo 'config classification: attempted-dos,Attempted Denial of Service,2' >> /etc/snort/classification.config
RUN echo 'config classification: successful-dos,Denial of Service,2' >> /etc/snort/classification.config
RUN echo 'config classification: attempted-user,Attempted User Privilege Gain,1' >> /etc/snort/classification.config
RUN echo 'config classification: unsuccessful-user,Unsuccessful User Privilege Gain,1' >> /etc/snort/classification.config
RUN echo 'config classification: successful-user,Successful User Privilege Gain,1' >> /etc/snort/classification.config
RUN echo 'config classification: attempted-admin,Attempted Administrator Privilege Gain,1' >> /etc/snort/classification.config
RUN echo 'config classification: successful-admin,Successful Administrator Privilege Gain,1' >> /etc/snort/classification.config
RUN echo 'config classification: rpc-portmap-decode,Decode of RPC Query,2' >> /etc/snort/classification.config
RUN echo 'config classification: shellcode-detect,Executable code was detected,1' >> /etc/snort/classification.config
RUN echo 'config classification: string-detect,A suspicious string was detected,3' >> /etc/snort/classification.config
RUN echo 'config classification: suspicious-filename-detect,A suspicious filename was detected,2' >> /etc/snort/classification.config
RUN echo 'config classification: suspicious-login,An attempted login using a suspicious username was detected,2' >> /etc/snort/classification.config
RUN echo 'config classification: system-call-detect,A system call was detected,2' >> /etc/snort/classification.config
RUN echo 'config classification: tcp-connection,A TCP connection was detected,4' >> /etc/snort/classification.config
RUN echo 'config classification: trojan-activity,A Network Trojan was detected,1' >> /etc/snort/classification.config
RUN echo 'config classification: unusual-client-port-connection,A client was using an unusual port,2' >> /etc/snort/classification.config
RUN echo 'config classification: network-scan,Detection of a Network Scan,3' >> /etc/snort/classification.config
RUN echo 'config classification: denial-of-service,Detection of a Denial of Service Attack,2' >> /etc/snort/classification.config
RUN echo 'config classification: non-standard-protocol,Detection of a non-standard protocol or event,2' >> /etc/snort/classification.config
RUN echo 'config classification: protocol-command-decode,Generic Protocol Command Decode,3' >> /etc/snort/classification.config
RUN echo 'config classification: web-application-activity,access to a potentially vulnerable web application,2' >> /etc/snort/classification.config
RUN echo 'config classification: web-application-attack,Web Application Attack,1' >> /etc/snort/classification.config

# Configuración básica de reference.config
RUN echo 'config reference: bugtraq   http://www.securityfocus.com/bid/' > /etc/snort/reference.config
RUN echo 'config reference: cve       http://cve.mitre.org/cgi-bin/cvename.cgi?name=' >> /etc/snort/reference.config
RUN echo 'config reference: arachNIDS http://www.whitehats.com/info/IDS' >> /etc/snort/reference.config

# Crear reglas básicas vacías para evitar errores
RUN touch /etc/snort/rules/local.rules
RUN touch /etc/snort/rules/ssh.rules
RUN touch /etc/snort/rules/ftp.rules
RUN mkdir -p /etc/snort/preproc_rules
RUN touch /etc/snort/preproc_rules/preprocessor.rules
RUN touch /etc/snort/preproc_rules/decoder.rules
RUN touch /etc/snort/preproc_rules/sensitive-data.rules

# Script de inicio de Snort
COPY start-snort.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-snort.sh

# Crear usuario snort
RUN groupadd snort || true && useradd -g snort -s /bin/false snort || true
RUN chown -R snort:snort /var/log/snort
RUN chown -R snort:snort /etc/snort

EXPOSE 514

CMD ["/usr/local/bin/start-snort.sh"]