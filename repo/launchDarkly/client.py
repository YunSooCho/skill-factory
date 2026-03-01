"""
LaunchDarkly API Client - Feature flag management platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class LaunchDarklyError(Exception):
    """Base exception for LaunchDarkly errors"""
    pass


class LaunchDarklyRateLimitError(LaunchDarklyError):
    """Rate limit exceeded"""
    pass


class LaunchDarklyAuthenticationError(LaunchDarklyError):
    """Authentication failed"""
    pass


class LaunchDarklyClient:
    """Client for LaunchDarkly API"""

    BASE_URL = "https://api.launchdarkly.com/api/v2"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize LaunchDarkly client

        Args:
            access_token: LaunchDarkly API key
            timeout: Request timeout in seconds
        """
        self.access_token = access_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'{access_token}',
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
            raise LaunchDarklyRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise LaunchDarklyAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise LaunchDarklyError(f"API error ({response.status_code}): {error_msg}")

        # LaunchDarkly returns items directly, wrap in dict for consistency
        try:
            return response.json()
        except:
            return {}

    def get_flags(self, project_key: str, environment_key: Optional[str] = None) -> Dict[str, Any]:
        """Get feature flags"""
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/flags/{project_key}"
        if environment_key:
            url += f"?environmentKey={environment_key}"

        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LaunchDarklyError(f"Request failed: {str(e)}")

    def get_flag(self, project_key: str, flag_key: str,
                 environment_key: Optional[str] = None) -> Dict[str, Any]:
        """Get specific feature flag"""
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/flags/{project_key}/{flag_key}"
        if environment_key:
            url += f"?environmentKey={environment_key}"

        try:
            response = self.session.get(url, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LaunchDarklyError(f"Request failed: {str(e)}")

    def create_flag(self, project_key: str, flag_key: str, **kwargs) -> Dict[str, Any]:
        """Create feature flag"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/flags/{project_key}/{flag_key}",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LaunchDarklyError(f"Request failed: {str(e)}")

    def update_flag(self, project_key: str, flag_key: str,
                    patch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update feature flag"""
        self._enforce_rate_limit()
        try:
            response = self.session.patch(
                f"{self.BASE_URL}/flags/{project_key}/{flag_key}",
                json=patch,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LaunchDarklyError(f"Request failed: {str(e)}")

    def delete_flag(self, project_key: str, flag_key: str) -> Dict[str, Any]:
        """Delete feature flag"""
        self._enforce_rate_limit()
        try:
            response = self.session.delete(
                f"{self.BASE_URL}/flags/{project_key}/{flag_key}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LaunchDarklyError(f"Request failed: {str(e)}")

    def get_projects(self) -> Dict[str, Any]:
        """Get all projects"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/projects",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LaunchDarklyError(f"Request failed: {str(e)}")

    def get_project(self, project_key: str) -> Dict[str, Any]:
        """Get project details"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/projects/{project_key}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LaunchDarklyError(f"Request failed: {str(e)}")

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
            raise LaunchDarklyError(f"Request failed: {str(e)}")

    def get_environments(self, project_key: str) -> Dict[str, Any]:
        """Get environments in project"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/projects/{project_key}/environments",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise LaunchDarklyError(f"Request failed: {str(e)}")