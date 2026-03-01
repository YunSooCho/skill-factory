"""
Harness API Client - Software delivery and DevOps platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class HarnessError(Exception):
    """Base exception for Harness errors"""
    pass


class HarnessRateLimitError(HarnessError):
    """Rate limit exceeded"""
    pass


class HarnessAuthenticationError(HarnessError):
    """Authentication failed"""
    pass


class HarnessClient:
    """Client for Harness API"""

    BASE_URL = "https://api.harness.io/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Harness client

        Args:
            access_token: Harness OAuth access token
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
            raise HarnessRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise HarnessAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise HarnessError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_pipelines(self, **kwargs) -> Dict[str, Any]:
        """Get pipelines"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/pipelines",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise HarnessError(f"Request failed: {str(e)}")

    def create_pipeline(self, **kwargs) -> Dict[str, Any]:
        """Create pipeline"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/pipelines",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise HarnessError(f"Request failed: {str(e)}")

    def get_deployments(self, **kwargs) -> Dict[str, Any]:
        """Get deployments"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/deployments",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise HarnessError(f"Request failed: {str(e)}")

    def create_deployment(self, **kwargs) -> Dict[str, Any]:
        """Create deployment"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/deployments",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise HarnessError(f"Request failed: {str(e)}")

    def get_services(self, **kwargs) -> Dict[str, Any]:
        """Get services"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/services",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise HarnessError(f"Request failed: {str(e)}")

    def create_service(self, **kwargs) -> Dict[str, Any]:
        """Create service"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/services",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise HarnessError(f"Request failed: {str(e)}")

