#!/usr/bin/env python3
"""
LLM-Generated Password Pattern Detector & Generator
Educational/Research purposes only

Based on Ecuadorian dataset analysis:
- 47% usan Nombre + Fecha de nacimiento
- 67% incluyen información personal
- 78% vulnerables a ataques de diccionario
- 89% tienen contexto cultural ecuatoriano
- 31% usan fechas entre 1980-2010
- 54% terminan en símbolos (@, *, #)
- 23% incluyen secuencias numéricas
"""

import random
import re
import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import hashlib

class PasswordPattern(Enum):
    NAME_BIRTHDATE = "name_birthdate"
    PERSONAL_INFO = "personal_info" 
    CULTURAL_CONTEXT = "cultural_context"
    SUBSTITUTION_BASIC = "substitution_basic"
    SYMBOL_SUFFIX = "symbol_suffix"
    NUMERIC_SEQUENCE = "numeric_sequence"
    INSTITUTION_REF = "institution_ref"

@dataclass
class EcuadorianProfile:
    """Profile based on Ecuadorian cultural patterns"""
    name: str = ""
    birth_year: int = 0
    institution: str = ""
    interests: List[str] = None
    family_names: List[str] = None
    
    def __post_init__(self):
        if self.interests is None:
            self.interests = []
        if self.family_names is None:
            self.family_names = []

