# config/hidden.py

import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def scan_hidden_pages(target, wordlist, threads=5, timeout=5):
    """
    Scan for hidden pages and directories on a target web server.
    
    Args:
        target (str): Target domain or IP address
        wordlist (str): Path to wordlist file
        threads (int): Number of concurrent threads
        timeout (int): Request timeout in seconds
    """
    try:
        print(f"\n[+] Starting hidden pages scan on {target}")
        print(f"[+] Using wordlist: {wordlist}")
        
        # Validate inputs
        if not target:
            print("[-] Error: Target cannot be empty")
            return
            
        wordlist_path = Path(wordlist)
        if not wordlist_path.exists():
            print(f"[-] Error: Wordlist file '{wordlist}' not found")
            return

        # Read wordlist
        with open(wordlist_path, "r") as file:
            words = file.read().splitlines()
        
        print(f"[+] Loaded {len(words)} words from wordlist")
        
        # Create session for connection pooling
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Thrain-Scanner/1.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        })

        discovered_pages = []

        def check_url(word):
            """Worker function to check individual URLs"""
            url = f"http://{target}/{word.strip()}"
            try:
                response = session.get(url, timeout=timeout, allow_redirects=True)
                status = response.status_code
                
                # Check for interesting status codes
                if status == 200:
                    print(f"[+] Found: {url} (Status: {status})")
                    discovered_pages.append((url, status, "Accessible"))
                elif status == 403:
                    print(f"[+] Found (Forbidden): {url} (Status: {status})")
                    discovered_pages.append((url, status, "Forbidden"))
                elif status in [301, 302, 307, 308]:
                    redirect_url = response.headers.get('Location', '')
                    print(f"[+] Redirect: {url} → {redirect_url}")
                    discovered_pages.append((url, status, f"Redirect → {redirect_url}"))
                elif status == 404:
                    # Skip 404 pages as they are not interesting
                    pass
                else:
                    print(f"[+] Found (Other): {url} (Status: {status})")
                    discovered_pages.append((url, status, "Other"))
                    
                # Add small delay to prevent overwhelming the server
                time.sleep(0.1)
                
            except requests.exceptions.RequestException as e:
                if "connection" in str(e).lower():
                    print(f"[-] Connection error for {url}")
                elif "timeout" in str(e).lower():
                    print(f"[-] Timeout reached for {url}")
                else:
                    print(f"[-] Error accessing {url}: {str(e)}")
            except Exception as e:
                print(f"[-] Unexpected error checking {url}: {str(e)}")

        # Use ThreadPoolExecutor for concurrent scanning
        try:
            with ThreadPoolExecutor(max_workers=threads) as executor:
                list(executor.map(check_url, words))
        except KeyboardInterrupt:
            print("\n[-] Scan interrupted by user")
            return
        except Exception as e:
            print(f"[-] Error during scan execution: {str(e)}")
            return

        # Print summary
        print("\n=== Scan Summary ===")
        print(f"Total discovered pages: {len(discovered_pages)}")
        if discovered_pages:
            print("\nDiscovered Pages:")
            for url, status, description in discovered_pages:
                print(f"  - {url} (Status: {status}, Description: {description})")
        
        print("\n[+] Hidden pages scan completed")

    except KeyboardInterrupt:
        print("\n[-] Scan aborted by user")
    except Exception as e:
        print(f"[-] Critical error during hidden pages scan: {str(e)}")