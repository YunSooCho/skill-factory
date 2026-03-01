"""
Google Business Profile API Actions implementation.
"""
import requests
import time
from typing import Optional, List, Dict, Any
from .exceptions import (
    GoogleBusinessProfileError,
    GoogleBusinessProfileAuthenticationError,
    GoogleBusinessProfileRateLimitError,
    GoogleBusinessProfileNotFoundError,
    GoogleBusinessProfileValidationError,
)


class GoogleBusinessProfileActions:
    """API actions for integration."""

    BASE_URL = "https://mybusiness.googleapis.com/v4"

    def __init__(self, api_key: Optional[str] = None, access_token: Optional[str] = None, timeout: int = 30):
        """
        Initialize API client.

        Args:
            api_key: API key for authentication
            access_token: OAuth access token
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.access_token = access_token
        self.timeout = timeout
        self.session = requests.Session()
        headers = {"Content-Type": "application/json"}
        headers.update({
            "Authorization": f"Bearer {{self.access_token}}",
        })
        self.session.headers.update(headers)

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
                raise GoogleBusinessProfileAuthenticationError(
                    message=error_data.get("message", "Authentication failed"),
                    status_code=401,
                    response=error_data,
                )
            elif response.status_code == 404:
                raise GoogleBusinessProfileNotFoundError(
                    message="Resource not found", status_code=404
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(method, endpoint, params, data, False)
                raise GoogleBusinessProfileRateLimitError(
                    message="Rate limit exceeded", status_code=429
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise GoogleBusinessProfileError(
                    message=error_data.get("message", f"API Error: {response.status_code}"),
                    status_code=response.status_code,
                    response=error_data,
                )

            return response.json()

        except requests.Timeout:
            raise GoogleBusinessProfileError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise GoogleBusinessProfileError(f"Request failed: {str(e)}")


    def get_business_info(self, **kwargs) -> Dict[str, Any]:
        """
        get_business_info - GET request.
        
        Returns:
            API response as dict
        """
        return self._make_request("GET", "/get_business_info", data=kwargs if "GET" in ["POST", "PUT", "PATCH"] else None, params=kwargs if "GET" in ["GET", "DELETE"] else None)

    def get_reviews(self, **kwargs) -> Dict[str, Any]:
        """
        get_reviews - GET request.
        
        Returns:
            API response as dict
        """
        return self._make_request("GET", "/get_reviews", data=kwargs if "GET" in ["POST", "PUT", "PATCH"] else None, params=kwargs if "GET" in ["GET", "DELETE"] else None)

    def close(self):
        """Close the session."""
        self.session.close()
