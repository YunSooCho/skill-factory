"""
Servicem API - Service Management Client

Supports:
- Clients management
- Jobs management
- Tasks management
"""

import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import os


@dataclass
class Client:
    """Client information"""
    client_id: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    status: str
    created_at: str
    updated_at: str


@dataclass
class Job:
    """Job information"""
    job_id: str
    client_id: str
    title: str
    description: Optional[str]
    status: str
    priority: Optional[str]
    scheduled_date: Optional[str]
    completed_date: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Task:
    """Task information"""
    task_id: str
    job_id: Optional[str]
    client_id: Optional[str]
    title: str
    description: Optional[str]
    status: str
    priority: Optional[str]
    due_date: Optional[str]
    completed_date: Optional[str]
    created_at: str
    updated_at: str


class ServicemClient:
    """
    Servicem API client for service management.

    API Documentation: https://lp.yoom.fun/apps/servicem
    Requires API key from Yoom integration.
    """

    BASE_URL = "https://api.servicem.com/v1"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize Servicem client.

        Args:
            api_key: API key (defaults to YOOM_SERVICEM_API_KEY env var)
            base_url: Custom base URL for testing
        """
        self.api_key = api_key or os.environ.get("YOOM_SERVICEM_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set YOOM_SERVICEM_API_KEY environment variable")

        self.base_url = base_url or self.BASE_URL
        self.session = None
        self._rate_limit_delay = 0.3  # 300ms between requests

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request with rate limiting"""
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async with statement")

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        headers["Content-Type"] = "application/json"

        # Rate limiting
        await asyncio.sleep(self._rate_limit_delay)

        url = f"{self.base_url}{endpoint}"

        async with self.session.request(method, url, headers=headers, **kwargs) as response:
            if response.status == 429:
                retry_after = int(response.headers.get("Retry-After", 2))
                await asyncio.sleep(retry_after)
                return await self._request(method, endpoint, **kwargs)

            if response.status >= 400:
                error_text = await response.text()
                raise Exception(f"API error {response.status}: {error_text}")

            if response.status == 204:
                return {}

            return await response.json()

    # ==================== Client Operations ====================

    async def create_client(self, client_data: Dict[str, Any]) -> Client:
        """Create a new client"""
        data = await self._request("POST", "/clients", json=client_data)

        return Client(
            client_id=data.get("client_id", ""),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            status=data.get("status", "active"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def get_client(self, client_id: str) -> Client:
        """Get client by ID"""
        data = await self._request("GET", f"/clients/{client_id}")

        return Client(
            client_id=data.get("client_id", client_id),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            status=data.get("status", "active"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def update_client(self, client_id: str, update_data: Dict[str, Any]) -> Client:
        """Update client"""
        data = await self._request("PATCH", f"/clients/{client_id}", json=update_data)

        return Client(
            client_id=data.get("client_id", client_id),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            status=data.get("status", "active"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def delete_client(self, client_id: str) -> Dict[str, Any]:
        """Delete client"""
        return await self._request("DELETE", f"/clients/{client_id}")

    async def list_clients(self, **filters) -> List[Client]:
        """List clients with optional filters"""
        data = await self._request("GET", "/clients", params=filters)

        clients = []
        for item in data.get("clients", []):
            clients.append(Client(
                client_id=item.get("client_id", ""),
                name=item.get("name", ""),
                email=item.get("email"),
                phone=item.get("phone"),
                address=item.get("address"),
                status=item.get("status", "active"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return clients

    # ==================== Job Operations ====================

    async def create_job(self, job_data: Dict[str, Any]) -> Job:
        """Create a new job"""
        data = await self._request("POST", "/jobs", json=job_data)

        return Job(
            job_id=data.get("job_id", ""),
            client_id=data.get("client_id", ""),
            title=data.get("title", ""),
            description=data.get("description"),
            status=data.get("status", "pending"),
            priority=data.get("priority"),
            scheduled_date=data.get("scheduled_date"),
            completed_date=data.get("completed_date"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def get_job(self, job_id: str) -> Job:
        """Get job by ID"""
        data = await self._request("GET", f"/jobs/{job_id}")

        return Job(
            job_id=data.get("job_id", job_id),
            client_id=data.get("client_id", ""),
            title=data.get("title", ""),
            description=data.get("description"),
            status=data.get("status", "pending"),
            priority=data.get("priority"),
            scheduled_date=data.get("scheduled_date"),
            completed_date=data.get("completed_date"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def update_job(self, job_id: str, update_data: Dict[str, Any]) -> Job:
        """Update job"""
        data = await self._request("PATCH", f"/jobs/{job_id}", json=update_data)

        return Job(
            job_id=data.get("job_id", job_id),
            client_id=data.get("client_id", ""),
            title=data.get("title", ""),
            description=data.get("description"),
            status=data.get("status", "pending"),
            priority=data.get("priority"),
            scheduled_date=data.get("scheduled_date"),
            completed_date=data.get("completed_date"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def delete_job(self, job_id: str) -> Dict[str, Any]:
        """Delete job"""
        return await self._request("DELETE", f"/jobs/{job_id}")

    async def list_jobs(self, **filters) -> List[Job]:
        """List jobs with optional filters"""
        data = await self._request("GET", "/jobs", params=filters)

        jobs = []
        for item in data.get("jobs", []):
            jobs.append(Job(
                job_id=item.get("job_id", ""),
                client_id=item.get("client_id", ""),
                title=item.get("title", ""),
                description=item.get("description"),
                status=item.get("status", "pending"),
                priority=item.get("priority"),
                scheduled_date=item.get("scheduled_date"),
                completed_date=item.get("completed_date"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return jobs

    # ==================== Task Operations ====================

    async def create_task(self, task_data: Dict[str, Any]) -> Task:
        """Create a new task"""
        data = await self._request("POST", "/tasks", json=task_data)

        return Task(
            task_id=data.get("task_id", ""),
            job_id=data.get("job_id"),
            client_id=data.get("client_id"),
            title=data.get("title", ""),
            description=data.get("description"),
            status=data.get("status", "pending"),
            priority=data.get("priority"),
            due_date=data.get("due_date"),
            completed_date=data.get("completed_date"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def get_task(self, task_id: str) -> Task:
        """Get task by ID"""
        data = await self._request("GET", f"/tasks/{task_id}")

        return Task(
            task_id=data.get("task_id", task_id),
            job_id=data.get("job_id"),
            client_id=data.get("client_id"),
            title=data.get("title", ""),
            description=data.get("description"),
            status=data.get("status", "pending"),
            priority=data.get("priority"),
            due_date=data.get("due_date"),
            completed_date=data.get("completed_date"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def update_task(self, task_id: str, update_data: Dict[str, Any]) -> Task:
        """Update task"""
        data = await self._request("PATCH", f"/tasks/{task_id}", json=update_data)

        return Task(
            task_id=data.get("task_id", task_id),
            job_id=data.get("job_id"),
            client_id=data.get("client_id"),
            title=data.get("title", ""),
            description=data.get("description"),
            status=data.get("status", "pending"),
            priority=data.get("priority"),
            due_date=data.get("due_date"),
            completed_date=data.get("completed_date"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete task"""
        return await self._request("DELETE", f"/tasks/{task_id}")

    async def list_tasks(self, **filters) -> List[Task]:
        """List tasks with optional filters"""
        data = await self._request("GET", "/tasks", params=filters)

        tasks = []
        for item in data.get("tasks", []):
            tasks.append(Task(
                task_id=item.get("task_id", ""),
                job_id=item.get("job_id"),
                client_id=item.get("client_id"),
                title=item.get("title", ""),
                description=item.get("description"),
                status=item.get("status", "pending"),
                priority=item.get("priority"),
                due_date=item.get("due_date"),
                completed_date=item.get("completed_date"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return tasks

    # ==================== Webhook Handlers ====================

    async def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming webhook events"""
        event_type = payload.get("event_type")

        if event_type == "job_queued":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "new_job":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "job_completed":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "new_client":
            return {"status": "acknowledged", "event_type": event_type}
        else:
            return {"status": "acknowledged", "event_type": event_type}