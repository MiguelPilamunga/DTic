#!/usr/bin/env python3
"""
Intelligent Password Management System
Educational/Research purposes only

Features:
- SQLite database for password management
- Common passwords first approach
- Contextual password generation based on target info
- Success/failure tracking and invalidation
- Pattern analysis and optimization
"""

import sqlite3
import json
import time
import hashlib
import random
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class PasswordStatus(Enum):
    UNTESTED = "untested"
    TESTING = "testing"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    INVALID = "invalid"
    EXPIRED = "expired"

@dataclass
class TargetInfo:
    """Target information for contextual password generation"""
    name: str = ""
    birth_date: str = ""
    city: str = ""
    profession: str = ""
    institution: str = ""
    pets: List[str] = None
    sports: List[str] = None
    hobbies: List[str] = None
    family: List[str] = None
    significant_numbers: List[str] = None
    
    def __post_init__(self):
        # Initialize empty lists if None
        for field in ['pets', 'sports', 'hobbies', 'family', 'significant_numbers']:
            if getattr(self, field) is None:
                setattr(self, field, [])

class IntelligentPasswordManager:
    """Advanced password management with contextual generation"""
    
    def __init__(self, db_path: str = "password_intelligence.db"):
        self.db_path = db_path
        self.connection = None
        self.target_info = None
        self.initialize_database()
        self.load_common_passwords()
        
    def initialize_database(self):
        """Initialize SQLite database with comprehensive schema"""
        self.connection = sqlite3.connect(self.db_path)
        cursor = self.connection.cursor()
        
        # Main passwords table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                category TEXT NOT NULL,
                priority INTEGER DEFAULT 0,
                status TEXT DEFAULT 'untested',
                attempts_count INTEGER DEFAULT 0,
                last_attempt TIMESTAMP,
                success_timestamp TIMESTAMP,
                generation_method TEXT,
                context_score REAL DEFAULT 0.0,
                pattern_tags TEXT,  -- JSON array of pattern tags
                length INTEGER,
                complexity_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Password patterns and analytics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS password_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT NOT NULL,
                pattern_regex TEXT,
                success_rate REAL DEFAULT 0.0,
                usage_count INTEGER DEFAULT 0,
                last_success TIMESTAMP,
                effectiveness_score REAL DEFAULT 0.0
            )
        ''')
        
        # Target information
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS target_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_name TEXT NOT NULL,
                profile_data TEXT,  -- JSON data
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Attack sessions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attack_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_name TEXT NOT NULL,
                target_ip TEXT,
                target_port INTEGER,
                protocol TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                total_attempts INTEGER DEFAULT 0,
                successful_attempts INTEGER DEFAULT 0,
                session_data TEXT  -- JSON data
            )
        ''')
        
        self.connection.commit()
        print("✅ Password intelligence database initialized")
        
    def load_common_passwords(self):
        """Load and prioritize common passwords"""
        common_passwords = [
            # Top 50 most common passwords (high priority)
            ("123456", "common", 10),
            ("password", "common", 10),
            ("123456789", "common", 10),
            ("12345678", "common", 9),
            ("12345", "common", 9),
            ("111111", "common", 9),
            ("1234567", "common", 9),
            ("sunshine", "common", 8),
            ("qwerty", "common", 8),
            ("iloveyou", "common", 8),
            ("princess", "common", 8),
            ("admin", "common", 8),
            ("welcome", "common", 8),
            ("666666", "common", 7),
            ("abc123", "common", 7),
            ("football", "common", 7),
            ("123123", "common", 7),
            ("monkey", "common", 7),
            ("654321", "common", 7),
            ("!@#$%^&*", "common", 7),
            
            # System defaults
            ("root", "system", 9),
            ("toor", "system", 9),
            ("admin", "system", 9),
            ("administrator", "system", 8),
            ("guest", "system", 7),
            ("user", "system", 7),
            ("test", "system", 7),
            ("demo", "system", 6),
            ("service", "system", 6),
            ("backup", "system", 6),
            
            # Service-specific defaults
            ("oracle", "service", 8),
            ("postgres", "service", 8),
            ("mysql", "service", 8),
            ("redis", "service", 7),
            ("ubuntu", "service", 7),
            ("centos", "service", 7),
            ("pi", "service", 7),
            ("raspberry", "service", 7),
            
            # Variations and combinations
            ("password123", "variation", 6),
            ("admin123", "variation", 6),
            ("root123", "variation", 6),
            ("123admin", "variation", 6),
            ("password1", "variation", 5),
            ("admin1", "variation", 5),
            ("test123", "variation", 5),
            ("demo123", "variation", 5)
        ]
        
        cursor = self.connection.cursor()
        for password, category, priority in common_passwords:
            self.add_password(password, category, priority, "common_list")
            
        print(f"✅ Loaded {len(common_passwords)} common passwords")
        
    def add_password(self, password: str, category: str, priority: int = 0, generation_method: str = "manual"):
        """Add password to database with metadata"""
        cursor = self.connection.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        complexity_score = self.calculate_complexity(password)
        pattern_tags = json.dumps(self.analyze_patterns(password))
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO passwords 
                (password, password_hash, category, priority, generation_method, 
                 length, complexity_score, pattern_tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (password, password_hash, category, priority, generation_method,
                  len(password), complexity_score, pattern_tags))
            
            self.connection.commit()
            return cursor.lastrowid
            
        except sqlite3.Error as e:
            print(f"❌ Error adding password: {e}")
            return None
            
    def calculate_complexity(self, password: str) -> float:
        """Calculate password complexity score (0-10)"""
        score = 0
        
        # Length bonus
        score += min(len(password) * 0.5, 4)
        
        # Character variety
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 2
            
        # Avoid common patterns penalty
        if password.lower() in ["password", "123456", "admin"]:
            score *= 0.3
            
        return min(score, 10.0)
        
    def analyze_patterns(self, password: str) -> List[str]:
        """Analyze password patterns for categorization"""
        patterns = []
        
        if password.isdigit():
            patterns.append("numeric_only")
        if password.isalpha():
            patterns.append("alpha_only")
        if any(c.isdigit() for c in password):
            patterns.append("contains_numbers")
        if any(c.isupper() for c in password):
            patterns.append("contains_uppercase")
        if any(c.islower() for c in password):
            patterns.append("contains_lowercase")
        if any(c in "!@#$%^&*" for c in password):
            patterns.append("contains_special")
        if len(password) <= 6:
            patterns.append("short")
        elif len(password) >= 12:
            patterns.append("long")
            
        # Sequential patterns
        if "123" in password or "abc" in password.lower():
            patterns.append("sequential")
        if password[-4:].isdigit():
            patterns.append("year_suffix")
            
        return patterns
        
    def set_target_info(self, target_info: TargetInfo):
        """Set target information for contextual generation"""
        self.target_info = target_info
        
        # Save to database
        cursor = self.connection.cursor()
        profile_data = json.dumps({
            'name': target_info.name,
            'birth_date': target_info.birth_date,
            'city': target_info.city,
            'profession': target_info.profession,
            'institution': target_info.institution,
            'pets': target_info.pets,
            'sports': target_info.sports,
            'hobbies': target_info.hobbies,
            'family': target_info.family,
            'significant_numbers': target_info.significant_numbers
        })
        
        cursor.execute('''
            INSERT INTO target_profiles (target_name, profile_data)
            VALUES (?, ?)
        ''', (target_info.name, profile_data))
        
        self.connection.commit()
        print(f"✅ Target profile set: {target_info.name}")
        
    def generate_contextual_passwords(self, count: int = 50) -> List[str]:
        """Generate contextual passwords based on target information"""
        if not self.target_info:
            print("⚠️  No target information set")
            return []
            
        contextual_passwords = []
        info = self.target_info
        
        # Name-based variations
        if info.name:
            name_parts = info.name.lower().split()
            for name in name_parts:
                contextual_passwords.extend([
                    name,
                    name.capitalize(),
                    name + "123",
                    name + "2024",
                    name + "1",
                    "123" + name,
                    name[:3] + "123"
                ])
                
        # Date-based variations  
        if info.birth_date:
            # Extract different date formats
            date_formats = self.extract_date_variations(info.birth_date)
            contextual_passwords.extend(date_formats)
            
        # Location-based
        if info.city:
            city = info.city.lower()
            contextual_passwords.extend([
                city, city.capitalize(), city + "123", city + "2024"
            ])
            
        # Profession/Institution
        for field in [info.profession, info.institution]:
            if field:
                field_clean = field.lower().replace(" ", "")
                contextual_passwords.extend([
                    field_clean, field_clean + "123", field_clean + "2024"
                ])
                
        # Personal interests combinations
        all_personal = info.pets + info.sports + info.hobbies + info.family
        for item in all_personal:
            if item:
                item_clean = item.lower().replace(" ", "")
                contextual_passwords.extend([
                    item_clean, item_clean + "123", item_clean + "1"
                ])
                
        # Significant numbers combinations
        for number in info.significant_numbers:
            if number:
                contextual_passwords.extend([
                    number, "password" + number, "admin" + number, 
                    info.name.lower()[:3] + number if info.name else number
                ])
                
        # Remove duplicates and limit
        unique_passwords = list(set(contextual_passwords))[:count]
        
        # Add to database
        for password in unique_passwords:
            if password and len(password) >= 3:  # Basic validation
                context_score = self.calculate_context_score(password)
                self.add_password(password, "contextual", 
                                priority=int(context_score*2), 
                                generation_method="contextual_ai")
                
        print(f"✅ Generated {len(unique_passwords)} contextual passwords")
        return unique_passwords
        
    def extract_date_variations(self, birth_date: str) -> List[str]:
        """Extract various date format variations"""
        variations = []
        
        # Try to parse different formats
        formats_to_try = [
            "%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%d-%m-%y",
            "%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%m/%d/%y"
        ]
        
        for fmt in formats_to_try:
            try:
                date_obj = datetime.strptime(birth_date, fmt)
                variations.extend([
                    date_obj.strftime("%d%m%Y"),
                    date_obj.strftime("%d%m%y"), 
                    date_obj.strftime("%Y"),
                    date_obj.strftime("%m%d"),
                    date_obj.strftime("%d%m")
                ])
                break
            except ValueError:
                continue
                
        return variations
        
    def calculate_context_score(self, password: str) -> float:
        """Calculate how contextually relevant a password is (0-10)"""
        if not self.target_info:
            return 0.0
            
        score = 0.0
        password_lower = password.lower()
        
        # Name relevance
        if self.target_info.name:
            name_parts = [part.lower() for part in self.target_info.name.split()]
            for part in name_parts:
                if part in password_lower:
                    score += 3.0
                    
        # Personal data relevance
        all_personal = (self.target_info.pets + self.target_info.sports + 
                       self.target_info.hobbies + self.target_info.family)
        for item in all_personal:
            if item and item.lower() in password_lower:
                score += 2.0
                
        # Date relevance
        if self.target_info.birth_date:
            date_variations = self.extract_date_variations(self.target_info.birth_date)
            for date_var in date_variations:
                if date_var in password:
                    score += 1.5
                    
        return min(score, 10.0)
        
    def get_next_passwords(self, count: int = 5) -> List[Tuple[str, int, str]]:
        """Get next passwords to test, prioritized by effectiveness"""
        cursor = self.connection.cursor()
        
        cursor.execute('''
            SELECT password, priority, category, id
            FROM passwords 
            WHERE status = 'untested'
            ORDER BY priority DESC, context_score DESC, complexity_score DESC
            LIMIT ?
        ''', (count,))
        
        results = cursor.fetchall()
        
        # Mark as testing
        if results:
            ids = [str(row[3]) for row in results]
            cursor.execute(f'''
                UPDATE passwords 
                SET status = 'testing', last_attempt = CURRENT_TIMESTAMP
                WHERE id IN ({','.join(['?'] * len(ids))})
            ''', ids)
            self.connection.commit()
            
        return [(row[0], row[1], row[2]) for row in results]
        
    def mark_password_result(self, password: str, success: bool, details: str = ""):
        """Mark password test result and update statistics"""
        cursor = self.connection.cursor()
        
        status = "successful" if success else "failed"
        timestamp_field = "success_timestamp" if success else "last_attempt"
        
        cursor.execute(f'''
            UPDATE passwords 
            SET status = ?, {timestamp_field} = CURRENT_TIMESTAMP, 
                attempts_count = attempts_count + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE password = ?
        ''', (status, password))
        
        self.connection.commit()
        
        # Update pattern success rates if successful
        if success:
            self.update_pattern_success_rates(password)
            
        print(f"{'✅' if success else '❌'} Password '{password}': {status}")
        
    def update_pattern_success_rates(self, successful_password: str):
        """Update pattern success rates based on successful password"""
        patterns = self.analyze_patterns(successful_password)
        cursor = self.connection.cursor()
        
        for pattern in patterns:
            cursor.execute('''
                INSERT OR REPLACE INTO password_patterns 
                (pattern_name, success_rate, usage_count, last_success, effectiveness_score)
                VALUES (?, 
                    COALESCE((SELECT success_rate FROM password_patterns WHERE pattern_name = ?), 0) + 1,
                    COALESCE((SELECT usage_count FROM password_patterns WHERE pattern_name = ?), 0) + 1,
                    CURRENT_TIMESTAMP,
                    COALESCE((SELECT effectiveness_score FROM password_patterns WHERE pattern_name = ?), 0) + 1
                )
            ''', (pattern, pattern, pattern, pattern))
            
        self.connection.commit()
        
    def get_statistics(self) -> Dict:
        """Get comprehensive password testing statistics"""
        cursor = self.connection.cursor()
        
        # Basic stats
        cursor.execute('''
            SELECT 
                status,
                COUNT(*) as count,
                AVG(complexity_score) as avg_complexity
            FROM passwords 
            GROUP BY status
        ''')
        status_stats = {row[0]: {'count': row[1], 'avg_complexity': row[2]} 
                       for row in cursor.fetchall()}
        
        # Success rate by category
        cursor.execute('''
            SELECT 
                category,
                COUNT(*) as total,
                SUM(CASE WHEN status = 'successful' THEN 1 ELSE 0 END) as successes
            FROM passwords 
            WHERE status IN ('successful', 'failed')
            GROUP BY category
        ''')
        category_stats = {}
        for row in cursor.fetchall():
            category_stats[row[0]] = {
                'total': row[1],
                'successes': row[2],
                'success_rate': (row[2] / row[1] * 100) if row[1] > 0 else 0
            }
        
        # Top patterns
        cursor.execute('''
            SELECT pattern_name, effectiveness_score, usage_count
            FROM password_patterns
            ORDER BY effectiveness_score DESC
            LIMIT 10
        ''')
        top_patterns = [{'pattern': row[0], 'score': row[1], 'usage': row[2]} 
                       for row in cursor.fetchall()]
        
        return {
            'status_breakdown': status_stats,
            'category_success_rates': category_stats,
            'top_patterns': top_patterns,
            'database_path': self.db_path
        }
        
    def generate_report(self) -> str:
        """Generate comprehensive password analysis report"""
        stats = self.get_statistics()
        
        report = f"""
{'='*80}
INTELLIGENT PASSWORD ANALYSIS REPORT
{'='*80}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Database: {self.db_path}

STATUS BREAKDOWN:
{'-'*40}
"""
        
        for status, data in stats['status_breakdown'].items():
            report += f"{status.upper():12}: {data['count']:4} passwords (avg complexity: {data['avg_complexity']:.1f})\n"
        
        report += f"""
CATEGORY SUCCESS RATES:
{'-'*40}
"""
        
        for category, data in stats['category_success_rates'].items():
            report += f"{category.upper():12}: {data['successes']}/{data['total']} ({data['success_rate']:.1f}% success)\n"
        
        if stats['top_patterns']:
            report += f"""
TOP EFFECTIVE PATTERNS:
{'-'*40}
"""
            for i, pattern in enumerate(stats['top_patterns'], 1):
                report += f"{i:2}. {pattern['pattern']:15}: Score {pattern['score']:.1f} (used {pattern['usage']} times)\n"
        
        report += f"\n{'='*80}\n"
        
        return report
        
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

