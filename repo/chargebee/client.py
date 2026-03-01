"""
Chargebee API Client - Subscription and recurring billing platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class ChargebeeError(Exception):
    """Base exception for Chargebee errors"""
    pass


class ChargebeeRateLimitError(ChargebeeError):
    """Rate limit exceeded"""
    pass


class ChargebeeAuthenticationError(ChargebeeError):
    """Authentication failed"""
    pass


class ChargebeeClient:
    """Client for Chargebee API"""

    BASE_URL = "https://api.chargebee.com/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Chargebee client

        Args:
            access_token: Chargebee OAuth access token
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
            raise ChargebeeRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise ChargebeeAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise ChargebeeError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_subscribers(self, **kwargs) -> Dict[str, Any]:
        """Get subscribers"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/subscribers",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ChargebeeError(f"Request failed: {str(e)}")

    def create_subscriber(self, **kwargs) -> Dict[str, Any]:
        """Create subscriber"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/subscribers",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ChargebeeError(f"Request failed: {str(e)}")

    def get_invoices(self, **kwargs) -> Dict[str, Any]:
        """Get invoices"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/invoices",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ChargebeeError(f"Request failed: {str(e)}")

    def create_invoice(self, **kwargs) -> Dict[str, Any]:
        """Create invoice"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/invoices",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ChargebeeError(f"Request failed: {str(e)}")

    def get_subscriptions(self, **kwargs) -> Dict[str, Any]:
        """Get subscriptions"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/subscriptions",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ChargebeeError(f"Request failed: {str(e)}")

    def create_subscription(self, **kwargs) -> Dict[str, Any]:
        """Create subscription"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/subscriptions",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ChargebeeError(f"Request failed: {str(e)}")

