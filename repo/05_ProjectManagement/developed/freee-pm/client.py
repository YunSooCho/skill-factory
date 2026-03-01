"""
Freee PM API Client - Project Management
"""

import requests
import time
from typing import Optional, Dict, Any


class FreeePMError(Exception):
    """Base exception"""

class FreeePMRateLimitError(FreeePMError):
    """Rate limit"""

class FreeePMAuthenticationError(FreeePMError):
    """Auth failed"""

class FreeePMClient:
    BASE_URL = "https://api.freee.co.jp/pm/api/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        self.access_token = access_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
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
            raise FreeePMRateLimitError("Rate limit")
        if resp.status_code == 401:
            raise FreeePMAuthenticationError("Auth failed")
        if resp.status_code >= 400:
            raise FreeePMError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_projects(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects", timeout=self.timeout)
        return self._handle_response(resp)

    def get_project(self, project_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects/{project_id}", timeout=self.timeout)
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

    def update_task(self, task_id: str, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/tasks/{task_id}", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_members(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/members", timeout=self.timeout)
        return self._handle_response(resp)