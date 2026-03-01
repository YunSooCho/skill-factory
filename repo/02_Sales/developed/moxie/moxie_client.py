"""
Moxie API - Client and Project Management Client

Supports clients, projects, tickets, invoices, tasks, calendar events, expenses, and file uploads.

API Actions (16):
1. Create Client
2. Add Comment to Ticket
3. Create Form Submission
4. Approve Deliverable
5. Create Contact
6. Search Client
7. Search Client Invoices
8. Create Project
9. Upload File
10. Create or Update Calendar Event
11. Create Expense
12. Create Invoice
13. Create Ticket
14. Search Projects
15. Create Task
16. Search Contact
"""

import aiohttp
import asyncio
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Client:
    """Client data model"""
    id: Optional[str] = None
    name: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    address: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""
    status: str = "active"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Contact:
    """Contact data model"""
    id: Optional[str] = None
    first_name: str = ""
    last_name: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    client_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Project:
    """Project data model"""
    id: Optional[str] = None
    name: str = ""
    description: str = ""
    client_id: Optional[str] = None
    status: str = "active"
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    budget: float = 0.0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Task:
    """Task data model"""
    id: Optional[str] = None
    title: str = ""
    description: str = ""
    project_id: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"
    due_date: Optional[str] = None
    assignee_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Ticket:
    """Ticket data model"""
    id: Optional[str] = None
    title: str = ""
    description: str = ""
    client_id: Optional[str] = None
    status: str = "open"
    priority: str = "normal"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Invoice:
    """Invoice data model"""
    id: Optional[str] = None
    client_id: str
    number: str = ""
    due_date: Optional[str] = None
    total: float = 0.0
    currency: str = "USD"
    status: str = "draft"
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Expense:
    """Expense data model"""
    id: Optional[str] = None
    project_id: Optional[str] = None
    amount: float = 0.0
    currency: str = "USD"
    description: str = ""
    date: Optional[str] = None
    category: str = ""
    created_at: Optional[str] = None


