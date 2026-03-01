"""
Toodledo API Client - Task and to-do list management
"""

import requests
import time
from typing import Optional, Dict, Any, List


class ToodledoError(Exception):
    """Base exception for Toodledo errors"""
    pass


class ToodledoRateLimitError(ToodledoError):
    """Rate limit exceeded"""
    pass


class ToodledoAuthenticationError(ToodledoError):
    """Authentication failed"""
    pass


class ToodledoClient:
    """Client for Toodledo API"""

    BASE_URL = "https://api.toodledo.com/3"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Toodledo client

        Args:
            access_token: Toodledo OAuth access token
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
            raise ToodledoRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise ToodledoAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise ToodledoError(f"API error ({response.status_code}): {error_msg}")

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
            raise ToodledoError(f"Request failed: {str(e)}")

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
            raise ToodledoError(f"Request failed: {str(e)}")

    def get_folders(self, **kwargs) -> Dict[str, Any]:
        """Get folders"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/folders",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ToodledoError(f"Request failed: {str(e)}")

    def create_folder(self, **kwargs) -> Dict[str, Any]:
        """Create folder"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/folders",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ToodledoError(f"Request failed: {str(e)}")

    def get_goals(self, **kwargs) -> Dict[str, Any]:
        """Get goals"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/goals",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ToodledoError(f"Request failed: {str(e)}")

    def create_goal(self, **kwargs) -> Dict[str, Any]:
        """Create goal"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/goals",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ToodledoError(f"Request failed: {str(e)}")