def main():
    """Demo of the intelligent password manager"""
    
    # Initialize manager
    manager = IntelligentPasswordManager()
    
    # Set target information from the provided data
    target_info = TargetInfo(
        name="Luis Miguel Pilamunga",
        birth_date="05/10/1996",  # 05 de octubre del 96
        pets=["Andrea"],  # le gusta andrea (interpreting as pet/significant person)
        significant_numbers=["96", "1996", "05", "10", "0510"]
    )
    
    manager.set_target_info(target_info)
    
    # Generate contextual passwords
    contextual_passwords = manager.generate_contextual_passwords(30)
    
    print("\n📊 PASSWORD MANAGER INITIALIZED")
    print(f"✅ Common passwords loaded: High priority system defaults")
    print(f"✅ Contextual passwords generated: {len(contextual_passwords)}")
    print(f"✅ Target profile: {target_info.name}")
    
    # Get next batch for testing
    next_passwords = manager.get_next_passwords(10)
    print(f"\n🎯 NEXT PASSWORDS FOR TESTING:")
    for i, (password, priority, category) in enumerate(next_passwords, 1):
        print(f"   {i:2}. {password:15} (Priority: {priority}, Category: {category})")
    
    # Demo: Simulate some results
    if next_passwords:
        # Simulate finding the known working password
        if "toor" in [p[0] for p in next_passwords]:
            manager.mark_password_result("toor", True, "SSH login successful")
        else:
            # Mark first few as failed for demo
            for password, _, _ in next_passwords[:3]:
                manager.mark_password_result(password, False, "Authentication failed")
    
    # Generate report
    report = manager.generate_report()
    print(report)
    
    # Save report to file
    report_file = f"password_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"📊 Report saved: {report_file}")
    
    manager.close()

if __name__ == "__main__":
    main()