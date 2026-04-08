import os
import hashlib
import time
import requests

MONITOR_PATH = "./"
BLOOD_MOON_URL = "http://localhost:8000/state/update"
SCAN_INTERVAL = 60

def calculate_dir_hash(path):
    hashes = []
    for root, dirs, files in os.walk(path):
        for file in sorted(files):
            if file in ["blood_moon.db", "witch_hunter.py"]: continue
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    hashes.append(hashlib.md5(f.read()).hexdigest())
            except: continue
    return hashlib.md5("".join(hashes).encode()).hexdigest()

baseline = calculate_dir_hash(MONITOR_PATH)
print(f"[WITCH HUNTER] Baseline established: {baseline}")

while True:
    current = calculate_dir_hash(MONITOR_PATH)
    if current != baseline:
        print(f"[!] ALERT: Integrity Breach in {MONITOR_PATH}")
    
    payload = {
        "agent_id": "WitchHunter_FS",
        "state_blob": {"integrity_hash": current, "status": "active"},
        "security_hash": hashlib.sha256(current.encode()).hexdigest()
    }
    try:
        requests.post(BLOOD_MOON_URL, json=payload, timeout=5)
    except:
        pass
    time.sleep(SCAN_INTERVAL)
