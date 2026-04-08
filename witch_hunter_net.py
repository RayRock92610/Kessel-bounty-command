import socket
import time
import requests
import hashlib

BLOOD_MOON_URL = "http://localhost:36132/state/update"
SCAN_INTERVAL = 120
ALLOWED_PORTS = [36132, 8022] 

def get_open_listeners():
    listeners = []
    # Scanning block 36130-36140
    for port in range(36130, 36140): 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.01)
            if s.connect_ex(('127.0.0.1', port)) == 0:
                listeners.append(port)
    # Manual check for SSH
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.01)
        if s.connect_ex(('127.0.0.1', 8022)) == 0:
            listeners.append(8022)
    return sorted(list(set(listeners)))

while True:
    active = get_open_listeners()
    unauthorized = [p for p in active if p not in ALLOWED_PORTS]
    
    payload = {
        "agent_id": "WitchHunter_NET",
        "state_blob": {"active_ports": active, "unauthorized": unauthorized},
        "security_hash": hashlib.sha256(str(active).encode()).hexdigest()
    }
    try:
        requests.post(BLOOD_MOON_URL, json=payload, timeout=5)
    except:
        pass
    time.sleep(SCAN_INTERVAL)
