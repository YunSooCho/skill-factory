"""
Aircall API Client

Cloud call center software API for managing:
- Calls (search, tags, transcription, sentiment)
- Contacts (create, update, delete, search)
- Tags (create, delete, list, assign to calls)

API Actions (15):
1. Delete Tag
2. Search Calls
3. Create Contact
4. Add Tag to Call
5. Create Tag
6. Delete Contact
7. Get Call Summary
8. Get Tags List
9. Search Contacts
10. Update Contact
11. Get Call Transcription
12. Get Contact
13. Get Call
14. Get Call Sentiment
15. Get Topics from a Call

Triggers (9):
- New Agent Call
- Hungup Call
- Agent Call Declined
- Send Message
- Updated Contact
- New Contact
- Removed Contact
- Ended Call
- New Call

Authentication: API Token (Bearer)
Base URL: https://api.aircall.io/v1
Documentation: https://developer.aircall.io/
Rate Limiting: 100 requests per minute per token
"""

import aiohttp
import asyncio
import hmac
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Contact:
    """Contact model"""
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone_number: str = ""
    company: Optional[str] = None
    information: Optional[Dict[str, Any]] = None
    is_company: bool = False
    personal_email: Optional[str] = None
    is_deleted: bool = False


@dataclass
class Call:
    """Call model"""
    id: Optional[int] = None
    direction: str = ""
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    answered_at: Optional[str] = None
    duration: int = 0
    raw_duration: int = 0
    status: str = ""
    missed: bool = False
    voicemail: bool = False
    user_id: Optional[int] = None
    number_id: Optional[int] = None
    contact_id: Optional[int] = None
    tags: List[str] = None
    from_number: Optional[str] = None
    to_number: Optional[str] = None


@dataclass
class Tag:
    """Tag model"""
    id: Optional[int] = None
    name: str = ""
    color: str = ""
    description: Optional[str] = None


@dataclass
class CallSummary:
    """Call summary model"""
    call_id: int
    summary: str
    key_topics: List[str]
    action_items: List[str]
    sentiment: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class CallTranscription:
    """Call transcription model"""
    call_id: int
    content: str
    language: str
    confidence: float
    speaker_diarization: Optional[List[Dict[str, Any]]] = None


@dataclass
class CallSentiment:
    """Call sentiment model"""
    call_id: int
    overall_sentiment: str
    sentiment_score: float
    positive_percentage: float
    negative_percentage: float
    neutral_percentage: float


@dataclass
class CallTopics:
    """Call topics model"""
    call_id: int
    topics: List[Dict[str, Any]]
    dominant_topic: str
    confidence: float


