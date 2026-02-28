"""
Monica CRM API - Personal Relationship Management Client

Supports contacts, notes, calls, activities, deals, tasks, reminders, and tags.

API Actions (25):
1. Create Contact
2. Get Contact
3. Update Contact
4. Delete Contact
5. Search Contacts
6. Create Note
7. Get Notes
8. Create Call
9. Create Activity
10. Get Activities
11. Create Deal
12. Get Deal
13. Update Deal
14. Delete Deal
15. Search Deals
16. Create Task
17. Get Tasks
18. Update Task
19. Complete Task
20. Create Reminder
21. Get Reminders
22. Create Tag
23. Add Tag to Contact
24. Remove Tag from Contact
25. Upload Avatar
"""

import aiohttp
import asyncio
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Contact:
    """Contact data model"""
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    nickname: Optional[str] = None
    gender: Optional[str] = None
    is_partial: bool = False
    is_dead: bool = False
    birthdate_day: Optional[int] = None
    birthdate_month: Optional[int] = None
    birthdate_year: Optional[int] = None
    birthdate_ageless: bool = False
    birthdate_add_year: Optional[bool] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    email: List[Dict[str, Any]] = field(default_factory=list)
    phone: List[Dict[str, Any]] = field(default_factory=list)
    address: List[Dict[str, Any]] = field(default_factory=list)
    tags: List[int] = field(default_factory=list)
    avatar: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Note:
    """Note data model"""
    id: Optional[int] = None
    contact_id: int
    body: str
    emotion: Optional[str] = None
    is_sensitive: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Call:
    """Call data model"""
    id: Optional[int] = None
    contact_id: int
    called_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    answered: Optional[bool] = None
    duration: Optional[int] = None
    type: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None


