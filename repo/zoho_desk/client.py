"""
Zoho Desk API Client - Customer support and help desk
"""

import requests
import time
from typing import Optional, Dict, Any, List


class ZohoDeskError(Exception):
    """Base exception for Zoho Desk errors"""
    pass


class ZohoDeskRateLimitError(ZohoDeskError):
    """Rate limit exceeded"""
    pass


class ZohoDeskAuthenticationError(ZohoDeskError):
    """Authentication failed"""
    pass


class ZohoDeskClient:
    """Client for Zoho Desk API"""

    BASE_URL = "https://desk.zoho.com/api/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Zoho Desk client

        Args:
            access_token: Zoho Desk OAuth access token
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
            raise ZohoDeskRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise ZohoDeskAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise ZohoDeskError(f"API error ({response.status_code}): {error_msg}")

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
            raise ZohoDeskError(f"Request failed: {str(e)}")

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
            raise ZohoDeskError(f"Request failed: {str(e)}")

    def get_contacts(self, **kwargs) -> Dict[str, Any]:
        """Get contacts"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/contacts",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ZohoDeskError(f"Request failed: {str(e)}")

    def create_contact(self, **kwargs) -> Dict[str, Any]:
        """Create contact"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/contacts",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ZohoDeskError(f"Request failed: {str(e)}")

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
            raise ZohoDeskError(f"Request failed: {str(e)}")

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
            raise ZohoDeskError(f"Request failed: {str(e)}")

