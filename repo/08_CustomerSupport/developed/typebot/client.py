"""
Typebot API Client - Chatbot and conversation platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class TypebotError(Exception):
    """Base exception for Typebot errors"""
    pass


class TypebotRateLimitError(TypebotError):
    """Rate limit exceeded"""
    pass


class TypebotAuthenticationError(TypebotError):
    """Authentication failed"""
    pass


class TypebotClient:
    """Client for Typebot API"""

    BASE_URL = "https://api.typebot.io/v2"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Typebot client

        Args:
            access_token: Typebot OAuth access token
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
            raise TypebotRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise TypebotAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise TypebotError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_bots(self, **kwargs) -> Dict[str, Any]:
        """Get bots"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/bots",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TypebotError(f"Request failed: {str(e)}")

    def create_bot(self, **kwargs) -> Dict[str, Any]:
        """Create bot"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/bots",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TypebotError(f"Request failed: {str(e)}")

    def get_conversations(self, **kwargs) -> Dict[str, Any]:
        """Get conversations"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/conversations",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TypebotError(f"Request failed: {str(e)}")

    def create_conversation(self, **kwargs) -> Dict[str, Any]:
        """Create conversation"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/conversations",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TypebotError(f"Request failed: {str(e)}")

    def get_results(self, **kwargs) -> Dict[str, Any]:
        """Get results"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/results",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TypebotError(f"Request failed: {str(e)}")

    def create_result(self, **kwargs) -> Dict[str, Any]:
        """Create result"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/results",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TypebotError(f"Request failed: {str(e)}")

