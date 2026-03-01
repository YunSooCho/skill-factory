"""
Telnyx API Client - Communication and telecommunications API
"""

import requests
import time
from typing import Optional, Dict, Any, List


class TelnyxError(Exception):
    """Base exception for Telnyx errors"""
    pass


class TelnyxRateLimitError(TelnyxError):
    """Rate limit exceeded"""
    pass


class TelnyxAuthenticationError(TelnyxError):
    """Authentication failed"""
    pass


class TelnyxClient:
    """Client for Telnyx API"""

    BASE_URL = "https://api.telnyx.com/v2"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Telnyx client

        Args:
            access_token: Telnyx OAuth access token
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
            raise TelnyxRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise TelnyxAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise TelnyxError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_messages(self, **kwargs) -> Dict[str, Any]:
        """Get messages"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/messages",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TelnyxError(f"Request failed: {str(e)}")

    def create_message(self, **kwargs) -> Dict[str, Any]:
        """Create message"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/messages",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TelnyxError(f"Request failed: {str(e)}")

    def get_numbers(self, **kwargs) -> Dict[str, Any]:
        """Get numbers"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/numbers",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TelnyxError(f"Request failed: {str(e)}")

    def create_number(self, **kwargs) -> Dict[str, Any]:
        """Create number"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/numbers",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TelnyxError(f"Request failed: {str(e)}")

    def get_calls(self, **kwargs) -> Dict[str, Any]:
        """Get calls"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/calls",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TelnyxError(f"Request failed: {str(e)}")

    def create_call(self, **kwargs) -> Dict[str, Any]:
        """Create call"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/calls",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TelnyxError(f"Request failed: {str(e)}")

