#!/usr/bin/env python3
"""
Custom IDS Detection Script for Stealth Attack Patterns
Complements Snort rules with advanced statistical analysis
"""

import time
import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta
import numpy as np
from scipy import stats

class StealthAttackDetector:
    """Advanced detector for stealth brute force patterns"""
    
    def __init__(self):
        self.connection_log = defaultdict(list)
        self.timing_analysis = {}
        self.alert_threshold = 0.7
        
    def log_ssh_connection(self, source_ip: str, timestamp: float, success: bool = False):
        """Log SSH connection for analysis"""
        self.connection_log[source_ip].append({
            'timestamp': timestamp,
            'success': success,
            'datetime': datetime.fromtimestamp(timestamp)
        })
        
        # Trigger analysis if enough data points
        if len(self.connection_log[source_ip]) >= 5:
            self.analyze_timing_pattern(source_ip)
            
    def analyze_timing_pattern(self, source_ip: str) -> float:
        """Analyze timing patterns for artificial generation indicators"""
        connections = self.connection_log[source_ip]
        if len(connections) < 3:
            return 0.0
            
        # Calculate inter-arrival times
        intervals = []
        for i in range(1, len(connections)):
            interval = connections[i]['timestamp'] - connections[i-1]['timestamp']
            intervals.append(interval)
            
        if len(intervals) < 3:
            return 0.0
            
        # Statistical analysis
        intervals_array = np.array(intervals)
        
        # Test 1: Entropy analysis (low entropy = artificial)
        entropy_score = self.calculate_entropy(intervals_array)
        
        # Test 2: Lognormal distribution test (our scripts use lognormal)
        lognormal_p = self.test_lognormal_distribution(intervals_array)
        
        # Test 3: Regularity analysis (too regular = artificial)
        regularity_score = self.analyze_regularity(intervals_array)
        
        # Test 4: Ultra-slow pattern (5+ minute intervals consistently)
        ultra_slow_score = self.detect_ultra_slow_pattern(intervals_array)
        
        # Combine scores
        suspicion_score = (
            (1 - entropy_score) * 0.3 +  # Low entropy is suspicious
            lognormal_p * 0.2 +           # Lognormal suggests our script
            regularity_score * 0.2 +      # Too regular is suspicious
            ultra_slow_score * 0.3        # Ultra-slow is very suspicious
        )
        
        if suspicion_score > self.alert_threshold:
            self.generate_alert(source_ip, suspicion_score, {
                'entropy': entropy_score,
                'lognormal_p': lognormal_p,
                'regularity': regularity_score,
                'ultra_slow': ultra_slow_score
            })
            
        return suspicion_score
        
    def calculate_entropy(self, intervals: np.ndarray) -> float:
        """Calculate entropy of timing intervals"""
        # Bin the intervals into buckets
        hist, _ = np.histogram(intervals, bins=10)
        hist = hist[hist > 0]  # Remove zero bins
        
        # Calculate entropy
        probs = hist / hist.sum()
        entropy = -np.sum(probs * np.log2(probs))
        
        # Normalize to 0-1 scale
        max_entropy = np.log2(len(probs))
        return entropy / max_entropy if max_entropy > 0 else 0
        
    def test_lognormal_distribution(self, intervals: np.ndarray) -> float:
        """Test if intervals follow lognormal distribution (our script pattern)"""
        if len(intervals) < 5:
            return 0.0
            
        # Apply log transformation
        log_intervals = np.log(intervals[intervals > 0])
        
        # Shapiro-Wilk test for normality of log-transformed data
        try:
            _, p_value = stats.shapiro(log_intervals)
            return p_value  # High p-value suggests lognormal
        except:
            return 0.0
            
    def analyze_regularity(self, intervals: np.ndarray) -> float:
        """Analyze if intervals are suspiciously regular"""
        if len(intervals) < 3:
            return 0.0
            
        # Calculate coefficient of variation
        cv = np.std(intervals) / np.mean(intervals)
        
        # Very low CV suggests artificial regularity
        # Very high CV suggests natural human behavior
        if cv < 0.2:  # Very regular
            return 0.9
        elif cv < 0.5:  # Somewhat regular
            return 0.6
        else:  # Natural variation
            return 0.1
            
    def detect_ultra_slow_pattern(self, intervals: np.ndarray) -> float:
        """Detect ultra-slow attack pattern (5+ minutes between attempts)"""
        minutes_5 = 300  # 5 minutes in seconds
        
        # Count intervals longer than 5 minutes
        ultra_slow_count = np.sum(intervals > minutes_5)
        total_intervals = len(intervals)
        
        if total_intervals == 0:
            return 0.0
            
        # High percentage of ultra-slow intervals is suspicious
        ultra_slow_ratio = ultra_slow_count / total_intervals
        
        if ultra_slow_ratio > 0.7:  # 70%+ ultra-slow
            return 0.9
        elif ultra_slow_ratio > 0.4:  # 40%+ ultra-slow
            return 0.6
        else:
            return ultra_slow_ratio * 0.5
            
    def generate_alert(self, source_ip: str, score: float, details: dict):
        """Generate security alert"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'source_ip': source_ip,
            'alert_type': 'STEALTH_BRUTE_FORCE_SUSPECTED',
            'suspicion_score': score,
            'details': details,
            'confidence': 'HIGH' if score > 0.8 else 'MEDIUM'
        }
        
        print(f"🚨 STEALTH ATTACK ALERT: {source_ip}")
        print(f"   Suspicion Score: {score:.2f}")
        print(f"   Entropy: {details['entropy']:.2f}")
        print(f"   Lognormal P-value: {details['lognormal_p']:.3f}")
        print(f"   Regularity: {details['regularity']:.2f}")
        print(f"   Ultra-slow Pattern: {details['ultra_slow']:.2f}")
        print(f"   Confidence: {alert['confidence']}")
        
        # Log to file
        with open(f"stealth_alerts_{datetime.now().strftime('%Y%m%d')}.json", 'a') as f:
            f.write(json.dumps(alert) + "\n")

def main():
    """Demo of the detection system"""
    detector = StealthAttackDetector()
    
    # Simulate our stealth attack pattern for testing
    base_time = time.time()
    source_ip = "172.18.0.3"  # Our attacker IP
    
    # Simulate ultra-slow attack with lognormal timing (like our script)
    for i in range(8):
        # Generate lognormal interval (like our script does)
        interval = np.random.lognormal(mean=0, sigma=0.4) * 600  # Base 10 minutes
        interval = max(300, min(interval, 1800))  # 5-30 minutes like our script
        
        timestamp = base_time + (i * interval)
        detector.log_ssh_connection(source_ip, timestamp, success=False)
        
    print("Detection analysis complete.")

if __name__ == "__main__":
    main()
