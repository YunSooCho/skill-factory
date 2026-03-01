"""
Crowdin API Client - Localization Management
"""

import requests
import time
from typing import Optional, Dict, Any


class CrowdinError(Exception):
    """Base exception"""

class CrowdinRateLimitError(CrowdinError):
    """Rate limit"""

class CrowdinAuthenticationError(CrowdinError):
    """Auth failed"""

class CrowdinClient:
    BASE_URL = "https://api.crowdin.com/api/v2"

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
            raise CrowdinRateLimitError("Rate limit")
        if resp.status_code == 401:
            raise CrowdinAuthenticationError("Auth failed")
        if resp.status_code >= 400:
            raise CrowdinError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def list_projects(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects", timeout=self.timeout)
        return self._handle_response(resp)

    def get_project(self, project_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects/{project_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def list_projects_files(self, project_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects/{project_id}/files", timeout=self.timeout)
        return self._handle_response(resp)

    def add_file(self, project_id: str, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/projects/{project_id}/files", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_translation_status(self, project_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects/{project_id}/translations/status", timeout=self.timeout)
        return self._handle_response(resp)

    def list_languages(self, project_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects/{project_id}/languages", timeout=self.timeout)
        return self._handle_response(resp)