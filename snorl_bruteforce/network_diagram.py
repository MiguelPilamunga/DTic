#!/usr/bin/env python3
"""
Network Diagram Generator for Snort Brute Force Lab
Generates ASCII diagram of the lab architecture
"""

def generate_network_diagram():
    diagram = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        SNORT BRUTE FORCE LAB ARCHITECTURE                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Docker Host: 192.168.0.105                                                 ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │  Docker Bridge Network (br-e4a61fe26bee): 172.18.0.0/16              │ ║
║  │                                                                        │ ║
║  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    │ ║
║  │  │  🎯 TARGET      │    │  ⚔️  ATTACKER   │    │  🛡️  SNORT IDS  │    │ ║
║  │  │  Ubuntu 22.04   │    │  Kali Linux     │    │  Ubuntu 22.04   │    │ ║
║  │  │  172.18.0.2     │    │  172.18.0.3     │    │  Host Network   │    │ ║
║  │  │  target-ubuntu  │    │  kali-attacker  │    │  snort-monitor  │    │ ║
║  │  │                 │    │                 │    │                 │    │ ║
║  │  │  Services:      │    │  Tools:         │    │  Monitoring:    │    │ ║
║  │  │  • SSH:22       │◄───┤  • Hydra        │    │  • Interface:   │    │ ║
║  │  │  • FTP:21       │    │  • Nmap         │    │    br-e4a61fe26bee │ ║
║  │  │  • HTTP:80      │    │  • SSH clients  │    │  • Packet       │    │ ║
║  │  │                 │    │                 │    │    Capture      │    │ ║
║  │  │  Users:         │    │  Attack Types:  │    │  • Traffic      │    │ ║
║  │  │  • admin:admin  │    │  • SSH Brute    │    │    Analysis     │    │ ║
║  │  │  • root:toor    │    │    Force        │    │  • Logging      │    │ ║
║  │  │  • test:password│    │  • Multiple     │    │                 │    │ ║
║  │  │  • guest:guest  │    │    Connections  │    │                 │    │ ║
║  │  └─────────────────┘    └─────────────────┘    └─────────────────┘    │ ║
║  │                                                                        │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  Port Mapping to Host:                                                       ║
║  ┌──────────────────┐                                                       ║
║  │  Host:2222 → SSH:22                                                      ║
║  │  Host:2121 → FTP:21                                                      ║
║  │  Host:8080 → HTTP:80                                                     ║
║  └──────────────────┘                                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

ATTACK FLOW DETECTED:
═══════════════════════

1. Kali Attacker (172.18.0.3) → Target Ubuntu (172.18.0.2:22)
   ├── Multiple SSH connections using different source ports
   ├── Ports used: 54050, 54056, 54064, 54072, 54084...
   ├── 626 packets captured in attack session
   └── Credentials found: admin:admin, root:toor

2. Snort IDS Detection:
   ├── Monitoring Docker bridge interface
   ├── Captures all inter-container traffic  
   ├── Logs saved to: /var/log/snort/snort.log.1752616559
   └── Identifies SSH protocol and connection patterns

INDICATORS OF BRUTE FORCE ATTACK:
═════════════════════════════════

✅ Multiple simultaneous connections from single IP
✅ Different source ports in rapid succession  
✅ SSH protocol handshakes (SSH-2.0-libssh_0.11.2)
✅ Rapid connection establishment and termination
✅ Automated connection pattern (non-human timing)
✅ High volume of SSH traffic in short timeframe

COMMANDS TO REPRODUCE:
═════════════════════

1. Start Lab:     docker-compose up -d
2. SSH Attack:    docker exec kali-attacker hydra -L users.txt -P pass.txt ssh://target-ubuntu:22
3. View Capture:  docker exec snort-monitor tcpdump -r /var/log/snort/snort.log.*
4. Stop Lab:      docker-compose down
"""
    return diagram

if __name__ == "__main__":
    print(generate_network_diagram())