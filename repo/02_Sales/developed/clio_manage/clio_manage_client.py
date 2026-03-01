"""
Clio Manage API Client

Clio Manage is a legal practice management platform.

Supports:
- Create Matter Note
- Create Matter Folder
- Create Matter
- Update Matter
- Search Matters
- Create Person Contact
- Update Person Contact
- Create Company Contact
- Update Company Contact
- Search Persons or Companies
- Create Task
- Update Task
- Assign Task Template List
- Create Calendar Entry
- Create Time Entry
- Create Expense Entry
- Search Bills
- Create Communication
- Search User
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Matter:
    """Matter object (Legal Case/Project)"""
    id: int
    display_number: str
    description: str
    status: str
    matter_type: Optional[str]
    client_id: int
    client_name: Optional[str]
    opened_at: str
    closed_at: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Contact:
    """Contact object (Person or Company)"""
    id: int
    name: str
    type: str  # Person or Company
    first_name: Optional[str]
    last_name: Optional[str]
    primary_email: Optional[str]
    primary_phone: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Task:
    """Task object"""
    id: int
    matter_id: Optional[int]
    description: str
    status: str  # open, completed, cancelled
    priority: str  # low, medium, high
    due_at: Optional[str]
    completed_at: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class CalendarEntry:
    """Calendar Entry object"""
    id: int
    matter_id: Optional[int]
    title: str
    description: Optional[str]
    start_at: str
    end_at: str
    location: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class TimeEntry:
    """Time Entry object"""
    id: int
    matter_id: int
    duration: int  # seconds
    description: str
    date: str
    created_at: str
    updated_at: str


@dataclass
class ExpenseEntry:
    """Expense Entry object"""
    id: int
    matter_id: int
    amount: float
    currency: str
    description: str
    date: str
    created_at: str
    updated_at: str


class ClioManageClient:
    """
    Clio Manage API client for legal practice management.

    Authentication: OAuth 2.0
    Documentation: https://app.clio.com/api/v4/documentation
    Base URL: https://app.clio.com/api/v4
    """

    BASE_URL = "https://app.clio.com/api/v4"

    def __init__(self, access_token: str):
        """
        Initialize Clio Manage API client.

        Args:
            access_token: OAuth access token
        """
        self.access_token = access_token
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.access_token}",
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
        Make HTTP request to Clio Manage API.

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
            data = await response.json()

            if response.status not in [200, 201, 204]:
                error_msg = data.get("message", "Unknown error")
                raise Exception(f"Clio Manage API error ({response.status}): {error_msg}")

            return data

    # ==================== Matters ====================

    async def create_matter(
        self,
        description: str,
        client_id: int,
        matter_type_id: Optional[int] = None,
        status: str = "Open"
    ) -> Matter:
        """
        Create a new matter.

        Args:
            description: Matter description
            client_id: Client (contact) ID
            matter_type_id: Optional matter type ID
            status: Matter status

        Returns:
            Matter object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "data": {
                "description": description,
                "client": {"id": client_id},
                "status": status
            }
        }

        if matter_type_id:
            json_data["data"]["matter_type"] = {"id": matter_type_id}

        data = await self._request("POST", "/matters.json", json_data=json_data)

        return self._parse_matter(data["data"])

    async def get_matter(self, matter_id: int) -> Matter:
        """
        Get a matter by ID.

        Args:
            matter_id: Matter ID

        Returns:
            Matter object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/matters/{matter_id}.json")
        return self._parse_matter(data["data"])

    async def search_matters(
        self,
        client_id: Optional[int] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Matter]:
        """
        Search for matters.

        Args:
            client_id: Filter by client ID
            status: Filter by status
            limit: Maximum number of results

        Returns:
            List of Matter objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit}

        if client_id:
            params["client_id"] = client_id
        if status:
            params["status"] = status

        data = await self._request("GET", "/matters.json", params=params)

        return [self._parse_matter(m) for m in data.get("data", [])]

    async def update_matter(
        self,
        matter_id: int,
        description: Optional[str] = None,
        status: Optional[str] = None,
        close_date: Optional[str] = None
    ) -> Matter:
        """
        Update a matter.

        Args:
            matter_id: Matter ID
            description: New description
            status: New status
            close_date: Close date (YYYY-MM-DD)

        Returns:
            Updated Matter object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if description:
            json_data["description"] = description
        if status:
            json_data["status"] = status
        if close_date:
            json_data["closed_at"] = close_date

        data = await self._request(
            "PUT",
            f"/matters/{matter_id}.json",
            json_data={"data": json_data}
        )

        return self._parse_matter(data["data"])

    async def create_matter_note(
        self,
        matter_id: int,
        content: str,
        private: bool = False
    ) -> Dict[str, Any]:
        """
        Create a note for a matter.

        Args:
            matter_id: Matter ID
            content: Note content
            private: Whether note is private

        Returns:
            Created note data

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "data": {
                "content": content,
                "private": private,
                "matter": {"id": matter_id}
            }
        }

        data = await self._request("POST", "/notes.json", json_data=json_data)
        return data["data"]

    async def create_matter_folder(
        self,
        matter_id: int,
        name: str
    ) -> Dict[str, Any]:
        """
        Create a folder for a matter.

        Args:
            matter_id: Matter ID
            name: Folder name

        Returns:
            Created folder data

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "data": {
                "name": name,
                "folder": {"id": matter_id}
            }
        }

        data = await self._request("POST", "/folders.json", json_data=json_data)
        return data["data"]

    def _parse_matter(self, data: Dict[str, Any]) -> Matter:
        """Parse matter data"""
        client = data.get("client", {})
        return Matter(
            id=int(data.get("id", 0)),
            display_number=data.get("display_number", ""),
            description=data.get("description", ""),
            status=data.get("status", ""),
            matter_type=data.get("matter_type", {}).get("name") if data.get("matter_type") else None,
            client_id=int(client.get("id", 0)) if client else 0,
            client_name=client.get("name") if client else None,
            opened_at=data.get("opened_at", ""),
            closed_at=data.get("closed_at"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Contacts ====================

    async def create_person_contact(
        self,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        title: Optional[str] = None
    ) -> Contact:
        """
        Create a new person contact.

        Args:
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number
            title: Job title

        Returns:
            Contact object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "data": {
                "type": "Person",
                "first_name": first_name,
                "last_name": last_name
            }
        }

        if email:
            json_data["data"]["primary_email"] = email
        if phone:
            json_data["data"]["primary_phone_number"] = phone
        if title:
            json_data["data"]["title"] = title

        data = await self._request("POST", "/contacts.json", json_data=json_data)

        return self._parse_contact(data["data"])

    async def create_company_contact(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        website: Optional[str] = None
    ) -> Contact:
        """
        Create a new company contact.

        Args:
            name: Company name
            email: Email address
            phone: Phone number
            website: Website URL

        Returns:
            Contact object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "data": {
                "type": "Company",
                "name": name
            }
        }

        if email:
            json_data["data"]["primary_email"] = email
        if phone:
            json_data["data"]["primary_phone_number"] = phone
        if website:
            json_data["data"]["website"] = website

        data = await self._request("POST", "/contacts.json", json_data=json_data)

        return self._parse_contact(data["data"])

    async def search_contacts(
        self,
        query: Optional[str] = None,
        contact_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Contact]:
        """
        Search for contacts (persons or companies).

        Args:
            query: Search query
            contact_type: Filter by type (Person, Company)
            limit: Maximum number of results

        Returns:
            List of Contact objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit}

        if query:
            params["q"] = query
        if contact_type:
            params["type"] = contact_type

        data = await self._request("GET", "/contacts.json", params=params)

        return [self._parse_contact(c) for c in data.get("data", [])]

    async def update_person_contact(
        self,
        contact_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        title: Optional[str] = None
    ) -> Contact:
        """
        Update a person contact.

        Args:
            contact_id: Contact ID
            first_name: New first name
            last_name: New last name
            email: New email
            phone: New phone
            title: New title

        Returns:
            Updated Contact object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if first_name:
            json_data["first_name"] = first_name
        if last_name:
            json_data["last_name"] = last_name
        if email:
            json_data["primary_email"] = email
        if phone:
            json_data["primary_phone_number"] = phone
        if title:
            json_data["title"] = title

        data = await self._request(
            "PUT",
            f"/contacts/{contact_id}.json",
            json_data={"data": json_data}
        )

        return self._parse_contact(data["data"])

    async def update_company_contact(
        self,
        contact_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        website: Optional[str] = None
    ) -> Contact:
        """
        Update a company contact.

        Args:
            contact_id: Contact ID
            name: New name
            email: New email
            phone: New phone
            website: New website

        Returns:
            Updated Contact object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if email:
            json_data["primary_email"] = email
        if phone:
            json_data["primary_phone_number"] = phone
        if website:
            json_data["website"] = website

        data = await self._request(
            "PUT",
            f"/contacts/{contact_id}.json",
            json_data={"data": json_data}
        )

        return self._parse_contact(data["data"])

    def _parse_contact(self, data: Dict[str, Any]) -> Contact:
        """Parse contact data"""
        return Contact(
            id=int(data.get("id", 0)),
            name=data.get("name", ""),
            type=data.get("type", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            primary_email=data.get("primary_email"),
            primary_phone=data.get("primary_phone_number"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Tasks ====================

    async def create_task(
        self,
        description: str,
        matter_id: Optional[int] = None,
        priority: str = "normal",
        due_at: Optional[str] = None
    ) -> Task:
        """
        Create a new task.

        Args:
            description: Task description
            matter_id: Optional matter ID
            priority: Priority (low, normal, high)
            due_at: Due date (ISO 8601)

        Returns:
            Task object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "data": {
                "description": description,
                "priority": priority
            }
        }

        if matter_id:
            json_data["data"]["matter"] = {"id": matter_id}
        if due_at:
            json_data["data"]["due_at"] = due_at

        data = await self._request("POST", "/tasks.json", json_data=json_data)

        return self._parse_task(data["data"])

    async def update_task(
        self,
        task_id: int,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        due_at: Optional[str] = None
    ) -> Task:
        """
        Update a task.

        Args:
            task_id: Task ID
            description: New description
            status: New status (open, completed, cancelled)
            priority: New priority (low, normal, high)
            due_at: New due date

        Returns:
            Updated Task object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if description:
            json_data["description"] = description
        if status:
            json_data["status"] = status
        if priority:
            json_data["priority"] = priority
        if due_at:
            json_data["due_at"] = due_at

        if status == "completed":
            json_data["completed_at"] = datetime.utcnow().isoformat()

        data = await self._request(
            "PUT",
            f"/tasks/{task_id}.json",
            json_data={"data": json_data}
        )

        return self._parse_task(data["data"])

    async def assign_task_template_list(
        self,
        matter_id: int,
        task_template_list_id: int
    ) -> Dict[str, Any]:
        """
        Assign a task template list to a matter.

        Args:
            matter_id: Matter ID
            task_template_list_id: Task template list ID

        Returns:
            Assignment result

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "data": {
                "matter": {"id": matter_id},
                "task_template_list": {"id": task_template_list_id}
            }
        }

        data = await self._request("POST", "/task_assignments.json", json_data=json_data)

        return data["data"]

    # ==================== Calendar Entries ====================

    async def create_calendar_entry(
        self,
        title: str,
        start_at: str,
        end_at: str,
        matter_id: Optional[int] = None,
        description: Optional[str] = None,
        location: Optional[str] = None
    ) -> CalendarEntry:
        """
        Create a new calendar entry.

        Args:
            title: Entry title
            start_at: Start time (ISO 8601)
            end_at: End time (ISO 8601)
            matter_id: Optional matter ID
            description: Description
            location: Location

        Returns:
            CalendarEntry object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "data": {
                "title": title,
                "start_at": start_at,
                "end_at": end_at
            }
        }

        if matter_id:
            json_data["data"]["matter"] = {"id": matter_id}
        if description:
            json_data["data"]["description"] = description
        if location:
            json_data["data"]["location"] = location

        data = await self._request("POST", "/calendar_entries.json", json_data=json_data)

        return self._parse_calendar_entry(data["data"])

    # ==================== Time Entries ====================

    async def create_time_entry(
        self,
        matter_id: int,
        duration: int,
        description: str,
        activity_date: Optional[str] = None
    ) -> TimeEntry:
        """
        Create a new time entry.

        Args:
            matter_id: Matter ID
            duration: Duration in seconds
            description: Description
            activity_date: Activity date (YYYY-MM-DD)

        Returns:
            TimeEntry object

        Raises:
            Exception: If API returns error
        """
        if not activity_date:
            activity_date = datetime.utcnow().strftime("%Y-%m-%d")

        json_data = {
            "data": {
                "matter": {"id": matter_id},
                "duration": duration,
                "description": description,
                "date": activity_date
            }
        }

        data = await self._request("POST", "/activities.json", json_data=json_data)

        return self._parse_time_entry(data["data"])

    # ==================== Expense Entries ====================

    async def create_expense_entry(
        self,
        matter_id: int,
        amount: float,
        description: str,
        currency: str = "USD",
        expense_date: Optional[str] = None
    ) -> ExpenseEntry:
        """
        Create a new expense entry.

        Args:
            matter_id: Matter ID
            amount: Amount
            description: Description
            currency: Currency code
            expense_date: Expense date (YYYY-MM-DD)

        Returns:
            ExpenseEntry object

        Raises:
            Exception: If API returns error
        """
        if not expense_date:
            expense_date = datetime.utcnow().strftime("%Y-%m-%d")

        json_data = {
            "data": {
                "matter": {"id": matter_id},
                "amount": amount,
                "currency": currency,
                "description": description,
                "date": expense_date
            }
        }

        data = await self._request("POST", "/expense_entries.json", json_data=json_data)

        return self._parse_expense_entry(data["data"])

    # ====================communications ====================

    async def create_communication(
        self,
        subject: str,
        body: str,
        contact_id: int,
        sent_to: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Create a new communication.

        Args:
            subject: Subject
            body: Body text
            contact_id: Contact ID
            sent_to: List of recipient contact IDs

        Returns:
            Created communication data

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "data": {
                "subject": subject,
                "body": body,
                "people": [{"id": contact_id}]
            }
        }

        if sent_to:
            for recipient_id in sent_to:
                json_data["data"]["people"].append({"id": recipient_id})

        data = await self._request("POST", "/communications.json", json_data=json_data)

        return data["data"]

    # ==================== Bills ====================

    async def search_bills(
        self,
        matter_id: Optional[int] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search for bills.

        Args:
            matter_id: Filter by matter ID
            status: Filter by status
            limit: Maximum number of results

        Returns:
            List of bill objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit}

        if matter_id:
            params["matter_id"] = matter_id
        if status:
            params["status"] = status

        data = await self._request("GET", "/bills.json", params=params)

        return data.get("data", [])

    # ==================== Users ====================

    async def search_users(
        self,
        query: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search for users.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of user objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit}

        if query:
            params["q"] = query

        data = await self._request("GET", "/users.json", params=params)

        return data.get("data", [])

    # ==================== Helper Methods ====================

    def _parse_task(self, data: Dict[str, Any]) -> Task:
        """Parse task data"""
        return Task(
            id=int(data.get("id", 0)),
            matter_id=int(data.get("matter", {}).get("id", 0)) if data.get("matter") else None,
            description=data.get("description", ""),
            status=data.get("status", "open"),
            priority=data.get("priority", "normal"),
            due_at=data.get("due_at"),
            completed_at=data.get("completed_at"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    def _parse_calendar_entry(self, data: Dict[str, Any]) -> CalendarEntry:
        """Parse calendar entry data"""
        return CalendarEntry(
            id=int(data.get("id", 0)),
            matter_id=int(data.get("matter", {}).get("id", 0)) if data.get("matter") else None,
            title=data.get("title", ""),
            description=data.get("description"),
            start_at=data.get("start_at", ""),
            end_at=data.get("end_at", ""),
            location=data.get("location"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    def _parse_time_entry(self, data: Dict[str, Any]) -> TimeEntry:
        """Parse time entry data"""
        return TimeEntry(
            id=int(data.get("id", 0)),
            matter_id=int(data.get("matter", {}).get("id", 0)),
            duration=int(data.get("duration", 0)),
            description=data.get("description", ""),
            date=data.get("date", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    def _parse_expense_entry(self, data: Dict[str, Any]) -> ExpenseEntry:
        """Parse expense entry data"""
        return ExpenseEntry(
            id=int(data.get("id", 0)),
            matter_id=int(data.get("matter", {}).get("id", 0)),
            amount=float(data.get("amount", 0)),
            currency=data.get("currency", "USD"),
            description=data.get("description", ""),
            date=data.get("date", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )


# ==================== Example Usage ====================

async def main():
    """Example usage of Clio Manage API client"""

    access_token = "your_clio_access_token"

    async with ClioManageClient(access_token) as client:
        # Create a person contact
        person = await client.create_person_contact(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="+1234567890"
        )
        print(f"Created person contact: {person.id}")

        # Create a company contact
        company = await client.create_company_contact(
            name="Acme Corp",
            email="info@acme.com",
            website="https://acme.com"
        )
        print(f"Created company contact: {company.id}")

        # Create a matter
        matter = await client.create_matter(
            description="Legal Case: Doe vs. Smith",
            client_id=person.id
        )
        print(f"Created matter: {matter.id}")

        # Create a task
        task = await client.create_task(
            description="File initial documents",
            matter_id=matter.id,
            priority="high"
        )
        print(f"Created task: {task.id}")

        # Create a time entry
        time_entry = await client.create_time_entry(
            matter_id=matter.id,
            duration=3600,  # 1 hour in seconds
            description="Client consultation"
        )
        print(f"Created time entry: {time_entry.id}")

        # Search matters
        matters = await client.search_matters(limit=10)
        print(f"Found {len(matters)} matters")


if __name__ == "__main__":
    asyncio.run(main())