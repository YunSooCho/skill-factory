"""
Kommo CRM API - Sales and Communication Client

Supports leads, contacts, companies, tasks, and notes management.

API Actions (18):
1. Update Note
2. Add Note
3. Search Tags
4. Search Notes by Entity Type
5. Add Task
6. Search Contacts
7. Add Lead
8. Update Contact
9. Update Company
10. Search Tasks
11. Search Leads
12. Add Contact
13. Update Task
14. Update Lead
15. Add Company
16. Search Companies
17. Add Tags to Entity
18. Search Notes by Entity ID
"""

import aiohttp
import asyncio
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Lead:
    """Lead/Deal data model"""
    id: Optional[int] = None
    name: str = ""
    status_id: Optional[int] = None
    pipeline_id: Optional[int] = None
    price: float = 0.0
    responsible_user_id: Optional[int] = None
    created_by: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    closed_at: Optional[int] = None
    closest_task_at: Optional[int] = None
    is_deleted: bool = False
    custom_fields: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Contact:
    """Contact data model"""
    id: Optional[int] = None
    name: str = ""
    first_name: str = ""
    last_name: str = ""
    responsible_user_id: Optional[int] = None
    created_by: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    is_deleted: bool = False
    custom_fields: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Company:
    """Company data model"""
    id: Optional[int] = None
    name: str = ""
    responsible_user_id: Optional[int] = None
    created_by: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    is_deleted: bool = False
    custom_fields: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Task:
    """Task data model"""
    id: Optional[int] = None
    text: str = ""
    task_type_id: Optional[int] = None
    entity_type: str = ""
    entity_id: Optional[int] = None
    complete_till: Optional[int] = None
    created_by: Optional[int] = None
    responsible_user_id: Optional[int] = None
    is_completed: bool = False
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    result: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Note:
    """Note data model"""
    id: Optional[int] = None
    note_type: str = ""
    entity_type: str = ""
    entity_id: Optional[int] = None
    text: str = ""
    created_by: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    params: Dict[str, Any] = field(default_factory=dict)


