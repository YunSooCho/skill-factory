"""
Satismeter API Client Implementation

Provides methods for:
- Add or Update User: Add new user or update existing user
- List Users: List survey users
- New Survey Response Trigger: Webhook handling for survey responses
"""

import requests
import time
import hmac
import hashlib
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class RateLimiter:
    """Rate limiter for API requests"""
    max_requests: int = 500  # Maximum requests per time window
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


class SatismeterError(Exception):
    """Base exception for Satismeter API errors"""
    pass


class AuthenticationError(SatismeterError):
    """Raised when authentication fails"""
    pass


class RateLimitError(SatismeterError):
    """Raised when rate limit is exceeded"""
    pass


class InvalidRequestError(SatismeterError):
    """Raised when request parameters are invalid"""
    pass


class APIError(SatismeterError):
    """Raised for general API errors"""
    pass


class SatismeterClient:
    """
    Satismeter API Client

    API for user management and survey response handling.
    """

    BASE_URL = "https://app.satismeter.com/api"

    def __init__(
        self,
        api_key: str,
        write_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize Satismeter client

        Args:
            api_key: Your Satismeter API key (for read operations)
            write_key: Your Satismeter write key (for write operations)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.api_key = api_key
        self.write_key = write_key or api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limiter = RateLimiter(max_requests=500, time_window=60)
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        use_write_key: bool = False
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Satismeter API

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            use_write_key: Whether to use write key for authentication

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

        # Use appropriate authentication
        headers = self.session.headers.copy()
        if use_write_key:
            headers["Authorization"] = f"Bearer {self.write_key}"
        else:
            headers["Authorization"] = f"Bearer {self.api_key}"

        for attempt in range(self.max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=headers,
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

    def add_or_update_user(
        self,
        user_id: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a new user or update an existing user

        Args:
            user_id: Unique user identifier (required)
            email: User email address
            name: User name
            properties: Additional user properties as key-value pairs
            project_id: Project identifier (optional, uses default if not provided)

        Returns:
            Dictionary containing:
                - created: Boolean indicating if user was created (True) or updated (False)
                - user_id: User ID
                - email: User email
                - properties: User properties

        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If user_id is missing
            APIError: For other API errors

        Example:
            >>> client = SatismeterClient(api_key="your-api-key")
            >>> result = client.add_or_update_user(
            ...     user_id="user123",
            ...     email="john@example.com",
            ...     name="John Doe",
            ...     properties={"plan": "pro", "signup_date": "2024-01-01"}
            ... )
            >>> print(f"User {'created' if result['created'] else 'updated'}")
        """
        if not user_id:
            raise InvalidRequestError("user_id is required")

        data = {"userId": user_id}

        if email:
            data["email"] = email
        if name:
            data["name"] = name
        if properties:
            data["properties"] = properties
        if project_id:
            data["projectId"] = project_id

        return self._make_request("POST", "/users", data=data, use_write_key=True)

    def list_users(
        self,
        project_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List survey users

        Args:
            project_id: Project identifier to filter users (optional)
            limit: Maximum number of users to return (default: 100, max: 1000)
            offset: Offset for pagination (default: 0)
            email: Filter by email address (optional)

        Returns:
            Dictionary containing:
                - users: List of user objects
                - total: Total number of users
                - limit: Requested limit
                - offset: Requested offset

        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If parameters are invalid
            APIError: For other API errors

        Example:
            >>> client = SatismeterClient(api_key="your-api-key")
            >>> result = client.list_users(limit=50)
            >>> for user in result['users']:
            ...     print(f"{user['name']} ({user['email']})")
        """
        if limit > 1000:
            raise InvalidRequestError("limit cannot exceed 1000")
        if offset < 0:
            raise InvalidRequestError("offset cannot be negative")

        params = {"limit": limit, "offset": offset}

        if project_id:
            params["projectId"] = project_id
        if email:
            params["email"] = email

        return self._make_request("GET", "/users", params=params)

    def verify_webhook_signature(
        self,
        payload: str,
        signature: str,
        webhook_secret: str
    ) -> bool:
        """
        Verify webhook signature from Satismeter

        Args:
            payload: Raw webhook payload (as string)
            signature: Signature from X-Satismeter-Signature header
            webhook_secret: Your webhook secret key

        Returns:
            True if signature is valid, False otherwise

        Example:
            >>> client = SatismeterClient(api_key="your-api-key")
            >>> payload = request.get_data(as_text=True)
            >>> signature = request.headers.get('X-Satismeter-Signature')
            >>> is_valid = client.verify_webhook_signature(payload, signature, "your-webhook-secret")
        """
        if not webhook_secret:
            return False

        # Split signature into version and hash
        if not signature or '=' not in signature:
            return False

        version, hash_value = signature.split('=', 1)

        if version != 'sha256':
            return False

        # Calculate expected signature
        expected_hash = hmac.new(
            webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        # Use compare_digest to prevent timing attacks
        return hmac.compare_digest(expected_hash, hash_value)

    def handle_webhook_event(
        self,
        payload: Dict[str, Any],
        signature: Optional[str] = None,
        webhook_secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle webhook events from Satismeter (Trigger: New Survey Response)

        Args:
            payload: Webhook payload data
            signature: Signature from X-Satismeter-Signature header (optional)
            webhook_secret: Your webhook secret key (required if signature provided)

        Returns:
            Dictionary containing:
                - event_type: Type of event (e.g., "survey_response")
                - user: User information
                - response: Survey response data
                - survey: Survey details
                - answers: List of answers

        Raises:
            InvalidRequestError: If signature verification fails
            AuthenticationError: If webhook secret is provided with signature but invalid

        Example:
            >>> client = SatismeterClient(api_key="your-api-key")
            >>> payload = request.get_json()
            >>> signature = request.headers.get('X-Satismeter-Signature')
            >>> webhook_secret = "your-webhook-secret"
            >>>
            >>> event = client.handle_webhook_event(payload, signature, webhook_secret)
            >>> print(f"New response from user: {event['user']['name']}")
        """
        # Verify signature if both signature and secret are provided
        if signature and webhook_secret:
            # payload should be the raw string for signature verification
            # This is a simplified version - in practice you'd need the raw payload
            if not self.verify_webhook_signature(str(payload), signature, webhook_secret):
                raise InvalidRequestError("Invalid webhook signature")

        # Validate event type
        event_type = payload.get('type')

        if not event_type:
            raise InvalidRequestError("Missing event type in webhook payload")

        # Process known event types
        if event_type == 'survey_response':
            return {
                'event_type': event_type,
                'user': payload.get('user', {}),
                'response': payload.get('response', {}),
                'survey': payload.get('survey', {}),
                'answers': payload.get('answers', []),
                'timestamp': payload.get('createdAt')
            }
        else:
            # Return generic event structure
            return {
                'event_type': event_type,
                'data': payload,
                'timestamp': payload.get('createdAt')
            }

    def close(self):
        """Close the HTTP session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()