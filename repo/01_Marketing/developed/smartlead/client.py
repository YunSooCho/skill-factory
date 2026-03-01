"""
Smartlead Client - Email marketing
"""

import requests

class SmartleadError(Exception): pass
class APIError(SmartleadError): pass

class SmartleadClient:
    BASE_URL = "https://server.smartlead.ai/api/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({"X-API-KEY": api_key, "Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        try:
            r = requests.request(method, f"{self.BASE_URL}{endpoint}", json=data, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def update_campaign_schedule(self, campaign_id: int, schedule: dict) -> dict:
        return self._request("PUT", f"/campaigns/{campaign_id}/schedule", schedule)

    def add_leads_to_campaign(self, campaign_id: int, leads: list) -> dict:
        return self._request("POST", f"/campaigns/{campaign_id}/leads", {"leads": leads})

    def update_lead(self, lead_id: str, data: dict) -> dict:
        return self._request("PUT", f"/leads/{lead_id}", data)

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()