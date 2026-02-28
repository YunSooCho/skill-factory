"""
Stores YK Client - Customer service
"""

import requests

class Stores_ykError(Exception): pass
class APIError(Stores_ykError): pass

class Stores_ykClient:
    BASE_URL = "https://api.stores-yk.com/v1"

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

    def search_customer(self, query: str) -> dict:
        return self._request("GET", "/customers", params={"query": query})

    def list_reservations(self, customer_id: str = None) -> dict:
        params = {}
        if customer_id: params["customer_id"] = customer_id
        return self._request("GET", "/reservations", params=params)

    def get_customer(self, customer_id: str) -> dict:
        return self._request("GET", f"/customers/{customer_id}")

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()