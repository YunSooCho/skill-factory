"""
SignUpGenius API Client - Online sign up and scheduling platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class SignupgeniusError(Exception):
    """Base exception for SignUpGenius errors"""
    pass


class SignupgeniusRateLimitError(SignupgeniusError):
    """Rate limit exceeded"""
    pass


class SignupgeniusAuthenticationError(SignupgeniusError):
    """Authentication failed"""
    pass


class SignupgeniusClient:
    """Client for SignUpGenius API"""

    BASE_URL = "https://api.signupgenius.com/v2"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize SignUpGenius client

        Args:
            access_token: SignUpGenius OAuth access token
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
            raise SignupgeniusRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise SignupgeniusAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise SignupgeniusError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_signups(self, **kwargs) -> Dict[str, Any]:
        """Get signups"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/signups",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise SignupgeniusError(f"Request failed: {str(e)}")

    def create_signup(self, **kwargs) -> Dict[str, Any]:
        """Create signup"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/signups",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise SignupgeniusError(f"Request failed: {str(e)}")

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
            raise SignupgeniusError(f"Request failed: {str(e)}")

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
            raise SignupgeniusError(f"Request failed: {str(e)}")

    def get_users(self, **kwargs) -> Dict[str, Any]:
        """Get users"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/users",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise SignupgeniusError(f"Request failed: {str(e)}")

    def create_user(self, **kwargs) -> Dict[str, Any]:
        """Create user"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/users",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise SignupgeniusError(f"Request failed: {str(e)}")

