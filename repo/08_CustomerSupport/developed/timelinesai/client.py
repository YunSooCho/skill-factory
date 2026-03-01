"""
TimelinesAI API Client - Timeline and schedule management
"""

import requests
import time
from typing import Optional, Dict, Any, List


class TimelinesaiError(Exception):
    """Base exception for TimelinesAI errors"""
    pass


class TimelinesaiRateLimitError(TimelinesaiError):
    """Rate limit exceeded"""
    pass


class TimelinesaiAuthenticationError(TimelinesaiError):
    """Authentication failed"""
    pass


class TimelinesaiClient:
    """Client for TimelinesAI API"""

    BASE_URL = "https://api.timelines.ai/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize TimelinesAI client

        Args:
            access_token: TimelinesAI OAuth access token
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
            raise TimelinesaiRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise TimelinesaiAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise TimelinesaiError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_timelines(self, **kwargs) -> Dict[str, Any]:
        """Get timelines"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/timelines",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TimelinesaiError(f"Request failed: {str(e)}")

    def create_timeline(self, **kwargs) -> Dict[str, Any]:
        """Create timeline"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/timelines",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TimelinesaiError(f"Request failed: {str(e)}")

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
            raise TimelinesaiError(f"Request failed: {str(e)}")

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
            raise TimelinesaiError(f"Request failed: {str(e)}")

    def get_milestones(self, **kwargs) -> Dict[str, Any]:
        """Get milestones"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/milestones",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TimelinesaiError(f"Request failed: {str(e)}")

    def create_milestone(self, **kwargs) -> Dict[str, Any]:
        """Create milestone"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/milestones",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise TimelinesaiError(f"Request failed: {str(e)}")

