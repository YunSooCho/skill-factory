"""
Shortcut API Client - Project management platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class ShortcutError(Exception):
    """Base exception for Shortcut errors"""
    pass


class ShortcutRateLimitError(ShortcutError):
    """Rate limit exceeded"""
    pass


class ShortcutAuthenticationError(ShortcutError):
    """Authentication failed"""
    pass


class ShortcutClient:
    """Client for Shortcut API"""

    BASE_URL = "https://api.app.shortcut.com/api/v3"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Shortcut client

        Args:
            access_token: Shortcut OAuth access token
            timeout: Request timeout in seconds
        """
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
        """Enforce rate limiting between requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.min_delay:
            time.sleep(self.min_delay - time_since_last_request)

        self.last_request_time = time.time()

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if response.status_code == 429:
            raise ShortcutRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise ShortcutAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise ShortcutError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_stories(self, **kwargs) -> Dict[str, Any]:
        """Get stories"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/stories",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ShortcutError(f"Request failed: {str(e)}")

    def create_storie(self, **kwargs) -> Dict[str, Any]:
        """Create storie"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/stories",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ShortcutError(f"Request failed: {str(e)}")

    def get_epics(self, **kwargs) -> Dict[str, Any]:
        """Get epics"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/epics",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ShortcutError(f"Request failed: {str(e)}")

    def create_epic(self, **kwargs) -> Dict[str, Any]:
        """Create epic"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/epics",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ShortcutError(f"Request failed: {str(e)}")

    def get_projects(self, **kwargs) -> Dict[str, Any]:
        """Get projects"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/projects",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ShortcutError(f"Request failed: {str(e)}")

    def create_project(self, **kwargs) -> Dict[str, Any]:
        """Create project"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/projects",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ShortcutError(f"Request failed: {str(e)}")

