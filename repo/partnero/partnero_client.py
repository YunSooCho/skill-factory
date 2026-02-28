"""
Partnero API - Partnership Management Client

Supports:
- Partners management
- Customers management
- Transactions management
"""

import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import os


@dataclass
class Partner:
    """Partner information"""
    partner_id: str
    name: str
    email: Optional[str]
    status: str
    commission_rate: Optional[float]
    total_earnings: Optional[float]
    created_at: str
    updated_at: str


@dataclass
class Customer:
    """Customer information"""
    customer_id: str
    email: str
    name: Optional[str]
    status: str
    referred_by: Optional[str]
    total_spent: Optional[float]
    created_at: str
    updated_at: str


@dataclass
class Transaction:
    """Transaction information"""
    transaction_id: str
    customer_id: str
    partner_id: Optional[str]
    amount: float
    commission: Optional[float]
    status: str
    transaction_date: str
    created_at: str


class PartneroClient:
    """
    Partnero API client for partnership management.

    API Documentation: https://lp.yoom.fun/apps/partnero
    Requires API key from Yoom integration.
    """

    BASE_URL = "https://api.partnero.com/v1"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize Partnero client.

        Args:
            api_key: API key (defaults to YOOM_PARTNERO_API_KEY env var)
            base_url: Custom base URL for testing
        """
        self.api_key = api_key or os.environ.get("YOOM_PARTNERO_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set YOOM_PARTNERO_API_KEY environment variable")

        self.base_url = base_url or self.BASE_URL
        self.session = None
        self._rate_limit_delay = 0.3  # 300ms between requests

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request with rate limiting"""
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async with statement")

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        headers["Content-Type"] = "application/json"

        # Rate limiting
        await asyncio.sleep(self._rate_limit_delay)

        url = f"{self.base_url}{endpoint}"

        async with self.session.request(method, url, headers=headers, **kwargs) as response:
            if response.status == 429:
                retry_after = int(response.headers.get("Retry-After", 2))
                await asyncio.sleep(retry_after)
                return await self._request(method, endpoint, **kwargs)

            if response.status >= 400:
                error_text = await response.text()
                raise Exception(f"API error {response.status}: {error_text}")

            if response.status == 204:
                return {}

            return await response.json()

    # ==================== Partner Operations ====================

    async def create_partner(self, partner_data: Dict[str, Any]) -> Partner:
        """Create a new partner"""
        data = await self._request("POST", "/partners", json=partner_data)

        return Partner(
            partner_id=data.get("id", ""),
            name=data.get("name", ""),
            email=data.get("email"),
            status=data.get("status", "active"),
            commission_rate=data.get("commission_rate"),
            total_earnings=data.get("total_earnings"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def get_partner(self, partner_id: str) -> Partner:
        """Get partner by ID"""
        data = await self._request("GET", f"/partners/{partner_id}")

        return Partner(
            partner_id=data.get("id", partner_id),
            name=data.get("name", ""),
            email=data.get("email"),
            status=data.get("status", "active"),
            commission_rate=data.get("commission_rate"),
            total_earnings=data.get("total_earnings"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def update_partner(self, partner_id: str, update_data: Dict[str, Any]) -> Partner:
        """Update partner"""
        data = await self._request("PUT", f"/partners/{partner_id}", json=update_data)

        return Partner(
            partner_id=data.get("id", partner_id),
            name=data.get("name", ""),
            email=data.get("email"),
            status=data.get("status", "active"),
            commission_rate=data.get("commission_rate"),
            total_earnings=data.get("total_earnings"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def delete_partner(self, partner_id: str) -> Dict[str, Any]:
        """Delete partner"""
        return await self._request("DELETE", f"/partners/{partner_id}")

    async def list_partners(self, **filters) -> List[Partner]:
        """List partners with optional filters"""
        data = await self._request("GET", "/partners", params=filters)

        partners = []
        for item in data.get("data", []):
            partners.append(Partner(
                partner_id=item.get("id", ""),
                name=item.get("name", ""),
                email=item.get("email"),
                status=item.get("status", "active"),
                commission_rate=item.get("commission_rate"),
                total_earnings=item.get("total_earnings"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return partners

    async def search_partners(self, query: str, **filters) -> List[Partner]:
        """Search partners"""
        params = {"query": query, **filters}
        data = await self._request("GET", "/partners/search", params=params)

        partners = []
        for item in data.get("data", []):
            partners.append(Partner(
                partner_id=item.get("id", ""),
                name=item.get("name", ""),
                email=item.get("email"),
                status=item.get("status", "active"),
                commission_rate=item.get("commission_rate"),
                total_earnings=item.get("total_earnings"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return partners

    # ==================== Customer Operations ====================

    async def create_customer(self, customer_data: Dict[str, Any]) -> Customer:
        """Create a new customer"""
        data = await self._request("POST", "/customers", json=customer_data)

        return Customer(
            customer_id=data.get("id", ""),
            email=data.get("email", ""),
            name=data.get("name"),
            status=data.get("status", "active"),
            referred_by=data.get("referred_by"),
            total_spent=data.get("total_spent"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def get_customer(self, customer_id: str) -> Customer:
        """Get customer by ID"""
        data = await self._request("GET", f"/customers/{customer_id}")

        return Customer(
            customer_id=data.get("id", customer_id),
            email=data.get("email", ""),
            name=data.get("name"),
            status=data.get("status", "active"),
            referred_by=data.get("referred_by"),
            total_spent=data.get("total_spent"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def update_customer(self, customer_id: str, update_data: Dict[str, Any]) -> Customer:
        """Update customer"""
        data = await self._request("PUT", f"/customers/{customer_id}", json=update_data)

        return Customer(
            customer_id=data.get("id", customer_id),
            email=data.get("email", ""),
            name=data.get("name"),
            status=data.get("status", "active"),
            referred_by=data.get("referred_by"),
            total_spent=data.get("total_spent"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def delete_customer(self, customer_id: str) -> Dict[str, Any]:
        """Delete customer"""
        return await self._request("DELETE", f"/customers/{customer_id}")

    async def list_customers(self, **filters) -> List[Customer]:
        """List customers with optional filters"""
        data = await self._request("GET", "/customers", params=filters)

        customers = []
        for item in data.get("data", []):
            customers.append(Customer(
                customer_id=item.get("id", ""),
                email=item.get("email", ""),
                name=item.get("name"),
                status=item.get("status", "active"),
                referred_by=item.get("referred_by"),
                total_spent=item.get("total_spent"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return customers

    # ==================== Transaction Operations ====================

    async def create_transaction(self, transaction_data: Dict[str, Any]) -> Transaction:
        """Create a new transaction"""
        data = await self._request("POST", "/transactions", json=transaction_data)

        return Transaction(
            transaction_id=data.get("id", ""),
            customer_id=data.get("customer_id", ""),
            partner_id=data.get("partner_id"),
            amount=data.get("amount", 0.0),
            commission=data.get("commission"),
            status=data.get("status", "pending"),
            transaction_date=data.get("transaction_date", datetime.now(timezone.utc).isoformat()),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat())
        )

    async def get_transaction(self, transaction_id: str) -> Transaction:
        """Get transaction by ID"""
        data = await self._request("GET", f"/transactions/{transaction_id}")

        return Transaction(
            transaction_id=data.get("id", transaction_id),
            customer_id=data.get("customer_id", ""),
            partner_id=data.get("partner_id"),
            amount=data.get("amount", 0.0),
            commission=data.get("commission"),
            status=data.get("status", "pending"),
            transaction_date=data.get("transaction_date", ""),
            created_at=data.get("created_at", "")
        )

    async def delete_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """Delete transaction"""
        return await self._request("DELETE", f"/transactions/{transaction_id}")

    async def list_transactions(self, **filters) -> List[Transaction]:
        """List transactions with optional filters"""
        data = await self._request("GET", "/transactions", params=filters)

        transactions = []
        for item in data.get("data", []):
            transactions.append(Transaction(
                transaction_id=item.get("id", ""),
                customer_id=item.get("customer_id", ""),
                partner_id=item.get("partner_id"),
                amount=item.get("amount", 0.0),
                commission=item.get("commission"),
                status=item.get("status", "pending"),
                transaction_date=item.get("transaction_date", ""),
                created_at=item.get("created_at", "")
            ))

        return transactions

    # ==================== Webhook Handlers ====================

    async def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming webhook events"""
        event_type = payload.get("event_type")

        if event_type == "customer_created":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "customer_updated":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "customer_deleted":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "partner_created":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "partner_updated":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "partner_deleted":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "transaction_created":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "transaction_deleted":
            return {"status": "acknowledged", "event_type": event_type}
        else:
            return {"status": "acknowledged", "event_type": event_type}