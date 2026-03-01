"""
Keap API - Marketing & Sales Automation Client

Supports contacts, tasks, notes, products, and sales opportunities management.
Part of the Yoom automation infrastructure.

API Actions (25):
1. Update Sales Opportunity
2. Create Product
3. Delete Note
4. Get Notes
5. Search Contacts
6. Create Task
7. Delete Contact
8. Update Note
9. Delete Task
10. Update Product
11. Create Note
12. Create Contact
13. Create Sales Opportunity
14. Get Product
15. Search Products
16. Get Task
17. Search Opportunities
18. Remove Tag from Contacts
19. Delete Product
20. Apply Tag to Contacts
21. Update Contact
22. Search Tasks
23. Update Task
24. Get Sales Opportunity
25. Get Contact
"""

import aiohttp
import asyncio
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Contact:
    """Contact data model"""
    id: Optional[str] = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: Optional[str] = None
    website: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    street1: Optional[str] = None
    street2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    date_created: Optional[str] = None
    last_updated: Optional[str] = None


@dataclass
class Task:
    """Task data model"""
    id: Optional[str] = None
    title: str = ""
    description: str = ""
    status: str = "open"  # open, completed
    priority: str = "medium"  # low, medium, high
    due_date: Optional[str] = None
    contact_id: Optional[str] = None
    assigned_user_id: Optional[str] = None
    completed_date: Optional[str] = None
    date_created: Optional[str] = None
    last_updated: Optional[str] = None


@dataclass
class Note:
    """Note data model"""
    id: Optional[str] = None
    title: str = ""
    description: str = ""
    contact_id: Optional[str] = None
    user_id: Optional[str] = None
    date_created: Optional[str] = None
    last_updated: Optional[str] = None


@dataclass
class Product:
    """Product data model"""
    id: Optional[str] = None
    product_name: str = ""
    sku: str = ""
    price: float = 0.0
    description: str = ""
    short_description: str = ""
    taxable: bool = False
    weight: float = 0.0
    is_active: bool = True
    date_created: Optional[str] = None
    last_updated: Optional[str] = None


@dataclass
class SalesOpportunity:
    """Sales Opportunity data model"""
    id: Optional[str] = None
    opportunity_title: str = ""
    estimated_value: float = 0.0
    probability: int = 0
    stage_id: Optional[str] = None
    stage_name: str = ""
    contact_id: Optional[str] = None
    user_id: Optional[str] = None
    projected_close_date: Optional[str] = None
    notes: str = ""
    date_created: Optional[str] = None
    last_updated: Optional[str] = None


