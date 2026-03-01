"""
Snack Prompt API Client - Element Search
"""

import requests
import time
from typing import Optional, Dict, Any, List


class SnackPromptError(Exception):
    """Base exception for Snack Prompt errors"""
    pass


class SnackPromptRateLimitError(SnackPromptError):
    """Rate limit exceeded"""
    pass


class SnackPromptAuthenticationError(SnackPromptError):
    """Authentication failed"""
    pass


class SnackPromptClient:
    """Client for Snack Prompt Element Search API"""

    BASE_URL = "https://api.snackprompt.com/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize Snack Prompt client

        Args:
            api_key: Snack Prompt API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        # Rate limiting
        self.min_delay = 0.1
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        """Enforce rate limiting between requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.min_delay:
            time.sleep(self.min_delay - time_since_last_request)

        self.last_request_time = time.time()

    def search_elementals(self, query: str,
                          category: Optional[str] = None,
                          tags: Optional[List[str]] = None,
                          limit: int = 20,
                          offset: int = 0,
                          **kwargs) -> Dict[str, Any]:
        """
        Search for elementals (prompt templates, UI elements, etc.)

        Args:
            query: Search query string
            category: Filter by category (optional)
            tags: Filter by tags (optional list)
            limit: Number of results to return (default: 20)
            offset: Number of results to skip (default: 0)
            **kwargs: Additional search parameters

        Returns:
            Dictionary containing search results

        Raises:
            SnackPromptError: If search fails
            SnackPromptRateLimitError: If rate limit exceeded
            SnackPromptAuthenticationError: If authentication fails
        """
        self._enforce_rate_limit()

        params = {
            'q': query,
            'limit': limit,
            'offset': offset
        }

        if category:
            params['category'] = category

        if tags:
            params['tags'] = ','.join(tags)

        params.update(kwargs)

        try:
            response = self.session.get(
                f'{self.BASE_URL}/elementals/search',
                params=params,
                timeout=self.timeout
            )

            # Handle rate limiting
            if response.status_code == 429:
                raise SnackPromptRateLimitError(
                    "Rate limit exceeded. Please try again later."
                )

            # Handle authentication errors
            if response.status_code == 401:
                raise SnackPromptAuthenticationError(
                    "Authentication failed. Please check your API key."
                )

            # Handle other errors
            if response.status_code >= 400:
                error_msg = response.text or response.reason
                raise SnackPromptError(
                    f"API request failed with status {response.status_code}: {error_msg}"
                )

            return response.json()

        except requests.exceptions.Timeout:
            raise SnackPromptError("Request timed out")

        except requests.exceptions.RequestException as e:
            raise SnackPromptError(f"Request failed: {str(e)}")

    def get_elemental(self, elemental_id: str) -> Dict[str, Any]:
        """
        Get details of a specific elemental

        Args:
            elemental_id: Elemental ID to retrieve

        Returns:
            Dictionary containing elemental details

        Raises:
            SnackPromptError: If request fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f'{self.BASE_URL}/elementals/{elemental_id}',
                timeout=self.timeout
            )

            if response.status_code == 401:
                raise SnackPromptAuthenticationError(
                    "Authentication failed. Please check your API key."
                )

            if response.status_code == 404:
                raise SnackPromptError("Elemental not found")

            if response.status_code >= 400:
                error_msg = response.text or response.reason
                raise SnackPromptError(
                    f"API request failed with status {response.status_code}: {error_msg}"
                )

            return response.json()

        except requests.exceptions.RequestException as e:
            raise SnackPromptError(f"Request failed: {str(e)}")

    def list_categories(self) -> Dict[str, Any]:
        """
        List all available categories

        Returns:
            Dictionary containing list of categories

        Raises:
            SnackPromptError: If request fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f'{self.BASE_URL}/categories',
                timeout=self.timeout
            )

            if response.status_code >= 400:
                error_msg = response.text or response.reason
                raise SnackPromptError(
                    f"API request failed with status {response.status_code}: {error_msg}"
                )

            return response.json()

        except requests.exceptions.RequestException as e:
            raise SnackPromptError(f"Request failed: {str(e)}")