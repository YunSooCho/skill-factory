"""
Rd Station API Actions implementation.
"""
import requests
import time
from typing import Optional, List, Dict, Any
from .exceptions import (
    RdStationError,
    RdStationAuthenticationError,
    RdStationRateLimitError,
    RdStationNotFoundError,
    RdStationValidationError,
)


class RdStationActions:
    """API actions for integration."""

    BASE_URL = "https://api.rd.services"

    def __init__(self, access_token: Optional[str] = None, timeout: int = 30):
        """
        Initialize API client with OAuth access token.

        Args:
            access_token: OAuth access token for authentication
            timeout: Request timeout in seconds
        """
        self.access_token = access_token
        self.timeout = timeout
        self.session = requests.Session()
        if self.access_token:
            self.session.headers.update({
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            })

        # Rate limiting configuration
        self.last_request_time = 0
        self.min_request_interval = 0.2
        self.rate_limit_remaining = 500

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        retry_on_rate_limit: bool = True,
    ) -> Dict[str, Any]:
        """Make authenticated request with rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)

        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self.timeout,
            )
            self.last_request_time = time.time()

            if response.status_code == 401:
                error_data = response.json() if response.text else {}
                raise RdStationAuthenticationError(
                    message=error_data.get("error", "Authentication failed"),
                    status_code=401,
                    response=error_data,
                )
            elif response.status_code == 404:
                raise RdStationNotFoundError(
                    message="Resource not found", status_code=404
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(method, endpoint, params, json_data, False)
                raise RdStationRateLimitError(
                    message="Rate limit exceeded", status_code=429
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise RdStationError(
                    message=error_data.get("error", f"API Error: {response.status_code}"),
                    status_code=response.status_code,
                    response=error_data,
                )

            return response.json()

        except requests.Timeout:
            raise RdStationError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise RdStationError(f"Request failed: {str(e)}")

    # API Actions

    def create_lead(self, **kwargs) -> Dict[str, Any]:
        """
        Create a new lead in Rd Station.

        Returns:
            Created lead object
        """
        return self._make_request("POST", "/platform/contacts", json_data=kwargs)

    def update_lead(self, uuid: str, **kwargs) -> Dict[str, Any]:
        """
        Update an existing lead in Rd Station.

        Args:
            uuid: Lead UUID
            **kwargs: Lead fields to update

        Returns:
            Updated lead object
        """
        return self._make_request("PATCH", f"/platform/contacts/{uuid}", json_data=kwargs)

    def get_lead(self, uuid: str) -> Dict[str, Any]:
        """
        Get a lead by UUID.

        Args:
            uuid: Lead UUID

        Returns:
            Lead object
        """
        return self._make_request("GET", f"/platform/contacts/{uuid}")

    def get_conversions(self, event_identifier: str, limit: int = 100, page: int = 1) -> Dict[str, Any]:
        """
        Get conversion data for an event.

        Args:
            event_identifier: Event identifier
            limit: Number of results per page
            page: Page number

        Returns:
            Conversion data
        """
        params = {"event_identifier": event_identifier, "limit": limit, "page": page}
        return self._make_request("GET", "/platform/analytics/conversions", params=params)

    def track_conversion(self, event_uuid: str, email: str, **kwargs) -> Dict[str, Any]:
        """
        Track a conversion event.

        Args:
            event_uuid: Event UUID
            email: Lead email
            **kwargs: Additional conversion data

        Returns:
            Conversion result
        """
        data = {"event_uuid": event_uuid, "email": email, **kwargs}
        return self._make_request("POST", "/platform/events/conversions", json_data=data)

    def close(self):
        """Close the session."""
        self.session.close()