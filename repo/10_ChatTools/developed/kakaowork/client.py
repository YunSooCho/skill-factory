"""
Kakaowork API Client

Kakaowork is a Korean enterprise messaging platform for business communication.

API Actions (6):
1. Send Message
2. Get Messages
3. Get Users
4. Get Departments
5. Create Task
6. Get Tasks

Triggers (2):
- Message Created
- Task Created

Authentication: API Key
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class KakaoworkMessage:
    """Kakaowork message model"""
    message_id: str
    conversation_id: str
    user_id: str
    content: str
    created_at: str
    message_type: str = "text"
    attachments: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class KakaoworkUser:
    """Kakaowork user model"""
    user_id: str
    name: str
    email: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    avatar_url: Optional[str] = None
    status: str = "active"


@dataclass
class KakaoworkDepartment:
    """Kakaowork department model"""
    department_id: str
    name: str
    parent_id: Optional[str] = None
    member_count: int = 0


@dataclass
class KakaoworkTask:
    """Kakaowork task model"""
    task_id: str
    title: str
    description: Optional[str] = None
    assignee_id: str
    due_date: Optional[str] = None
    status: str = "pending"
    created_at: str = None


class KakaoworkClient:
    """
    Kakaowork API client for enterprise messaging.
    """

    BASE_URL = "https://api.kakaowork.com/v1/api"
    RATE_LIMIT = 10  # requests per second

    def __init__(self, api_key: str):
        """Initialize Kakaowork client."""
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
                error_msg = result.get("error", {}).get("message", "Unknown error")
                raise Exception(f"Kakaowork API error: {response.status} - {error_msg}")

            return result

    async def send_message(
        self,
        user_id: str,
        content: str,
        blocks: Optional[List[Dict[str, Any]]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Send a message to a user."""
        data = {
            "user_id": user_id,
            "text": content
        }

        if blocks:
            data["blocks"] = blocks
        if attachments:
            data["attachments"] = attachments

        response = await self._make_request("POST", "/messages", data=data)
        return response.get("message_id")

    async def get_messages(
        self,
        conversation_id: str,
        limit: int = 50,
        cursor: Optional[str] = None
    ) -> List[KakaoworkMessage]:
        """Get messages from a conversation."""
        params = {
            "conversation_id": conversation_id,
            "limit": limit
        }

        if cursor:
            params["cursor"] = cursor

        response = await self._make_request("GET", "/messages.list", params=params)
        messages = response.get("messages", [])

        return [KakaoworkMessage(**m) for m in messages]

    async def get_users(
        self,
        department_id: Optional[str] = None,
        limit: int = 100,
        cursor: Optional[str] = None
    ) -> List[KakaoworkUser]:
        """Get users (optionally filtered by department)."""
        params = {"limit": limit}

        if department_id:
            params["department_id"] = department_id
        if cursor:
            params["cursor"] = cursor

        response = await self._make_request("GET", "/users.list", params=params)
        users = response.get("users", [])

        return [KakaoworkUser(**u) for u in users]

    async def get_departments(
        self,
        limit: int = 100,
        cursor: Optional[str] = None
    ) -> List[KakaoworkDepartment]:
        """Get departments."""
        params = {"limit": limit}

        if cursor:
            params["cursor"] = cursor

        response = await self._make_request("GET", "/departments.list", params=params)
        departments = response.get("departments", [])

        return [KakaoworkDepartment(**d) for d in departments]

    async def create_task(
        self,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> KakaoworkTask:
        """Create a task for a user."""
        data = {
            "user_id": user_id,
            "title": title
        }

        if description:
            data["description"] = description
        if due_date:
            data["due_date"] = due_date

        response = await self._make_request("POST", "/tasks", data=data)
        return KakaoworkTask(**response)

    async def get_tasks(
        self,
        user_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        cursor: Optional[str] = None
    ) -> List[KakaoworkTask]:
        """Get tasks (optionally filtered by user and status)."""
        params = {"limit": limit}

        if user_id:
            params["user_id"] = user_id
        if status:
            params["status"] = status
        if cursor:
            params["cursor"] = cursor

        response = await self._make_request("GET", "/tasks.list", params=params)
        tasks = response.get("tasks", [])

        return [KakaoworkTask(**t) for t in tasks]

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook events."""
        event_type = webhook_data.get("type", "unknown")

        result = {"event_type": event_type, "raw_data": webhook_data}

        if event_type == "message.created":
            result["message"] = KakaoworkMessage(**webhook_data.get("message", {}))
            result["conversation_id"] = webhook_data.get("conversation_id")
        elif event_type == "task.created":
            result["task"] = KakaoworkTask(**webhook_data.get("task", {}))

        return result