"""
SMS Hana Client - Korean SMS service
"""

import requests

class Sms_hanaError(Exception): pass
class APIError(Sms_hanaError): pass

class Sms_hanaClient:
    BASE_URL = "https://api.sms-hana.com/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({"X-API-KEY": api_key, "Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        try:
            r = requests.request(method, f"{self.BASE_URL}{endpoint}", json=data, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def get_sms_result(self, sms_id: str) -> dict:
        return self._request("GET", f"/sms/{sms_id}/result")

    def cancel_sms(self, sms_id: str) -> dict:
        return self._request("DELETE", f"/sms/{sms_id}")

    def list_phone_numbers(self) -> dict:
        return self._request("GET", "/phone-numbers")

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()