class AircallClient:
    """
    Aircall API client for call center operations.

    Supports: Calls, Contacts, Tags, Webhooks
    Rate limit: 100 requests/minute per token
    """

    BASE_URL = "https://api.aircall.io/v1"
    RATE_LIMIT = 100  # requests per minute

    def __init__(self, api_token: str):
        """
        Initialize Aircall client.

        Args:
            api_token: Aircall API token (from account settings)
        """
        self.api_token = api_token
        self.session = None
        self._request_count = 0
        self._request_window_start = datetime.now()
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
        time_window = (now - self._request_window_start).total_seconds()

        if time_window >= 60:
            # Reset counter
            self._request_count = 0
            self._request_window_start = now

        if self._request_count >= self.RATE_LIMIT:
            wait_time = 60 - int(time_window)
            if wait_time > 0:
                await asyncio.sleep(wait_time)
                self._request_count = 0
                self._request_window_start = datetime.now()

        self._request_count += 1

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API request with rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response JSON

        Raises:
            Exception: If request fails
        """
        await self._check_rate_limit()

        url = f"{self.BASE_URL}{endpoint}"

        async with self.session.request(
            method,
            url,
            headers=self._headers,
            json=data,
            params=params
        ) as response:
            result = await response.json()

            if response.status not in [200, 201]:
                raise Exception(
                    f"Aircall API error: {response.status} - {result.get(
                        'message', 'Unknown error')}"
                )

            return result

    # ==================== Contact Operations ====================

    async def create_contact(
        self,
        first_name: str,
        last_name: str,
        email: str = "",
        phone_number: str = "",
        company: Optional[str] = None,
        information: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """
        Create a new contact.

        Args:
            first_name: Contact's first name
            last_name: Contact's last name
            email: Contact's email
            phone_number: Contact's phone number
            company: Contact's company name
            information: Additional custom information

        Returns:
            Created Contact object

        Raises:
            Exception: If creation fails
        """
        data = {
            "contact": {
                "first_name": first_name,
                "last_name": last_name
            }
        }

        if email:
            data["contact"]["emails"] = [{"label": "Work", "value": email}]
        if phone_number:
            data["contact"]["phone_numbers"] = [{
                "label": "Work",
                "value": phone_number
            }]
        if company:
            data["contact"]["company_name"] = company
        if information:
            data["contact"]["information"] = information

        response = await self._make_request("POST", "/contacts", data=data)
        return Contact(**response.get("contact", {}))

    async def get_contact(self, contact_id: int) -> Contact:
        """
        Get contact by ID.

        Args:
            contact_id: Contact ID

        Returns:
            Contact object

        Raises:
            Exception: If retrieval fails
        """
        response = await self._make_request("GET", f"/contacts/{contact_id}")
        return Contact(**response.get("contact", {}))

    async def update_contact(
        self,
        contact_id: int,
        **fields
    ) -> Contact:
        """
        Update contact.

        Args:
            contact_id: Contact ID
            **fields: Fields to update (first_name, last_name, email, etc.)

        Returns:
            Updated Contact object

        Raises:
            Exception: If update fails
        """
        data = {"contact": fields}
        response = await self._make_request(
            "PUT",
            f"/contacts/{contact_id}",
            data=data
        )
        return Contact(**response.get("contact", {}))

    async def delete_contact(self, contact_id: int) -> bool:
        """
        Delete contact.

        Args:
            contact_id: Contact ID

        Returns:
            True if deletion successful

        Raises:
            Exception: If deletion fails
        """
        await self._make_request("DELETE", f"/contacts/{contact_id}")
        return True

    async def search_contacts(
        self,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> List[Contact]:
        """
        Search contacts.

        Args:
            email: Email to search for
            phone_number: Phone number to search for
            page: Page number
            per_page: Items per page

        Returns:
            List of Contact objects

        Raises:
            Exception: If search fails
        """
        params = {"page": page, "per_page": per_page}

        if email:
            params["email"] = email
        if phone_number:
            params["phone_number"] = phone_number

        response = await self._make_request("GET", "/contacts", params=params)
        contacts = response.get("contacts", [])
        return [Contact(**c) for c in contacts]

    # ==================== Call Operations ====================

    async def search_calls(
        self,
        from_number: Optional[str] = None,
        to_number: Optional[str] = None,
        contact_id: Optional[int] = None,
        status: Optional[str] = None,
        limit: int = 20
    ) -> List[Call]:
        """
        Search calls.

        Args:
            from_number: Filter by caller number
            to_number: Filter by receiver number
            contact_id: Filter by contact ID
            status: Filter by status (answered, voicemail, missed)
            limit: Maximum number of results

        Returns:
            List of Call objects

        Raises:
            Exception: If search fails
        """
        params = {"per_page": limit}

        if from_number:
            params["from"] = from_number
        if to_number:
            params["to"] = to_number
        if contact_id:
            params["contact_id"] = contact_id
        if status:
            params["status"] = status

        response = await self._make_request("GET", "/calls", params=params)
        calls = response.get("calls", [])
        return [Call(**c) for c in calls]

    async def get_call(self, call_id: int) -> Call:
        """
        Get call by ID.

        Args:
            call_id: Call ID

        Returns:
            Call object

        Raises:
            Exception: If retrieval fails
        """
        response = await self._make_request("GET", f"/calls/{call_id}")
        return Call(**response.get("call", {}))

    async def get_call_summary(self, call_id: int) -> CallSummary:
        """
        Get call summary (if AI analysis is enabled).

        Args:
            call_id: Call ID

        Returns:
            CallSummary object

        Raises:
            Exception: If retrieval fails
        """
        response = await self._make_request("GET", f"/calls/{call_id}/summary")
        data = response.get("data", {})
        return CallSummary(
            call_id=call_id,
            summary=data.get("summary", ""),
            key_topics=data.get("key_topics", []),
            action_items=data.get("action_items", []),
            sentiment=data.get("sentiment"),
            created_at=data.get("created_at")
        )

    async def get_call_transcription(self, call_id: int) -> CallTranscription:
        """
        Get call transcription (if available).

        Args:
            call_id: Call ID

        Returns:
            CallTranscription object

        Raises:
            Exception: If retrieval fails
        """
        response = await self._make_request("GET", f"/calls/{call_id}/transcription")
        data = response.get("data", {})
        return CallTranscription(
            call_id=call_id,
            content=data.get("content", ""),
            language=data.get("language", ""),
            confidence=data.get("confidence", 0.0),
            speaker_diarization=data.get("speaker_diarization")
        )

    async def get_call_sentiment(self, call_id: int) -> CallSentiment:
        """
        Get call sentiment analysis.

        Args:
            call_id: Call ID

        Returns:
            CallSentiment object

        Raises:
            Exception: If retrieval fails
        """
        response = await self._make_request("GET", f"/calls/{call_id}/sentiment")
        data = response.get("data", {})
        return CallSentiment(
            call_id=call_id,
            overall_sentiment=data.get("overall_sentiment", ""),
            sentiment_score=data.get("sentiment_score", 0.0),
            positive_percentage=data.get("positive_percentage", 0.0),
            negative_percentage=data.get("negative_percentage", 0.0),
            neutral_percentage=data.get("neutral_percentage", 0.0)
        )

    async def get_call_topics(self, call_id: int) -> CallTopics:
        """
        Get topics discussed in call.

        Args:
            call_id: Call ID

        Returns:
            CallTopics object

        Raises:
            Exception: If retrieval fails
        """
        response = await self._make_request("GET", f"/calls/{call_id}/topics")
        data = response.get("data", {})
        topics = data.get("topics", [])
        return CallTopics(
            call_id=call_id,
            topics=topics,
            dominant_topic=max(topics, key=lambda x: x.get("confidence", 0)).get("topic", "") if topics else "",
            confidence=max(t.get("confidence", 0) for t in topics) if topics else 0.0
        )

    # ==================== Tag Operations ====================

    async def create_tag(
        self,
        name: str,
        color: str = "#000000",
        description: Optional[str] = None
    ) -> Tag:
        """
        Create a new tag.

        Args:
            name: Tag name
            color: Tag color (hex code)
            description: Tag description

        Returns:
            Created Tag object

        Raises:
            Exception: If creation fails
        """
        data = {
            "tag": {
                "name": name,
                "color": color
            }
        }

        if description:
            data["tag"]["description"] = description

        response = await self._make_request("POST", "/tags", data=data)
        return Tag(**response.get("tag", {}))

    async def get_tags_list(self, limit: int = 100) -> List[Tag]:
        """
        Get list of all tags.

        Args:
            limit: Maximum number of tags to return

        Returns:
            List of Tag objects

        Raises:
            Exception: If retrieval fails
        """
        params = {"per_page": limit}
        response = await self._make_request("GET", "/tags", params=params)
        tags = response.get("tags", [])
        return [Tag(**t) for t in tags]

    async def delete_tag(self, tag_id: int) -> bool:
        """
        Delete a tag.

        Args:
            tag_id: Tag ID

        Returns:
            True if deletion successful

        Raises:
            Exception: If deletion fails
        """
        await self._make_request("DELETE", f"/tags/{tag_id}")
        return True

    async def add_tag_to_call(self, call_id: int, tag_id: int) -> bool:
        """
        Add tag to a call.

        Args:
            call_id: Call ID
            tag_id: Tag ID

        Returns:
            True if tag added successfully

        Raises:
            Exception: If operation fails
        """
        data = {"tag_id": tag_id}
        await self._make_request("POST", f"/calls/{call_id}/tags", data=data)
        return True

    # ==================== Webhook Handling ====================

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle webhook events from Aircall.

        Args:
            webhook_data: Webhook payload

        Returns:
            Processed event data

        Supported triggers:
        - New Agent Call
        - Hungup Call
        - Agent Call Declined
        - Send Message
        - Updated Contact
        - New Contact
        - Removed Contact
        - Ended Call
        - New Call
        """
        event_type = webhook_data.get("event", "unknown")
        data = webhook_data.get("data", {})

        return {
            "event_type": event_type,
            "call_id": data.get("id"),
            "contact_id": data.get("contact_id"),
            "user_id": data.get("user_id"),
            "direction": data.get("direction"),
            "status": data.get("status"),
            "raw_data": webhook_data
        }


# ==================== Example Usage ====================

async def main():
    """Example usage of Aircall client"""

    # Replace with your actual API token
    api_token = "your_aircall_api_token"

    async with AircallClient(api_token) as client:
        # Create a contact
        contact = await client.create_contact(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+14155552671"
        )
        print(f"Created contact: {contact.first_name} {contact.last_name}")

        # Search contacts
        contacts = await client.search_contacts(email="john.doe@example.com")
        print(f"Found {len(contacts)} contacts")

        # Create a tag
        tag = await client.create_tag("VIP", "#FFD700", "Important customer")
        print(f"Created tag: {tag.name}")

        # Get list of tags
        tags = await client.get_tags_list()
        print(f"Total tags: {len(tags)}")

        # Search calls
        calls = await client.search_calls(limit=10)
        print(f"Found {len(calls)} recent calls")


if __name__ == "__main__":
    asyncio.run(main())