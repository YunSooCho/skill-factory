"""
Timing API Client - Productivity and time tracking
"""

import requests
import time
from typing import Optional, Dict, Any, List


class TimingError(Exception):
    """Base exception for Timing errors"""
    pass


class TimingRateLimitError(TimingError):
    """Rate limit exceeded"""
    pass


class TimingAuthenticationError(TimingError):
    """Authentication failed"""
    pass


class TimingClient:
    """Client for Timing API"""

    BASE_URL = "https://timingapp.com/api/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Timing client

        Args:
            access_token: Timing OAuth access token
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
            raise TimingRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise TimingAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise TimingError(f"API error ({response.status_code}): {error_msg}")

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
            raise TimingError(f"Request failed: {str(e)}")

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
            raise TimingError(f"Request failed: {str(e)}")

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
            raise TimingError(f"Request failed: {str(e)}")

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
            raise TimingError(f"Request failed: {str(e)}")

    def get_categories(self, **kwargs) -> Dict[str, Any]:
        """Get categories"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/categories",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TimingError(f"Request failed: {str(e)}")

    def create_categorie(self, **kwargs) -> Dict[str, Any]:
        """Create categorie"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/categories",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TimingError(f"Request failed: {str(e)}")

