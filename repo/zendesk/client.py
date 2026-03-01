"""
Zendesk API Client - Customer support and ticketing platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class ZendeskError(Exception):
    """Base exception for Zendesk errors"""
    pass


class ZendeskRateLimitError(ZendeskError):
    """Rate limit exceeded"""
    pass


class ZendeskAuthenticationError(ZendeskError):
    """Authentication failed"""
    pass


class ZendeskClient:
    """Client for Zendesk API"""

    BASE_URL = "https://api.zendesk.com/api/v2"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Zendesk client

        Args:
            access_token: Zendesk OAuth access token
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
            raise ZendeskRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise ZendeskAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise ZendeskError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_tickets(self, **kwargs) -> Dict[str, Any]:
        """Get tickets"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/tickets",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ZendeskError(f"Request failed: {str(e)}")

    def create_ticket(self, **kwargs) -> Dict[str, Any]:
        """Create ticket"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/tickets",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ZendeskError(f"Request failed: {str(e)}")

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
            raise ZendeskError(f"Request failed: {str(e)}")

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
            raise ZendeskError(f"Request failed: {str(e)}")

    def get_organizations(self, **kwargs) -> Dict[str, Any]:
        """Get organizations"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/organizations",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ZendeskError(f"Request failed: {str(e)}")

    def create_organization(self, **kwargs) -> Dict[str, Any]:
        """Create organization"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/organizations",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ZendeskError(f"Request failed: {str(e)}")

