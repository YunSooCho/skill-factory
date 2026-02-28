"""
Assignar API Client

Construction management platform for field operations including:
- Workers, Crews, Scheduling
- Projects, Tasks
- Equipment Management
- Timesheets, Compliance

API Actions (estimated 12-15):
1. Create Worker
2. Update Worker
3. Get Worker
4. Create Crew
5. Schedule Worker
6. Create Project
7. Update Project
8. Get Project
9. Create Task
10. Get Timesheets
11. Submit Timesheet
12. Get Compliance Status

Triggers (estimated 5-6):
- Worker Check-in/Check-out
- Task Completed
- Timesheet Submitted
- Project Status Changed
- Compliance Alert

Authentication: OAuth 2.0 (Client Credentials)
Base URL: https://api.assignar-stage.com/v2 (production differs)
Documentation: https://developer.assignar.com/
Rate Limiting: 1000 requests per hour
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class Worker:
    """Worker model"""
    worker_id: str
    first_name: str
    last_name: str
    email: str
    phone: str = ""
    status: str = ""
    is_active: bool = True
    created_at: Optional[str] = None


@dataclass
class Crew:
    """Crew model"""
    crew_id: str
    name: str
    description: str = ""
    supervisor_id: Optional[str] = None
    members: List[str] = field(default_factory=list)


@dataclass
class Project:
    """Project model"""
    project_id: str
    name: str
    code: str = ""
    status: str = ""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[Dict[str, str]] = None
    client_id: Optional[str] = None


@dataclass
class Task:
    """Task model"""
    task_id: str
    title: str
    description: str = ""
    status: str = ""
    priority: str = "Medium"
    project_id: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[str] = None


@dataclass
class Timesheet:
    """Timesheet model"""
    timesheet_id: str
    worker_id: str
    project_id: str
    date: str
    hours: float
    notes: str = ""
    status: str = "draft"


@dataclass
class Compliance:
    """Compliance status model"""
    worker_id: str
    is_compliant: bool
    certifications: List[Dict[str, Any]] = field(default_factory=list)
    expiry_dates: List[Dict[str, str]] = field(default_factory=list)


class AssignarClient:
    """
    Assignar API client for construction management.

    Supports: Workers, Crews, Projects, Tasks, Timesheets, Compliance
    Rate limit: 1000 requests/hour
    """

    BASE_URL = "https://api.assignar.com/v2"
    RATE_LIMIT = 1000  # requests per hour

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize Assignar client.

        Args:
            client_id: OAuth 2.0 client ID
            client_secret: OAuth 2.0 client secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = None
        self._access_token = None
        self._token_expiry = None
        self._request_count = 0
        self._request_window_start = datetime.now()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        await self._get_access_token()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _get_access_token(self):
        """Get OAuth 2.0 access token"""
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        url = f"{self.BASE_URL}/oauth/token"
        async with self.session.post(url, json=data) as response:
            result = await response.json()

            if response.status != 200:
                raise Exception(f"Failed to get access token: {result}")

            self._access_token = result.get("access_token")
            expires_in = result.get("expires_in", 3600)
            self._token_expiry = asyncio.get_event_loop().time() + expires_in

    async def _check_token(self):
        """Check if token needs refresh"""
        if not self._access_token or not self._token_expiry:
            await self._get_access_token()
        elif asyncio.get_event_loop().time() >= self._token_expiry - 60:
            await self._get_access_token()

    async def _check_rate_limit(self):
        """Check and enforce rate limiting"""
        now = datetime.now()
        time_window = (now - self._request_window_start).total_seconds()

        if time_window >= 3600:
            self._request_count = 0
            self._request_window_start = now

        if self._request_count >= self.RATE_LIMIT:
            wait_time = 3600 - int(time_window)
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
        """Make API request with authentication"""
        await self._check_token()
        await self._check_rate_limit()

        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json"
        }

        async with self.session.request(
            method,
            url,
            headers=headers,
            json=data,
            params=params
        ) as response:
            result = await response.json()

            if response.status not in [200, 201]:
                raise Exception(
                    f"Assignar API error: {response.status} - {result}"
                )

            return result

    # ==================== Worker Operations ====================

    async def create_worker(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str = ""
    ) -> Worker:
        """Create a new worker"""
        data = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": phone
        }
        response = await self._make_request("POST", "/workers", data=data)
        worker_data = response.get("data", response)
        return Worker(
            worker_id=worker_data.get("id", ""),
            first_name=worker_data.get("firstName", first_name),
            last_name=worker_data.get("lastName", last_name),
            email=worker_data.get("email", email),
            phone=worker_data.get("phone", phone),
            status=worker_data.get("status", ""),
            is_active=worker_data.get("isActive", True),
            created_at=worker_data.get("createdAt")
        )

    async def get_worker(self, worker_id: str) -> Worker:
        """Get worker by ID"""
        response = await self._make_request("GET", f"/workers/{worker_id}")
        worker_data = response.get("data", response)
        return Worker(
            worker_id=worker_data.get("id", ""),
            first_name=worker_data.get("firstName", ""),
            last_name=worker_data.get("lastName", ""),
            email=worker_data.get("email", ""),
            phone=worker_data.get("phone", ""),
            status=worker_data.get("status", ""),
            is_active=worker_data.get("isActive", True),
            created_at=worker_data.get("createdAt")
        )

    async def update_worker(
        self,
        worker_id: str,
        **fields
    ) -> Worker:
        """Update a worker"""
        response = await self._make_request(
            "PUT",
            f"/workers/{worker_id}",
            data=fields
        )
        worker_data = response.get("data", response)
        return Worker(
            worker_id=worker_data.get("id", ""),
            first_name=worker_data.get("firstName", ""),
            last_name=worker_data.get("lastName", ""),
            email=worker_data.get("email", ""),
            phone=worker_data.get("phone", ""),
            status=worker_data.get("status", "")
        )

    # ==================== Crew Operations ====================

    async def create_crew(
        self,
        name: str,
        description: str = "",
        supervisor_id: Optional[str] = None
    ) -> Crew:
        """Create a new crew"""
        data = {
            "name": name,
            "description": description
        }
        if supervisor_id:
            data["supervisorId"] = supervisor_id

        response = await self._make_request("POST", "/crews", data=data)
        crew_data = response.get("data", response)
        return Crew(
            crew_id=crew_data.get("id", ""),
            name=crew_data.get("name", name),
            description=crew_data.get("description", description),
            supervisor_id=crew_data.get("supervisorId"),
            members=crew_data.get("members", [])
        )

    async def schedule_worker(
        self,
        worker_id: str,
        crew_id: str,
        project_id: str,
        date: str
    ) -> bool:
        """Schedule a worker to a crew/project"""
        data = {
            "workerId": worker_id,
            "crewId": crew_id,
            "projectId": project_id,
            "date": date
        }
        await self._make_request("POST", "/schedules", data=data)
        return True

    # ==================== Project Operations ====================

    async def create_project(
        self,
        name: str,
        code: str = "",
        **fields
    ) -> Project:
        """Create a new project"""
        data = {
            "name": name,
            "code": code,
            **fields
        }
        response = await self._make_request("POST", "/projects", data=data)
        project_data = response.get("data", response)
        return Project(
            project_id=project_data.get("id", ""),
            name=project_data.get("name", name),
            code=project_data.get("code", code),
            status=project_data.get("status", ""),
            start_date=project_data.get("startDate"),
            end_date=project_data.get("endDate"),
            location=project_data.get("location"),
            client_id=project_data.get("clientId")
        )

    async def get_project(self, project_id: str) -> Project:
        """Get project by ID"""
        response = await self._make_request("GET", f"/projects/{project_id}")
        project_data = response.get("data", response)
        return Project(
            project_id=project_data.get("id", ""),
            name=project_data.get("name", ""),
            code=project_data.get("code", ""),
            status=project_data.get("status", ""),
            start_date=project_data.get("startDate"),
            end_date=project_data.get("endDate"),
            location=project_data.get("location"),
            client_id=project_data.get("clientId")
        )

    async def update_project(
        self,
        project_id: str,
        **fields
    ) -> Project:
        """Update a project"""
        response = await self._make_request(
            "PUT",
            f"/projects/{project_id}",
            data=fields
        )
        product_data = response.get("data", response)
        return Project(
            project_id=product_data.get("id", ""),
            name=product_data.get("name", ""),
            code=product_data.get("code", ""),
            status=product_data.get("status", "")
        )

    # ==================== Task Operations ====================

    async def create_task(
        self,
        title: str,
        project_id: str,
        **fields
    ) -> Task:
        """Create a task"""
        data = {
            "title": title,
            "projectId": project_id,
            **fields
        }
        response = await self._make_request("POST", "/tasks", data=data)
        task_data = response.get("data", response)
        return Task(
            task_id=task_data.get("id", ""),
            title=task_data.get("title", title),
            description=task_data.get("description", ""),
            status=task_data.get("status", ""),
            priority=task_data.get("priority", "Medium"),
            project_id=task_data.get("projectId"),
            assigned_to=task_data.get("assignedTo"),
            due_date=task_data.get("dueDate")
        )

    # ==================== Timesheet Operations ====================

    async def get_timesheets(
        self,
        project_id: Optional[str] = None,
        worker_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> List[Timesheet]:
        """Get timesheets with optional filters"""
        params = {}
        if project_id:
            params["projectId"] = project_id
        if worker_id:
            params["workerId"] = worker_id
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to

        response = await self._make_request("GET", "/timesheets", params=params)
        timesheets_data = response.get("data", [])
        return [
            Timesheet(
                timesheet_id=ts.get("id", ""),
                worker_id=ts.get("workerId", ""),
                project_id=ts.get("projectId", ""),
                date=ts.get("date", ""),
                hours=ts.get("hours", 0.0),
                notes=ts.get("notes", ""),
                status=ts.get("status", "draft")
            )
            for ts in timesheets_data
        ]

    async def submit_timesheet(
        self,
        timesheet_id: str
    ) -> Timesheet:
        """Submit a timesheet for approval"""
        response = await self._make_request(
            "POST",
            f"/timesheets/{timesheet_id}/submit"
        )
        ts_data = response.get("data", response)
        return Timesheet(
            timesheet_id=ts_data.get("id", ""),
            worker_id=ts_data.get("workerId", ""),
            project_id=ts_data.get("projectId", ""),
            date=ts_data.get("date", ""),
            hours=ts_data.get("hours", 0.0),
            status=ts_data.get("status", "submitted")
        )

    # ==================== Compliance Operations ====================

    async def get_compliance_status(self, worker_id: str) -> Compliance:
        """Get worker compliance status"""
        response = await self._make_request("GET", f"/workers/{worker_id}/compliance")
        compliance_data = response.get("data", response)
        return Compliance(
            worker_id=worker_id,
            is_compliant=compliance_data.get("isCompliant", False),
            certifications=compliance_data.get("certifications", []),
            expiry_dates=compliance_data.get("expiryDates", [])
        )

    # ==================== Webhook Handling ====================

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook events from Assignar"""
        event_type = webhook_data.get("event_type", "unknown")
        resource_type = webhook_data.get("resource_type", "unknown")
        resource_id = webhook_data.get("resource_id")

        return {
            "event_type": event_type,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "raw_data": webhook_data
        }


async def main():
    """Example usage"""
    client_id = "your_client_id"
    client_secret = "your_client_secret"

    async with AssignarClient(client_id, client_secret) as client:
        # Create a worker
        worker = await client.create_worker(
            first_name="John",
            last_name="Smith",
            email="john.smith@example.com"
        )
        print(f"Created worker: {worker.worker_id}")

        # Get compliance status
        compliance = await client.get_compliance_status(worker.worker_id)
        print(f"Worker compliant: {compliance.is_compliant}")

if __name__ == "__main__":
    asyncio.run(main())