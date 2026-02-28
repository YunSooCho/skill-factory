"""
Capsule CRM API Client

Capsule CRM provides customer relationship management with parties, opportunities, tasks, and projects.

Supports:
- Search Party
- Get Party
- List Party
- Create Party
- Update Party
- Delete Party
- Search Opportunity
- Get Opportunity
- List Opportunity
- Create Opportunity
- Update Opportunity
- Delete Opportunity
- Search Task
- Get Task
- List Task
- Create Task
- Update Task
- Delete Task
- Search Project
- Get Project
- List Project
- Create Project
- Update Project
- Delete Project
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Party:
    """Party object (Person or Organization)"""
    id: int
    type: str  # person or organization
    display_name: str
    first_name: Optional[str]
    last_name: Optional[str]
    organisation_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    created_on: str
    updated_on: str


@dataclass
class Opportunity:
    """Opportunity object"""
    id: int
    party_id: int
    party_name: str
    name: str
    milestone_id: int
    milestone_name: str
    probability: Optional[int]
    value: float
    currency: str
    expected_close_date: Optional[str]
    created_on: str
    updated_on: str


@dataclass
class Task:
    """Task object"""
    id: int
    party_id: Optional[int]
    party_name: Optional[str]
    description: str
    due_date: Optional[str]
    status: str  # OPEN, COMPLETED, CANCELLED
    category: Optional[str]
    created_on: str
    updated_on: str


@dataclass
class Project:
    """Project object"""
    id: int
    party_id: Optional[int]
    party_name: Optional[str]
    name: str
    description: str
    status: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    created_on: str
    updated_on: str


class CapsuleCRMClient:
    """
    Capsule CRM API client for CRM operations.

    Authentication: API Key
    Documentation: https://developer.capsulecrm.com/v2/overview/
    Base URL: https://api.capsulecrm.com/api/v2
    """

    BASE_URL = "https://api.capsulecrm.com/api/v2"

    def __init__(self, api_key: str, account_name: str):
        """
        Initialize Capsule CRM API client.

        Args:
            api_key: Capsule CRM API key
            account_name: Capsule CRM account name (from URL, e.g., "company" in company.capsulecrm.com)
        """
        self.api_key = api_key
        self.account_name = account_name
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
        Make HTTP request to Capsule CRM API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            aiohttp.ClientError: If request fails
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
                raise Exception(f"Capsule CRM API error ({response.status}): {error_msg}")

            return data

    # ==================== Parties ====================

    async def create_party(
        self,
        party_type: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        organisation_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        title: Optional[str] = None
    ) -> Party:
        """
        Create a new party (person or organization).

        Args:
            party_type: Type - "person" or "organization"
            first_name: First name (for person)
            last_name: Last name (for person)
            organisation_name: Organization name (for organization)
            email: Email address
            phone: Phone number
            title: Job title

        Returns:
            Party object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {"type": party_type}

        if party_type == "person":
            if first_name or last_name:
                json_data["firstName"] = first_name or ""
                json_data["lastName"] = last_name or ""
        elif party_type == "organization":
            if organisation_name:
                json_data["name"] = organisation_name

        if email:
            json_data["emailAddresses"] = [{"type": "Work", "address": email}]
        if phone:
            json_data["phoneNumbers"] = [{"type": "Mobile", "phoneNumber": phone}]
        if title:
            json_data["title"] = title

        data = await self._request("POST", "/parties", json_data=json_data)

        return self._parse_party(data)

    async def get_party(self, party_id: int) -> Party:
        """
        Get a party by ID.

        Args:
            party_id: Party ID

        Returns:
            Party object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request("GET", f"/parties/{party_id}")
        return self._parse_party(data)

    async def list_parties(
        self,
        party_type: Optional[str] = None,
        since: Optional[str] = None,
        limit: int = 50,
        last_id: Optional[int] = None
    ) -> List[Party]:
        """
        List parties.

        Args:
            party_type: Filter by type (person, organization)
            since: Filter by modification date (ISO 8601)
            limit: Maximum number of parties to return (max 100)
            last_id: Last party ID for pagination

        Returns:
            List of Party objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"perPage": min(limit, 100)}

        if party_type:
            params["type"] = party_type
        if since:
            params["since"] = since
        if last_id:
            params["lastId"] = last_id

        data = await self._request("GET", "/parties", params=params)

        parties = data.get("parties", [])
        return [self._parse_party(p) for p in parties]

    async def search_parties(
        self,
        query: str,
        limit: int = 50
    ) -> List[Party]:
        """
        Search for parties.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of Party objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"q": query, "perPage": min(limit, 100)}

        data = await self._request("GET", "/parties", params=params)

        parties = data.get("parties", [])
        return [self._parse_party(p) for p in parties]

    async def update_party(
        self,
        party_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        organisation_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        title: Optional[str] = None
    ) -> Party:
        """
        Update a party.

        Args:
            party_id: Party ID
            first_name: New first name
            last_name: New last name
            organisation_name: New organization name
            email: New email
            phone: New phone
            title: New title

        Returns:
            Updated Party object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {}

        if first_name is not None:
            json_data["firstName"] = first_name
        if last_name is not None:
            json_data["lastName"] = last_name
        if organisation_name is not None:
            json_data["name"] = organisation_name
        if email:
            json_data["emailAddresses"] = [{"type": "Work", "address": email}]
        if phone:
            json_data["phoneNumbers"] = [{"type": "Mobile", "phoneNumber": phone}]
        if title:
            json_data["title"] = title

        data = await self._request("PUT", f"/parties/{party_id}", json_data=json_data)

        return self._parse_party(data)

    async def delete_party(self, party_id: int) -> bool:
        """
        Delete a party.

        Args:
            party_id: Party ID

        Returns:
            True if deleted successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        await self._request("DELETE", f"/parties/{party_id}")
        return True

    def _parse_party(self, data: Dict[str, Any]) -> Party:
        """Parse party data from API response"""
        party_type = data.get("type", "")

        first_name = None
        last_name = None
        organisation_name = None

        if party_type == "person":
            first_name = data.get("firstName")
            last_name = data.get("lastName")
        elif party_type == "organization":
            organisation_name = data.get("name")

        # Get email
        email = None
        emails = data.get("emailAddresses", [])
        if emails:
            email = emails[0].get("address")

        # Get phone
        phone = None
        phones = data.get("phoneNumbers", [])
        if phones:
            phone = phones[0].get("phoneNumber")

        return Party(
            id=int(data.get("id", 0)),
            type=party_type,
            display_name=data.get("name", data.get("fullName", "")),
            first_name=first_name,
            last_name=last_name,
            organisation_name=organisation_name,
            email=email,
            phone=phone,
            created_on=data.get("createdOn", ""),
            updated_on=data.get("updatedOn", "")
        )

    # ==================== Opportunities ====================

    async def create_opportunity(
        self,
        party_id: int,
        name: str,
        milestone_id: int,
        value: float,
        currency: str = "USD",
        expected_close_date: Optional[str] = None,
        description: Optional[str] = None
    ) -> Opportunity:
        """
        Create a new opportunity.

        Args:
            party_id: Party ID
            name: Opportunity name
            milestone_id: Milestone ID
            value: Opportunity value
            currency: Currency code (default: USD)
            expected_close_date: Expected close date (ISO 8601)
            description: Description

        Returns:
            Opportunity object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {
            "partyId": party_id,
            "name": name,
            "milestoneId": milestone_id,
            "value": {
                "amount": value,
                "currency": currency
            }
        }

        if expected_close_date:
            json_data["expectedCloseDate"] = expected_close_date
        if description:
            json_data["description"] = description

        data = await self._request("POST", "/opportunities", json_data=json_data)

        return self._parse_opportunity(data)

    async def get_opportunity(self, opportunity_id: int) -> Opportunity:
        """
        Get an opportunity by ID.

        Args:
            opportunity_id: Opportunity ID

        Returns:
            Opportunity object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request("GET", f"/opportunities/{opportunity_id}")
        return self._parse_opportunity(data)

    async def list_opportunities(
        self,
        party_id: Optional[int] = None,
        milestone_id: Optional[int] = None,
        since: Optional[str] = None,
        limit: int = 50
    ) -> List[Opportunity]:
        """
        List opportunities.

        Args:
            party_id: Filter by party ID
            milestone_id: Filter by milestone ID
            since: Filter by modification date (ISO 8601)
            limit: Maximum number of results

        Returns:
            List of Opportunity objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"perPage": min(limit, 100)}

        if party_id:
            params["partyId"] = party_id
        if milestone_id:
            params["milestoneId"] = milestone_id
        if since:
            params["since"] = since

        data = await self._request("GET", "/opportunities", params=params)

        opportunities = data.get("opportunities", [])
        return [self._parse_opportunity(o) for o in opportunities]

    async def search_opportunities(
        self,
        query: str,
        limit: int = 50
    ) -> List[Opportunity]:
        """
        Search for opportunities.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of Opportunity objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"q": query, "perPage": min(limit, 100)}

        data = await self._request("GET", "/opportunities", params=params)

        opportunities = data.get("opportunities", [])
        return [self._parse_opportunity(o) for o in opportunities]

    async def update_opportunity(
        self,
        opportunity_id: int,
        name: Optional[str] = None,
        milestone_id: Optional[int] = None,
        value: Optional[float] = None,
        expected_close_date: Optional[str] = None,
        description: Optional[str] = None
    ) -> Opportunity:
        """
        Update an opportunity.

        Args:
            opportunity_id: Opportunity ID
            name: New name
            milestone_id: New milestone ID
            value: New value
            expected_close_date: New expected close date
            description: New description

        Returns:
            Updated Opportunity object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if milestone_id:
            json_data["milestoneId"] = milestone_id
        if value is not None:
            json_data["value"] = {
                "amount": value,
                "currency": "USD"  # Default currency
            }
        if expected_close_date:
            json_data["expectedCloseDate"] = expected_close_date
        if description:
            json_data["description"] = description

        data = await self._request("PUT", f"/opportunities/{opportunity_id}", json_data=json_data)

        return self._parse_opportunity(data)

    async def delete_opportunity(self, opportunity_id: int) -> bool:
        """
        Delete an opportunity.

        Args:
            opportunity_id: Opportunity ID

        Returns:
            True if deleted successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        await self._request("DELETE", f"/opportunities/{opportunity_id}")
        return True

    def _parse_opportunity(self, data: Dict[str, Any]) -> Opportunity:
        """Parse opportunity data from API response"""
        value_data = data.get("value", {})

        return Opportunity(
            id=int(data.get("id", 0)),
            party_id=int(data.get("partyId", 0)),
            party_name=data.get("partyName", ""),
            name=data.get("name", ""),
            milestone_id=int(data.get("milestoneId", 0)),
            milestone_name=data.get("milestoneName", ""),
            probability=data.get("probability"),
            value=float(value_data.get("amount", 0)),
            currency=value_data.get("currency", "USD"),
            expected_close_date=data.get("expectedCloseDate"),
            created_on=data.get("createdOn", ""),
            updated_on=data.get("updatedOn", "")
        )

    # ==================== Tasks ====================

    async def create_task(
        self,
        description: str,
        party_id: Optional[int] = None,
        due_date: Optional[str] = None,
        category: Optional[str] = None
    ) -> Task:
        """
        Create a new task.

        Args:
            description: Task description
            party_id: Optional party ID
            due_date: Due date (ISO 8601)
            category: Task category

        Returns:
            Task object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {"description": description}

        if party_id:
            json_data["partyId"] = party_id
        if due_date:
            json_data["dueOn"] = due_date
        if category:
            json_data["category"] = category

        data = await self._request("POST", "/tasks", json_data=json_data)

        return self._parse_task(data)

    async def get_task(self, task_id: int) -> Task:
        """
        Get a task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request("GET", f"/tasks/{task_id}")
        return self._parse_task(data)

    async def list_tasks(
        self,
        party_id: Optional[int] = None,
        status: Optional[str] = None,
        since: Optional[str] = None,
        limit: int = 50
    ) -> List[Task]:
        """
        List tasks.

        Args:
            party_id: Filter by party ID
            status: Filter by status (OPEN, COMPLETED, CANCELLED)
            since: Filter by modification date (ISO 8601)
            limit: Maximum number of results

        Returns:
            List of Task objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"perPage": min(limit, 100)}

        if party_id:
            params["partyId"] = party_id
        if status:
            params["status"] = status
        if since:
            params["since"] = since

        data = await self._request("GET", "/tasks", params=params)

        tasks = data.get("tasks", [])
        return [self._parse_task(t) for t in tasks]

    async def search_tasks(
        self,
        query: str,
        limit: int = 50
    ) -> List[Task]:
        """
        Search for tasks.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of Task objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"q": query, "perPage": min(limit, 100)}

        data = await self._request("GET", "/tasks", params=params)

        tasks = data.get("tasks", [])
        return [self._parse_task(t) for t in tasks]

    async def update_task(
        self,
        task_id: int,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        status: Optional[str] = None,
        category: Optional[str] = None
    ) -> Task:
        """
        Update a task.

        Args:
            task_id: Task ID
            description: New description
            due_date: New due date (ISO 8601)
            status: New status (OPEN, COMPLETED, CANCELLED)
            category: New category

        Returns:
            Updated Task object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {}

        if description:
            json_data["description"] = description
        if due_date:
            json_data["dueOn"] = due_date
        if status:
            json_data["status"] = status
        if category:
            json_data["category"] = category

        data = await self._request("PUT", f"/tasks/{task_id}", json_data=json_data)

        return self._parse_task(data)

    async def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.

        Args:
            task_id: Task ID

        Returns:
            True if deleted successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        await self._request("DELETE", f"/tasks/{task_id}")
        return True

    def _parse_task(self, data: Dict[str, Any]) -> Task:
        """Parse task data from API response"""
        return Task(
            id=int(data.get("id", 0)),
            party_id=int(data["partyId"]) if data.get("partyId") else None,
            party_name=data.get("partyName"),
            description=data.get("description", ""),
            due_date=data.get("dueOn"),
            status=data.get("status", "OPEN"),
            category=data.get("category"),
            created_on=data.get("createdOn", ""),
            updated_on=data.get("updatedOn", "")
        )

    # ==================== Projects ====================

    async def create_project(
        self,
        name: str,
        description: str = "",
        party_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Project:
        """
        Create a new project.

        Args:
            name: Project name
            description: Project description
            party_id: Optional party ID
            start_date: Start date (ISO 8601)
            end_date: End date (ISO 8601)

        Returns:
            Project object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        # Note: Projects in Capsule CRm may be tracked as custom fields or Kases
        # This is a placeholder implementation
        json_data = {
            "name": name,
            "description": description
        }

        if party_id:
            json_data["partyId"] = party_id
        if start_date:
            json_data["startDate"] = start_date
        if end_date:
            json_data["endDate"] = end_date

        data = await self._request("POST", "/kases", json_data=json_data)

        return self._parse_project(data)

    async def get_project(self, project_id: int) -> Project:
        """
        Get a project by ID.

        Args:
            project_id: Project ID

        Returns:
            Project object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request("GET", f"/kases/{project_id}")
        return self._parse_project(data)

    async def list_projects(
        self,
        party_id: Optional[int] = None,
        since: Optional[str] = None,
        limit: int = 50
    ) -> List[Project]:
        """
        List projects.

        Args:
            party_id: Filter by party ID
            since: Filter by modification date (ISO 8601)
            limit: Maximum number of results

        Returns:
            List of Project objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"perPage": min(limit, 100)}

        if party_id:
            params["partyId"] = party_id
        if since:
            params["since"] = since

        data = await self._request("GET", "/kases", params=params)

        projects = data.get("kases", [])
        return [self._parse_project(p) for p in projects]

    async def search_projects(
        self,
        query: str,
        limit: int = 50
    ) -> List[Project]:
        """
        Search for projects.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of Project objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"q": query, "perPage": min(limit, 100)}

        data = await self._request("GET", "/kases", params=params)

        projects = data.get("kases", [])
        return [self._parse_project(p) for p in projects]

    async def update_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        status: Optional[str] = None
    ) -> Project:
        """
        Update a project.

        Args:
            project_id: Project ID
            name: New name
            description: New description
            start_date: New start date (ISO 8601)
            end_date: New end date (ISO 8601)
            status: New status

        Returns:
            Updated Project object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if description:
            json_data["description"] = description
        if start_date:
            json_data["startDate"] = start_date
        if end_date:
            json_data["endDate"] = end_date
        if status:
            json_data["status"] = status

        data = await self._request("PUT", f"/kases/{project_id}", json_data=json_data)

        return self._parse_project(data)

    async def delete_project(self, project_id: int) -> bool:
        """
        Delete a project.

        Args:
            project_id: Project ID

        Returns:
            True if deleted successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        await self._request("DELETE", f"/kases/{project_id}")
        return True

    def _parse_project(self, data: Dict[str, Any]) -> Project:
        """Parse project data from API response"""
        return Project(
            id=int(data.get("id", 0)),
            party_id=int(data["partyId"]) if data.get("partyId") else None,
            party_name=data.get("partyName"),
            name=data.get("name", ""),
            description=data.get("description", ""),
            status=data.get("status"),
            start_date=data.get("startDate"),
            end_date=data.get("endDate"),
            created_on=data.get("createdOn", ""),
            updated_on=data.get("updatedOn", "")
        )


