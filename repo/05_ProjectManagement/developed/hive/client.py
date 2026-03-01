"""
Hive API Client - Project management and collaboration platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class HiveError(Exception):
    """Base exception for Hive errors"""
    pass


class HiveRateLimitError(HiveError):
    """Rate limit exceeded"""
    pass


class HiveAuthenticationError(HiveError):
    """Authentication failed"""
    pass


class HiveClient:
    """Client for Hive API"""

    BASE_URL = "https://api.hive.com/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Hive client

        Args:
            access_token: Hive OAuth access token
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
            raise HiveRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise HiveAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise HiveError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
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
            raise HiveError(f"Request failed: {str(e)}")

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
            raise HiveError(f"Request failed: {str(e)}")

    def get_tasks(self, **kwargs) -> Dict[str, Any]:
        """Get tasks"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/tasks",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise HiveError(f"Request failed: {str(e)}")

    def create_task(self, **kwargs) -> Dict[str, Any]:
        """Create task"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/tasks",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise HiveError(f"Request failed: {str(e)}")

    def get_actions(self, **kwargs) -> Dict[str, Any]:
        """Get actions"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/actions",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise HiveError(f"Request failed: {str(e)}")

    def create_action(self, **kwargs) -> Dict[str, Any]:
        """Create action"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/actions",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise HiveError(f"Request failed: {str(e)}")

