"""
DX Suite API Client - Digital transformation platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class DxSuiteError(Exception):
    """Base exception for DX Suite errors"""
    pass


class DxSuiteRateLimitError(DxSuiteError):
    """Rate limit exceeded"""
    pass


class DxSuiteAuthenticationError(DxSuiteError):
    """Authentication failed"""
    pass


class DxSuiteClient:
    """Client for DX Suite API"""

    BASE_URL = "https://api.dx-suite.com/v1"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize DX Suite client

        Args:
            access_token: DX Suite OAuth access token
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
            raise DxSuiteRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise DxSuiteAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise DxSuiteError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_workflows(self, **kwargs) -> Dict[str, Any]:
        """Get workflows"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/workflows",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise DxSuiteError(f"Request failed: {str(e)}")

    def create_workflow(self, **kwargs) -> Dict[str, Any]:
        """Create workflow"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/workflows",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise DxSuiteError(f"Request failed: {str(e)}")

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
            raise DxSuiteError(f"Request failed: {str(e)}")

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
            raise DxSuiteError(f"Request failed: {str(e)}")

    def get_tasks(self, **kwargs) -> Dict[str, Any]:
        """Get tasks"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/tasks",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise DxSuiteError(f"Request failed: {str(e)}")

    def create_task(self, **kwargs) -> Dict[str, Any]:
        """Create task"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/tasks",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise DxSuiteError(f"Request failed: {str(e)}")

