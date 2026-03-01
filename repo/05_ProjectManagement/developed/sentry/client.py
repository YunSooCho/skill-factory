"""
Sentry API Client - Error tracking and performance monitoring
"""

import requests
import time
from typing import Optional, Dict, Any, List


class SentryError(Exception):
    """Base exception for Sentry errors"""
    pass


class SentryRateLimitError(SentryError):
    """Rate limit exceeded"""
    pass


class SentryAuthenticationError(SentryError):
    """Authentication failed"""
    pass


class SentryClient:
    """Client for Sentry API"""

    BASE_URL = "https://sentry.io/api/v0"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Sentry client

        Args:
            access_token: Sentry OAuth access token
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
            raise SentryRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise SentryAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise SentryError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_issues(self, **kwargs) -> Dict[str, Any]:
        """Get issues"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/issues",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise SentryError(f"Request failed: {str(e)}")

    def create_issue(self, **kwargs) -> Dict[str, Any]:
        """Create issue"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/issues",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise SentryError(f"Request failed: {str(e)}")

    def get_events(self, **kwargs) -> Dict[str, Any]:
        """Get events"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/events",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise SentryError(f"Request failed: {str(e)}")

    def create_event(self, **kwargs) -> Dict[str, Any]:
        """Create event"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/events",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise SentryError(f"Request failed: {str(e)}")

    def get_projects(self, **kwargs) -> Dict[str, Any]:
        """Get projects"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/projects",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise SentryError(f"Request failed: {str(e)}")

    def create_project(self, **kwargs) -> Dict[str, Any]:
        """Create project"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/projects",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise SentryError(f"Request failed: {str(e)}")

