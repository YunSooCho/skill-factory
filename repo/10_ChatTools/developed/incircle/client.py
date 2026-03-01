"""
Incircle API Client

Incircle is a team communication and collaboration platform for distributed teams.

API Actions (6):
1. Send Message
2. List Channels
3. Create Channel
4. Get Channel
5. List Members
6. Invite Member

Triggers (2):
- New Message
- Member Invited

Authentication: API Token
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class IncircleMessage:
    """Incircle message model"""
    id: str
    channel_id: str
    user_id: str
    content: str
    created_at: str
    reactions: List[Dict[str, Any]] = field(default_factory=list)
    attachments: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class IncircleChannel:
    """Incircle channel model"""
    id: str
    name: str
    description: Optional[str] = None
    type: str
    created_at: str
    member_count: int = 0
    is_private: bool = False


@dataclass
class IncircleMember:
    """Incircle member model"""
    id: str
    name: str
    email: Optional[str] = None
    role: str = "member"
    avatar_url: Optional[str] = None
    status: str = "active"


class IncircleClient:
    """
    Incircle API client for team communication.
    """

    BASE_URL = "https://api.incircle.io/v1"
    RATE_LIMIT = 20  # requests per second

    def __init__(self, api_token: str):
        """Initialize Incircle client."""
        self.api_token = api_token
        self.session = None
        self._last_request_time = datetime.now()
        self._headers = {
            "Authorization": f"Bearer {api_token}",
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
                raise Exception(f"Incircle API error: {response.status} - {error_msg}")

            return result

    async def send_message(
        self,
        channel_id: str,
        content: str,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> IncircleMessage:
        """Send a message to a channel."""
        data = {"content": content}

        if attachments:
            data["attachments"] = attachments

        response = await self._make_request("POST", f"/channels/{channel_id}/messages", data=data)
        return IncircleMessage(**response)

    async def list_channels(
        self,
        channel_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[IncircleChannel]:
        """List channels."""
        params = {"limit": limit, "offset": offset}

        if channel_type:
            params["type"] = channel_type

        response = await self._make_request("GET", "/channels", params=params)
        channels = response.get("channels", [])

        return [IncircleChannel(**c) for c in channels]

    async def create_channel(
        self,
        name: str,
        description: Optional[str] = None,
        channel_type: str = "public",
        is_private: bool = False
    ) -> IncircleChannel:
        """Create a new channel."""
        data = {
            "name": name,
            "type": channel_type,
            "is_private": is_private
        }

        if description:
            data["description"] = description

        response = await self._make_request("POST", "/channels", data=data)
        return IncircleChannel(**response)

    async def get_channel(self, channel_id: str) -> IncircleChannel:
        """Get channel details."""
        response = await self._make_request("GET", f"/channels/{channel_id}")
        return IncircleChannel(**response)

    async def list_members(
        self,
        channel_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[IncircleMember]:
        """List members (channel members or all members)."""
        params = {"limit": limit, "offset": offset}

        endpoint = "/members"
        if channel_id:
            endpoint = f"/channels/{channel_id}/members"

        response = await self._make_request("GET", endpoint, params=params)
        members = response.get("members", [])

        return [IncircleMember(**m) for m in members]

    async def invite_member(
        self,
        channel_id: str,
        email: str,
        role: str = "member"
    ) -> IncircleMember:
        """Invite a member to a channel."""
        data = {"email": email, "role": role}

        response = await self._make_request("POST", f"/channels/{channel_id}/members", data=data)
        return IncircleMember(**response)

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook events."""
        event_type = webhook_data.get("event_type", "unknown")

        result = {"event_type": event_type, "raw_data": webhook_data}

        if event_type == "message.created":
            result["message"] = IncircleMessage(**webhook_data.get("message", {}))
            result["channel_id"] = webhook_data.get("channel_id")
        elif event_type == "member.invited":
            result["member"] = IncircleMember(**webhook_data.get("member", {}))
            result["channel_id"] = webhook_data.get("channel_id")

        return result