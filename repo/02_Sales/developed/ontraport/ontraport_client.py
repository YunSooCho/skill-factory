"""
Ontraport API - CRM and Marketing Automation Client

Supports contacts, tasks, products, and transactions management.

API Actions (14):
1. Search Contact
2. Create Task Message
3. Create Contact
4. Create Product
5. Update Contact
6. Search Transaction
7. Search Product
8. Add Task to Contact
9. Get Transaction
10. Get Contact
11. Get Product
12. Delete Contact
13. Delete Product
14. Update Product
"""

import aiohttp
import asyncio
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class Contact:
    """Contact data model"""
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    address: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Product:
    """Product data model"""
    id: Optional[int] = None
    product_name: str = ""
    description: str = ""
    price: float = 0.0
    sku: Optional[str] = None
    quantity: int = 0
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Transaction:
    """Transaction data model"""
    id: Optional[int] = None
    contact_id: Optional[int] = None
    product_id: Optional[int] = None
    amount: float = 0.0
    currency: str = "USD"
    status: str = "pending"
    transaction_date: Optional[str] = None
    payment_method: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Task:
    """Task data model"""
    id: Optional[int] = None
    contact_id: int
    title: str = ""
    description: str = ""
    due_date: Optional[str] = None
    status: str = "pending"
    assigned_to: Optional[int] = None
    created_at: Optional[str] = None


