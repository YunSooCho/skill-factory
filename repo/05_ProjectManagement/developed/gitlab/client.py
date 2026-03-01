"""
GitLab API Client - Git repository management and DevOps platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class GitlabError(Exception):
    """Base exception for GitLab errors"""
    pass


class GitlabRateLimitError(GitlabError):
    """Rate limit exceeded"""
    pass


class GitlabAuthenticationError(GitlabError):
    """Authentication failed"""
    pass


class GitlabClient:
    """Client for GitLab API"""

    BASE_URL = "https://gitlab.com/api/v4"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize GitLab client

        Args:
            access_token: GitLab OAuth access token
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
            raise GitlabRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise GitlabAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise GitlabError(f"API error ({response.status_code}): {error_msg}")

        return response.json()
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
            raise GitlabError(f"Request failed: {str(e)}")

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
            raise GitlabError(f"Request failed: {str(e)}")

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
            raise GitlabError(f"Request failed: {str(e)}")

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
            raise GitlabError(f"Request failed: {str(e)}")

    def get_merge_requests(self, **kwargs) -> Dict[str, Any]:
        """Get merge requests"""
        self._enforce_rate_limit()
        try:
            response = self.session.get(
                f"{self.BASE_URL}/merge_requests",
                params=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise GitlabError(f"Request failed: {str(e)}")

    def create_merge_request(self, **kwargs) -> Dict[str, Any]:
        """Create merge request"""
        self._enforce_rate_limit()
        try:
            response = self.session.post(
                f"{self.BASE_URL}/merge_requests",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise GitlabError(f"Request failed: {str(e)}")

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
            raise GitlabError(f"Request failed: {str(e)}")

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
            raise GitlabError(f"Request failed: {str(e)}")

