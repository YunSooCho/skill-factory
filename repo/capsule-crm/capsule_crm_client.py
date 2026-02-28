"""
Capsule CRM API Client

Relationship management platform for managing:
- Parties (people and organizations)
- Opportunities
- Projects
- Tasks

API Actions (21):
Full CRUD for parties, opportunities, projects, tasks
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Party:
    id: Optional[int] = None
    type: Optional[str] = None
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_addresses: List[Dict[str, str]] = None
    phone_numbers: List[Dict[str, str]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        if self.email_addresses is None:
            self.email_addresses = []
        if self.phone_numbers is None:
            self.phone_numbers = []


@dataclass
class Opportunity:
    id: Optional[int] = None
    party_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    milestone_id: Optional[int] = None
    value: Optional[float] = None
    currency: Optional[str] = None
    probability: Optional[int] = None
    expected_close_date: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Project:
    id: Optional[int] = None
    party_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Task:
    id: Optional[int] = None
    party_id: Optional[int] = None
    project_id: Optional[int] = None
    opportunity_id: Optional[int] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None
    completed_at: Optional[str] = None
    created_at: Optional[str] = None


class RateLimiter:
    def __init__(self, calls_per_second: int = 10):
        self.calls_per_second = calls_per_second
        self.tokens = calls_per_second
        self.last_update = datetime.now()

    async def acquire(self):
        now = datetime.now()
        elapsed = (now - self.last_update).total_seconds()
        self.tokens = min(self.calls_per_second, self.tokens + elapsed * self.calls_per_second)
        self.last_update = now
        if self.tokens < 1:
            sleep_time = (1 - self.tokens) / self.calls_per_second
            await asyncio.sleep(sleep_time)
            self.tokens = self.calls_per_second
        else:
            self.tokens -= 1


class CapsuleCRMError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}" if status_code else message)


class CapsuleCRMClient:
    """Capsule CRM API Client"""

    def __init__(self, api_token: str, base_url: str = "https://api.capsulecrm.com/api/v2"):
        self.api_token = api_token
        self.base_url = base_url.rstrip('/')
        self._headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        self._rate_limiter = RateLimiter(calls_per_second=10)

    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        await self._rate_limiter.acquire()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method=method, url=url, headers=self._headers, json=data, params=params) as response:
                    if response.status == 204:
                        return {"status": "success"}
                    if response.status >= 400:
                        try:
                            error_data = await response.json()
                            error_msg = error_data.get("message", "Unknown error")
                        except:
                            error_msg = await response.text()
                        raise CapsuleCRMError(error_msg, response.status)
                    return await response.json()
            except aiohttp.ClientError as e:
                raise CapsuleCRMError(f"Network error: {str(e)}")
            except asyncio.TimeoutError:
                raise CapsuleCRMError("Request timeout")

    # Party methods
    async def create_party(self, data: Dict[str, Any]) -> Party:
        """Create party (person or organization)"""
        data_type = data.get("type", "person")
        if data_type not in ["person", "organization"]:
            raise CapsuleCRMError("Party type must be 'person' or 'organization'")

        if data_type == "person" and not data.get("firstName"):
            raise CapsuleCRMError("Person firstName is required")
        if data_type == "organization" and not data.get("name"):
            raise CapsuleCRMError("Organization name is required")

        response = await self._make_request("POST", "/parties", data={"party": data})
        return Party(**response)

    async def get_party(self, party_id: int) -> Party:
        """Get party by ID"""
        response = await self._make_request("GET", f"/parties/{party_id}")
        return Party(**response)

    async def update_party(self, party_id: int, data: Dict[str, Any]) -> Party:
        """Update party"""
        response = await self._make_request("PUT", f"/parties/{party_id}", data={"party": data})
        return Party(**response)

    async def delete_party(self, party_id: int) -> Dict[str, str]:
        """Delete party"""
        await self._make_request("DELETE", f"/parties/{party_id}")
        return {"status": "deleted", "party_id": str(party_id)}

    async def search_party(self, **params) -> List[Party]:
        """Search parties"""
        response = await self._make_request("GET", "/parties", params=params)
        if "parties" in response:
            return [Party(**item) for item in response["parties"]]
        return []

    # Opportunity methods
    async def create_opportunity(self, data: Dict[str, Any]) -> Opportunity:
        """Create opportunity"""
        if not data.get("name"):
            raise CapsuleCRMError("Opportunity name is required")
        response = await self._make_request("POST", "/opportunities", data={"opportunity": data})
        return Opportunity(**response)

    async def get_opportunity(self, opportunity_id: int) -> Opportunity:
        """Get opportunity by ID"""
        response = await self._make_request("GET", f"/opportunities/{opportunity_id}")
        return Opportunity(**response)

    async def update_opportunity(self, opportunity_id: int, data: Dict[str, Any]) -> Opportunity:
        """Update opportunity"""
        response = await self._make_request("PUT", f"/opportunities/{opportunity_id}", data={"opportunity": data})
        return Opportunity(**response)

    async def delete_opportunity(self, opportunity_id: int) -> Dict[str, str]:
        """Delete opportunity"""
        await self._make_request("DELETE", f"/opportunities/{opportunity_id}")
        return {"status": "deleted", "opportunity_id": str(opportunity_id)}

    async def search_opportunity(self, **params) -> List[Opportunity]:
        """Search opportunities"""
        response = await self._make_request("GET", "/opportunities", params=params)
        if "opportunities" in response:
            return [Opportunity(**item) for item in response["opportunities"]]
        return []

    async def list_opportunities(self, **params) -> List[Opportunity]:
        """List opportunities"""
        return await self.search_opportunity(**params)

    # Project methods
    async def create_project(self, data: Dict[str, Any]) -> Project:
        """Create project"""
        if not data.get("name"):
            raise CapsuleCRMError("Project name is required")
        response = await self._make_request("POST", "/projects", data={"project": data})
        return Project(**response)

    async def get_project(self, project_id: int) -> Project:
        """Get project by ID"""
        response = await self._make_request("GET", f"/projects/{project_id}")
        return Project(**response)

    async def update_project(self, project_id: int, data: Dict[str, Any]) -> Project:
        """Update project"""
        response = await self._make_request("PUT", f"/projects/{project_id}", data={"project": data})
        return Project(**response)

    async def delete_project(self, project_id: int) -> Dict[str, str]:
        """Delete project"""
        await self._make_request("DELETE", f"/projects/{project_id}")
        return {"status": "deleted", "project_id": str(project_id)}

    async def search_project(self, **params) -> List[Project]:
        """Search projects"""
        response = await self._make_request("GET", "/projects", params=params)
        if "projects" in response:
            return [Project(**item) for item in response["projects"]]
        return []

    async def list_project(self, **params) -> List[Project]:
        """List projects"""
        return await self.search_project(**params)

    # Task methods
    async def create_task(self, data: Dict[str, Any]) -> Task:
        """Create task"""
        if not data.get("description"):
            raise CapsuleCRMError("Task description is required")
        response = await self._make_request("POST", "/tasks", data={"task": data})
        return Task(**response)

    async def get_task(self, task_id: int) -> Task:
        """Get task by ID"""
        response = await self._make_request("GET", f"/tasks/{task_id}")
        return Task(**response)

    async def update_task(self, task_id: int, data: Dict[str, Any]) -> Task:
        """Update task"""
        response = await self._make_request("PUT", f"/tasks/{task_id}", data={"task": data})
        return Task(**response)

    async def delete_task(self, task_id: int) -> Dict[str, str]:
        """Delete task"""
        await self._make_request("DELETE", f"/tasks/{task_id}")
        return {"status": "deleted", "task_id": str(task_id)}

    async def list_task(self, **params) -> List[Task]:
        """List tasks"""
        response = await self._make_request("GET", "/tasks", params=params)
        if "tasks" in response:
            return [Task(**item) for item in response["tasks"]]
        return []

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process webhook event"""
        return {
            "event_type": webhook_data.get("event_type", "unknown"),
            "entity_type": webhook_data.get("entity_type", "unknown"),
            "entity_id": webhook_data.get("entity_id"),
            "data": webhook_data
        }