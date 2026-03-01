"""
ChartMogul API Client - SaaS analytics and metrics platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class ChartmogulError(Exception):
    """Base exception for ChartMogul errors"""
    pass


class ChartmogulRateLimitError(ChartmogulError):
    """Rate limit exceeded"""
    pass


class ChartmogulAuthenticationError(ChartmogulError):
    """Authentication failed"""
    pass


class ChartmogulClient:
    """Client for ChartMogul API"""

    BASE_URL = "https://api.chartmogul.com/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize ChartMogul client

        Args:
            access_token: ChartMogul OAuth access token
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
            raise ChartmogulRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise ChartmogulAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise ChartmogulError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_metrics(self, **kwargs) -> Dict[str, Any]:
        """Get metrics"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/metrics",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ChartmogulError(f"Request failed: {str(e)}")

    def create_metric(self, **kwargs) -> Dict[str, Any]:
        """Create metric"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/metrics",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ChartmogulError(f"Request failed: {str(e)}")

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
            raise ChartmogulError(f"Request failed: {str(e)}")

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
            raise ChartmogulError(f"Request failed: {str(e)}")

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
            raise ChartmogulError(f"Request failed: {str(e)}")

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
            raise ChartmogulError(f"Request failed: {str(e)}")

