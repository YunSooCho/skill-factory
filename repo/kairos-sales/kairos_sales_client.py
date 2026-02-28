"""
Kairos Sales API - CRM Client

Supports deal, company, and customer management with tags, todos, and sales logs.

API Actions (23):
1. Add sales log to deal
2. Add tag to company
3. Create deal
4. Create company
5. Delete customer
6. Update deal
7. Search company
8. Update customer
9. Add tag to customer
10. Add todo to deal
11. Delete company tag
12. Get customer
13. Delete customer tag
14. Delete company
15. Add todo to customer
16. Get company
17. Delete deal
18. Search deal
19. Create customer
20. Add sales log to customer
21. Search customer
22. Get deal
23. Update company
"""

import aiohttp
import asyncio
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Deal:
    """Deal/Opportunity data model"""
    id: Optional[str] = None
    name: str = ""
    value: float = 0.0
    currency: str = "USD"
    stage: str = ""
    probability: int = 0
    expected_close_date: Optional[str] = None
    customer_id: Optional[str] = None
    company_id: Optional[str] = None
    description: str = ""
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Company:
    """Company/Account data model"""
    id: Optional[str] = None
    name: str = ""
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    address: Dict[str, str] = field(default_factory=dict)
    phone: Optional[str] = None
    description: str = ""
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Customer:
    """Customer/Contact data model"""
    id: Optional[str] = None
    first_name: str = ""
    last_name: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None
    company_id: Optional[str] = None
    title: Optional[str] = None
    description: str = ""
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class SalesLog:
    """Sales log/Note data model"""
    id: Optional[str] = None
    content: str = ""
    author_id: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Todo:
    """Todo/Task data model"""
    id: Optional[str] = None
    subject: str = ""
    due_date: Optional[str] = None
    priority: str = "medium"
    status: str = "open"
    assignee_id: Optional[str] = None
    description: str = ""
    created_at: Optional[str] = None
    completed_at: Optional[str] = None


