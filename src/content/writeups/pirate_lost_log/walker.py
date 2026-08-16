
import subprocess
import re

SERVER = "129.21.21.95"
CURRENT = "000n96.linksnsec.stellasec.com."
APEX = "linksnsec.stellasec.com."

print(f"[*] Starting walk from: {CURRENT}")
print("-" * 50)

visited = set()
longest_record = ""
max_len = 0

while CURRENT and CURRENT != APEX and CURRENT not in visited:
    visited.add(CURRENT)
    try:
        txt_cmd = ["dig", "+tcp", "+short", "TXT", CURRENT, f"@{SERVER}"]
        txt_data = subprocess.check_output(txt_cmd).decode().strip().replace('"', '')
        
        if txt_data:
            length = len(txt_data)
            print(f"[+] Node: {CURRENT[:10]}... | Len: {length} | Data: {txt_data}")
            
            if length > max_len:
                max_len = length
                longest_record = txt_data
    except Exception as e:
        print(f"[!] Error fetching TXT: {e}")

    try:
        nsec_cmd = ["dig", "+tcp", "+dnssec", CURRENT, f"@{SERVER}", "+noall", "+auth"]
        nsec_out = subprocess.check_output(nsec_cmd).decode()
        
        # Regex to find the domain immediately following 'NSEC'
        match = re.search(r"NSEC\s+([a-z0-9]+\.linksnsec\.stellasec\.com\.)", nsec_out)
        if match:
            CURRENT = match.group(1)
        else:
            print("[*] Reached end of chain.")
            break
    except Exception as e:
        print(f"[!] Error fetching NSEC: {e}")
        break

print("-" * 50)
print(f"Longest Entry Found ({max_len} chars):")
print(longest_record)
