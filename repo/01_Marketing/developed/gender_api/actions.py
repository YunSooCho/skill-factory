"""Gender API Actions implementation."""
import requests
import time
from typing import Optional, Dict, Any
from .exceptions import (
    GenderAPIError,
    GenderAPIAuthenticationError,
    GenderAPIRateLimitError,
    GenderAPINotFoundError,
    GenderAPIValidationError,
)


class GenderAPIActions:
    """API actions for Gender API integration."""

    BASE_URL = "https://gender-api.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize API client.

        Args:
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
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

        # Add API key to params
        if params is None:
            params = {}
        params["key"] = self.api_key

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
                raise GenderAPIAuthenticationError(
                    message=error_data.get("errorMessage", "Authentication failed"),
                    status_code=401,
                    response=error_data,
                )
            elif response.status_code == 404:
                raise GenderAPINotFoundError(
                    message="Resource not found", status_code=404
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(method, endpoint, params, data, False)
                raise GenderAPIRateLimitError(
                    message="Rate limit exceeded", status_code=429
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise GenderAPIError(
                    message=error_data.get("errorMessage", f"API Error: {response.status_code}"),
                    status_code=response.status_code,
                    response=error_data,
                )

            return response.json()

        except requests.Timeout:
            raise GenderAPIError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise GenderAPIError(f"Request failed: {str(e)}")

    def get_account_stats(self, **kwargs) -> Dict[str, Any]:
        """
        Get account usage statistics.

        Returns:
            API response as dict with account stats
        """
        return self._make_request("GET", "/v2/account")

    def get_country_of_origin(self, **kwargs) -> Dict[str, Any]:
        """
        Get country of origin for a name.

        Args:
            name: First name to analyze
            country: (optional) ISO country code

        Returns:
            API response as dict with country origin data
        """
        return self._make_request("GET", "/v2/country", params=kwargs)

    def query_gender_by_first_name(self, **kwargs) -> Dict[str, Any]:
        """
        Query gender by first name.

        Args:
            name: First name to analyze
            country: (optional) ISO country code for better accuracy
            locale: (optional) Locale for improved accuracy

        Returns:
            API response as dict with gender prediction
        """
        return self._make_request("GET", "/v2/gender", params=kwargs)

    def close(self):
        """Close the session."""
        self.session.close()