"""OneSignal API Actions implementation."""
import requests
import time
from typing import Optional, Dict, Any, List
from .exceptions import (
    OneSignalError,
    OneSignalAuthenticationError,
    OneSignalRateLimitError,
    OneSignalNotFoundError,
    OneSignalValidationError,
)


class OneSignalActions:
    """API actions for OneSignal integration."""

    BASE_URL = "https://onesignal.com/api/v1"

    def __init__(
        self,
        app_id: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize API client.

        Args:
            app_id: OneSignal App ID
            api_key: REST API Key for authentication
            timeout: Request timeout in seconds
        """
        self.app_id = app_id
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

        # Add authentication headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.api_key}"
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
                raise OneSignalAuthenticationError(
                    message=error_data.get("errors", ["Authentication failed"])[0] if error_data.get("errors") else "Authentication failed",
                    status_code=401,
                    response=error_data,
                )
            elif response.status_code == 404:
                raise OneSignalNotFoundError(
                    message=error_data.get("errors", ["Resource not found"])[0] if response.text else "Resource not found",
                    status_code=404,
                    response=response.json() if response.text else None,
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(method, endpoint, params, data, False)
                raise OneSignalRateLimitError(
                    message="Rate limit exceeded", status_code=429
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise OneSignalError(
                    message=error_data.get("errors", [f"API Error: {response.status_code}"])[0] if error_data.get("errors") else f"API Error: {response.status_code}",
                    status_code=response.status_code,
                    response=error_data,
                )

            return response.json()

        except requests.Timeout:
            raise OneSignalError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise OneSignalError(f"Request failed: {str(e)}")

    def delete_subscription(self, **kwargs) -> Dict[str, Any]:
        """
        Delete a subscription.

        Args:
            subscription_id: ID of subscription to delete
            app_id: (optional) App ID (uses default if not provided)

        Returns:
            API response as dict
        """
        subscription_id = kwargs.get("subscription_id")
        app_id = kwargs.get("app_id", self.app_id)
        endpoint = f"/apps/{app_id}/subscriptions/{subscription_id}"

        return self._make_request("DELETE", endpoint)

    def cancel_message(self, **kwargs) -> Dict[str, Any]:
        """
        Cancel a scheduled/outstanding message.

        Args:
            message_id: ID of message to cancel
            app_id: (optional) App ID (uses default if not provided)

        Returns:
            API response as dict
        """
        message_id = kwargs.get("message_id")
        app_id = kwargs.get("app_id", self.app_id)
        endpoint = f"/apps/{app_id}/notifications/{message_id}"

        return self._make_request("DELETE", endpoint)

    def create_user(self, **kwargs) -> Dict[str, Any]:
        """
        Create a new user.

        Args:
            app_id: (optional) App ID (uses default if not provided)
            properties: User properties
            subscriptions: (optional) List of subscriptions

        Returns:
            API response as dict
        """
        app_id = kwargs.get("app_id", self.app_id)
        endpoint = f"/apps/{app_id}/users"

        return self._make_request("POST", endpoint, data=kwargs)

    def add_subscription(self, **kwargs) -> Dict[str, Any]:
        """
        Add a subscription to a user.

        Args:
            user_id: User ID to add subscription to
            app_id: (optional) App ID (uses default if not provided)
            subscription: Subscription object with device details

        Returns:
            API response as dict
        """
        user_id = kwargs.get("user_id")
        app_id = kwargs.get("app_id", self.app_id)
        endpoint = f"/apps/{app_id}/users/{user_id}/subscriptions"

        return self._make_request("POST", endpoint, data=kwargs)

    def update_subscription(self, **kwargs) -> Dict[str, Any]:
        """
        Update a subscription.

        Args:
            subscription_id: ID of subscription to update
            app_id: (optional) App ID (uses default if not provided)
            subscription: Updated subscription properties

        Returns:
            API response as dict
        """
        subscription_id = kwargs.get("subscription_id")
        app_id = kwargs.get("app_id", self.app_id)
        endpoint = f"/apps/{app_id}/subscriptions/{subscription_id}"

        return self._make_request("PUT", endpoint, data=kwargs)

    def search_messages(self, **kwargs) -> Dict[str, Any]:
        """
        Search for messages.

        Args:
            app_id: (optional) App ID (uses default if not provided)
            limit: (optional) Maximum number of results
            offset: (optional) Offset for pagination
            kind: (optional) Message kind filter
            status: (optional) Message status filter

        Returns:
            API response as dict
        """
        app_id = kwargs.get("app_id", self.app_id)
        endpoint = f"/apps/{app_id}/notifications"

        return self._make_request("GET", endpoint, params=kwargs)

    def get_message(self, **kwargs) -> Dict[str, Any]:
        """
        Get message details.

        Args:
            message_id: ID of message to retrieve
            app_id: (optional) App ID (uses default if not provided)

        Returns:
            API response as dict
        """
        message_id = kwargs.get("message_id")
        app_id = kwargs.get("app_id", self.app_id)
        endpoint = f"/apps/{app_id}/notifications/{message_id}"

        return self._make_request("GET", endpoint)

    def update_user(self, **kwargs) -> Dict[str, Any]:
        """
        Update a user.

        Args:
            user_id: ID of user to update
            app_id: (optional) App ID (uses default if not provided)
            properties: (optional) Updated user properties

        Returns:
            API response as dict
        """
        user_id = kwargs.get("user_id")
        app_id = kwargs.get("app_id", self.app_id)
        endpoint = f"/apps/{app_id}/users/{user_id}"

        return self._make_request("PUT", endpoint, data=kwargs)

    def get_user(self, **kwargs) -> Dict[str, Any]:
        """
        Get user details.

        Args:
            user_id: ID of user to retrieve
            app_id: (optional) App ID (uses default if not provided)

        Returns:
            API response as dict
        """
        user_id = kwargs.get("user_id")
        app_id = kwargs.get("app_id", self.app_id)
        endpoint = f"/apps/{app_id}/users/{user_id}"

        return self._make_request("GET", endpoint)

    def close(self):
        """Close the session."""
        self.session.close()