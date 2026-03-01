"""
GetResponse Email Marketing API Actions implementation.
"""
import requests
import time
from typing import Optional, List, Dict, Any
from .exceptions import (
    GetresponseApiError,
    GetresponseApiAuthenticationError,
    GetresponseApiRateLimitError,
    GetresponseApiNotFoundError,
    GetresponseApiValidationError,
)


class GetresponseApiActions:
    """API actions for integration."""

    BASE_URL = "https://api.getresponse.com/v3"

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
            "X-API-Key": self.api_key,
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
                raise GetresponseApiAuthenticationError(
                    message=error_data.get("message", "Authentication failed"),
                    status_code=401,
                    response=error_data,
                )
            elif response.status_code == 404:
                raise GetresponseApiNotFoundError(
                    message="Resource not found", status_code=404
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(method, endpoint, params, data, False)
                raise GetresponseApiRateLimitError(
                    message="Rate limit exceeded", status_code=429
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise GetresponseApiError(
                    message=error_data.get("message", f"API Error: {response.status_code}"),
                    status_code=response.status_code,
                    response=error_data,
                )

            return response.json()

        except requests.Timeout:
            raise GetresponseApiError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise GetresponseApiError(f"Request failed: {str(e)}")


    def get_contact_lists(self, **kwargs) -> Dict[str, Any]:
        """
        get_contact_lists - GET request.
        
        Returns:
            API response as dict
        """
        return self._make_request("GET", "/get_contact_lists", data=kwargs if "GET" in ["POST", "PUT", "PATCH"] else None, params=kwargs if "GET" in ["GET", "DELETE"] else None)

    def get_newsletters(self, **kwargs) -> Dict[str, Any]:
        """
        get_newsletters - GET request.
        
        Returns:
            API response as dict
        """
        return self._make_request("GET", "/get_newsletters", data=kwargs if "GET" in ["POST", "PUT", "PATCH"] else None, params=kwargs if "GET" in ["GET", "DELETE"] else None)

    def delete_contact(self, **kwargs) -> Dict[str, Any]:
        """
        delete_contact - DELETE request.
        
        Returns:
            API response as dict
        """
        return self._make_request("DELETE", "/delete_contact", data=kwargs if "DELETE" in ["POST", "PUT", "PATCH"] else None, params=kwargs if "DELETE" in ["GET", "DELETE"] else None)

    def get_contact(self, **kwargs) -> Dict[str, Any]:
        """
        get_contact - GET request.
        
        Returns:
            API response as dict
        """
        return self._make_request("GET", "/get_contact", data=kwargs if "GET" in ["POST", "PUT", "PATCH"] else None, params=kwargs if "GET" in ["GET", "DELETE"] else None)

    def create_contact(self, **kwargs) -> Dict[str, Any]:
        """
        create_contact - POST request.
        
        Returns:
            API response as dict
        """
        return self._make_request("POST", "/create_contact", data=kwargs if "POST" in ["POST", "PUT", "PATCH"] else None, params=kwargs if "POST" in ["GET", "DELETE"] else None)

    def create_newsletter(self, **kwargs) -> Dict[str, Any]:
        """
        create_newsletter - POST request.
        
        Returns:
            API response as dict
        """
        return self._make_request("POST", "/create_newsletter", data=kwargs if "POST" in ["POST", "PUT", "PATCH"] else None, params=kwargs if "POST" in ["GET", "DELETE"] else None)

    def update_contact(self, **kwargs) -> Dict[str, Any]:
        """
        update_contact - PUT request.
        
        Returns:
            API response as dict
        """
        return self._make_request("PUT", "/update_contact", data=kwargs if "PUT" in ["POST", "PUT", "PATCH"] else None, params=kwargs if "PUT" in ["GET", "DELETE"] else None)

    def close(self):
        """Close the session."""
        self.session.close()
