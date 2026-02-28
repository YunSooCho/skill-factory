"""
ClickUp API Client - Project Management
"""

import requests
import time
from typing import Optional, Dict, Any


class ClickUpError(Exception):
    """Base exception"""

class ClickUpRateLimitError(ClickUpError):
    """Rate limit"""

class ClickUpAuthenticationError(ClickUpError):
    """Auth failed"""

class ClickUpClient:
    BASE_URL = "https://api.clickup.com/api/v2"

    def __init__(self, api_token: str, timeout: int = 30):
        self.api_token = api_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': self.api_token,
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
            raise ClickUpRateLimitError("Rate limit")
        if resp.status_code == 401:
            raise ClickUpAuthenticationError("Auth failed")
        if resp.status_code >= 400:
            raise ClickUpError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_workspace(self, workspace_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/team/{workspace_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def get_teams(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/team", timeout=self.timeout)
        return self._handle_response(resp)

    def get_spaces(self, team_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/team/{team_id}/space", timeout=self.timeout)
        return self._handle_response(resp)

    def get_projects(self, space_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/space/{space_id}/project", timeout=self.timeout)
        return self._handle_response(resp)

    def get_lists(self, folder_id: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        params = {}
        if folder_id:
            params['folder_id'] = folder_id
        if project_id:
            params['project_id'] = project_id
        resp = self.session.get(f"{self.BASE_URL}/list", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_tasks(self, list_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/list/{list_id}/task", timeout=self.timeout)
        return self._handle_response(resp)

    def create_task(self, list_id: str, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/list/{list_id}/task", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/task/{task_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def update_task(self, task_id: str, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/task/{task_id}", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def create_comment(self, task_id: str, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/task/{task_id}/comment", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_time_entries(self, team_id: str, start: int, end: int) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/team/{team_id}/time_entries", params={'start_date': start, 'end_date': end}, timeout=self.timeout)
        return self._handle_response(resp)