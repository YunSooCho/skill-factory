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


@dataclass
class DiscordThread:
    """Discord thread model"""
    id: str
    name: str
    type: int
    guild_id: str
    parent_id: Optional[str] = None
    owner_id: Optional[str] = None
    message_count: int = 0
    member_count: int = 0
    archived: bool = False

@dataclass
class DiscordInvite:
    """Discord invite URL model"""
    code: str
    guild: Optional[Dict[str, Any]] = None
    channel: Optional[Dict[str, Any]] = None
    inviter: Optional[Dict[str, Any]] = None
    max_age: int = 0
    max_uses: int = 0
    uses: int = 0
    
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
        msg_fields = {k: v for k, v in response.items() if k in DiscordMessage.__annotations__}
        return DiscordMessage(**msg_fields)

    async def send_message_to_thread(
        self,
        thread_id: str,
        content: str,
        embeds: Optional[List[Dict[str, Any]]] = None,
        tts: bool = False
    ) -> DiscordMessage:
        """Send a message to a thread (which acts like a channel)."""
        return await self.send_message(thread_id, content, embeds, tts)

    async def send_file(
        self,
        channel_id: str,
        file_path: str,
        content: Optional[str] = None
    ) -> DiscordMessage:
        """Send a file with optional content to a channel."""
        await self._check_rate_limit()
        url = f"{self.BASE_URL}/channels/{channel_id}/messages"
        
        data = aiohttp.FormData()
        if content:
            data.add_field('payload_json', '{"content": "%s"}' % content, content_type='application/json')
            
        import os
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            file_data = f.read()
            
        data.add_field('files[0]', file_data, filename=filename)

        async with self.session.post(url, headers={"Authorization": f"Bot {self.bot_token}"}, data=data) as response:
            try:
                result = await response.json()
            except:
                result = {}

            if response.status not in [200, 201]:
                error_msg = result.get("message", result.get("error", "Unknown error"))
                raise Exception(f"Discord API error: {response.status} - {error_msg}")

            msg_fields = {k: v for k, v in result.items() if k in DiscordMessage.__annotations__}
            return DiscordMessage(**msg_fields)

    async def download_message_file(self, url: str, save_path: str) -> str:
        """Download a file from a message attachment URL."""
        async with self.session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Failed to download file: HTTP {response.status}")
                
            file_data = await response.read()
            with open(save_path, 'wb') as f:
                f.write(file_data)
                
            return save_path

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
        channel_fields = {k: v for k, v in response.items() if k in DiscordChannel.__annotations__}
        return DiscordChannel(**channel_fields)

    async def get_guild_info(self, guild_id: str) -> DiscordGuild:
        """Get guild (server) information."""
        response = await self._make_request("GET", f"/guilds/{guild_id}")
        guild_fields = {k: v for k, v in response.items() if k in DiscordGuild.__annotations__}
        return DiscordGuild(**guild_fields)

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
        role_fields = {k: v for k, v in response.items() if k in DiscordRole.__annotations__}
        return DiscordRole(**role_fields)

    async def get_role_info(self, guild_id: str, role_id: str) -> Optional[DiscordRole]:
        """Get role information from a guild. (Searches through all roles)"""
        response = await self._make_request("GET", f"/guilds/{guild_id}/roles")
        # response is a list of roles
        for role_data in response:
            if role_data.get("id") == role_id:
                role_fields = {k: v for k, v in role_data.items() if k in DiscordRole.__annotations__}
                return DiscordRole(**role_fields)
        return None

    async def get_member_info(self, guild_id: str, user_id: str) -> DiscordMember:
        """Get member information in a guild."""
        response = await self._make_request("GET", f"/guilds/{guild_id}/members/{user_id}")
        member_fields = {k: v for k, v in response.items() if k in DiscordMember.__annotations__}
        return DiscordMember(**member_fields)

    async def search_guild_members(self, guild_id: str, query: str, limit: int = 1) -> List[DiscordMember]:
        """Search members in a guild."""
        response = await self._make_request("GET", f"/guilds/{guild_id}/members/search", params={"query": query, "limit": limit})
        members = []
        for member_data in response:
            member_fields = {k: v for k, v in member_data.items() if k in DiscordMember.__annotations__}
            members.append(DiscordMember(**member_fields))
        return members

    async def add_member_role(self, guild_id: str, user_id: str, role_id: str) -> bool:
        """Add a specific role to a user."""
        await self._make_request("PUT", f"/guilds/{guild_id}/members/{user_id}/roles/{role_id}")
        return True

    async def remove_member_role(self, guild_id: str, user_id: str, role_id: str) -> bool:
        """Remove a role from a user."""
        await self._make_request("DELETE", f"/guilds/{guild_id}/members/{user_id}/roles/{role_id}")
        return True

    async def overwrite_member_roles(self, guild_id: str, user_id: str, role_ids: List[str]) -> bool:
        """Overwrite member's roles completely."""
        await self._make_request("PATCH", f"/guilds/{guild_id}/members/{user_id}", data={"roles": role_ids})
        return True

    async def kick_member(self, guild_id: str, user_id: str) -> bool:
        """Remove a user from the server (Kick)."""
        await self._make_request("DELETE", f"/guilds/{guild_id}/members/{user_id}")
        return True

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

    async def create_dm_channel(self, recipient_id: str) -> DiscordChannel:
        """Create a direct message channel with a user."""
        response = await self._make_request("POST", "/users/@me/channels", data={"recipient_id": recipient_id})
        channel_fields = {k: v for k, v in response.items() if k in DiscordChannel.__annotations__}
        return DiscordChannel(**channel_fields)

    async def delete_channel(self, channel_id: str) -> DiscordChannel:
        """Delete or close a channel/thread."""
        response = await self._make_request("DELETE", f"/channels/{channel_id}")
        channel_fields = {k: v for k, v in response.items() if k in DiscordChannel.__annotations__}
        return DiscordChannel(**channel_fields)

    async def rename_channel(self, channel_id: str, new_name: str) -> DiscordChannel:
        """Rename a channel."""
        response = await self._make_request("PATCH", f"/channels/{channel_id}", data={"name": new_name})
        channel_fields = {k: v for k, v in response.items() if k in DiscordChannel.__annotations__}
        return DiscordChannel(**channel_fields)

    async def create_channel_invite(self, channel_id: str, max_age: int = 86400, max_uses: int = 0) -> DiscordInvite:
        """Create an invite URL for a channel."""
        data = {"max_age": max_age, "max_uses": max_uses}
        response = await self._make_request("POST", f"/channels/{channel_id}/invites", data=data)
        invite_fields = {k: v for k, v in response.items() if k in DiscordInvite.__annotations__}
        return DiscordInvite(**invite_fields)

    async def create_forum_thread(self, channel_id: str, name: str, message_content: str) -> DiscordThread:
        """Create a thread in a forum channel with an initial message."""
        data = {
            "name": name,
            "message": {"content": message_content}
        }
        response = await self._make_request("POST", f"/channels/{channel_id}/threads", data=data)
        thread_fields = {k: v for k, v in response.items() if k in DiscordThread.__annotations__}
        return DiscordThread(**thread_fields)

    async def create_thread_from_message(self, channel_id: str, message_id: str, name: str) -> DiscordThread:
        """Create a thread from an existing message."""
        data = {"name": name}
        response = await self._make_request("POST", f"/channels/{channel_id}/messages/{message_id}/threads", data=data)
        thread_fields = {k: v for k, v in response.items() if k in DiscordThread.__annotations__}
        return DiscordThread(**thread_fields)

    async def get_guild_channels(self, guild_id: str) -> List[DiscordChannel]:
        """Get list of channels in a server."""
        response = await self._make_request("GET", f"/guilds/{guild_id}/channels")
        channels = []
        for ch_data in response:
            ch_fields = {k: v for k, v in ch_data.items() if k in DiscordChannel.__annotations__}
            channels.append(DiscordChannel(**ch_fields))
        return channels

    async def get_active_threads(self, guild_id: str) -> List[DiscordThread]:
        """Get list of active threads in a server."""
        response = await self._make_request("GET", f"/guilds/{guild_id}/threads/active")
        threads = []
        for th_data in response.get("threads", []):
            th_fields = {k: v for k, v in th_data.items() if k in DiscordThread.__annotations__}
            threads.append(DiscordThread(**th_fields))
        return threads

    async def get_channel_messages(self, channel_id: str, limit: int = 50) -> List[DiscordMessage]:
        """Get list of messages in a text channel or thread."""
        response = await self._make_request("GET", f"/channels/{channel_id}/messages", params={"limit": limit})
        messages = []
        for msg_data in response:
            msg_fields = {k: v for k, v in msg_data.items() if k in DiscordMessage.__annotations__}
            messages.append(DiscordMessage(**msg_fields))
        return messages

    async def get_thread_messages(self, thread_id: str, limit: int = 50) -> List[DiscordMessage]:
        """Get list of messages in a thread (alias for get_channel_messages)."""
        return await self.get_channel_messages(thread_id, limit)

    async def get_message(self, channel_id: str, message_id: str) -> DiscordMessage:
        """Get a specific message."""
        response = await self._make_request("GET", f"/channels/{channel_id}/messages/{message_id}")
        msg_fields = {k: v for k, v in response.items() if k in DiscordMessage.__annotations__}
        return DiscordMessage(**msg_fields)

    async def custom_connect(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Any:
        """Custom raw request wrapper for external system integration (e.g., Yoom)."""
        return await self._make_request(method, endpoint, data=data, params=params)

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook/gateway events."""
        event_type = webhook_data.get("t", "unknown")

        result = {"event_type": event_type, "raw_data": webhook_data}
        d_data = webhook_data.get("d", {}) or {}

        if event_type == "MESSAGE_CREATE":
            # 必要なフィールドだけを抽出
            msg_fields = {k: v for k, v in d_data.items() if k in DiscordMessage.__annotations__}
            result["message"] = DiscordMessage(**msg_fields)
            result["guild_id"] = d_data.get("guild_id")
        elif event_type == "GUILD_MEMBER_ADD":
            member_fields = {k: v for k, v in d_data.items() if k in DiscordMember.__annotations__}
            result["member"] = DiscordMember(**member_fields)
            result["guild_id"] = d_data.get("guild_id")

        return result