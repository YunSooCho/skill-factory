"""
ZixFlow API Client
WhatsApp messaging and marketing
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import time


@dataclass
class WhatsAppMessage:
    """WhatsApp message data model"""
    recipient_phone: str
    template_name: Optional[str] = None
    template_params: Optional[List[str]] = None
    message_text: Optional[str] = None


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, max_requests: int = 120, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.time()
            self.requests = [req_time for req_time in self.requests
                            if now - req_time < self.per_seconds]

            if len(self.requests) >= self.maxRequests:
                sleep_time = self.per_seconds - (now - self.requests[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    self.requests = []

            self.requests.append(now)


class ZixflowClient:
    """
    ZixFlow API client for WhatsApp messaging.

    Rate Limit: 120 requests per minute
    """

    BASE_URL = "https://api.zixflow.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize ZixFlow API client.

        Args:
            api_key: Your ZixFlow API key
        """
        self.api_key = api_key
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=120, per_seconds=60)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API request with error handling and rate limiting.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails or returns error
        """
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}{endpoint}"

        try:
            async with self.session.request(
                method,
                url,
                headers=self._get_headers(),
                params=params,
                json=json_data
            ) as response:
                try:
                    data = await response.json()
                except:
                    text = await response.text()
                    data = {"raw_response": text}

                if response.status >= 400:
                    error_msg = data.get("error", data.get("message", "Unknown error"))
                    raise Exception(f"ZixFlow API error ({response.status}): {error_msg}")

                return data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during ZixFlow API request: {str(e)}")

    # ==================== WhatsApp Messaging ====================

    async def send_whatsapp_template(
        self,
        recipient_phone: str,
        template_name: str,
        template_params: Optional[List[str]] = None,
        language_code: str = "en"
    ) -> Dict[str, Any]:
        """
        Send a WhatsApp template message.

        Args:
            recipient_phone: Recipient phone number (with country code)
            template_name: WhatsApp template name
            template_params: Template parameters for dynamic content
            language_code: Template language code (default: en)

        Returns:
            Response with message ID

        Raises:
            Exception: If request fails
        """
        data = {
            "to": recipient_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code}
            }
        }

        if template_params:
            data["template"]["components"] = [{
                "type": "body",
                "parameters": [{"type": "text", "text": param} for param in template_params]
            }]

        return await self._request("POST", "/whatsapp/messages", json_data=data)

    async def send_whatsapp_text(
        self,
        recipient_phone: str,
        message_text: str
    ) -> Dict[str, Any]:
        """
        Send a WhatsApp text message.

        Args:
            recipient_phone: Recipient phone number (with country code)
            message_text: Message text content

        Returns:
            Response with message ID

        Raises:
            Exception: If request fails
        """
        data = {
            "to": recipient_phone,
            "type": "text",
            "text": {
                "body": message_text
            }
        }

        return await self._request("POST", "/whatsapp/messages", json_data=data)