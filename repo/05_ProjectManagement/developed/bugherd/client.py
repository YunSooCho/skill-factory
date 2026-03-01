"""
BugHerd API Client - Bug Tracking
"""

import requests
import time
from typing import Optional, Dict, Any


class BugHerdError(Exception):
    """Base exception"""

class BugHerdRateLimitError(BugHerdError):
    """Rate limit"""

class BugHerdAuthenticationError(BugHerdError):
    """Auth failed"""

class BugHerdClient:
    BASE_URL = "https://www.bugherd.com/api_v2"

    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = (api_key, 'x')
        self.session.headers.update({'Content-Type': 'application/json'})
        self.min_delay = 0.1
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        current = time.time()
        if (current - self.last_request_time) < self.min_delay:
            time.sleep(self.min_delay - (current - self.last_request_time))
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        if resp.status_code == 429:
            raise BugHerdRateLimitError("Rate limit")
        if resp.status_code == 401:
            raise BugHerdAuthenticationError("Auth failed")
        if resp.status_code >= 400:
            raise BugHerdError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_projects(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects", timeout=self.timeout)
        return self._handle_response(resp)

    def get_project(self, project_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects/{project_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def get_tasks(self, project_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects/{project_id}/tasks", timeout=self.timeout)
        return self._handle_response(resp)

    def create_task(self, project_id: str, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/projects/{project_id}/tasks", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_task(self, project_id: str, task_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects/{project_id}/tasks/{task_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def update_task(self, project_id: str, task_id: str, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/projects/{project_id}/tasks/{task_id}", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_task(self, project_id: str, task_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.BASE_URL}/projects/{project_id}/tasks/{task_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def get_comments(self, project_id: str, task_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects/{project_id}/tasks/{task_id}/comments", timeout=self.timeout)
        return self._handle_response(resp)