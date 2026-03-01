"""
Textmagic Client - SMS service
"""

import requests

class TextmagicError(Exception): pass
class APIError(TextmagicError): pass

class TextmagicClient:
    BASE_URL = "https://rest.textmagic.com/api/v2"

    def __init__(self, username: str, password: str, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.auth = (username, password)
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
        try:
            r = requests.request(method, f"{self.BASE_URL}{endpoint}", json=data, params=params, timeout=self.timeout, auth=self.session.auth)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def delete_contact(self, contact_id: str) -> dict:
        return self._request("DELETE", f"/contacts/{contact_id}")

    def search_contact(self, query: str) -> dict:
        return self._request("GET", "/contacts", params={"search": query})

    def delete_contact_from_list(self, list_id: int, contact_id: int) -> dict:
        return self._request("DELETE", f"/lists/{list_id}/contacts/{contact_id}")

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()