"""
Twilio_verify Client - Verification service
"""

import requests

class Twilio_verifyError(Exception): pass
class APIError(Twilio_verifyError): pass

class Twilio_verifyClient:
    BASE_URL = "https://verify.twilio.com/v2"

    def __init__(self, account_sid: str, auth_token: str, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.auth = (account_sid, auth_token)
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        try:
            r = requests.request(method, f"{self.BASE_URL}{endpoint}", json=data, timeout=self.timeout, auth=self.session.auth)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def create_verification(self, to: str, channel: str = "sms") -> dict:
        data = {"to": to, "channel": channel}
        return self._request("POST", f"/services/{self.service_sid}/verifications", data)

    def check_verification(self, to: str, code: str) -> dict:
        data = {"to": to, "code": code}
        return self._request("POST", f"/services/{self.service_sid}/verifications/check", data)

    def __init__(self, account_sid: str, auth_token: str, service_sid: str = None, timeout: int = 30):
        self.service_sid = service_sid
        self.session = requests.Session()
        self.timeout = timeout
        self._auth = (account_sid, auth_token)
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        try:
            r = requests.request(method, f"{self.BASE_URL}{endpoint}", json=data, timeout=self.timeout, auth=self._auth, headers=self.session.headers)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()