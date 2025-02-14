import socket
from datetime import datetime
import threading

def scan_tcp_port(target, port, timeout=0.5):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        result = sock.connect_ex((target, port))
        
        if result == 0:
            try:
                service_name = socket.getservbyport(port, "tcp")
            except:
                service_name = "unknown"
            print(f"[+] Port {port} ({service_name}): Open")
            return port, service_name
        
        sock.close()
    except Exception as e:
        print(f"[-] Error scanning port {port}: {e}")
    
    return None

def scan_tcp_ports(target, start_port, end_port, timeout=0.5, max_threads=100):
    print(f"\n[+] Starting TCP Scan on Target: {target}")
    print(f"[+] Scanning Ports: {start_port}-{end_port}")
    print(f"[+] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    open_ports = []
    threads = []

    def worker(port):
        result = scan_tcp_port(target, port, timeout)
        if result:
            open_ports.append(result)

    for port in range(start_port, end_port + 1):
        while threading.active_count() > max_threads:
            pass
        thread = threading.Thread(target=worker, args=(port,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if not open_ports:
        print("[-] No open TCP ports found.")
    print(f"\n[+] TCP Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return open_ports