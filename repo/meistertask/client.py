"""
MeisterTask API Client - Project and task management platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class MeistertaskError(Exception):
    """Base exception for MeisterTask errors"""
    pass


class MeistertaskRateLimitError(MeistertaskError):
    """Rate limit exceeded"""
    pass


class MeistertaskAuthenticationError(MeistertaskError):
    """Authentication failed"""
    pass


class MeistertaskClient:
    """Client for MeisterTask API"""

    BASE_URL = "https://api.meistertask.com/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize MeisterTask client

        Args:
            access_token: MeisterTask OAuth access token
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
            raise MeistertaskRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise MeistertaskAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise MeistertaskError(f"API error ({response.status_code}): {error_msg}")

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
            raise MeistertaskError(f"Request failed: {str(e)}")

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
            raise MeistertaskError(f"Request failed: {str(e)}")

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
            raise MeistertaskError(f"Request failed: {str(e)}")

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
            raise MeistertaskError(f"Request failed: {str(e)}")

    def get_sections(self, **kwargs) -> Dict[str, Any]:
        """Get sections"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/sections",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise MeistertaskError(f"Request failed: {str(e)}")

    def create_section(self, **kwargs) -> Dict[str, Any]:
        """Create section"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/sections",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise MeistertaskError(f"Request failed: {str(e)}")

