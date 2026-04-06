class PlatformAdapter:
    def __init__(self, api_key: str): self.api_key = api_key
    def parse_payload(self, data: dict): pass

class HackerOneAdapter(PlatformAdapter):
    def parse_payload(self, data: dict):
        return {"title": data.get("title"), "severity": data.get("severity"), "ext_id": data.get("id")}

class BugcrowdAdapter(PlatformAdapter):
    def parse_payload(self, data: dict):
        return {"title": data.get("summary"), "severity": data.get("vulnerability_rating"), "ext_id": data.get("uuid")}

class IntigritiAdapter(PlatformAdapter):
    def parse_payload(self, data: dict):
        return {"title": data.get("title"), "severity": data.get("severity", {}).get("value"), "ext_id": data.get("id")}
