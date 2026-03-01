"""
Whoisfreaks Client - WHOIS service
"""

import requests

class WhoisfreaksError(Exception): pass
class APIError(WhoisfreaksError): pass

class WhoisfreaksClient:
    BASE_URL = "https://api.whoisfreaks.com/v1.0"

    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"X-API-KEY": api_key, "Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        try:
            r = requests.request(method, f"{self.BASE_URL}{endpoint}", json=data, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def historical_whois_lookup(self, domain: str, date: str = None) -> dict:
        params = {"domain": domain}
        if date: params["date"] = date
        return self._request("GET", "/whois/historical", params)

    def ip_whois_lookup(self, ip: str) -> dict:
        return self._request("GET", f"/whois/ip?ip={ip}")

    def reverse_whois_lookup(self, query: str) -> dict:
        return self._request("POST", "/reverse-whois", {"query": query})

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()