"""
Clio Manage API Client

Complete client for Clio Manage legal practice management system.
Supports matter management, contacts, tasks, time tracking, communications,
and billing operations.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, field
import json


class ClioAPIError(Exception):
    """Base exception for Clio API errors"""

    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class ClioRateLimitError(ClioAPIError):
    """Raised when rate limit is exceeded"""


@dataclass
class Matter:
    """Matter (Case) data model"""
    matter_id: str
    name: str
    client_id: str
    status: str
    description: Optional[str] = None
    practice_area: Optional[str] = None
    date_opened: Optional[str] = None
    date_closed: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PersonContact:
    """Person contact data model"""
    contact_id: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    type: str = "person"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CompanyContact:
    """Company contact data model"""
    contact_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    type: str = "company"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """Task data model"""
    task_id: str
    name: str
    matter_id: str
    status: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TimeEntry:
    """Time entry data model"""
    time_entry_id: str
    matter_id: str
    person_id: str
    duration: int  # in seconds
    date: str
    note: Optional[str] = None
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExpenseEntry:
    """Expense entry data model"""
    expense_id: str
    matter_id: str
    person_id: str
    amount: float
    date: str
    note: Optional[str] = None
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Communication:
    """Communication data model"""
    communication_id: str
    matter_id: str
    direction: str  # "incoming", "outgoing", "internal"
    subject: Optional[str] = None
    body: Optional[str] = None
    date: Optional[str] = None
    communication_type: Optional[str] = None  # "email", "call", "note"
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CalendarEntry:
    """Calendar entry data model"""
    entry_id: str
    matter_id: str
    title: str
    start_datetime: str
    end_datetime: str
    location: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Bill:
    """Bill data model"""
    bill_id: str
    matter_id: str
    total_amount: float
    status: str
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class ClioManageClient:
    """
    Clio Manage API Client

    Provides complete access to Clio Manage API for legal practice
    management, including matters, contacts, tasks, time tracking,
    communications, and billing.
    """

    BASE_URL = "https://app.clio.com/api/v4"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        max_requests_per_minute: int = 100,
        timeout: int = 30
    ):
        """
        Initialize Clio Manage client.

        Args:
            api_key: API key for authentication
            base_url: Optional custom base URL
            max_requests_per_minute: Rate limit (requests per minute)
            timeout: Request timeout in seconds
        """
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
        """
        Make an API request with error handling and rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters

        Returns:
            Response data as dict
        """
        await self._check_rate_limit()

        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
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
                headers=headers
            ) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = await response.text()

                if response.status == 429:
                    raise ClioRateLimitError(
                        "Rate limit exceeded",
                        status_code=429,
                        response=response_data
                    )

                if response.status >= 400:
                    error_msg = response_data.get("error", {}).get("message", str(response_data))
                    raise ClioAPIError(
                        error_msg,
                        status_code=response.status,
                        response=response_data
                    )

                return response_data if isinstance(response_data, dict) else {}

        except aiohttp.ClientError as e:
            raise ClioAPIError(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise ClioAPIError(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            if isinstance(e, ClioAPIError):
                raise
            raise ClioAPIError(f"Unexpected error: {str(e)}")

    # ==================== Matters ====================

    async def create_matter(self, matter_data: Dict[str, Any]) -> Matter:
        """Create a new matter (case)."""
        data = await self._request("POST", "/matters", data={"data": matter_data})
        result = data.get("data", {})
        return Matter(
            matter_id=result.get("id", ""),
            name=result.get("name", ""),
            client_id=result.get("client", {}).get("id", ""),
            status=result.get("status", ""),
            description=result.get("description"),
            practice_area=result.get("practice_area"),
            date_opened=result.get("date_opened"),
            date_closed=result.get("date_closed"),
            created_at=result.get("created_at"),
            updated_at=result.get("updated_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "name", "client", "status", "description",
                "practice_area", "date_opened", "date_closed",
                "created_at", "updated_at"
            ]}
        )

    async def update_matter(self, matter_id: str, update_data: Dict[str, Any]) -> Matter:
        """Update an existing matter."""
        data = await self._request("PUT", f"/matters/{matter_id}", data={"data": update_data})
        result = data.get("data", {})
        return Matter(
            matter_id=result.get("id", matter_id),
            name=result.get("name", ""),
            client_id=result.get("client", {}).get("id", ""),
            status=result.get("status", ""),
            description=result.get("description"),
            practice_area=result.get("practice_area"),
            date_opened=result.get("date_opened"),
            date_closed=result.get("date_closed"),
            created_at=result.get("created_at"),
            updated_at=result.get("updated_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "name", "client", "status", "description",
                "practice_area", "date_opened", "date_closed",
                "created_at", "updated_at"
            ]}
        )

    async def get_matter(self, matter_id: str) -> Matter:
        """Get matter details."""
        data = await self._request("GET", f"/matters/{matter_id}")
        result = data.get("data", {})
        return Matter(
            matter_id=result.get("id", matter_id),
            name=result.get("name", ""),
            client_id=result.get("client", {}).get("id", ""),
            status=result.get("status", ""),
            description=result.get("description"),
            practice_area=result.get("practice_area"),
            date_opened=result.get("date_opened"),
            date_closed=result.get("date_closed"),
            created_at=result.get("created_at"),
            updated_at=result.get("updated_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "name", "client", "status", "description",
                "practice_area", "date_opened", "date_closed",
                "created_at", "updated_at"
            ]}
        )

    async def search_matters(
        self,
        client_id: Optional[str] = None,
        status: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Matter]:
        """Search for matters."""
        params = {"limit": limit, "offset": offset}
        if client_id:
            params["client_id"] = client_id
        if status:
            params["status"] = status
        if query:
            params["query"] = query

        data = await self._request("GET", "/matters", params=params)
        results = data.get("data", [])

        return [
            Matter(
                matter_id=r.get("id", ""),
                name=r.get("name", ""),
                client_id=r.get("client", {}).get("id", ""),
                status=r.get("status", ""),
                description=r.get("description"),
                practice_area=r.get("practice_area"),
                date_opened=r.get("date_opened"),
                date_closed=r.get("date_closed"),
                created_at=r.get("created_at"),
                updated_at=r.get("updated_at"),
                additional_data={k: v for k, v in r.items() if k not in [
                    "id", "name", "client", "status", "description",
                    "practice_area", "date_opened", "date_closed",
                    "created_at", "updated_at"
                ]}
            )
            for r in results
        ]

    async def create_matter_folder(self, matter_id: str, folder_name: str) -> Dict[str, Any]:
        """Create a folder within a matter."""
        return await self._request(
            "POST",
            f"/matters/{matter_id}/folders",
            data={"name": folder_name}
        )

    async def create_matter_note(self, matter_id: str, note_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a note within a matter."""
        return await self._request(
            "POST",
            f"/matters/{matter_id}/notes",
            data=note_data
        )

    # ==================== Contacts ====================

    async def create_person_contact(self, contact_data: Dict[str, Any]) -> PersonContact:
        """Create a new person contact."""
        data = await self._request("POST", "/persons", data={"data": contact_data})
        result = data.get("data", {})
        return PersonContact(
            contact_id=result.get("id", ""),
            first_name=result.get("first_name", ""),
            last_name=result.get("last_name", ""),
            email=result.get("email"),
            phone=result.get("primary_phone_number"),
            address=result.get("primary_address"),
            type="person",
            created_at=result.get("created_at"),
            updated_at=result.get("updated_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "first_name", "last_name", "email",
                "primary_phone_number", "primary_address",
                "created_at", "updated_at"
            ]}
        )

    async def update_person_contact(
        self,
        contact_id: str,
        update_data: Dict[str, Any]
    ) -> PersonContact:
        """Update a person contact."""
        data = await self._request("PUT", f"/persons/{contact_id}", data={"data": update_data})
        result = data.get("data", {})
        return PersonContact(
            contact_id=result.get("id", contact_id),
            first_name=result.get("first_name", ""),
            last_name=result.get("last_name", ""),
            email=result.get("email"),
            phone=result.get("primary_phone_number"),
            address=result.get("primary_address"),
            type="person",
            created_at=result.get("created_at"),
            updated_at=result.get("updated_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "first_name", "last_name", "email",
                "primary_phone_number", "primary_address",
                "created_at", "updated_at"
            ]}
        )

    async def create_company_contact(self, contact_data: Dict[str, Any]) -> CompanyContact:
        """Create a new company contact."""
        data = await self._request("POST", "/companies", data={"data": contact_data})
        result = data.get("data", {})
        return CompanyContact(
            contact_id=result.get("id", ""),
            name=result.get("name", ""),
            email=result.get("email"),
            phone=result.get("primary_phone_number"),
            address=result.get("primary_address"),
            type="company",
            created_at=result.get("created_at"),
            updated_at=result.get("updated_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "name", "email", "primary_phone_number",
                "primary_address", "created_at", "updated_at"
            ]}
        )

    async def update_company_contact(
        self,
        contact_id: str,
        update_data: Dict[str, Any]
    ) -> CompanyContact:
        """Update a company contact."""
        data = await self._request("PUT", f"/companies/{contact_id}", data={"data": update_data})
        result = data.get("data", {})
        return CompanyContact(
            contact_id=result.get("id", contact_id),
            name=result.get("name", ""),
            email=result.get("email"),
            phone=result.get("primary_phone_number"),
            address=result.get("primary_address"),
            type="company",
            created_at=result.get("created_at"),
            updated_at=result.get("updated_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "name", "email", "primary_phone_number",
                "primary_address", "created_at", "updated_at"
            ]}
        )

    async def search_persons_or_companies(
        self,
        query: Optional[str] = None,
        contact_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Any]:
        """Search for contacts (persons and companies)."""
        params = {"limit": limit, "offset": offset}
        if query:
            params["query"] = query
        if contact_type:
            params["type"] = contact_type

        data = await self._request("GET", "/contacts", params=params)
        results = data.get("data", [])

        contacts = []
        for r in results:
            contact_type = r.get("type", "Person")
            if contact_type == "Person":
                contacts.append(PersonContact(
                    contact_id=r.get("id", ""),
                    first_name=r.get("first_name", ""),
                    last_name=r.get("last_name", ""),
                    email=r.get("email"),
                    phone=r.get("primary_phone_number"),
                    address=r.get("primary_address"),
                    type="person",
                    created_at=r.get("created_at"),
                    updated_at=r.get("updated_at"),
                    additional_data={k: v for k, v in r.items() if k not in [
                        "id", "first_name", "last_name", "email",
                        "primary_phone_number", "primary_address",
                        "created_at", "updated_at", "type"
                    ]}
                ))
            else:
                contacts.append(CompanyContact(
                    contact_id=r.get("id", ""),
                    name=r.get("name", ""),
                    email=r.get("email"),
                    phone=r.get("primary_phone_number"),
                    address=r.get("primary_address"),
                    type="company",
                    created_at=r.get("created_at"),
                    updated_at=r.get("updated_at"),
                    additional_data={k: v for k, v in r.items() if k not in [
                        "id", "name", "email", "primary_phone_number",
                        "primary_address", "created_at", "updated_at", "type"
                    ]}
                ))

        return contacts

    async def search_user(self, query: str) -> List[Dict[str, Any]]:
        """Search for users."""
        params = {"query": query}
        data = await self._request("GET", "/users", params=params)
        return data.get("data", [])

    # ==================== Tasks ====================

    async def create_task(self, task_data: Dict[str, Any]) -> Task:
        """Create a new task."""
        data = await self._request("POST", "/tasks", data={"data": task_data})
        result = data.get("data", {})
        return Task(
            task_id=result.get("id", ""),
            name=result.get("name", ""),
            matter_id=result.get("matter", {}).get("id", ""),
            status=result.get("status", ""),
            description=result.get("description"),
            due_date=result.get("due_date"),
            created_at=result.get("created_at"),
            updated_at=result.get("updated_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "name", "matter", "status", "description",
                "due_date", "created_at", "updated_at"
            ]}
        )

    async def update_task(self, task_id: str, update_data: Dict[str, Any]) -> Task:
        """Update an existing task."""
        data = await self._request("PUT", f"/tasks/{task_id}", data={"data": update_data})
        result = data.get("data", {})
        return Task(
            task_id=result.get("id", task_id),
            name=result.get("name", ""),
            matter_id=result.get("matter", {}).get("id", ""),
            status=result.get("status", ""),
            description=result.get("description"),
            due_date=result.get("due_date"),
            created_at=result.get("created_at"),
            updated_at=result.get("updated_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "name", "matter", "status", "description",
                "due_date", "created_at", "updated_at"
            ]}
        )

    async def get_task(self, task_id: str) -> Task:
        """Get task details."""
        data = await self._request("GET", f"/tasks/{task_id}")
        result = data.get("data", {})
        return Task(
            task_id=result.get("id", task_id),
            name=result.get("name", ""),
            matter_id=result.get("matter", {}).get("id", ""),
            status=result.get("status", ""),
            description=result.get("description"),
            due_date=result.get("due_date"),
            created_at=result.get("created_at"),
            updated_at=result.get("updated_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "name", "matter", "status", "description",
                "due_date", "created_at", "updated_at"
            ]}
        )

    async def assign_task_template_list(
        self,
        task_id: str,
        template_id: str
    ) -> Dict[str, Any]:
        """Assign a task template list to a task."""
        return await self._request(
            "POST",
            f"/tasks/{task_id}/templates",
            data={"template_id": template_id}
        )

    # ==================== Time & Expenses ====================

    async def create_time_entry(self, time_data: Dict[str, Any]) -> TimeEntry:
        """Create a new time entry."""
        data = await self._request("POST", "/time_entries", data={"data": time_data})
        result = data.get("data", {})
        return TimeEntry(
            time_entry_id=result.get("id", ""),
            matter_id=result.get("matter", {}).get("id", ""),
            person_id=result.get("person", {}).get("id", ""),
            duration=result.get("duration", 0),
            date=result.get("date", ""),
            note=result.get("note"),
            created_at=result.get("created_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "matter", "person", "duration", "date", "note", "created_at"
            ]}
        )

    async def create_expense_entry(self, expense_data: Dict[str, Any]) -> ExpenseEntry:
        """Create a new expense entry."""
        data = await self._request("POST", "/expense_entries", data={"data": expense_data})
        result = data.get("data", {})
        return ExpenseEntry(
            expense_id=result.get("id", ""),
            matter_id=result.get("matter", {}).get("id", ""),
            person_id=result.get("person", {}).get("id", ""),
            amount=result.get("amount", 0.0),
            date=result.get("date", ""),
            note=result.get("note"),
            created_at=result.get("created_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "matter", "person", "amount", "date", "note", "created_at"
            ]}
        )

    # ==================== Communications ====================

    async def create_communication(
        self,
        comm_data: Dict[str, Any]
    ) -> Communication:
        """Create a new communication."""
        data = await self._request("POST", "/communications", data={"data": comm_data})
        result = data.get("data", {})
        return Communication(
            communication_id=result.get("id", ""),
            matter_id=result.get("matter", {}).get("id", ""),
            direction=result.get("direction", ""),
            subject=result.get("subject"),
            body=result.get("body"),
            date=result.get("date"),
            communication_type=result.get("type"),
            created_at=result.get("created_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "matter", "direction", "subject", "body", "date", "type", "created_at"
            ]}
        )

    # ==================== Calendar ====================

    async def create_calendar_entry(
        self,
        entry_data: Dict[str, Any]
    ) -> CalendarEntry:
        """Create a new calendar entry."""
        data = await self._request("POST", "/calendar_entries", data={"data": entry_data})
        result = data.get("data", {})
        return CalendarEntry(
            entry_id=result.get("id", ""),
            matter_id=result.get("matter", {}).get("id", ""),
            title=result.get("title", ""),
            start_datetime=result.get("start_at", ""),
            end_datetime=result.get("end_at", ""),
            location=result.get("location"),
            description=result.get("description"),
            created_at=result.get("created_at"),
            additional_data={k: v for k, v in result.items() if k not in [
                "id", "matter", "title", "start_at", "end_at",
                "location", "description", "created_at"
            ]}
        )

    # ==================== Billing ====================

    async def search_bills(
        self,
        matter_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Bill]:
        """Search for bills."""
        params = {"limit": limit, "offset": offset}
        if matter_id:
            params["matter_id"] = matter_id
        if status:
            params["status"] = status

        data = await self._request("GET", "/bills", params=params)
        results = data.get("data", [])

        return [
            Bill(
                bill_id=r.get("id", ""),
                matter_id=r.get("matter", {}).get("id", ""),
                total_amount=r.get("total", 0.0),
                status=r.get("status", ""),
                invoice_date=r.get("invoice_date"),
                due_date=r.get("due_date"),
                created_at=r.get("created_at"),
                additional_data={k: v for k, v in r.items() if k not in [
                    "id", "matter", "total", "status",
                    "invoice_date", "due_date", "created_at"
                ]}
            )
            for r in results
        ]

    async def close(self):
        """Close the client session."""
        if self.session and not self.session.closed:
            await self.session.close()


# ==================== Example Usage ====================

async def main():
    """Example usage of Clio Manage client."""

    async with ClioManageClient(api_key="your_api_key") as client:
        # Create a matter
        matter = await client.create_matter({
            "name": "Client Smith - Divorce Case",
            "client_id": "12345",
            "description": "Divorce proceedings",
            "status": "Open"
        })
        print(f"Created matter: {matter.matter_id}")

        # Create a person contact
        contact = await client.create_person_contact({
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com"
        })
        print(f"Created contact: {contact.contact_id}")

        # Create a task
        task = await client.create_task({
            "name": "File divorce petition",
            "matter": {"id": matter.matter_id},
            "status": "Pending"
        })
        print(f"Created task: {task.task_id}")

        # Create a time entry
        time_entry = await client.create_time_entry({
            "matter": {"id": matter.matter_id},
            "duration": 3600,  # 1 hour
            "date": "2024-01-15",
            "note": "Initial consultation"
        })
        print(f"Created time entry: {time_entry.time_entry_id}")


if __name__ == "__main__":
    asyncio.run(main())