"""
Bakuraku Kyotsukanri API Client - Shared management platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class BakurakuKyotsukanriError(Exception):
    """Base exception for Bakuraku Kyotsukanri errors"""
    pass


class BakurakuKyotsukanriRateLimitError(BakurakuKyotsukanriError):
    """Rate limit exceeded"""
    pass


class BakurakuKyotsukanriAuthenticationError(BakurakuKyotsukanriError):
    """Authentication failed"""
    pass


class BakurakuKyotsukanriClient:
    """Client for Bakuraku Kyotsukanri API"""

    BASE_URL = "https://api.bakuraku.jp/v1/kyotsukanri"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Bakuraku Kyotsukanri client

        Args:
            access_token: Bakuraku Kyotsukanri OAuth access token
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
            raise BakurakuKyotsukanriRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise BakurakuKyotsukanriAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise BakurakuKyotsukanriError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_shared_items(self, **kwargs) -> Dict[str, Any]:
        """Get shared items"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/shared_items",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuKyotsukanriError(f"Request failed: {str(e)}")

    def create_shared_item(self, **kwargs) -> Dict[str, Any]:
        """Create shared item"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/shared_items",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuKyotsukanriError(f"Request failed: {str(e)}")

    def get_permissions(self, **kwargs) -> Dict[str, Any]:
        """Get permissions"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/permissions",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuKyotsukanriError(f"Request failed: {str(e)}")

    def create_permission(self, **kwargs) -> Dict[str, Any]:
        """Create permission"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/permissions",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuKyotsukanriError(f"Request failed: {str(e)}")

    def get_groups(self, **kwargs) -> Dict[str, Any]:
        """Get groups"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/groups",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuKyotsukanriError(f"Request failed: {str(e)}")

    def create_group(self, **kwargs) -> Dict[str, Any]:
        """Create group"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/groups",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuKyotsukanriError(f"Request failed: {str(e)}")

