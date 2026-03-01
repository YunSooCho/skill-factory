"""
Linear API Client - Project and issue tracking platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class LinearError(Exception):
    """Base exception for Linear errors"""
    pass


class LinearRateLimitError(LinearError):
    """Rate limit exceeded"""
    pass


class LinearAuthenticationError(LinearError):
    """Authentication failed"""
    pass


class LinearClient:
    """Client for Linear API"""

    BASE_URL = "https://api.linear.app/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Linear client

        Args:
            access_token: Linear OAuth access token
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
            raise LinearRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise LinearAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise LinearError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_issues(self, **kwargs) -> Dict[str, Any]:
        """Get issues"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/issues",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LinearError(f"Request failed: {str(e)}")

    def create_issue(self, **kwargs) -> Dict[str, Any]:
        """Create issue"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/issues",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LinearError(f"Request failed: {str(e)}")

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
            raise LinearError(f"Request failed: {str(e)}")

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
            raise LinearError(f"Request failed: {str(e)}")

    def get_teams(self, **kwargs) -> Dict[str, Any]:
        """Get teams"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/teams",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LinearError(f"Request failed: {str(e)}")

    def create_team(self, **kwargs) -> Dict[str, Any]:
        """Create team"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/teams",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LinearError(f"Request failed: {str(e)}")

    def get_cycles(self, **kwargs) -> Dict[str, Any]:
        """Get cycles"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/cycles",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LinearError(f"Request failed: {str(e)}")

    def create_cycle(self, **kwargs) -> Dict[str, Any]:
        """Create cycle"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/cycles",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LinearError(f"Request failed: {str(e)}")

