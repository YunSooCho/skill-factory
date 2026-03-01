"""
Timely API Client - Time tracking and project management
"""

import requests
import time
from typing import Optional, Dict, Any, List


class TimelyError(Exception):
    """Base exception for Timely errors"""
    pass


class TimelyRateLimitError(TimelyError):
    """Rate limit exceeded"""
    pass


class TimelyAuthenticationError(TimelyError):
    """Authentication failed"""
    pass


class TimelyClient:
    """Client for Timely API"""

    BASE_URL = "https://api.timelyapp.com/v1.4"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Timely client

        Args:
            access_token: Timely OAuth access token
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
            raise TimelyRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise TimelyAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise TimelyError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_time_entries(self, **kwargs) -> Dict[str, Any]:
        """Get time entries"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/time_entries",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TimelyError(f"Request failed: {str(e)}")

    def create_time_entrie(self, **kwargs) -> Dict[str, Any]:
        """Create time entrie"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/time_entries",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TimelyError(f"Request failed: {str(e)}")

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
            raise TimelyError(f"Request failed: {str(e)}")

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
            raise TimelyError(f"Request failed: {str(e)}")

    def get_hours(self, **kwargs) -> Dict[str, Any]:
        """Get hours"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/hours",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TimelyError(f"Request failed: {str(e)}")

    def create_hour(self, **kwargs) -> Dict[str, Any]:
        """Create hour"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/hours",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TimelyError(f"Request failed: {str(e)}")

