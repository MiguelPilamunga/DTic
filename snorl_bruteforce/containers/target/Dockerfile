FROM ubuntu:22.04

# Evitar prompts durante instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instalar servicios vulnerables
RUN apt-get update && apt-get install -y \
    openssh-server \
    vsftpd \
    apache2 \
    telnetd \
    xinetd \
    curl \
    wget \
    nano \
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Configurar SSH vulnerable
RUN mkdir /var/run/sshd
COPY sshd_config_vulnerable /etc/ssh/sshd_config
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Crear usuarios vulnerables
RUN useradd -m -s /bin/bash testuser1 && echo 'testuser1:password' | chpasswd
RUN useradd -m -s /bin/bash testuser2 && echo 'testuser2:123456' | chpasswd
RUN useradd -m -s /bin/bash admin && echo 'admin:admin' | chpasswd
RUN useradd -m -s /bin/bash guest && echo 'guest:guest' | chpasswd
RUN echo 'root:toor' | chpasswd

# Configurar FTP vulnerable
COPY vsftpd_vulnerable.conf /etc/vsftpd.conf
RUN mkdir -p /var/ftp/pub
RUN chmod 755 /var/ftp
RUN chmod 777 /var/ftp/pub
RUN useradd -d /var/ftp -s /bin/false ftp || true
RUN chown ftp:ftp /var/ftp

# Configurar Apache con autenticación básica
RUN a2enmod auth_basic
RUN a2enmod authn_file
RUN a2enmod authz_user
COPY apache-auth.conf /etc/apache2/sites-available/auth.conf
RUN a2ensite auth.conf
RUN htpasswd -cb /etc/apache2/.htpasswd admin admin
RUN htpasswd -b /etc/apache2/.htpasswd test password

# Crear directorios de logs
RUN mkdir -p /var/log/target

# Script de inicio
COPY start-services.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-services.sh

# Banner SSH
RUN echo "*** RESEARCH LAB - AUTHORIZED ACCESS ONLY ***" > /etc/ssh/banner

# Exponer puertos
EXPOSE 22 21 80 23

# Comando de inicio
CMD ["/usr/local/bin/start-services.sh"]