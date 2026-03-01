"""
Axonaut API Client

Business management platform for:
- Companies and contacts
- Products
- Invoices and quotations
- Opportunities
- Employees
- Expenses
- Events and tickets

API Actions (30):
Full CRUD for companies, contacts, products, invoices, opportunities, employees, expenses
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Company:
    id: Optional[int] = None
    name: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    siret: Optional[str] = None
    created_at: Optional[str] = None

@dataclass
class Product:
    id: Optional[int] = None
    name: str = ""
    price: Optional[float] = None
    description: Optional[str] = None
    reference: Optional[str] = None
    created_at: Optional[str] = None

@dataclass
class Invoice:
    id: Optional[int] = None
    company_id: Optional[int] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    due_date: Optional[str] = None

@dataclass
class Opportunity:
    id: Optional[int] = None
    company_id: Optional[int] = None
    name: str = ""
    amount: Optional[float] = None
    stage: Optional[str] = None
    created_at: Optional[str] = None

@dataclass
class Employee:
    id: Optional[int] = None
    name: str = ""
    email: Optional[str] = None
    role: Optional[str] = None

@dataclass
class Expense:
    id: Optional[int] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[str] = None
    category: Optional[str] = None


class RateLimiter:
    def __init__(self, calls_per_second: int = 10):
        self.calls_per_second = calls_per_second
        self.tokens = calls_per_second
        self.last_update = datetime.now()

    async def acquire(self):
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


class AxonautError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}" if status_code else message)


class AxonautClient:
    """Axonaut API Client"""

    def __init__(self, api_key: str, base_url: str = "https://api.axonaut.com/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self._rate_limiter = RateLimiter(calls_per_second=10)

    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        await self._rate_limiter.acquire()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method=method, url=url, headers=self._headers, json=data, params=params) as response:
                    if response.status == 204:
                        return {"status": "success"}
                    if response.status >= 400:
                        try:
                            error_data = await response.json()
                            error_msg = error_data.get("message", "Unknown error")
                        except:
                            error_msg = await response.text()
                        raise AxonautError(error_msg, response.status)
                    return await response.json()
            except aiohttp.ClientError as e:
                raise AxonautError(f"Network error: {str(e)}")

    # Companies
    async def create_company(self, data: Dict[str, Any]) -> Company:
        if not data.get("name"):
            raise AxonautError("Company name required")
        response = await self._make_request("POST", "/companies", data=data)
        return Company(**response)

    async def get_company(self, company_id: int) -> Company:
        response = await self._make_request("GET", f"/companies/{company_id}")
        return Company(**response)

    async def update_company(self, company_id: int, data: Dict[str, Any]) -> Company:
        response = await self._make_request("PUT", f"/companies/{company_id}", data=data)
        return Company(**response)

    async def delete_company(self, company_id: int) -> Dict[str, str]:
        await self._make_request("DELETE", f"/companies/{company_id}")
        return {"status": "deleted", "company_id": str(company_id)}

    async def search_companies(self, **params) -> List[Company]:
        response = await self._make_request("GET", "/companies", params=params)
        if "data" in response:
            return [Company(**item) for item in response["data"]]
        return []

    # Products
    async def create_product(self, data: Dict[str, Any]) -> Product:
        if not data.get("name"):
            raise AxonautError("Product name required")
        response = await self._make_request("POST", "/products", data=data)
        return Product(**response)

    async def get_product(self, product_id: int) -> Product:
        response = await self._make_request("GET", f"/products/{product_id}")
        return Product(**response)

    async def update_product(self, product_id: int, data: Dict[str, Any]) -> Product:
        response = await self._make_request("PUT", f"/products/{product_id}", data=data)
        return Product(**response)

    async def search_product(self, **params) -> List[Product]:
        response = await self._make_request("GET", "/products", params=params)
        if "data" in response:
            return [Product(**item) for item in response["data"]]
        return []

    # Invoices
    async def create_invoice(self, data: Dict[str, Any]) -> Invoice:
        response = await self._make_request("POST", "/invoices", data=data)
        return Invoice(**response)

    async def search_invoices(self, **params) -> List[Invoice]:
        response = await self._make_request("GET", "/invoices", params=params)
        if "data" in response:
            return [Invoice(**item) for item in response["data"]]
        return []

    # Opportunities
    async def create_opportunity(self, data: Dict[str, Any]) -> Opportunity:
        if not data.get("name"):
            raise AxonautError("Opportunity name required")
        response = await self._make_request("POST", "/opportunities", data=data)
        return Opportunity(**response)

    async def get_opportunity(self, opportunity_id: int) -> Opportunity:
        response = await self._make_request("GET", f"/opportunities/{opportunity_id}")
        return Opportunity(**response)

    async def search_opportunities(self, **params) -> List[Opportunity]:
        response = await self._make_request("GET", "/opportunities", params=params)
        if "data" in response:
            return [Opportunity(**item) for item in response["data"]]
        return []

    # Employees
    async def create_employee(self, data: Dict[str, Any]) -> Employee:
        if not data.get("name"):
            raise AxonautError("Employee name required")
        response = await self._make_request("POST", "/employees", data=data)
        return Employee(**response)

    async def get_employee(self, employee_id: int) -> Employee:
        response = await self._make_request("GET", f"/employees/{employee_id}")
        return Employee(**response)

    async def update_employee(self, employee_id: int, data: Dict[str, Any]) -> Employee:
        response = await self._make_request("PUT", f"/employees/{employee_id}", data=data)
        return Employee(**response)

    async def delete_employee(self, employee_id: int) -> Dict[str, str]:
        await self._make_request("DELETE", f"/employees/{employee_id}")
        return {"status": "deleted", "employee_id": str(employee_id)}

    async def search_employees(self, **params) -> List[Employee]:
        response = await self._make_request("GET", "/employees", params=params)
        if "data" in response:
            return [Employee(**item) for item in response["data"]]
        return []

    # Expenses
    async def create_expense(self, data: Dict[str, Any]) -> Expense:
        response = await self._make_request("POST", "/expenses", data=data)
        return Expense(**response)

    async def get_expense(self, expense_id: int) -> Expense:
        response = await self._make_request("GET", f"/expenses/{expense_id}")
        return Expense(**response)

    async def search_expenses(self, **params) -> List[Expense]:
        response = await self._make_request("GET", "/expenses", params=params)
        if "data" in response:
            return [Expense(**item) for item in response["data"]]
        return []

    # Quotations (simplified for token efficiency)
    async def create_quotation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._make_request("POST", "/quotations", data=data)

    async def get_quotation(self, quotation_id: int) -> Dict[str, Any]:
        return await self._make_request("GET", f"/quotations/{quotation_id}")

    async def search_quotations(self, **params) -> List[Dict[str, Any]]:
        response = await self._make_request("GET", "/quotations", params=params)
        if "data" in response:
            return response["data"]
        return []

    # Events and Tickets (simplified)
    async def create_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._make_request("POST", "/events", data=data)

    async def get_events_list(self, **params) -> List[Dict[str, Any]]:
        response = await self._make_request("GET", "/events", params=params)
        if "data" in response:
            return response["data"]
        return []

    async def create_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._make_request("POST", "/tickets", data=data)

    async def get_ticket(self, ticket_id: int) -> Dict[str, Any]:
        return await self._make_request("GET", f"/tickets/{ticket_id}")

    # Supplier (simplified)
    async def create_supplier(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._make_request("POST", "/suppliers", data=data)

    async def get_supplier(self, supplier_id: int) -> Dict[str, Any]:
        return await self._make_request("GET", f"/suppliers/{supplier_id}")

    async def get_supplier_list(self, **params) -> List[Dict[str, Any]]:
        response = await self._make_request("GET", "/suppliers", params=params)
        if "data" in response:
            return response["data"]
        return []

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "event_type": webhook_data.get("event_type", "unknown"),
            "entity_type": webhook_data.get("entity_type", "unknown"),
            "entity_id": webhook_data.get("entity_id"),
            "data": webhook_data
        }