"""
Clockify API Client - Time Tracking
"""

import requests
import time
from typing import Optional, Dict, Any


class ClockifyError(Exception):
    """Base exception"""

class ClockifyRateLimitError(ClockifyError):
    """Rate limit"""

class ClockifyAuthenticationError(ClockifyError):
    """Auth failed"""

class ClockifyClient:
    BASE_URL = "https://api.clockify.me/api/v1"

    def __init__(self, api_key: str, workspace_id: str, timeout: int = 30):
        self.api_key = api_key
        self.workspace_id = workspace_id
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
            raise ClockifyRateLimitError("Rate limit")
        if resp.status_code == 401:
            raise ClockifyAuthenticationError("Auth failed")
        if resp.status_code >= 400:
            raise ClockifyError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_workspace(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/workspaces/{self.workspace_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def get_projects(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/workspaces/{self.workspace_id}/projects", timeout=self.timeout)
        return self._handle_response(resp)

    def get_time_entries(self, start: str, end: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/workspaces/{self.workspace_id}/timeEntries",
                                  params={'start': start, 'end': end},
                                  timeout=self.timeout)
        return self._handle_response(resp)

    def create_time_entry(self, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        data['start'] = data.get('start', time.strftime('%Y-%m-%dT%H:%M:%SZ'))
        resp = self.session.post(f"{self.BASE_URL}/workspaces/{self.workspace_id}/timeEntries",
                                   json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_users(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/workspaces/{self.workspace_id}/users", timeout=self.timeout)
        return self._handle_response(resp)

    def get_clients(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/workspaces/{self.workspace_id}/clients", timeout=self.timeout)
        return self._handle_response(resp)