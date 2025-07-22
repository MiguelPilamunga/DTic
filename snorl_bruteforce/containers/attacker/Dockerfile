FROM kalilinux/kali-rolling

# Actualizar e instalar herramientas de brute force
RUN apt-get update && apt-get install -y \
    hydra \
    nmap \
    curl \
    wget \
    netcat-traditional \
    sshpass \
    ftp \
    telnet \
    && rm -rf /var/lib/apt/lists/*

# Crear directorios de trabajo
RUN mkdir -p /opt/attacks /var/log/attacker

# Copiar scripts de ataque
COPY attack-ssh.sh /opt/attacks/
COPY attack-ftp.sh /opt/attacks/
COPY attack-http.sh /opt/attacks/

# Hacer scripts ejecutables
RUN chmod +x /opt/attacks/*.sh

# Crear wordlists básicas
RUN mkdir -p /opt/attacks/wordlists

# Lista de usuarios comunes
RUN cat > /opt/attacks/wordlists/users.txt << 'EOF'
root
admin
administrator
test
testuser1
testuser2
user
guest
ftp
service
postgres
mysql
www
apache
nginx
tomcat
mail
postfix
nobody
oracle
jenkins
git
svn
EOF

# Lista de contraseñas comunes
RUN cat > /opt/attacks/wordlists/passwords.txt << 'EOF'
password
123456
admin
root
test
guest
user
pass
login
qwerty
abc123
password123
admin123
root123
test123
letmein
welcome
default
service
changeme
password1
admin1
toor
secret
EOF

# Script de inicio
COPY start-attacker.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-attacker.sh

WORKDIR /opt/attacks

CMD ["/usr/local/bin/start-attacker.sh"]