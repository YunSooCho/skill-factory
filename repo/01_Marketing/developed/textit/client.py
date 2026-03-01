"""
Textit Client - SMS service
"""

import requests

class TextitError(Exception): pass
class APIError(TextitError): pass

class TextitClient:
    BASE_URL = "https://api.textit.in/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({"Authorization": f"Token {api_key}", "Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
        try:
            r = requests.request(method, f"{self.BASE_URL}{endpoint}", json=data, params=params, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def search_contacts(self, query: str) -> dict:
        return self._request("GET", f"/contacts", params={"search": query})

    def delete_contact(self, contact_id: str) -> dict:
        return self._request("DELETE", f"/contacts/{contact_id}")

    def search_messages(self, contact_id: str = None) -> dict:
        params = {}
        if contact_id: params["contact"] = contact_id
        return self._request("GET", "/messages", params=params)

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()