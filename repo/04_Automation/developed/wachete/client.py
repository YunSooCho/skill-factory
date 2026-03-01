"""
Wachete API Client - Web Page Monitoring
"""

import requests
import time
from typing import Optional, Dict, Any, List


class WacheteError(Exception):
    """Base exception for Wachete errors"""
    pass


class WacheteRateLimitError(WacheteError):
    """Rate limit exceeded"""
    pass


class WacheteAuthenticationError(WacheteError):
    """Authentication failed"""
    pass


class WacheteClient:
    """Client for Wachete Web Page Monitoring API"""

    BASE_URL = "https://api.wachete.com/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize Wachete client

        Args:
            api_key: Wachete API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
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
            raise WacheteRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise WacheteAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', or error_data.get('error', ''))
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise WacheteError(f"API error ({response.status_code}): {error_msg}")

        return response.json()

    def create_wachet(self, url: str, name: str,
                      check_interval: int = 3600,
                      email_notification: bool = False,
                      **kwargs) -> Dict[str, Any]:
        """
        Create or update a wachet (web monitoring task)

        Args:
            url: URL to monitor
            name: Wachet name
            check_interval: Check interval in seconds (default: 3600)
            email_notification: Enable email notifications (default: False)
            **kwargs: Additional parameters

        Returns:
            Dictionary containing wachet details

        Raises:
            WacheteError: If creation fails
        """
        self._enforce_rate_limit()

        payload = {
            "url": url,
            "name": name,
            "check_interval": check_interval,
            "email_notification": email_notification
        }
        payload.update(kwargs)

        try:
            response = self.session.post(
                f"{self.BASE_URL}/wachets",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise WacheteError(f"Request failed: {str(e)}")

    def update_wachet(self, wachet_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update an existing wachet

        Args:
            wachet_id: Wachet ID to update
            **kwargs: Fields to update

        Returns:
            Dictionary containing updated wachet details

        Raises:
            WacheteError: If update fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.put(
                f"{self.BASE_URL}/wachets/{wachet_id}",
                json=kwargs,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise WacheteError(f"Request failed: {str(e)}")

    def get_wachet(self, wachet_id: str) -> Dict[str, Any]:
        """
        Get details of a wachet

        Args:
            wachet_id: Wachet ID to retrieve

        Returns:
            Dictionary containing wachet details

        Raises:
            WacheteError: If request fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/wachets/{wachet_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise WacheteError(f"Request failed: {str(e)}")

    def search_wachets(self, limit: int = 20, offset: int = 0,
                       status: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for wachets

        Args:
            limit: Number of results
            offset: Pagination offset
            status: Filter by status (optional)

        Returns:
            Dictionary containing wachet search results

        Raises:
            WacheteError: If search fails
        """
        self._enforce_rate_limit()

        params = {"limit": limit, "offset": offset}

        if status:
            params["status"] = status

        try:
            response = self.session.get(
                f"{self.BASE_URL}/wachets",
                params=params,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise WacheteError(f"Request failed: {str(e)}")

    def delete_wachet(self, wachet_id: str) -> Dict[str, Any]:
        """
        Delete a wachet

        Args:
            wachet_id: Wachet ID to delete

        Returns:
            Dictionary containing delete confirmation

        Raises:
            WacheteError: If deletion fails
        """
        self._enforce_rate_limit()

        try:
            response = self.session.delete(
                f"{self.BASE_URL}/wachets/{wachet_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise WacheteError(f"Request failed: {str(e)}")

    def get_wachet_changes(self, wachet_id: str, limit: int = 20) -> Dict[str, Any]:
        """
        Get changes detected for a wachet

        Args:
            wachet_id: Wachet ID
            limit: Number of changes to retrieve

        Returns:
            Dictionary containing change history

        Raises:
            WacheteError: If request fails
        """
        self._enforce_rate_limit()

        params = {"limit": limit}

        try:
            response = self.session.get(
                f"{self.BASE_URL}/wachets/{wachet_id}/changes",
                params=params,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise WacheteError(f"Request failed: {str(e)}")