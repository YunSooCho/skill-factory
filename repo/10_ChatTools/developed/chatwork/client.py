"""
Chatwork API Client

Chatwork is a Japanese team chat and collaboration platform.

API Actions (6):
1. Send Message
2. List Messages
3. Create Task
4. Get My Tasks
5. Get Room Info
6. List Rooms

Triggers (2):
- New Message
- Task Completed

Authentication: API Token
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class ChatworkMessage:
    """Chatwork message model"""
    message_id: str
    account_id: str
    room_id: str
    body: str
    send_time: int
    update_time: int
    account: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatworkRoom:
    """Chatwork room model"""
    room_id: int
    name: str
    type: str
    role: str
    sticky: bool
    unread_num: int
    mention_num: int
    mytask_num: int
    message_num: int
    file_num: int
    task_num: int
    icon_path: str
    last_update_time: int
    description: str = ""


@dataclass
class ChatworkTask:
    """Chatwork task model"""
    task_id: int
    account: Dict[str, Any]
    assigned_by_account: Dict[str, Any]
    room_id: int
    status: str
    body: str
    limit_time: int
    limit_type: str
    created_at: int
    updated_at: int


@dataclass
class ChatworkAccount:
    """Chatwork account model"""
    account_id: int
    name: str
    avatar_image_url: str


class ChatworkClient:
    """
    Chatwork API client for team collaboration operations.
    """

    BASE_URL = "https://api.chatwork.com/v2"
    RATE_LIMIT = 5  # requests per second (Chatwork limit)

    def __init__(self, api_token: str):
        """
        Initialize Chatwork client.

        Args:
            api_token: Your Chatwork API token
        """
        self.api_token = api_token
        self.session = None
        self._last_request_time = datetime.now()
        self._headers = {
            "X-ChatworkToken": api_token,
            "Content-Type": "application/x-www-form-urlencoded"
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
        params: Optional[Dict[str, Any]] = None,
        json_body: bool = False
    ) -> Any:
        """
        Make API request with rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            json_body: Whether to send as JSON

        Returns:
            Response JSON or list

        Raises:
            Exception: If request fails
        """
        await self._check_rate_limit()

        url = f"{self.BASE_URL}{endpoint}"

        headers = self._headers.copy()
        if json_body:
            headers["Content-Type"] = "application/json"

        async with self.session.request(
            method,
            url,
            headers=headers,
            data=data,
            json=data if json_body else None,
            params=params
        ) as response:
            if response.status not in [200, 201]:
                try:
                    result = await response.json()
                except:
                    result = {}
                error_msg = result.get("errors", result.get("message", "Unknown error"))
                raise Exception(
                    f"Chatwork API error: {response.status} - {error_msg}"
                )

            try:
                return await response.json()
            except:
                return await response.text()

    async def send_message(
        self,
        room_id: int,
        body: str,
        self_unread: bool = False
    ) -> str:
        """
        Send a message to a room.

        Args:
            room_id: Room ID
            body: Message body
            self_unread: Whether to mark as unread for sender

        Returns:
            Message ID

        Raises:
            Exception: If sending fails
        """
        data = {
            "body": body,
            "self_unread": 1 if self_unread else 0
        }

        result = await self._make_request("POST", f"/rooms/{room_id}/messages", data=data)
        return result.get("message_id")

    async def list_messages(
        self,
        room_id: int,
        force: bool = False
    ) -> List[ChatworkMessage]:
        """
        List messages from a room.

        Args:
            room_id: Room ID
            force: Whether to force refresh from server

        Returns:
            List of ChatworkMessage objects

        Raises:
            Exception: If retrieval fails
        """
        params = {"force": 1 if force else 0}
        result = await self._make_request("GET", f"/rooms/{room_id}/messages", params=params)

        if not isinstance(result, list):
            return []

        return [ChatworkMessage(**m) for m in result]

    async def create_task(
        self,
        room_id: int,
        body: str,
        to_account_ids: List[int],
        limit_time: Optional[int] = None,
        limit_type: str = "none"
    ) -> List[int]:
        """
        Create a task in a room.

        Args:
            room_id: Room ID
            body: Task description
            to_account_ids: List of account IDs to assign task to
            limit_time: Optional unix timestamp for task deadline
            limit_type: Limit type (none, date, time)

        Returns:
            Created task ID

        Raises:
            Exception: If creation fails
        """
        data = {
            "body": body,
            "to_account_ids": to_account_ids,
            "limit_type": limit_type
        }

        if limit_time:
            data["limit_time"] = limit_time

        result = await self._make_request("POST", f"/rooms/{room_id}/tasks", data=data)
        return [task.get("task_id") for task in result.get("task_ids", [])]

    async def get_my_tasks(
        self,
        status: Optional[str] = None
    ) -> List[ChatworkTask]:
        """
        Get tasks assigned to current user.

        Args:
            status: Filter by status (open, done)

        Returns:
            List of ChatworkTask objects

        Raises:
            Exception: If retrieval fails
        """
        params = {}
        if status:
            params["status"] = status

        result = await self._make_request("GET", "/my/tasks", params=params)

        if not isinstance(result, list):
            return []

        return [ChatworkTask(**t) for t in result]

    async def get_room_info(self, room_id: int) -> ChatworkRoom:
        """
        Get information about a room.

        Args:
            room_id: Room ID

        Returns:
            ChatworkRoom object

        Raises:
            Exception: If retrieval fails
        """
        result = await self._make_request("GET", f"/rooms/{room_id}")
        return ChatworkRoom(**result)

    async def list_rooms(self) -> List[ChatworkRoom]:
        """
        List all accessible rooms.

        Returns:
            List of ChatworkRoom objects

        Raises:
            Exception: If retrieval fails
        """
        result = await self._make_request("GET", "/rooms")

        if not isinstance(result, list):
            return []

        return [ChatworkRoom(**r) for r in result]

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle webhook events from Chatwork.

        Args:
            webhook_data: Webhook payload

        Returns:
            Processed event data

        Supported triggers:
        - New Message
        - Task Completed
        """
        webhook_event = webhook_data.get("webhook_event", {})
        event_type = webhook_event.get("event_type", "unknown")

        result = {
            "event_type": event_type,
            "raw_data": webhook_data
        }

        if event_type == "message_created":
            result["message"] = ChatworkMessage(**webhook_event)
            result["room_id"] = webhook_event.get("room_id")
        elif event_type == "task_created":
            result["task"] = ChatworkTask(**webhook_event)
            result["room_id"] = webhook_event.get("room_id")

        return result