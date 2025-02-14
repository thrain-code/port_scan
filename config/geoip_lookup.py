import requests
import socket

def get_public_ip():
    try:
        print("[+] Retrieving public IP address...")
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status() 
        data = response.json()
        public_ip = data.get("ip")
        print(f"[+] Public IP Address: {public_ip}")
        return public_ip
    except Exception as e:
        print(f"[-] Error retrieving public IP address: {e}")
        return None

def get_ip_geolocation(ip):
    try:
        print(f"[+] Retrieving accurate geolocation information for {ip}...")
        
        response = requests.get(f"http://ip-api.com/json/{ip}")
        response.raise_for_status()  
        data = response.json()

        if data.get("status") == "fail":
            print(f"[-] Error: {data.get('message')}")
            return

        print("[+] Geolocation Information:")
        print(f"  IP: {data.get('query')}")
        print(f"  City: {data.get('city')}")
        print(f"  Region: {data.get('regionName')}")
        print(f"  Country: {data.get('country')}")
        print(f"  Location: {data.get('lat')}, {data.get('lon')}")
        print(f"  ISP: {data.get('isp')}")
        print(f"  Timezone: {data.get('timezone')}")
        print(f"  ZIP Code: {data.get('zip')}")
        print()

        print("[+] Additional Information:")
        
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            print(f"  Hostname: {hostname}")
        except socket.herror:
            print("  Hostname: Not available (no reverse DNS record)")

        asn = data.get("as")
        if asn:
            print(f"  ASN: {asn}")
        else:
            print("  ASN: Not available")
        print()

    except requests.exceptions.RequestException as e:
        print(f"[-] Error retrieving geolocation information: {e}")
    except Exception as e:
        print(f"[-] Unexpected error: {e}")

def get_server_info():
    try:
        print("[+] Retrieving server information...")
        
        public_ip = get_public_ip()
        if not public_ip:
            return
        
        get_ip_geolocation(public_ip)
    
    except Exception as e:
        print(f"[-] Error retrieving server information: {e}")

if __name__ == "__main__":
    get_server_info()