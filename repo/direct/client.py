"""
Direct API Client

Direct is a direct messaging platform for instant communication.

API Actions (6):
1. Send Message
2. List Conversations
3. Create Conversation
4. Get Conversation
5. Mark as Read
6. Delete Message

Triggers (2):
- New Message
- Message Read

Authentication: API Key
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class DirectMessage:
    """Direct message model"""
    id: str
    conversation_id: str
    sender_id: str
    receiver_id: str
    content: str
    sent_at: str
    read_at: Optional[str] = None
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DirectConversation:
    """Direct conversation model"""
    id: str
    user_id: str
    peer_id: str
    created_at: str
    updated_at: str
    last_message: Optional[DirectMessage] = None
    unread_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DirectUser:
    """Direct user model"""
    id: str
    name: str
    avatar_url: Optional[str] = None
    status: str = "active"


class DirectClient:
    """
    Direct API client for direct messaging operations.
    """

    BASE_URL = "https://api.direct.com/v1"
    RATE_LIMIT = 20  # requests per second

    def __init__(self, api_key: str):
        """
        Initialize Direct client.

        Args:
            api_key: Your Direct API key
        """
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
        """
        Make API request with rate limiting.
        """
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
                raise Exception(f"Direct API error: {response.status} - {error_msg}")

            return result

    async def send_message(
        self,
        conversation_id: str,
        content: str,
        attachments: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DirectMessage:
        """Send a message to a conversation."""
        data = {"conversation_id": conversation_id, "content": content}

        if attachments:
            data["attachments"] = attachments
        if metadata:
            data["metadata"] = metadata

        response = await self._make_request("POST", "/messages", data=data)
        return DirectMessage(**response)

    async def list_conversations(
        self,
        limit: int = 50,
        offset: str = None,
        unread_only: bool = False
    ) -> List[DirectConversation]:
        """List all conversations."""
        params = {"limit": limit}

        if offset:
            params["offset"] = offset
        if unread_only:
            params["unread_only"] = "true"

        response = await self._make_request("GET", "/conversations", params=params)
        conversations = response.get("conversations", [])

        result = []
        for conv in conversations:
            conv_data = conv.copy()
            if conv.get("last_message"):
                conv_data["last_message"] = DirectMessage(**conv["last_message"])
            result.append(DirectConversation(**conv_data))

        return result

    async def create_conversation(
        self,
        peer_id: str,
        initial_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DirectConversation:
        """Create a new conversation."""
        data = {"peer_id": peer_id}

        if initial_message:
            data["initial_message"] = initial_message
        if metadata:
            data["metadata"] = metadata

        response = await self._make_request("POST", "/conversations", data=data)
        conv_data = response.copy()
        if response.get("last_message"):
            conv_data["last_message"] = DirectMessage(**response["last_message"])

        return DirectConversation(**conv_data)

    async def get_conversation(
        self,
        conversation_id: str,
        include_messages: bool = False,
        message_limit: int = 50
    ) -> DirectConversation:
        """Get a specific conversation."""
        params = {}
        if include_messages:
            params["include_messages"] = "true"
            params["message_limit"] = message_limit

        response = await self._make_request("GET", f"/conversations/{conversation_id}", params=params)
        conv_data = response.copy()
        if response.get("last_message"):
            conv_data["last_message"] = DirectMessage(**response["last_message"])

        return DirectConversation(**conv_data)

    async def mark_as_read(self, conversation_id: str, message_id: str = None) -> bool:
        """Mark conversation or message as read."""
        data = {}
        if message_id:
            data["message_id"] = message_id

        response = await self._make_request("POST", f"/conversations/{conversation_id}/read", data=data)
        return response.get("success", False)

    async def delete_message(self, message_id: str) -> bool:
        """Delete a message."""
        response = await self._make_request("DELETE", f"/messages/{message_id}")
        return response.get("success", False)

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook events."""
        event_type = webhook_data.get("event_type", "unknown")

        result = {"event_type": event_type, "raw_data": webhook_data}

        if event_type == "message.created":
            result["message"] = DirectMessage(**webhook_data.get("message", {}))
            result["conversation_id"] = webhook_data.get("conversation_id")
        elif event_type == "message.read":
            result["message_id"] = webhook_data.get("message_id")
            result["conversation_id"] = webhook_data.get("conversation_id")
            result["read_at"] = webhook_data.get("read_at")

        return result