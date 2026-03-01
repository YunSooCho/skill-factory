"""
Inout WhatsApp API Client

Inout WhatsApp provides WhatsApp Business API integration for messaging.

API Actions (6):
1. Send Message
2. Send Template
3. Get Message Status
4. List Messages
5. Get Contact
6. List Contacts

Triggers (2):
- Message Received
- Status Updated

Authentication: API Key
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class WhatsAppMessage:
    """WhatsApp message model"""
    id: str
    to: str
    from_: str = None
    content: Optional[str] = None
    template_name: Optional[str] = None
    status: str = "sent"
    created_at: str = None
    delivered_at: Optional[str] = None
    read_at: Optional[str] = None

    def __post_init__(self):
        """Handle 'from' keyword"""
        if not hasattr(self, 'from_'):
            self.from_ = None
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class WhatsAppContact:
    """WhatsApp contact model"""
    phone: str
    name: Optional[str] = None
    profile_picture: Optional[str] = None
    status: str = "active"


@dataclass
class MessageStatus:
    """Message status model"""
    message_id: str
    status: str
    timestamp: str


class InoutWhatsAppClient:
    """
    Inout WhatsApp API client for WhatsApp messaging.
    """

    BASE_URL = "https://api.inout-whatsapp.com/v1"
    RATE_LIMIT = 10  # requests per second

    def __init__(self, api_key: str):
        """Initialize WhatsApp client."""
        self.api_key = api_key
        self.session = None
        self._last_request_time = datetime.now()
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _check_rate_limit(self):
        """Check and enforce rate limiting"""
        now = datetime.now()
        time_since_last = (now - self._last_request_time).total_seconds()

        if time_since_last < (1.0 / self.RATE_LIMIT):
            wait_time = (1.0 / self.RATE_LIMIT) - time_since_last
            await asyncio.sleep(wait_time)

        self._last_request_time = datetime.now()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make API request with rate limiting."""
        await self._check_rate_limit()

        url = f"{self.BASE_URL}{endpoint}"

        async with self.session.request(
            method,
            url,
            headers=self._headers,
            json=data,
            params=params
        ) as response:
            try:
                result = await response.json()
            except:
                result = {}

            if response.status not in [200, 201]:
                error_msg = result.get("error", result.get("message", "Unknown error"))
                raise Exception(f"WhatsApp API error: {response.status} - {error_msg}")

            return result

    async def send_message(
        self,
        to: str,
        content: str,
        media_url: Optional[str] = None
    ) -> WhatsAppMessage:
        """Send a WhatsApp message."""
        data = {"to": to, "content": content}

        if media_url:
            data["media_url"] = media_url

        response = await self._make_request("POST", "/messages", data=data)
        return WhatsAppMessage(**response)

    async def send_template(
        self,
        to: str,
        template_name: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> WhatsAppMessage:
        """Send a WhatsApp template message."""
        data = {
            "to": to,
            "template_name": template_name,
            "language": "en"
        }

        if parameters:
            data["parameters"] = parameters

        response = await self._make_request("POST", "/templates", data=data)
        return WhatsAppMessage(**response)

    async def get_message_status(self, message_id: str) -> MessageStatus:
        """Get message delivery status."""
        response = await self._make_request("GET", f"/messages/{message_id}/status")
        return MessageStatus(**response)

    async def list_messages(
        self,
        phone: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[WhatsAppMessage]:
        """List messages."""
        params = {"limit": limit, "offset": offset}

        if phone:
            params["phone"] = phone

        response = await self._make_request("GET", "/messages", params=params)
        messages = response.get("messages", [])

        return [WhatsAppMessage(**m) for m in messages]

    async def get_contact(self, phone: str) -> WhatsAppContact:
        """Get contact information."""
        response = await self._make_request("GET", f"/contacts/{phone}")
        return WhatsAppContact(**response)

    async def list_contacts(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[WhatsAppContact]:
        """List contacts."""
        params = {"limit": limit, "offset": offset}

        response = await self._make_request("GET", "/contacts", params=params)
        contacts = response.get("contacts", [])

        return [WhatsAppContact(**c) for c in contacts]

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook events."""
        event_type = webhook_data.get("event_type", "unknown")

        result = {"event_type": event_type, "raw_data": webhook_data}

        if event_type == "message.received":
            result["message"] = WhatsAppMessage(**webhook_data.get("message", {}))
        elif event_type == "message.status.updated":
            result["status"] = MessageStatus(**webhook_data.get("status", {}))

        return result