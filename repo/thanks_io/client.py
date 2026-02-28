"""
Thanks_io Client - Thank you cards service
"""

import requests

class Thanks_ioError(Exception): pass
class APIError(Thanks_ioError): pass

class Thanks_ioClient:
    BASE_URL = "https://api.thanks.io/api/v1"

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

    def list_recipients(self, limit: int = 100) -> dict:
        return self._request("GET", "/recipients", params={"limit": limit})

    def delete_recipient(self, recipient_id: str) -> dict:
        return self._request("DELETE", f"/recipients/{recipient_id}")

    def list_orders(self, limit: int = 100) -> dict:
        return self._request("GET", "/orders", params={"limit": limit})

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()