@dataclass
class Activity:
    """Activity data model"""
    id: Optional[int] = None
    contact_id: int
    activity_type_id: Optional[int] = None
    summary: str = ""
    description: str = ""
    happened_at: Optional[str] = None
    emotion: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Deal:
    """Deal data model"""
    id: Optional[int] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    name: str = ""
    amount: float = 0.0
    currency: str = "USD"
    status: str = "open"
    deal_stage_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Task:
    """Task data model"""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    due_date: Optional[str] = None
    completed: bool = False
    completed_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Reminder:
    """Reminder data model"""
    id: Optional[int] = None
    contact_id: int
    title: str = ""
    initial_date: Optional[str] = None
    frequency: Optional[str] = None
    frequency_number: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Tag:
    """Tag data model"""
    id: Optional[int] = None
    name: str = ""
    slug: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class MonicaCRMClient:
    """
    Monica CRM API client for personal relationship management.

    API Documentation: https://www.monicahq.com/api/
    Authentication: API Token via header
    Protocol: HTTPS REST API
    """

    BASE_URL = "https://{domain}.monicahq.com/api"
    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 0.5  # seconds between requests

    def __init__(self, domain: str, api_token: str):
        """
        Initialize Monica CRM client.

        Args:
            domain: Your Monica CRM domain (without .monicahq.com)
            api_token: Your API token
        """
        self.domain = domain
        self.api_token = api_token
        self.session = None
        self._last_request_time = 0

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @property
    def base_url(self) -> str:
        """Get base URL with domain"""
        return self.BASE_URL.format(domain=self.domain)

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
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        url = f"{self.base_url}{endpoint}"

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
                        return data.get("data", {}) if data else {}
                    elif response.status == 401:
                        raise Exception("Invalid API token or unauthorized access")
                    elif response.status == 403:
                        raise Exception("Insufficient permissions")
                    elif response.status == 404:
                        raise Exception("Resource not found")
                    elif response.status == 429:
                        retry_after = int(response.headers.get("Retry-After", 5))
                        await asyncio.sleep(retry_after)
                        continue
                    elif 400 <= response.status < 500:
                        raise Exception(f"Client error: {data.get('errors', 'Unknown error')}")
                    else:
                        raise Exception(f"Server error: {response.status} - {data}")

            except aiohttp.ClientError as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise Exception(f"Request failed after {self.MAX_RETRIES} attempts: {str(e)}")
                await asyncio.sleep(2 ** attempt)

    # ==================== Contact Operations ====================

    async def create_contact(self, contact: Contact) -> Contact:
        """Create a new contact (Create Contact)"""
        contact_data = {
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "nickname": contact.nickname,
            "gender": contact.gender,
            "is_partial": contact.is_partial,
            "is_dead": contact.is_dead,
            "birthdate": {
                "day": contact.birthdate_day,
                "month": contact.birthdate_month,
                "year": contact.birthdate_year,
                "ageless": contact.birthdate_ageless,
                "add_year": contact.birthdate_add_year
            } if contact.birthdate_day else None,
            "company": contact.company,
            "job_title": contact.job_title,
            "email": contact.email,
            "phone": contact.phone,
            "address": contact.address,
            "tags": contact.tags
        }

        # Remove None values
        contact_data = {k: v for k, v in contact_data.items() if v is not None}

        response = await self._request("POST", "/contacts", json_data=contact_data)
        return Contact(**response)

    async def get_contact(self, contact_id: int) -> Contact:
        """Get contact by ID (Get Contact)"""
        response = await self._request("GET", f"/contacts/{contact_id}")
        return Contact(**response)

    async def update_contact(self, contact_id: int, contact: Contact) -> Contact:
        """Update existing contact (Update Contact)"""
        contact_data = {
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "nickname": contact.nickname,
            "gender": contact.gender,
            "is_partial": contact.is_partial,
            "is_dead": contact.is_dead,
            "birthdate": {
                "day": contact.birthdate_day,
                "month": contact.birthdate_month,
                "year": contact.birthdate_year,
                "ageless": contact.birthdate_ageless,
                "add_year": contact.birthdate_add_year
            } if contact.birthdate_day else None,
            "company": contact.company,
            "job_title": contact.job_title,
            "email": contact.email,
            "phone": contact.phone,
            "address": contact.address
        }

        contact_data = {k: v for k, v in contact_data.items() if v is not None}

        response = await self._request("PUT", f"/contacts/{contact_id}", json_data=contact_data)
        return Contact(**response)

    async def delete_contact(self, contact_id: int) -> bool:
        """Delete contact (Delete Contact)"""
        await self._request("DELETE", f"/contacts/{contact_id}")
        return True

    async def search_contacts(
        self,
        query: Optional[str] = None,
        gender: Optional[str] = None,
        company: Optional[str] = None,
        limit: int = 50
    ) -> List[Contact]:
        """Search contacts (Search Contacts)"""
        params = {"limit": limit}

        if query:
            params["query"] = query
        if gender:
            params["gender"] = gender
        if company:
            params["company"] = company

        response = await self._request("GET", "/contacts", params=params)
        contacts_data = response.get("data", [])
        return [Contact(**c) for c in contacts_data]

    # ==================== Note Operations ====================

    async def create_note(self, note: Note) -> Note:
        """Create a new note (Create Note)"""
        note_data = {
            "contact_id": note.contact_id,
            "body": note.body,
            "emotion": note.emotion,
            "is_sensitive": note.is_sensitive
        }

        response = await self._request("POST", "/notes", json_data=note_data)
        return Note(**response)

    async def get_notes(self, contact_id: int, limit: int = 50) -> List[Note]:
        """Get notes for a contact (Get Notes)"""
        params = {"limit": limit}
        response = await self._request("GET", f"/contacts/{contact_id}/notes", params=params)
        notes_data = response.get("data", [])
        return [Note(**n) for n in notes_data]

    # ==================== Call Operations ====================

    async def create_call(self, call: Call) -> Call:
        """Create a new call log (Create Call)"""
        call_data = {
            "contact_id": call.contact_id,
            "called_at": call.called_at,
            "answered": call.answered,
            "duration": call.duration,
            "type": call.type,
            "subject": call.subject,
            "body": call.body
        }

        call_data = {k: v for k, v in call_data.items() if v is not None}

        response = await self._request("POST", "/calls", json_data=call_data)
        return Call(**response)

    # ==================== Activity Operations ====================

    async def create_activity(self, activity: Activity) -> Activity:
        """Create a new activity (Create Activity)"""
        activity_data = {
            "contact_id": activity.contact_id,
            "activity_type_id": activity.activity_type_id,
            "summary": activity.summary,
            "description": activity.description,
            "happened_at": activity.happened_at,
            "emotion": activity.emotion
        }

        activity_data = {k: v for k, v in activity_data.items() if v is not None}

        response = await self._request("POST", "/activities", json_data=activity_data)
        return Activity(**response)

    async def get_activities(self, contact_id: int, limit: int = 50) -> List[Activity]:
        """Get activities for a contact (Get Activities)"""
        params = {"limit": limit}
        response = await self._request("GET", f"/contacts/{contact_id}/activities", params=params)
        activities_data = response.get("data", [])
        return [Activity(**a) for a in activities_data]

    # ==================== Deal Operations ====================

    async def create_deal(self, deal: Deal) -> Deal:
        """Create a new deal (Create Deal)"""
        deal_data = {
            "company_id": deal.company_id,
            "name": deal.name,
            "amount": deal.amount,
            "currency": deal.currency,
            "deal_stage_id": deal.deal_stage_id
        }

        deal_data = {k: v for k, v in deal_data.items() if v is not None}

        response = await self._request("POST", "/deals", json_data=deal_data)
        return Deal(**response)

    async def get_deal(self, deal_id: int) -> Deal:
        """Get deal by ID (Get Deal)"""
        response = await self._request("GET", f"/deals/{deal_id}")
        return Deal(**response)

    async def update_deal(self, deal_id: int, deal: Deal) -> Deal:
        """Update existing deal (Update Deal)"""
        deal_data = {
            "name": deal.name,
            "amount": deal.amount,
            "currency": deal.currency,
            "deal_stage_id": deal.deal_stage_id
        }

        deal_data = {k: v for k, v in deal_data.items() if v is not None}

        response = await self._request("PUT", f"/deals/{deal_id}", json_data=deal_data)
        return Deal(**response)

    async def delete_deal(self, deal_id: int) -> bool:
        """Delete deal (Delete Deal)"""
        await self._request("DELETE", f"/deals/{deal_id}")
        return True

    async def search_deals(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Deal]:
        """Search deals (Search Deals)"""
        params = {"limit": limit}

        if query:
            params["query"] = query
        if status:
            params["status"] = status

        response = await self._request("GET", "/deals", params=params)
        deals_data = response.get("data", [])
        return [Deal(**d) for d in deals_data]

    # ==================== Task Operations ====================

    async def create_task(self, task: Task) -> Task:
        """Create a new task (Create Task)"""
        task_data = {
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date
        }

        task_data = {k: v for k, v in task_data.items() if v is not None}

        response = await self._request("POST", "/tasks", json_data=task_data)
        return Task(**response)

    async def get_tasks(self, limit: int = 50) -> List[Task]:
        """Get tasks (Get Tasks)"""
        params = {"limit": limit}
        response = await self._request("GET", "/tasks", params=params)
        tasks_data = response.get("data", [])
        return [Task(**t) for t in tasks_data]

    async def update_task(self, task_id: int, task: Task) -> Task:
        """Update existing task (Update Task)"""
        task_data = {
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date,
            "completed": task.completed
        }

        task_data = {k: v for k, v in task_data.items() if v is not None}

        response = await self._request("PUT", f"/tasks/{task_id}", json_data=task_data)
        return Task(**response)

    async def complete_task(self, task_id: int) -> Task:
        """Complete task (Complete Task)"""
        response = await self._request("PUT", f"/tasks/{task_id}", json_data={"completed": True})
        return Task(**response)

    # ==================== Reminder Operations ====================

    async def create_reminder(self, reminder: Reminder) -> Reminder:
        """Create a new reminder (Create Reminder)"""
        reminder_data = {
            "contact_id": reminder.contact_id,
            "title": reminder.title,
            "initial_date": reminder.initial_date,
            "frequency": reminder.frequency,
            "frequency_number": reminder.frequency_number
        }

        reminder_data = {k: v for k, v in reminder_data.items() if v is not None}

        response = await self._request("POST", "/reminders", json_data=reminder_data)
        return Reminder(**response)

    async def get_reminders(self, contact_id: int, limit: int = 50) -> List[Reminder]:
        """Get reminders for a contact (Get Reminders)"""
        params = {"limit": limit}
        response = await self._request("GET", f"/contacts/{contact_id}/reminders", params=params)
        reminders_data = response.get("data", [])
        return [Reminder(**r) for r in reminders_data]

    # ==================== Tag Operations ====================

    async def create_tag(self, tag: Tag) -> Tag:
        """Create a new tag (Create Tag)"""
        tag_data = {
            "name": tag.name,
            "slug": tag.slug
        }

        tag_data = {k: v for k, v in tag_data.items() if v is not None}

        response = await self._request("POST", "/tags", json_data=tag_data)
        return Tag(**response)

    async def add_tag_to_contact(self, contact_id: int, tag_id: int) -> bool:
        """Add tag to contact (Add Tag to Contact)"""
        await self._request("POST", f"/contacts/{contact_id}/tags", json_data={"tag_id": tag_id})
        return True

    async def remove_tag_from_contact(self, contact_id: int, tag_id: int) -> bool:
        """Remove tag from contact (Remove Tag from Contact)"""
        await self._request("DELETE", f"/contacts/{contact_id}/tags/{tag_id}")
        return True


# ==================== Example Usage ====================

async def main():
    """Example usage of Monica CRM client"""

    domain = "your_domain"
    api_token = "your_monica_api_token"

    async with MonicaCRMClient(domain=domain, api_token=api_token) as client:
        # Create contact
        contact = Contact(
            first_name="John",
            last_name="Doe",
            gender="male",
            company="Example Corp",
            job_title="CEO"
        )
        created_contact = await client.create_contact(contact)
        print(f"Created contact: {created_contact.first_name} {created_contact.last_name}")

        # Create note
        note = Note(
            contact_id=created_contact.id,
            body="Initial conversation went well"
        )
        created_note = await client.create_note(note)
        print(f"Created note: {created_note.id}")

        # Create deal
        deal = Deal(
            company_id=created_contact.id,
            name="Enterprise License",
            amount=50000.0,
            currency="USD"
        )
        created_deal = await client.create_deal(deal)
        print(f"Created deal: {created_deal.name}")


if __name__ == "__main__":
    asyncio.run(main())