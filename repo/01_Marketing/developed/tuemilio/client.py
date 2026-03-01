"""
Tuemilio Client - Email verification
"""

import requests

class TuemilioError(Exception): pass
class APIError(TuemilioError): pass

class TuemilioClient:
    BASE_URL = "https://api.tuemilio.com/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({"X-API-Key": api_key, "Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        try:
            r = requests.request(method, f"{self.BASE_URL}{endpoint}", json=data, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def list_emails(self, campaign_id: str = None) -> dict:
        params = {}
        if campaign_id: params["campaign_id"] = campaign_id
        return self._request("GET", "/emails")

    def update_email(self, email_id: str, data: dict) -> dict:
        return self._request("PUT", f"/emails/{email_id}", data)

    def create_email(self, data: dict) -> dict:
        return self._request("POST", "/emails", data)

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()