@dataclass
class CalendarEvent:
    """Calendar event data model"""
    id: Optional[str] = None
    title: str = ""
    description: str = ""
    start: Optional[str] = None
    end: Optional[str] = None
    all_day: bool = False
    client_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class MoxieClient:
    """
    Moxie API client for client and project management.

    API Documentation: https://www.moxie.com/api/
    Authentication: API Key via header
    Protocol: HTTPS REST API
    """

    BASE_URL = "https://api.moxie.com/v1"
    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 0.5  # seconds between requests

    def __init__(self, api_key: str):
        """Initialize Moxie client"""
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
        json_data: Optional[Dict] = None,
        data: Optional[bytes] = None
    ) -> Dict[str, Any]:
        """Make API request with retry logic and error handling"""
        await self._rate_limit()

        headers = {
            "X-API-Key": self.api_key,
            "Accept": "application/json"
        }

        if json_data:
            headers["Content-Type"] = "application/json"
        elif data:
            headers["Content-Type"] = "multipart/form-data"

        url = f"{self.BASE_URL}{endpoint}"

        for attempt in range(self.MAX_RETRIES):
            try:
                async with self.session.request(
                    method,
                    url,
                    params=params,
                    json=json_data,
                    data=data,
                    headers=headers
                ) as response:
                    if response.status == 204:
                        return {}

                    try:
                        data = await response.json()
                    except:
                        data = {}

                    if response.status in (200, 201, 204):
                        return data
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
                        raise Exception(f"Client error: {data.get('message', 'Unknown error')}")
                    else:
                        raise Exception(f"Server error: {response.status} - {data}")

            except aiohttp.ClientError as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise Exception(f"Request failed after {self.MAX_RETRIES} attempts: {str(e)}")
                await asyncio.sleep(2 ** attempt)

    # ==================== Client Operations ====================

    async def create_client(self, client: Client) -> Client:
        """Create a new client (Create Client)"""
        client_data = {
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "company": client.company,
            "address": client.address,
            "notes": client.notes,
            "status": client.status
        }

        client_data = {k: v for k, v in client_data.items() if v is not None}

        response = await self._request("POST", "/clients", json_data=client_data)
        return Client(**response.get("data", {}))

    async def search_client(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Client]:
        """Search clients (Search Client)"""
        params = {"limit": limit}

        if query:
            params["query"] = query
        if status:
            params["status"] = status

        response = await self._request("GET", "/clients", params=params)
        clients_data = response.get("data", [])
        return [Client(**c) for c in clients_data]

    async def search_client_invoices(
        self,
        client_id: str,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Invoice]:
        """Search client invoices (Search Client Invoices)"""
        params = {"limit": limit}

        if status:
            params["status"] = status

        response = await self._request("GET", f"/clients/{client_id}/invoices", params=params)
        invoices_data = response.get("data", [])
        return [Invoice(**i) for i in invoices_data]

    # ==================== Contact Operations ====================

    async def create_contact(self, contact: Contact) -> Contact:
        """Create a new contact (Create Contact)"""
        contact_data = {
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "email": contact.email,
            "phone": contact.phone,
            "job_title": contact.job_title,
            "client_id": contact.client_id
        }

        contact_data = {k: v for k, v in contact_data.items() if v is not None}

        response = await self._request("POST", "/contacts", json_data=contact_data)
        return Contact(**response.get("data", {}))

    async def search_contact(
        self,
        query: Optional[str] = None,
        client_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Contact]:
        """Search contacts (Search Contact)"""
        params = {"limit": limit}

        if query:
            params["query"] = query
        if client_id:
            params["client_id"] = client_id

        response = await self._request("GET", "/contacts", params=params)
        contacts_data = response.get("data", [])
        return [Contact(**c) for c in contacts_data]

    # ==================== Project Operations ====================

    async def create_project(self, project: Project) -> Project:
        """Create a new project (Create Project)"""
        project_data = {
            "name": project.name,
            "description": project.description,
            "client_id": project.client_id,
            "status": project.status,
            "start_date": project.start_date,
            "due_date": project.due_date,
            "budget": project.budget
        }

        project_data = {k: v for k, v in project_data.items() if v is not None}

        response = await self._request("POST", "/projects", json_data=project_data)
        return Project(**response.get("data", {}))

    async def search_projects(
        self,
        query: Optional[str] = None,
        client_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Project]:
        """Search projects (Search Projects)"""
        params = {"limit": limit}

        if query:
            params["query"] = query
        if client_id:
            params["client_id"] = client_id
        if status:
            params["status"] = status

        response = await self._request("GET", "/projects", params=params)
        projects_data = response.get("data", [])
        return [Project(**p) for p in projects_data]

    # ==================== Task Operations ====================

    async def create_task(self, task: Task) -> Task:
        """Create a new task (Create Task)"""
        task_data = {
            "title": task.title,
            "description": task.description,
            "project_id": task.project_id,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date,
            "assignee_id": task.assignee_id
        }

        task_data = {k: v for k, v in task_data.items() if v is not None}

        response = await self._request("POST", "/tasks", json_data=task_data)
        return Task(**response.get("data", {}))

    # ==================== Ticket Operations ====================

    async def create_ticket(self, ticket: Ticket) -> Ticket:
        """Create a new ticket (Create Ticket)"""
        ticket_data = {
            "title": ticket.title,
            "description": ticket.description,
            "client_id": ticket.client_id,
            "status": ticket.status,
            "priority": ticket.priority
        }

        ticket_data = {k: v for k, v in ticket_data.items() if v is not None}

        response = await self._request("POST", "/tickets", json_data=ticket_data)
        return Ticket(**response.get("data", {}))

    async def add_comment_to_ticket(
        self,
        ticket_id: str,
        comment: str
    ) -> bool:
        """Add comment to ticket (Add Comment to Ticket)"""
        await self._request(
            "POST",
            f"/tickets/{ticket_id}/comments",
            json_data={"comment": comment}
        )
        return True

    async def approve_deliverable(self, deliverable_id: str) -> bool:
        """Approve deliverable (Approve Deliverable)"""
        await self._request("POST", f"/deliverables/{deliverable_id}/approve")
        return True

    # ==================== Invoice Operations ====================

    async def create_invoice(self, invoice: Invoice) -> Invoice:
        """Create a new invoice (Create Invoice)"""
        invoice_data = {
            "client_id": invoice.client_id,
            "number": invoice.number,
            "due_date": invoice.due_date,
            "total": invoice.total,
            "currency": invoice.currency,
            "status": invoice.status,
            "line_items": invoice.line_items
        }

        invoice_data = {k: v for k, v in invoice_data.items() if v is not None}

        response = await self._request("POST", "/invoices", json_data=invoice_data)
        return Invoice(**response.get("data", {}))

    # ==================== Expense Operations ====================

    async def create_expense(self, expense: Expense) -> Expense:
        """Create a new expense (Create Expense)"""
        expense_data = {
            "project_id": expense.project_id,
            "amount": expense.amount,
            "currency": expense.currency,
            "description": expense.description,
            "date": expense.date,
            "category": expense.category
        }

        expense_data = {k: v for k, v in expense_data.items() if v is not None}

        response = await self._request("POST", "/expenses", json_data=expense_data)
        return Expense(**response.get("data", {}))

    # ==================== Calendar Operations ====================

    async def create_or_update_calendar_event(self, event: CalendarEvent) -> CalendarEvent:
        """Create or update calendar event (Create or Update Calendar Event)"""
        event_data = {
            "title": event.title,
            "description": event.description,
            "start": event.start,
            "end": event.end,
            "all_day": event.all_day,
            "client_id": event.client_id
        }

        event_data = {k: v for k, v in event_data.items() if v is not None}

        if event.id:
            response = await self._request("PUT", f"/calendar/events/{event.id}", json_data=event_data)
        else:
            response = await self._request("POST", "/calendar/events", json_data=event_data)

        return CalendarEvent(**response.get("data", {}))

    # ==================== Form Operations ====================

    async def create_form_submission(
        self,
        form_id: str,
        submission_data: Dict[str, Any]
    ) -> bool:
        """Create form submission (Create Form Submission)"""
        await self._request(
            "POST",
            f"/forms/{form_id}/submissions",
            json_data=submission_data
        )
        return True

    # ==================== File Operations ====================

    async def upload_file(
        self,
        file_path: str,
        project_id: Optional[str] = None,
        client_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload file (Upload File)"""
        with open(file_path, 'rb') as f:
            file_data = f.read()

        data = {"file": file_data}

        if project_id:
            data["project_id"] = project_id
        if client_id:
            data["client_id"] = client_id

        response = await self._request("POST", "/files/upload", data=data)
        return response


# ==================== Example Usage ====================

async def main():
    """Example usage of Moxie client"""

    api_key = "your_moxie_api_key"

    async with MoxieClient(api_key=api_key) as client:
        # Create client
        client = Client(
            name="Example Corp",
            email="billing@example.com",
            company="Example Corp"
        )
        created_client = await client.create_client(client)
        print(f"Created client: {created_client.name}")

        # Create project
        project = Project(
            name="Website Redesign",
            client_id=created_client.id,
            status="active"
        )
        created_project = await client.create_project(project)
        print(f"Created project: {created_project.name}")

        # Create task
        task = Task(
            title="Design homepage",
            project_id=created_project.id,
            priority="high"
        )
        created_task = await client.create_task(task)
        print(f"Created task: {created_task.title}")


if __name__ == "__main__":
    asyncio.run(main())