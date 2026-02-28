"""
Agendor API Client

CRM and Sales Automation Platform for managing:
- Organizations (companies)
- People (contacts)
- Deals (opportunities)
- Products
- Tasks

API Actions (27):
1. Create Organization
2. Search Deal
3. Search Organization
4. Get Organization
5. Search Tasks of Person
6. Get Product
7. Update Deal
8. Create Task For Person
9. Update Deal Stage
10. Search Tasks of Deals
11. Update Product
12. Create Task For Organization
13. Create Person
14. Create Product
15. Update Organization
16. Create Task For Deal
17. Get Deal Of Person
18. Create Deal For Organization
19. Get Person
20. Update Person
21. Get Deal For Organization
22. Search Product
23. Search Tasks of Organization
24. Get Deal
25. Update Deal Status
26. Create Deal For Person
27. Search Person

Triggers (13):
- Updated Stage Deal
- Created Organization
- Updated Deal
- Won Deal
- Updated Person
- Lost Deal
- Created Activity/Task/Comment
- Deleted Person
- Updated Organization
- Created Deal
- Deleted Organization
- Created Person
- Deleted Deal

Authentication: API Token
Base URL: https://api.agendor.com.br/v3
Documentation: https://app.agendor.com.br/api
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class DealStage(Enum):
    """Deal stage enum"""
    PROSPECTING = "prospecting"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class DealStatus(Enum):
    """Deal status enum"""
    OPEN = "open"
    WON = "won"
    LOST = "lost"
    CANCELLED = "cancelled"


@dataclass
class Organization:
    """Organization model"""
    id: Optional[int] = None
    name: str = ""
    cnpj: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    annual_revenue: Optional[float] = None
    person_count: Optional[int] = None
    linkedin: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    instagram: Optional[str] = None
    industry: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Person:
    """Person model"""
    id: Optional[int] = None
    name: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    role: Optional[str] = None
    organization_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Deal:
    """Deal model"""
    id: Optional[int] = None
    title: str = ""
    value: Optional[float] = None
    stage: Optional[str] = None
    status: Optional[str] = None
    organization_id: Optional[int] = None
    person_id: Optional[int] = None
    closing_date: Optional[str] = None
    probability: Optional[int] = None
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Product:
    """Product model"""
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    price: Optional[float] = None
    sku: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Task:
    """Task model"""
    id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None
    person_id: Optional[int] = None
    organization_id: Optional[int] = None
    deal_id: Optional[int] = None
    task_type: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, calls_per_second: int = 10):
        self.calls_per_second = calls_per_second
        self.tokens = calls_per_second
        self.last_update = datetime.now()

    async def acquire(self):
        """Acquire a token from the rate limiter"""
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


class AgendorError(Exception):
    """Base exception for Agendor errors"""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}" if status_code else message)


class AgendorClient:
    """
    Agendor API Client

    Example usage:
        ```python
        client = AgendorClient(api_token="your_token")
        
        # Create an organization
        org = await client.create_organization(
            name="Acme Corp",
            website="https://acme.com"
        )
        
        # Create a person
        person = await client.create_person(
            name="John Doe",
            email="john@acme.com",
            organization_id=org.id
        )
        
        # Create a deal
        deal = await client.create_deal(
            title="New Project",
            value=10000.0,
            organization_id=org.id,
            person_id=person.id
        )
        ```
    """

    def __init__(self, api_token: str, base_url: str = "https://api.agendor.com.br/v3"):
        """
        Initialize Agendor client

        Args:
            api_token: Agendor API token
            base_url: API base URL (default: https://api.agendor.com.br/v3)
        """
        self.api_token = api_token
        self.base_url = base_url.rstrip('/')
        self._headers = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json"
        }
        self._rate_limiter = RateLimiter(calls_per_second=10)

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Agendor API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response JSON data

        Raises:
            AgendorError: If request fails
        """
        await self._rate_limiter.acquire()

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method=method,
                    url=url,
                    headers=self._headers,
                    json=data,
                    params=params
                ) as response:
                    response_text = await response.text()

                    if response.status == 204:
                        return {"status": "success"}

                    if response.status >= 400:
                        try:
                            error_data = await response.json()
                            error_msg = error_data.get("message", error_data.get("error", "Unknown error"))
                        except:
                            error_msg = response_text if response_text else "HTTP error"
                        raise AgendorError(error_msg, response.status)

                    return await response.json()

            except aiohttp.ClientError as e:
                raise AgendorError(f"Network error: {str(e)}")
            except asyncio.TimeoutError:
                raise AgendorError("Request timeout")

    # Organization methods

    async def create_organization(self, data: Dict[str, Any]) -> Organization:
        """
        Create a new organization

        Args:
            data: Organization data (name, cnpj, website, etc.)

        Returns:
            Created Organization object

        Example:
            ```python
            org = await client.create_organization({
                "name": "Acme Corp",
                "website": "https://acme.com",
                "annual_revenue": 1000000
            })
            ```
        """
        if not data.get("name"):
            raise AgendorError("Organization name is required")

        response = await self._make_request("POST", "/organizations", data=data)
        return Organization(**response)

    async def get_organization(self, organization_id: int) -> Organization:
        """
        Get organization by ID

        Args:
            organization_id: Organization ID

        Returns:
            Organization object
        """
        response = await self._make_request("GET", f"/organizations/{organization_id}")
        return Organization(**response)

    async def update_organization(self, organization_id: int, data: Dict[str, Any]) -> Organization:
        """
        Update organization

        Args:
            organization_id: Organization ID
            data: Update data

        Returns:
            Updated Organization object
        """
        response = await self._make_request("PUT", f"/organizations/{organization_id}", data=data)
        return Organization(**response)

    async def search_organization(self, **params) -> List[Organization]:
        """
        Search organizations

        Args:
            **params: Search parameters (name, cnpj, website, etc.)

        Returns:
            List of Organization objects
        """
        response = await self._make_request("GET", "/organizations", params=params)
        if "data" in response:
            return [Organization(**item) for item in response["data"]]
        return [Organization(**response)]

    # Person methods

    async def create_person(self, data: Dict[str, Any]) -> Person:
        """
        Create a new person

        Args:
            data: Person data (name, email, phone, organization_id, etc.)

        Returns:
            Created Person object
        """
        if not data.get("name"):
            raise AgendorError("Person name is required")

        response = await self._make_request("POST", "/people", data=data)
        return Person(**response)

    async def get_person(self, person_id: int) -> Person:
        """
        Get person by ID

        Args:
            person_id: Person ID

        Returns:
            Person object
        """
        response = await self._make_request("GET", f"/people/{person_id}")
        return Person(**response)

    async def update_person(self, person_id: int, data: Dict[str, Any]) -> Person:
        """
        Update person

        Args:
            person_id: Person ID
            data: Update data

        Returns:
            Updated Person object
        """
        response = await self._make_request("PUT", f"/people/{person_id}", data=data)
        return Person(**response)

    async def search_person(self, **params) -> List[Person]:
        """
        Search people

        Args:
            **params: Search parameters (name, email, organization_id, etc.)

        Returns:
            List of Person objects
        """
        response = await self._make_request("GET", "/people", params=params)
        if "data" in response:
            return [Person(**item) for item in response["data"]]
        return [Person(**response)]

    # Deal methods

    async def create_deal(self, data: Dict[str, Any]) -> Deal:
        """
        Create a new deal

        Args:
            data: Deal data (title, value, organization_id, person_id, stage, etc.)

        Returns:
            Created Deal object
        """
        if not data.get("title"):
            raise AgendorError("Deal title is required")

        response = await self._make_request("POST", "/deals", data=data)
        return Deal(**response)

    async def create_deal_for_organization(self, organization_id: int, data: Dict[str, Any]) -> Deal:
        """
        Create deal for organization

        Args:
            organization_id: Organization ID
            data: Deal data

        Returns:
            Created Deal object
        """
        data["organization_id"] = organization_id
        return await self.create_deal(data)

    async def create_deal_for_person(self, person_id: int, data: Dict[str, Any]) -> Deal:
        """
        Create deal for person

        Args:
            person_id: Person ID
            data: Deal data

        Returns:
            Created Deal object
        """
        data["person_id"] = person_id
        return await self.create_deal(data)

    async def get_deal(self, deal_id: int) -> Deal:
        """
        Get deal by ID

        Args:
            deal_id: Deal ID

        Returns:
            Deal object
        """
        response = await self._make_request("GET", f"/deals/{deal_id}")
        return Deal(**response)

    async def get_deal_of_person(self, person_id: int, deal_id: int) -> Deal:
        """
        Get deal for specific person

        Args:
            person_id: Person ID
            deal_id: Deal ID

        Returns:
            Deal object
        """
        deal = await self.get_deal(deal_id)
        if deal.person_id != person_id:
            raise AgendorError(f"Deal {deal_id} does not belong to person {person_id}")
        return deal

    async def get_deal_for_organization(self, organization_id: int, deal_id: int) -> Deal:
        """
        Get deal for specific organization

        Args:
            organization_id: Organization ID
            deal_id: Deal ID

        Returns:
            Deal object
        """
        deal = await self.get_deal(deal_id)
        if deal.organization_id != organization_id:
            raise AgendorError(f"Deal {deal_id} does not belong to organization {organization_id}")
        return deal

    async def update_deal(self, deal_id: int, data: Dict[str, Any]) -> Deal:
        """
        Update deal

        Args:
            deal_id: Deal ID
            data: Update data

        Returns:
            Updated Deal object
        """
        response = await self._make_request("PUT", f"/deals/{deal_id}", data=data)
        return Deal(**response)

    async def update_deal_stage(self, deal_id: int, stage: DealStage) -> Deal:
        """
        Update deal stage

        Args:
            deal_id: Deal ID
            stage: New stage

        Returns:
            Updated Deal object
        """
        return await self.update_deal(deal_id, {"deal_stage_name": stage.value})

    async def update_deal_status(self, deal_id: int, status: DealStatus) -> Deal:
        """
        Update deal status

        Args:
            deal_id: Deal ID
            status: New status

        Returns:
            Updated Deal object
        """
        return await self.update_deal(deal_id, {"status": status.value})

    async def search_deal(self, **params) -> List[Deal]:
        """
        Search deals

        Args:
            **params: Search parameters (organization_id, person_id, stage, status, etc.)

        Returns:
            List of Deal objects
        """
        response = await self._make_request("GET", "/deals", params=params)
        if "data" in response:
            return [Deal(**item) for item in response["data"]]
        return [Deal(**response)]

    # Product methods

    async def create_product(self, data: Dict[str, Any]) -> Product:
        """
        Create a new product

        Args:
            data: Product data (name, description, price, sku, etc.)

        Returns:
            Created Product object
        """
        if not data.get("name"):
            raise AgendorError("Product name is required")

        response = await self._make_request("POST", "/products", data=data)
        return Product(**response)

    async def get_product(self, product_id: int) -> Product:
        """
        Get product by ID

        Args:
            product_id: Product ID

        Returns:
            Product object
        """
        response = await self._make_request("GET", f"/products/{product_id}")
        return Product(**response)

    async def update_product(self, product_id: int, data: Dict[str, Any]) -> Product:
        """
        Update product

        Args:
            product_id: Product ID
            data: Update data

        Returns:
            Updated Product object
        """
        response = await self._make_request("PUT", f"/products/{product_id}", data=data)
        return Product(**response)

    async def search_product(self, **params) -> List[Product]:
        """
        Search products

        Args:
            **params: Search parameters (name, sku, etc.)

        Returns:
            List of Product objects
        """
        response = await self._make_request("GET", "/products", params=params)
        if "data" in response:
            return [Product(**item) for item in response["data"]]
        return [Product(**response)]

    # Task methods

    async def create_task(self, data: Dict[str, Any]) -> Task:
        """
        Create a new task

        Args:
            data: Task data (title, description, due_date, person_id, organization_id, deal_id, etc.)

        Returns:
            Created Task object
        """
        if not data.get("title"):
            raise AgendorError("Task title is required")

        response = await self._make_request("POST", "/tasks", data=data)
        return Task(**response)

    async def create_task_for_person(self, person_id: int, data: Dict[str, Any]) -> Task:
        """
        Create task for person

        Args:
            person_id: Person ID
            data: Task data

        Returns:
            Created Task object
        """
        data["person_id"] = person_id
        return await self.create_task(data)

    async def create_task_for_organization(self, organization_id: int, data: Dict[str, Any]) -> Task:
        """
        Create task for organization

        Args:
            organization_id: Organization ID
            data: Task data

        Returns:
            Created Task object
        """
        data["organization_id"] = organization_id
        return await self.create_task(data)

    async def create_task_for_deal(self, deal_id: int, data: Dict[str, Any]) -> Task:
        """
        Create task for deal

        Args:
            deal_id: Deal ID
            data: Task data

        Returns:
            Created Task object
        """
        data["deal_id"] = deal_id
        return await self.create_task(data)

    async def search_tasks_of_person(self, person_id: int, **params) -> List[Task]:
        """
        Search tasks for person

        Args:
            person_id: Person ID
            **params: Additional search parameters

        Returns:
            List of Task objects
        """
        params["person_id"] = person_id
        response = await self._make_request("GET", "/tasks", params=params)
        if "data" in response:
            return [Task(**item) for item in response["data"]]
        return [Task(**response)]

    async def search_tasks_of_organization(self, organization_id: int, **params) -> List[Task]:
        """
        Search tasks for organization

        Args:
            organization_id: Organization ID
            **params: Additional search parameters

        Returns:
            List of Task objects
        """
        params["organization_id"] = organization_id
        response = await self._make_request("GET", "/tasks", params=params)
        if "data" in response:
            return [Task(**item) for item in response["data"]]
        return [Task(**response)]

    async def search_tasks_of_deals(self, deal_id: int, **params) -> List[Task]:
        """
        Search tasks for deal

        Args:
            deal_id: Deal ID
            **params: Additional search parameters

        Returns:
            List of Task objects
        """
        params["deal_id"] = deal_id
        response = await self._make_request("GET", "/tasks", params=params)
        if "data" in response:
            return [Task(**item) for item in response["data"]]
        return [Task(**response)]

    # Webhook handling for triggers

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process webhook event from Agendor

        Args:
            webhook_data: Webhook payload

        Returns:
            Processed event data with event type and entity info

        Supported triggers:
        - Updated Stage Deal
        - Created Organization
        - Updated Deal
        - Won Deal
        - Lost Deal
        - Updated Person
        - Created Activity/Task/Comment
        - Deleted Person
        - Updated Organization
        - Created Deal
        - Deleted Organization
        - Created Person
        - Deleted Deal
        """
        event_type = webhook_data.get("event_type", "unknown")
        entity_type = webhook_data.get("entity_type", "unknown")
        entity_id = webhook_data.get("entity_id")

        return {
            "event_type": event_type,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "data": webhook_data
        }