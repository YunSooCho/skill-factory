"""
Bird API Client

Bird provides conversation and communication management services.

Supports:
- Create Conversation
- Search Conversation Messages
- Add Participant to Conversation
- Get Participant
- List Contacts
- Create Conversation Message
- Create Contact
- Get Conversation Message
- Search Channels
- Delete Conversation
- Get Conversation
- Delete Contact
- Update Contact
- List Conversations
- Get Contact
- List Participants
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Conversation:
    """Conversation object"""
    id: str
    name: str
    participants: List[str]
    created_at: str
    updated_at: str


@dataclass
class Contact:
    """Contact object"""
    id: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Participant:
    """Participant object"""
    id: str
    user_id: str
    conversation_id: str
    role: str
    joined_at: str


@dataclass
class Message:
    """Message object"""
    id: str
    conversation_id: str
    sender_id: str
    content: str
    message_type: str
    created_at: str


@dataclass
class Channel:
    """Channel object"""
    id: str
    name: str
    description: Optional[str]
    created_at: str
    updated_at: str


class BirdAPIClient:
    """
    Bird API client for conversation and communication management.

    Authentication: API Key
    Base URL: https://api.bird.com
    """

    BASE_URL = "https://api.bird.com"

    def __init__(self, api_key: str):
        """
        Initialize Bird API client.

        Args:
            api_key: Bird API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Bird API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        url = f"{self.BASE_URL}{endpoint}"

        async with self.session.request(
            method,
            url,
            params=params,
            json=json_data
        ) as response:
            data = await response.json()

            if response.status not in [200, 201, 204]:
                raise Exception(f"Bird API error ({response.status}): {data}")

            return data

    # ==================== Conversations ====================

    async def create_conversation(
        self,
        name: str,
        participant_ids: List[str],
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Conversation:
        """
        Create a new conversation.

        Args:
            name: Conversation name
            participant_ids: List of user IDs to add as participants
            description: Optional conversation description
            metadata: Optional metadata dictionary

        Returns:
            Conversation object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {
            "name": name,
            "participants": participant_ids
        }

        if description:
            json_data["description"] = description
        if metadata:
            json_data["metadata"] = metadata

        data = await self._request("POST", "/conversations", json_data=json_data)

        return Conversation(
            id=data.get("id", ""),
            name=data.get("name", name),
            participants=data.get("participants", participant_ids),
            created_at=data.get("created_at", datetime.utcnow().isoformat()),
            updated_at=data.get("updated_at", datetime.utcnow().isoformat())
        )

    async def get_conversation(self, conversation_id: str) -> Conversation:
        """
        Get a conversation by ID.

        Args:
            conversation_id: Conversation ID

        Returns:
            Conversation object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request("GET", f"/conversations/{conversation_id}")

        return Conversation(
            id=data.get("id", conversation_id),
            name=data.get("name", ""),
            participants=data.get("participants", []),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def list_conversations(
        self,
        limit: int = 50,
        offset: int = 0,
        participant_id: Optional[str] = None
    ) -> List[Conversation]:
        """
        List conversations.

        Args:
            limit: Maximum number of conversations to return
            offset: Pagination offset
            participant_id: Optional filter by participant ID

        Returns:
            List of Conversation objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"limit": limit, "offset": offset}

        if participant_id:
            params["participant_id"] = participant_id

        data = await self._request("GET", "/conversations", params=params)

        conversations = data.get("conversations", [])
        return [
            Conversation(
                id=c.get("id", ""),
                name=c.get("name", ""),
                participants=c.get("participants", []),
                created_at=c.get("created_at", ""),
                updated_at=c.get("updated_at", "")
            )
            for c in conversations
        ]

    async def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation.

        Args:
            conversation_id: Conversation ID

        Returns:
            True if deleted successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        await self._request("DELETE", f"/conversations/{conversation_id}")
        return True

    async def search_conversation_messages(
        self,
        conversation_id: str,
        query: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Message]:
        """
        Search for messages in a conversation.

        Args:
            conversation_id: Conversation ID
            query: Search query string
            limit: Maximum number of messages to return
            offset: Pagination offset

        Returns:
            List of Message objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {
            "q": query,
            "limit": limit,
            "offset": offset
        }

        data = await self._request(
            "GET",
            f"/conversations/{conversation_id}/messages/search",
            params=params
        )

        messages = data.get("messages", [])
        return [
            Message(
                id=m.get("id", ""),
                conversation_id=m.get("conversation_id", conversation_id),
                sender_id=m.get("sender_id", ""),
                content=m.get("content", ""),
                message_type=m.get("type", "text"),
                created_at=m.get("created_at", "")
            )
            for m in messages
        ]

    # ==================== Participants ====================

    async def add_participant_to_conversation(
        self,
        conversation_id: str,
        user_id: str,
        role: str = "member"
    ) -> Participant:
        """
        Add a participant to a conversation.

        Args:
            conversation_id: Conversation ID
            user_id: User ID to add
            role: Participant role (e.g., "admin", "member")

        Returns:
            Participant object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {
            "user_id": user_id,
            "role": role
        }

        data = await self._request(
            "POST",
            f"/conversations/{conversation_id}/participants",
            json_data=json_data
        )

        return Participant(
            id=data.get("id", ""),
            user_id=data.get("user_id", user_id),
            conversation_id=data.get("conversation_id", conversation_id),
            role=data.get("role", role),
            joined_at=data.get("joined_at", datetime.utcnow().isoformat())
        )

    async def get_participant(
        self,
        conversation_id: str,
        participant_id: str
    ) -> Participant:
        """
        Get a participant by ID.

        Args:
            conversation_id: Conversation ID
            participant_id: Participant ID

        Returns:
            Participant object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request(
            "GET",
            f"/conversations/{conversation_id}/participants/{participant_id}"
        )

        return Participant(
            id=data.get("id", participant_id),
            user_id=data.get("user_id", ""),
            conversation_id=data.get("conversation_id", conversation_id),
            role=data.get("role", ""),
            joined_at=data.get("joined_at", "")
        )

    async def list_participants(
        self,
        conversation_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Participant]:
        """
        List participants in a conversation.

        Args:
            conversation_id: Conversation ID
            limit: Maximum number of participants to return
            offset: Pagination offset

        Returns:
            List of Participant objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"limit": limit, "offset": offset}

        data = await self._request(
            "GET",
            f"/conversations/{conversation_id}/participants",
            params=params
        )

        participants = data.get("participants", [])
        return [
            Participant(
                id=p.get("id", ""),
                user_id=p.get("user_id", ""),
                conversation_id=p.get("conversation_id", conversation_id),
                role=p.get("role", ""),
                joined_at=p.get("joined_at", "")
            )
            for p in participants
        ]

    # ==================== Contacts ====================

    async def create_contact(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """
        Create a new contact.

        Args:
            name: Contact name
            email: Optional email address
            phone: Optional phone number
            metadata: Optional metadata dictionary

        Returns:
            Contact object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {"name": name}

        if email:
            json_data["email"] = email
        if phone:
            json_data["phone"] = phone
        if metadata:
            json_data["metadata"] = metadata

        data = await self._request("POST", "/contacts", json_data=json_data)

        return Contact(
            id=data.get("id", ""),
            name=data.get("name", name),
            email=data.get("email", email),
            phone=data.get("phone", phone),
            created_at=data.get("created_at", datetime.utcnow().isoformat()),
            updated_at=data.get("updated_at", datetime.utcnow().isoformat())
        )

    async def get_contact(self, contact_id: str) -> Contact:
        """
        Get a contact by ID.

        Args:
            contact_id: Contact ID

        Returns:
            Contact object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request("GET", f"/contacts/{contact_id}")

        return Contact(
            id=data.get("id", contact_id),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def list_contacts(
        self,
        limit: int = 50,
        offset: int = 0,
        search: Optional[str] = None
    ) -> List[Contact]:
        """
        List contacts.

        Args:
            limit: Maximum number of contacts to return
            offset: Pagination offset
            search: Optional search query

        Returns:
            List of Contact objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"limit": limit, "offset": offset}

        if search:
            params["search"] = search

        data = await self._request("GET", "/contacts", params=params)

        contacts = data.get("contacts", [])
        return [
            Contact(
                id=c.get("id", ""),
                name=c.get("name", ""),
                email=c.get("email"),
                phone=c.get("phone"),
                created_at=c.get("created_at", ""),
                updated_at=c.get("updated_at", "")
            )
            for c in contacts
        ]

    async def update_contact(
        self,
        contact_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """
        Update a contact.

        Args:
            contact_id: Contact ID
            name: Optional new name
            email: Optional new email
            phone: Optional new phone
            metadata: Optional metadata to update

        Returns:
            Updated Contact object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if email:
            json_data["email"] = email
        if phone:
            json_data["phone"] = phone
        if metadata:
            json_data["metadata"] = metadata

        data = await self._request(
            "PUT",
            f"/contacts/{contact_id}",
            json_data=json_data
        )

        return Contact(
            id=data.get("id", contact_id),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", datetime.utcnow().isoformat())
        )

    async def delete_contact(self, contact_id: str) -> bool:
        """
        Delete a contact.

        Args:
            contact_id: Contact ID

        Returns:
            True if deleted successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        await self._request("DELETE", f"/contacts/{contact_id}")
        return True

    # ==================== Messages ====================

    async def create_conversation_message(
        self,
        conversation_id: str,
        content: str,
        message_type: str = "text",
        sender_id: Optional[str] = None
    ) -> Message:
        """
        Create a message in a conversation.

        Args:
            conversation_id: Conversation ID
            content: Message content
            message_type: Message type (e.g., "text", "attachment")
            sender_id: Optional sender ID (uses authenticated user if not provided)

        Returns:
            Message object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {
            "content": content,
            "type": message_type
        }

        if sender_id:
            json_data["sender_id"] = sender_id

        data = await self._request(
            "POST",
            f"/conversations/{conversation_id}/messages",
            json_data=json_data
        )

        return Message(
            id=data.get("id", ""),
            conversation_id=data.get("conversation_id", conversation_id),
            sender_id=data.get("sender_id", ""),
            content=data.get("content", content),
            message_type=data.get("type", message_type),
            created_at=data.get("created_at", datetime.utcnow().isoformat())
        )

    async def get_conversation_message(
        self,
        conversation_id: str,
        message_id: str
    ) -> Message:
        """
        Get a message by ID.

        Args:
            conversation_id: Conversation ID
            message_id: Message ID

        Returns:
            Message object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request(
            "GET",
            f"/conversations/{conversation_id}/messages/{message_id}"
        )

        return Message(
            id=data.get("id", message_id),
            conversation_id=data.get("conversation_id", conversation_id),
            sender_id=data.get("sender_id", ""),
            content=data.get("content", ""),
            message_type=data.get("type", "text"),
            created_at=data.get("created_at", "")
        )

    # ==================== Channels ====================

    async def search_channels(
        self,
        query: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Channel]:
        """
        Search for channels.

        Args:
            query: Search query string
            limit: Maximum number of channels to return
            offset: Pagination offset

        Returns:
            List of Channel objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {
            "q": query,
            "limit": limit,
            "offset": offset
        }

        data = await self._request("GET", "/channels/search", params=params)

        channels = data.get("channels", [])
        return [
            Channel(
                id=c.get("id", ""),
                name=c.get("name", ""),
                description=c.get("description"),
                created_at=c.get("created_at", ""),
                updated_at=c.get("updated_at", "")
            )
            for c in channels
        ]


# ==================== Webhook Support ====================

class BirdWebhookHandler:
    """
    Bird webhook handler for processing incoming events.

    Supported webhook events:
    - Received Email Message
    - Send Email Message
    - Created Conversation
    - Created Channel
    - Opened Email
    - Deleted Conversation
    - Updated Conversation
    - Updated Channel
    """

    @staticmethod
    def parse_webhook_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and validate webhook payload.

        Args:
            payload: Raw webhook payload

        Returns:
            Parsed event data with event_type and data

        Raises:
            ValueError: If payload is invalid
        """
        if "event_type" not in payload:
            raise ValueError("Invalid webhook payload: missing event_type")

        return {
            "event_type": payload["event_type"],
            "timestamp": payload.get("timestamp", ""),
            "data": payload.get("data", {})
        }

    @staticmethod
    def handle_email_received(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle received email message event"""
        return {
            "email_id": payload.get("email_id"),
            "from": payload.get("from"),
            "to": payload.get("to"),
            "subject": payload.get("subject"),
            "body": payload.get("body"),
            "timestamp": payload.get("timestamp")
        }

    @staticmethod
    def handle_conversation_created(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle conversation created event"""
        return {
            "conversation_id": payload.get("conversation_id"),
            "name": payload.get("name"),
            "participants": payload.get("participants", []),
            "created_by": payload.get("created_by"),
            "timestamp": payload.get("timestamp")
        }


# ==================== Example Usage ====================

async def main():
    """Example usage of Bird API client"""

    api_key = "your_bird_api_key"

    async with BirdAPIClient(api_key=api_key) as client:
        # Create a conversation
        conversation = await client.create_conversation(
            name="Sales Team",
            participant_ids=["user1", "user2"],
            description="Sales team discussion"
        )
        print(f"Created conversation: {conversation.id}")

        # List conversations
        conversations = await client.list_conversations(limit=10)
        print(f"Found {len(conversations)} conversations")

        # Create a contact
        contact = await client.create_contact(
            name="John Doe",
            email="john@example.com",
            phone="+1234567890"
        )
        print(f"Created contact: {contact.id}")

        # Send a message
        message = await client.create_conversation_message(
            conversation_id=conversation.id,
            content="Hello team!"
        )
        print(f"Sent message: {message.id}")

        # Search messages
        messages = await client.search_conversation_messages(
            conversation_id=conversation.id,
            query="Hello"
        )
        print(f"Found {len(messages)} messages matching query")


if __name__ == "__main__":
    asyncio.run(main())