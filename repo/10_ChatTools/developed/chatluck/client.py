"""
Chatluck API Client

Chatluck is a chat-based messaging platform for team communication.

API Actions (6):
1. Send Message
2. List Messages
3. Create Channel
4. List Channels
5. Get User Info
6. List Users

Triggers (2):
- New Message
- User Joined

Authentication: API Key
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class ChatluckMessage:
    """Chatluck message model"""
    id: str
    channel_id: str
    user_id: str
    content: str
    created_at: str
    updated_at: Optional[str] = None
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatluckChannel:
    """Chatluck channel model"""
    id: str
    name: str
    description: Optional[str] = None
    created_at: str = None
    is_private: bool = False
    member_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatluckUser:
    """Chatluck user model"""
    id: str
    name: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    status: str = "active"
    created_at: str = None


@dataclass
class ChannelOptions:
    """Options for creating a channel"""
    name: str
    description: Optional[str] = None
    is_private: bool = False
    member_ids: List[str] = field(default_factory=list)


class ChatluckClient:
    """
    Chatluck API client for messaging operations.
    """

    BASE_URL = "https://api.chatluck.com/v1"
    RATE_LIMIT = 10  # requests per second

    def __init__(self, api_key: str):
        """
        Initialize Chatluck client.

        Args:
            api_key: Your Chatluck API key
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

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response JSON

        Raises:
            Exception: If request fails
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
                raise Exception(
                    f"Chatluck API error: {response.status} - {error_msg}"
                )

            return result

    async def send_message(
        self,
        channel_id: str,
        content: str,
        user_id: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ChatluckMessage:
        """
        Send a message to a channel.

        Args:
            channel_id: Channel ID to send message to
            content: Message content
            user_id: Optional user ID (defaults to API key owner)
            attachments: Optional list of attachment URLs
            metadata: Optional metadata for the message

        Returns:
            Created ChatluckMessage object

        Raises:
            Exception: If sending fails
        """
        data = {
            "channel_id": channel_id,
            "content": content
        }

        if user_id:
            data["user_id"] = user_id
        if attachments:
            data["attachments"] = attachments
        if metadata:
            data["metadata"] = metadata

        response = await self._make_request("POST", "/messages", data=data)
        return ChatluckMessage(**response)

    async def list_messages(
        self,
        channel_id: str,
        limit: int = 50,
        offset: str = None,
        before: str = None,
        after: str = None
    ) -> List[ChatluckMessage]:
        """
        List messages from a channel.

        Args:
            channel_id: Channel ID
            limit: Maximum number of messages to return
            offset: Pagination offset
            before: Get messages before this message ID
            after: Get messages after this message ID

        Returns:
            List of ChatluckMessage objects

        Raises:
            Exception: If retrieval fails
        """
        params = {"channel_id": channel_id, "limit": limit}

        if offset:
            params["offset"] = offset
        if before:
            params["before"] = before
        if after:
            params["after"] = after

        response = await self._make_request("GET", "/messages", params=params)
        messages = response.get("messages", [])

        return [ChatluckMessage(**m) for m in messages]

    async def create_channel(
        self,
        name: str,
        description: Optional[str] = None,
        is_private: bool = False,
        member_ids: Optional[List[str]] = None
    ) -> ChatluckChannel:
        """
        Create a new channel.

        Args:
            name: Channel name
            description: Optional channel description
            is_private: Whether channel is private
            member_ids: Optional list of member IDs to add

        Returns:
            Created ChatluckChannel object

        Raises:
            Exception: If creation fails
        """
        data = {"name": name}

        if description:
            data["description"] = description
        if is_private:
            data["is_private"] = is_private
        if member_ids:
            data["member_ids"] = member_ids

        response = await self._make_request("POST", "/channels", data=data)
        return ChatluckChannel(**response)

    async def list_channels(
        self,
        limit: int = 50,
        offset: str = None,
        include_private: bool = False
    ) -> List[ChatluckChannel]:
        """
        List channels.

        Args:
            limit: Maximum number of channels
            offset: Pagination offset
            include_private: Whether to include private channels

        Returns:
            List of ChatluckChannel objects

        Raises:
            Exception: If retrieval fails
        """
        params = {"limit": limit}

        if offset:
            params["offset"] = offset
        if include_private:
            params["include_private"] = "true"

        response = await self._make_request("GET", "/channels", params=params)
        channels = response.get("channels", [])

        return [ChatluckChannel(**c) for c in channels]

    async def get_user_info(self, user_id: str) -> ChatluckUser:
        """
        Get user information.

        Args:
            user_id: User ID

        Returns:
            ChatluckUser object

        Raises:
            Exception: If retrieval fails
        """
        response = await self._make_request("GET", f"/users/{user_id}")
        return ChatluckUser(**response)

    async def list_users(
        self,
        limit: int = 50,
        offset: str = None,
        status: Optional[str] = None
    ) -> List[ChatluckUser]:
        """
        List users.

        Args:
            limit: Maximum number of users
            offset: Pagination offset
            status: Filter by status (active, inactive)

        Returns:
            List of ChatluckUser objects

        Raises:
            Exception: If retrieval fails
        """
        params = {"limit": limit}

        if offset:
            params["offset"] = offset
        if status:
            params["status"] = status

        response = await self._make_request("GET", "/users", params=params)
        users = response.get("users", [])

        return [ChatluckUser(**u) for u in users]

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle webhook events from Chatluck.

        Args:
            webhook_data: Webhook payload

        Returns:
            Processed event data

        Supported triggers:
        - New Message
        - User Joined
        """
        event_type = webhook_data.get("event_type", "unknown")

        result = {
            "event_type": event_type,
            "raw_data": webhook_data
        }

        if event_type == "message.created":
            result["message"] = ChatluckMessage(**webhook_data.get("message", {}))
        elif event_type == "user.joined":
            result["user"] = ChatluckUser(**webhook_data.get("user", {}))
            result["channel_id"] = webhook_data.get("channel_id")

        return result