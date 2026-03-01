"""
Scraptio API Client - Web Scraping Service
"""

import requests
import time
from typing import Optional, Dict, Any, List


class ScraptioError(Exception):
    """Base exception for Scraptio errors"""
    pass


class ScraptioRateLimitError(ScraptioError):
    """Rate limit exceeded"""
    pass


class ScraptioAuthenticationError(ScraptioError):
    """Authentication failed"""
    pass


class ScraptioClient:
    """Client for Scraptio Web Scraping API"""

    BASE_URL = "https://api.scraptio.com/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize Scraptio client

        Args:
            api_key: Scraptio API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        # Rate limiting: minimum delay between requests
        self.min_delay = 0.1  # 100ms
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        """Enforce rate limiting between requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.min_delay:
            time.sleep(self.min_delay - time_since_last_request)

        self.last_request_time = time.time()

    def scrape_url(self, url: str,
                   wait: Optional[int] = None,
                   css_selectors: Optional[Dict[str, str]] = None,
                   extract_emails: bool = False,
                   extract_links: bool = False,
                   extract_texts: bool = True,
                   **kwargs) -> Dict[str, Any]:
        """
        Scrape a URL and extract data

        Args:
            url: URL to scrape
            wait: Wait time before scraping in milliseconds
            css_selectors: Dict of field names to CSS selectors for targeted extraction
            extract_emails: Extract email addresses
            extract_links: Extract links
            extract_texts: Extract text content
            **kwargs: Additional parameters

        Returns:
            Dictionary containing scraped data

        Raises:
            ScraptioError: If scraping fails
            ScraptioRateLimitError: If rate limit exceeded
            ScraptioAuthenticationError: If authentication fails
        """
        self._enforce_rate_limit()

        payload = {
            'url': url,
            'extract_emails': extract_emails,
            'extract_links': extract_links,
            'extract_texts': extract_texts
        }

        if wait:
            payload['wait'] = wait

        if css_selectors:
            payload['css_selectors'] = css_selectors

        payload.update(kwargs)

        try:
            response = self.session.post(
                f'{self.BASE_URL}/scrape',
                json=payload,
                timeout=self.timeout
            )

            # Handle rate limiting
            if response.status_code == 429:
                raise ScraptioRateLimitError(
                    "Rate limit exceeded. Please try again later."
                )

            # Handle authentication errors
            if response.status_code == 401:
                raise ScraptioAuthenticationError(
                    "Authentication failed. Please check your API key."
                )

            # Handle other errors
            if response.status_code >= 400:
                error_msg = response.text or response.reason
                raise ScraptioError(
                    f"API request failed with status {response.status_code}: {error_msg}"
                )

            return response.json()

        except requests.exceptions.Timeout:
            raise ScraptioError("Request timed out")

        except requests.exceptions.RequestException as e:
            raise ScraptioError(f"Request failed: {str(e)}")

    def get_scrape_result(self, scrape_id: str) -> Dict[str, Any]:
        """
        Get results of a scrape operation

        Args:
            scrape_id: ID of the scrape operation

        Returns:
            Dictionary containing scrape results

        Raises:
            ScraptioError: If getting results fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f'{self.BASE_URL}/scrape/{scrape_id}',
                timeout=self.timeout
            )

            if response.status_code == 401:
                raise ScraptioAuthenticationError(
                    "Authentication failed. Please check your API key."
                )

            if response.status_code >= 400:
                error_msg = response.text or response.reason
                raise ScraptioError(
                    f"API request failed with status {response.status_code}: {error_msg}"
                )

            return response.json()

        except requests.exceptions.RequestException as e:
            raise ScraptioError(f"Request failed: {str(e)}")

    def list_scrapes(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """
        List recent scrape operations

        Args:
            limit: Number of results to return
            offset: Number of results to skip

        Returns:
            Dictionary containing list of scrapes

        Raises:
            ScraptioError: If listing scrapes fails
        """
        self._enforce_rate_limit()

        params = {
            'limit': limit,
            'offset': offset
        }

        try:
            response = self.session.get(
                f'{self.BASE_URL}/scrapes',
                params=params,
                timeout=self.timeout
            )

            if response.status_code == 401:
                raise ScraptioAuthenticationError(
                    "Authentication failed. Please check your API key."
                )

            if response.status_code >= 400:
                error_msg = response.text or response.reason
                raise ScraptioError(
                    f"API request failed with status {response.status_code}: {error_msg}"
                )

            return response.json()

        except requests.exceptions.RequestException as e:
            raise ScraptioError(f"Request failed: {str(e)}")