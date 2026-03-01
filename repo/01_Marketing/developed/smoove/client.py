"""
Smoove Client - Email marketing
"""

import requests

class SmooveError(Exception): pass
class APIError(SmooveError): pass

class SmooveClient:
    BASE_URL = "https://api.smoove.io"

    def __init__(self, api_key: str, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
        try:
            r = requests.request(method, f"{self.BASE_URL}{endpoint}", json=data, params=params, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def search_contacts(self, query: str, limit: int = 100) -> dict:
        return self._request("GET", "/contacts/search", params={"query": query, "limit": limit})

    def get_contact_details(self, contact_id: str) -> dict:
        return self._request("GET", f"/contacts/{contact_id}")

    def get_lists(self, limit: int = 100) -> dict:
        return self._request("GET", "/lists", params={"limit": limit})

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()