class KeapClient:
    """
    Keap (formerly Infusionsoft) API client for marketing and sales automation.

    API Documentation: https://developer.keap.com/
    Authentication: OAuth 2.0 or API Key
    Protocol: HTTPS REST API
    """

    BASE_URL = "https://api.infusionsoft.com/crm/rest/v1"
    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 0.5  # seconds between requests

    def __init__(self, access_token: str):
        """
        Initialize Keap client.

        Args:
            access_token: OAuth access token or API key
        """
        self.access_token = access_token
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
            "Authorization": f"Bearer {self.access_token}",
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

                    if response.status in (200, 201, 204):
                        return data
                    elif response.status == 401:
                        raise Exception("Invalid access token or unauthorized access")
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

    # ==================== Contact Operations ====================

    async def create_contact(self, contact: Contact) -> Contact:
        """Create a new contact (Create Contact)"""
        contact_data = {
            "given_name": contact.first_name,
            "family_name": contact.last_name,
            "email_addresses": [{"email": contact.email, "field": "EMAIL1"}],
            "phone_numbers": [{"number": contact.phone, "field": "PHONE1"}] if contact.phone else [],
            "website": contact.website,
            "company": {"name": contact.company} if contact.company else None,
            "job_title": contact.job_title,
            "addresses": [{
                "line1": contact.street1,
                "line2": contact.street2,
                "city": contact.city,
                "region": contact.state,
                "postal_code": contact.postal_code,
                "country_code": contact.country,
                "field": "BILLING"
            }] if contact.city else None
        }

        # Remove None values
        contact_data = {k: v for k, v in contact_data.items() if v is not None}

        response = await self._request("POST", "/contacts", json_data=contact_data)
        return Contact(**self._map_contact_data(response))

    async def get_contact(self, contact_id: str) -> Contact:
        """Get contact by ID (Get Contact)"""
        response = await self._request("GET", f"/contacts/{contact_id}")
        return Contact(**self._map_contact_data(response))

    async def update_contact(self, contact_id: str, contact: Contact) -> Contact:
        """Update existing contact (Update Contact)"""
        contact_data = {
            "given_name": contact.first_name,
            "family_name": contact.last_name,
            "phone_numbers": [{"number": contact.phone, "field": "PHONE1"}] if contact.phone else [],
            "website": contact.website,
            "company": {"name": contact.company} if contact.company else None,
            "job_title": contact.job_title,
            "addresses": [{
                "line1": contact.street1,
                "line2": contact.street2,
                "city": contact.city,
                "region": contact.state,
                "postal_code": contact.postal_code,
                "country_code": contact.country,
                "field": "BILLING"
            }] if contact.city else None
        }

        # Remove None values
        contact_data = {k: v for k, v in contact_data.items() if v is not None}

        response = await self._request("PATCH", f"/contacts/{contact_id}", json_data=contact_data)
        return Contact(**self._map_contact_data(response))

    async def delete_contact(self, contact_id: str) -> bool:
        """Delete contact (Delete Contact)"""
        await self._request("DELETE", f"/contacts/{contact_id}")
        return True

    async def search_contacts(
        self,
        query: Optional[str] = None,
        email: Optional[str] = None,
        limit: int = 50
    ) -> List[Contact]:
        """Search contacts (Search Contacts)"""
        params = {"limit": limit, "order": "date_created DESC"}

        if email:
            params["email"] = email
        elif query:
            params["filter"] = f"given_name:*{query}* OR family_name:*{query}* OR company:*{query}*"

        response = await self._request("GET", "/contacts", params=params)
        contacts = response.get("contacts", [])
        return [Contact(**self._map_contact_data(c)) for c in contacts]

    async def apply_tag_to_contacts(self, contact_ids: List[str], tag_id: str) -> bool:
        """Apply tag to contacts (Apply Tag to Contacts)"""
        for contact_id in contact_ids:
            await self._request("POST", f"/contacts/{contact_id}/tags", json_data={"tag_id": tag_id})
        return True

    async def remove_tag_from_contacts(self, contact_ids: List[str], tag_id: str) -> bool:
        """Remove tag from contacts (Remove Tag from Contacts)"""
        for contact_id in contact_ids:
            await self._request("DELETE", f"/contacts/{contact_id}/tags/{tag_id}")
        return True

    def _map_contact_data(self, data: Dict) -> Dict:
        """Map Keap contact data to our Contact model"""
        email_addresses = data.get("email_addresses", [])
        phone_numbers = data.get("phone_numbers", [])
        addresses = data.get("addresses", [])
        tags = data.get("tag_ids", [])
        company_data = data.get("company", {})

        return {
            "id": str(data.get("id")) if data.get("id") else None,
            "first_name": data.get("given_name", ""),
            "last_name": data.get("family_name", ""),
            "email": email_addresses[0]["email"] if email_addresses else "",
            "phone": phone_numbers[0]["number"] if phone_numbers else None,
            "website": data.get("website"),
            "company": company_data.get("name", ""),
            "job_title": data.get("job_title"),
            "street1": addresses[0]["line1"] if addresses and "line1" in addresses[0] else None,
            "street2": addresses[0]["line2"] if addresses and "line2" in addresses[0] else None,
            "city": addresses[0]["city"] if addresses and addresses[0].get("city") else None,
            "state": addresses[0]["region"] if addresses and addresses[0].get("region") else None,
            "postal_code": addresses[0]["postal_code"] if addresses and addresses[0].get("postal_code") else None,
            "country": addresses[0]["country_code"] if addresses and addresses[0].get("country_code") else None,
            "tags": [str(t) for t in tags],
            "date_created": data.get("date_created"),
            "last_updated": data.get("last_updated")
        }

    # ==================== Task Operations ====================

    async def create_task(self, task: Task) -> Task:
        """Create a new task (Create Task)"""
        task_data = {
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date,
            "contact_id": task.contact_id,
            "user_id": task.assigned_user_id
        }

        # Remove None values
        task_data = {k: v for k, v in task_data.items() if v is not None}

        response = await self._request("POST", "/tasks", json_data=task_data)
        return Task(**self._map_task_data(response))

    async def get_task(self, task_id: str) -> Task:
        """Get task by ID (Get Task)"""
        response = await self._request("GET", f"/tasks/{task_id}")
        return Task(**self._map_task_data(response))

    async def update_task(self, task_id: str, task: Task) -> Task:
        """Update existing task (Update Task)"""
        task_data = {
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date,
            "user_id": task.assigned_user_id
        }

        # Remove None values
        task_data = {k: v for k, v in task_data.items() if v is not None}

        response = await self._request("PATCH", f"/tasks/{task_id}", json_data=task_data)
        return Task(**self._map_task_data(response))

    async def delete_task(self, task_id: str) -> bool:
        """Delete task (Delete Task)"""
        await self._request("DELETE", f"/tasks/{task_id}")
        return True

    async def search_tasks(
        self,
        contact_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Task]:
        """Search tasks (Search Tasks)"""
        params = {"limit": limit, "order": "due_date ASC"}

        if contact_id:
            params["contact_id"] = contact_id
        if status:
            params["status"] = status

        response = await self._request("GET", "/tasks", params=params)
        tasks = response.get("tasks", [])
        return [Task(**self._map_task_data(t)) for t in tasks]

    def _map_task_data(self, data: Dict) -> Dict:
        """Map Keap task data to our Task model"""
        return {
            "id": str(data.get("id")) if data.get("id") else None,
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "status": data.get("status", "open"),
            "priority": data.get("priority", "medium"),
            "due_date": data.get("due_date"),
            "contact_id": str(data.get("contact_id")) if data.get("contact_id") else None,
            "assigned_user_id": str(data.get("user_id")) if data.get("user_id") else None,
            "completed_date": data.get("completed_date"),
            "date_created": data.get("date_created"),
            "last_updated": data.get("last_updated")
        }

    # ==================== Note Operations ====================

    async def create_note(self, note: Note) -> Note:
        """Create a new note (Create Note)"""
        note_data = {
            "title": note.title,
            "description": note.description,
            "contact_id": note.contact_id
        }

        # Remove None values
        note_data = {k: v for k, v in note_data.items() if v is not None}

        response = await self._request("POST", "/notes", json_data=note_data)
        return Note(**self._map_note_data(response))

    async def get_note(self, note_id: str) -> Note:
        """Get note by ID"""
        response = await self._request("GET", f"/notes/{note_id}")
        return Note(**self._map_note_data(response))

    async def get_notes(self, contact_id: Optional[str] = None, limit: int = 50) -> List[Note]:
        """Get notes (Get Notes)"""
        params = {"limit": limit, "order": "date_created DESC"}

        if contact_id:
            params["contact_id"] = contact_id

        response = await self._request("GET", "/notes", params=params)
        notes = response.get("notes", [])
        return [Note(**self._map_note_data(n)) for n in notes]

    async def update_note(self, note_id: str, note: Note) -> Note:
        """Update existing note (Update Note)"""
        note_data = {
            "title": note.title,
            "description": note.description
        }

        # Remove None values
        note_data = {k: v for k, v in note_data.items() if v is not None}

        response = await self._request("PATCH", f"/notes/{note_id}", json_data=note_data)
        return Note(**self._map_note_data(response))

    async def delete_note(self, note_id: str) -> bool:
        """Delete note (Delete Note)"""
        await self._request("DELETE", f"/notes/{note_id}")
        return True

    def _map_note_data(self, data: Dict) -> Dict:
        """Map Keap note data to our Note model"""
        return {
            "id": str(data.get("id")) if data.get("id") else None,
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "contact_id": str(data.get("contact_id")) if data.get("contact_id") else None,
            "user_id": str(data.get("user_id")) if data.get("user_id") else None,
            "date_created": data.get("date_created"),
            "last_updated": data.get("last_updated")
        }

    # ==================== Product Operations ====================

    async def create_product(self, product: Product) -> Product:
        """Create a new product (Create Product)"""
        product_data = {
            "product_name": product.product_name,
            "sku": product.sku,
            "price": product.price,
            "description": product.description,
            "short_description": product.short_description,
            "taxable": product.taxable,
            "weight": product.weight,
            "status": product.is_active
        }

        response = await self._request("POST", "/products", json_data=product_data)
        return Product(**self._map_product_data(response))

    async def get_product(self, product_id: str) -> Product:
        """Get product by ID (Get Product)"""
        response = await self._request("GET", f"/products/{product_id}")
        return Product(**self._map_product_data(response))

    async def update_product(self, product_id: str, product: Product) -> Product:
        """Update existing product (Update Product)"""
        product_data = {
            "product_name": product.product_name,
            "price": product.price,
            "description": product.description,
            "short_description": product.short_description,
            "taxable": product.taxable,
            "weight": product.weight,
            "status": product.is_active
        }

        response = await self._request("PATCH", f"/products/{product_id}", json_data=product_data)
        return Product(**self._map_product_data(response))

    async def delete_product(self, product_id: str) -> bool:
        """Delete product (Delete Product)"""
        await self._request("DELETE", f"/products/{product_id}")
        return True

    async def search_products(
        self,
        query: Optional[str] = None,
        limit: int = 50
    ) -> List[Product]:
        """Search products (Search Products)"""
        params = {"limit": limit, "order": "product_name ASC"}

        if query:
            params["filter"] = f"product_name:*{query}*"

        response = await self._request("GET", "/products", params=params)
        products = response.get("products", [])
        return [Product(**self._map_product_data(p)) for p in products]

    def _map_product_data(self, data: Dict) -> Dict:
        """Map Keap product data to our Product model"""
        return {
            "id": str(data.get("id")) if data.get("id") else None,
            "product_name": data.get("product_name", ""),
            "sku": data.get("sku", ""),
            "price": float(data.get("price", 0.0)),
            "description": data.get("description", ""),
            "short_description": data.get("short_description", ""),
            "taxable": data.get("taxable", False),
            "weight": float(data.get("weight", 0.0)),
            "is_active": data.get("status", True),
            "date_created": data.get("date_created"),
            "last_updated": data.get("last_updated")
        }

    # ==================== Sales Opportunity Operations ====================

    async def create_sales_opportunity(self, opportunity: SalesOpportunity) -> SalesOpportunity:
        """Create a new sales opportunity (Create Sales Opportunity)"""
        opportunity_data = {
            "opportunity_title": opportunity.opportunity_title,
            "estimated_value": opportunity.estimated_value,
            "probability": opportunity.probability,
            "stage_id": opportunity.stage_id,
            "contact_id": opportunity.contact_id,
            "user_id": opportunity.user_id,
            "projected_close_date": opportunity.projected_close_date,
            "notes": opportunity.notes
        }

        # Remove None values
        opportunity_data = {k: v for k, v in opportunity_data.items() if v is not None}

        response = await self._request("POST", "/opportunities", json_data=opportunity_data)
        return SalesOpportunity(**self._map_opportunity_data(response))

    async def get_sales_opportunity(self, opportunity_id: str) -> SalesOpportunity:
        """Get sales opportunity by ID (Get Sales Opportunity)"""
        response = await self._request("GET", f"/opportunities/{opportunity_id}")
        return SalesOpportunity(**self._map_opportunity_data(response))

    async def update_sales_opportunity(self, opportunity_id: str, opportunity: SalesOpportunity) -> SalesOpportunity:
        """Update existing sales opportunity (Update Sales Opportunity)"""
        opportunity_data = {
            "opportunity_title": opportunity.opportunity_title,
            "estimated_value": opportunity.estimated_value,
            "probability": opportunity.probability,
            "stage_id": opportunity.stage_id,
            "user_id": opportunity.user_id,
            "projected_close_date": opportunity.projected_close_date,
            "notes": opportunity.notes
        }

        # Remove None values
        opportunity_data = {k: v for k, v in opportunity_data.items() if v is not None}

        response = await self._request("PATCH", f"/opportunities/{opportunity_id}", json_data=opportunity_data)
        return SalesOpportunity(**self._map_opportunity_data(response))

    async def search_opportunities(
        self,
        contact_id: Optional[str] = None,
        stage_id: Optional[str] = None,
        limit: int = 50
    ) -> List[SalesOpportunity]:
        """Search sales opportunities (Search Opportunities)"""
        params = {"limit": limit, "order": "estimated_value DESC"}

        if contact_id:
            params["contact_id"] = contact_id
        if stage_id:
            params["stage_id"] = stage_id

        response = await self._request("GET", "/opportunities", params=params)
        opportunities = response.get("opportunities", [])
        return [SalesOpportunity(**self._map_opportunity_data(o)) for o in opportunities]

    def _map_opportunity_data(self, data: Dict) -> Dict:
        """Map Keap opportunity data to our SalesOpportunity model"""
        return {
            "id": str(data.get("id")) if data.get("id") else None,
            "opportunity_title": data.get("opportunity_title", ""),
            "estimated_value": float(data.get("estimated_value", 0.0)),
            "probability": int(data.get("probability", 0)),
            "stage_id": str(data.get("stage_id")) if data.get("stage_id") else None,
            "stage_name": data.get("stage", {}).get("stage_name", ""),
            "contact_id": str(data.get("contact_id")) if data.get("contact_id") else None,
            "user_id": str(data.get("user_id")) if data.get("user_id") else None,
            "projected_close_date": data.get("projected_close_date"),
            "notes": data.get("notes", ""),
            "date_created": data.get("date_created"),
            "last_updated": data.get("last_updated")
        }


