"""Cuénote SMS API Actions implementation."""
import requests
import time
from typing import Optional, Dict, Any, List
from .exceptions import (
    CuenoteSMSError,
    CuenoteSMSAuthenticationError,
    CuenoteSMSRateLimitError,
    CuenoteSMSNotFoundError,
    CuenoteSMSValidationError,
)


class CuenoteSMSActions:
    """API actions for Cuénote SMS integration."""

    BASE_URL = "https://api.cuenote.jp/api/v1"

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

        # Add authentication headers
        headers = {
            "X-Cuenote-Api-Key": self.api_key,
            "X-Cuenote-Api-Secret": self.api_secret,
            "Content-Type": "application/json"
        }

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=headers,
                timeout=self.timeout,
            )
            self.last_request_time = time.time()

            if response.status_code == 401:
                error_data = response.json() if response.text else {}
                raise CuenoteSMSAuthenticationError(
                    message=error_data.get("error", "Authentication failed"),
                    status_code=401,
                    response=error_data,
                )
            elif response.status_code == 404:
                raise CuenoteSMSNotFoundError(
                    message="Resource not found", status_code=404
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(method, endpoint, params, data, False)
                raise CuenoteSMSRateLimitError(
                    message="Rate limit exceeded", status_code=429
                )
            elif response.status_code == 422:
                error_data = response.json() if response.text else {}
                raise CuenoteSMSValidationError(
                    message=error_data.get("error", "Validation error"),
                    status_code=422,
                    response=error_data,
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise CuenoteSMSError(
                    message=error_data.get("error", f"API Error: {response.status_code}"),
                    status_code=response.status_code,
                    response=error_data,
                )

            return response.json()

        except requests.Timeout:
            raise CuenoteSMSError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise CuenoteSMSError(f"Request failed: {str(e)}")

    def get_address_book(self, **kwargs) -> Dict[str, Any]:
        """
        Get address book details.

        Args:
            address_book_id: Address book ID

        Returns:
            API response as dict
        """
        address_book_id = kwargs.get("address_book_id")
        return self._make_request("GET", f"/address-books/{address_book_id}")

    def delete_address_book(self, **kwargs) -> Dict[str, Any]:
        """
        Delete address book.

        Args:
            address_book_id: Address book ID

        Returns:
            API response as dict
        """
        address_book_id = kwargs.get("address_book_id")
        return self._make_request("DELETE", f"/address-books/{address_book_id}")

    def update_sms_delivery_phone(self, **kwargs) -> Dict[str, Any]:
        """
        Update SMS delivery for phone numbers.

        Args:
            delivery_id: SMS delivery ID
            phone_numbers: List of phone numbers to update
            status: (optional) New status

        Returns:
            API response as dict
        """
        delivery_id = kwargs.get("delivery_id")
        return self._make_request("PUT", f"/sms-deliveries/{delivery_id}/phone-numbers", data=kwargs)

    def create_address_book(self, **kwargs) -> Dict[str, Any]:
        """
        Create address book.

        Args:
            name: Address book name
            description: (optional) Description

        Returns:
            API response as dict
        """
        return self._make_request("POST", "/address-books", data=kwargs)

    def list_address_books(self, **kwargs) -> Dict[str, Any]:
        """
        List address books.

        Args:
            limit: (optional) Maximum number of results
            offset: (optional) Offset for pagination

        Returns:
            API response as dict
        """
        return self._make_request("GET", "/address-books", params=kwargs)

    def get_delivery(self, **kwargs) -> Dict[str, Any]:
        """
        Get SMS delivery details.

        Args:
            delivery_id: SMS delivery ID

        Returns:
            API response as dict
        """
        delivery_id = kwargs.get("delivery_id")
        return self._make_request("GET", f"/sms-deliveries/{delivery_id}")

    def search_delivery(self, **kwargs) -> Dict[str, Any]:
        """
        Search SMS deliveries.

        Args:
            status: (optional) Filter by status
            start_date: (optional) Start date for filtering
            end_date: (optional) End date for filtering

        Returns:
            API response as dict
        """
        return self._make_request("GET", "/sms-deliveries", params=kwargs)

    def update_address_book(self, **kwargs) -> Dict[str, Any]:
        """
        Update address book.

        Args:
            address_book_id: Address book ID
            name: (optional) Updated name
            description: (optional) Updated description

        Returns:
            API response as dict
        """
        address_book_id = kwargs.get("address_book_id")
        return self._make_request("PUT", f"/address-books/{address_book_id}", data=kwargs)

    def create_sms_delivery_phone(self, **kwargs) -> Dict[str, Any]:
        """
        Create SMS delivery for phone numbers.

        Args:
            message: Message content
            phone_numbers: List of recipient phone numbers
            schedule: (optional) Scheduled delivery time

        Returns:
            API response as dict
        """
        return self._make_request("POST", "/sms-deliveries/phone-numbers", data=kwargs)

    def close(self):
        """Close the session."""
        self.session.close()