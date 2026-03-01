"""
Short Io Client - URL shortener
"""

import requests

class ShortIoError(Exception): pass
class APIError(ShortIoError): pass

class ShortIoClient:
    BASE_URL = "https://api-sv2.short.io"

    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({"Authorization": api_key, "Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        url = f"{self.BASE_URL}{endpoint}"
        try:
            r = requests.request(method, url, json=data, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def get_link_from_path(self, domain_id: str, path: str) -> dict:
        return self._request("GET", f"/links/{domain_id}{path}")

    def delete_link(self, link_id: str) -> dict:
        return self._request("DELETE", f"/links/{link_id}")

    def generate_qr_code(self, link_id: str, format: str = "png") -> dict:
        return self._request("GET", f"/links/{link_id}/qr?format={format}")

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()