class LLMPasswordAnalyzer:
    """Analyze and generate passwords using LLM-identified patterns"""
    
    def __init__(self):
        # Ecuadorian cultural context data
        self.ecuadorian_names = [
            "Jose", "David", "Mariana", "Carlos", "Ana", "Luis", "Sofia", "Miguel",
            "Carmen", "Diego", "Alejandra", "Fernando", "Gabriela", "Ricardo", 
            "Patricia", "Andres", "Elena", "Roberto", "Daniela", "Eduardo"
        ]
        
        self.ecuadorian_institutions = [
            "PUCE", "UCE", "USFQ", "EPN", "UTN", "UTPL", "UTE", "UDLA",
            "ESPOL", "ESPE", "UPS", "UIDE", "UEA", "UNAE"
        ]
        
        self.cultural_references = [
            "peluchin", "halamadrid", "Batman", "Ecuador", "Quito", "Guayaquil",
            "Cuenca", "Barcelona", "Real", "Futbol", "Seleccion", "Tricolor",
            "Condor", "Andes", "Costa", "Sierra", "Oriente", "Galapagos"
        ]
        
        self.common_substitutions = {
            'a': '@', 'A': '@',
            'o': '0', 'O': '0',
            'e': '3', 'E': '3',
            'i': '1', 'I': '1',
            's': '$', 'S': '$',
            't': '7', 'T': '7'
        }
        
        self.symbol_suffixes = ['@', '*', '#', '!', '$', '%', '&', '+', '=']
        
        # Birth year ranges (31% use 1980-2010)
        self.common_birth_years = list(range(1980, 2011))
        self.extended_birth_years = list(range(1970, 2005))
        
        # Pattern statistics from dataset
        self.pattern_probabilities = {
            PasswordPattern.NAME_BIRTHDATE: 0.47,
            PasswordPattern.PERSONAL_INFO: 0.67,
            PasswordPattern.CULTURAL_CONTEXT: 0.89,
            PasswordPattern.SUBSTITUTION_BASIC: 0.45,
            PasswordPattern.SYMBOL_SUFFIX: 0.54,
            PasswordPattern.NUMERIC_SEQUENCE: 0.23,
            PasswordPattern.INSTITUTION_REF: 0.35
        }
        
        self.generated_passwords = set()
        self.pattern_usage = {pattern: 0 for pattern in PasswordPattern}
        
    def generate_name_birthdate_pattern(self, profile: EcuadorianProfile) -> List[str]:
        """Generate Name + Birthdate patterns (47% of dataset)"""
        passwords = []
        name = profile.name.lower() if profile.name else random.choice(self.ecuadorian_names).lower()
        
        # Birth year variations
        birth_years = [profile.birth_year] if profile.birth_year else random.sample(self.common_birth_years, 3)
        
        for year in birth_years:
            # Standard combinations
            passwords.extend([
                f"{name}{year}",
                f"{name}{str(year)[2:]}",  # Last 2 digits
                f"{year}{name}",
                f"{name}_{year}",
                f"{name}.{year}",
                f"{name}{year}@",
                f"{name}{year}*",
                f"{name}{year}#"
            ])
            
            # With month/day if available
            for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                for day in [1, 5, 10, 15, 20, 25]:
                    if random.random() < 0.1:  # 10% probability
                        passwords.append(f"{name}{day:02d}{month:02d}{year}")
                        passwords.append(f"{name}{month:02d}{year}")
                        
        self.pattern_usage[PasswordPattern.NAME_BIRTHDATE] += len(passwords)
        return passwords
        
    def generate_personal_info_pattern(self, profile: EcuadorianProfile) -> List[str]:
        """Generate personal information patterns (67% of dataset)"""
        passwords = []
        
        # Family names
        if profile.family_names:
            for family_name in profile.family_names:
                passwords.extend([
                    family_name.lower(),
                    f"{profile.name.lower()}{family_name.lower()}",
                    f"{family_name.lower()}{profile.birth_year}" if profile.birth_year else f"{family_name.lower()}123"
                ])
                
        # Interests/hobbies
        if profile.interests:
            for interest in profile.interests:
                passwords.extend([
                    interest.lower(),
                    f"{interest.lower()}123",
                    f"{profile.name.lower()}{interest.lower()}",
                    f"{interest.lower()}{profile.birth_year}" if profile.birth_year else f"{interest.lower()}2024"
                ])
                
        # Pet names simulation
        pet_names = ["Max", "Bella", "Luna", "Rocky", "Princess", "Buddy"]
        for pet in random.sample(pet_names, 2):
            passwords.extend([
                pet.lower(),
                f"{pet.lower()}123",
                f"{profile.name.lower()}{pet.lower()}"
            ])
            
        self.pattern_usage[PasswordPattern.PERSONAL_INFO] += len(passwords)
        return passwords
        
    def generate_cultural_context_pattern(self, profile: EcuadorianProfile) -> List[str]:
        """Generate Ecuadorian cultural context patterns (89% of dataset)"""
        passwords = []
        name = profile.name.lower() if profile.name else random.choice(self.ecuadorian_names).lower()
        
        # Institution references
        if profile.institution:
            institution = profile.institution.upper()
            passwords.extend([
                f"{name}{institution}",
                f"{institution}{profile.birth_year}" if profile.birth_year else f"{institution}2024",
                f"{institution.lower()}123",
                f"{name}{institution.lower()}"
            ])
        else:
            # Random institutions
            for inst in random.sample(self.ecuadorian_institutions, 3):
                passwords.extend([
                    f"{name}{inst.lower()}",
                    f"{inst.lower()}123",
                    f"{inst.lower()}{random.randint(1980, 2010)}"
                ])
                
        # Cultural references
        for ref in random.sample(self.cultural_references, 5):
            passwords.extend([
                f"{name}{ref.lower()}",
                f"{ref.lower()}123",
                f"{ref.lower()}{profile.birth_year}" if profile.birth_year else f"{ref.lower()}2024",
                ref.lower()
            ])
            
        # Football teams (very common in Ecuador)
        football_teams = ["barcelona", "emelec", "liga", "independiente", "nacionalquito"]
        for team in random.sample(football_teams, 2):
            passwords.extend([
                f"{name}{team}",
                f"{team}123",
                f"{team}{profile.birth_year}" if profile.birth_year else f"{team}2024"
            ])
            
        self.pattern_usage[PasswordPattern.CULTURAL_CONTEXT] += len(passwords)
        return passwords
        
    def apply_basic_substitutions(self, password: str) -> List[str]:
        """Apply basic character substitutions (45% of users)"""
        variations = [password]
        
        # Apply single substitutions
        for char, sub in self.common_substitutions.items():
            if char in password:
                new_password = password.replace(char, sub)
                variations.append(new_password)
                
        # Apply multiple substitutions
        multi_sub = password
        for char, sub in self.common_substitutions.items():
            multi_sub = multi_sub.replace(char, sub)
        if multi_sub != password:
            variations.append(multi_sub)
            
        # Selective substitutions (common patterns)
        if 'a' in password:
            variations.append(password.replace('a', '@', 1))  # Replace only first occurrence
        if 'o' in password:
            variations.append(password.replace('o', '0', 1))
        if 'e' in password:
            variations.append(password.replace('e', '3', 1))
            
        self.pattern_usage[PasswordPattern.SUBSTITUTION_BASIC] += len(variations) - 1
        return variations
        
    def add_symbol_suffixes(self, passwords: List[str]) -> List[str]:
        """Add symbol suffixes (54% of dataset)"""
        enhanced = []
        
        for password in passwords:
            enhanced.append(password)  # Original
            
            # Single symbols
            for symbol in random.sample(self.symbol_suffixes, 4):
                enhanced.append(f"{password}{symbol}")
                
            # Double symbols
            if random.random() < 0.2:  # 20% get double symbols
                symbol1, symbol2 = random.sample(self.symbol_suffixes, 2)
                enhanced.append(f"{password}{symbol1}{symbol2}")
                
            # Number + symbol combinations
            for num in [1, 12, 123, random.randint(10, 99)]:
                symbol = random.choice(self.symbol_suffixes)
                enhanced.append(f"{password}{num}{symbol}")
                enhanced.append(f"{password}{symbol}{num}")
                
        suffix_added = len(enhanced) - len(passwords)
        self.pattern_usage[PasswordPattern.SYMBOL_SUFFIX] += suffix_added
        return enhanced
        
    def add_numeric_sequences(self, passwords: List[str]) -> List[str]:
        """Add numeric sequences (23% of dataset)"""
        enhanced = []
        
        numeric_sequences = [
            "123", "321", "111", "000", "456", "789", "012",
            "1234", "4321", "1111", "0000", "2024", "2025"
        ]
        
        for password in passwords:
            enhanced.append(password)  # Original
            
            if random.random() < 0.23:  # 23% probability
                sequence = random.choice(numeric_sequences)
                enhanced.extend([
                    f"{password}{sequence}",
                    f"{sequence}{password}",
                    f"{password}_{sequence}"
                ])
                
        sequences_added = len(enhanced) - len(passwords)
        self.pattern_usage[PasswordPattern.NUMERIC_SEQUENCE] += sequences_added
        return enhanced
        
    def generate_contextual_passwords(self, profile: EcuadorianProfile, count: int = 100) -> List[str]:
        """Generate contextual passwords based on Ecuadorian patterns"""
        all_passwords = set()
        
        # Generate base patterns
        name_birth_passwords = self.generate_name_birthdate_pattern(profile)
        personal_passwords = self.generate_personal_info_pattern(profile)
        cultural_passwords = self.generate_cultural_context_pattern(profile)
        
        base_passwords = name_birth_passwords + personal_passwords + cultural_passwords
        
        # Apply transformations
        enhanced_passwords = []
        for password in base_passwords:
            if password and len(password) >= 4:  # Minimum length
                # Apply substitutions
                substituted = self.apply_basic_substitutions(password)
                enhanced_passwords.extend(substituted)
                
        # Add symbols and sequences
        with_symbols = self.add_symbol_suffixes(enhanced_passwords)
        with_sequences = self.add_numeric_sequences(with_symbols)
        
        # Remove duplicates and filter by realistic length
        unique_passwords = list(set(with_sequences))
        filtered_passwords = [p for p in unique_passwords if 6 <= len(p) <= 20]
        
        # Sort by likelihood (shorter, more common patterns first)
        filtered_passwords.sort(key=lambda x: (len(x), x.count('1'), x.count('@')))
        
        return filtered_passwords[:count]
        
    def analyze_password_strength(self, password: str) -> Dict:
        """Analyze password strength and patterns"""
        analysis = {
            'length': len(password),
            'patterns_detected': [],
            'vulnerability_score': 0,
            'cultural_indicators': [],
            'substitution_patterns': []
        }
        
        # Pattern detection
        if re.search(r'[a-zA-Z]+\d{4}', password):
            analysis['patterns_detected'].append('name_year')
        if re.search(r'[a-zA-Z]+\d{2,4}[@*#]', password):
            analysis['patterns_detected'].append('name_year_symbol')
        if any(ref in password.lower() for ref in self.cultural_references):
            analysis['patterns_detected'].append('cultural_reference')
        if any(inst in password.upper() for inst in self.ecuadorian_institutions):
            analysis['patterns_detected'].append('institution_reference')
            
        # Cultural indicators
        for ref in self.cultural_references:
            if ref.lower() in password.lower():
                analysis['cultural_indicators'].append(ref)
                
        # Substitution patterns
        for original, sub in self.common_substitutions.items():
            if sub in password:
                analysis['substitution_patterns'].append(f"{original}->{sub}")
                
        # Vulnerability score (higher = more vulnerable)
        score = 0
        score += len(analysis['patterns_detected']) * 20
        score += len(analysis['cultural_indicators']) * 15
        score += len(analysis['substitution_patterns']) * 10
        
        if len(password) < 8:
            score += 30
        if password.lower() in ['password', 'admin', '123456']:
            score += 50
            
        analysis['vulnerability_score'] = min(score, 100)
        
        return analysis
        
    def generate_detection_rules(self) -> List[str]:
        """Generate detection rules for LLM-generated password patterns"""
        
        rules = []
        
        # Rule 1: Ecuadorian Institution Pattern Detection
        institutions_regex = "|".join(self.ecuadorian_institutions)
        rules.append(f"""
# LLM PATTERN RULE 1: Ecuadorian Institution References
# Detects passwords containing common Ecuadorian university/institution abbreviations
# Pattern: Name + Institution (PUCE, UCE, USFQ, etc.)
alert tcp any any -> any 22 (msg:"LLM-Generated Password Pattern - Institution Ref"; 
    flow:to_server,established; content:"userauth"; 
    pcre:"/[a-zA-Z]+({institutions_regex})[0-9]*[@*#]?/i";
    classtype:policy-violation; priority:3; sid:5000001; rev:1;)
        """)
        
        # Rule 2: Cultural Reference Pattern  
        cultural_regex = "|".join([ref.lower() for ref in self.cultural_references[:10]])
        rules.append(f"""
# LLM PATTERN RULE 2: Ecuadorian Cultural References
# Detects passwords with cultural context (peluchin, halamadrid, etc.)
alert tcp any any -> any 22 (msg:"LLM-Generated Password Pattern - Cultural Context"; 
    flow:to_server,established; content:"userauth";
    pcre:"/({cultural_regex})[0-9]*[@*#]?/i";
    classtype:policy-violation; priority:3; sid:5000002; rev:1;)
        """)
        
        # Rule 3: Name + Birth Year Pattern
        rules.append(f"""
# LLM PATTERN RULE 3: Name + Birth Year Pattern
# Detects common pattern of Name + 1980-2010 year range
alert tcp any any -> any 22 (msg:"LLM-Generated Password Pattern - Name+BirthYear"; 
    flow:to_server,established; content:"userauth";
    pcre:"/[a-zA-Z]+((19[8-9][0-9])|(20[0-1][0-9]))[@*#]?/";
    classtype:policy-violation; priority:2; sid:5000003; rev:1;)
        """)
        
        # Rule 4: Basic Substitution Pattern
        rules.append(f"""
# LLM PATTERN RULE 4: Basic Character Substitutions
# Detects @ for a, 0 for o, 3 for e substitutions
alert tcp any any -> any 22 (msg:"LLM-Generated Password Pattern - Basic Substitutions"; 
    flow:to_server,established; content:"userauth";
    pcre:"/[a-zA-Z]*[@03\\$17][a-zA-Z0-9@*#]*[@*#]?/";
    classtype:policy-violation; priority:3; sid:5000004; rev:1;)
        """)
        
        # Rule 5: Symbol Suffix Pattern (54% of dataset)
        rules.append(f"""
# LLM PATTERN RULE 5: Symbol Suffix Pattern
# Detects passwords ending with common symbols (@, *, #, etc.)
alert tcp any any -> any 22 (msg:"LLM-Generated Password Pattern - Symbol Suffix"; 
    flow:to_server,established; content:"userauth";
    pcre:"/[a-zA-Z0-9]+[@*#!$%&+=]+$/";
    classtype:policy-violation; priority:3; sid:5000005; rev:1;)
        """)
        
        return rules
        
    def generate_comprehensive_wordlist(self, profiles: List[EcuadorianProfile]) -> str:
        """Generate comprehensive wordlist based on all profiles"""
        
        all_passwords = set()
        
        for profile in profiles:
            passwords = self.generate_contextual_passwords(profile, 200)
            all_passwords.update(passwords)
            
        # Add common Ecuadorian patterns without profiles
        generic_profile = EcuadorianProfile()
        generic_passwords = self.generate_contextual_passwords(generic_profile, 300)
        all_passwords.update(generic_passwords)
        
        # Sort by likelihood
        sorted_passwords = sorted(list(all_passwords))
        
        # Generate statistics
        stats = {
            'total_passwords': len(sorted_passwords),
            'pattern_usage': dict(self.pattern_usage),
            'average_length': sum(len(p) for p in sorted_passwords) / len(sorted_passwords),
            'generation_timestamp': datetime.now().isoformat()
        }
        
        # Create wordlist content
        wordlist_content = f"""# LLM-Generated Ecuadorian Context Wordlist
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Total passwords: {len(sorted_passwords)}
# Average length: {stats['average_length']:.1f} characters
#
# Pattern Distribution:
# - Name+Birthdate: {self.pattern_usage[PasswordPattern.NAME_BIRTHDATE]} instances
# - Personal Info: {self.pattern_usage[PasswordPattern.PERSONAL_INFO]} instances  
# - Cultural Context: {self.pattern_usage[PasswordPattern.CULTURAL_CONTEXT]} instances
# - Symbol Suffixes: {self.pattern_usage[PasswordPattern.SYMBOL_SUFFIX]} instances
# - Numeric Sequences: {self.pattern_usage[PasswordPattern.NUMERIC_SEQUENCE]} instances
# - Basic Substitutions: {self.pattern_usage[PasswordPattern.SUBSTITUTION_BASIC]} instances
#
# Usage: High-priority passwords for brute force attacks against Ecuadorian targets
#
"""
        
        wordlist_content += "\n".join(sorted_passwords)
        
        return wordlist_content

