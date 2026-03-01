"""
Float API Client - Resource Scheduling
"""

import requests
import time
from typing import Optional, Dict, Any


class FloatError(Exception):
    """Base exception"""

class FloatRateLimitError(FloatError):
    """Rate limit"""

class FloatAuthenticationError(FloatError):
    """Auth failed"""

class FloatClient:
    BASE_URL = "https://api.float.com/v1"

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
            raise FloatRateLimitError("Rate limit")
        if resp.status_code == 401:
            raise FloatAuthenticationError("Auth failed")
        if resp.status_code >= 400:
            raise FloatError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_people(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/people", timeout=self.timeout)
        return self._handle_response(resp)

    def get_projects(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects", timeout=self.timeout)
        return self._handle_response(resp)

    def get_schedules(self, start: str, end: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/schedules", params={'start': start, 'end': end}, timeout=self.timeout)
        return self._handle_response(resp)

    def get_clients(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/clients", timeout=self.timeout)
        return self._handle_response(resp)

    def get_tasks(self, project_id: Optional[str] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        params = {}
        if project_id:
            params['project_id'] = project_id
        resp = self.session.get(f"{self.BASE_URL}/tasks", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_task(self, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/tasks", json=data, timeout=self.timeout)
        return self._handle_response(resp)