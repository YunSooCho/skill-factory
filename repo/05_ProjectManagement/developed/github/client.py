"""
GitHub API Client - Version control and collaboration platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class GithubError(Exception):
    """Base exception for GitHub errors"""
    pass


class GithubRateLimitError(GithubError):
    """Rate limit exceeded"""
    pass


class GithubAuthenticationError(GithubError):
    """Authentication failed"""
    pass


class GithubClient:
    """Client for GitHub API"""

    BASE_URL = "https://api.github.com"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize GitHub client

        Args:
            access_token: GitHub OAuth access token
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
            raise GithubRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise GithubAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise GithubError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
    def get_repos(self, **kwargs) -> Dict[str, Any]:
        """Get repos"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/repos",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise GithubError(f"Request failed: {str(e)}")

    def create_repo(self, **kwargs) -> Dict[str, Any]:
        """Create repo"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/repos",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise GithubError(f"Request failed: {str(e)}")

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
            raise GithubError(f"Request failed: {str(e)}")

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
            raise GithubError(f"Request failed: {str(e)}")

    def get_pulls(self, **kwargs) -> Dict[str, Any]:
        """Get pulls"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/pulls",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise GithubError(f"Request failed: {str(e)}")

    def create_pull(self, **kwargs) -> Dict[str, Any]:
        """Create pull"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/pulls",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise GithubError(f"Request failed: {str(e)}")

    def get_users(self, **kwargs) -> Dict[str, Any]:
        """Get users"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/users",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise GithubError(f"Request failed: {str(e)}")

    def create_user(self, **kwargs) -> Dict[str, Any]:
        """Create user"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/users",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise GithubError(f"Request failed: {str(e)}")

