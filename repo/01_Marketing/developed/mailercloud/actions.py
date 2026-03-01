"""
MailerCloud Email API Actions implementation.
"""
import requests
import time
from typing import Optional, List, Dict, Any
from .exceptions import (
    MailercloudError,
    MailercloudAuthenticationError,
    MailercloudRateLimitError,
    MailercloudNotFoundError,
    MailercloudValidationError,
)


class MailercloudActions:
    """API actions for integration."""

    BASE_URL = "https://cloudapi.mailercloud.com/api"

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
                raise MailercloudAuthenticationError(
                    message=error_data.get("message", "Authentication failed"),
                    status_code=401,
                    response=error_data,
                )
            elif response.status_code == 404:
                raise MailercloudNotFoundError(
                    message="Resource not found", status_code=404
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(method, endpoint, params, data, False)
                raise MailercloudRateLimitError(
                    message="Rate limit exceeded", status_code=429
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise MailercloudError(
                    message=error_data.get("message", f"API Error: {response.status_code}"),
                    status_code=response.status_code,
                    response=error_data,
                )

            return response.json()

        except requests.Timeout:
            raise MailercloudError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise MailercloudError(f"Request failed: {str(e)}")


    def add_contact(self, **kwargs) -> Dict[str, Any]:
        """
        add_contact - POST request.
        
        Returns:
            API response as dict
        """
        return self._make_request("POST", "/add_contact", data=kwargs if "POST" in ["POST", "PUT", "PATCH"] else None, params=kwargs if "POST" in ["GET", "DELETE"] else None)

    def send_email(self, **kwargs) -> Dict[str, Any]:
        """
        send_email - POST request.
        
        Returns:
            API response as dict
        """
        return self._make_request("POST", "/send_email", data=kwargs if "POST" in ["POST", "PUT", "PATCH"] else None, params=kwargs if "POST" in ["GET", "DELETE"] else None)

    def close(self):
        """Close the session."""
        self.session.close()
