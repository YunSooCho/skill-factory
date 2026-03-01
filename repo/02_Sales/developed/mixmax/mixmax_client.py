"""
Mixmax API - Email Sequences and Messaging Client

Supports email sequences, message sending, and draft management.

API Actions (8):
1. Cancel Active Sequence Recipients
2. Add Recipients to Sequence
3. Send Message
4. Get Message
5. Create Email Draft
6. Get Recipient Sequence
7. List Messages
8. Search Sequence
"""

import aiohttp
import asyncio
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Message:
    """Message data model"""
    id: Optional[str] = None
    to: List[str] = field(default_factory=list)
    cc: List[str] = field(default_factory=list)
    bcc: List[str] = field(default_factory=list)
    subject: str = ""
    body: str = ""
    html_body: str = ""
    sender: str = ""
    status: str = ""
    created_at: Optional[str] = None
    sent_at: Optional[str] = None
    message_id: Optional[str] = None
    thread_id: Optional[str] = None


@dataclass
class EmailDraft:
    """Email draft data model"""
    id: Optional[str] = None
    to: List[str] = field(default_factory=list)
    cc: List[str] = field(default_factory=list)
    bcc: List[str] = field(default_factory=list)
    subject: str = ""
    body: str = ""
    html_body: str = ""
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Sequence:
    """Email sequence data model"""
    id: Optional[str] = None
    name: str = ""
    description: str = ""
    status: str = "active"
    recipients: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class SequenceRecipient:
    """Sequence recipient data model"""
    recipient_id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: str = "active"
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class MixmaxClient:
    """
    Mixmax API client for email sequences and messaging.

    API Documentation: https://api.mixmax.com/
    Authentication: API Key via header
    Protocol: HTTPS REST API
    """

    BASE_URL = "https://api.mixmax.com/v1"
    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 0.5  # seconds between requests

    def __init__(self, api_key: str):
        """Initialize Mixmax client"""
        self.api_key = api_key
        self.session = None
        self._last_request_time = 0

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _rate_limit(self):
        """Simple rate limiting"""
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self.RATE_LIMIT_DELAY:
            await asyncio.sleep(self.RATE_LIMIT_DELAY - time_since_last_request)
        self._last_request_time = time.time()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make API request with retry logic and error handling"""
        await self._rate_limit()

        headers = {
            "X-API-Token": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        url = f"{self.BASE_URL}{endpoint}"

        for attempt in range(self.MAX_RETRIES):
            try:
                async with self.session.request(
                    method,
                    url,
                    params=params,
                    json=json_data,
                    headers=headers
                ) as response:
                    data = await response.json()

                    if response.status in (200, 201, 204):
                        return data if data else {}
                    elif response.status == 401:
                        raise Exception("Invalid API key or unauthorized access")
                    elif response.status == 403:
                        raise Exception("Insufficient permissions")
                    elif response.status == 404:
                        raise Exception("Resource not found")
                    elif response.status == 429:
                        retry_after = int(response.headers.get("Retry-After", 5))
                        await asyncio.sleep(retry_after)
                        continue
                    elif response.status == 400:
                        raise Exception(f"Client error: {data.get('message', 'Unknown error')}")
                    else:
                        raise Exception(f"Server error: {response.status} - {data}")

            except aiohttp.ClientError as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise Exception(f"Request failed after {self.MAX_RETRIES} attempts: {str(e)}")
                await asyncio.sleep(2 ** attempt)

    # ==================== Message Operations ====================

    async def send_message(self, message: Message) -> Message:
        """Send a message (Send Message)"""
        message_data = {
            "to": message.to,
            "cc": message.cc,
            "bcc": message.bcc,
            "subject": message.subject,
            "body": message.body,
            "htmlBody": message.html_body
        }

        response = await self._request("POST", "/messages/send", json_data=message_data)
        return Message(**self._map_message_data(response))

    async def get_message(self, message_id: str) -> Message:
        """Get message by ID (Get Message)"""
        response = await self._request("GET", f"/messages/{message_id}")
        return Message(**self._map_message_data(response))

    async def list_messages(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[Message]:
        """List messages (List Messages)"""
        params = {"limit": limit, "skip": offset}

        response = await self._request("GET", "/messages", params=params)
        messages = response.get("results", [])
        return [Message(**self._map_message_data(m)) for m in messages]

    def _map_message_data(self, data: Dict) -> Dict:
        """Map Mixmax message data to our Message model"""
        return {
            "id": data.get("_id"),
            "to": data.get("to", []),
            "cc": data.get("cc", []),
            "bcc": data.get("bcc", []),
            "subject": data.get("subject", ""),
            "body": data.get("body", ""),
            "html_body": data.get("htmlBody", ""),
            "sender": data.get("from", ""),
            "status": data.get("status", ""),
            "created_at": data.get("createdDate"),
            "sent_at": data.get("sentDate"),
            "message_id": data.get("messageId"),
            "thread_id": data.get("threadId")
        }

    # ==================== Draft Operations ====================

    async def create_email_draft(self, draft: EmailDraft) -> EmailDraft:
        """Create an email draft (Create Email Draft)"""
        draft_data = {
            "to": draft.to,
            "cc": draft.cc,
            "bcc": draft.bcc,
            "subject": draft.subject,
            "body": draft.body,
            "htmlBody": draft.html_body,
            "attachments": draft.attachments
        }

        # Remove None values and empty lists
        draft_data = {k: v for k, v in draft_data.items() if v}

        response = await self._request("POST", "/drafts", json_data=draft_data)
        return EmailDraft(**self._map_draft_data(response))

    def _map_draft_data(self, data: Dict) -> Dict:
        """Map Mixmax draft data to our EmailDraft model"""
        return {
            "id": data.get("_id"),
            "to": data.get("to", []),
            "cc": data.get("cc", []),
            "bcc": data.get("bcc", []),
            "subject": data.get("subject", ""),
            "body": data.get("body", ""),
            "html_body": data.get("htmlBody", ""),
            "attachments": data.get("attachments", []),
            "created_at": data.get("createdDate"),
            "updated_at": data.get("updatedDate")
        }

    # ==================== Sequence Operations ====================

    async def add_recipients_to_sequence(
        self,
        sequence_id: str,
        recipients: List[SequenceRecipient]
    ) -> List[SequenceRecipient]:
        """Add recipients to sequence (Add Recipients to Sequence)"""
        recipients_data = []

        for recipient in recipients:
            recipient_data = {
                "recipientId": recipient.recipient_id,
                "email": recipient.email,
                "firstName": recipient.first_name,
                "lastName": recipient.last_name
            }
            recipients_data.append(recipient_data)

        response = await self._request(
            "POST",
            f"/sequences/{sequence_id}/recipients",
            json_data={"recipients": recipients_data}
        )

        return [
            SequenceRecipient(
                recipient_id=r.get("recipientId"),
                email=r.get("email"),
                first_name=r.get("firstName"),
                last_name=r.get("lastName"),
                status=r.get("status", "active")
            )
            for r in response.get("recipients", [])
        ]

    async def cancel_active_sequence_recipients(
        self,
        sequence_id: str,
        recipient_ids: List[str]
    ) -> bool:
        """Cancel active sequence recipients (Cancel Active Sequence Recipients)"""
        for recipient_id in recipient_ids:
            await self._request(
                "DELETE",
                f"/sequences/{sequence_id}/recipients/{recipient_id}"
            )
        return True

    async def get_recipient_sequence(
        self,
        sequence_id: str,
        recipient_id: str
    ) -> Dict[str, Any]:
        """Get recipient sequence (Get Recipient Sequence)"""
        response = await self._request(
            "GET",
            f"/sequences/{sequence_id}/recipients/{recipient_id}"
        )
        return response

    async def search_sequences(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Sequence]:
        """Search sequences (Search Sequence)"""
        params = {"limit": limit}

        if query:
            params["q"] = query
        if status:
            params["status"] = status

        response = await self._request("GET", "/sequences", params=params)
        sequences = response.get("results", [])
        return [
            Sequence(
                id=s.get("_id"),
                name=s.get("name", ""),
                description=s.get("description", ""),
                status=s.get("status", "active"),
                recipients=s.get("recipientCount", 0),
                created_at=s.get("createdDate"),
                updated_at=s.get("updatedDate")
            )
            for s in sequences
        ]


# ==================== Example Usage ====================

async def main():
    """Example usage of Mixmax client"""

    api_key = "your_mixmax_api_key"

    async with MixmaxClient(api_key=api_key) as client:
        # Send a message
        message = Message(
            to=["recipient@example.com"],
            subject="Test Message",
            body="Hello, this is a test message from Mixmax."
        )
        sent_message = await client.send_message(message)
        print(f"Sent message ID: {sent_message.id}")

        # Create an email draft
        draft = EmailDraft(
            to=["draft@example.com"],
            subject="Draft Subject",
            body="Draft content here"
        )
        created_draft = await client.create_email_draft(draft)
        print(f"Draft created: {created_draft.id}")

        # Search sequences
        sequences = await client.search_sequences(status="active")
        print(f"Found {len(sequences)} active sequences")


if __name__ == "__main__":
    asyncio.run(main())