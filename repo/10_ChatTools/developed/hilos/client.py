"""
Hilos API Client

Hilos is a customer messaging platform for businesses.

API Actions (6):
1. Send Message
2. List Conversations
3. Get Conversation
4. Send Template
5. Get Contact
6. List Contacts

Triggers (2):
- Message Received
- Conversation Created

Authentication: API Key
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class HilosMessage:
    """Hilos message model"""
    id: str
    conversation_id: str
    direction: str
    content: str
    status: str
    created_at: str
    attachments: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class HilosConversation:
    """Hilos conversation model"""
    id: str
    contact_id: str
    status: str
    channel: str
    created_at: str
    updated_at: str
    last_message: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HilosContact:
    """Hilos contact model"""
    id: str
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class HilosClient:
    """
    Hilos API client for customer messaging.
    """

    BASE_URL = "https://api.hilos.co/v1"
    RATE_LIMIT = 15  # requests per second

    def __init__(self, api_key: str):
        """Initialize Hilos client."""
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
                raise Exception(f"Hilos API error: {response.status} - {error_msg}")

            return result

    async def send_message(
        self,
        conversation_id: str,
        content: str,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> HilosMessage:
        """Send a message to a conversation."""
        data = {"content": content}

        if attachments:
            data["attachments"] = attachments

        response = await self._make_request("POST", f"/conversations/{conversation_id}/messages", data=data)
        return HilosMessage(**response)

    async def list_conversations(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[HilosConversation]:
        """List conversations."""
        params = {"limit": limit, "offset": offset}

        if status:
            params["status"] = status

        response = await self._make_request("GET", "/conversations", params=params)
        conversations = response.get("conversations", [])

        return [HilosConversation(**c) for c in conversations]

    async def get_conversation(self, conversation_id: str) -> HilosConversation:
        """Get conversation details."""
        response = await self._make_request("GET", f"/conversations/{conversation_id}")
        return HilosConversation(**response)

    async def send_template(
        self,
        contact_id: str,
        template_name: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> HilosMessage:
        """Send a template message."""
        data = {"template_name": template_name}

        if parameters:
            data["parameters"] = parameters

        response = await self._make_request("POST", f"/contacts/{contact_id}/templates", data=data)
        return HilosMessage(**response)

    async def get_contact(self, contact_id: str) -> HilosContact:
        """Get contact details."""
        response = await self._make_request("GET", f"/contacts/{contact_id}")
        return HilosContact(**response)

    async def list_contacts(
        self,
        limit: int = 50,
        offset: int = 0,
        tag: Optional[str] = None
    ) -> List[HilosContact]:
        """List contacts."""
        params = {"limit": limit, "offset": offset}

        if tag:
            params["tag"] = tag

        response = await self._make_request("GET", "/contacts", params=params)
        contacts = response.get("contacts", [])

        return [HilosContact(**c) for c in contacts]

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook events."""
        event_type = webhook_data.get("event_type", "unknown")

        result = {"event_type": event_type, "raw_data": webhook_data}

        if event_type == "message.received":
            result["message"] = HilosMessage(**webhook_data.get("message", {}))
            result["conversation_id"] = webhook_data.get("conversation_id")
        elif event_type == "conversation.created":
            result["conversation"] = HilosConversation(**webhook_data.get("conversation", {}))

        return result