"""
Cloze API Client

Complete client for Cloze - smart inbox and contact management system.
Supports people and companies, projects, communications, and tasks.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import json


class ClozeAPIError(Exception):
    """Base exception for Cloze API errors"""

    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class ClozeRateLimitError(ClozeAPIError):
    """Raised when rate limit is exceeded"""


@dataclass
class Person:
    """Person data model"""
    person_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Company:
    """Company data model"""
    company_id: str
    name: str
    website: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Project:
    """Project data model"""
    project_id: str
    name: str
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class ClozeClient:
    """Cloze API Client for contact and project management."""

    BASE_URL = "https://www.cloze.com/api"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        max_requests_per_minute: int = 100,
        timeout: int = 30
    ):
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
            "Authorization": f"Bearer {self.api_key}",
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
                    raise ClozeRateLimitError("Rate limit exceeded", status_code=429)

                if response.status >= 400:
                    error_msg = response_data.get("error", str(response_data))
                    raise ClozeAPIError(error_msg, status_code=response.status)

                return response_data if isinstance(response_data, dict) else {}

        except aiohttp.ClientError as e:
            raise ClozeAPIError(f"Network error: {str(e)}")

    async def create_or_update_person(self, person_data: Dict[str, Any]) -> Person:
        data = await self._request("POST", "/people", data=person_data)
        return Person(
            person_id=data.get("id", ""),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "email", "phone", "created_at", "updated_at"]}
        )

    async def create_or_update_company(self, company_data: Dict[str, Any]) -> Company:
        data = await self._request("POST", "/companies", data=company_data)
        return Company(
            company_id=data.get("id", ""),
            name=data.get("name", ""),
            website=data.get("website"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "website", "created_at", "updated_at"]}
        )

    async def get_person(self, person_id: str) -> Person:
        data = await self._request("GET", f"/people/{person_id}")
        return Person(
            person_id=data.get("id", person_id),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "email", "phone", "created_at", "updated_at"]}
        )

    async def delete_person(self, person_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/people/{person_id}")

    async def search_people(self, query: str, limit: int = 100) -> List[Person]:
        params = {"query": query, "limit": limit}
        data = await self._request("GET", "/people/search", params=params)
        results = data.get("results", [])

        return [Person(
            person_id=r.get("id", ""),
            name=r.get("name", ""),
            email=r.get("email"),
            phone=r.get("phone"),
            created_at=r.get("created_at"),
            updated_at=r.get("updated_at"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "name", "email", "phone", "created_at", "updated_at"]}
        ) for r in results]

    async def get_company(self, company_id: str) -> Company:
        data = await self._request("GET", f"/companies/{company_id}")
        return Company(
            company_id=data.get("id", company_id),
            name=data.get("name", ""),
            website=data.get("website"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "website", "created_at", "updated_at"]}
        )

    async def delete_company(self, company_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/companies/{company_id}")

    async def search_company(self, query: str, limit: int = 100) -> List[Company]:
        params = {"query": query, "limit": limit}
        data = await self._request("GET", "/companies/search", params=params)
        results = data.get("results", [])

        return [Company(
            company_id=r.get("id", ""),
            name=r.get("name", ""),
            website=r.get("website"),
            created_at=r.get("created_at"),
            updated_at=r.get("updated_at"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "name", "website", "created_at", "updated_at"]}
        ) for r in results]

    async def get_project(self, project_id: str) -> Project:
        data = await self._request("GET", f"/projects/{project_id}")
        return Project(
            project_id=data.get("id", project_id),
            name=data.get("name", ""),
            status=data.get("status", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "status", "created_at", "updated_at"]}
        )

    async def delete_project(self, project_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/projects/{project_id}")

    async def search_project(self, query: str, limit: int = 100) -> List[Project]:
        params = {"query": query, "limit": limit}
        data = await self._request("GET", "/projects/search", params=params)
        results = data.get("results", [])

        return [Project(
            project_id=r.get("id", ""),
            name=r.get("name", ""),
            status=r.get("status", ""),
            created_at=r.get("created_at"),
            updated_at=r.get("updated_at"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "name", "status", "created_at", "updated_at"]}
        ) for r in results]

    async def create_communication_record(self, comm_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/communications", data=comm_data)

    async def create_timeline_content(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/timeline", data=content_data)

    async def create_to_do(self, todo_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/todo", data=todo_data)

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


async def main():
    async with ClozeClient(api_key="your_api_key") as client:
        person = await client.create_or_update_person({
            "name": "John Smith",
            "email": "john@example.com"
        })
        print(f"Created/updated person: {person.person_id}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())