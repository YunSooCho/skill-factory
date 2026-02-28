"""
Backlog API Client - Project & Issue Tracking
"""

import requests
import time
from typing import Optional, Dict, Any


class BacklogError(Exception):
    """Base exception"""

class BacklogRateLimitError(BacklogError):
    """Rate limit"""

class BacklogAuthenticationError(BacklogError):
    """Auth failed"""

class BacklogClient:
    BASE_URL = "https://{}.backlog.jp/api/v2"

    def __init__(self, space_key: str, api_key: str, timeout: int = 30):
        self.space_key = space_key
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.min_delay = 0.1
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        current = time.time()
        if (current - self.last_request_time) < self.min_delay:
            time.sleep(self.min_delay - (current - self.last_request_time))
        self.last_request_time = time.time()

    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        params = params or {}
        params['apiKey'] = self.api_key

        try:
            url = self.BASE_URL.format(self.space_key) + endpoint
            resp = self.session.request(method, url, params=params, json=data, timeout=self.timeout)

            if resp.status_code == 429:
                raise BacklogRateLimitError("Rate limit")
            if resp.status_code == 401:
                raise BacklogAuthenticationError("Auth failed")
            if resp.status_code >= 400:
                raise BacklogError(f"Error ({resp.status_code}): {resp.text}")

            return resp.json()

        except Exception as e:
            if isinstance(e, BacklogError):
                raise
            raise BacklogError(f"Failed: {str(e)}")

    def get_projects(self) -> Dict[str, Any]:
        return self._request('GET', '/projects')

    def get_project(self, project_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/projects/{project_id}')

    def get_issues(self, project_id: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if project_id:
            params['projectId[]'] = project_id
        return self._request('GET', '/issues', params=params)

    def get_issue(self, issue_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/issues/{issue_id}')

    def create_issue(self, data: Dict) -> Dict[str, Any]:
        return self._request('POST', '/issues', data=data)

    def update_issue(self, issue_id: str, data: Dict) -> Dict[str, Any]:
        return self._request('PATCH', f'/issues/{issue_id}', data=data)

    def add_comment(self, issue_id: str, content: str) -> Dict[str, Any]:
        return self._request('POST', f'/issues/{issue_id}/comments', data={'content': content})

    def get_users(self) -> Dict[str, Any]:
        return self._request('GET', '/users')

    def get_project_users(self, project_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/projects/{project_id}/users')