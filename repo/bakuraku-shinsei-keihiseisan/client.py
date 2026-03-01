"""
Bakuraku Shinsei Keihiseisan API Client - Application and trip fee calculation
"""

import requests
import time
from typing import Optional, Dict, Any, List


class BakurakuShinseiKeihiseisanError(Exception):
    """Base exception for Bakuraku Shinsei Keihiseisan errors"""
    pass


class BakurakuShinseiKeihiseisanRateLimitError(BakurakuShinseiKeihiseisanError):
    """Rate limit exceeded"""
    pass


class BakurakuShinseiKeihiseisanAuthenticationError(BakurakuShinseiKeihiseisanError):
    """Authentication failed"""
    pass


class BakurakuShinseiKeihiseisanClient:
    """Client for Bakuraku Shinsei Keihiseisan API"""

    BASE_URL = "https://api.bakuraku.jp/v1/shinsei-keihiseisan"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Bakuraku Shinsei Keihiseisan client

        Args:
            access_token: Bakuraku Shinsei Keihiseisan OAuth access token
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
            raise BakurakuShinseiKeihiseisanRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise BakurakuShinseiKeihiseisanAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise BakurakuShinseiKeihiseisanError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_applications(self, **kwargs) -> Dict[str, Any]:
        """Get applications"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/applications",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuShinseiKeihiseisanError(f"Request failed: {str(e)}")

    def create_application(self, **kwargs) -> Dict[str, Any]:
        """Create application"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/applications",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuShinseiKeihiseisanError(f"Request failed: {str(e)}")

    def get_calculations(self, **kwargs) -> Dict[str, Any]:
        """Get calculations"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/calculations",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuShinseiKeihiseisanError(f"Request failed: {str(e)}")

    def create_calculation(self, **kwargs) -> Dict[str, Any]:
        """Create calculation"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/calculations",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuShinseiKeihiseisanError(f"Request failed: {str(e)}")

    def get_fees(self, **kwargs) -> Dict[str, Any]:
        """Get fees"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/fees",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuShinseiKeihiseisanError(f"Request failed: {str(e)}")

    def create_fee(self, **kwargs) -> Dict[str, Any]:
        """Create fee"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/fees",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuShinseiKeihiseisanError(f"Request failed: {str(e)}")

