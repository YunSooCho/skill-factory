"""
Pinterest API Actions implementation.
"""
import requests
import time
from typing import Optional, List, Dict, Any
from .models import PinterestPin, PinterestBoard, PinterestPaginatedResponse
from .exceptions import (
    PinterestAPIError,
    PinterestAuthenticationError,
    PinterestRateLimitError,
    PinterestNotFoundError,
    PinterestValidationError,
)


class PinterestActions:
    """Pinterest API actions for Yoom integration."""

    BASE_URL = "https://api.pinterest.com/v5"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Pinterest API client.

        Args:
            access_token: OAuth access token
            timeout: Request timeout in seconds
        """
        self.access_token = access_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        )

        # Rate limiting state
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
        self.rate_limit_remaining = 1000

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        retry_on_rate_limit: bool = True,
    ) -> Dict[str, Any]:
        """
        Make authenticated request to Pinterest API with rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data
            retry_on_rate_limit: Whether to retry on 429 errors

        Returns:
            Response JSON as dict

        Raises:
            PinterestAPIError: For API errors
            PinterestAuthenticationError: For auth errors
            PinterestRateLimitError: For rate limit errors
            PinterestNotFoundError: For 404 errors
        """
        # Rate limiting
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

            # Update rate limit info from headers
            self.rate_limit_remaining = int(
                response.headers.get("X-RateLimit-Remaining", 0)
            )

            # Handle error responses
            if response.status_code == 401:
                error_data = response.json() if response.text else {}
                raise PinterestAuthenticationError(
                    message=error_data.get("message", "Authentication failed"),
                    status_code=401,
                    response=error_data,
                )
            elif response.status_code == 404:
                raise PinterestNotFoundError(
                    message="Resource not found",
                    status_code=404,
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(
                        method, endpoint, params, data, retry_on_rate_limit=False
                    )
                raise PinterestRateLimitError(
                    message="Rate limit exceeded",
                    status_code=429,
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise PinterestAPIError(
                    message=error_data.get("message", f"API Error: {response.status_code}"),
                    status_code=response.status_code,
                    response=error_data,
                )

            return response.json()

        except requests.Timeout:
            raise PinterestAPIError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise PinterestAPIError(f"Request failed: {str(e)}")

    # ==================== API Actions ====================

    def get_pin(self, pin_id: str) -> PinterestPin:
        """
        Get details of a specific pin.

        Args:
            pin_id: Pinterest Pin ID

        Returns:
            PinterestPin object with pin details

        Raises:
            PinterestNotFoundError: If pin not found
            PinterestAPIError: For other errors
        """
        if not pin_id:
            raise PinterestValidationError("pin_id is required")

        response = self._make_request("GET", f"/pins/{pin_id}")
        return PinterestPin.from_dict(response)

    def create_pin(
        self,
        board_id: str,
        image_url: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        link: Optional[str] = None,
        alt_text: Optional[str] = None,
    ) -> PinterestPin:
        """
        Create a new pin.

        Args:
            board_id: Board ID to pin to
            image_url: URL of the image
            title: Pin title
            description: Pin description
            link: Destination URL
            alt_text: Alt text for accessibility

        Returns:
            Created PinterestPin object

        Raises:
            PinterestValidationError: If required fields missing
            PinterestAPIError: For API errors
        """
        if not board_id or not image_url:
            raise PinterestValidationError("board_id and image_url are required")

        data = {"board_id": board_id, "media": {"source": {"url": image_url}}}

        if title:
            data["title"] = title
        if description:
            data["description"] = description
        if link:
            data["link"] = link
        if alt_text:
            data["alt_text"] = alt_text

        response = self._make_request("POST", "/pins", data=data)
        return PinterestPin.from_dict(response)

    def get_board(self, board_id: str) -> PinterestBoard:
        """
        Get details of a specific board.

        Args:
            board_id: Pinterest Board ID

        Returns:
            PinterestBoard object with board details

        Raises:
            PinterestNotFoundError: If board not found
            PinterestAPIError: For other errors
        """
        if not board_id:
            raise PinterestValidationError("board_id is required")

        response = self._make_request("GET", f"/boards/{board_id}")
        return PinterestBoard.from_dict(response)

    def create_board(
        self,
        name: str,
        description: Optional[str] = None,
        privacy: Optional[str] = "public",
    ) -> PinterestBoard:
        """
        Create a new board.

        Args:
            name: Board name
            description: Board description
            privacy: Board privacy ('public' or 'secret')

        Returns:
            Created PinterestBoard object

        Raises:
            PinterestValidationError: If name is missing
            PinterestAPIError: For API errors
        """
        if not name:
            raise PinterestValidationError("name is required")

        data = {"name": name}

        if description:
            data["description"] = description
        if privacy:
            data["privacy"] = privacy

        response = self._make_request("POST", "/boards", data=data)
        return PinterestBoard.from_dict(response)

    def list_pins(
        self,
        board_id: str,
        page_size: int = 25,
        bookmark: Optional[str] = None,
    ) -> PinterestPaginatedResponse:
        """
        List pins on a board.

        Args:
            board_id: Board ID
            page_size: Number of pins per page (1-250)
            bookmark: Pagination bookmark string

        Returns:
            PinterestPaginatedResponse with list of pins

        Raises:
            PinterestValidationError: If board_id missing or page_size invalid
            PinterestAPIError: For API errors
        """
        if not board_id:
            raise PinterestValidationError("board_id is required")

        if not 1 <= page_size <= 250:
            raise PinterestValidationError("page_size must be between 1 and 250")

        params = {"page_size": page_size}
        if bookmark:
            params["bookmark"] = bookmark

        response = self._make_request("GET", f"/boards/{board_id}/pins", params=params)
        return PinterestPaginatedResponse.from_dict(response, PinterestPin)

    def update_board(
        self,
        board_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        privacy: Optional[str] = None,
    ) -> PinterestBoard:
        """
        Update an existing board.

        Args:
            board_id: Board ID to update
            name: New name (optional)
            description: New description (optional)
            privacy: New privacy setting (optional)

        Returns:
            Updated PinterestBoard object

        Raises:
            PinterestValidationError: If no fields to update
            PinterestAPIError: For API errors
        """
        if not any([name, description, privacy]):
            raise PinterestValidationError("At least one field must be provided for update")

        data = {}
        if name:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if privacy:
            data["privacy"] = privacy

        response = self._make_request("PATCH", f"/boards/{board_id}", data=data)
        return PinterestBoard.from_dict(response)

    def list_boards(
        self, page_size: int = 25, bookmark: Optional[str] = None
    ) -> PinterestPaginatedResponse:
        """
        List all boards for the authenticated user.

        Args:
            page_size: Number of boards per page (1-100)
            bookmark: Pagination bookmark string

        Returns:
            PinterestPaginatedResponse with list of boards

        Raises:
            PinterestValidationError: If page_size invalid
            PinterestAPIError: For API errors
        """
        if not 1 <= page_size <= 100:
            raise PinterestValidationError("page_size must be between 1 and 100")

        params = {"page_size": page_size}
        if bookmark:
            params["bookmark"] = bookmark

        response = self._make_request("GET", "/boards", params=params)
        return PinterestPaginatedResponse.from_dict(response, PinterestBoard)

    def close(self):
        """Close the session."""
        self.session.close()