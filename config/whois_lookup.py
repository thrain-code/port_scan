import whois
import requests

def get_whois_info(domain):
    try:
        print(f"\n[+] Retrieving WHOIS information for {domain}...")

        try:
            whois_info = whois.whois(domain)
            
            if not whois_info.domain_name:
                raise ValueError("No WHOIS data found using python-whois.")
            
            print("[+] WHOIS Information (from python-whois):")
            print(f"  Domain Name: {whois_info.domain_name}")
            print(f"  Registrar: {whois_info.registrar}")
            print(f"  Creation Date: {whois_info.creation_date}")
            print(f"  Expiration Date: {whois_info.expiration_date}")
            
            if whois_info.name_servers:
                print(f"  Name Servers: {', '.join(whois_info.name_servers)}")
            else:
                print("  Name Servers: None")
        
        except Exception as e:
            print(f"[-] python-whois failed: {e}")
            print("[+] Falling back to WHOIS API...")
            
            whois_info = get_whois_from_api(domain)
            if whois_info:
                print("[+] WHOIS Information (from API):")
                for key, value in whois_info.items():
                    print(f"  {key.capitalize()}: {value}")
            else:
                print("[-] No WHOIS information found.")
        
        print()
    
    except Exception as e:
        print(f"[-] Error retrieving WHOIS information: {e}")

def get_whois_from_api(domain):
    try:
        api_url = f"https://api.whois.vu/?q={domain}"
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()  
        
        data = response.json()
        if data.get("status") == "ok":
            return data
        else:
            return None
    
    except Exception as e:
        print(f"[-] WHOIS API error: {e}")
        return None