class KommoClient:
    """
    Kommo CRM API client.

    API Documentation: https://www.kommo.com/developers/
    Authentication: API Key or OAuth 2.0
    Protocol: HTTPS REST API
    """

    BASE_URL = "https://{subdomain}.kommo.com/api/v4"
    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 0.5  # seconds between requests

    def __init__(self, subdomain: str, api_key: str):
        """
        Initialize Kommo client.

        Args:
            subdomain: Your Kommo account subdomain
            api_key: Your Kommo API key or access token
        """
        self.subdomain = subdomain
        self.api_key = api_key
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
        """Get base URL with subdomain"""
        return self.BASE_URL.format(subdomain=self.subdomain)

    async def _rate_limit(self):
        """Simple rate limiting by delaying between requests"""
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
        """
        Make API request with retry logic and error handling.
        """
        await self._rate_limit()

        headers = {
            "Authorization": f"Bearer {self.api_key}",
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
                    elif 400 <= response.status < 500:
                        raise Exception(f"Client error: {data.get('detail', 'Unknown error')}")
                    else:
                        raise Exception(f"Server error: {response.status} - {data}")

            except aiohttp.ClientError as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise Exception(f"Request failed after {self.MAX_RETRIES} attempts: {str(e)}")
                await asyncio.sleep(2 ** attempt)

    # ==================== Lead Operations ====================

    async def add_lead(self, lead: Lead) -> Lead:
        """Add a new lead (Add Lead)"""
        lead_data = {
            "name": lead.name,
            "status_id": lead.status_id,
            "pipeline_id": lead.pipeline_id,
            "price": lead.price,
            "responsible_user_id": lead.responsible_user_id,
            "created_by": lead.created_by,
            "custom_fields_values": lead.custom_fields
        }

        # Remove None values
        lead_data = {k: v for k, v in lead_data.items() if v is not None}

        response = await self._request("POST", "/leads", json_data=[lead_data])
        lead_data = response.get("_embedded", {}).get("leads", [])[0]
        return Lead(**lead_data)

    async def update_lead(self, lead_id: int, lead: Lead) -> Lead:
        """Update existing lead (Update Lead)"""
        lead_data = {
            "name": lead.name,
            "status_id": lead.status_id,
            "pipeline_id": lead.pipeline_id,
            "price": lead.price,
            "responsible_user_id": lead.responsible_user_id,
            "custom_fields_values": lead.custom_fields
        }

        lead_data = {k: v for k, v in lead_data.items() if v is not None}

        response = await self._request("PATCH", f"/leads/{lead_id}", json_data=lead_data)
        return Lead(**response)

    async def search_leads(
        self,
        query: Optional[str] = None,
        status_id: Optional[int] = None,
        limit: int = 50
    ) -> List[Lead]:
        """Search leads (Search Leads)"""
        params = {"limit": limit}

        if query:
            params["query"] = query
        if status_id:
            params["filter[status_id]"] = status_id

        response = await self._request("GET", "/leads", params=params)
        leads = response.get("_embedded", {}).get("leads", [])
        return [Lead(**l) for l in leads]

    # ==================== Contact Operations ====================

    async def add_contact(self, contact: Contact) -> Contact:
        """Add a new contact (Add Contact)"""
        contact_data = {
            "name": contact.name,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "responsible_user_id": contact.responsible_user_id,
            "created_by": contact.created_by,
            "custom_fields_values": contact.custom_fields
        }

        contact_data = {k: v for k, v in contact_data.items() if v is not None}

        response = await self._request("POST", "/contacts", json_data=[contact_data])
        contact_data = response.get("_embedded", {}).get("contacts", [])[0]
        return Contact(**contact_data)

    async def update_contact(self, contact_id: int, contact: Contact) -> Contact:
        """Update existing contact (Update Contact)"""
        contact_data = {
            "name": contact.name,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "responsible_user_id": contact.responsible_user_id,
            "custom_fields_values": contact.custom_fields
        }

        contact_data = {k: v for k, v in contact_data.items() if v is not None}

        response = await self._request("PATCH", f"/contacts/{contact_id}", json_data=contact_data)
        return Contact(**response)

    async def search_contacts(
        self,
        query: Optional[str] = None,
        limit: int = 50
    ) -> List[Contact]:
        """Search contacts (Search Contacts)"""
        params = {"limit": limit}

        if query:
            params["query"] = query

        response = await self._request("GET", "/contacts", params=params)
        contacts = response.get("_embedded", {}).get("contacts", [])
        return [Contact(**c) for c in contacts]

    # ==================== Company Operations ====================

    async def add_company(self, company: Company) -> Company:
        """Add a new company (Add Company)"""
        company_data = {
            "name": company.name,
            "responsible_user_id": company.responsible_user_id,
            "created_by": company.created_by,
            "custom_fields_values": company.custom_fields
        }

        company_data = {k: v for k, v in company_data.items() if v is not None}

        response = await self._request("POST", "/companies", json_data=[company_data])
        company_data = response.get("_embedded", {}).get("companies", [])[0]
        return Company(**company_data)

    async def update_company(self, company_id: int, company: Company) -> Company:
        """Update existing company (Update Company)"""
        company_data = {
            "name": company.name,
            "responsible_user_id": company.responsible_user_id,
            "custom_fields_values": company.custom_fields
        }

        company_data = {k: v for k, v in company_data.items() if v is not None}

        response = await self._request("PATCH", f"/companies/{company_id}", json_data=company_data)
        return Company(**response)

    async def search_companies(
        self,
        query: Optional[str] = None,
        limit: int = 50
    ) -> List[Company]:
        """Search companies (Search Companies)"""
        params = {"limit": limit}

        if query:
            params["query"] = query

        response = await self._request("GET", "/companies", params=params)
        companies = response.get("_embedded", {}).get("companies", [])
        return [Company(**c) for c in companies]

    # ==================== Task Operations ====================

    async def add_task(self, task: Task) -> Task:
        """Add a new task (Add Task)"""
        task_data = {
            "text": task.text,
            "task_type_id": task.task_type_id,
            "entity_type": task.entity_type,
            "entity_id": task.entity_id,
            "complete_till": task.complete_till,
            "created_by": task.created_by,
            "responsible_user_id": task.responsible_user_id
        }

        task_data = {k: v for k, v in task_data.items() if v is not None}

        response = await self._request("POST", "/tasks", json_data=[task_data])
        task_data = response.get("_embedded", {}).get("tasks", [])[0]
        return Task(**task_data)

    async def update_task(self, task_id: int, task: Task) -> Task:
        """Update existing task (Update Task)"""
        task_data = {
            "text": task.text,
            "task_type_id": task.task_type_id,
            "complete_till": task.complete_till,
            "is_completed": task.is_completed,
            "responsible_user_id": task.responsible_user_id,
            "result": task.result
        }

        task_data = {k: v for k, v in task_data.items() if v is not None}

        response = await self._request("PATCH", f"/tasks/{task_id}", json_data=task_data)
        return Task(**response)

    async def search_tasks(
        self,
        entity_type: Optional[str] = None,
        entity_id: Optional[int] = None,
        is_completed: Optional[bool] = None,
        limit: int = 50
    ) -> List[Task]:
        """Search tasks (Search Tasks)"""
        params = {"limit": limit}

        if entity_type:
            params["filter[entity_type]"] = entity_type
        if entity_id:
            params["filter[entity_id]"] = entity_id
        if is_completed is not None:
            params["filter[is_completed]"] = is_completed

        response = await self._request("GET", "/tasks", params=params)
        tasks = response.get("_embedded", {}).get("tasks", [])
        return [Task(**t) for t in tasks]

    # ==================== Note Operations ====================

    async def add_note(self, note: Note) -> Note:
        """Add a new note (Add Note)"""
        note_data = {
            "note_type": note.note_type,
            "entity_type": note.entity_type,
            "entity_id": note.entity_id,
            "params": note.params,
            "created_by": note.created_by
        }

        # Handle text based on note type
        if note.note_type == "common":
            note_data["params"]["text"] = note.text

        note_data = {k: v for k, v in note_data.items() if v is not None}

        response = await self._request("POST", "/notes", json_data=[note_data])
        note_data = response.get("_embedded", {}).get("notes", [])[0]
        return Note(**note_data)

    async def update_note(self, note_id: int, note: Note) -> Note:
        """Update existing note (Update Note)"""
        note_data = {
            "params": note.params,
            "updated_by": note.created_by
        }

        # Handle text based on note type
        if note.note_type == "common":
            if "params" not in note_data:
                note_data["params"] = {}
            note_data["params"]["text"] = note.text

        note_data = {k: v for k, v in note_data.items() if v is not None}

        response = await self._request("PATCH", f"/notes/{note_id}", json_data=note_data)
        return Note(**response)

    async def search_notes_by_entity_type(
        self,
        entity_type: str,
        entity_id: Optional[int] = None,
        limit: int = 50
    ) -> List[Note]:
        """Search notes by entity type (Search Notes by Entity Type)"""
        params = {
            "filter[entity_type]": entity_type,
            "limit": limit
        }

        if entity_id:
            params["filter[entity_id]"] = entity_id

        response = await self._request("GET", "/notes", params=params)
        notes = response.get("_embedded", {}).get("notes", [])
        return [Note(**n) for n in notes]

    async def search_notes_by_entity_id(
        self,
        entity_type: str,
        entity_id: int,
        note_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Note]:
        """Search notes by entity ID (Search Notes by Entity ID)"""
        params = {
            "filter[entity_type]": entity_type,
            "filter[entity_id]": entity_id,
            "limit": limit
        }

        if note_type:
            params["filter[note_type]"] = note_type

        response = await self._request("GET", "/notes", params=params)
        notes = response.get("_embedded", {}).get("notes", [])
        return [Note(**n) for n in notes]

    # ==================== Tag Operations ====================

    async def search_tags(
        self,
        entity_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Search tags (Search Tags)"""
        params = {"limit": limit}

        if entity_type:
            params["filter[entity_type]"] = entity_type

        response = await self._request("GET", "/tags", params=params)
        tags = response.get("_embedded", {}).get("tags", [])
        return tags

    async def add_tags_to_entity(
        self,
        entity_type: str,
        entity_id: int,
        tags: List[int]
    ) -> bool:
        """Add tags to entity (Add Tags to Entity)"""
        for tag_id in tags:
            endpoint = f"/{entity_type}/{entity_id}/tags/{tag_id}"
            await self._request("POST", endpoint)
        return True


# ==================== Example Usage ====================

async def main():
    """Example usage of Kommo client"""

    # Replace with your actual credentials
    subdomain = "your_subdomain"
    api_key = "your_kommo_api_key"

    async with KommoClient(subdomain=subdomain, api_key=api_key) as client:
        # Add a lead
        lead = Lead(
            name="New Deal",
            status_id=123,
            pipeline_id=1,
            price=50000.0,
            responsible_user_id=1
        )
        created_lead = await client.add_lead(lead)
        print(f"Created lead: {created_lead.name} (ID: {created_lead.id})")

        # Add a contact
        contact = Contact(
            name="John Doe",
            first_name="John",
            last_name="Doe",
            responsible_user_id=1
        )
        created_contact = await client.add_contact(contact)
        print(f"Created contact: {created_contact.name} (ID: {created_contact.id})")

        # Add a task
        task = Task(
            text="Follow up call",
            task_type_id=1,
            entity_type="leads",
            entity_id=created_lead.id,
            complete_till=int(time.time()) + 86400  # 24 hours from now
        )
        created_task = await client.add_task(task)
        print(f"Created task: {created_task.text}")


if __name__ == "__main__":
    asyncio.run(main())