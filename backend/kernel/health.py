#!/usr/bin/env python3
import os
import json
from datetime import datetime
import sqlite3

def log_event(service, level, action, status, details=None):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "service": service,
        "level": level,
        "action": action,
        "status": status,
        "details": details or {}
    }
    os.makedirs("logs", exist_ok=True)
    with open(f"logs/{service}.jsonl", "a") as f:
        f.write(json.dumps(log) + "
")

def check_system_health():
    health = {"status": "healthy", "services": {}}
    
    # API check
    try:
        import requests
        resp = requests.get("http://127.0.0.1:8010/health", timeout=3)
        health["services"]["api"] = {"status": resp.json()["status"]}
    except:
        health["services"]["api"] = {"status": "degraded"}
        health["status"] = "degraded"
    
    # Disk space (30-day log cleanup)
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