class KairosSalesClient:
    """
    Kairos Sales CRM API client.

    API Documentation: https://lp.yoom.fun/apps/kairos-sales
    Authentication: API Key via header
    Protocol: HTTPS REST API
    """

    BASE_URL = "https://api.kairos-sales.com/v1"
    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 0.5  # seconds between requests

    def __init__(self, api_key: str):
        """
        Initialize Kairos Sales client.

        Args:
            api_key: Your Kairos Sales API key
        """
        self.api_key = api_key
        self.session = None
        self._last_request_time = 0

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _rate_limit(self):
        """Simple rate limiting by delaying between requests"""
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self.RATE_LIMIT_DELAY:
            await asyncio.sleep(self.RATE_LIMIT_DELAY - time_since_last_request)
        self._last_request_time = time.time()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make API request with retry logic and error handling.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters for GET requests
            json_data: JSON body for POST/PUT requests

        Returns:
            Response data as dictionary

        Raises:
            aiohttp.ClientError: If request fails after retries
            Exception: For API errors
        """
        await self._rate_limit()

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        url = f"{self.BASE_URL}{endpoint}"

        for attempt in range(self.MAX_RETRIES):
            try:
                async with self.session.request(
                    method,
                    url,
                    params=params,
                    json=json_data,
                    headers=headers
                ) as response:
                    data = await response.json()

                    if response.status in (200, 201):
                        return data
                    elif response.status == 401:
                        raise Exception("Invalid API key or unauthorized access")
                    elif response.status == 403:
                        raise Exception("Insufficient permissions")
                    elif response.status == 404:
                        raise Exception("Resource not found")
                    elif response.status == 429:
                        # Rate limit hit, wait and retry
                        retry_after = int(response.headers.get("Retry-After", 5))
                        await asyncio.sleep(retry_after)
                        continue
                    elif 400 <= response.status < 500:
                        raise Exception(f"Client error: {data.get('message', 'Unknown error')}")
                    else:
                        raise Exception(f"Server error: {response.status} - {data}")

            except aiohttp.ClientError as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise Exception(f"Request failed after {self.MAX_RETRIES} attempts: {str(e)}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

    # ==================== Deal Operations ====================

    async def create_deal(self, deal: Deal) -> Deal:
        """Create a new deal (案件を作成)"""
        deal_data = {
            "name": deal.name,
            "value": deal.value,
            "currency": deal.currency,
            "stage": deal.stage,
            "probability": deal.probability,
            "expected_close_date": deal.expected_close_date,
            "customer_id": deal.customer_id,
            "company_id": deal.company_id,
            "description": deal.description,
            "custom_fields": deal.custom_fields
        }

        response = await self._request("POST", "/deals", json_data=deal_data)
        return Deal(**response.get("data", {}))

    async def get_deal(self, deal_id: str) -> Deal:
        """Get deal by ID (案件を取得)"""
        response = await self._request("GET", f"/deals/{deal_id}")
        return Deal(**response.get("data", {}))

    async def update_deal(self, deal_id: str, deal: Deal) -> Deal:
        """Update existing deal (案件を更新)"""
        response = await self._request("PUT", f"/deals/{deal_id}", json_data={
            "name": deal.name,
            "value": deal.value,
            "currency": deal.currency,
            "stage": deal.stage,
            "probability": deal.probability,
            "expected_close_date": deal.expected_close_date,
            "customer_id": deal.customer_id,
            "company_id": deal.company_id,
            "description": deal.description,
            "custom_fields": deal.custom_fields
        })
        return Deal(**response.get("data", {}))

    async def delete_deal(self, deal_id: str) -> bool:
        """Delete deal (案件を削除)"""
        await self._request("DELETE", f"/deals/{deal_id}")
        return True

    async def search_deals(
        self,
        query: Optional[str] = None,
        customer_id: Optional[str] = None,
        company_id: Optional[str] = None,
        stage: Optional[str] = None,
        limit: int = 50
    ) -> List[Deal]:
        """Search deals (案件を検索)"""
        params = {"limit": limit}
        if query:
            params["q"] = query
        if customer_id:
            params["customer_id"] = customer_id
        if company_id:
            params["company_id"] = company_id
        if stage:
            params["stage"] = stage

        response = await self._request("GET", "/deals", params=params)
        return [Deal(**item) for item in response.get("data", [])]

    async def add_deal_sales_log(self, deal_id: str, log: SalesLog) -> SalesLog:
        """Add sales log to deal (案件に営業ログを追加)"""
        response = await self._request("POST", f"/deals/{deal_id}/sales-logs", json_data={
            "content": log.content
        })
        return SalesLog(**response.get("data", {}))

    async def add_deal_todo(self, deal_id: str, todo: Todo) -> Todo:
        """Add todo to deal (案件にToDoを追加)"""
        response = await self._request("POST", f"/deals/{deal_id}/todos", json_data={
            "subject": todo.subject,
            "due_date": todo.due_date,
            "priority": todo.priority,
            "assignee_id": todo.assignee_id,
            "description": todo.description
        })
        return Todo(**response.get("data", {}))

    # ==================== Company Operations ====================

    async def create_company(self, company: Company) -> Company:
        """Create a new company (会社を作成)"""
        company_data = {
            "name": company.name,
            "website": company.website,
            "industry": company.industry,
            "size": company.size,
            "address": company.address,
            "phone": company.phone,
            "description": company.description,
            "custom_fields": company.custom_fields
        }

        response = await self._request("POST", "/companies", json_data=company_data)
        return Company(**response.get("data", {}))

    async def get_company(self, company_id: str) -> Company:
        """Get company by ID (会社を取得)"""
        response = await self._request("GET", f"/companies/{company_id}")
        return Company(**response.get("data", {}))

    async def update_company(self, company_id: str, company: Company) -> Company:
        """Update existing company (会社を更新)"""
        response = await self._request("PUT", f"/companies/{company_id}", json_data={
            "name": company.name,
            "website": company.website,
            "industry": company.industry,
            "size": company.size,
            "address": company.address,
            "phone": company.phone,
            "description": company.description,
            "custom_fields": company.custom_fields
        })
        return Company(**response.get("data", {}))

    async def delete_company(self, company_id: str) -> bool:
        """Delete company (会社を削除)"""
        await self._request("DELETE", f"/companies/{company_id}")
        return True

    async def search_companies(
        self,
        query: Optional[str] = None,
        industry: Optional[str] = None,
        limit: int = 50
    ) -> List[Company]:
        """Search companies (会社を検索)"""
        params = {"limit": limit}
        if query:
            params["q"] = query
        if industry:
            params["industry"] = industry

        response = await self._request("GET", "/companies", params=params)
        return [Company(**item) for item in response.get("data", [])]

    async def add_company_tag(self, company_id: str, tag: str) -> List[str]:
        """Add tag to company (会社にタグを追加)"""
        response = await self._request("POST", f"/companies/{company_id}/tags", json_data={
            "tag": tag
        })
        return response.get("data", {}).get("tags", [])

    async def delete_company_tag(self, company_id: str, tag: str) -> List[str]:
        """Delete tag from company (会社のタグを削除)"""
        response = await self._request("DELETE", f"/companies/{company_id}/tags/{tag}")
        return response.get("data", {}).get("tags", [])

    # ==================== Customer Operations ====================

    async def create_customer(self, customer: Customer) -> Customer:
        """Create a new customer (顧客を作成)"""
        customer_data = {
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
            "company_id": customer.company_id,
            "title": customer.title,
            "description": customer.description,
            "custom_fields": customer.custom_fields
        }

        response = await self._request("POST", "/customers", json_data=customer_data)
        return Customer(**response.get("data", {}))

    async def get_customer(self, customer_id: str) -> Customer:
        """Get customer by ID (顧客を取得)"""
        response = await self._request("GET", f"/customers/{customer_id}")
        return Customer(**response.get("data", {}))

    async def update_customer(self, customer_id: str, customer: Customer) -> Customer:
        """Update existing customer (顧客を更新)"""
        response = await self._request("PUT", f"/customers/{customer_id}", json_data={
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
            "company_id": customer.company_id,
            "title": customer.title,
            "description": customer.description,
            "custom_fields": customer.custom_fields
        })
        return Customer(**response.get("data", {}))

    async def delete_customer(self, customer_id: str) -> bool:
        """Delete customer (顧客を削除)"""
        await self._request("DELETE", f"/customers/{customer_id}")
        return True

    async def search_customers(
        self,
        query: Optional[str] = None,
        company_id: Optional[str] = None,
        email: Optional[str] = None,
        limit: int = 50
    ) -> List[Customer]:
        """Search customers (顧客を検索)"""
        params = {"limit": limit}
        if query:
            params["q"] = query
        if company_id:
            params["company_id"] = company_id
        if email:
            params["email"] = email

        response = await self._request("GET", "/customers", params=params)
        return [Customer(**item) for item in response.get("data", [])]

    async def add_customer_tag(self, customer_id: str, tag: str) -> List[str]:
        """Add tag to customer (顧客にタグを追加)"""
        response = await self._request("POST", f"/customers/{customer_id}/tags", json_data={
            "tag": tag
        })
        return response.get("data", {}).get("tags", [])

    async def delete_customer_tag(self, customer_id: str, tag: str) -> List[str]:
        """Delete tag from customer (顧客のタグを削除)"""
        response = await self._request("DELETE", f"/customers/{customer_id}/tags/{tag}")
        return response.get("data", {}).get("tags", [])

    async def add_customer_sales_log(self, customer_id: str, log: SalesLog) -> SalesLog:
        """Add sales log to customer (顧客に営業ログを追加)"""
        response = await self._request("POST", f"/customers/{customer_id}/sales-logs", json_data={
            "content": log.content
        })
        return SalesLog(**response.get("data", {}))

    async def add_customer_todo(self, customer_id: str, todo: Todo) -> Todo:
        """Add todo to customer (顧客にToDoを追加)"""
        response = await self._request("POST", f"/customers/{customer_id}/todos", json_data={
            "subject": todo.subject,
            "due_date": todo.due_date,
            "priority": todo.priority,
            "assignee_id": todo.assignee_id,
            "description": todo.description
        })
        return Todo(**response.get("data", {}))


# ==================== Example Usage ====================

async def main():
    """Example usage of Kairos Sales client"""

    # Replace with your actual API key
    api_key = "your_kairos_sales_api_key"

    async with KairosSalesClient(api_key=api_key) as client:
        # Create a company
        company = Company(
            name="Example Corporation",
            website="https://example.com",
            industry="Technology",
            size="51-200",
            address={
                "street": "123 Business St",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94105",
                "country": "USA"
            },
            phone="+1-555-1234"
        )
        created_company = await client.create_company(company)
        print(f"Created company: {created_company.name} (ID: {created_company.id})")

        # Add a tag to the company
        tags = await client.add_company_tag(created_company.id, "Enterprise")
        print(f"Company tags: {tags}")

        # Create a customer
        customer = Customer(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="+1-555-5678",
            company_id=created_company.id,
            title="CTO"
        )
        created_customer = await client.create_customer(customer)
        print(f"Created customer: {created_customer.first_name} {created_customer.last_name}")

        # Create a deal
        deal = Deal(
            name="Software License Deal",
            value=50000.0,
            currency="USD",
            stage="Proposal",
            probability=60,
            expected_close_date="2024-04-30",
            customer_id=created_customer.id,
            company_id=created_company.id,
            description="Enterprise software license agreement"
        )
        created_deal = await client.create_deal(deal)
        print(f"Created deal: {created_deal.name} (${created_deal.value})")

        # Add sales log to deal
        log = await client.add_deal_sales_log(
            created_deal.id,
            SalesLog(content="Initial discovery call completed. Customer interested in features X and Y.")
        )
        print(f"Added sales log to deal: {log.id}")

        # Add todo to deal
        todo = await client.add_deal_todo(
            created_deal.id,
            Todo(
                subject="Send proposal",
                due_date="2024-03-01",
                priority="high"
            )
        )
        print(f"Added todo to deal: {todo.subject}")

        # Search deals
        deals = await client.search_deals(customer_id=created_customer.id)
        print(f"Found {len(deals)} deals for customer")


if __name__ == "__main__":
    asyncio.run(main())