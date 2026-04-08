import time
import requests
import os
from signal_flare import launch_flare

API_BASE = "http://localhost:36132"
POLL_INTERVAL = 10

def trigger_lockdown(reason):
    print(f"[!] CLIVE EMERGENCY: {reason}")
    success = launch_flare({"reason": reason})
    if success:
        print("[CLIVE] Signal Flare successfully deployed.")

def check_security_status():
    try:
        # Check File System
        fs_res = requests.get(f"{API_BASE}/state/WitchHunter_FS", timeout=5)
        if fs_res.status_code == 200:
            if fs_res.json().get("status") == "breach":
                trigger_lockdown("File System Integrity Failure")

        # Check Network
        net_res = requests.get(f"{API_BASE}/state/WitchHunter_NET", timeout=5)
        if net_res.status_code == 200:
            if net_res.json().get("unauthorized"):
                trigger_lockdown(f"Unauthorized Ports: {net_res.json()['unauthorized']}")
    except:
        pass

print("[CLIVE] Orchestrator active with Signal Flare. Port: 36132")
while True:
    check_security_status()
    time.sleep(POLL_INTERVAL)
