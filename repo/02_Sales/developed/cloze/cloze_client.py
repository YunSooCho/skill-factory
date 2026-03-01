"""
Cloze API Client

Cloze is a relationship management platform.

Supports:
- Get Company
- Create or Update Company
- Search Company
- Delete Company
- Get Person (Get Person)
- Create or Update Person
- Search People
- Delete Person
- Get Project
- Search Project
- Delete Project
- Create To Do
- Create Timeline Content
- Create Communication Record
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Company:
    """Company object"""
    id: str
    name: str
    website: Optional[str]
    description: Optional[str]
    industry: Optional[str]
    employees: Optional[int]
    created_at: str
    updated_at: str


@dataclass
class Person:
    """Person object"""
    id: str
    first_name: str
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    company_id: Optional[str]
    company_name: Optional[str]
    title: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Project:
    """Project object"""
    id: str
    name: str
    description: Optional[str]
    status: str
    start_date: Optional[str]
    end_date: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class ToDo:
    """To Do object"""
    id: str
    description: str
    completed: bool
    due_date: Optional[str]
    created_at: str


@dataclass
class TimelineContent:
    """Timeline Content object"""
    id: str
    content_type: str
    content: str
    person_id: Optional[str]
    company_id: Optional[str]
    created_at: str


class ClozeAPIClient:
    """
    Cloze API client for relationship management.

    Authentication: API Key
    Base URL: https://api.cloze.com
    """

    BASE_URL = "https://api.cloze.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Cloze API client.

        Args:
            api_key: Cloze API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
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
        Make HTTP request to Cloze API.

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
            if response.status == 204:
                return {}

            data = await response.json()

            if response.status not in [200, 201]:
                error_msg = data.get("message", "Unknown error") if isinstance(data, dict) else str(data)
                raise Exception(f"Cloze API error ({response.status}): {error_msg}")

            return data

    # ==================== Companies ====================

    async def create_or_update_company(
        self,
        name: str,
        website: Optional[str] = None,
        description: Optional[str] = None,
        industry: Optional[str] = None,
        employee_count: Optional[int] = None,
        external_id: Optional[str] = None
    ) -> Company:
        """
        Create or update a company.

        Args:
            name: Company name
            website: Company website
            description: Company description
            industry: Industry
            employee_count: Number of employees
            external_id: External ID for deduplication

        Returns:
            Company object

        Raises:
            Exception: If API returns error
        """
        json_data = {"name": name}

        if website:
            json_data["url"] = website
        if description:
            json_data["description"] = description
        if industry:
            json_data["industry"] = industry
        if employee_count:
            json_data["employees"] = employee_count
        if external_id:
            json_data["external_id"] = external_id

        data = await self._request("POST", "/companies", json_data=json_data)

        return self._parse_company(data)

    async def get_company(self, company_id: str) -> Company:
        """
        Get a company by ID.

        Args:
            company_id: Company ID

        Returns:
            Company object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/companies/{company_id}")
        return self._parse_company(data)

    async def search_companies(
        self,
        query: Optional[str] = None,
        industry: Optional[str] = None,
        limit: int = 50
    ) -> List[Company]:
        """
        Search for companies.

        Args:
            query: Search query
            industry: Filter by industry
            limit: Maximum number of results

        Returns:
            List of Company objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit}

        if query:
            params["q"] = query
        if industry:
            params["industry"] = industry

        data = await self._request("GET", "/companies", params=params)

        return [self._parse_company(c) for c in data.get("companies", [])]

    async def delete_company(self, company_id: str) -> bool:
        """
        Delete a company.

        Args:
            company_id: Company ID

        Returns:
            True if deleted successfully

        Raises:
            Exception: If API returns error
        """
        await self._request("DELETE", f"/companies/{company_id}")
        return True

    def _parse_company(self, data: Dict[str, Any]) -> Company:
        """Parse company data"""
        return Company(
            id=data.get("id", ""),
            name=data.get("name", ""),
            website=data.get("url") or data.get("website"),
            description=data.get("description"),
            industry=data.get("industry"),
            employees=data.get("employee_count") or data.get("employees"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== People ====================

    async def create_or_update_person(
        self,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company_id: Optional[str] = None,
        title: Optional[str] = None,
        external_id: Optional[str] = None
    ) -> Person:
        """
        Create or update a person.

        Args:
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number
            company_id: Associated company ID
            title: Job title
            external_id: External ID for deduplication

        Returns:
            Person object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "first_name": first_name,
            "last_name": last_name
        }

        if email:
            json_data["email"] = email
        if phone:
            json_data["phone"] = phone
        if company_id:
            json_data["company_id"] = company_id
        if title:
            json_data["title"] = title
        if external_id:
            json_data["external_id"] = external_id

        data = await self._request("POST", "/people", json_data=json_data)

        return self._parse_person(data)

    async def get_person(self, person_id: str) -> Person:
        """
        Get a person by ID.

        Args:
            person_id: Person ID

        Returns:
            Person object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/people/{person_id}")
        return self._parse_person(data)

    async def search_people(
        self,
        query: Optional[str] = None,
        company_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Person]:
        """
        Search for people.

        Args:
            query: Search query
            company_id: Filter by company ID
            limit: Maximum number of results

        Returns:
            List of Person objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit}

        if query:
            params["q"] = query
        if company_id:
            params["company_id"] = company_id

        data = await self._request("GET", "/people", params=params)

        return [self._parse_person(p) for p in data.get("people", [])]

    async def delete_person(self, person_id: str) -> bool:
        """
        Delete a person.

        Args:
            person_id: Person ID

        Returns:
            True if deleted successfully

        Raises:
            Exception: If API returns error
        """
        await self._request("DELETE", f"/people/{person_id}")
        return True

    def _parse_person(self, data: Dict[str, Any]) -> Person:
        """Parse person data"""
        company = data.get("company", {})
        return Person(
            id=data.get("id", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            company_id=company.get("id") if company else None,
            company_name=company.get("name") if company else None,
            title=data.get("title"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Projects ====================

    async def get_project(self, project_id: str) -> Project:
        """
        Get a project by ID.

        Args:
            project_id: Project ID

        Returns:
            Project object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/projects/{project_id}")
        return self._parse_project(data)

    async def search_projects(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Project]:
        """
        Search for projects.

        Args:
            query: Search query
            status: Filter by status
            limit: Maximum number of results

        Returns:
            List of Project objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit}

        if query:
            params["q"] = query
        if status:
            params["status"] = status

        data = await self._request("GET", "/projects", params=params)

        return [self._parse_project(p) for p in data.get("projects", [])]

    async def delete_project(self, project_id: str) -> bool:
        """
        Delete a project.

        Args:
            project_id: Project ID

        Returns:
            True if deleted successfully

        Raises:
            Exception: If API returns error
        """
        await self._request("DELETE", f"/projects/{project_id}")
        return True

    def _parse_project(self, data: Dict[str, Any]) -> Project:
        """Parse project data"""
        return Project(
            id=data.get("id", ""),
            name=data.get("name", ""),
            description=data.get("description"),
            status=data.get("status", ""),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== To Do ====================

    async def create_to_do(
        self,
        description: str,
        person_id: Optional[str] = None,
        company_id: Optional[str] = None,
        due_date: Optional[str] = None,
        completed: bool = False
    ) -> ToDo:
        """
        Create a new to-do.

        Args:
            description: To-do description
            person_id: Associated person ID
            company_id: Associated company ID
            due_date: Due date (YYYY-MM-DD)
            completed: Whether already completed

        Returns:
            ToDo object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "description": description,
            "completed": completed
        }

        if person_id:
            json_data["person_id"] = person_id
        if company_id:
            json_data["company_id"] = company_id
        if due_date:
            json_data["due_date"] = due_date

        data = await self._request("POST", "/todos", json_data=json_data)

        return ToDo(
            id=data.get("id", ""),
            description=data.get("description", description),
            completed=data.get("completed", completed),
            due_date=data.get("due_date") or due_date,
            created_at=data.get("created_at", "")
        )

    # ==================== Timeline Content ====================

    async def create_timeline_content(
        self,
        content_type: str,
        content: str,
        person_id: Optional[str] = None,
        company_id: Optional[str] = None
    ) -> TimelineContent:
        """
        Create timeline content.

        Args:
            content_type: Type of content (note, email, call, meeting, etc)
            content: Content
            person_id: Associated person ID
            company_id: Associated company ID

        Returns:
            TimelineContent object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "content_type": content_type,
            "content": content
        }

        if person_id:
            json_data["person_id"] = person_id
        if company_id:
            json_data["company_id"] = company_id

        data = await self._request("POST", "/timeline", json_data=json_data)

        return TimelineContent(
            id=data.get("id", ""),
            content_type=data.get("content_type", content_type),
            content=data.get("content", content),
            person_id=data.get("person_id") or person_id,
            company_id=data.get("company_id") or company_id,
            created_at=data.get("created_at", "")
        )

    # ==================== Communication Records ====================

    async def create_communication_record(
        self,
        communication_type: str,
        content: str,
        person_id: Optional[str] = None,
        company_id: Optional[str] = None,
        direction: Optional[str] = None,
        subject: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a communication record.

        Args:
            communication_type: Type (email, call, meeting, note)
            content: Content
            person_id: Associated person ID
            company_id: Associated company ID
            direction: Direction (inbound, outbound)
            subject: Subject (for emails)

        Returns:
            Created communication record

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "type": communication_type,
            "content": content
        }

        if person_id:
            json_data["person_id"] = person_id
        if company_id:
            json_data["company_id"] = company_id
        if direction:
            json_data["direction"] = direction
        if subject:
            json_data["subject"] = subject

        data = await self._request("POST", "/communications", json_data=json_data)

        return data


# ==================== Example Usage ====================

async def main():
    """Example usage of Cloze API client"""

    api_key = "your_cloze_api_key"

    async with ClozeAPIClient(api_key) as client:
        # Create a company
        company = await client.create_or_update_company(
            name="Acme Corp",
            website="https://acme.com",
            industry="Technology",
            employee_count=100
        )
        print(f"Created company: {company.id}")

        # Create a person
        person = await client.create_or_update_person(
            first_name="John",
            last_name="Doe",
            email="john@acme.com",
            company_id=company.id,
            title="CEO"
        )
        print(f"Created person: {person.id}")

        # Create a to-do
        todo = await client.create_to_do(
            description="Follow up with John",
            person_id=person.id,
            due_date="2024-02-28"
        )
        print(f"Created to-do: {todo.id}")

        # Create timeline content
        timeline = await client.create_timeline_content(
            content_type="note",
            content="Had a call with John about new partnership",
            person_id=person.id
        )
        print(f"Created timeline content: {timeline.id}")

        # Search companies
        companies = await client.search_companies(query="Acme", limit=10)
        print(f"Found {len(companies)} companies")

        # Search people
        people = await client.search_people(query="John", limit=10)
        print(f"Found {len(people)} people")


if __name__ == "__main__":
    asyncio.run(main())