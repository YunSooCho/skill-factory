"""
Jandi API Client

Jandi is a Korean team collaboration and messaging platform.

API Actions (6):
1. Send Message
2. List Topics
3. Get Topic
4. Create Entity
5. List Entities
6. Get Entity

Triggers (2):
- Message Created
- Entity Created

Authentication: API Key
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class JandiMessage:
    """Jandi message model"""
    id: str
    topic_id: str
    writer_id: str
    content: str
    created_time: str
    mention_ids: List[str] = field(default_factory=list)
    attachments: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class JandiTopic:
    """Jandi topic model"""
    id: str
    name: str
    type: str
    created_time: str
    member_count: int = 0
    is_public: bool = True
    description: Optional[str] = None


@dataclass
class JandiEntity:
    """Jandi entity model"""
    id: str
    topic_id: str
    title: str
    content: Optional[str] = None
    creator_id: str = None
    created_time: str = None
    status: str = "active"


@dataclass
class JandiUser:
    """Jandi user model"""
    id: str
    name: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    status: str = "active"


class JandiClient:
    """
    Jandi API client for team collaboration.
    """

    BASE_URL = "https://api.jandi.com/connect"
    RATE_LIMIT = 15  # requests per second

    def __init__(self, api_key: str):
        """Initialize Jandi client."""
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
                raise Exception(f"Jandi API error: {response.status} - {error_msg}")

            return result

    async def send_message(
        self,
        topic_id: str,
        body: str,
        connect_color: Optional[str] = None,
        connect_info: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Send a message to a topic."""
        data = {
            "body": body,
            "connectColor": connect_color or "#FAC11B",
            "connectInfo": connect_info or []
        }

        response = await self._make_request("POST", f"/topics/{topic_id}/messages", data=data)
        return response.get("message_id")

    async def list_topics(
        self,
        topic_type: Optional[str] = None,
        limit: int = 50
    ) -> List[JandiTopic]:
        """List topics."""
        params = {"limit": limit}

        if topic_type:
            params["type"] = topic_type

        response = await self._make_request("GET", "/topics", params=params)
        topics = response.get("topics", [])

        return [JandiTopic(**t) for t in topics]

    async def get_topic(self, topic_id: str) -> JandiTopic:
        """Get topic details."""
        response = await self._make_request("GET", f"/topics/{topic_id}")
        return JandiTopic(**response)

    async def create_entity(
        self,
        topic_id: str,
        title: str,
        content: Optional[str] = None
    ) -> JandiEntity:
        """Create an entity in a topic."""
        data = {"title": title}

        if content:
            data["content"] = content

        response = await self._make_request("POST", f"/topics/{topic_id}/entities", data=data)
        return JandiEntity(**response)

    async def list_entities(
        self,
        topic_id: str,
        limit: int = 50,
        status: Optional[str] = None
    ) -> List[JandiEntity]:
        """List entities in a topic."""
        params = {"limit": limit}

        if status:
            params["status"] = status

        response = await self._make_request("GET", f"/topics/{topic_id}/entities", params=params)
        entities = response.get("entities", [])

        return [JandiEntity(**e) for e in entities]

    async def get_entity(self, topic_id: str, entity_id: str) -> JandiEntity:
        """Get entity details."""
        response = await self._make_request("GET", f"/topics/{topic_id}/entities/{entity_id}")
        return JandiEntity(**response)

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook events."""
        event_type = webhook_data.get("event", {}).get("type", "unknown")

        result = {"event_type": event_type, "raw_data": webhook_data}

        if event_type == "message.created":
            result["message"] = JandiMessage(**webhook_data.get("event", {}).get("message", {}))
            result["topic_id"] = webhook_data.get("event", {}).get("topic_id")
        elif event_type == "entity.created":
            result["entity"] = JandiEntity(**webhook_data.get("event", {}).get("entity", {}))
            result["topic_id"] = webhook_data.get("event", {}).get("topic_id")

        return result