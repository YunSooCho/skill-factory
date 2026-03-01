"""
Bakuraku Denshichobohozon API Client - Electronic book preservation platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class BakurakuDenshichobohozonError(Exception):
    """Base exception for Bakuraku Denshichobohozon errors"""
    pass


class BakurakuDenshichobohozonRateLimitError(BakurakuDenshichobohozonError):
    """Rate limit exceeded"""
    pass


class BakurakuDenshichobohozonAuthenticationError(BakurakuDenshichobohozonError):
    """Authentication failed"""
    pass


class BakurakuDenshichobohozonClient:
    """Client for Bakuraku Denshichobohozon API"""

    BASE_URL = "https://api.bakuraku.jp/v1/denshichobohozon"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Bakuraku Denshichobohozon client

        Args:
            access_token: Bakuraku Denshichobohozon OAuth access token
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
            raise BakurakuDenshichobohozonRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise BakurakuDenshichobohozonAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise BakurakuDenshichobohozonError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_documents(self, **kwargs) -> Dict[str, Any]:
        """Get documents"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/documents",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuDenshichobohozonError(f"Request failed: {str(e)}")

    def create_document(self, **kwargs) -> Dict[str, Any]:
        """Create document"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/documents",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuDenshichobohozonError(f"Request failed: {str(e)}")

    def get_preservations(self, **kwargs) -> Dict[str, Any]:
        """Get preservations"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/preservations",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuDenshichobohozonError(f"Request failed: {str(e)}")

    def create_preservation(self, **kwargs) -> Dict[str, Any]:
        """Create preservation"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/preservations",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuDenshichobohozonError(f"Request failed: {str(e)}")

    def get_archive(self, **kwargs) -> Dict[str, Any]:
        """Get archive"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/archive",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuDenshichobohozonError(f"Request failed: {str(e)}")

    def create_archive(self, **kwargs) -> Dict[str, Any]:
        """Create archive"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/archive",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BakurakuDenshichobohozonError(f"Request failed: {str(e)}")

