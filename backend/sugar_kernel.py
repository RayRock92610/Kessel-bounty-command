#!/usr/bin/env python3
import os
import json
import time
from datetime import datetime

def log_event(service, level, action, status, details=None):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # 30-Day Overwrite Logic (Kessel Protocol)
    now = time.time()
    for f in os.listdir(log_dir):
        f_path = os.path.join(log_dir, f)
        if os.path.isfile(f_path) and os.stat(f_path).st_mtime < now - (30 * 86400):
            os.remove(f_path) 

    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "service": service,
        "level": level,
        "action": action,
        "status": status,
        "details": details or {}
    }
    with open(f"{log_dir}/{service}.jsonl", "a") as log_file:
        log_file.write(json.dumps(log) + "\n")

def check_system_health():
    health = {"status": "healthy", "services": {}}
    try:
        import requests
        resp = requests.get("http://127.0.0.1:8010/health", timeout=3)
        health["services"]["api"] = {"status": resp.json().get("status", "unknown")}
    except Exception as e:
        health["services"]["api"] = {"status": "degraded", "error": str(e)}
        health["status"] = "degraded"

    try:
        stat = os.statvfs(".")
        free_gb = stat.f_frsize * stat.f_bavail / (1024**3)
        health["services"]["disk"] = {"free_gb": round(free_gb, 1)}
        if free_gb < 1.0:
            health["status"] = "degraded"
    except:
        health["services"]["disk"] = {"status": "unknown"}

    log_event("sugar-kernel", "INFO", "health-check", health["status"], health)
    return health

if __name__ == "__main__":
    print(json.dumps(check_system_health(), indent=2))
