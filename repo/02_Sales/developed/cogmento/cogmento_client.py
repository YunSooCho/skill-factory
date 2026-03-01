"""
Cogmento API Client

Cogmento is a CRM platform for managing companies, contacts, deals, and tasks.

Supports:
- Get Company
- Create Company
- Update Company
- Delete Company
- List Companies
- Get Contact
- Create Contact
- Update Contact
- Delete Contact
- List Contacts
- Get Deal
- Create Deal
- Update Deal
- List Deals
- Get Product
- Create Product
- Update Product
- List Products
- Get Task
- Create Task
- Update Task
- List Tasks
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
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Contact:
    """Contact object"""
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
class Deal:
    """Deal object"""
    id: str
    name: str
    amount: float
    currency: str
    stage: str
    probability: int
    contact_id: Optional[str]
    company_id: Optional[str]
    expected_close_date: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Product:
    """Product object"""
    id: str
    name: str
    code: Optional[str]
    price: float
    currency: str
    description: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Task:
    """Task object"""
    id: str
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[str]
    related_entity_type: Optional[str]
    related_entity_id: Optional[str]
    created_at: str
    updated_at: str


class CogmentoAPIClient:
    """
    Cogmento API client for CRM operations.

    Authentication: API Key
    Base URL: https://api.cogmento.com/v1
    """

    BASE_URL = "https://api.cogmento.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Cogmento API client.

        Args:
            api_key: Cogmento API key
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
        Make HTTP request to Cogmento API.

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
                raise Exception(f"Cogmento API error ({response.status}): {error_msg}")

            return data

    # ==================== Companies ====================

    async def create_company(
        self,
        name: str,
        website: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None
    ) -> Company:
        """
        Create a new company.

        Args:
            name: Company name
            website: Company website
            address: Company address
            phone: Company phone
            email: Company email

        Returns:
            Company object

        Raises:
            Exception: If API returns error
        """
        json_data = {"name": name}

        if website:
            json_data["website"] = website
        if address:
            json_data["address"] = address
        if phone:
            json_data["phone"] = phone
        if email:
            json_data["email"] = email

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

    async def list_companies(
        self,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Company]:
        """
        List companies.

        Args:
            search: Search query
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of Company objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit, "offset": offset}

        if search:
            params["search"] = search

        data = await self._request("GET", "/companies", params=params)

        return [self._parse_company(c) for c in data.get("data", [])]

    async def update_company(
        self,
        company_id: str,
        name: Optional[str] = None,
        website: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None
    ) -> Company:
        """
        Update a company.

        Args:
            company_id: Company ID
            name: New name
            website: New website
            address: New address
            phone: New phone
            email: New email

        Returns:
            Updated Company object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if website:
            json_data["website"] = website
        if address:
            json_data["address"] = address
        if phone:
            json_data["phone"] = phone
        if email:
            json_data["email"] = email

        data = await self._request("PUT", f"/companies/{company_id}", json_data=json_data)

        return self._parse_company(data)

    def _parse_company(self, data: Dict[str, Any]) -> Company:
        """Parse company data"""
        return Company(
            id=data.get("id", ""),
            name=data.get("name", ""),
            website=data.get("website"),
            address=data.get("address"),
            phone=data.get("phone"),
            email=data.get("email"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Contacts ====================

    async def create_contact(
        self,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company_id: Optional[str] = None,
        title: Optional[str] = None
    ) -> Contact:
        """
        Create a new contact.

        Args:
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number
            company_id: Associated company ID
            title: Job title

        Returns:
            Contact object

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

        data = await self._request("POST", "/contacts", json_data=json_data)

        return self._parse_contact(data)

    async def get_contact(self, contact_id: str) -> Contact:
        """
        Get a contact by ID.

        Args:
            contact_id: Contact ID

        Returns:
            Contact object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/contacts/{contact_id}")
        return self._parse_contact(data)

    async def list_contacts(
        self,
        search: Optional[str] = None,
        company_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Contact]:
        """
        List contacts.

        Args:
            search: Search query
            company_id: Filter by company ID
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of Contact objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit, "offset": offset}

        if search:
            params["search"] = search
        if company_id:
            params["company_id"] = company_id

        data = await self._request("GET", "/contacts", params=params)

        return [self._parse_contact(c) for c in data.get("data", [])]

    async def update_contact(
        self,
        contact_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company_id: Optional[str] = None,
        title: Optional[str] = None
    ) -> Contact:
        """
        Update a contact.

        Args:
            contact_id: Contact ID
            first_name: New first name
            last_name: New last name
            email: New email
            phone: New phone
            company_id: New company ID
            title: New title

        Returns:
            Updated Contact object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if first_name:
            json_data["first_name"] = first_name
        if last_name:
            json_data["last_name"] = last_name
        if email:
            json_data["email"] = email
        if phone:
            json_data["phone"] = phone
        if company_id:
            json_data["company_id"] = company_id
        if title:
            json_data["title"] = title

        data = await self._request("PUT", f"/contacts/{contact_id}", json_data=json_data)

        return self._parse_contact(data)

    def _parse_contact(self, data: Dict[str, Any]) -> Contact:
        """Parse contact data"""
        # Try to get company info
        company_name = None
        if data.get("company"):
            company_name = data["company"].get("name")

        return Contact(
            id=data.get("id", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            company_id=data.get("company_id"),
            company_name=company_name,
            title=data.get("title"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Deals ====================

    async def create_deal(
        self,
        name: str,
        amount: float,
        currency: str = "USD",
        stage: str = "new",
        probability: int = 50,
        contact_id: Optional[str] = None,
        company_id: Optional[str] = None,
        expected_close_date: Optional[str] = None
    ) -> Deal:
        """
        Create a new deal.

        Args:
            name: Deal name
            amount: Deal amount
            currency: Currency code
            stage: Deal stage
            probability: Win probability (0-100)
            contact_id: Associated contact ID
            company_id: Associated company ID
            expected_close_date: Expected close date (YYYY-MM-DD)

        Returns:
            Deal object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "name": name,
            "amount": amount,
            "currency": currency,
            "stage": stage,
            "probability": probability
        }

        if contact_id:
            json_data["contact_id"] = contact_id
        if company_id:
            json_data["company_id"] = company_id
        if expected_close_date:
            json_data["expected_close_date"] = expected_close_date

        data = await self._request("POST", "/deals", json_data=json_data)

        return self._parse_deal(data)

    async def get_deal(self, deal_id: str) -> Deal:
        """
        Get a deal by ID.

        Args:
            deal_id: Deal ID

        Returns:
            Deal object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/deals/{deal_id}")
        return self._parse_deal(data)

    async def list_deals(
        self,
        search: Optional[str] = None,
        stage: Optional[str] = None,
        contact_id: Optional[str] = None,
        company_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Deal]:
        """
        List deals.

        Args:
            search: Search query
            stage: Filter by stage
            contact_id: Filter by contact ID
            company_id: Filter by company ID
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of Deal objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit, "offset": offset}

        if search:
            params["search"] = search
        if stage:
            params["stage"] = stage
        if contact_id:
            params["contact_id"] = contact_id
        if company_id:
            params["company_id"] = company_id

        data = await self._request("GET", "/deals", params=params)

        return [self._parse_deal(d) for d in data.get("data", [])]

    async def update_deal(
        self,
        deal_id: str,
        name: Optional[str] = None,
        amount: Optional[float] = None,
        stage: Optional[str] = None,
        probability: Optional[int] = None,
        expected_close_date: Optional[str] = None
    ) -> Deal:
        """
        Update a deal.

        Args:
            deal_id: Deal ID
            name: New name
            amount: New amount
            stage: New stage
            probability: New probability (0-100)
            expected_close_date: New expected close date

        Returns:
            Updated Deal object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if amount is not None:
            json_data["amount"] = amount
        if stage:
            json_data["stage"] = stage
        if probability is not None:
            json_data["probability"] = probability
        if expected_close_date:
            json_data["expected_close_date"] = expected_close_date

        data = await self._request("PUT", f"/deals/{deal_id}", json_data=json_data)

        return self._parse_deal(data)

    def _parse_deal(self, data: Dict[str, Any]) -> Deal:
        """Parse deal data"""
        return Deal(
            id=data.get("id", ""),
            name=data.get("name", ""),
            amount=float(data.get("amount", 0)),
            currency=data.get("currency", "USD"),
            stage=data.get("stage", ""),
            probability=int(data.get("probability", 50)),
            contact_id=data.get("contact_id"),
            company_id=data.get("company_id"),
            expected_close_date=data.get("expected_close_date"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Products ====================

    async def create_product(
        self,
        name: str,
        price: float,
        currency: str = "USD",
        code: Optional[str] = None,
        description: Optional[str] = None
    ) -> Product:
        """
        Create a new product.

        Args:
            name: Product name
            price: Product price
            currency: Currency code
            code: Product code
            description: Product description

        Returns:
            Product object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "name": name,
            "price": price,
            "currency": currency
        }

        if code:
            json_data["code"] = code
        if description:
            json_data["description"] = description

        data = await self._request("POST", "/products", json_data=json_data)

        return self._parse_product(data)

    async def get_product(self, product_id: str) -> Product:
        """
        Get a product by ID.

        Args:
            product_id: Product ID

        Returns:
            Product object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/products/{product_id}")
        return self._parse_product(data)

    async def list_products(
        self,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Product]:
        """
        List products.

        Args:
            search: Search query
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of Product objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit, "offset": offset}

        if search:
            params["search"] = search

        data = await self._request("GET", "/products", params=params)

        return [self._parse_product(p) for p in data.get("data", [])]

    async def update_product(
        self,
        product_id: str,
        name: Optional[str] = None,
        price: Optional[float] = None,
        code: Optional[str] = None,
        description: Optional[str] = None
    ) -> Product:
        """
        Update a product.

        Args:
            product_id: Product ID
            name: New name
            price: New price
            code: New code
            description: New description

        Returns:
            Updated Product object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if price is not None:
            json_data["price"] = price
        if code:
            json_data["code"] = code
        if description:
            json_data["description"] = description

        data = await self._request("PUT", f"/products/{product_id}", json_data=json_data)

        return self._parse_product(data)

    def _parse_product(self, data: Dict[str, Any]) -> Product:
        """Parse product data"""
        return Product(
            id=data.get("id", ""),
            name=data.get("name", ""),
            code=data.get("code"),
            price=float(data.get("price", 0)),
            currency=data.get("currency", "USD"),
            description=data.get("description"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Tasks ====================

    async def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        status: str = "pending",
        priority: str = "normal",
        due_date: Optional[str] = None,
        related_entity_type: Optional[str] = None,
        related_entity_id: Optional[str] = None
    ) -> Task:
        """
        Create a new task.

        Args:
            title: Task title
            description: Task description
            status: Task status (pending, in_progress, completed, cancelled)
            priority: Task priority (low, normal, high, urgent)
            due_date: Due date (YYYY-MM-DD)
            related_entity_type: Related entity type (contact, company, deal)
            related_entity_id: Related entity ID

        Returns:
            Task object

        Raises:
            Exception: If API returns error
        """
        json_data = {
            "title": title,
            "status": status,
            "priority": priority
        }

        if description:
            json_data["description"] = description
        if due_date:
            json_data["due_date"] = due_date
        if related_entity_type:
            json_data["related_entity_type"] = related_entity_type
        if related_entity_id:
            json_data["related_entity_id"] = related_entity_id

        data = await self._request("POST", "/tasks", json_data=json_data)

        return self._parse_task(data)

    async def get_task(self, task_id: str) -> Task:
        """
        Get a task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task object

        Raises:
            Exception: If API returns error
        """
        data = await self._request("GET", f"/tasks/{task_id}")
        return self._parse_task(data)

    async def list_tasks(
        self,
        search: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        related_entity_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Task]:
        """
        List tasks.

        Args:
            search: Search query
            status: Filter by status
            priority: Filter by priority
            related_entity_type: Filter by related entity type
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of Task objects

        Raises:
            Exception: If API returns error
        """
        params = {"limit": limit, "offset": offset}

        if search:
            params["search"] = search
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        if related_entity_type:
            params["related_entity_type"] = related_entity_type

        data = await self._request("GET", "/tasks", params=params)

        return [self._parse_task(t) for t in data.get("data", [])]

    async def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> Task:
        """
        Update a task.

        Args:
            task_id: Task ID
            title: New title
            description: New description
            status: New status
            priority: New priority
            due_date: New due date

        Returns:
            Updated Task object

        Raises:
            Exception: If API returns error
        """
        json_data = {}

        if title:
            json_data["title"] = title
        if description:
            json_data["description"] = description
        if status:
            json_data["status"] = status
        if priority:
            json_data["priority"] = priority
        if due_date:
            json_data["due_date"] = due_date

        data = await self._request("PUT", f"/tasks/{task_id}", json_data=json_data)

        return self._parse_task(data)

    def _parse_task(self, data: Dict[str, Any]) -> Task:
        """Parse task data"""
        return Task(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description"),
            status=data.get("status", ""),
            priority=data.get("priority", ""),
            due_date=data.get("due_date"),
            related_entity_type=data.get("related_entity_type"),
            related_entity_id=data.get("related_entity_id"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )


# ==================== Example Usage ====================

async def main():
    """Example usage of Cogmento API client"""

    api_key = "your_cogmento_api_key"

    async with CogmentoAPIClient(api_key) as client:
        # Create a company
        company = await client.create_company(
            name="Startup Inc",
            website="https://startup.com",
            email="info@startup.com"
        )
        print(f"Created company: {company.id}")

        # Create a contact
        contact = await client.create_contact(
            first_name="Jane",
            last_name="Smith",
            email="jane@startup.com",
            company_id=company.id,
            title="Founder"
        )
        print(f"Created contact: {contact.id}")

        # Create a deal
        deal = await client.create_deal(
            name="Enterprise Contract",
            amount=100000.0,
            currency="USD",
            stage="proposal",
            probability=70,
            contact_id=contact.id,
            company_id=company.id
        )
        print(f"Created deal: {deal.id}")

        # Create a product
        product = await client.create_product(
            name="Pro Subscription",
            price=99.99,
            currency="USD",
            code="PRO-001"
        )
        print(f"Created product: {product.id}")

        # Create a task
        task = await client.create_task(
            title="Send follow-up email",
            description="Follow up with Jane about the deal",
            status="pending",
            priority="high",
            related_entity_type="deal",
            related_entity_id=deal.id
        )
        print(f"Created task: {task.id}")

        # List companies
        companies = await client.list_companies(limit=10)
        print(f"Found {len(companies)} companies")


if __name__ == "__main__":
    asyncio.run(main())