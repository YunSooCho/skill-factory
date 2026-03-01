"""
Contactship AI API Client

Contactship AI is an AI-powered contact management platform with phone call capabilities.

Supports:
- List Agents
- AI Phone Call
- Create Contact
- Get Contact
- Update Contact
- Delete Contact
- Search Contact
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Agent:
    """AI Agent object"""
    id: str
    name: str
    description: Optional[str]
    language: Optional[str]
    voice: Optional[str]
    status: str
    created_at: str
    updated_at: str


@dataclass
class Contact:
    """Contact object"""
    id: str
    name: str
    phone: str
    email: Optional[str]
    company: Optional[str]
    notes: Optional[str]
    custom_fields: Optional[Dict[str, Any]]
    created_at: str
    updated_at: str


@dataclass
class PhoneCall:
    """Phone Call object"""
    id: str
    agent_id: str
    contact_id: str
    status: str
    duration: int  # seconds
    transcript: Optional[str]
    summary: Optional[str]
    recording_url: Optional[str]
    started_at: str
    ended_at: Optional[str]


@dataclass
class CallResult:
    """Phone Call Result object"""
    call_id: str
    status: str
    message: str
    call_url: Optional[str]


class ContactshipAIClient:
    """
    Contactship AI API client for AI-powered contact management.

    Authentication: API Key
    Base URL: https://api.contactship.ai/v1
    """

    BASE_URL = "https://api.contactship.ai/v1"

    def __init__(self, api_key: str):
        """
        Initialize Contactship AI client.

        Args:
            api_key: Contactship AI API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
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
        Make HTTP request to Contactship AI API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data

        Raises:
            Exception: If API returns error
        """
        url = f"{self.BASE_URL}{endpoint}"

        async with self.session.request(
            method,
            url,
            params=params,
            json=json_data
        ) as response:
            if response.status == 204:
                return {}

            data = await response.json()

            if response.status not in [200, 201, 202]:
                error_msg = data.get("message", "Unknown error") if isinstance(data, dict) else str(data)
                raise Exception(f"Contactship AI API error ({response.status}): {error_msg}")

            return data

    # ==================== Agents ====================

    async def list_agents(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Agent]:
        """
        List available AI agents.

        List Agents

        Args:
            status: Filter by status (active, inactive)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of Agent objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit, "offset": offset}

        if status:
            params["status"] = status

        data = await self._request("GET", "/agents", params=params)

        agents = data.get("agents", [])
        return [
            Agent(
                id=agent.get("id", ""),
                name=agent.get("name", ""),
                description=agent.get("description"),
                language=agent.get("language"),
                voice=agent.get("voice"),
                status=agent.get("status", "active"),
                created_at=agent.get("created_at", ""),
                updated_at=agent.get("updated_at", "")
            )
            for agent in agents
        ]

    async def get_agent(self, agent_id: str) -> Agent:
        """
        Get an agent by ID.

        Args:
            agent_id: Agent ID

        Returns:
            Agent object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/agents/{agent_id}")

        agent = data.get("agent", {})
        return Agent(
            id=agent.get("id", agent_id),
            name=agent.get("name", ""),
            description=agent.get("description"),
            language=agent.get("language"),
            voice=agent.get("voice"),
            status=agent.get("status", "active"),
            created_at=agent.get("created_at", ""),
            updated_at=agent.get("updated_at", "")
        )

    # ==================== AI Phone Calls ====================

    async def ai_phone_call(
        self,
        agent_id: str,
        contact_id: str,
        phone_number: str,
        script: Optional[str] = None,
        call_purpose: Optional[str] = None,
        max_duration: int = 300,
        scheduled_for: Optional[str] = None
    ) -> CallResult:
        """
        Initiate an AI phone call to a contact.

        AI Phone Call

        Args:
            agent_id: AI agent ID to use for call
            contact_id: Contact ID
            phone_number: Phone number to call
            script: Optional call script/template
            call_purpose: Purpose of the call
            max_duration: Maximum call duration in seconds (default: 300)
            scheduled_for: Optional schedule time (ISO 8601 format)

        Returns:
            CallResult object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "agent_id": agent_id,
            "contact_id": contact_id,
            "phone_number": phone_number,
            "max_duration": max_duration
        }

        if script:
            json_data["script"] = script
        if call_purpose:
            json_data["call_purpose"] = call_purpose
        if scheduled_for:
            json_data["scheduled_for"] = scheduled_for

        data = await self._request("POST", "/calls", json_data=json_data)

        return CallResult(
            call_id=data.get("call_id", ""),
            status=data.get("status", "pending"),
            message=data.get("message", ""),
            call_url=data.get("call_url")
        )

    async def get_phone_call(self, call_id: str) -> PhoneCall:
        """
        Get a phone call by ID.

        Args:
            call_id: Call ID

        Returns:
            PhoneCall object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/calls/{call_id}")

        return self._parse_phone_call(data.get("call", {}))

    async def list_phone_calls(
        self,
        contact_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[PhoneCall]:
        """
        List phone calls.

        Args:
            contact_id: Filter by contact ID
            agent_id: Filter by agent ID
            status: Filter by status
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of PhoneCall objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit, "offset": offset}

        if contact_id:
            params["contact_id"] = contact_id
        if agent_id:
            params["agent_id"] = agent_id
        if status:
            params["status"] = status

        data = await self._request("GET", "/calls", params=params)

        calls = data.get("calls", [])
        return [self._parse_phone_call(call) for call in calls]

    async def cancel_phone_call(self, call_id: str) -> bool:
        """
        Cancel a pending or in-progress phone call.

        Args:
            call_id: Call ID

        Returns:
            True if cancelled successfully

        Raises:
            Exception: If API returns error
        """
        await self._request("POST", f"/calls/{call_id}/cancel")
        return True

    def _parse_phone_call(self, data: Dict[str, Any]) -> PhoneCall:
        """Parse phone call data"""
        return PhoneCall(
            id=data.get("id", ""),
            agent_id=data.get("agent_id", ""),
            contact_id=data.get("contact_id", ""),
            status=data.get("status", ""),
            duration=int(data.get("duration", 0)),
            transcript=data.get("transcript"),
            summary=data.get("summary"),
            recording_url=data.get("recording_url"),
            started_at=data.get("started_at", ""),
            ended_at=data.get("ended_at") or data.get("completed_at")
        )

    # ==================== Contacts ====================

    async def create_contact(
        self,
        name: str,
        phone: str,
        email: Optional[str] = None,
        company: Optional[str] = None,
        notes: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """
        Create a new contact.

        Create Contact

        Args:
            name: Contact name
            phone: Phone number
            email: Email address
            company: Company name
            notes: Additional notes
            custom_fields: Custom field values

        Returns:
            Contact object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "name": name,
            "phone": phone
        }

        if email:
            json_data["email"] = email
        if company:
            json_data["company"] = company
        if notes:
            json_data["notes"] = notes
        if custom_fields:
            json_data["custom_fields"] = custom_fields

        data = await self._request("POST", "/contacts", json_data=json_data)

        return self._parse_contact(data.get("contact", {}))

    async def get_contact(self, contact_id: str) -> Contact:
        """
        Get a contact by ID.

        Get Contact

        Args:
            contact_id: Contact ID

        Returns:
            Contact object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/contacts/{contact_id}")

        return self._parse_contact(data.get("contact", {}))

    async def search_contacts(
        self,
        query: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Contact]:
        """
        Search for contacts.

        Search Contact

        Args:
            query: General search query
            phone: Filter by phone number
            email: Filter by email
            company: Filter by company
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of Contact objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit, "offset": offset}

        if query:
            params["q"] = query
        if phone:
            params["phone"] = phone
        if email:
            params["email"] = email
        if company:
            params["company"] = company

        data = await self._request("GET", "/contacts", params=params)

        contacts = data.get("contacts", [])
        return [self._parse_contact(c) for c in contacts]

    async def update_contact(
        self,
        contact_id: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        notes: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """
        Update a contact.

        Update Contact

        Args:
            contact_id: Contact ID
            name: New name
            phone: New phone number
            email: New email address
            company: New company
            notes: New notes
            custom_fields: Custom fields to update

        Returns:
            Updated Contact object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if phone:
            json_data["phone"] = phone
        if email:
            json_data["email"] = email
        if company:
            json_data["company"] = company
        if notes:
            json_data["notes"] = notes
        if custom_fields:
            json_data["custom_fields"] = custom_fields

        data = await self._request("PUT", f"/contacts/{contact_id}", json_data=json_data)

        return self._parse_contact(data.get("contact", {}))

    async def delete_contact(self, contact_id: str) -> bool:
        """
        Delete a contact.

        Delete Contact

        Args:
            contact_id: Contact ID

        Returns:
            True if deleted successfully

        Raises:
            Exception: If API returns error
        """
        await self._request("DELETE", f"/contacts/{contact_id}")
        return True

    def _parse_contact(self, data: Dict[str, Any]) -> Contact:
        """Parse contact data"""
        return Contact(
            id=data.get("id", ""),
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            email=data.get("email"),
            company=data.get("company"),
            notes=data.get("notes"),
            custom_fields=data.get("custom_fields"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Call Transcripts and Analysis ====================

    async def get_call_transcript(self, call_id: str) -> Dict[str, Any]:
        """
        Get the transcript of a completed call.

        Args:
            call_id: Call ID

        Returns:
            Transcript data

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/calls/{call_id}/transcript")
        return data.get("transcript", {})

    async def get_call_summary(self, call_id: str) -> Dict[str, Any]:
        """
        Get the AI-generated summary of a completed call.

        Args:
            call_id: Call ID

        Returns:
            Summary data with key points, next steps, etc.

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/calls/{call_id}/summary")
        return data.get("summary", {})

    async def get_call_sentiment(self, call_id: str) -> Dict[str, Any]:
        """
        Get sentiment analysis of a call.

        Args:
            call_id: Call ID

        Returns:
            Sentiment analysis data

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/calls/{call_id}/sentiment")
        return data.get("sentiment", {})


# ==================== Webhook Support ====================

class ContactshipAIWebhookHandler:
    """
    Contactship AI webhook handler for processing call events.

    Process incoming webhook events about call completion, status changes, etc.
    """

    @staticmethod
    def parse_webhook_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and validate webhook payload.

        Args:
            payload: Raw webhook payload

        Returns:
            Parsed event data with event_type and data
        """
        event_type = payload.get("event", payload.get("event_type", ""))

        return {
            "event_type": event_type,
            "timestamp": payload.get("timestamp", datetime.utcnow().isoformat()),
            "data": payload.get("data", {})
        }

    @staticmethod
    def handle_call_completed(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle call completed event"""
        return {
            "call_id": payload.get("call_id"),
            "agent_id": payload.get("agent_id"),
            "contact_id": payload.get("contact_id"),
            "duration": payload.get("duration"),
            "status": payload.get("status"),
            "summary": payload.get("summary"),
            "timestamp": payload.get("timestamp")
        }

    @staticmethod
    def handle_call_started(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle call started event"""
        return {
            "call_id": payload.get("call_id"),
            "agent_id": payload.get("agent_id"),
            "contact_id": payload.get("contact_id"),
            "phone_number": payload.get("phone_number"),
            "started_at": payload.get("started_at"),
            "timestamp": payload.get("timestamp")
        }


# ==================== Example Usage ====================

async def main():
    """Example usage of Contactship AI API client"""

    api_key = "your_contactship_ai_api_key"

    async with ContactshipAIClient(api_key) as client:
        # List available agents
        agents = await client.list_agents()
        print(f"Found {len(agents)} agents")

        if agents:
            agent = agents[0]
            print(f"Using agent: {agent.name}")

            # Create a contact
            contact = await client.create_contact(
                name="John Doe",
                phone="+1234567890",
                email="john@example.com",
                company="Example Corp",
                notes="Important prospect"
            )
            print(f"Created contact: {contact.id}")

            # Initiate an AI phone call
            call_result = await client.ai_phone_call(
                agent_id=agent.id,
                contact_id=contact.id,
                phone_number=contact.phone,
                call_purpose="Follow up on proposal",
                script="Hello, this is calling from your account to follow up on our proposal"
            )
            print(f"Initiated call: {call_result.call_id}, status: {call_result.status}")

            # Update contact
            updated = await client.update_contact(
                contact.id,
                notes="Contacted on 2024-02-28"
            )
            print(f"Updated contact: {updated.notes}")

            # Search contacts
            contacts = await client.search_contacts(query="John", limit=10)
            print(f"Found {len(contacts)} contacts")

            # Get call details
            if call_result.call_id:
                call = await client.get_phone_call(call_result.call_id)
                print(f"Call duration: {call.duration}s, status: {call.status}")


if __name__ == "__main__":
    asyncio.run(main())