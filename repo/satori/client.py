"""
Satori API Client Implementation

Provides methods for:
- Register Customer: Create new customer
- Register or Update Customer: Create or update customer
- Register Customer Action: Log customer action/event
- Delete Customer: Remove customer
"""

import requests
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class RateLimiter:
    """Rate limiter for API requests"""
    max_requests: int = 300  # Maximum requests per time window
    time_window: int = 60  # Time window in seconds
    requests: list = None

    def __post_init__(self):
        if self.requests is None:
            self.requests = []

    def wait_if_needed(self):
        """Wait if rate limit has been reached"""
        now = time.time()
        # Remove requests outside the time window
        self.requests = [r for r in self.requests if now - r < self.time_window]

        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
                # Clean up old requests after waiting
                self.requests = []

        # Add current request
        self.requests.append(now)


class SatoriError(Exception):
    """Base exception for Satori API errors"""
    pass


class AuthenticationError(SatoriError):
    """Raised when authentication fails"""
    pass


class RateLimitError(SatoriError):
    """Raised when rate limit is exceeded"""
    pass


class InvalidRequestError(SatoriError):
    """Raised when request parameters are invalid"""
    pass


class APIError(SatoriError):
    """Raised for general API errors"""
    pass


class SatoriClient:
    """
    Satori API Client

    API for customer management and action tracking.
    """

    BASE_URL = "https://api.satori.com"

    def __init__(self, api_key: str, timeout: int = 30, max_retries: int = 3):
        """
        Initialize Satori client

        Args:
            api_key: Your Satori API key
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limiter = RateLimiter(max_requests=300, time_window=60)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Satori API

        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            Response data as dictionary

        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            InvalidRequestError: If request parameters are invalid
            APIError: For other API errors
        """
        self.rate_limiter.wait_if_needed()

        url = f"{self.BASE_URL}{endpoint}"
        last_error = None

        for attempt in range(self.max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    timeout=self.timeout
                )

                # Handle specific status codes
                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key or authentication failed")
                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    raise RateLimitError(f"Rate limit exceeded. Retry after {retry_after} seconds")
                elif response.status_code == 400:
                    error_data = response.json() if response.content else {}
                    raise InvalidRequestError(f"Invalid request: {error_data.get('message', 'Unknown error')}")
                elif response.status_code == 404:
                    raise InvalidRequestError("Resource not found")
                elif response.status_code >= 500:
                    error_data = response.json() if response.content else {}
                    raise APIError(f"Server error: {error_data.get('message', 'Unknown error')}")

                response.raise_for_status()

                return response.json()

            except requests.Timeout:
                last_error = f"Request timeout after {self.timeout} seconds"
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise APIError(last_error)

            except requests.RequestException as e:
                last_error = str(e)
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise APIError(f"Request failed: {last_error}")

        raise APIError(f"Max retries exceeded: {last_error}")

    def register_customer(
        self,
        customer_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Register a new customer

        Args:
            customer_id: Unique customer identifier (required)
            name: Customer name
            email: Customer email
            phone: Customer phone number
            properties: Additional customer properties as key-value pairs

        Returns:
            Dictionary containing:
                - customer_id: Customer ID
                - created: Timestamp of creation
                - status: Success status

        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If customer_id is missing
            APIError: For other API errors

        Example:
            >>> client = SatoriClient(api_key="your-api-key")
            >>> result = client.register_customer(
            ...     customer_id="cust123",
            ...     name="John Doe",
            ...     email="john@example.com"
            ... )
            >>> print(f"Customer created at {result['created']}")
        """
        if not customer_id:
            raise InvalidRequestError("customer_id is required")

        data = {"customer_id": customer_id}

        if name:
            data["name"] = name
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if properties:
            data["properties"] = properties

        return self._make_request("POST", "/customers", data=data)

    def register_or_update_customer(
        self,
        customer_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Register a new customer or update an existing customer

        If the customer already exists, it will be updated with the provided data.

        Args:
            customer_id: Unique customer identifier (required)
            name: Customer name
            email: Customer email
            phone: Customer phone number
            properties: Additional customer properties (merged with existing)

        Returns:
            Dictionary containing:
                - customer_id: Customer ID
                - created: If new customer, creation timestamp
                - updated: If existing customer, update timestamp
                - status: Success status

        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If customer_id is missing
            APIError: For other API errors

        Example:
            >>> client = SatoriClient(api_key="your-api-key")
            >>> result = client.register_or_update_customer(
            ...     customer_id="cust123",
            ...     email="john@example.com",
            ...     properties={"plan": "pro"}
            ... )
            >>> if 'created' in result:
            ...     print("New customer created")
            >>> else:
            ...     print("Customer updated")
        """
        if not customer_id:
            raise InvalidRequestError("customer_id is required")

        data = {"customer_id": customer_id}

        if name:
            data["name"] = name
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if properties:
            data["properties"] = properties

        return self._make_request("PUT", "/customers", data=data)

    def register_customer_action(
        self,
        customer_id: str,
        action_name: str,
        action_value: Optional[Any] = None,
        action_properties: Optional[Dict[str, Any]] = None,
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register a customer action/event

        Track customer behavior, events, or custom actions for analytics and automation.

        Args:
            customer_id: Customer identifier (required)
            action_name: Name of the action/event (required)
            action_value: Optional value associated with the action
            action_properties: Additional properties for the action
            timestamp: ISO 8601 timestamp (defaults to current time)

        Returns:
            Dictionary containing:
                - action_id: Action ID
                - customer_id: Customer ID
                - action_name: Action name
                - recorded_at: Timestamp when action was recorded

        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If customer_id or action_name is missing
            APIError: For other API errors

        Example:
            >>> client = SatoriClient(api_key="your-api-key")
            >>> result = client.register_customer_action(
            ...     customer_id="cust123",
            ...     action_name="purchase",
            ...     action_value=99.99,
            ...     action_properties={"product_id": "prod456"}
            ... )
            >>> print(f"Action registered: {result['action_id']}")
        """
        if not customer_id:
            raise InvalidRequestError("customer_id is required")
        if not action_name:
            raise InvalidRequestError("action_name is required")

        data = {
            "customer_id": customer_id,
            "action_name": action_name
        }

        if action_value is not None:
            data["action_value"] = action_value
        if action_properties:
            data["action_properties"] = action_properties
        if timestamp:
            data["timestamp"] = timestamp

        return self._make_request("POST", "/customers/actions", data=data)

    def delete_customer(self, customer_id: str) -> Dict[str, Any]:
        """
        Delete a customer

        Args:
            customer_id: Customer identifier to delete

        Returns:
            Dictionary containing:
                - customer_id: Deleted customer ID
                - deleted: Timestamp of deletion
                - status: Success status

        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If customer_id is missing
            APIError: For other API errors

        Example:
            >>> client = SatoriClient(api_key="your-api-key")
            >>> result = client.delete_customer("cust123")
            >>> print(f"Customer deleted at {result['deleted']}")
        """
        if not customer_id:
            raise InvalidRequestError("customer_id is required")

        return self._make_request("DELETE", f"/customers/{customer_id}")

    def close(self):
        """Close the HTTP session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()