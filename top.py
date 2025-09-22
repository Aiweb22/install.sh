import socket
import threading
import time
import sys

class NetworkSender:
    def __init__(self, target_ip, target_port, packet_size=1024):
        self.target_ip = target_ip
        self.target_port = target_port
        self.packet_size = packet_size
        self.total_sent = 0
        self.running = False
        
    def create_packet(self):
        """Create a packet of specified size"""
        return b'A' * self.packet_size
    
    def send_packets(self, thread_id):
        """Send packets continuously"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        packet = self.create_packet()
        
        try:
            while self.running:
                sock.sendto(packet, (self.target_ip, self.target_port))
                self.total_sent += self.packet_size
                
                # Print progress every 100MB
                if self.total_sent % (100 * 1024 * 1024) == 0:
                    print(f"Sent: {self.total_sent / (1024**3):.2f} GB")
                    
        except Exception as e:
            print(f"Thread {thread_id} error: {e}")
        finally:
            sock.close()
    
    def start_sending(self, target_gb=1024, num_threads=10):
        """Start sending data with multiple threads"""
        target_bytes = target_gb * 1024 * 1024 * 1024
        print(f"Starting to send {target_gb} GB to {self.target_ip}:{self.target_port}")
        print(f"Using {num_threads} threads")
        
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
        try:
            while self.total_sent < target_bytes and self.running:
                time.sleep(1)
                elapsed = time.time() - start_time
                rate_mbps = (self.total_sent / (1024**2)) / elapsed if elapsed > 0 else 0
                print(f"\rProgress: {self.total_sent/(1024**3):.2f}/{target_gb} GB | "
                      f"Rate: {rate_mbps:.2f} MB/s", end="")
                
        except KeyboardInterrupt:
            print("\nStopping...")
            
        self.running = False
        
        # Wait for threads to finish
        for thread in threads:
            thread.join()
            
        print(f"\nCompleted! Total sent: {self.total_sent/(1024**3):.2f} GB")

def main():
    # Configuration
    TARGET_IP = "194.180.176.231"  # Change this to target IP
    TARGET_PORT = 26000           # Change this to target port
    PACKET_SIZE = 1024           # Packet size in bytes
    TARGET_GB = 1024             # Total data to send in GB
    NUM_THREADS = 10             # Number of concurrent threads
    
    print("Network Data Sender - Campus Project")
    print("=" * 40)
    print(f"Target: {TARGET_IP}:{TARGET_PORT}")
    print(f"Packet Size: {PACKET_SIZE} bytes")
    print(f"Target Data: {TARGET_GB} GB")
    print(f"Threads: {NUM_THREADS}")
    print()
    
    # Confirm before starting
    response = input("Start sending? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    # Create sender and start
    sender = NetworkSender(TARGET_IP, TARGET_PORT, PACKET_SIZE)
    sender.start_sending(TARGET_GB, NUM_THREADS)

if __name__ == "__main__":
    main()