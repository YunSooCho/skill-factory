"""BurstSMS API Actions implementation."""
import requests
import time
from typing import Optional, Dict, Any, List
from .exceptions import (
    BurstSMSError,
    BurstSMSAuthenticationError,
    BurstSMSRateLimitError,
    BurstSMSNotFoundError,
    BurstSMSValidationError,
)


class BurstSMSActions:
    """API actions for BurstSMS integration."""

    BASE_URL = "https://api.transmitsms.com"

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

        # Add authentication to params
        auth_params = {"api_key": self.api_key, "api_secret": self.api_secret}
        if params is None:
            params = {}
        params.update(auth_params)

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
                raise BurstSMSAuthenticationError(
                    message=error_data.get("error", "Authentication failed"),
                    status_code=401,
                    response=error_data,
                )
            elif response.status_code == 404:
                raise BurstSMSNotFoundError(
                    message="Resource not found", status_code=404
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(method, endpoint, params, data, False)
                raise BurstSMSRateLimitError(
                    message="Rate limit exceeded", status_code=429
                )
            elif response.status_code == 422:
                error_data = response.json() if response.text else {}
                raise BurstSMSValidationError(
                    message=error_data.get("error", "Validation error"),
                    status_code=422,
                    response=error_data,
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise BurstSMSError(
                    message=error_data.get("error", f"API Error: {response.status_code}"),
                    status_code=response.status_code,
                    response=error_data,
                )

            return response.json()

        except requests.Timeout:
            raise BurstSMSError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise BurstSMSError(f"Request failed: {str(e)}")

    def send_sms(self, **kwargs) -> Dict[str, Any]:
        """
        Send SMS message.

        Args:
            to: Recipient phone number
            from_: Sender ID or phone number
            message: Message content
            schedule: (optional) Scheduled delivery time
            reference: (optional) Custom reference ID

        Returns:
            API response as dict
        """
        return self._make_request(
            "GET",
            "/send-sms.json",
            params=kwargs
        )

    def list_related_messages(self, **kwargs) -> Dict[str, Any]:
        """
        List related messages.

        Args:
            message_id: Original message ID to find related messages
            limit: (optional) Maximum number of results
            offset: (optional) Offset for pagination

        Returns:
            API response as dict
        """
        return self._make_request(
            "GET",
            "/get-sms.json",
            params=kwargs
        )

    def retrieve_messages(self, **kwargs) -> Dict[str, Any]:
        """
        Retrieve message details.

        Args:
            message_id: Message ID to retrieve
            start_date: (optional) Start date for filtering
            end_date: (optional) End date for filtering
            limit: (optional) Maximum number of results
            offset: (optional) Offset for pagination
            page: (optional) Page number

        Returns:
            API response as dict
        """
        return self._make_request(
            "GET",
            "/get-sms.json",
            params=kwargs
        )

    def close(self):
        """Close the session."""
        self.session.close()