# ==================== Webhook Support ====================

class CapsuleCRMWebhookHandler:
    """
    Capsule CRM webhook handler for processing incoming events.

    Supported webhook events:
    - Completed Task
    - Updated Opportunity Milestone
    - New Opportunity
    - Updated Opportunity
    - Updated Party
    - Updated to Specified Opportunity Milestone
    - Closed Opportunity
    - New Party
    - New Task
    - Updated Task
    """

    @staticmethod
    def parse_webhook_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and validate webhook payload.

        Args:
            payload: Raw webhook payload

        Returns:
            Parsed event data with event_type and data
        """
        event_type = payload.get("eventType", payload.get("event_type", ""))

        return {
            "event_type": event_type,
            "timestamp": payload.get("timestamp", datetime.utcnow().isoformat()),
            "data": payload.get("data", {})
        }

    @staticmethod
    def handle_new_party(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle new party event"""
        return {
            "party_id": payload.get("id"),
            "party_type": payload.get("type"),
            "name": payload.get("name") or payload.get("fullName"),
            "timestamp": payload.get("createdOn")
        }

    @staticmethod
    def handle_new_opportunity(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle new opportunity event"""
        return {
            "opportunity_id": payload.get("id"),
            "party_id": payload.get("partyId"),
            "name": payload.get("name"),
            "milestone_id": payload.get("milestoneId"),
            "value": payload.get("value", {}).get("amount"),
            "timestamp": payload.get("createdOn")
        }

    @staticmethod
    def handle_new_task(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle new task event"""
        return {
            "task_id": payload.get("id"),
            "party_id": payload.get("partyId"),
            "description": payload.get("description"),
            "due_date": payload.get("dueOn"),
            "timestamp": payload.get("createdOn")
        }


# ==================== Example Usage ====================

async def main():
    """Example usage of Capsule CRM API client"""

    api_key = "your_capsule_api_key"
    account_name = "your_account"

    async with CapsuleCRMClient(api_key, account_name) as client:
        # Create a party (person)
        person = await client.create_party(
            party_type="person",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="+1234567890"
        )
        print(f"Created person: {person.id}")

        # Create an opportunity
        opportunity = await client.create_opportunity(
            party_id=person.id,
            name="Website Development",
            milestone_id=1,
            value=10000.0,
            currency="USD"
        )
        print(f"Created opportunity: {opportunity.id}")

        # Create a task
        task = await client.create_task(
            description="Follow up with customer",
            party_id=person.id
        )
        print(f"Created task: {task.id}")

        # List parties
        parties = await client.list_parties(limit=10)
        print(f"Found {len(parties)} parties")

        # Search parties
        results = await client.search_parties("John")
        print(f"Search found {len(results)} results")


if __name__ == "__main__":
    asyncio.run(main())