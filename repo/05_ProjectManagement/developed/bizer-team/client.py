"""
Bizer Team API Client - Team Management
"""

import requests
import time
from typing import Optional, Dict, Any


class BizerTeamError(Exception):
    """Base exception"""

class BizerTeamRateLimitError(BizerTeamError):
    """Rate limit"""

class BizerTeamAuthenticationError(BizerTeamError):
    """Auth failed"""

class BizerTeamClient:
    BASE_URL = "https://api.bizerteam.com/v1"

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
            raise BizerTeamRateLimitError("Rate limit")
        if resp.status_code == 401:
            raise BizerTeamAuthenticationError("Auth failed")
        if resp.status_code >= 400:
            raise BizerTeamError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_teams(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/teams", timeout=self.timeout)
        return self._handle_response(resp)

    def get_members(self, team_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/teams/{team_id}/members", timeout=self.timeout)
        return self._handle_response(resp)

    def create_team(self, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/teams", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def create_task(self, team_id: str, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/teams/{team_id}/tasks", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_tasks(self, team_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/teams/{team_id}/tasks", timeout=self.timeout)
        return self._handle_response(resp)