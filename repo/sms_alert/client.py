"""
Sms_alert Client - SMS service
"""

import requests

class Sms_alertError(Exception): pass
class APIError(Sms_alertError): pass

class Sms_alertClient:
    BASE_URL = "https://api.sms-alert.com/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({"X-API-KEY": api_key, "Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
        try:
            r = requests.request(method, f"{self.BASE_URL}{endpoint}", json=data, params=params, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def search_contacts(self, query: str) -> dict:
        return self._request("GET", "/contacts", params={"query": query})

    def delete_contact(self, contact_id: str) -> dict:
        return self._request("DELETE", f"/contacts/{contact_id}")

    def send_sms(self, to: str, message: str, from_: str = None) -> dict:
        data = {"to": to, "message": message}
        if from_: data["from"] = from_
        return self._request("POST", "/sms/send", data)

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()