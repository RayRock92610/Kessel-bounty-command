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
