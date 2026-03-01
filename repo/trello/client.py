"""
Trello API Client - Kanban board project management
"""

import requests
import time
from typing import Optional, Dict, Any, List


class TrelloError(Exception):
    """Base exception for Trello errors"""
    pass


class TrelloRateLimitError(TrelloError):
    """Rate limit exceeded"""
    pass


class TrelloAuthenticationError(TrelloError):
    """Authentication failed"""
    pass


class TrelloClient:
    """Client for Trello API"""

    BASE_URL = "https://api.trello.com/1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Trello client

        Args:
            access_token: Trello OAuth access token
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
            raise TrelloRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise TrelloAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise TrelloError(f"API error ({response.status_code}): {error_msg}")

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
            raise TrelloError(f"Request failed: {str(e)}")

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
            raise TrelloError(f"Request failed: {str(e)}")

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
            raise TrelloError(f"Request failed: {str(e)}")

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
            raise TrelloError(f"Request failed: {str(e)}")

    def get_lists(self, **kwargs) -> Dict[str, Any]:
        """Get lists"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/lists",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TrelloError(f"Request failed: {str(e)}")

    def create_list(self, **kwargs) -> Dict[str, Any]:
        """Create list"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/lists",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TrelloError(f"Request failed: {str(e)}")

