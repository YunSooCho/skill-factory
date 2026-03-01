"""
Everhour API Client - Time Tracking
"""

import requests
import time
from typing import Optional, Dict, Any


class EverhourError(Exception):
    """Base exception"""

class EverhourRateLimitError(EverhourError):
    """Rate limit"""

class EverhourAuthenticationError(EverhourError):
    """Auth failed"""

class EverhourClient:
    BASE_URL = "https://api.everhour.com/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'X-Api-Key': api_key,
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
            raise EverhourRateLimitError("Rate limit")
        if resp.status_code == 401:
            raise EverhourAuthenticationError("Auth failed")
        if resp.status_code >= 400:
            raise EverhourError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_teams(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/teams", timeout=self.timeout)
        return self._handle_response(resp)

    def get_projects(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects", timeout=self.timeout)
        return self._handle_response(resp)

    def get_time_entries(self, start: str, end: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/time", params={'from': start, 'to': end}, timeout=self.timeout)
        return self._handle_response(resp)

    def create_time_entry(self, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/time", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_users(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/users", timeout=self.timeout)
        return self._handle_response(resp)

    def get_tasks(self, project_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects/{project_id}/tasks", timeout=self.timeout)
        return self._handle_response(resp)