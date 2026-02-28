"""
Ploomes API - Sales CRM Client

Supports 17 API Actions:
- Search Deals
- Delete Deal
- Update Task
- Delete Product
- Search Tasks
- Complete Task
- Create Contact
- Create Product
- Update Contact
- Create Deal
- Delete Task
- Search Contacts
- Delete Contact
- Update Deal
- Search Products
- Create Task
- Update Product

Triggers:
- Received Webhook
"""

import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Contact:
    """Contact entity"""
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    company_id: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Deal:
    """Deal entity"""
    id: str
    title: str
    value: float
    stage_id: Optional[str] = None
    contact_id: Optional[str] = None
    status: Optional[str] = None
    close_date: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Task:
    """Task entity"""
    id: str
    title: str
    deal_id: Optional[str] = None
    contact_id: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None
    completed: bool = False
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Product:
    """Product entity"""
    id: str
    name: str
    description: Optional[str] = None
    price: float = 0.0
    currency: str = "BRL"
    sku: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


class PloomesClientError(Exception):
    """Base exception for Ploomes client errors"""
    pass


class PloomesRateLimitError(PloomesClientError):
    """Raised when rate limit is exceeded"""
    pass


class PloomesClient:
    """
    Ploomes API client for sales CRM.

    API Documentation: https://developers.ploomes.com/
    Uses API Key for authentication via Bearer token.
    """

    BASE_URL = "https://api.ploomes.com"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize Ploomes client.

        Args:
            api_key: API key for authentication
            base_url: Optional custom base URL
        """
        self.api_key = api_key
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None
        self._rate_limit_remaining = 100
        self._rate_limit_reset = 0

        logger = logging.getLogger("ploomes")
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        self._logger = logger

    async def __aenter__(self):
        headers = {
            "User-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=timeout
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with error handling and rate limiting."""
        await self._check_rate_limit()

        url = f"{self.base_url}{endpoint}"

        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                self._logger.debug(f"Request: {method} {url}")
                if data:
                    self._logger.debug(f"Data: {data}")

                async with self.session.request(
                    method,
                    url,
                    json=data,
                    params=params
                ) as response:
                    await self._update_rate_limit(response)

                    if response.status in [200, 201]:
                        result = await response.json()
                        self._logger.debug(f"Response: {result}")
                        return result

                    elif response.status == 204:
                        return {}

                    elif response.status == 401:
                        raise PloomesClientError("Authentication failed")

                    elif response.status == 403:
                        raise PloomesClientError("Forbidden - insufficient permissions")

                    elif response.status == 404:
                        raise PloomesClientError("Resource not found")

                    elif response.status == 422:
                        error_data = await response.json()
                        raise PloomesClientError(
                            f"Validation error: {error_data.get('Message', 'Unknown error')}"
                        )

                    elif response.status == 429:
                        await self._handle_rate_limit()
                        retry_count += 1
                        continue

                    else:
                        error_text = await response.text()
                        raise PloomesClientError(
                            f"API error {response.status}: {error_text}"
                        )

            except aiohttp.ClientError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise PloomesClientError(f"Network error: {str(e)}")
                await asyncio.sleep(2 ** retry_count)

    async def _check_rate_limit(self):
        """Check if rate limit allows request"""
        if self._rate_limit_remaining <= 1:
            now = int(datetime.now().timestamp())
            if now < self._rate_limit_reset:
                wait_time = self._rate_limit_reset - now
                self._logger.warning(f"Rate limit reached, waiting {wait_time}s")
                await asyncio.sleep(wait_time)

    async def _update_rate_limit(self, response: aiohttp.ClientResponse):
        """Update rate limit info from response headers"""
        remaining = response.headers.get("X-RateLimit-Remaining")
        reset = response.headers.get("X-RateLimit-Reset")

        if remaining:
            self._rate_limit_remaining = int(remaining)
        if reset:
            self._rate_limit_reset = int(reset)

    async def _handle_rate_limit(self):
        """Handle rate limit by waiting"""
        now = int(datetime.now().timestamp())
        wait_time = max(0, self._rate_limit_reset - now + 1)
        self._logger.warning(f"Rate limited, waiting {wait_time}s")
        await asyncio.sleep(wait_time)

    async def create_contact(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        job_title: Optional[str] = None,
        company_id: Optional[str] = None,
        extra_fields: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """Create a new contact."""
        data = {"Name": name}
        if email:
            data["Email"] = email
        if phone:
            data["PhoneNumber"] = phone
        if job_title:
            data["JobTitle"] = job_title
        if company_id:
            data["CompanyId"] = company_id
        if extra_fields:
            data["ExtraFields"] = extra_fields

        self._logger.info(f"Creating contact: {name}")
        result = await self._request("POST", "/Contacts", data=data)

        value = result.get("Value", {})
        return Contact(
            id=str(value.get("Id", "")),
            name=value.get("Name", ""),
            email=value.get("Email"),
            phone=value.get("PhoneNumber"),
            job_title=value.get("JobTitle"),
            company_id=str(value.get("CompanyId", "")) if value.get("CompanyId") else None,
            created_at=value.get("InsertDate", ""),
            updated_at=value.get("UpdateDate", "")
        )

    async def update_contact(
        self,
        contact_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        job_title: Optional[str] = None
    ) -> Contact:
        """Update an existing contact."""
        data = {}
        if name is not None:
            data["Name"] = name
        if email is not None:
            data["Email"] = email
        if phone is not None:
            data["PhoneNumber"] = phone
        if job_title is not None:
            data["JobTitle"] = job_title

        self._logger.info(f"Updating contact {contact_id}")
        result = await self._request("PATCH", f"/Contacts({contact_id})", data=data)

        value = result.get("Value", {})
        return Contact(
            id=str(value.get("Id", "")),
            name=value.get("Name", ""),
            email=value.get("Email"),
            phone=value.get("PhoneNumber"),
            job_title=value.get("JobTitle"),
            created_at=value.get("InsertDate", ""),
            updated_at=value.get("UpdateDate", "")
        )

    async def delete_contact(self, contact_id: str) -> None:
        """Delete a contact."""
        self._logger.info(f"Deleting contact {contact_id}")
        await self._request("DELETE", f"/Contacts({contact_id})")

    async def search_contacts(
        self,
        query: Optional[str] = None,
        filter_expression: Optional[str] = None,
        top: int = 50,
        skip: int = 0
    ) -> List[Contact]:
        """Search for contacts."""
        params = {"$top": top, "$skip": skip}
        if query:
            params["$search"] = query
        if filter_expression:
            params["$filter"] = filter_expression

        self._logger.info("Searching contacts")
        result = await self._request("GET", "/Contacts", params=params)

        contacts = []
        for item in result.get("Value", []):
            contacts.append(Contact(
                id=str(item.get("Id", "")),
                name=item.get("Name", ""),
                email=item.get("Email"),
                phone=item.get("PhoneNumber"),
                job_title=item.get("JobTitle"),
                company_id=str(item.get("CompanyId", "")) if item.get("CompanyId") else None,
                created_at=item.get("InsertDate", ""),
                updated_at=item.get("UpdateDate", "")
            ))

        return contacts

    async def create_deal(
        self,
        title: str,
        value: float,
        stage_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        close_date: Optional[str] = None
    ) -> Deal:
        """Create a new deal."""
        data = {
            "Title": title,
            "Value": value
        }
        if stage_id:
            data["StageId"] = stage_id
        if contact_id:
            data["ContactId"] = contact_id
        if close_date:
            data["ClosingDate"] = close_date

        self._logger.info(f"Creating deal: {title}")
        result = await self._request("POST", "/Deals", data=data)

        value_obj = result.get("Value", {})
        return Deal(
            id=str(value_obj.get("Id", "")),
            title=value_obj.get("Title", ""),
            value=float(value_obj.get("Value", 0)),
            stage_id=str(value_obj.get("StageId", "")) if value_obj.get("StageId") else None,
            contact_id=str(value_obj.get("ContactId", "")) if value_obj.get("ContactId") else None,
            status=value_obj.get("Status"),
            close_date=value_obj.get("ClosingDate"),
            created_at=value_obj.get("InsertDate", ""),
            updated_at=value_obj.get("UpdateDate", "")
        )

    async def update_deal(
        self,
        deal_id: str,
        title: Optional[str] = None,
        value: Optional[float] = None,
        stage_id: Optional[str] = None,
        contact_id: Optional[str] = None
    ) -> Deal:
        """Update an existing deal."""
        data = {}
        if title is not None:
            data["Title"] = title
        if value is not None:
            data["Value"] = value
        if stage_id is not None:
            data["StageId"] = stage_id
        if contact_id is not None:
            data["ContactId"] = contact_id

        self._logger.info(f"Updating deal {deal_id}")
        result = await self._request("PATCH", f"/Deals({deal_id})", data=data)

        value_obj = result.get("Value", {})
        return Deal(
            id=str(value_obj.get("Id", "")),
            title=value_obj.get("Title", ""),
            value=float(value_obj.get("Value", 0)),
            stage_id=str(value_obj.get("StageId", "")) if value_obj.get("StageId") else None,
            contact_id=str(value_obj.get("ContactId", "")) if value_obj.get("ContactId") else None,
            status=value_obj.get("Status"),
            close_date=value_obj.get("ClosingDate"),
            created_at=value_obj.get("InsertDate", ""),
            updated_at=value_obj.get("UpdateDate", "")
        )

    async def delete_deal(self, deal_id: str) -> None:
        """Delete a deal."""
        self._logger.info(f"Deleting deal {deal_id}")
        await self._request("DELETE", f"/Deals({deal_id})")

    async def search_deals(
        self,
        contact_id: Optional[str] = None,
        stage_id: Optional[str] = None,
        top: int = 50,
        skip: int = 0
    ) -> List[Deal]:
        """Search for deals."""
        params = {"$top": top, "$skip": skip}
        if contact_id:
            params["$filter"] = f"ContactId eq {contact_id}"
        if stage_id:
            filter_str = f"StageId eq {stage_id}"
            if "$filter" in params:
                params["$filter"] = f"{params['$filter']} and {filter_str}"
            else:
                params["$filter"] = filter_str

        self._logger.info("Searching deals")
        result = await self._request("GET", "/Deals", params=params)

        deals = []
        for item in result.get("Value", []):
            deals.append(Deal(
                id=str(item.get("Id", "")),
                title=item.get("Title", ""),
                value=float(item.get("Value", 0)),
                stage_id=str(item.get("StageId", "")) if item.get("StageId") else None,
                contact_id=str(item.get("ContactId", "")) if item.get("ContactId") else None,
                status=item.get("Status"),
                close_date=item.get("ClosingDate"),
                created_at=item.get("InsertDate", ""),
                updated_at=item.get("UpdateDate", "")
            ))

        return deals

    async def create_task(
        self,
        title: str,
        deal_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> Task:
        """Create a new task."""
        data = {"Title": title}
        if deal_id:
            data["DealId"] = deal_id
        if contact_id:
            data["ContactId"] = contact_id
        if due_date:
            data["DueDate"] = due_date

        self._logger.info(f"Creating task: {title}")
        result = await self._request("POST", "/Tasks", data=data)

        value_obj = result.get("Value", {})
        return Task(
            id=str(value_obj.get("Id", "")),
            title=value_obj.get("Title", ""),
            deal_id=str(value_obj.get("DealId", "")) if value_obj.get("DealId") else None,
            contact_id=str(value_obj.get("ContactId", "")) if value_obj.get("ContactId") else None,
            due_date=value_obj.get("DueDate"),
            status=value_obj.get("Status"),
            completed=value_obj.get("Completed", False),
            created_at=value_obj.get("InsertDate", ""),
            updated_at=value_obj.get("UpdateDate", "")
        )

    async def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        due_date: Optional[str] = None,
        status: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Task:
        """Update an existing task."""
        data = {}
        if title is not None:
            data["Title"] = title
        if due_date is not None:
            data["DueDate"] = due_date
        if status is not None:
            data["Status"] = status
        if completed is not None:
            data["Completed"] = completed

        self._logger.info(f"Updating task {task_id}")
        result = await self._request("PATCH", f"/Tasks({task_id})", data=data)

        value_obj = result.get("Value", {})
        return Task(
            id=str(value_obj.get("Id", "")),
            title=value_obj.get("Title", ""),
            deal_id=str(value_obj.get("DealId", "")) if value_obj.get("DealId") else None,
            contact_id=str(value_obj.get("ContactId", "")) if value_obj.get("ContactId") else None,
            due_date=value_obj.get("DueDate"),
            status=value_obj.get("Status"),
            completed=value_obj.get("Completed", False),
            created_at=value_obj.get("InsertDate", ""),
            updated_at=value_obj.get("UpdateDate", "")
        )

    async def complete_task(self, task_id: str) -> Task:
        """Mark a task as completed."""
        self._logger.info(f"Completing task {task_id}")
        return await self.update_task(task_id, completed=True, status="Completed")

    async def delete_task(self, task_id: str) -> None:
        """Delete a task."""
        self._logger.info(f"Deleting task {task_id}")
        await self._request("DELETE", f"/Tasks({task_id})")

    async def search_tasks(
        self,
        deal_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        status: Optional[str] = None,
        top: int = 50,
        skip: int = 0
    ) -> List[Task]:
        """Search for tasks."""
        params = {"$top": top, "$skip": skip}
        filters = []
        if deal_id:
            filters.append(f"DealId eq {deal_id}")
        if contact_id:
            filters.append(f"ContactId eq {contact_id}")
        if status:
            filters.append(f"Status eq '{status}'")
        if filters:
            params["$filter"] = " and ".join(filters)

        self._logger.info("Searching tasks")
        result = await self._request("GET", "/Tasks", params=params)

        tasks = []
        for item in result.get("Value", []):
            tasks.append(Task(
                id=str(item.get("Id", "")),
                title=item.get("Title", ""),
                deal_id=str(item.get("DealId", "")) if item.get("DealId") else None,
                contact_id=str(item.get("ContactId", "")) if item.get("ContactId") else None,
                due_date=item.get("DueDate"),
                status=item.get("Status"),
                completed=item.get("Completed", False),
                created_at=item.get("InsertDate", ""),
                updated_at=item.get("UpdateDate", "")
            ))

        return tasks

    async def create_product(
        self,
        name: str,
        price: float,
        description: Optional[str] = None,
        currency: str = "BRL",
        sku: Optional[str] = None
    ) -> Product:
        """Create a new product."""
        data = {
            "Name": name,
            "Price": price,
            "Currency": currency
        }
        if description:
            data["Description"] = description
        if sku:
            data["Sku"] = sku

        self._logger.info(f"Creating product: {name}")
        result = await self._request("POST", "/Products", data=data)

        value_obj = result.get("Value", {})
        return Product(
            id=str(value_obj.get("Id", "")),
            name=value_obj.get("Name", ""),
            description=value_obj.get("Description"),
            price=float(value_obj.get("Price", 0)),
            currency=value_obj.get("Currency", "BRL"),
            sku=value_obj.get("Sku"),
            created_at=value_obj.get("InsertDate", ""),
            updated_at=value_obj.get("UpdateDate", "")
        )

    async def update_product(
        self,
        product_id: str,
        name: Optional[str] = None,
        price: Optional[float] = None,
        description: Optional[str] = None,
        sku: Optional[str] = None
    ) -> Product:
        """Update an existing product."""
        data = {}
        if name is not None:
            data["Name"] = name
        if price is not None:
            data["Price"] = price
        if description is not None:
            data["Description"] = description
        if sku is not None:
            data["Sku"] = sku

        self._logger.info(f"Updating product {product_id}")
        result = await self._request("PATCH", f"/Products({product_id})", data=data)

        value_obj = result.get("Value", {})
        return Product(
            id=str(value_obj.get("Id", "")),
            name=value_obj.get("Name", ""),
            description=value_obj.get("Description"),
            price=float(value_obj.get("Price", 0)),
            currency=value_obj.get("Currency", "BRL"),
            sku=value_obj.get("Sku"),
            created_at=value_obj.get("InsertDate", ""),
            updated_at=value_obj.get("UpdateDate", "")
        )

    async def delete_product(self, product_id: str) -> None:
        """Delete a product."""
        self.__logger.info(f"Deleting product {product_id}")
        await self._request("DELETE", f"/Products({product_id})")

    async def search_products(
        self,
        query: Optional[str] = None,
        top: int = 50,
        skip: int = 0
    ) -> List[Product]:
        """Search for products."""
        params = {"$top": top, "$skip": skip}
        if query:
            params["$search"] = query

        self._logger.info("Searching products")
        result = await self._request("GET", "/Products", params=params)

        products = []
        for item in result.get("Value", []):
            products.append(Product(
                id=str(item.get("Id", "")),
                name=item.get("Name", ""),
                description=item.get("Description"),
                price=float(item.get("Price", 0)),
                currency=item.get("Currency", "BRL"),
                sku=item.get("Sku"),
                created_at=item.get("InsertDate", ""),
                updated_at=item.get("UpdateDate", "")
            ))

        return products