class OntraportClient:
    """
    Ontraport API client for CRM and marketing automation.

    API Documentation: http://api.ontraport.com/doc/
    Authentication: API ID and Key
    Protocol: HTTPS REST API
    """

    BASE_URL = "https://api.ontraport.com/1"
    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 0.5  # seconds between requests

    def __init__(self, api_id: str, api_key: str):
        """
        Initialize Ontraport client.

        Args:
            api_id: Your Ontraport API ID
            api_key: Your Ontraport API key
        """
        self.api_id = api_id
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
        """Simple rate limiting"""
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
        """Make API request with retry logic and error handling"""
        await self._rate_limit()

        # Ontraport uses API ID and Key in body or params
        auth_params = {
            "appid": self.api_id,
            "key": self.api_key
        }

        if params:
            params.update(auth_params)
        else:
            params = auth_params

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        url = f"{self.BASE_URL}{endpoint}"

        for attempt in range(self.MAX_RETRIES):
            try:
                if json_data:
                    json_data.update(auth_params)

                async with self.session.request(
                    method,
                    url,
                    params=params,
                    json=json_data,
                    headers=headers
                ) as response:
                    data = await response.json()

                    if response.status in (200, 201, 204):
                        return data if data else {}
                    elif response.status == 401:
                        raise Exception("Invalid API credentials")
                    elif response.status == 403:
                        raise Exception("Insufficient permissions")
                    elif response.status == 404:
                        raise Exception("Resource not found")
                    elif response.status == 429:
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
                await asyncio.sleep(2 ** attempt)

    # ==================== Contact Operations ====================

    async def create_contact(self, contact: Contact) -> Contact:
        """Create a new contact (Create Contact)"""
        contact_data = {
            "objectID": 0,  # Contacts object type
            "firstname": contact.first_name,
            "lastname": contact.last_name,
            "email": contact.email,
            "office_phone": contact.phone,
            "company": contact.company,
            "title": contact.job_title,
            "billing_address": contact.address.get("street"),
            "billing_city": contact.address.get("city"),
            "billing_state": contact.address.get("state"),
            "billing_zip": contact.address.get("zip"),
            "billing_country": contact.address.get("country"),
            "tag": ",".join(contact.tags) if contact.tags else None
        }

        contact_data = {k: v for k, v in contact_data.items() if v is not None}

        response = await self._request("POST", "/objects", json_data=contact_data)
        contact_id = response.get("data", {}).get("info", {}).get("id")
        if contact_id:
            contact.id = contact_id
        return contact

    async def get_contact(self, contact_id: int) -> Contact:
        """Get contact by ID (Get Contact)"""
        params = {
            "objectID": 0,  # Contacts object type
            "id": contact_id
        }

        response = await self._request("GET", "/object", params=params)
        data = response.get("data", {})
        return Contact(**self._map_contact_data(data))

    async def update_contact(self, contact_id: int, contact: Contact) -> Contact:
        """Update existing contact (Update Contact)"""
        contact_data = {
            "objectID": 0,  # Contacts object type
            "id": contact_id,
            "firstname": contact.first_name,
            "lastname": contact.last_name,
            "office_phone": contact.phone,
            "company": contact.company,
            "title": contact.job_title
        }

        contact_data = {k: v for k, v in contact_data.items() if v is not None}

        await self._request("PUT", f"/objects/{contact_id}", json_data=contact_data)
        return Contact(id=contact_id, **contact_data)

    async def delete_contact(self, contact_id: int) -> bool:
        """Delete contact (Delete Contact)"""
        params = {"objectID": 0}
        await self._request("DELETE", f"/objects/{contact_id}", params=params)
        return True

    async def search_contact(
        self,
        search: Optional[str] = None,
        condition: Optional[Dict] = None,
        limit: int = 50
    ) -> List[Contact]:
        """Search contacts (Search Contact)"""
        params = {
            "objectID": 0,  # Contacts object type
            "range": f"0-{limit-1}"
        }

        if search:
            params["search"] = search
        if condition:
            params["condition"] = str(condition)

        response = await self._request("GET", "/objects", params=params)
        contacts_data = response.get("data", [])
        return [Contact(**self._map_contact_data(c)) for c in contacts_data]

    def _map_contact_data(self, data: Dict) -> Dict:
        """Map Ontraport contact data to our Contact model"""
        return {
            "id": data.get("id"),
            "first_name": data.get("firstname", ""),
            "last_name": data.get("lastname", ""),
            "email": data.get("email"),
            "phone": data.get("office_phone"),
            "company": data.get("company"),
            "job_title": data.get("title"),
            "address": {
                "street": data.get("billing_address"),
                "city": data.get("billing_city"),
                "state": data.get("billing_state"),
                "zip": data.get("billing_zip"),
                "country": data.get("billing_country")
            },
            "tags": data.get("tag", "").split(",") if data.get("tag") else [],
            "created_at": data.get("date_added"),
            "updated_at": data.get("date_update")
        }

    # ==================== Product Operations ====================

    async def create_product(self, product: Product) -> Product:
        """Create a new product (Create Product)"""
        product_data = {
            "objectID": 14,  # Products object type
            "name": product.product_name,
            "description": product.description,
            "price": product.price,
            "sku": product.sku,
            "quantity": product.quantity,
            "status": "Active" if product.is_active else "Inactive"
        }

        product_data = {k: v for k, v in product_data.items() if v is not None}

        response = await self._request("POST", "/objects", json_data=product_data)
        product_id = response.get("data", {}).get("info", {}).get("id")
        if product_id:
            product.id = product_id
        return product

    async def get_product(self, product_id: int) -> Product:
        """Get product by ID (Get Product)"""
        params = {
            "objectID": 14,  # Products object type
            "id": product_id
        }

        response = await self._request("GET", "/object", params=params)
        data = response.get("data", {})
        return Product(**self._map_product_data(data))

    async def update_product(self, product_id: int, product: Product) -> Product:
        """Update existing product (Update Product)"""
        product_data = {
            "objectID": 14,  # Products object type
            "id": product_id,
            "name": product.product_name,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
            "status": "Active" if product.is_active else "Inactive"
        }

        product_data = {k: v for k, v in product_data.items() if v is not None}

        await self._request("PUT", f"/objects/{product_id}", json_data=product_data)
        return Product(id=product_id, **product_data)

    async def delete_product(self, product_id: int) -> bool:
        """Delete product (Delete Product)"""
        params = {"objectID": 14}
        await self._request("DELETE", f"/objects/{product_id}", params=params)
        return True

    async def search_product(
        self,
        search: Optional[str] = None,
        limit: int = 50
    ) -> List[Product]:
        """Search products (Search Product)"""
        params = {
            "objectID": 14,  # Products object type
            "range": f"0-{limit-1}"
        }

        if search:
            params["search"] = search

        response = await self._request("GET", "/objects", params=params)
        products_data = response.get("data", [])
        return [Product(**self._map_product_data(p)) for p in products_data]

    def _map_product_data(self, data: Dict) -> Dict:
        """Map Ontraport product data to our Product model"""
        return {
            "id": data.get("id"),
            "product_name": data.get("name", ""),
            "description": data.get("description", ""),
            "price": float(data.get("price", 0.0)),
            "sku": data.get("sku"),
            "quantity": int(data.get("quantity", 0)),
            "is_active": data.get("status") == "Active",
            "created_at": data.get("date_added"),
            "updated_at": data.get("date_update")
        }

    # ==================== Transaction Operations ====================

    async def get_transaction(self, transaction_id: int) -> Transaction:
        """Get transaction by ID (Get Transaction)"""
        params = {
            "objectID": 15,  # Transactions object type
            "id": transaction_id
        }

        response = await self._request("GET", "/object", params=params)
        data = response.get("data", {})
        return Transaction(**self._map_transaction_data(data))

    async def search_transaction(
        self,
        contact_id: Optional[int] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Transaction]:
        """Search transactions (Search Transaction)"""
        params = {
            "objectID": 15,  # Transactions object type
            "range": f"0-{limit-1}"
        }

        if contact_id:
            params["search"] = f"contact={contact_id}"
        if status:
            params["status"] = status

        response = await self._request("GET", "/objects", params=params)
        transactions_data = response.get("data", [])
        return [Transaction(**self._map_transaction_data(t)) for t in transactions_data]

    def _map_transaction_data(self, data: Dict) -> Dict:
        """Map Ontraport transaction data to our Transaction model"""
        return {
            "id": data.get("id"),
            "contact_id": data.get("contact"),
            "product_id": data.get("product"),
            "amount": float(data.get("amount", 0.0)),
            "currency": data.get("currency", "USD"),
            "status": data.get("status", "pending"),
            "transaction_date": data.get("date"),
            "payment_method": data.get("payment_method"),
            "created_at": data.get("date_add")
        }

    # ==================== Task Operations ====================

    async def create_task_message(self, task: Task) -> Task:
        """Create task message (Create Task Message)"""
        task_data = {
            "objectID": 5,  # Tasks/Tasks object type
            "contact_id": task.contact_id,
            "name": task.title,
            "description": task.description,
            "due_date": task.due_date,
            "status": task.status,
            "assigned_to": task.assigned_to
        }

        task_data = {k: v for k, v in task_data.items() if v is not None}

        response = await self._request("POST", "/objects", json_data=task_data)
        task_id = response.get("data", {}).get("info", {}).get("id")
        if task_id:
            task.id = task_id
        return task

    async def add_task_to_contact(self, task: Task) -> Task:
        """Add task to contact (Add Task to Contact)"""
        return await self.create_task_message(task)


# ==================== Example Usage ====================

async def main():
    """Example usage of Ontraport client"""

    api_id = "your_api_id"
    api_key = "your_api_key"

    async with OntraportClient(api_id=api_id, api_key=api_key) as client:
        # Create contact
        contact = Contact(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            company="Example Corp"
        )
        created_contact = await client.create_contact(contact)
        print(f"Created contact: {created_contact.first_name} {created_contact.last_name}")

        # Create product
        product = Product(
            product_name="Premium Plan",
            price=99.99,
            sku="PREM-001"
        )
        created_product = await client.create_product(product)
        print(f"Created product: {created_product.product_name}")

        # Create task
        task = Task(
            contact_id=created_contact.id,
            title="Follow up call",
            description="Schedule follow-up call"
        )
        created_task = await client.create_task_message(task)
        print(f"Created task: {created_task.title}")


if __name__ == "__main__":
    asyncio.run(main())