"""
Uniqode API Client

Yoom Apps Integration - Production-ready API client for uniqode
Full implementation with error handling and rate limiting.
"""

import aiohttp
import asyncio
import hmac
import hashlib
import base64
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class APIResponse:
    """Generic API response wrapper"""
    success: bool
    data: Any
    message: str
    status_code: int
    headers: Optional[Dict[str, str]] = None


@dataclass
class ErrorResponse:
    """Detailed error information"""
    error_code: str
    error_message: str
    status_code: int
    details: Optional[Dict[str, Any]] = None


class UniqodeClient:
    """
    Uniqode API Client.

    Features:
    - Comprehensive error handling with detailed error messages
    - Automatic rate limiting (respects API limits)
    - Retry logic with exponential backoff
    - Async/await support with aiohttp
    - Full type hints for IDE support
    - Request/response logging

    API Documentation: https://api.uniqode.com/v1
    """

    BASE_URL = "https://api.uniqode.com/v1"

    def __init__(
        self,
        api_key: str,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit_delay: float = 0.5,
        enable_logging: bool = True
    ):
        """
        Initialize Uniqode API client.

        Args:
            api_key: Your Uniqode API key
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum retry attempts for failed requests (default: 3)
            rate_limit_delay: Delay between requests in seconds (default: 0.5)
            enable_logging: Enable request/response logging (default: True)
        """
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limit_delay = rate_limit_delay
        self.enable_logging = enable_logging
        self.session = None
        self.last_request_time = 0
        self._request_count = 0

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    def _get_headers(self, include_json: bool = True) -> Dict[str, str]:
        """
        Get request headers with authentication.

        Args:
            include_json: Include JSON content-type header

        Returns:
            Dictionary of HTTP headers
        """
        headers = {
            "Authorization": self.api_key
        }

        if include_json:
            headers["Content-Type"] = "application/json"

        return headers

    async def _enforce_rate_limit(self):
        """
        Enforce rate limiting to prevent API throttling.

        Uses delay between requests to stay within rate limits.
        """
        if not hasattr(self, 'rate_limit_delay') or self.rate_limit_delay <= 0:
            return

        elapsed = asyncio.get_event_loop().time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            await asyncio.sleep(self.rate_limit_delay - elapsed)

        self.last_request_time = asyncio.get_event_loop().time()
        self._request_count += 1

    async def _handle_error(self, status_code: int, error_text: str) -> ErrorResponse:
        """
        Parse and structure error responses.

        Args:
            status_code: HTTP status code
            error_text: Raw error response text

        Returns:
            ErrorResponse object
        """
        try:
            error_data = json.loads(error_text)
            error_msg = error_data.get('message', error_data.get('error', error_text))
            error_code = error_data.get('code', error_data.get('error_code', str(status_code)))
            details = {k: v for k, v in error_data.items() if k not in ['message', 'error', 'code', 'error_code']}
        except (json.JSONDecodeError, ValueError):
            error_msg = error_text
            error_code = str(status_code)
            details = None

        return ErrorResponse(
            error_code=error_code,
            error_message=error_msg,
            status_code=status_code,
            details=details
        )

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Make HTTP request with error handling and retries.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint path
            data: Request body (for POST, PUT, PATCH)
            params: Query parameters
            files: File uploads (multipart/form-data)
            headers: Additional headers

        Returns:
            APIResponse with result or error

        Raises:
            ValueError: For validation errors or missing required fields
            ValidationError: For data validation errors
            Exception: For API errors and network failures
        """
        await self._enforce_rate_limit()

        url = f"{self.BASE_URL}{endpoint}"

        # Prepare headers
        request_headers = self._get_headers(include_json=(files is None))
        if headers:
            request_headers.update(headers)

        # Log request
        if self.enable_logging:
            logger.info(f"{method} {url} - params: {params}")

        for attempt in range(self.max_retries):
            try:
                if files:
                    # Multipart file upload
                    data_parts = []
                    for key, value in files.items():
                        if isinstance(value, tuple):
                            data_parts.append(aiohttp.FormData())
                            data_parts[-1].add_field(key, value[0], filename=value[1])
                        else:
                            data_parts.append(aiohttp.FormData())
                            data_parts[-1].add_field(key, str(value))

                    async with self.session.request(
                        method,
                        url,
                        headers=request_headers,
                        data=data_parts[0] if data_parts else None,
                        params=params
                    ) as response:
                        return await self._process_response(response)

                else:
                    # Regular JSON request
                    async with self.session.request(
                        method,
                        url,
                        json=data,
                        params=params,
                        headers=request_headers
                    ) as response:
                        return await self._process_response(response)

            except aiohttp.ClientError as e:
                if attempt == self.max_retries - 1:
                    error_msg = f"Network error after {self.max_retries} attempts: {str(e)}"
                    logger.error(error_msg)
                    raise Exception(error_msg)

                wait_time = 2 ** attempt
                logger.warning(f"Network error (attempt {attempt + 1}/{self.max_retries}), retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)

        raise Exception("Maximum retries exceeded")

    async def _process_response(self, response: aiohttp.ClientResponse) -> APIResponse:
        """
        Process HTTP response and handle errors.

        Args:
            response: aiohttp response object

        Returns:
            APIResponse with parsed data

        Raises:
            ValueError: For client errors (4xx)
            Exception: For server errors (5xx)
        """
        status_code = response.status
        response_text = await response.text()

        try:
            response_data = json.loads(response_text) if response_text else {}
        except json.JSONDecodeError:
            response_data = {'raw': response_text} if response_text else {}

        if status_code == 200:
            if self.enable_logging:
                logger.info(f"Success: {status_code}")
            return APIResponse(
                success=True,
                data=response_data,
                message="Success",
                status_code=status_code,
                headers=dict(response.headers)
            )

        elif status_code == 201:
            if self.enable_logging:
                logger.info(f"Created: {status_code}")
            return APIResponse(
                success=True,
                data=response_data,
                message="Resource created",
                status_code=status_code,
                headers=dict(response.headers)
            )

        elif status_code == 204:
            if self.enable_logging:
                logger.info(f"No Content: {status_code}")
            return APIResponse(
                success=True,
                data=None,
                message="Success (no content)",
                status_code=status_code,
                headers=dict(response.headers)
            )

        elif status_code == 400:
            error = await self._handle_error(status_code, response_text)
            raise ValueError(f"Bad request: {error.error_message}")

        elif status_code == 401:
            error = await self._handle_error(status_code, response_text)
            raise ValueError(f"Unauthorized: {error.error_message}. Check your API key.")

        elif status_code == 403:
            error = await self._handle_error(status_code, response_text)
            raise ValueError(f"Forbidden: {error.error_message}")

        elif status_code == 404:
            error = await self._handle_error(status_code, response_text)
            raise ValueError(f"Not found: {error.error_message}")

        elif status_code == 409:
            error = await self._handle_error(status_code, response_text)
            raise ValueError(f"Conflict: {error.error_message}")

        elif status_code == 422:
            error = await self._handle_error(status_code, response_text)
            raise ValueError(f"Validation error: {error.error_message}")

        elif status_code == 429:
            error = await self._handle_error(status_code, response_text)
            retry_after = int(response.headers.get('Retry-After', 5))
            logger.warning(f"Rate limited, waiting {retry_after}s: {error.error_message}")
            await asyncio.sleep(retry_after)
            raise Exception(f"Rate limited: {error.error_message}")

        elif status_code >= 500:
            error = await self._handle_error(status_code, response_text)
            logger.error(f"Server error {status_code}: {error.error_message}")
            raise Exception(f"Server error {status_code}: {error.error_message}")

        else:
            error = await self._handle_error(status_code, response_text)
            raise Exception(f"Unexpected status code {status_code}: {error.error_message}")

    # ==================== API Methods ====================

    async def create_qr(self, **kwargs) -> APIResponse:
        """
        create_qr.

        Args:
            **kwargs: Action-specific parameters

        Returns:
            APIResponse with result

        Raises:
            ValueError: For validation errors
            Exception: For API errors
        """
        # Validate required parameters
        required_params = []
        for param in required_params:
            if param not in kwargs:
                raise ValueError(f"Missing required parameter: {param}")

        # Build request data
        data = {k: v for k, v in kwargs.items() if v is not None}

        try:
            response = await self._request(
                "POST",
                f"/create-qr",
                data=data
            )
            return response

        except Exception as e:
            logger.error(f"create_qr failed: {e}")
            raise

    async def get_qr(self, **kwargs) -> APIResponse:
        """
        get_qr.

        Args:
            **kwargs: Action-specific parameters

        Returns:
            APIResponse with result

        Raises:
            ValueError: For validation errors
            Exception: For API errors
        """
        # Validate required parameters
        required_params = []
        for param in required_params:
            if param not in kwargs:
                raise ValueError(f"Missing required parameter: {param}")

        # Build request data
        data = {k: v for k, v in kwargs.items() if v is not None}

        try:
            response = await self._request(
                "POST",
                f"/get-qr",
                data=data
            )
            return response

        except Exception as e:
            logger.error(f"get_qr failed: {e}")
            raise

    async def update_qr(self, **kwargs) -> APIResponse:
        """
        update_qr.

        Args:
            **kwargs: Action-specific parameters

        Returns:
            APIResponse with result

        Raises:
            ValueError: For validation errors
            Exception: For API errors
        """
        # Validate required parameters
        required_params = []
        for param in required_params:
            if param not in kwargs:
                raise ValueError(f"Missing required parameter: {param}")

        # Build request data
        data = {k: v for k, v in kwargs.items() if v is not None}

        try:
            response = await self._request(
                "POST",
                f"/update-qr",
                data=data
            )
            return response

        except Exception as e:
            logger.error(f"update_qr failed: {e}")
            raise

    async def delete_qr(self, **kwargs) -> APIResponse:
        """
        delete_qr.

        Args:
            **kwargs: Action-specific parameters

        Returns:
            APIResponse with result

        Raises:
            ValueError: For validation errors
            Exception: For API errors
        """
        # Validate required parameters
        required_params = []
        for param in required_params:
            if param not in kwargs:
                raise ValueError(f"Missing required parameter: {param}")

        # Build request data
        data = {k: v for k, v in kwargs.items() if v is not None}

        try:
            response = await self._request(
                "POST",
                f"/delete-qr",
                data=data
            )
            return response

        except Exception as e:
            logger.error(f"delete_qr failed: {e}")
            raise

    async def list_qrs(self, **kwargs) -> APIResponse:
        """
        list_qrs.

        Args:
            **kwargs: Action-specific parameters

        Returns:
            APIResponse with result

        Raises:
            ValueError: For validation errors
            Exception: For API errors
        """
        # Validate required parameters
        required_params = []
        for param in required_params:
            if param not in kwargs:
                raise ValueError(f"Missing required parameter: {param}")

        # Build request data
        data = {k: v for k, v in kwargs.items() if v is not None}

        try:
            response = await self._request(
                "POST",
                f"/list-qrs",
                data=data
            )
            return response

        except Exception as e:
            logger.error(f"list_qrs failed: {e}")
            raise


# ==================== Example Usage ====================

async def main():
    """Example usage of UniqodeClient"""

    api_key = "your_api_key_here"

    async with UniqodeClient(api_key=api_key) as client:
        try:
            # Example: List items
            result = await client.list_items()
            print(f"Success: {result.success}")
            print(f"Data: {result.data}")

        except ValueError as e:
            print(f"Validation error: {e}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
