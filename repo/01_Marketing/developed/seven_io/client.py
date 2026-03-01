"""
Seven_io Client - SMS service
"""

import requests
import time

class Seven_ioError(Exception): pass
class APIError(Seven_ioError): pass

class Seven_ioClient:
    BASE_URL = "https://api.seven.io"

    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"X-Api-Key": api_key, "Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        url = f"{self.BASE_URL}{endpoint}"
        for _ in range(3):
            try:
                r = self.session.request(method, url, json=data, timeout=self.timeout)
                r.raise_for_status()
                return r.json()
            except requests.RequestException as e:
                time.sleep(1)
        raise APIError(f"Request failed: {e}")

    def create_contact(self, phone: str, email: str = None, name: str = None) -> dict:
        if not phone: raise APIError("phone required")
        data = {"phone": phone}
        if email: data["email"] = email
        if name: data["name"] = name
        return self._request("POST", "/contacts", data)

    def update_contact(self, contact_id: str, phone: str = None, email: str = None, name: str = None) -> dict:
        if not contact_id: raise APIError("contact_id required")
        data = {}
        if phone: data["phone"] = phone
        if email: data["email"] = email
        if name: data["name"] = name
        return self._request("PUT", f"/contacts/{contact_id}", data)

    def search_contact(self, query: str) -> dict:
        return self._request("GET", f"/contacts?query={query}")

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()