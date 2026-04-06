#!/data/data/com.termux/files/usr/bin/bash

cd ~/kessel-bounty-command/backend
source venv/bin/activate

echo "[*] 1. Booting Kessel API Server in the background..."
export SQLALCHEMY_DATABASE_URI="sqlite:///./kessel_bounty.db"
nohup uvicorn app.main:app --host 127.0.0.1 --port 8000 > api.log 2>&1 &
sleep 4 # Give the server time to wake up and create the SQL tables

echo "[*] 2. Upgrading the Scout to push to SQL..."
cat << 'SCOUT_EOF' > integrated_scout.py
import requests, re
from urllib.parse import urlparse

TARGETS = ["https://bounty.apple.com", "https://api.github.com/zen"]
API_URL = "http://127.0.0.1:8000/api/v1/reports/"
DUMMY_PROGRAM_ID = "00000000-0000-0000-0000-000000000000"

STEALTH_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'X-Requested-With': 'XMLHttpRequest'
}

def push_to_db(domain, title, evidence):
    payload = {
        "title": f"[{domain}] {title}",
        "summary": "Automated discovery via Kessel Scout.",
        "description": evidence,
        "reproduction_steps": "Review Scout logs.",
        "impact_statement": "Requires manual triage.",
        "program_id": DUMMY_PROGRAM_ID,
        "state": "submitted",
        "severity": "medium"
    }
    try:
        res = requests.post(API_URL, json=payload)
        if res.status_code == 200:
            print(f"[Scout] 🟢 Successfully injected into SQL: {title}")
        else:
            print(f"[Scout] 🔴 API Error: {res.text}")
    except Exception as e:
        print(f"[Scout] 🔴 Connection Error: {e}")

for url in TARGETS:
    domain = urlparse(url).netloc
    try:
        res = requests.get(url, headers=STEALTH_HEADERS, timeout=5)
        endpoints = set(re.findall(r'href=["\'](/[^"\']+)["\']', res.text))
        if endpoints:
            push_to_db(domain, "Hidden Endpoints Detected", f"Found {len(endpoints)} paths.")
    except:
        pass
SCOUT_EOF

echo "[*] 3. Launching the Scout..."
python integrated_scout.py

echo "---------------------------------------------------"
echo "[*] 4. Querying the SQL Database to verify..."
echo "---------------------------------------------------"
# Fetch from the API and use grep to extract just the titles for easy reading
curl -s http://127.0.0.1:8000/api/v1/reports/ | grep -o '"title":"[^"]*"'

