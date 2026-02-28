"""
Close CRM API Client

Close is a modern CRM platform for sales teams.

Supports:
- Create Lead
- Get Lead
- Update Lead
- Delete Lead
- Search Lead
- Create Contact
- Get Contact
- Update Contact
- Delete Contact
- Search Contacts
- Create Opportunity
- Get Opportunity
- Update Opportunity
- Delete Opportunity
- Create Task
- Get task (Get Task)
- Update Task
- Delete Task
- Create Call Activity
- Create Email Activity
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Lead:
    """Lead object"""
    id: str
    name: str
    status_id: str
    status_label: str
    description: Optional[str]
    display_name: str
    url: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Contact:
    """Contact object"""
    id: str
    name: str
    title: Optional[str]
    emails: List[str]
    phones: List[str]
    url: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Opportunity:
    """Opportunity object"""
    id: str
    lead_id: str
    lead_name: Optional[str]
    value_amount: float
    value_currency: str
    value_period: str
    confidence: int
    status_id: str
    status_label: str
    status_type: str
    created_at: str
    updated_at: str


@dataclass
class Task:
    """Task object"""
    id: str
    lead_id: Optional[str]
    lead_name: Optional[str]
    status: str
    text: str
    is_done: bool
    due_date: Optional[str]
    completed_date: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class CallActivity:
    """Call Activity object"""
    id: str
    lead_id: str
    lead_name: Optional[str]
    status: str
    direction: str
    duration: int
    note: Optional[str]
    created_at: str


@dataclass
class EmailActivity:
    """Email Activity object"""
    id: str
    lead_id: str
    lead_name: Optional[str]
    status: str
    subject: str
    body: Optional[str]
    local_timezone: Optional[str]
    created_at: str


class CloseAPIClient:
    """
    Close CRM API client for sales management.

    Authentication: API Key
    Documentation: https://developer.close.com/
    Base URL: https://api.close.com/api/v1
    """

    BASE_URL = "https://api.close.com/api/v1"

    def __init__(self, api_key: str):
        """
        Initialize Close API client.

        Args:
            api_key: Close API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            auth=aiohttp.BasicAuth(self.api_key, ""),
            headers={"Content-Type": "application/json"}
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
        Make HTTP request to Close API.

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

            if response.status not in [200, 201]:
                error_msg = data.get("message", "Unknown error") if isinstance(data, dict) else str(data)
                raise Exception(f"Close API error ({response.status}): {error_msg}")

            return data

    # ==================== Leads ====================

    async def create_lead(
        self,
        name: str,
        status_id: str,
        description: Optional[str] = None,
        url: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Lead:
        """
        Create a new lead.

        Args:
            name: Lead name
            status_id: Status ID
            description: Description
            url: Website URL
            custom_fields: Custom field values

        Returns:
            Lead object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "name": name,
            "status_id": status_id
        }

        if description:
            json_data["description"] = description
        if url:
            json_data["url"] = url
        if custom_fields:
            json_data["custom_fields"] = custom_fields

        data = await self._request("POST", "/lead/", json_data=json_data)

        return self._parse_lead(data)

    async def get_lead(self, lead_id: str) -> Lead:
        """
        Get a lead by ID.

        Args:
            lead_id: Lead ID

        Returns:
            Lead object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/lead/{lead_id}/")
        return self._parse_lead(data)

    async def search_leads(
        self,
        query: Optional[str] = None,
        status_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Lead]:
        """
        Search for leads.

        Args:
            query: Search query
            status_id: Filter by status ID
            limit: Maximum number of results

        Returns:
            List of Lead objects

        Raises:
            Exception: If API returns error
        """
        params = {"_limit": limit, "_fields": "id,name,status_id,status_label,display_name,description,url,created_at,updated_at"}

        if query:
            params["query"] = query
        if status_id:
            params["status_id"] = status_id

        if query is None and status_id is None:
            params["query"] = ""  # Get all leads

        data = await self._request("GET", "/lead/", params=params)

        return [self._parse_lead(lead_data) for lead_data in data.get("data", [])]

    async def update_lead(
        self,
        lead_id: str,
        name: Optional[str] = None,
        status_id: Optional[str] = None,
        description: Optional[str] = None,
        url: Optional[str] = None
    ) -> Lead:
        """
        Update a lead.

        Args:
            lead_id: Lead ID
            name: New name
            status_id: New status ID
            description: New description
            url: New URL

        Returns:
            Updated Lead object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if status_id:
            json_data["status_id"] = status_id
        if description:
            json_data["description"] = description
        if url:
            json_data["url"] = url

        data = await self._request("PUT", f"/lead/{lead_id}/", json_data=json_data)

        return self._parse_lead(data)

    async def delete_lead(self, lead_id: str) -> bool:
        """
        Delete a lead.

        Args:
            lead_id: Lead ID

        Returns:
            True if deleted successfully

        Raises:
            Exception: If API returns error
        """
        await self._request("DELETE", f"/lead/{lead_id}/")
        return True

    def _parse_lead(self, data: Dict[str, Any]) -> Lead:
        """Parse lead data"""
        status = data.get("status", {})
        return Lead(
            id=data.get("id", ""),
            name=data.get("name", ""),
            status_id=data.get("status_id", ""),
            status_label=status.get("label", "") if status else "",
            description=data.get("description"),
            display_name=data.get("display_name", ""),
            url=data.get("url"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Contacts ====================

    async def create_contact(
        self,
        name: str,
        title: Optional[str] = None,
        emails: Optional[List[str]] = None,
        phones: Optional[List[str]] = None,
        lead_id: Optional[str] = None
    ) -> Contact:
        """
        Create a new contact.

        Args:
            name: Contact name
            title: Job title
            emails: List of email addresses
            phones: List of phone numbers
            lead_id: Associated lead ID

        Returns:
            Contact object

        Raises:
            Exception: If API returns error
        """
        json_data = {"name": name}

        if title:
            json_data["title"] = title
        if emails:
            json_data["emails"] = [{"email": e, "type": "office"} for e in emails]
        if phones:
            json_data["phones"] = [{"phone": p, "type": "office"} for p in phones]
        if lead_id:
            json_data["lead_id"] = lead_id

        data = await self._request("POST", "/contact/", json_data=json_data)

        return self._parse_contact(data)

    async def get_contact(self, contact_id: str) -> Contact:
        """
        Get a contact by ID.

        Args:
            contact_id: Contact ID

        Returns:
            Contact object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/contact/{contact_id}/")
        return self._parse_contact(data)

    async def search_contacts(
        self,
        query: Optional[str] = None,
        limit: int = 50
    ) -> List[Contact]:
        """
        Search for contacts.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of Contact objects

        Raises:
            Exception: If API returns error
        """
        params = {"_limit": limit, "_fields": "id,name,title,emails,phones,url,created_at,updated_at"}

        if query is None:
            query = ""

        params["query"] = query

        data = await self._request("GET", "/contact/", params=params)

        return [self._parse_contact(contact_data) for contact_data in data.get("data", [])]

    async def update_contact(
        self,
        contact_id: str,
        name: Optional[str] = None,
        title: Optional[str] = None,
        emails: Optional[List[str]] = None,
        phones: Optional[List[str]] = None
    ) -> Contact:
        """
        Update a contact.

        Args:
            contact_id: Contact ID
            name: New name
            title: New title
            emails: New list of emails
            phones: New list of phones

        Returns:
            Updated Contact object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if title:
            json_data["title"] = title
        if emails:
            json_data["emails"] = [{"email": e, "type": "office"} for e in emails]
        if phones:
            json_data["phones"] = [{"phone": p, "type": "office"} for p in phones]

        data = await self._request("PUT", f"/contact/{contact_id}/", json_data=json_data)

        return self._parse_contact(data)

    async def delete_contact(self, contact_id: str) -> bool:
        """
        Delete a contact.

        Args:
            contact_id: Contact ID

        Returns:
            True if deleted successfully

        Raises:
            Exception: If API returns error
        """
        await self._request("DELETE", f"/contact/{contact_id}/")
        return True

    def _parse_contact(self, data: Dict[str, Any]) -> Contact:
        """Parse contact data"""
        emails = []
        if data.get("emails"):
            emails = [e.get("email", "") for e in data["emails"] if e.get("email")]

        phones = []
        if data.get("phones"):
            phones = [p.get("phone", "") for p in data["phones"] if p.get("phone")]

        return Contact(
            id=data.get("id", ""),
            name=data.get("name", ""),
            title=data.get("title"),
            emails=emails,
            phones=phones,
            url=data.get("url"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Opportunities ====================

    async def create_opportunity(
        self,
        lead_id: str,
        value_amount: float,
        value_period: str = "monthly",
        confidence: int = 50,
        note: Optional[str] = None
    ) -> Opportunity:
        """
        Create a new opportunity.

        Args:
            lead_id: Lead ID
            value_amount: Opportunity value amount
            value_period: Value period (one_time, monthly, quarterly, annually)
            confidence: Confidence level (0-100)
            note: Optional note

        Returns:
            Opportunity object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "lead_id": lead_id,
            "value_currency": "USD",
            "value_amount": value_amount,
            "value_period": value_period,
            "confidence": confidence
        }

        if note:
            json_data["note"] = note

        data = await self._request("POST", "/opportunity/", json_data=json_data)

        return self._parse_opportunity(data)

    async def get_opportunity(self, opportunity_id: str) -> Opportunity:
        """
        Get an opportunity by ID.

        Args:
            opportunity_id: Opportunity ID

        Returns:
            Opportunity object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/opportunity/{opportunity_id}/")
        return self._parse_opportunity(data)

    async def update_opportunity(
        self,
        opportunity_id: str,
        value_amount: Optional[float] = None,
        confidence: Optional[int] = None,
        status_id: Optional[str] = None,
        note: Optional[str] = None
    ) -> Opportunity:
        """
        Update an opportunity.

        Args:
            opportunity_id: Opportunity ID
            value_amount: New value amount
            confidence: New confidence level (0-100)
            status_id: New status ID
            note: New note

        Returns:
            Updated Opportunity object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if value_amount is not None:
            json_data["value_amount"] = value_amount
        if confidence is not None:
            json_data["confidence"] = confidence
        if status_id:
            json_data["status_id"] = status_id
        if note:
            json_data["note"] = note

        data = await self._request("PUT", f"/opportunity/{opportunity_id}/", json_data=json_data)

        return self._parse_opportunity(data)

    def _parse_opportunity(self, data: Dict[str, Any]) -> Opportunity:
        """Parse opportunity data"""
        status = data.get("status", {})
        return Opportunity(
            id=data.get("id", ""),
            lead_id=data.get("lead_id", ""),
            lead_name=data.get("lead_name"),
            value_amount=float(data.get("value_amount", 0)),
            value_currency=data.get("value_currency", "USD"),
            value_period=data.get("value_period", "monthly"),
            confidence=int(data.get("confidence", 50)),
            status_id=data.get("status_id", ""),
            status_label=status.get("label", "") if status else "",
            status_type=status.get("type", "") if status else "",
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Tasks ====================

    async def create_task(
        self,
        text: str,
        lead_id: Optional[str] = None,
        due_date: Optional[str] = None,
        assigned_to: Optional[str] = None
    ) -> Task:
        """
        Create a new task.

        Args:
            text: Task description
            lead_id: Optional lead ID
            due_date: Due date (YYYY-MM-DDTHH:MM:SS)
            assigned_to: User ID to assign task to

        Returns:
            Task object

        Raises:
            Exception: If API returns error
        """
        json_data = {"text": text}

        if lead_id:
            json_data["lead_id"] = lead_id
        if due_date:
            json_data["due_date"] = due_date
        if assigned_to:
            json_data["assigned_to"] = assigned_to

        data = await self._request("POST", "/task/", json_data=json_data)

        return self._parse_task(data)

    async def get_task(self, task_id: str) -> Task:
        """
        Get a task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/task/{task_id}/")
        return self._parse_task(data)

    async def update_task(
        self,
        task_id: str,
        text: Optional[str] = None,
        completed: Optional[bool] = None,
        due_date: Optional[str] = None
    ) -> Task:
        """
        Update a task.

        Args:
            task_id: Task ID
            text: New text
            completed: Mark as completed
            due_date: New due date

        Returns:
            Updated Task object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if text:
            json_data["text"] = text
        if completed is not None:
            json_data["completed"] = completed
        if due_date:
            json_data["due_date"] = due_date

        data = await self._request("PUT", f"/task/{task_id}/", json_data=json_data)

        return self._parse_task(data)

    async def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.

        Args:
            task_id: Task ID

        Returns:
            True if deleted successfully

        Raises:
            Exception: If API returns error
        """
        await self._request("DELETE", f"/task/{task_id}/")
        return True

    def _parse_task(self, data: Dict[str, Any]) -> Task:
        """Parse task data"""
        return Task(
            id=data.get("id", ""),
            lead_id=data.get("lead_id"),
            lead_name=data.get("lead_name"),
            status=data.get("status", ""),
            text=data.get("text", ""),
            is_done=data.get("completed", False),
            due_date=data.get("due_date"),
            completed_date=data.get("completed_at"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Call Activities ====================

    async def create_call_activity(
        self,
        lead_id: str,
        status: str,
        direction: str,
        duration: int,
        note: Optional[str] = None
    ) -> CallActivity:
        """
        Create a new call activity.

        Args:
            lead_id: Lead ID
            status: Call status (completed, scheduled, etc)
            direction: Call direction (inbound, outbound)
            duration: Duration in seconds
            note: Optional note

        Returns:
            CallActivity object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "lead_id": lead_id,
            "status": status,
            "direction": direction,
            "duration": duration
        }

        if note:
            json_data["note"] = note

        data = await self._request("POST", "/activity/call/", json_data=json_data)

        return self._parse_call_activity(data)

    def _parse_call_activity(self, data: Dict[str, Any]) -> CallActivity:
        """Parse call activity data"""
        return CallActivity(
            id=data.get("id", ""),
            lead_id=data.get("lead_id", ""),
            lead_name=data.get("lead_name"),
            status=data.get("status", ""),
            direction=data.get("direction", ""),
            duration=int(data.get("duration", 0)),
            note=data.get("note"),
            created_at=data.get("created_at", "")
        )

    # ==================== Email Activities ====================

    async def create_email_activity(
        self,
        lead_id: str,
        status: str,
        subject: str,
        body: Optional[str] = None,
        local_timezone: Optional[str] = None
    ) -> EmailActivity:
        """
        Create a new email activity.

        Args:
            lead_id: Lead ID
            status: Email status (sent, received, draft, etc)
            subject: Email subject
            body: Email body
            local_timezone: Local timezone

        Returns:
            EmailActivity object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "lead_id": lead_id,
            "status": status,
            "subject": subject
        }

        if body:
            json_data["body_text"] = body
        if local_timezone:
            json_data["local_timezone"] = local_timezone

        data = await self._request("POST", "/activity/email/", json_data=json_data)

        return self._parse_email_activity(data)

    def _parse_email_activity(self, data: Dict[str, Any]) -> EmailActivity:
        """Parse email activity data"""
        return EmailActivity(
            id=data.get("id", ""),
            lead_id=data.get("lead_id", ""),
            lead_name=data.get("lead_name"),
            status=data.get("status", ""),
            subject=data.get("subject", ""),
            body=data.get("body_text") or data.get("body"),
            local_timezone=data.get("local_timezone"),
            created_at=data.get("created_at", "")
        )


# ==================== Example Usage ====================

async def main():
    """Example usage of Close API client"""

    api_key = "your_close_api_key"

    async with CloseAPIClient(api_key) as client:
        # Create a lead
        lead = await client.create_lead(
            name="Example Lead",
            status_id="lead_in",
            description="A new lead from website",
            url="https://example.com"
        )
        print(f"Created lead: {lead.id}")

        # Create a contact
        contact = await client.create_contact(
            name="John Doe",
            title="CEO",
            emails=["john@example.com"],
            phones=["+1234567890"]
        )
        print(f"Created contact: {contact.id}")

        # Create an opportunity
        opportunity = await client.create_opportunity(
            lead_id=lead.id,
            value_amount=50000.0,
            value_period="annually",
            confidence=75
        )
        print(f"Created opportunity: {opportunity.id}")

        # Create a task
        task = await client.create_task(
            text="Follow up with lead",
            lead_id=lead.id
        )
        print(f"Created task: {task.id}")

        # Search leads
        leads = await client.search_leads(query="Example", limit=10)
        print(f"Found {len(leads)} leads")

        # Search contacts
        contacts = await client.search_contacts(query="John", limit=10)
        print(f"Found {len(contacts)} contacts")


if __name__ == "__main__":
    asyncio.run(main())