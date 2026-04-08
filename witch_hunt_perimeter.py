import os
import requests
import time

# CONFIGURATION
TARGET_DIR = "/home/kessel-flow/bug_bounty_workspace"
API_BASE = "http://localhost:36132/state/update"
SUSPICIOUS_PATTERNS = [".jules", "keylog", "backdoor", "shadow"]

def scan_perimeter():
    findings = []
    for root, dirs, files in os.walk(TARGET_DIR):
        for name in files + dirs:
            for pattern in SUSPICIOUS_PATTERNS:
                if pattern in name.lower():
                    findings.append(os.path.join(root, name))
    return findings

while True:
    threats = scan_perimeter()
    if threats:
        payload = {
            "agent_id": "WitchHunter_PERIMETER",
            "state_blob": {"threats": threats, "status": "alert"},
            "security_hash": "PERIMETER_SCAN_ACTIVE"
        }
        try:
            requests.post(API_BASE, json=payload)
        except:
            pass
    time.sleep(300) # Scan every 5 minutes
