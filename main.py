# main.py

import pyfiglet
from config.port_scanner import scan_tcp_ports
from config.whois_lookup import get_whois_info
from config.geoip_lookup import get_ip_geolocation
from config.utils import display_target_info
from config.hidden import scan_hidden_pages
from config.wifi_bruteforce import wifi_bruteforce  # Import fungsi baru

def interactive_terminal():
    title = pyfiglet.figlet_format("Thrain Rush")
    print(title)
    print("Type 'help' for available commands.\n")

    while True:
        command = input("thrain> ").strip().lower()
        if command == "help":
            print("\nAvailable commands:")
            print("  scan         - Start a new TCP port scan")
            print("  whois        - Retrieve WHOIS information for a domain")
            print("  geoip        - Retrieve geolocation information for an IP")
            print("  hiddenpages  - Scan for hidden pages/directories on a web server")
            print("  wifibrute    - Bruteforce a Wi-Fi network")  # Perintah baru
            print("  exit         - Exit the thrain\n")
        elif command == "scan":
            target = input("Enter target IP or hostname: ").strip()
            try:
                start_port = int(input("Enter start port: ").strip())
                end_port = int(input("Enter end port: ").strip())
                ip = display_target_info(target)
                if ip:
                    scan_tcp_ports(ip, start_port, end_port)
            except ValueError:
                print("[-] Error: Please enter valid port numbers.")
            except KeyboardInterrupt:
                print("\n[-] Scan aborted by user.")
        elif command == "whois":
            domain = input("Enter domain name (e.g., example.com): ").strip()
            get_whois_info(domain)
        elif command == "geoip":
            ip = input("Enter IP address: ").strip()
            get_ip_geolocation(ip)
        elif command == "hiddenpages":
            target = input("Enter target domain or IP (e.g., example.com): ").strip()
            wordlist = input("Enter path to wordlist file (e.g., wordlist.txt): ").strip()
            scan_hidden_pages(target, wordlist)
        elif command == "wifibrute":  # Perintah baru
            ssid = input("Enter the SSID of the Wi-Fi network: ").strip()
            wordlist = input("Enter path to wordlist file (e.g., wordlist.txt): ").strip()
            wifi_bruteforce(ssid, wordlist)  # Panggil fungsi baru
        elif command == "exit":
            print("[+] Exiting the thrain. Goodbye!")
            break
        else:
            print(f"[-] Unknown command: {command}")

if __name__ == "__main__":
    try:
        interactive_terminal()
    except KeyboardInterrupt:
        print("\n[-] Exiting. Goodbye!")