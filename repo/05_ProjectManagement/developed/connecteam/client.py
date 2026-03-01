"""
Connecteam API Client - Workforce Management
"""

import requests
import time
from typing import Optional, Dict, Any


class ConnecteamError(Exception):
    """Base exception"""

class ConnecteamRateLimitError(ConnecteamError):
    """Rate limit"""

class ConnecteamAuthenticationError(ConnecteamError):
    """Auth failed"""

class ConnecteamClient:
    BASE_URL = "https://api.connecteam.com/api/v1"

    def __init__(self, api_token: str, timeout: int = 30):
        self.api_token = api_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        })
        self.min_delay = 0.1
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        current = time.time()
        if (current - self.last_request_time) < self.min_delay:
            time.sleep(self.min_delay - (current - self.last_request_time))
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        if resp.status_code == 429:
            raise ConnecteamRateLimitError("Rate limit")
        if resp.status_code == 401:
            raise ConnecteamAuthenticationError("Auth failed")
        if resp.status_code >= 400:
            raise ConnecteamError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_employees(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees", timeout=self.timeout)
        return self._handle_response(resp)

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def get_shifts(self, start: str, end: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/shifts", params={'start': start, 'end': end}, timeout=self.timeout)
        return self._handle_response(resp)

    def create_shift(self, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/shifts", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_timeclock_entries(self, start: str, end: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/timeclock", params={'start': start, 'end': end}, timeout=self.timeout)
        return self._handle_response(resp)