# ==================== Example Usage ====================

async def main():
    """Example usage of Keap client"""

    # Replace with your actual OAuth access token
    access_token = "your_keap_access_token"

    async with KeapClient(access_token=access_token) as client:
        # Create a contact
        contact = Contact(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="+1-555-1234",
            company="Example Corp",
            job_title="CEO"
        )
        created_contact = await client.create_contact(contact)
        print(f"Created contact: {created_contact.first_name} {created_contact.last_name}")

        # Create a task for the contact
        task = Task(
            title="Follow up call",
            description="Schedule follow-up call with John",
            contact_id=created_contact.id,
            priority="high",
            status="open"
        )
        created_task = await client.create_task(task)
        print(f"Created task: {created_task.title}")

        # Create a sales opportunity
        opportunity = SalesOpportunity(
            opportunity_title="Enterprise Deal",
            estimated_value=50000.0,
            probability=50,
            contact_id=created_contact.id,
            projected_close_date="2024-06-30"
        )
        created_opportunity = await client.create_sales_opportunity(opportunity)
        print(f"Created opportunity: {created_opportunity.opportunity_title} (${created_opportunity.estimated_value})")

        # Create a product
        product = Product(
            product_name="Premium Plan",
            sku="PREM-001",
            price=99.99,
            description="Premium subscription plan",
            taxable=True
        )
        created_product = await client.create_product(product)
        print(f"Created product: {created_product.product_name}")

        # Search contacts
        contacts = await client.search_contacts(query="John")
        print(f"Found {len(contacts)} contacts")


if __name__ == "__main__":
    asyncio.run(main())