"""
Systeme Io Client - Marketing platform
"""

import requests

class Systeme_ioError(Exception): pass
class APIError(Systeme_ioError): pass

class Systeme_ioClient:
    BASE_URL = "https://api.systeme.io/api/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({"X-API-Key": api_key, "Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        try:
            r = requests.request(method, f"{self.BASE_URL}{endpoint}", json=data, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def create_tag(self, name: str, color: str = None) -> dict:
        data = {"name": name}
        if color: data["color"] = color
        return self._request("POST", "/tags", data)

    def create_membership(self, level_id: str, email: str, name: str = None) -> dict:
        data = {"level_id": level_id, "email": email}
        if name: data["name"] = name
        return self._request("POST", "/memberships", data)

    def create_enrollment(self, course_id: str, email: str, name: str = None) -> dict:
        data = {"course_id": course_id, "email": email}
        if name: data["name"] = name
        return self._request("POST", "/enrollments", data)

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()