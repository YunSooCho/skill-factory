"""
Workast API Client - Task and project management
"""

import requests
import time
from typing import Optional, Dict, Any, List


class WorkastError(Exception):
    """Base exception for Workast errors"""
    pass


class WorkastRateLimitError(WorkastError):
    """Rate limit exceeded"""
    pass


class WorkastAuthenticationError(WorkastError):
    """Authentication failed"""
    pass


class WorkastClient:
    """Client for Workast API"""

    BASE_URL = "https://api.workast.com/v2"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Workast client

        Args:
            access_token: Workast OAuth access token
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
            raise WorkastRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise WorkastAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise WorkastError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
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
            raise WorkastError(f"Request failed: {str(e)}")

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
            raise WorkastError(f"Request failed: {str(e)}")

    def get_lists(self, **kwargs) -> Dict[str, Any]:
        """Get lists"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/lists",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise WorkastError(f"Request failed: {str(e)}")

    def create_list(self, **kwargs) -> Dict[str, Any]:
        """Create list"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/lists",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise WorkastError(f"Request failed: {str(e)}")

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
            raise WorkastError(f"Request failed: {str(e)}")

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
            raise WorkastError(f"Request failed: {str(e)}")

