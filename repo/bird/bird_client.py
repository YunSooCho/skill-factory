"""
Bird API Client

Omnichannel messaging platform for managing:
- Conversations
- Contacts
- Participants
- Channels
- Messages

API Actions (16):
Full CRUD for conversations, contacts, messages, participants
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Contact:
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    custom_data: Optional[Dict[str, Any]] = None


@dataclass
class Conversation:
    id: Optional[str] = None
    title: Optional[str] = None
    channel_type: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Message:
    id: Optional[str] = None
    conversation_id: Optional[str] = None
    sender_id: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Participant:
    id: Optional[str] = None
    conversation_id: Optional[str] = None
    participant_id: Optional[str] = None
    role: Optional[str] = None
    joined_at: Optional[str] = None


class RateLimiter:
    def __init__(self, calls_per_second: int = 10):
        self.calls_per_second = calls_per_second
        self.tokens = calls_per_second
        self.last_update = datetime.now()

    async def acquire(self):
        now = datetime.now()
        elapsed = (now - self.last_update).total_seconds()
        self.tokens = min(self.calls_per_second, self.tokens + elapsed * self.calls_per_second)
        self.last_update = now
        if self.tokens < 1:
            sleep_time = (1 - self.tokens) / self.calls_per_second
            await asyncio.sleep(sleep_time)
            self.tokens = self.calls_per_second
        else:
            self.tokens -= 1


class BirdError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}" if status_code else message)


class BirdClient:
    """Bird API Client"""

    def __init__(self, workspace_id: str, api_key: str, base_url: str = "https://api.bird.com/v1"):
        self.workspace_id = workspace_id
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self._rate_limiter = RateLimiter(calls_per_second=10)

    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        await self._rate_limiter.acquire()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method=method, url=url, headers=self._headers, json=data, params=params) as response:
                    if response.status == 204:
                        return {"status": "success"}
                    if response.status >= 400:
                        try:
                            error_data = await response.json()
                            error_msg = error_data.get("message", "Unknown error")
                        except:
                            error_msg = await response.text()
                        raise BirdError(error_msg, response.status)
                    return await response.json()
            except aiohttp.ClientError as e:
                raise BirdError(f"Network error: {str(e)}")

    # Contacts
    async def create_contact(self, data: Dict[str, Any]) -> Contact:
        response = await self._make_request("POST", f"/workspaces/{self.workspace_id}/contacts", data=data)
        return Contact(**response)

    async def get_contact(self, contact_id: str) -> Contact:
        response = await self._make_request("GET", f"/workspaces/{self.workspace_id}/contacts/{contact_id}")
        return Contact(**response)

    async def update_contact(self, contact_id: str, data: Dict[str, Any]) -> Contact:
        response = await self._make_request("PATCH", f"/workspaces/{self.workspace_id}/contacts/{contact_id}", data=data)
        return Contact(**response)

    async def delete_contact(self, contact_id: str) -> Dict[str, str]:
        await self._make_request("DELETE", f"/workspaces/{self.workspace_id}/contacts/{contact_id}")
        return {"status": "deleted", "contact_id": contact_id}

    async def list_contacts(self, **params) -> List[Contact]:
        response = await self._make_request("GET", f"/workspaces/{self.workspace_id}/contacts", params=params)
        if "data" in response:
            return [Contact(**item) for item in response["data"]]
        return []

    # Conversations
    async def create_conversation(self, data: Dict[str, Any]) -> Conversation:
        response = await self._make_request("POST", f"/workspaces/{self.workspace_id}/conversations", data=data)
        return Conversation(**response)

    async def get_conversation(self, conversation_id: str) -> Conversation:
        response = await self._make_request("GET", f"/workspaces/{self.workspace_id}/conversations/{conversation_id}")
        return Conversation(**response)

    async def delete_conversation(self, conversation_id: str) -> Dict[str, str]:
        await self._make_request("DELETE", f"/workspaces/{self.workspace_id}/conversations/{conversation_id}")
        return {"status": "deleted", "conversation_id": conversation_id}

    async def list_conversations(self, **params) -> List[Conversation]:
        response = await self._make_request("GET", f"/workspaces/{self.workspace_id}/conversations", params=params)
        if "data" in response:
            return [Conversation(**item) for item in response["data"]]
        return []

    # Messages
    async def create_conversation_message(self, conversation_id: str, data: Dict[str, Any]) -> Message:
        response = await self._make_request("POST", f"/workspaces/{self.workspace_id}/conversations/{conversation_id}/messages", data=data)
        return Message(**response)

    async def get_conversation_message(self, conversation_id: str, message_id: str) -> Message:
        response = await self._make_request("GET", f"/workspaces/{self.workspace_id}/conversations/{conversation_id}/messages/{message_id}")
        return Message(**response)

    async def search_conversation_messages(self, conversation_id: str, **params) -> List[Message]:
        response = await self._make_request("GET", f"/workspaces/{self.workspace_id}/conversations/{conversation_id}/messages", params=params)
        if "data" in response:
            return [Message(**item) for item in response["data"]]
        return []

    # Participants
    async def add_participant_to_conversation(self, conversation_id: str, data: Dict[str, Any]) -> Participant:
        response = await self._make_request("POST", f"/workspaces/{self.workspace_id}/conversations/{conversation_id}/participants", data=data)
        return Participant(**response)

    async def get_participant(self, conversation_id: str, participant_id: str) -> Participant:
        response = await self._make_request("GET", f"/workspaces/{self.workspace_id}/conversations/{conversation_id}/participants/{participant_id}")
        return Participant(**response)

    async def list_participants(self, conversation_id: str) -> List[Participant]:
        response = await self._make_request("GET", f"/workspaces/{self.workspace_id}/conversations/{conversation_id}/participants")
        if "data" in response:
            return [Participant(**item) for item in response["data"]]
        return []

    # Channels
    async def search_channels(self, **params) -> List[Dict[str, Any]]:
        response = await self._make_request("GET", f"/workspaces/{self.workspace_id}/channels", params=params)
        if "data" in response:
            return response["data"]
        return []

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "event_type": webhook_data.get("event_type", "unknown"),
            "entity_type": webhook_data.get("entity_type", "unknown"),
            "entity_id": webhook_data.get("entity_id"),
            "data": webhook_data
        }