"""
 Pinterest API v5 Client
"""

import time
import requests
from typing import Optional, Dict, List
from urllib.parse import urljoin

from .models import Pin, Board, PinListResponse, BoardListResponse
from .exceptions import (
    PinterestAPIError,
    RateLimitError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
)


class PinterestClient:
    """Pinterest API v5 Client"""

    BASE_URL = "https://api.pinterest.com/v5/"
    API_VERSION = "v5"

    def __init__(
        self,
        access_token: str,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize Pinterest client

        Args:
            access_token: OAuth2 access token
            app_id: Pinterest app ID (optional)
            app_secret: Pinterest app secret (optional)
            timeout: Request timeout in seconds
        """
        self.access_token = access_token
        self.app_id = app_id
        self.app_secret = app_secret
        self.timeout = timeout
        self.session = requests.Session()

        # Rate limiting
        self._last_request_time = 0
        self._min_request_interval = 0.1  # 100ms between requests (Pinterest allows ~5 requests per second)
        self._rate_limit_remaining = 200
        self._rate_limit_reset = time.time() + 3600

    def _wait_for_rate_limit(self):
        """Apply rate limiting to requests"""
        now = time.time()
        time_since_last = now - self._last_request_time

        if time_since_last < self._min_request_interval:
            sleep_time = self._min_request_interval - time_since_last
            time.sleep(sleep_time)

        self._last_request_time = time.time()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        files: Optional[Dict] = None,
    ) -> Dict:
        """
        Make API request with error handling and rate limiting

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint path
            params: URL query parameters
            data: Form data
            json_data: JSON body data
            files: Files to upload

        Returns:
            JSON response data

        Raises:
            PinterestAPIError: General API error
            RateLimitError: Rate limit exceeded
            AuthenticationError: Authentication failed
            ResourceNotFoundError: Resource not found
            ValidationError: Validation error
        """
        self._wait_for_rate_limit()

        url = urljoin(self.BASE_URL, endpoint)
        headers = {"Authorization": f"Bearer {self.access_token}"}

        if files:
            # Don't set Content-Type when uploading files - requests handles it with multipart/form-data
            pass
        elif json_data:
            headers["Content-Type"] = "application/json"

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json_data,
                files=files,
                timeout=self.timeout,
            )

            # Update rate limit info from headers
            self._update_rate_limit(response.headers)

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise PinterestAPIError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise PinterestAPIError(f"Request failed: {str(e)}")

    def _update_rate_limit(self, headers: Dict):
        """Update rate limit information from response headers"""
        if "Pinterest-API-Version" in headers:
            self._rate_limit_remaining = int(
                headers.get("X-RateLimit-Remaining", self._rate_limit_remaining)
            )
            if "X-RateLimit-Reset" in headers:
                self._rate_limit_reset = int(headers["X-RateLimit-Reset"])

    def _handle_response(self, response: requests.Response) -> Dict:
        """
        Handle API response and raise appropriate exceptions

        Args:
            response: HTTP response object

        Returns:
            JSON response data

        Raises:
            PinterestAPIError: General API error
            RateLimitError: Rate limit exceeded
            AuthenticationError: Authentication failed
            ResourceNotFoundError: Resource not found
            ValidationError: Validation error
        """
        try:
            data = response.json()
        except ValueError:
            data = response.text

        if response.status_code == 200:
            return data
        elif response.status_code == 201:
            return data
        elif response.status_code == 204:
            return {}
        elif response.status_code == 400:
            error_message = data.get("message", "Bad request") if isinstance(data, dict) else "Bad request"
            raise ValidationError(error_message, response=data)
        elif response.status_code == 401:
            error_message = data.get("message", "Unauthorized") if isinstance(data, dict) else "Unauthorized"
            raise AuthenticationError(error_message, response=data)
        elif response.status_code == 403:
            error_message = data.get("message", "Forbidden") if isinstance(data, dict) else "Forbidden"
            raise AuthenticationError(error_message, response=data)
        elif response.status_code == 404:
            error_message = data.get("message", "Not found") if isinstance(data, dict) else "Not found"
            raise ResourceNotFoundError(error_message, response=data)
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            error_message = data.get("message", "Rate limit exceeded") if isinstance(data, dict) else "Rate limit exceeded"
            raise RateLimitError(error_message, retry_after=retry_after, response=data)
        else:
            error_message = data.get("message", f"HTTP {response.status_code}") if isinstance(data, dict) else f"HTTP {response.status_code}"
            raise PinterestAPIError(error_message, status_code=response.status_code, response=data)

    # ==================== PIN ACTIONS ====================

    def get_pin(self, pin_id: str) -> Pin:
        """
        Get a pin by ID

        Args:
            pin_id: The pin ID

        Returns:
            Pin object

        Raises:
            PinterestAPIError: If the request fails
        """
        data = self._make_request("GET", f"pins/{pin_id}")
        return Pin.from_api_response(data)

    def create_pin(
        self,
        board_id: str,
        image_url: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        alt_text: Optional[str] = None,
        link: Optional[str] = None,
        source_url: Optional[str] = None,
    ) -> Pin:
        """
        Create a pin

        Args:
            board_id: The board ID to pin to
            image_url: URL of the image to pin
            title: Pin title
            description: Pin description
            alt_text: Alt text for accessibility
            link: Destination URL for clicks
            source_url: Source URL for attribution

        Returns:
            Created Pin object

        Raises:
            PinterestAPIError: If the request fails
            ValidationError: If validation fails
        """
        payload = {"board_id": board_id, "image_url": image_url}

        if title:
            payload["title"] = title
        if description:
            payload["description"] = description
        if alt_text:
            payload["alt_text"] = alt_text
        if link:
            payload["link"] = link
        if source_url:
            payload["source_url"] = source_url

        data = self._make_request("POST", "pins", json_data=payload)
        return Pin.from_api_response(data)

    def list_pins(
        self,
        board_id: Optional[str] = None,
        pin_id: Optional[str] = None,
        bookmark: Optional[str] = None,
        page_size: int = 25,
    ) -> PinListResponse:
        """
        List pins

        Args:
            board_id: Filter by board ID (optional)
            pin_id: Specific pin ID to get related pins (optional)
            bookmark: Pagination cursor (optional)
            page_size: Number of items per page (1-100, default 25)

        Returns:
            PinListResponse with pins and pagination info

        Raises:
            PinterestAPIError: If the request fails
        """
        if not 1 <= page_size <= 100:
            raise ValidationError("page_size must be between 1 and 100")

        params = {"page_size": page_size}
        if bookmark:
            params["bookmark"] = bookmark

        endpoint = "pins"
        if board_id:
            endpoint = f"boards/{board_id}/pins"
        elif pin_id:
            endpoint = f"pins/{pin_id}/related"

        data = self._make_request("GET", endpoint, params=params)
        return PinListResponse.from_api_response(data)

    def update_pin(
        self,
        pin_id: str,
        board_id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        alt_text: Optional[str] = None,
        link: Optional[str] = None,
    ) -> Pin:
        """
        Update a pin

        Args:
            pin_id: The pin ID
            board_id: New board ID (optional)
            title: New title (optional)
            description: New description (optional)
            alt_text: New alt text (optional)
            link: New destination URL (optional)

        Returns:
            Updated Pin object

        Raises:
            PinterestAPIError: If the request fails
            ResourceNotFoundError: If pin not found
        """
        payload = {}

        if board_id:
            payload["board_id"] = board_id
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if alt_text is not None:
            payload["alt_text"] = alt_text
        if link is not None:
            payload["link"] = link

        data = self._make_request("PATCH", f"pins/{pin_id}", json_data=payload)
        return Pin.from_api_response(data)

    def delete_pin(self, pin_id: str) -> bool:
        """
        Delete a pin

        Args:
            pin_id: The pin ID

        Returns:
            True if deleted successfully

        Raises:
            PinterestAPIError: If the request fails
            ResourceNotFoundError: If pin not found
        """
        self._make_request("DELETE", f"pins/{pin_id}")
        return True

    # ==================== BOARD ACTIONS ====================

    def get_board(self, board_id: str) -> Board:
        """
        Get a board by ID

        Args:
            board_id: The board ID

        Returns:
            Board object

        Raises:
            PinterestAPIError: If the request fails
            ResourceNotFoundError: If board not found
        """
        data = self._make_request("GET", f"boards/{board_id}")
        return Board.from_api_response(data)

    def create_board(
        self,
        name: str,
        description: Optional[str] = None,
        privacy: Optional[str] = "public",
    ) -> Board:
        """
        Create a board

        Args:
            name: Board name (max 255 chars)
            description: Board description (max 500 chars)
            privacy: Board privacy ('public' or 'secret')

        Returns:
            Created Board object

        Raises:
            PinterestAPIError: If the request fails
            ValidationError: If validation fails
        """
        if privacy not in ["public", "secret"]:
            raise ValidationError("privacy must be 'public' or 'secret'")

        payload = {"name": name}
        if description:
            payload["description"] = description
        payload["privacy"] = privacy

        data = self._make_request("POST", "boards", json_data=payload)
        return Board.from_api_response(data)

    def list_boards(
        self, bookmark: Optional[str] = None, page_size: int = 25
    ) -> BoardListResponse:
        """
        List user's boards

        Args:
            bookmark: Pagination cursor (optional)
            page_size: Number of items per page (1-100, default 25)

        Returns:
            BoardListResponse with boards and pagination info

        Raises:
            PinterestAPIError: If the request fails
        """
        if not 1 <= page_size <= 100:
            raise ValidationError("page_size must be between 1 and 100")

        params = {"page_size": page_size}
        if bookmark:
            params["bookmark"] = bookmark

        data = self._make_request("GET", "boards", params=params)
        return BoardListResponse.from_api_response(data)

    def update_board(
        self,
        board_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        privacy: Optional[str] = None,
    ) -> Board:
        """
        Update a board

        Args:
            board_id: The board ID
            name: New name (optional)
            description: New description (optional)
            privacy: New privacy setting ('public' or 'secret')

        Returns:
            Updated Board object

        Raises:
            PinterestAPIError: If the request fails
            ResourceNotFoundError: If board not found
            ValidationError: If validation fails
        """
        payload = {}

        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if privacy is not None:
            if privacy not in ["public", "secret"]:
                raise ValidationError("privacy must be 'public' or 'secret'")
            payload["privacy"] = privacy

        data = self._make_request("PATCH", f"boards/{board_id}", json_data=payload)
        return Board.from_api_response(data)

    def delete_board(self, board_id: str) -> bool:
        """
        Delete a board

        Args:
            board_id: The board ID

        Returns:
            True if deleted successfully

        Raises:
            PinterestAPIError: If the request fails
            ResourceNotFoundError: If board not found
        """
        self._make_request("DELETE", f"boards/{board_id}")
        return True

    # ==================== WEBHOOK/TRIGGER ACTIONS ====================

    def create_webhook(
        self,
        webhook_url: str,
        event_type: str = "pin.update",
        board_id: Optional[str] = None,
        access_token: Optional[str] = None,
    ) -> Dict:
        """
        Create a Pinterest webhook

        Args:
            webhook_url: URL to receive webhook events
            event_type: Type of event ('pin.update', 'board.update', etc.)
            board_id: Optional board ID to filter events
            access_token: Optional app access token (for event configuration)

        Returns:
            Webhook configuration data

        Raises:
            PinterestAPIError: If the request fails
        """
        payload = {"destination": webhook_url, "event_type": event_type}

        if board_id:
            payload["board_id"] = board_id

        # Webhook creation may require app access token
        access_token_to_use = access_token or self.app_secret
        if access_token_to_use:
            headers = {"Authorization": f"Bearer {access_token_to_use}"}
        else:
            headers = {"Authorization": f"Bearer {self.access_token}"}

        data = self._make_request("POST", "webhooks", json_data=payload)
        return data

    def list_webhooks(self) -> List[Dict]:
        """
        List all webhooks

        Returns:
            List of webhook configurations

        Raises:
            PinterestAPIError: If the request fails
        """
        data = self._make_request("GET", "webhooks")
        return data.get("webhooks", [])

    def delete_webhook(self, webhook_id: str) -> bool:
        """
        Delete a webhook

        Args:
            webhook_id: The webhook ID

        Returns:
            True if deleted successfully

        Raises:
            PinterestAPIError: If the request fails
        """
        self._make_request("DELETE", f"webhooks/{webhook_id}")
        return True

    def verify_webhook_event(self, payload: Dict, signature: Optional[str] = None) -> bool:
        """
        Verify webhook event signature

        Args:
            payload: Webhook event payload
            signature: X-Pinterest-Signature header value (optional)

        Returns:
            True if signature is valid

        Note:
            Pinterest webhooks use HMAC-SHA256 signature verification
        """
        if not signature or not self.app_secret:
            return False

        # Pinterest signature format: sha256=<hex_encoded_hmac>
        if signature.startswith("sha256="):
            signature = signature[7:]

        import hmac
        import hashlib

        # Compute HMAC with app secret
        computed = hmac.new(
            self.app_secret.encode(), str(payload).encode(), hashlib.sha256
        ).hexdigest()

        # Use constant-time comparison to prevent timing attacks
        return hmac.compare_digest(computed, signature)

    # ==================== HELPER METHODS ====================

    def get_user_account(self) -> Dict:
        """
        Get authenticated user account information

        Returns:
            User account data

        Raises:
            PinterestAPIError: If the request fails
        """
        data = self._make_request("GET", "user_account")
        return data

    def close(self):
        """Close the session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()