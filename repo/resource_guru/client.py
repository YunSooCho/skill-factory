"""
Resource Guru API Client - Resource scheduling and planning
"""

import requests
import time
from typing import Optional, Dict, Any, List


class ResourceGuruError(Exception):
    """Base exception for Resource Guru errors"""
    pass


class ResourceGuruRateLimitError(ResourceGuruError):
    """Rate limit exceeded"""
    pass


class ResourceGuruAuthenticationError(ResourceGuruError):
    """Authentication failed"""
    pass


class ResourceGuruClient:
    """Client for Resource Guru API"""

    BASE_URL = "https://api.resourceguruapp.com/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Resource Guru client

        Args:
            access_token: Resource Guru OAuth access token
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
            raise ResourceGuruRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise ResourceGuruAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise ResourceGuruError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_resources(self, **kwargs) -> Dict[str, Any]:
        """Get resources"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/resources",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ResourceGuruError(f"Request failed: {str(e)}")

    def create_resource(self, **kwargs) -> Dict[str, Any]:
        """Create resource"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/resources",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ResourceGuruError(f"Request failed: {str(e)}")

    def get_bookings(self, **kwargs) -> Dict[str, Any]:
        """Get bookings"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/bookings",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ResourceGuruError(f"Request failed: {str(e)}")

    def create_booking(self, **kwargs) -> Dict[str, Any]:
        """Create booking"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/bookings",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ResourceGuruError(f"Request failed: {str(e)}")

    def get_leaves(self, **kwargs) -> Dict[str, Any]:
        """Get leaves"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/leaves",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ResourceGuruError(f"Request failed: {str(e)}")

    def create_leave(self, **kwargs) -> Dict[str, Any]:
        """Create leave"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/leaves",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ResourceGuruError(f"Request failed: {str(e)}")

