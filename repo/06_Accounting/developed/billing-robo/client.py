"""
Billing Robo API Client - Billing and invoicing automation platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class BillingRoboError(Exception):
    """Base exception for Billing Robo errors"""
    pass


class BillingRoboRateLimitError(BillingRoboError):
    """Rate limit exceeded"""
    pass


class BillingRoboAuthenticationError(BillingRoboError):
    """Authentication failed"""
    pass


class BillingRoboClient:
    """Client for Billing Robo API"""

    BASE_URL = "https://api.billingrobo.com/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Billing Robo client

        Args:
            access_token: Billing Robo OAuth access token
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
            raise BillingRoboRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise BillingRoboAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise BillingRoboError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
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
            raise BillingRoboError(f"Request failed: {str(e)}")

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
            raise BillingRoboError(f"Request failed: {str(e)}")

    def get_customers(self, **kwargs) -> Dict[str, Any]:
        """Get customers"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/customers",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BillingRoboError(f"Request failed: {str(e)}")

    def create_customer(self, **kwargs) -> Dict[str, Any]:
        """Create customer"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/customers",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BillingRoboError(f"Request failed: {str(e)}")

    def get_payments(self, **kwargs) -> Dict[str, Any]:
        """Get payments"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/payments",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BillingRoboError(f"Request failed: {str(e)}")

    def create_payment(self, **kwargs) -> Dict[str, Any]:
        """Create payment"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/payments",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BillingRoboError(f"Request failed: {str(e)}")

