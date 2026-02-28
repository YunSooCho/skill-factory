"""
Dribbble API Client - Design Platform
"""

import requests
import time
from typing import Optional, Dict, Any


class DribbbleError(Exception):
    """Base exception"""

class DribbbleRateLimitError(DribbbleError):
    """Rate limit"""

class DribbbleAuthenticationError(DribbbleError):
    """Auth failed"""

class DribbbleClient:
    BASE_URL = "https://api.dribbble.com/v2"

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
            raise DribbbleRateLimitError("Rate limit")
        if resp.status_code == 401:
            raise DribbbleAuthenticationError("Auth failed")
        if resp.status_code >= 400:
            raise DribbbleError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_user(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/user", timeout=self.timeout)
        return self._handle_response(resp)

    def get_shots(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        endpoint = f"/user/{user_id}/shots" if user_id else "/user/shots"
        resp = self.session.get(f"{self.BASE_URL}{endpoint}", timeout=self.timeout)
        return self._handle_response(resp)

    def get_shot(self, shot_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/shots/{shot_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def get_projects(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/user/projects", timeout=self.timeout)
        return self._handle_response(resp)

    def get_followers(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        endpoint = f"/user/{user_id}/followers" if user_id else "/user/followers"
        resp = self.session.get(f"{self.BASE_URL}{endpoint}", timeout=self.timeout)
        return self._handle_response(resp)

    def get_comments(self, shot_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/shots/{shot_id}/comments", timeout=self.timeout)
        return self._handle_response(resp)