def main():
    """Demo of LLM password pattern analysis"""
    
    analyzer = LLMPasswordAnalyzer()
    
    # Create test profile based on provided information
    luis_profile = EcuadorianProfile(
        name="Luis",
        birth_year=1996,
        institution="PUCE",  # Assuming university context
        interests=["Andrea", "Batman"],  # From provided info
        family_names=["Miguel", "Pilamunga"]
    )
    
    print("🎯 LLM PASSWORD PATTERN ANALYZER")
    print("Based on Ecuadorian dataset analysis")
    print("="*60)
    
    # Generate contextual passwords
    contextual_passwords = analyzer.generate_contextual_passwords(luis_profile, 50)
    
    print(f"✅ Generated {len(contextual_passwords)} contextual passwords")
    print("\n🔥 TOP 20 MOST LIKELY PASSWORDS:")
    for i, password in enumerate(contextual_passwords[:20], 1):
        analysis = analyzer.analyze_password_strength(password)
        print(f"   {i:2}. {password:20} (Vulnerability: {analysis['vulnerability_score']}%)")
    
    # Generate detection rules
    detection_rules = analyzer.generate_detection_rules()
    
    print(f"\n🛡️  GENERATED {len(detection_rules)} DETECTION RULES")
    
    # Save wordlist
    wordlist_content = analyzer.generate_comprehensive_wordlist([luis_profile])
    
    with open("/home/labctrl/Documents/snor/snorl_bruteforce/ecuadorian_context_wordlist.txt", 'w') as f:
        f.write(wordlist_content)
    
    # Save detection rules
    rules_content = "\n".join(detection_rules)
    with open("/home/labctrl/Documents/snor/snorl_bruteforce/llm_password_detection.rules", 'w') as f:
        f.write(rules_content)
    
    print(f"\n📊 FILES GENERATED:")
    print(f"   • ecuadorian_context_wordlist.txt ({len(contextual_passwords)} passwords)")
    print(f"   • llm_password_detection.rules ({len(detection_rules)} rules)")
    
    print(f"\n📈 PATTERN STATISTICS:")
    for pattern, count in analyzer.pattern_usage.items():
        if count > 0:
            print(f"   • {pattern.value}: {count} instances")

if __name__ == "__main__":
    main()