"""
Just SFA API Client - Sales Force Automation platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class JustSfaError(Exception):
    """Base exception for Just SFA errors"""
    pass


class JustSfaRateLimitError(JustSfaError):
    """Rate limit exceeded"""
    pass


class JustSfaAuthenticationError(JustSfaError):
    """Authentication failed"""
    pass


class JustSfaClient:
    """Client for Just SFA API"""

    BASE_URL = "https://api.just-sfa.com/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Just SFA client

        Args:
            access_token: Just SFA OAuth access token
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
            raise JustSfaRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise JustSfaAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise JustSfaError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_leads(self, **kwargs) -> Dict[str, Any]:
        """Get leads"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/leads",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise JustSfaError(f"Request failed: {str(e)}")

    def create_lead(self, **kwargs) -> Dict[str, Any]:
        """Create lead"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/leads",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise JustSfaError(f"Request failed: {str(e)}")

    def get_deals(self, **kwargs) -> Dict[str, Any]:
        """Get deals"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/deals",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise JustSfaError(f"Request failed: {str(e)}")

    def create_deal(self, **kwargs) -> Dict[str, Any]:
        """Create deal"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/deals",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise JustSfaError(f"Request failed: {str(e)}")

    def get_activities(self, **kwargs) -> Dict[str, Any]:
        """Get activities"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/activities",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise JustSfaError(f"Request failed: {str(e)}")

    def create_activitie(self, **kwargs) -> Dict[str, Any]:
        """Create activitie"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/activities",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise JustSfaError(f"Request failed: {str(e)}")

