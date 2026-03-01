"""
Awork API Client - Work Management
"""

import requests
import time
from typing import Optional, Dict, Any


class AworkError(Exception):
    """Base exception"""

class AworkRateLimitError(AworkError):
    """Rate limit"""

class AworkAuthenticationError(AworkError):
    """Auth failed"""

class AworkClient:
    BASE_URL = "https://api.awork.com/api/v1"

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
            raise AworkRateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise AworkAuthenticationError("Auth failed")
        if resp.status_code >= 400:
            raise AworkError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_projects(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            resp = self.session.get(f"{self.BASE_URL}/projects", timeout=self.timeout)
            return self._handle_response(resp)
        except Exception as e:
            raise AworkError(f"Failed: {str(e)}")

    def create_project(self, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            resp = self.session.post(f"{self.BASE_URL}/projects", json=data, timeout=self.timeout)
            return self._handle_response(resp)
        except Exception as e:
            raise AworkError(f"Failed: {str(e)}")

    def get_tasks(self, project_id: Optional[str] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        params = {}
        if project_id:
            params['projectId'] = project_id
        try:
            resp = self.session.get(f"{self.BASE_URL}/tasks", params=params, timeout=self.timeout)
            return self._handle_response(resp)
        except Exception as e:
            raise AworkError(f"Failed: {str(e)}")

    def create_task(self, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            resp = self.session.post(f"{self.BASE_URL}/tasks", json=data, timeout=self.timeout)
            return self._handle_response(resp)
        except Exception as e:
            raise AworkError(f"Failed: {str(e)}")

    def get_users(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            resp = self.session.get(f"{self.BASE_URL}/users", timeout=self.timeout)
            return self._handle_response(resp)
        except Exception as e:
            raise AworkError(f"Failed: {str(e)}")

    def get_time_entries(self, start: str, end: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            resp = self.session.get(f"{self.BASE_URL}/timeentries", params={'from': start, 'to': end}, timeout=self.timeout)
            return self._handle_response(resp)
        except Exception as e:
            raise AworkError(f"Failed: {str(e)}")