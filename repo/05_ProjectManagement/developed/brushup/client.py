"""
Brushup API Client - Design Review
"""

import requests
import time
from typing import Optional, Dict, Any


class BrushupError(Exception):
    """Base exception"""

class BrushupRateLimitError(BrushupError):
    """Rate limit"""

class BrushupAuthenticationError(BrushupError):
    """Auth failed"""

class BrushupClient:
    BASE_URL = "https://api.brushup.io/v1"

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
            raise BrushupRateLimitError("Rate limit")
        if resp.status_code == 401:
            raise BrushupAuthenticationError("Auth failed")
        if resp.status_code >= 400:
            raise BrushupError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_projects(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects", timeout=self.timeout)
        return self._handle_response(resp)

    def create_design_review(self, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/reviews", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_review(self, review_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/reviews/{review_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def add_feedback(self, review_id: str, data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/reviews/{review_id}/feedback", json=data, timeout=self.timeout)
        return self._handle_response(resp)