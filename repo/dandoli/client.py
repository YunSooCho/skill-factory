"""
Dandoli API Client - Task Management
"""

import requests
import time
from typing import Optional, Dict, Any


class DandoliError(Exception):
    """Base exception"""

class DandoliRateLimitError(DandoliError):
    """Rate limit"""

class DandoliAuthenticationError(DandoliError):
    """Auth failed"""

class DandoliClient:
    BASE_URL = "https://api.dandoli.com/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
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
            raise DandoliRateLimitError("Rate limit")
        if resp.status_code == 401:
            raise DandoliAuthenticationError("Auth failed")
        if resp.status_code >= 400:
            raise DandoliError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_tasks(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/tasks", timeout=self.timeout)
        return self._handle_response(resp)

    def create_task(self, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/tasks", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/tasks/{task_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def update_task(self, task_id: str, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/tasks/{task_id}", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_projects(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects", timeout=self.timeout)
        return self._handle_response(resp)