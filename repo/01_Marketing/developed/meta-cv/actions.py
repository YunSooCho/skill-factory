"""Meta CV (Conversion API) Actions implementation."""
import requests
import time
from typing import Optional, Dict, Any, List
from .exceptions import (
    MetaCVError,
    MetaCVAuthenticationError,
    MetaCVRateLimitError,
    MetaCVNotFoundError,
    MetaCVValidationError,
)


class MetaCVActions:
    """API actions for Meta CV (Facebook Conversion API) integration."""

    BASE_URL = "https://graph.facebook.com/v19.0"

    def __init__(
        self,
        pixel_id: Optional[str] = None,
        access_token: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize API client.

        Args:
            pixel_id: Facebook Pixel ID
            access_token: Access token for authentication
            timeout: Request timeout in seconds
        """
        self.pixel_id = pixel_id
        self.access_token = access_token
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

        # Add access token to params
        if params is None:
            params = {}
        params["access_token"] = self.access_token

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=self.timeout,
            )
            self.last_request_time = time.time()

            if response.status_code == 401:
                error_data = response.json() if response.text else {}
                raise MetaCVAuthenticationError(
                    message=error_data.get("error", {}).get("message", "Authentication failed"),
                    status_code=401,
                    response=error_data,
                )
            elif response.status_code == 404:
                raise MetaCVNotFoundError(
                    message="Resource not found", status_code=404
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(method, endpoint, params, data, False)
                raise MetaCVRateLimitError(
                    message="Rate limit exceeded", status_code=429
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise MetaCVError(
                    message=error_data.get("error", {}).get("message", f"API Error: {response.status_code}"),
                    status_code=response.status_code,
                    response=error_data,
                )

            return response.json()

        except requests.Timeout:
            raise MetaCVError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise MetaCVError(f"Request failed: {str(e)}")

    def send_conversion_event_deprecated(self, **kwargs) -> Dict[str, Any]:
        """
        Send conversion event (deprecated method).

        Args:
            event_name: Name of the conversion event
            event_time: Unix timestamp of event
            user_data: User data object (email, phone, etc.)
            custom_data: Custom event data
            event_source_url: URL where event occurred
            action_source: Source of action (website, app, etc.)
            test_event_code: (optional) Test event code for verification

        Returns:
            API response as dict
        """
        pixel_id = kwargs.get("pixel_id", self.pixel_id)
        endpoint = f"/{pixel_id}/events"

        return self._make_request("POST", endpoint, data=kwargs)

    def send_conversion_event(self, **kwargs) -> Dict[str, Any]:
        """
        Send conversion event.

        Args:
            data: Array of event objects or single event object
            test_event_code: (optional) Test event code for verification
            partner_agent: (optional) Partner agent identifier

        Returns:
            API response as dict
        """
        pixel_id = kwargs.get("pixel_id", self.pixel_id)
        endpoint = f"/{pixel_id}/events"

        # Handle multiple events in batch
        if "events" in kwargs:
            payload = kwargs
        else:
            # Single event
            payload = {"data": [kwargs]}

        return self._make_request("POST", endpoint, data=payload)

    def close(self):
        """Close the session."""
        self.session.close()