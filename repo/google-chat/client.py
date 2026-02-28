"""
Google Chat API Client

Google Chat is Google's messaging platform for teams and workspace integration.

API Actions (6):
1. Send Message
2. List Spaces
3. Get Space
4. Create Message
5. Update Message
6. Delete Message

Triggers (2):
- Message Added
- Space Updated

Authentication: Service Account
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class GoogleChatMessage:
    """Google Chat message model"""
    name: str
    sender: Dict[str, Any]
    create_time: str
    text: Optional[str] = None
    cards: List[Dict[str, Any]] = field(default_factory=list)
    arguments: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class GoogleChatSpace:
    """Google Chat space model"""
    name: str
    display_name: str
    type: str
    single_user_bot_dms: bool = False
    threaded: bool = False


@dataclass
class GoogleChatUser:
    """Google Chat user model"""
    name: str
    display_name: str
    type: str


class GoogleChatClient:
    """
    Google Chat API client for messaging operations.
    """

    BASE_URL = "https://chat.googleapis.com/v1"
    RATE_LIMIT = 10  # requests per second

    def __init__(self, service_account_email: str, private_key: str):
        """
        Initialize Google Chat client.

        Args:
            service_account_email: Service account email
            private_key: Service account private key
        """
        self.service_account_email = service_account_email
        self.private_key = private_key
        self.session = None
        self._last_request_time = datetime.now()
        self._access_token = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        await self._get_access_token()
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

    async def _get_access_token(self):
        """Get OAuth2 access token from service account."""
        # Simplified token exchange - in production use google-auth library
        import json
        payload = {
            "iss": self.service_account_email,
            "scope": "https://www.googleapis.com/auth/chat.bot",
            "aud": "https://oauth2.googleapis.com/token",
            "iat": int(datetime.now().timestamp()),
            "exp": int(datetime.now().timestamp()) + 3600
        }

        import base64
        import hashlib

        # Simplified JWT signing (use google-auth in production)
        header = {"alg": "RS256", "typ": "JWT"}

        self._access_token = "placeholder_token"  # Use google-auth-library for real implementation

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

        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json"
        }

        async with self.session.request(
            method,
            url,
            headers=headers,
            json=data,
            params=params
        ) as response:
            try:
                result = await response.json()
            except:
                result = {}

            if response.status not in [200, 201]:
                error_msg = result.get("error", {}).get("message", "Unknown error")
                raise Exception(f"Google Chat API error: {response.status} - {error_msg}")

            return result

    async def send_message(
        self,
        space_name: str,
        text: Optional[str] = None,
        cards: Optional[List[Dict[str, Any]]] = None
    ) -> GoogleChatMessage:
        """Send a message to a space."""
        data = {}

        if text:
            data["text"] = text
        if cards:
            data["cards"] = cards

        response = await self._make_request("POST", f"/{space_name}/messages", data=data)
        return GoogleChatMessage(**response)

    async def list_spaces(
        self,
        page_size: int = 100,
        page_token: Optional[str] = None
    ) -> List[GoogleChatSpace]:
        """List accessible spaces."""
        params = {"pageSize": page_size}

        if page_token:
            params["pageToken"] = page_token

        response = await self._make_request("GET", "/spaces", params=params)
        spaces = response.get("spaces", [])

        return [GoogleChatSpace(**s) for s in spaces]

    async def get_space(self, space_name: str) -> GoogleChatSpace:
        """Get space details."""
        response = await self._make_request("GET", f"/{space_name}")
        return GoogleChatSpace(**response)

    async def create_message(
        self,
        space_name: str,
        text: Optional[str] = None,
        cards: Optional[List[Dict[str, Any]]] = None,
        thread_key: Optional[str] = None
    ) -> GoogleChatMessage:
        """Create a message in a space."""
        data = {}

        if text:
            data["text"] = text
        if cards:
            data["cards"] = cards
        if thread_key:
            data["threadKey"] = thread_key

        response = await self._make_request("POST", f"/{space_name}/messages", data=data)
        return GoogleChatMessage(**response)

    async def update_message(
        self,
        message_name: str,
        text: Optional[str] = None,
        cards: Optional[List[Dict[str, Any]]] = None
    ) -> GoogleChatMessage:
        """Update an existing message."""
        data = {}

        if text:
            data["text"] = text
        if cards:
            data["cards"] = cards

        response = await self._make_request("PUT", f"/{message_name}", data=data)
        return GoogleChatMessage(**response)

    async def delete_message(self, message_name: str) -> bool:
        """Delete a message."""
        await self._make_request("DELETE", f"/{message_name}")
        return True

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook events."""
        event_type = webhook_data.get("type", "unknown")

        result = {"event_type": event_type, "raw_data": webhook_data}

        if event_type == "MESSAGE":
            result["message"] = GoogleChatMessage(**webhook_data.get("event", {}))
        elif event_type == "UPDATED":
            result["space_name"] = webhook_data.get("name")

        return result