"""
Close API Client

Complete client for Close CRM - inside sales team management system.
Supports lead management, contacts, opportunities, tasks, and activities.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, field
import json


class CloseAPIError(Exception):
    """Base exception for Close API errors"""

    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class CloseRateLimitError(CloseAPIError):
    """Raised when rate limit is exceeded"""


@dataclass
class Lead:
    """Lead data model"""
    lead_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Contact:
    """Contact data model"""
    contact_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    company: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Opportunity:
    """Opportunity data model"""
    opportunity_id: str
    lead_id: str
    value: float
    currency: str
    status: str
    status_display_name: str
    user_id: Optional[str] = None
    confidence: Optional[int] = None
    date_won: Optional[str] = None
    date_lost: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """Task data model"""
    task_id: str
    lead_id: str
    text: str
    status: str
    due_date: Optional[str] = None
    completed_at: Optional[str] = None
    assigned_to: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Activity:
    """Activity data model"""
    activity_id: str
    lead_id: str
    activity_type: str  # "Email", "Call", "Note"
    user_id: str
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class CloseClient:
    """
    Close CRM API Client

    Provides complete access to Close API for lead management,
    contacts, opportunities, tasks, and activity tracking.
    """

    BASE_URL = "https://api.close.com/api/v1"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        max_requests_per_minute: int = 100,
        timeout: int = 30
    ):
        """Initialize Close client."""
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None
        self.max_requests_per_minute = max_requests_per_minute
        self._request_times: List[float] = []

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _check_rate_limit(self):
        """Check and enforce rate limiting"""
        now = asyncio.get_event_loop().time()
        self._request_times = [t for t in self._request_times if now - t < 60]

        if len(self._request_times) >= self.max_requests_per_minute:
            sleep_time = 60 - (now - self._request_times[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                self._request_times = []

        self._request_times.append(now)

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an API request with error handling and rate limiting."""
        await self._check_rate_limit()

        url = f"{self.base_url}{endpoint}"
        auth = aiohttp.BasicAuth(self.api_key, "")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if not self.session:
            raise RuntimeError("Client must be used as async context manager")

        try:
            async with self.session.request(
                method,
                url,
                json=data,
                params=params,
                auth=auth,
                headers=headers
            ) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = await response.text()

                if response.status == 429:
                    raise CloseRateLimitError(
                        "Rate limit exceeded",
                        status_code=429,
                        response=response_data
                    )

                if response.status >= 400:
                    error_msg = response_data if isinstance(response_data, str) else response_data.get("error", str(response_data))
                    raise CloseAPIError(
                        error_msg,
                        status_code=response.status,
                        response=response_data if isinstance(response_data, dict) else None
                    )

                return response_data if isinstance(response_data, dict) else {}

        except aiohttp.ClientError as e:
            raise CloseAPIError(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise CloseAPIError(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            if isinstance(e, CloseAPIError):
                raise
            raise CloseAPIError(f"Unexpected error: {str(e)}")

    # ==================== Leads ====================

    async def create_lead(self, lead_data: Dict[str, Any]) -> Lead:
        """Create a new lead."""
        data = await self._request("POST", "/lead/", data=lead_data)
        return Lead(
            lead_id=data.get("id", ""),
            name=data.get("name", lead_data.get("name", "")),
            email=data.get("email") or lead_data.get("email"),
            phone=data.get("phone") or lead_data.get("phone"),
            company=data.get("company") or lead_data.get("company"),
            status=data.get("status"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "id", "name", "email", "phone", "company", "status",
                "created_at", "updated_at"
            ]}
        )

    async def update_lead(self, lead_id: str, update_data: Dict[str, Any]) -> Lead:
        """Update an existing lead."""
        data = await self._request("PUT", f"/lead/{lead_id}/", data=update_data)
        return Lead(
            lead_id=lead_id,
            name=data.get("name", update_data.get("name", "")),
            email=data.get("email") or update_data.get("email"),
            phone=data.get("phone") or update_data.get("phone"),
            company=data.get("company") or update_data.get("company"),
            status=data.get("status"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "name", "email", "phone", "company", "status",
                "created_at", "updated_at"
            ]}
        )

    async def get_lead(self, lead_id: str) -> Lead:
        """Get lead details."""
        data = await self._request("GET", f"/lead/{lead_id}/")
        return Lead(
            lead_id=data.get("id", lead_id),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            company=data.get("company"),
            status=data.get("status"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "id", "name", "email", "phone", "company", "status",
                "created_at", "updated_at"
            ]}
        )

    async def delete_lead(self, lead_id: str) -> Dict[str, Any]:
        """Delete a lead."""
        return await self._request("DELETE", f"/lead/{lead_id}/")

    async def search_leads(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Lead]:
        """Search for leads."""
        params = {"limit": limit, "offset": offset}
        if query:
            params["query"] = query
        if status:
            params["status"] = status

        data = await self._request("GET", "/lead/", params=params)
        results = data.get("data", [])

        return [
            Lead(
                lead_id=r.get("id", ""),
                name=r.get("name", ""),
                email=r.get("email"),
                phone=r.get("phone"),
                company=r.get("company"),
                status=r.get("status"),
                created_at=r.get("created_at"),
                updated_at=r.get("updated_at"),
                additional_data={k: v for k, v in r.items() if k not in [
                    "id", "name", "email", "phone", "company", "status",
                    "created_at", "updated_at"
                ]}
            )
            for r in results
        ]

    # ==================== Contacts ====================

    async def create_contact(self, contact_data: Dict[str, Any]) -> Contact:
        """Create a new contact."""
        data = await self._request("POST", "/contact/", data=contact_data)
        return Contact(
            contact_id=data.get("id", ""),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            title=data.get("title"),
            url=data.get("url"),
            company=data.get("company"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "id", "name", "email", "phone", "title", "url",
                "company", "created_at", "updated_at"
            ]}
        )

    async def update_contact(self, contact_id: str, update_data: Dict[str, Any]) -> Contact:
        """Update an existing contact."""
        data = await self._request("PUT", f"/contact/{contact_id}/", data=update_data)
        return Contact(
            contact_id=contact_id,
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            title=data.get("title"),
            url=data.get("url"),
            company=data.get("company"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "name", "email", "phone", "title", "url",
                "company", "created_at", "updated_at"
            ]}
        )

    async def get_contact(self, contact_id: str) -> Contact:
        """Get contact details."""
        data = await self._request("GET", f"/contact/{contact_id}/")
        return Contact(
            contact_id=data.get("id", contact_id),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            title=data.get("title"),
            url=data.get("url"),
            company=data.get("company"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "id", "name", "email", "phone", "title", "url",
                "company", "created_at", "updated_at"
            ]}
        )

    async def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """Delete a contact."""
        return await self._request("DELETE", f"/contact/{contact_id}/")

    async def search_contacts(
        self,
        query: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Contact]:
        """Search for contacts."""
        params = {"limit": limit, "offset": offset}
        if query:
            params["query"] = query

        data = await self._request("GET", "/contact/", params=params)
        results = data.get("data", [])

        return [
            Contact(
                contact_id=r.get("id", ""),
                name=r.get("name", ""),
                email=r.get("email"),
                phone=r.get("phone"),
                title=r.get("title"),
                url=r.get("url"),
                company=r.get("company"),
                created_at=r.get("created_at"),
                updated_at=r.get("updated_at"),
                additional_data={k: v for k, v in r.items() if k not in [
                    "id", "name", "email", "phone", "title", "url",
                    "company", "created_at", "updated_at"
                ]}
            )
            for r in results
        ]

    # ==================== Opportunities ====================

    async def create_opportunity(self, opp_data: Dict[str, Any]) -> Opportunity:
        """Create a new opportunity."""
        data = await self._request("POST", "/opportunity/", data=opp_data)
        return Opportunity(
            opportunity_id=data.get("id", ""),
            lead_id=data.get("lead_id", ""),
            value=data.get("value", 0.0),
            currency=data.get("currency", ""),
            status=data.get("status", ""),
            status_display_name=data.get("status_label", ""),
            user_id=data.get("user_id"),
            confidence=data.get("confidence"),
            date_won=data.get("date_won"),
            date_lost=data.get("date_lost"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "id", "lead_id", "value", "currency", "status",
                "status_label", "user_id", "confidence",
                "date_won", "date_lost", "created_at", "updated_at"
            ]}
        )

    async def update_opportunity(self, opportunity_id: str, update_data: Dict[str, Any]) -> Opportunity:
        """Update an existing opportunity."""
        data = await self._request("PUT", f"/opportunity/{opportunity_id}/", data=update_data)
        return Opportunity(
            opportunity_id=opportunity_id,
            lead_id=data.get("lead_id", ""),
            value=data.get("value", 0.0),
            currency=data.get("currency", ""),
            status=data.get("status", ""),
            status_display_name=data.get("status_label", ""),
            user_id=data.get("user_id"),
            confidence=data.get("confidence"),
            date_won=data.get("date_won"),
            date_lost=data.get("date_lost"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "lead_id", "value", "currency", "status",
                "status_label", "user_id", "confidence",
                "date_won", "date_lost", "created_at", "updated_at"
            ]}
        )

    async def get_opportunity(self, opportunity_id: str) -> Opportunity:
        """Get opportunity details."""
        data = await self._request("GET", f"/opportunity/{opportunity_id}/")
        return Opportunity(
            opportunity_id=data.get("id", opportunity_id),
            lead_id=data.get("lead_id", ""),
            value=data.get("value", 0.0),
            currency=data.get("currency", ""),
            status=data.get("status", ""),
            status_display_name=data.get("status_label", ""),
            user_id=data.get("user_id"),
            confidence=data.get("confidence"),
            date_won=data.get("date_won"),
            date_lost=data.get("date_lost"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "id", "lead_id", "value", "currency", "status",
                "status_label", "user_id", "confidence",
                "date_won", "date_lost", "created_at", "updated_at"
            ]}
        )

    # ==================== Tasks ====================

    async def create_task(self, task_data: Dict[str, Any]) -> Task:
        """Create a new task."""
        data = await self._request("POST", "/task/", data=task_data)
        return Task(
            task_id=data.get("id", ""),
            lead_id=data.get("lead_id", ""),
            text=data.get("text", ""),
            status=data.get("status", ""),
            due_date=data.get("due_date"),
            completed_at=data.get("completed_at"),
            assigned_to=data.get("assigned_to"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "id", "lead_id", "text", "status", "due_date",
                "completed_at", "assigned_to", "created_at", "updated_at"
            ]}
        )

    async def update_task(self, task_id: str, update_data: Dict[str, Any]) -> Task:
        """Update an existing task."""
        data = await self._request("PUT", f"/task/{task_id}/", data=update_data)
        return Task(
            task_id=task_id,
            lead_id=data.get("lead_id", ""),
            text=data.get("text", ""),
            status=data.get("status", ""),
            due_date=data.get("due_date"),
            completed_at=data.get("completed_at"),
            assigned_to=data.get("assigned_to"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "lead_id", "text", "status", "due_date",
                "completed_at", "assigned_to", "created_at", "updated_at"
            ]}
        )

    async def get_task(self, task_id: str) -> Task:
        """Get task details."""
        data = await self._request("GET", f"/task/{task_id}/")
        return Task(
            task_id=data.get("id", task_id),
            lead_id=data.get("lead_id", ""),
            text=data.get("text", ""),
            status=data.get("status", ""),
            due_date=data.get("due_date"),
            completed_at=data.get("completed_at"),
            assigned_to=data.get("assigned_to"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "id", "lead_id", "text", "status", "due_date",
                "completed_at", "assigned_to", "created_at", "updated_at"
            ]}
        )

    async def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete a task."""
        return await self._request("DELETE", f"/task/{task_id}/")

    # ==================== Activities ====================

    async def create_email_activity(self, activity_data: Dict[str, Any]) -> Activity:
        """Create an email activity."""
        data = await self._request("POST", "/activity/email/", data=activity_data)
        return Activity(
            activity_id=data.get("id", ""),
            lead_id=data.get("lead_id", ""),
            activity_type="Email",
            user_id=data.get("user_id", ""),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "id", "lead_id", "user_id", "created_at"
            ]}
        )

    async def create_call_activity(self, activity_data: Dict[str, Any]) -> Activity:
        """Create a call activity."""
        data = await self._request("POST", "/activity/call/", data=activity_data)
        return Activity(
            activity_id=data.get("id", ""),
            lead_id=data.get("lead_id", ""),
            activity_type="Call",
            user_id=data.get("user_id", ""),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "id", "lead_id", "user_id", "created_at"
            ]}
        )

    async def close(self):
        """Close the client session."""
        if self.session and not self.session.closed:
            await self.session.close()


# ==================== Example Usage ====================

async def main():
    """Example usage of Close client."""

    async with CloseClient(api_key="your_api_key") as client:
        # Create a lead
        lead = await client.create_lead({
            "name": "John Smith",
            "email": "john@example.com",
            "phone": "555-1234",
            "company": "Acme Corp",
            "status": "Potential"
        })
        print(f"Created lead: {lead.lead_id}")

        # Create a task
        task = await client.create_task({
            "lead_id": lead.lead_id,
            "text": "Follow up call",
            "due_date": "2024-01-20",
            "status": "open"
        })
        print(f"Created task: {task.task_id}")

        # Create an opportunity
        opportunity = await client.create_opportunity({
            "lead_id": lead.lead_id,
            "value": 50000.0,
            "currency": "USD",
            "status": "Potential"
        })
        print(f"Created opportunity: {opportunity.opportunity_id}")


if __name__ == "__main__":
    asyncio.run(main())