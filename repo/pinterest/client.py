"""
Pinterest API Client - Visual Discovery Platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class PinterestError(Exception):
    """Base exception for Pinterest errors"""
    pass


class PinterestRateLimitError(PinterestError):
    """Rate limit exceeded"""
    pass


class PinterestAuthenticationError(PinterestError):
    """Authentication failed"""
    pass


class PinterestClient:
    """Client for Pinterest API"""

    BASE_URL = "https://api.pinterest.com/v5"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Pinterest client

        Args:
            access_token: Pinterest OAuth access token
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
            raise PinterestRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise PinterestAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise PinterestError(f"API error ({response.status_code}): {error_msg}")

        return response.json()

    def get_user_account(self) -> Dict[str, Any]:
        """Get current user account information"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/user_account",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PinterestError(f"Request failed: {str(e)}")

    def get_boards(self, page_size: int = 25) -> Dict[str, Any]:
        """Get user's boards"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/boards",
                params={'page_size': page_size},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PinterestError(f"Request failed: {str(e)}")

    def get_board(self, board_id: str) -> Dict[str, Any]:
        """Get board details"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/boards/{board_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PinterestError(f"Request failed: {str(e)}")

    def create_board(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Create a new board"""
        self._enforce_rate_limit()
        payload = {'name': name}
        if description:
            payload['description'] = description

        try:
            response = self.session.post(
                f"{self.BASE_URL}/boards",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PinterestError(f"Request failed: {str(e)}")

    def update_board(self, board_id: str, **kwargs) -> Dict[str, Any]:
        """Update board"""
        self._enforce_rate_limit()
        try:
            response = self.session.patch(
                f"{self.BASE_URL}/boards/{board_id}",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PinterestError(f"Request failed: {str(e)}")

    def delete_board(self, board_id: str) -> Dict[str, Any]:
        """Delete board"""
        self._enforce_rate_limit()
        try:
            response = self.session.delete(
                f"{self.BASE_URL}/boards/{board_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PinterestError(f"Request failed: {str(e)}")

    def get_pins(self, board_id: Optional[str] = None, page_size: int = 25) -> Dict[str, Any]:
        """Get pins"""
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/pins"
        params = {'page_size': page_size}
        if board_id:
            url = f"{self.BASE_URL}/boards/{board_id}/pins"

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PinterestError(f"Request failed: {str(e)}")

    def get_pin(self, pin_id: str) -> Dict[str, Any]:
        """Get pin details"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/pins/{pin_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PinterestError(f"Request failed: {str(e)}")

    def create_pin(self, board_id: str, title: str, description: str,
                    source_url: str, media_source: Dict[str, str]) -> Dict[str, Any]:
        """Create a pin"""
        self._enforce_rate_limit()
        payload = {
            'board_id': board_id,
            'title': title,
            'description': description,
            'source_url': source_url,
            'media_source': media_source
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/pins",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PinterestError(f"Request failed: {str(e)}")

    def update_pin(self, pin_id: str, **kwargs) -> Dict[str, Any]:
        """Update pin"""
        self._enforce_rate_limit()
        try:
            response = self.session.patch(
                f"{self.BASE_URL}/pins/{pin_id}",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PinterestError(f"Request failed: {str(e)}")

    def delete_pin(self, pin_id: str) -> Dict[str, Any]:
        """Delete pin"""
        self._enforce_rate_limit()
        try:
            response = self.session.delete(
                f"{self.BASE_URL}/pins/{pin_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise PinterestError(f"Request failed: {str(e)}")