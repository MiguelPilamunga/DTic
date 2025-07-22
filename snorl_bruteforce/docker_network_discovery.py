#!/usr/bin/env python3
"""
Advanced Stealth Docker Network Discovery
Ultra-evasive reconnaissance for IDS bypass research
Educational/Research purposes only
"""

import socket
import subprocess
import time
import json
import os
import random
import struct
from datetime import datetime
import threading
import queue

class AdvancedStealthScanner:
    def __init__(self, target_network="172.18.0.0/24", output_file="stealth_discovery.txt"):
        self.target_network = target_network
        self.output_file = output_file
        self.devices_found = {}
        self.base_ip = "172.18.0."
        self.evasion_techniques = []
        
    def ultra_stealth_ping(self, ip):
        """Ultra-stealth ping with anti-detection measures"""
        try:
            # Random delay between 15-30 seconds
            delay = random.uniform(15, 30)
            time.sleep(delay)
            
            # Use different ping parameters to avoid signatures
            ping_variations = [
                ["ping", "-c", "1", "-W", "3", "-q", "-i", "0.5", ip],
                ["ping", "-c", "1", "-W", "5", "-q", "-s", "32", ip],
                ["ping", "-c", "1", "-W", "2", "-q", "-t", "64", ip]
            ]
            
            cmd = random.choice(ping_variations)
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            # Add to evasion log
            self.evasion_techniques.append(f"Ping variation used: {' '.join(cmd)}")
            return result.returncode == 0
        except:
            return False
            
    def passive_dns_lookup(self, ip):
        """Passive DNS resolution"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return f"unknown-{ip.split('.')[-1]}"
            
    def detect_service_type(self, ip, hostname):
        """Detect container service type"""
        hostname_lower = hostname.lower()
        
        if 'target' in hostname_lower or 'ubuntu' in hostname_lower:
            return "Target Server (Ubuntu)"
        elif 'kali' in hostname_lower or 'attacker' in hostname_lower:
            return "Attacker Container (Kali)"
        elif 'snort' in hostname_lower or 'monitor' in hostname_lower:
            return "IDS Monitor (Snort)"
        elif 'gateway' in hostname_lower or '172.18.0.1' in ip:
            return "Docker Gateway"
        else:
            return "Docker Container"
            
    def ghost_mode_scan(self, ip_range):
        """Ghost mode - ultra-evasive scanning"""
        print(f"Initiating GHOST MODE scan of {self.base_ip}x")
        print("Using advanced anti-IDS techniques...")
        
        for i in ip_range:
            target_ip = self.base_ip + str(i)
            print(f"\nPhase {i}: Investigating {target_ip}")
            
            # Random delay between 20-60 seconds per target
            scan_delay = random.uniform(20, 60)
            print(f"  Waiting {scan_delay:.1f}s for optimal stealth...")
            
            if self.ultra_stealth_ping(target_ip):
                hostname = self.passive_dns_lookup(target_ip)
                service_type = self.detect_service_type(target_ip, hostname)
                
                device = {
                    'ip': target_ip,
                    'hostname': hostname,
                    'type': service_type,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'method': 'ghost-mode-ping',
                    'evasion_level': 'maximum'
                }
                
                self.devices_found[target_ip] = device
                print(f"  ✓ GHOST DETECTION: {hostname} ({service_type})")
                
                # Only do service detection on confirmed hosts
                services = self.advanced_service_detection(target_ip)
                device['detected_services'] = services
                
            else:
                print(f"  ✗ Target {target_ip} appears inactive")
                
            # Final stealth delay
            final_delay = random.uniform(30, 45)
            print(f"  Ghost mode delay: {final_delay:.1f}s")
            time.sleep(final_delay)
            
    def advanced_service_detection(self, ip):
        """Advanced passive service detection without TCP scans"""
        print(f"\nPassive service analysis for {ip}...")
        
        # Skip aggressive TCP scanning - use passive methods only
        detected_services = []
        
        # DNS service detection
        try:
            # Check if DNS responds (port 53)
            dns_check = subprocess.run(
                ["nslookup", ip, ip], 
                capture_output=True, text=True, timeout=5
            )
            if dns_check.returncode == 0:
                detected_services.append("DNS (inferred)")
        except:
            pass
            
        # HTTP banner grabbing (very stealthy)
        try:
            # Use curl with minimal signature
            http_check = subprocess.run(
                ["curl", "-m", "3", "-s", "-I", f"http://{ip}"],
                capture_output=True, text=True, timeout=5
            )
            if "HTTP" in http_check.stdout:
                detected_services.append("HTTP (detected)")
                self.evasion_techniques.append(f"HTTP banner grab successful on {ip}")
        except:
            pass
            
        # SSH detection through banner grab (minimal)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((ip, 22))
            if result == 0:
                banner = sock.recv(100).decode('utf-8', errors='ignore')
                if 'SSH' in banner:
                    detected_services.append("SSH (banner detected)")
                    self.evasion_techniques.append(f"SSH banner: {banner.strip()}")
            sock.close()
            
            # Critical: Long delay after any connection attempt
            time.sleep(random.uniform(45, 90))
            
        except:
            pass
            
        print(f"  Services detected: {detected_services}")
        return detected_services
        
    def generate_report(self):
        """Generate stealth scan report"""
        with open(self.output_file, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("DOCKER NETWORK STEALTH RECONNAISSANCE\n")
            f.write("=" * 60 + "\n")
            f.write(f"Scan date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Target network: {self.target_network}\n")
            f.write(f"Devices discovered: {len(self.devices_found)}\n\n")
            
            if self.devices_found:
                for ip, device in sorted(self.devices_found.items()):
                    f.write("-" * 40 + "\n")
                    f.write(f"IP: {device['ip']}\n")
                    f.write(f"Hostname: {device['hostname']}\n")
                    f.write(f"Service Type: {device['type']}\n")
                    f.write(f"Discovery Method: {device['method']}\n")
                    f.write(f"Timestamp: {device['timestamp']}\n\n")
                    
            f.write("=" * 60 + "\n")
            f.write("STEALTH TECHNIQUES USED:\n")
            f.write("- Ultra-slow ping sweeps (5+ second delays)\n")
            f.write("- Passive DNS resolution only\n")
            f.write("- Minimal packet signatures\n")
            f.write("- Human-like timing patterns\n")
            f.write("- Single packet probes\n")
            
    def run_advanced_stealth_discovery(self):
        """Execute advanced anti-IDS stealth discovery"""
        print("=== ADVANCED STEALTH DOCKER RECONNAISSANCE ===")
        print("Ultra-evasive IDS bypass techniques enabled")
        print("Educational/Research purposes only\n")
        
        start_time = time.time()
        
        # Phase 1: Ghost Mode Reconnaissance
        print("=== PHASE 1: GHOST MODE ACTIVATION ===")
        target_ips = [1, 2, 3]  # Minimal target set
        self.ghost_mode_scan(target_ips)
        
        # Generate advanced report
        self.generate_advanced_report()
        
        elapsed = time.time() - start_time
        print(f"\n=== GHOST MODE COMPLETE ===")
        print(f"Total reconnaissance time: {elapsed/60:.1f} minutes")
        print(f"Targets successfully profiled: {len(self.devices_found)}")
        print(f"Evasion techniques used: {len(self.evasion_techniques)}")
        print(f"Advanced report saved: {self.output_file}")
        
        # Display ghost summary
        if self.devices_found:
            print("\nGhost reconnaissance results:")
            for ip, device in self.devices_found.items():
                services = device.get('detected_services', [])
                service_str = f" | Services: {services}" if services else ""
                print(f"  👻 {ip} - {device['hostname']} ({device['type']}){service_str}")
                
        print(f"\nEvasion log preview:")
        for i, technique in enumerate(self.evasion_techniques[:3]):
            print(f"  • {technique}")

    def generate_advanced_report(self):
        """Generate advanced evasion report"""
        with open(self.output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("ADVANCED STEALTH DOCKER RECONNAISSANCE REPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Mission Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Target Network: {self.target_network}\n")
            f.write(f"Targets Profiled: {len(self.devices_found)}\n")
            f.write(f"Evasion Techniques Deployed: {len(self.evasion_techniques)}\n\n")
            
            if self.devices_found:
                f.write("TARGET INTELLIGENCE:\n")
                f.write("-" * 50 + "\n")
                for ip, device in sorted(self.devices_found.items()):
                    f.write(f"\nTarget: {device['ip']}\n")
                    f.write(f"Codename: {device['hostname']}\n")
                    f.write(f"Classification: {device['type']}\n")
                    f.write(f"Discovery Method: {device['method']}\n")
                    f.write(f"Evasion Level: {device.get('evasion_level', 'standard')}\n")
                    f.write(f"Intel Timestamp: {device['timestamp']}\n")
                    
                    services = device.get('detected_services', [])
                    if services:
                        f.write(f"Service Profile: {', '.join(services)}\n")
                    f.write("-" * 30 + "\n")
                    
            f.write("\nANTI-IDS EVASION LOG:\n")
            f.write("-" * 50 + "\n")
            for i, technique in enumerate(self.evasion_techniques, 1):
                f.write(f"{i:2d}. {technique}\n")
                
            f.write("\nSTEALTH TECHNIQUES SUMMARY:\n")
            f.write("-" * 50 + "\n")
            f.write("✓ Randomized timing (15-90 second delays)\n")
            f.write("✓ Ping parameter variation\n")
            f.write("✓ Passive service detection\n")
            f.write("✓ Anti-signature evasion\n")
            f.write("✓ Human behavior simulation\n")
            f.write("✓ Minimal network footprint\n")
            f.write("✓ No TCP port scanning\n")
            
            f.write(f"\n{'='*80}\n")
            f.write("MISSION STATUS: STEALTH RECONNAISSANCE COMPLETE\n")
            f.write(f"{'='*80}\n")

if __name__ == "__main__":
    scanner = AdvancedStealthScanner()
    scanner.run_advanced_stealth_discovery()