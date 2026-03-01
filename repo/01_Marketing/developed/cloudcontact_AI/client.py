"""
CloudContact AI API Client - AI-powered contact center platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class CloudcontactAIError(Exception):
    """Base exception for CloudContact AI errors"""
    pass


class CloudcontactAIRateLimitError(CloudcontactAIError):
    """Rate limit exceeded"""
    pass


class CloudcontactAIAuthenticationError(CloudcontactAIError):
    """Authentication failed"""
    pass


class CloudContactAIClient:
    """Client for CloudContact AI API"""

    BASE_URL = "https://api.cloudcontact.ai/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize CloudContact AI client

        Args:
            access_token: CloudContact AI OAuth access token
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
            raise CloudcontactAIRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise CloudcontactAIAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise CloudcontactAIError(f"API error ({response.status_code}): {error_msg}")

        return response.json()

    def get_contacts(self, page_size: int = 25, **kwargs) -> Dict[str, Any]:
        """Get contacts"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/contacts",
                params={'page_size': page_size, **kwargs},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise CloudcontactAIError(f"Request failed: {str(e)}")

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
            raise CloudcontactAIError(f"Request failed: {str(e)}")

    def get_calls(self, page_size: int = 25, **kwargs) -> Dict[str, Any]:
        """Get calls"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/calls",
                params={'page_size': page_size, **kwargs},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise CloudcontactAIError(f"Request failed: {str(e)}")

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
            raise CloudcontactAIError(f"Request failed: {str(e)}")

    def get_chats(self, page_size: int = 25, **kwargs) -> Dict[str, Any]:
        """Get chats"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/chats",
                params={'page_size': page_size, **kwargs},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise CloudcontactAIError(f"Request failed: {str(e)}")