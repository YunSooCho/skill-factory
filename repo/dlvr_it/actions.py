"""DLVR.it API Actions implementation."""
import requests
import time
from typing import Optional, Dict, Any, List
from .exceptions import (
    DlvrItError,
    DlvrItAuthenticationError,
    DlvrItRateLimitError,
    DlvrItNotFoundError,
    DlvrItValidationError,
)


class DlvrItActions:
    """API actions for DLVR.it integration."""

    BASE_URL = "https://api.dlvr.it"

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize API client.

        Args:
            api_key: API key for authentication
            api_secret: API secret for authentication
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.timeout = timeout
        self.session = requests.Session()

        # Rate limiting state
        self.last_request_time = 0
        self.min_request_interval = 0.1
        self.rate_limit_remaining = 1000

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        retry_on_rate_limit: bool = True,
    ) -> Dict[str, Any]:
        """Make authenticated request with rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)

        url = f"{self.BASE_URL}{endpoint}"

        # Add authentication
        auth = (self.api_key, self.api_secret)

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                auth=auth,
                timeout=self.timeout,
            )
            self.last_request_time = time.time()

            if response.status_code == 401:
                error_data = response.json() if response.text else {}
                raise DlvrItAuthenticationError(
                    message=error_data.get("error", "Authentication failed"),
                    status_code=401,
                    response=error_data,
                )
            elif response.status_code == 404:
                raise DlvrItNotFoundError(
                    message="Resource not found", status_code=404
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(method, endpoint, params, data, False)
                raise DlvrItRateLimitError(
                    message="Rate limit exceeded", status_code=429
                )
            elif response.status_code == 422:
                error_data = response.json() if response.text else {}
                raise DlvrItValidationError(
                    message=error_data.get("error", "Validation error"),
                    status_code=422,
                    response=error_data,
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise DlvrItError(
                    message=error_data.get("error", f"API Error: {response.status_code}"),
                    status_code=response.status_code,
                    response=error_data,
                )

            return response.json()

        except requests.Timeout:
            raise DlvrItError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise DlvrItError(f"Request failed: {str(e)}")

    def create_post_to_account(self, **kwargs) -> Dict[str, Any]:
        """
        Create post to specific account.

        Args:
            account_id: Target account ID
            text: Post content/text
            media_urls: (optional) List of media URLs
            scheduled_at: (optional) Scheduled posting time

        Returns:
            API response as dict
        """
        return self._make_request("POST", "/api/v1/posts", data=kwargs)

    def create_post_to_route(self, **kwargs) -> Dict[str, Any]:
        """
        Create post to route (multiple accounts).

        Args:
            route_id: Target route ID
            text: Post content/text
            media_urls: (optional) List of media URLs
            scheduled_at: (optional) Scheduled posting time

        Returns:
            API response as dict
        """
        return self._make_request("POST", "/api/v1/posts/route", data=kwargs)

    def list_accounts(self, **kwargs) -> Dict[str, Any]:
        """
        List connected social media accounts.

        Args:
            limit: (optional) Maximum number of results
            offset: (optional) Offset for pagination

        Returns:
            API response as dict
        """
        return self._make_request("GET", "/api/v1/accounts", params=kwargs)

    def list_routes(self, **kwargs) -> Dict[str, Any]:
        """
        List routes (distribution paths).

        Args:
            limit: (optional) Maximum number of results
            offset: (optional) Offset for pagination

        Returns:
            API response as dict
        """
        return self._make_request("GET", "/api/v1/routes", params=kwargs)

    def close(self):
        """Close the session."""
        self.session.close()