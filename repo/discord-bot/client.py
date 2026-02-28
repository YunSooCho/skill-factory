"""
Discord Bot API Client

Discord Bot provides messaging, slash commands, and server management for Discord.

API Actions (6):
1. Send Message
2. Create Channel
3. Get Guild Info
4. Create Role
5. Get Member Info
6. Modify Member

Triggers (2):
- Message Created
- Member Joined

Authentication: Bot Token
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class DiscordMessage:
    """Discord message model"""
    id: str
    channel_id: str
    author: Dict[str, Any]
    content: str
    timestamp: str
    edited_timestamp: Optional[str] = None
    mentions: List[Dict[str, Any]] = field(default_factory=list)
    embeds: List[Dict[str, Any]] = field(default_factory=list)
    attachments: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class DiscordChannel:
    """Discord channel model"""
    id: str
    name: str
    type: int
    guild_id: str
    position: int
    parent_id: Optional[str] = None
    nsfw: bool = False
    topic: Optional[str] = None


@dataclass
class DiscordGuild:
    """Discord guild (server) model"""
    id: str
    name: str
    owner_id: str
    region: Optional[str] = None
    afk_channel_id: Optional[str] = None
    afk_timeout: int = 0
    member_count: int = 0
    roles: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class DiscordRole:
    """Discord role model"""
    id: str
    name: str
    color: int
    hoist: bool
    position: int
    permissions: str
    managed: bool
    mentionable: bool


@dataclass
class DiscordMember:
    """Discord member model"""
    user: Dict[str, Any]
    nick: Optional[str] = None
    roles: List[str] = field(default_factory=list)
    joined_at: Optional[str] = None
    premium_since: Optional[str] = None


class DiscordBotClient:
    """
    Discord Bot API client for server management.
    """

    BASE_URL = "https://discord.com/api/v10"
    RATE_LIMIT = 50  # requests per second (varies by endpoint)

    def __init__(self, bot_token: str):
        """
        Initialize Discord Bot client.

        Args:
            bot_token: Your Discord bot token
        """
        self.bot_token = bot_token
        self.session = None
        self._last_request_time = datetime.now()
        self._headers = {
            "Authorization": f"Bot {bot_token}",
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

            if response.status not in [200, 201, 204]:
                error_msg = result.get("message", result.get("error", "Unknown error"))
                raise Exception(f"Discord API error: {response.status} - {error_msg}")

            return result

    async def send_message(
        self,
        channel_id: str,
        content: str,
        embeds: Optional[List[Dict[str, Any]]] = None,
        tts: bool = False
    ) -> DiscordMessage:
        """Send a message to a channel."""
        data = {"content": content, "tts": tts}

        if embeds:
            data["embeds"] = embeds

        response = await self._make_request("POST", f"/channels/{channel_id}/messages", data=data)
        return DiscordMessage(**response)

    async def create_channel(
        self,
        guild_id: str,
        name: str,
        channel_type: int = 0,
        parent_id: Optional[str] = None,
        topic: Optional[str] = None
    ) -> DiscordChannel:
        """Create a new channel in a guild."""
        data = {"name": name, "type": channel_type}

        if parent_id:
            data["parent_id"] = parent_id
        if topic:
            data["topic"] = topic

        response = await self._make_request("POST", f"/guilds/{guild_id}/channels", data=data)
        return DiscordChannel(**response)

    async def get_guild_info(self, guild_id: str) -> DiscordGuild:
        """Get guild (server) information."""
        response = await self._make_request("GET", f"/guilds/{guild_id}")
        return DiscordGuild(**response)

    async def create_role(
        self,
        guild_id: str,
        name: str,
        color: int = 0,
        hoist: bool = False,
        mentionable: bool = False
    ) -> DiscordRole:
        """Create a new role in a guild."""
        data = {
            "name": name,
            "color": color,
            "hoist": hoist,
            "mentionable": mentionable
        }

        response = await self._make_request("POST", f"/guilds/{guild_id}/roles", data=data)
        return DiscordRole(**response)

    async def get_member_info(self, guild_id: str, user_id: str) -> DiscordMember:
        """Get member information in a guild."""
        response = await self._make_request("GET", f"/guilds/{guild_id}/members/{user_id}")
        return DiscordMember(**response)

    async def modify_member(
        self,
        guild_id: str,
        user_id: str,
        nick: Optional[str] = None,
        roles: Optional[List[str]] = None,
        mute: Optional[bool] = None
    ) -> bool:
        """Modify member information."""
        data = {}

        if nick is not None:
            data["nick"] = nick
        if roles is not None:
            data["roles"] = roles
        if mute is not None:
            data["mute"] = mute

        await self._make_request("PATCH", f"/guilds/{guild_id}/members/{user_id}", data=data)
        return True

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook/gateway events."""
        event_type = webhook_data.get("t", "unknown")

        result = {"event_type": event_type, "raw_data": webhook_data}

        if event_type == "MESSAGE_CREATE":
            result["message"] = DiscordMessage(**webhook_data.get("d", {}))
            result["guild_id"] = webhook_data.get("d", {}).get("guild_id")
        elif event_type == "GUILD_MEMBER_ADD":
            result["member"] = DiscordMember(**webhook_data.get("d", {}))
            result["guild_id"] = webhook_data.get("d", {}).get("guild_id")

        return result