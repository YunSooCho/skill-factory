"""
KanbanZone API Client - Kanban project management platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class KanbanzoneError(Exception):
    """Base exception for KanbanZone errors"""
    pass


class KanbanzoneRateLimitError(KanbanzoneError):
    """Rate limit exceeded"""
    pass


class KanbanzoneAuthenticationError(KanbanzoneError):
    """Authentication failed"""
    pass


class KanbanzoneClient:
    """Client for KanbanZone API"""

    BASE_URL = "https://api.kanbanzone.com/v2"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize KanbanZone client

        Args:
            access_token: KanbanZone OAuth access token
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
            raise KanbanzoneRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise KanbanzoneAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise KanbanzoneError(f"API error ({response.status_code}): {error_msg}")

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
            raise KanbanzoneError(f"Request failed: {str(e)}")

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
            raise KanbanzoneError(f"Request failed: {str(e)}")

    def get_cards(self, **kwargs) -> Dict[str, Any]:
        """Get cards"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/cards",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise KanbanzoneError(f"Request failed: {str(e)}")

    def create_card(self, **kwargs) -> Dict[str, Any]:
        """Create card"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/cards",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise KanbanzoneError(f"Request failed: {str(e)}")

    def get_zones(self, **kwargs) -> Dict[str, Any]:
        """Get zones"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/zones",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise KanbanzoneError(f"Request failed: {str(e)}")

    def create_zone(self, **kwargs) -> Dict[str, Any]:
        """Create zone"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/zones",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise KanbanzoneError(f"Request failed: {str(e)}")

