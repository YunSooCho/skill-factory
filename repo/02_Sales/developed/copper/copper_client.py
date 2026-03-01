"""
Copper API Client

Complete client for Copper CRM (formerly ProsperWorks).
Supports companies, people, and tasks with Google Workspace integration.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import json
import base64


class CopperAPIError(Exception):
    """Base exception for Copper API errors"""

    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class CopperRateLimitError(CopperAPIError):
    """Raised when rate limit is exceeded"""


@dataclass
class Company:
    company_id: str
    name: str
    website: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Person:
    person_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company_id: Optional[str] = None
    title: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    task_id: str
    name: str
    status: str
    priority: Optional[str] = None
    due_date: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class CopperClient:
    """Copper CRM API Client."""

    BASE_URL = "https://api.copper.com/developer_api/v1"

    def __init__(
        self,
        api_key: str,
        email: str,
        base_url: Optional[str] = None,
        max_requests_per_minute: int = 100,
        timeout: int = 30
    ):
        self.api_key = api_key
        self.email = email
        self.base_url = base_url or self.BASE_URL
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None
        self.max_requests_per_minute = max_requests_per_minute
        self._request_times: List[float] = []

    def _get_auth_header(self):
        credentials = base64.b64encode(f"{self.email}:{self.api_key}".encode()).decode()
        return f"Basic {credentials}"

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _check_rate_limit(self):
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
        await self._check_rate_limit()
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": self._get_auth_header(),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if not self.session:
            raise RuntimeError("Client must be used as async context manager")

        try:
            async with self.session.request(
                method, url, json=data, params=params, headers=headers
            ) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = await response.text()

                if response.status == 429:
                    raise CopperRateLimitError("Rate limit exceeded", status_code=429)

                if response.status >= 400:
                    error_msg = response_data.get("error", str(response_data))
                    raise CopperAPIError(error_msg, status_code=response.status)

                return response_data if isinstance(response_data, dict) else {}

        except aiohttp.ClientError as e:
            raise CopperAPIError(f"Network error: {str(e)}")

    async def create_company(self, company_data: Dict[str, Any]) -> Company:
        data = await self._request("POST", "/companies", data=company_data)
        return Company(
            company_id=str(data.get("id", "")),
            name=data.get("name", ""),
            website=data.get("website"),
            created_at=data.get("date_created"),
            updated_at=data.get("date_modified"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "website", "date_created", "date_modified"]}
        )

    async def get_company(self, company_id: str) -> Company:
        data = await self._request("GET", f"/companies/{company_id}")
        return Company(
            company_id=str(data.get("id", company_id)),
            name=data.get("name", ""),
            website=data.get("website"),
            created_at=data.get("date_created"),
            updated_at=data.get("date_modified"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "website", "date_created", "date_modified"]}
        )

    async def update_company(self, company_id: str, update_data: Dict[str, Any]) -> Company:
        data = await self._request("PUT", f"/companies/{company_id}", data=update_data)
        return Company(
            company_id=company_id,
            name=data.get("name", ""),
            website=data.get("website"),
            created_at=data.get("date_created"),
            updated_at=data.get("date_modified"),
            additional_data={k: v for k, v in data.items() if k not in ["name", "website", "date_created", "date_modified"]}
        )

    async def search_companies(
        self,
        query: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Company]:
        params = {"page_size": limit, "page_number": offset // limit + 1}
        if query:
            params["query"] = query

        data = await self._request("GET", "/companies/search", params=params)
        results = data.get("results", [])

        return [Company(
            company_id=str(r.get("id", "")),
            name=r.get("name", ""),
            website=r.get("website"),
            created_at=r.get("date_created"),
            updated_at=r.get("date_modified"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "name", "website", "date_created", "date_modified"]}
        ) for r in results]

    async def create_person(self, person_data: Dict[str, Any]) -> Person:
        data = await self._request("POST", "/people", data=person_data)
        return Person(
            person_id=str(data.get("id", "")),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            company_id=str(data.get("company_id", "")) if data.get("company_id") else None,
            title=data.get("title"),
            created_at=data.get("date_created"),
            updated_at=data.get("date_modified"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "email", "phone", "company_id", "title", "date_created", "date_modified"]}
        )

    async def get_person(self, person_id: str) -> Person:
        data = await self._request("GET", f"/people/{person_id}")
        return Person(
            person_id=str(data.get("id", person_id)),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            company_id=str(data.get("company_id", "")) if data.get("company_id") else None,
            title=data.get("title"),
            created_at=data.get("date_created"),
            updated_at=data.get("date_modified"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "email", "phone", "company_id", "title", "date_created", "date_modified"]}
        )

    async def update_person(self, person_id: str, update_data: Dict[str, Any]) -> Person:
        data = await self._request("PUT", f"/people/{person_id}", data=update_data)
        return Person(
            person_id=person_id,
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            company_id=str(data.get("company_id", "")) if data.get("company_id") else None,
            title=data.get("title"),
            created_at=data.get("date_created"),
            updated_at=data.get("date_modified"),
            additional_data={k: v for k, v in data.items() if k not in ["name", "email", "phone", "company_id", "title", "date_created", "date_modified"]}
        )

    async def search_people(
        self,
        query: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Person]:
        params = {"page_size": limit, "page_number": offset // limit + 1}
        if query:
            params["query"] = query

        data = await self._request("GET", "/people/search", params=params)
        results = data.get("results", [])

        return [Person(
            person_id=str(r.get("id", "")),
            name=r.get("name", ""),
            email=r.get("email"),
            phone=r.get("phone"),
            company_id=str(r.get("company_id", "")) if r.get("company_id") else None,
            title=r.get("title"),
            created_at=r.get("date_created"),
            updated_at=r.get("date_modified"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "name", "email", "phone", "company_id", "title", "date_created", "date_modified"]}
        ) for r in results]

    async def create_task(self, task_data: Dict[str, Any]) -> Task:
        data = await self._request("POST", "/tasks", data=task_data)
        return Task(
            task_id=str(data.get("id", "")),
            name=data.get("name", ""),
            status=data.get("status", ""),
            priority=data.get("priority"),
            due_date=data.get("due_date"),
            created_at=data.get("date_created"),
            updated_at=data.get("date_modified"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "status", "priority", "due_date", "date_created", "date_modified"]}
        )

    async def get_task(self, task_id: str) -> Task:
        data = await self._request("GET", f"/tasks/{task_id}")
        return Task(
            task_id=str(data.get("id", task_id)),
            name=data.get("name", ""),
            status=data.get("status", ""),
            priority=data.get("priority"),
            due_date=data.get("due_date"),
            created_at=data.get("date_created"),
            updated_at=data.get("date_modified"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "status", "priority", "due_date", "date_created", "date_modified"]}
        )

    async def update_task(self, task_id: str, update_data: Dict[str, Any]) -> Task:
        data = await self._request("PUT", f"/tasks/{task_id}", data=update_data)
        return Task(
            task_id=task_id,
            name=data.get("name", ""),
            status=data.get("status", ""),
            priority=data.get("priority"),
            due_date=data.get("due_date"),
            created_at=data.get("date_created"),
            updated_at=data.get("date_modified"),
            additional_data={k: v for k, v in data.items() if k not in ["name", "status", "priority", "due_date", "date_created", "date_modified"]}
        )

    async def search_tasks(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Task]:
        params = {"page_size": limit, "page_number": offset // limit + 1}
        if status:
            params["status"] = status

        data = await self._request("GET", "/tasks", params=params)
        results = data.get("results", [])

        return [Task(
            task_id=str(r.get("id", "")),
            name=r.get("name", ""),
            status=r.get("status", ""),
            priority=r.get("priority"),
            due_date=r.get("due_date"),
            created_at=r.get("date_created"),
            updated_at=r.get("date_modified"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "name", "status", "priority", "due_date", "date_created", "date_modified"]}
        ) for r in results]

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


async def main():
    async with CopperClient(api_key="your_api_key", email="your_email@example.com") as client:
        company = await client.create_company({
            "name": "Acme Corp",
            "website": "https://acme.com"
        })
        print(f"Created company: {company.company_id}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())