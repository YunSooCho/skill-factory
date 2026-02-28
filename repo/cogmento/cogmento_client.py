"""
Cogmento API Client

Complete client for Cogmento CRM system.
Supports deals, contacts, companies, tasks, and products.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import json


class CogmentoAPIError(Exception):
    """Base exception for Cogmento API errors"""

    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class CogmentoRateLimitError(CogmentoAPIError):
    """Raised when rate limit is exceeded"""


@dataclass
class Deal:
    deal_id: str
    name: str
    value: float
    stage: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Company:
    company_id: str
    name: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Contact:
    contact_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    task_id: str
    name: str
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Product:
    product_id: str
    name: str
    price: float
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class CogmentoClient:
    """Cogmento CRM API Client."""

    BASE_URL = "https://api.cogmento.com/v1"

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
                    raise CogmentoRateLimitError("Rate limit exceeded", status_code=429)

                if response.status >= 400:
                    error_msg = response_data.get("error", str(response_data))
                    raise CogmentoAPIError(error_msg, status_code=response.status)

                return response_data if isinstance(response_data, dict) else {}

        except aiohttp.ClientError as e:
            raise CogmentoAPIError(f"Network error: {str(e)}")

    def _to_model(self, data: Dict, model_class, id_field: str) -> Any:
        return model_class(
            **{id_field: data.get("id", "") or data.get(id_field, ""),
               **{k: v for k, v in data.items() if k not in ["id", id_field]}}
        )

    async def create_deal(self, deal_data: Dict[str, Any]) -> Deal:
        data = await self._request("POST", "/deals", data=deal_data)
        return Deal(
            deal_id=data.get("id", ""),
            name=data.get("name", ""),
            value=data.get("value", 0.0),
            stage=data.get("stage", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "value", "stage", "created_at", "updated_at"]}
        )

    async def update_deal(self, deal_id: str, update_data: Dict[str, Any]) -> Deal:
        data = await self._request("PUT", f"/deals/{deal_id}", data=update_data)
        return Deal(
            deal_id=deal_id,
            name=data.get("name", ""),
            value=data.get("value", 0.0),
            stage=data.get("stage", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["name", "value", "stage", "created_at", "updated_at"]}
        )

    async def get_deal(self, deal_id: str) -> Deal:
        data = await self._request("GET", f"/deals/{deal_id}")
        return Deal(
            deal_id=data.get("id", deal_id),
            name=data.get("name", ""),
            value=data.get("value", 0.0),
            stage=data.get("stage", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "value", "stage", "created_at", "updated_at"]}
        )

    async def list_deals(self, limit: int = 100, offset: int = 0) -> List[Deal]:
        params = {"limit": limit, "offset": offset}
        data = await self._request("GET", "/deals", params=params)
        results = data.get("results", [])

        return [Deal(
            deal_id=r.get("id", ""),
            name=r.get("name", ""),
            value=r.get("value", 0.0),
            stage=r.get("stage", ""),
            created_at=r.get("created_at"),
            updated_at=r.get("updated_at"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "name", "value", "stage", "created_at", "updated_at"]}
        ) for r in results]

    async def create_company(self, company_data: Dict[str, Any]) -> Company:
        data = await self._request("POST", "/companies", data=company_data)
        return Company(
            company_id=data.get("id", ""),
            name=data.get("name", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "created_at", "updated_at"]}
        )

    async def update_company(self, company_id: str, update_data: Dict[str, Any]) -> Company:
        data = await self._request("PUT", f"/companies/{company_id}", data=update_data)
        return Company(
            company_id=company_id,
            name=data.get("name", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["name", "created_at", "updated_at"]}
        )

    async def get_company(self, company_id: str) -> Company:
        data = await self._request("GET", f"/companies/{company_id}")
        return Company(
            company_id=data.get("id", company_id),
            name=data.get("name", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "created_at", "updated_at"]}
        )

    async def list_companies(self, limit: int = 100, offset: int = 0) -> List[Company]:
        params = {"limit": limit, "offset": offset}
        data = await self._request("GET", "/companies", params=params)
        results = data.get("results", [])

        return [Company(
            company_id=r.get("id", ""),
            name=r.get("name", ""),
            created_at=r.get("created_at"),
            updated_at=r.get("updated_at"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "name", "created_at", "updated_at"]}
        ) for r in results]

    async def create_contact(self, contact_data: Dict[str, Any]) -> Contact:
        data = await self._request("POST", "/contacts", data=contact_data)
        return Contact(
            contact_id=data.get("id", ""),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "email", "phone", "created_at", "updated_at"]}
        )

    async def update_contact(self, contact_id: str, update_data: Dict[str, Any]) -> Contact:
        data = await self._request("PUT", f"/contacts/{contact_id}", data=update_data)
        return Contact(
            contact_id=contact_id,
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["name", "email", "phone", "created_at", "updated_at"]}
        )

    async def get_contact(self, contact_id: str) -> Contact:
        data = await self._request("GET", f"/contacts/{contact_id}")
        return Contact(
            contact_id=data.get("id", contact_id),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "email", "phone", "created_at", "updated_at"]}
        )

    async def list_contacts(self, limit: int = 100, offset: int = 0) -> List[Contact]:
        params = {"limit": limit, "offset": offset}
        data = await self._request("GET", "/contacts", params=params)
        results = data.get("results", [])

        return [Contact(
            contact_id=r.get("id", ""),
            name=r.get("name", ""),
            email=r.get("email"),
            phone=r.get("phone"),
            created_at=r.get("created_at"),
            updated_at=r.get("updated_at"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "name", "email", "phone", "created_at", "updated_at"]}
        ) for r in results]

    async def create_task(self, task_data: Dict[str, Any]) -> Task:
        data = await self._request("POST", "/tasks", data=task_data)
        return Task(
            task_id=data.get("id", ""),
            name=data.get("name", ""),
            status=data.get("status", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "status", "created_at", "updated_at"]}
        )

    async def update_task(self, task_id: str, update_data: Dict[str, Any]) -> Task:
        data = await self._request("PUT", f"/tasks/{task_id}", data=update_data)
        return Task(
            task_id=task_id,
            name=data.get("name", ""),
            status=data.get("status", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["name", "status", "created_at", "updated_at"]}
        )

    async def get_task(self, task_id: str) -> Task:
        data = await self._request("GET", f"/tasks/{task_id}")
        return Task(
            task_id=data.get("id", task_id),
            name=data.get("name", ""),
            status=data.get("status", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "status", "created_at", "updated_at"]}
        )

    async def list_tasks(self, limit: int = 100, offset: int = 0) -> List[Task]:
        params = {"limit": limit, "offset": offset}
        data = await self._request("GET", "/tasks", params=params)
        results = data.get("results", [])

        return [Task(
            task_id=r.get("id", ""),
            name=r.get("name", ""),
            status=r.get("status", ""),
            created_at=r.get("created_at"),
            updated_at=r.get("updated_at"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "name", "status", "created_at", "updated_at"]}
        ) for r in results]

    async def create_product(self, product_data: Dict[str, Any]) -> Product:
        data = await self._request("POST", "/products", data=product_data)
        return Product(
            product_id=data.get("id", ""),
            name=data.get("name", ""),
            price=data.get("price", 0.0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "price", "created_at", "updated_at"]}
        )

    async def update_product(self, product_id: str, update_data: Dict[str, Any]) -> Product:
        data = await self._request("PUT", f"/products/{product_id}", data=update_data)
        return Product(
            product_id=product_id,
            name=data.get("name", ""),
            price=data.get("price", 0.0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["name", "price", "created_at", "updated_at"]}
        )

    async def get_product(self, product_id: str) -> Product:
        data = await self._request("GET", f"/products/{product_id}")
        return Product(
            product_id=data.get("id", product_id),
            name=data.get("name", ""),
            price=data.get("price", 0.0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in ["id", "name", "price", "created_at", "updated_at"]}
        )

    async def list_products(self, limit: int = 100, offset: int = 0) -> List[Product]:
        params = {"limit": limit, "offset": offset}
        data = await self._request("GET", "/products", params=params)
        results = data.get("results", [])

        return [Product(
            product_id=r.get("id", ""),
            name=r.get("name", ""),
            price=r.get("price", 0.0),
            created_at=r.get("created_at"),
            updated_at=r.get("updated_at"),
            additional_data={k: v for k, v in r.items() if k not in ["id", "name", "price", "created_at", "updated_at"]}
        ) for r in results]

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


async def main():
    async with CogmentoClient(api_key="your_api_key") as client:
        deal = await client.create_deal({
            "name": "Enterprise Contract",
            "value": 100000.0,
            "stage": "Negotiation"
        })
        print(f"Created deal: {deal.deal_id}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())