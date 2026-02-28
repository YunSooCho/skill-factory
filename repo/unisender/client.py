"""
Unisender Client - Email marketing
"""

import requests

class UnisenderError(Exception): pass
class APIError(UnisenderError): pass

class UnisenderClient:
    BASE_URL = "https://api.unisender.com/api/v3"

    def __init__(self, api_key: str, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        if data is None: data = {}
        data["api_key"] = self.api_key
        try:
            r = requests.request(method, f"{self.BASE_URL}{endpoint}", json=data, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def create_contact_list(self, title: str) -> dict:
        return self._request("POST", "/lists", {"title": title})

    def list_contact_lists(self) -> dict:
        return self._request("GET", "/lists")

    def create_or_update_contact(self, list_id: str, email: str, fields: dict = None) -> dict:
        data = {"list_id": list_id, "email": email}
        if fields: data["fields"] = fields
        return self._request("POST", "/contacts", data)

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()