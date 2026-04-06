#!/usr/bin/env python3
import json
import requests

BASE_URL = "http://127.0.0.1:8010"

def test_one(path):
    url = BASE_URL + path
    print("Testing", url)
    try:
        resp = requests.get(url, timeout=5)
        print("Status:", resp.status_code)
        ctype = resp.headers.get("content-type", "")
        if "application/json" in ctype:
            try:
                print(json.dumps(resp.json(), indent=2)[:400])
            except Exception as e:
                print("JSON parse error:", str(e))
                print(resp.text[:400])
        else:
            print(resp.text[:400])
    except Exception as e:
        print("Request failed:", str(e))
    print("-" * 40)

def main():
    print("KESSEL BOUNTY COMMAND API SCOUT")
    print("=" * 40)
    for path in ["/", "/health", "/docs", "/openapi.json"]:
        test_one(path)
    print("SCOUT COMPLETE")

if __name__ == "__main__":
    main()
