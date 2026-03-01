"""
ClimberCloud API Client - Cloud computing and infrastructure platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class ClimbercloudError(Exception):
    """Base exception for ClimberCloud errors"""
    pass


class ClimbercloudRateLimitError(ClimbercloudError):
    """Rate limit exceeded"""
    pass


class ClimbercloudAuthenticationError(ClimbercloudError):
    """Authentication failed"""
    pass


class ClimbercloudClient:
    """Client for ClimberCloud API"""

    BASE_URL = "https://api.climbercloud.com/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize ClimberCloud client

        Args:
            access_token: ClimberCloud OAuth access token
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
            raise ClimbercloudRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise ClimbercloudAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise ClimbercloudError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_servers(self, **kwargs) -> Dict[str, Any]:
        """Get servers"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/servers",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ClimbercloudError(f"Request failed: {str(e)}")

    def create_server(self, **kwargs) -> Dict[str, Any]:
        """Create server"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/servers",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ClimbercloudError(f"Request failed: {str(e)}")

    def get_storage(self, **kwargs) -> Dict[str, Any]:
        """Get storage"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/storage",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ClimbercloudError(f"Request failed: {str(e)}")

    def create_storage(self, **kwargs) -> Dict[str, Any]:
        """Create storage"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/storage",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ClimbercloudError(f"Request failed: {str(e)}")

    def get_networks(self, **kwargs) -> Dict[str, Any]:
        """Get networks"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/networks",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ClimbercloudError(f"Request failed: {str(e)}")

    def create_network(self, **kwargs) -> Dict[str, Any]:
        """Create network"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/networks",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ClimbercloudError(f"Request failed: {str(e)}")

