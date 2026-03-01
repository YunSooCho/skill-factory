"""
Kyusms API - SMS Messaging Client

Supports 3 API Actions:
- Send SMS Request
- Send SMS Cancel
- Get SMS Send Result

Triggers:
- None
"""

import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class SMSStatus(str, Enum):
    """SMS status enum"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"


@dataclass
class SMSRequest:
    """SMS request entity"""
    request_id: str
    phone: str
    message: str
    status: SMSStatus
    scheduled_time: Optional[str] = None
    created_at: str = ""


@dataclass
class SMSResult:
    """SMS result entity"""
    request_id: str
    phone: str
    status: SMSStatus
    delivered: bool
    send_time: Optional[str] = None
    delivery_time: Optional[str] = None
    error_message: Optional[str] = None


class KyusmsClientError(Exception):
    """Base exception for Kyusms client errors"""
    pass


class KyusmsRateLimitError(KyusmsClientError):
    """Raised when rate limit is exceeded"""
    pass


class KyusmsClient:
    """
    Kyusms API client for SMS messaging.

    API Documentation: contact Kyusms for API documentation
    Uses API Key for authentication via Bearer token.
    """

    BASE_URL = "https://api.kyusms.com/v1"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize Kyusms client.

        Args:
            api_key: API key for authentication
            base_url: Optional custom base URL
        """
        self.api_key = api_key
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None
        self._rate_limit_remaining = 100
        self._rate_limit_reset = 0

        logger = logging.getLogger("kyusms")
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        self._logger = logger

    async def __aenter__(self):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=timeout
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with error handling and rate limiting."""
        await self._check_rate_limit()

        url = f"{self.base_url}{endpoint}"

        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                self._logger.debug(f"Request: {method} {url}")
                if data:
                    self._logger.debug(f"Data: {data}")

                async with self.session.request(
                    method,
                    url,
                    json=data,
                    params=params
                ) as response:
                    await self._update_rate_limit(response)

                    if response.status in [200, 201]:
                        result = await response.json()
                        self._logger.debug(f"Response: {result}")
                        return result

                    elif response.status == 204:
                        return {}

                    elif response.status == 401:
                        raise KyusmsClientError("Authentication failed")

                    elif response.status == 403:
                        raise KyusmsClientError("Forbidden - insufficient permissions")

                    elif response.status == 404:
                        raise KyusmsClientError("Resource not found")

                    elif response.status == 422:
                        error_data = await response.json()
                        raise KyusmsClientError(
                            f"Validation error: {error_data.get('message', 'Unknown error')}"
                        )

                    elif response.status == 429:
                        await self._handle_rate_limit()
                        retry_count += 1
                        continue

                    else:
                        error_text = await response.text()
                        raise KyusmsClientError(
                            f"API error {response.status}: {error_text}"
                        )

            except aiohttp.ClientError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise KyusmsClientError(f"Network error: {str(e)}")
                await asyncio.sleep(2 ** retry_count)

    async def _check_rate_limit(self):
        """Check if rate limit allows request"""
        if self._rate_limit_remaining <= 1:
            now = int(datetime.now().timestamp())
            if now < self._rate_limit_reset:
                wait_time = self._rate_limit_reset - now
                self._logger.warning(f"Rate limit reached, waiting {wait_time}s")
                await asyncio.sleep(wait_time)

    async def _update_rate_limit(self, response: aiohttp.ClientResponse):
        """Update rate limit info from response headers"""
        remaining = response.headers.get("X-RateLimit-Remaining")
        reset = response.headers.get("X-RateLimit-Reset")

        if remaining:
            self._rate_limit_remaining = int(remaining)
        if reset:
            self._rate_limit_reset = int(reset)

    async def _handle_rate_limit(self):
        """Handle rate limit by waiting"""
        now = int(datetime.now().timestamp())
        wait_time = max(0, self._rate_limit_reset - now + 1)
        self._logger.warning(f"Rate limited, waiting {wait_time}s")
        await asyncio.sleep(wait_time)

    async def send_sms(
        self,
        phone: str,
        message: str,
        scheduled_time: Optional[str] = None
    ) -> SMSRequest:
        """
        Send an SMS message.

        Args:
            phone: Phone number (E.164 format recommended)
            message: SMS message content
            scheduled_time: Optional ISO datetime string for scheduled delivery

        Returns:
            SMS request object with request ID

        Raises:
            KyusmsClientError: On API errors
        """
        data = {
            "phone": phone,
            "message": message
        }
        if scheduled_time:
            data["scheduled_time"] = scheduled_time

        self._logger.info(f"Sending SMS to {phone}")
        result = await self._request("POST", "/sms/send", data=data)

        return SMSRequest(
            request_id=str(result.get("request_id", "")),
            phone=phone,
            message=message,
            status=SMSStatus.PENDING,
            scheduled_time=scheduled_time,
            created_at=result.get("created_at", "")
        )

    async def cancel_sms(self, request_id: str) -> Dict[str, Any]:
        """
        Cancel a scheduled SMS.

        Args:
            request_id: ID of the SMS request to cancel

        Returns:
            Cancellation result

        Raises:
            KyusmsClientError: On API errors
        """
        self._logger.info(f"Cancelling SMS {request_id}")
        result = await self._request("POST", f"/sms/{request_id}/cancel".format(request_id=request_id), data={})

        return {
            "request_id": request_id,
            "cancelled": result.get("cancelled", False),
            "message": result.get("message", "")
        }

    async def get_sms_result(self, request_id: str) -> SMSResult:
        """
        Get the delivery status of an SMS.

        Args:
            request_id: ID of the SMS request

        Returns:
            SMS result object with delivery status

        Raises:
            KyusmsClientError: On API errors
        """
        self._logger.info(f"Getting SMS result for {request_id}")
        result = await self._request("GET", f"/sms/{request_id}/status".format(request_id=request_id))

        status_str = result.get("status", "pending")
        try:
            status = SMSStatus(status_str.lower())
        except ValueError:
            status = SMSStatus.PENDING

        return SMSResult(
            request_id=request_id,
            phone=result.get("phone", ""),
            status=status,
            delivered=result.get("delivered", False),
            send_time=result.get("send_time"),
            delivery_time=result.get("delivery_time"),
            error_message=result.get("error_message")
        )