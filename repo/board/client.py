"""
Board API Client - Digital whiteboard collaboration platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class BoardError(Exception):
    """Base exception for Board errors"""
    pass


class BoardRateLimitError(BoardError):
    """Rate limit exceeded"""
    pass


class BoardAuthenticationError(BoardError):
    """Authentication failed"""
    pass


class BoardClient:
    """Client for Board API"""

    BASE_URL = "https://api.board.com/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Board client

        Args:
            access_token: Board OAuth access token
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
            raise BoardRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise BoardAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise BoardError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_boards(self, **kwargs) -> Dict[str, Any]:
        """Get boards"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/boards",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BoardError(f"Request failed: {str(e)}")

    def create_board(self, **kwargs) -> Dict[str, Any]:
        """Create board"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/boards",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BoardError(f"Request failed: {str(e)}")

    def get_items(self, **kwargs) -> Dict[str, Any]:
        """Get items"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/items",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BoardError(f"Request failed: {str(e)}")

    def create_item(self, **kwargs) -> Dict[str, Any]:
        """Create item"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/items",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BoardError(f"Request failed: {str(e)}")

    def get_comments(self, **kwargs) -> Dict[str, Any]:
        """Get comments"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/comments",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BoardError(f"Request failed: {str(e)}")

    def create_comment(self, **kwargs) -> Dict[str, Any]:
        """Create comment"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/comments",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise BoardError(f"Request failed: {str(e)}")

