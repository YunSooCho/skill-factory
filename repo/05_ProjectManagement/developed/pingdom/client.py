"""
Pingdom API Client - Website monitoring and analytics
"""

import requests
import time
from typing import Optional, Dict, Any, List


class PingdomError(Exception):
    """Base exception for Pingdom errors"""
    pass


class PingdomRateLimitError(PingdomError):
    """Rate limit exceeded"""
    pass


class PingdomAuthenticationError(PingdomError):
    """Authentication failed"""
    pass


class PingdomClient:
    """Client for Pingdom API"""

    BASE_URL = "https://api.pingdom.com/api/3.1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Pingdom client

        Args:
            access_token: Pingdom OAuth access token
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
            raise PingdomRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise PingdomAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise PingdomError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_checks(self, **kwargs) -> Dict[str, Any]:
        """Get checks"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/checks",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PingdomError(f"Request failed: {str(e)}")

    def create_check(self, **kwargs) -> Dict[str, Any]:
        """Create check"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/checks",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PingdomError(f"Request failed: {str(e)}")

    def get_results(self, **kwargs) -> Dict[str, Any]:
        """Get results"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/results",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PingdomError(f"Request failed: {str(e)}")

    def create_result(self, **kwargs) -> Dict[str, Any]:
        """Create result"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/results",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PingdomError(f"Request failed: {str(e)}")

    def get_analysis(self, **kwargs) -> Dict[str, Any]:
        """Get analysis"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/analysis",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PingdomError(f"Request failed: {str(e)}")

    def create_analysi(self, **kwargs) -> Dict[str, Any]:
        """Create analysi"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/analysis",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PingdomError(f"Request failed: {str(e)}")

