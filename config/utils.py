import socket

def display_target_info(target):
    try:
        ip_address = socket.gethostbyname(target)
        print(f"\n[+] Target Information:")
        print(f"  Hostname: {target}")
        print(f"  IP Address: {ip_address}\n")
        return ip_address
    except socket.gaierror:
        print(f"[-] Error: Unable to resolve hostname {target}.")
        return None