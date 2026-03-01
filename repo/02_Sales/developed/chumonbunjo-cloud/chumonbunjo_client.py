"""
Chumonbunjo Cloud API Client

Complete client for Japanese real estate sales and contract management system.
Supports 28 API endpoints with full CRUD operations for contracts, customers,
quotes, purchase orders, vendors, and partners.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, field
import json


class ChumonbunjoAPIError(Exception):
    """Base exception for Chumonbunjo Cloud API errors"""

    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class ChumonbunjoRateLimitError(ChumonbunjoAPIError):
    """Raised when rate limit is exceeded"""


@dataclass
class Customer:
    """Customer data model"""
    customer_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Contract:
    """Contract data model (both ordered and developed housing)"""
    contract_id: str
    contract_type: str  # "ordered" or "developed"
    customer_id: str
    status: str
    contract_date: Optional[str] = None
    amount: Optional[float] = None
    property_address: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Quote:
    """Quote data model"""
    quote_id: str
    customer_id: str
    quote_date: str
    total_amount: float
    status: str
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PurchaseOrder:
    """Purchase order data model"""
    order_id: str
    vendor_id: str
    order_date: str
    total_amount: float
    status: str
    created_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Vendor:
    """Vendor data model"""
    vendor_id: str
    name: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Partner:
    """Partner account data model"""
    partner_id: str
    name: str
    company_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class ChumonbunjoClient:
    """
    Chumonbunjo Cloud API Client

    Provides complete access to Chumonbunjo Cloud API for real estate
    and contract management in Japan.
    """

    BASE_URL = "https://api.chumonbunjo.cloud/v1"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        max_requests_per_minute: int = 60,
        timeout: int = 30
    ):
        """
        Initialize Chumonbunjo Cloud client.

        Args:
            api_key: API key for authentication
            base_url: Optional custom base URL
            max_requests_per_minute: Rate limit (requests per minute)
            timeout: Request timeout in seconds
        """
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
        """Check and enforce rate limiting"""
        now = asyncio.get_event_loop().time()
        # Remove requests older than 1 minute
        self._request_times = [t for t in self._request_times if now - t < 60]

        if len(self._request_times) >= self.max_requests_per_minute:
            sleep_time = 60 - (now - self._request_times[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                # Clean up old requests after sleeping
                self._request_times = []

        self._request_times.append(now)

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an API request with error handling and rate limiting.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters

        Returns:
            Response data as dict

        Raises:
            ChumonbunjoAPIError: On API errors
            ChumonbunjoRateLimitError: On rate limit exceeded
        """
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
                method,
                url,
                json=data,
                params=params,
                headers=headers
            ) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = await response.text()

                if response.status == 429:
                    raise ChumonbunjoRateLimitError(
                        "Rate limit exceeded",
                        status_code=429,
                        response=response_data
                    )

                if response.status >= 400:
                    error_msg = response_data.get("error", {}).get("message", str(response_data))
                    raise ChumonbunjoAPIError(
                        error_msg,
                        status_code=response.status,
                        response=response_data
                    )

                return response_data if isinstance(response_data, dict) else {}

        except aiohttp.ClientError as e:
            raise ChumonbunjoAPIError(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise ChumonbunjoAPIError(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            if isinstance(e, ChumonbunjoAPIError):
                raise
            raise ChumonbunjoAPIError(f"Unexpected error: {str(e)}")

    # ==================== Ordered Housing Contracts (注文住宅) ====================

    async def create_ordered_contract(self, contract_data: Dict[str, Any]) -> Contract:
        """
        Create a new ordered housing contract.

        Args:
            contract_data: Contract information including customer_id, property details

        Returns:
            Created Contract object

        Raises:
            ChumonbunjoAPIError: On API errors
        """
        data = await self._request("POST", "/contracts/ordered", data=contract_data)
        return Contract(
            contract_id=data.get("contract_id", ""),
            contract_type="ordered",
            customer_id=data.get("customer_id", ""),
            status=data.get("status", ""),
            contract_date=data.get("contract_date"),
            amount=data.get("amount"),
            property_address=data.get("property_address"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "contract_id", "status", "contract_date", "amount",
                "property_address", "created_at", "updated_at"
            ]}
        )

    async def update_ordered_contract(
        self,
        contract_id: str,
        update_data: Dict[str, Any]
    ) -> Contract:
        """
        Update an existing ordered housing contract.

        Args:
            contract_id: Contract ID to update
            update_data: Fields to update

        Returns:
            Updated Contract object
        """
        data = await self._request("PUT", f"/contracts/ordered/{contract_id}", data=update_data)
        return Contract(
            contract_id=contract_id,
            contract_type="ordered",
            customer_id=data.get("customer_id", ""),
            status=data.get("status", ""),
            contract_date=data.get("contract_date"),
            amount=data.get("amount"),
            property_address=data.get("property_address"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "customer_id", "status", "contract_date", "amount",
                "property_address", "created_at", "updated_at"
            ]}
        )

    async def get_ordered_contract(self, contract_id: str) -> Contract:
        """
        Get details of an ordered housing contract.

        Args:
            contract_id: Contract ID to retrieve

        Returns:
            Contract object with full details
        """
        data = await self._request("GET", f"/contracts/ordered/{contract_id}")
        return Contract(
            contract_id=data.get("contract_id", contract_id),
            contract_type="ordered",
            customer_id=data.get("customer_id", ""),
            status=data.get("status", ""),
            contract_date=data.get("contract_date"),
            amount=data.get("amount"),
            property_address=data.get("property_address"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "customer_id", "status", "contract_date", "amount",
                "property_address", "created_at", "updated_at"
            ]}
        )

    async def search_ordered_contracts(
        self,
        customer_id: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Contract]:
        """
        Search for ordered housing contracts.

        Args:
            customer_id: Filter by customer ID
            status: Filter by status
            start_date: Start date filter (YYYY-MM-DD)
            end_date: End date filter (YYYY-MM-DD)
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of Contract objects
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        if customer_id:
            params["customer_id"] = customer_id
        if status:
            params["status"] = status
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        data = await self._request("GET", "/contracts/ordered/search", params=params)
        contracts = data.get("contracts", [])

        return [
            Contract(
                contract_id=c.get("contract_id", ""),
                contract_type="ordered",
                customer_id=c.get("customer_id", ""),
                status=c.get("status", ""),
                contract_date=c.get("contract_date"),
                amount=c.get("amount"),
                property_address=c.get("property_address"),
                created_at=c.get("created_at"),
                updated_at=c.get("updated_at"),
                additional_data={k: v for k, v in c.items() if k not in [
                    "contract_id", "customer_id", "status", "contract_date",
                    "amount", "property_address", "created_at", "updated_at"
                ]}
            )
            for c in contracts
        ]

    # ==================== Developed Housing Contracts (分譲住宅) ====================

    async def create_developed_contract(self, contract_data: Dict[str, Any]) -> Contract:
        """Create a new developed housing contract."""
        data = await self._request("POST", "/contracts/developed", data=contract_data)
        return Contract(
            contract_id=data.get("contract_id", ""),
            contract_type="developed",
            customer_id=data.get("customer_id", ""),
            status=data.get("status", ""),
            contract_date=data.get("contract_date"),
            amount=data.get("amount"),
            property_address=data.get("property_address"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "contract_id", "customer_id", "status", "contract_date",
                "amount", "property_address", "created_at", "updated_at"
            ]}
        )

    async def update_developed_contract(
        self,
        contract_id: str,
        update_data: Dict[str, Any]
    ) -> Contract:
        """Update an existing developed housing contract."""
        data = await self._request("PUT", f"/contracts/developed/{contract_id}", data=update_data)
        return Contract(
            contract_id=contract_id,
            contract_type="developed",
            customer_id=data.get("customer_id", ""),
            status=data.get("status", ""),
            contract_date=data.get("contract_date"),
            amount=data.get("amount"),
            property_address=data.get("property_address"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "customer_id", "status", "contract_date", "amount",
                "property_address", "created_at", "updated_at"
            ]}
        )

    async def get_developed_contract(self, contract_id: str) -> Contract:
        """Get details of a developed housing contract."""
        data = await self._request("GET", f"/contracts/developed/{contract_id}")
        return Contract(
            contract_id=data.get("contract_id", contract_id),
            contract_type="developed",
            customer_id=data.get("customer_id", ""),
            status=data.get("status", ""),
            contract_date=data.get("contract_date"),
            amount=data.get("amount"),
            property_address=data.get("property_address"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "customer_id", "status", "contract_date", "amount",
                "property_address", "created_at", "updated_at"
            ]}
        )

    async def search_developed_contracts(
        self,
        customer_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Contract]:
        """Search for developed housing contracts."""
        params = {"limit": limit, "offset": offset}
        if customer_id:
            params["customer_id"] = customer_id
        if status:
            params["status"] = status

        data = await self._request("GET", "/contracts/developed/search", params=params)
        contracts = data.get("contracts", [])

        return [
            Contract(
                contract_id=c.get("contract_id", ""),
                contract_type="developed",
                customer_id=c.get("customer_id", ""),
                status=c.get("status", ""),
                contract_date=c.get("contract_date"),
                amount=c.get("amount"),
                property_address=c.get("property_address"),
                created_at=c.get("created_at"),
                updated_at=c.get("updated_at"),
                additional_data={k: v for k, v in c.items() if k not in [
                    "contract_id", "customer_id", "status", "contract_date",
                    "amount", "property_address", "created_at", "updated_at"
                ]}
            )
            for c in contracts
        ]

    # ==================== Customers (顧客データ) ====================

    async def create_customer(self, customer_data: Dict[str, Any]) -> Customer:
        """Create a new customer."""
        data = await self._request("POST", "/customers", data=customer_data)
        return Customer(
            customer_id=data.get("customer_id", ""),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "customer_id", "name", "email", "phone", "address",
                "created_at", "updated_at"
            ]}
        )

    async def update_customer(
        self,
        customer_id: str,
        update_data: Dict[str, Any]
    ) -> Customer:
        """Update an existing customer."""
        data = await self._request("PUT", f"/customers/{customer_id}", data=update_data)
        return Customer(
            customer_id=customer_id,
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "name", "email", "phone", "address", "created_at", "updated_at"
            ]}
        )

    async def get_customer(self, customer_id: str) -> Customer:
        """Get customer details."""
        data = await self._request("GET", f"/customers/{customer_id}")
        return Customer(
            customer_id=data.get("customer_id", customer_id),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "name", "email", "phone", "address", "created_at", "updated_at"
            ]}
        )

    async def search_customers(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Customer]:
        """Search for customers."""
        params = {"limit": limit, "offset": offset}
        if name:
            params["name"] = name
        if email:
            params["email"] = email
        if phone:
            params["phone"] = phone

        data = await self._request("GET", "/customers/search", params=params)
        customers = data.get("customers", [])

        return [
            Customer(
                customer_id=c.get("customer_id", ""),
                name=c.get("name", ""),
                email=c.get("email"),
                phone=c.get("phone"),
                address=c.get("address"),
                created_at=c.get("created_at"),
                updated_at=c.get("updated_at"),
                additional_data={k: v for k, v in c.items() if k not in [
                    "customer_id", "name", "email", "phone", "address",
                    "created_at", "updated_at"
                ]}
            )
            for c in customers
        ]

    # ==================== Quotes (見積書) ====================

    async def get_quote(self, quote_id: str) -> Quote:
        """Get quote details."""
        data = await self._request("GET", f"/quotes/{quote_id}")
        return Quote(
            quote_id=data.get("quote_id", quote_id),
            customer_id=data.get("customer_id", ""),
            quote_date=data.get("quote_date", ""),
            total_amount=data.get("total_amount", 0.0),
            status=data.get("status", ""),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "quote_id", "customer_id", "quote_date", "total_amount",
                "status", "created_at"
            ]}
        )

    async def search_quotes(
        self,
        customer_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Quote]:
        """Search for quotes."""
        params = {"limit": limit, "offset": offset}
        if customer_id:
            params["customer_id"] = customer_id
        if status:
            params["status"] = status

        data = await self._request("GET", "/quotes/search", params=params)
        quotes = data.get("quotes", [])

        return [
            Quote(
                quote_id=q.get("quote_id", ""),
                customer_id=q.get("customer_id", ""),
                quote_date=q.get("quote_date", ""),
                total_amount=q.get("total_amount", 0.0),
                status=q.get("status", ""),
                created_at=q.get("created_at"),
                additional_data={k: v for k, v in q.items() if k not in [
                    "quote_id", "customer_id", "quote_date", "total_amount",
                    "status", "created_at"
                ]}
            )
            for q in quotes
        ]

    async def create_quote_csv(self, quote_ids: List[str]) -> str:
        """
        Create CSV file for quotes.

        Args:
            quote_ids: List of quote IDs to include in CSV

        Returns:
            CSV file download URL
        """
        data = await self._request("POST", "/quotes/csv", data={"quote_ids": quote_ids})
        return data.get("download_url", "")

    async def get_quote_csv_file(self, csv_id: str) -> str:
        """
        Get CSV file for quotes.

        Args:
            csv_id: CSV file ID

        Returns:
            CSV file content or download URL
        """
        data = await self._request("GET", f"/quotes/csv/{csv_id}")
        return data.get("content", "") or data.get("download_url", "")

    # ==================== Purchase Orders (発注データ) ====================

    async def get_purchase_order(self, order_id: str) -> PurchaseOrder:
        """Get purchase order details."""
        data = await self._request("GET", f"/purchase-orders/{order_id}")
        return PurchaseOrder(
            order_id=data.get("order_id", order_id),
            vendor_id=data.get("vendor_id", ""),
            order_date=data.get("order_date", ""),
            total_amount=data.get("total_amount", 0.0),
            status=data.get("status", ""),
            created_at=data.get("created_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "order_id", "vendor_id", "order_date", "total_amount",
                "status", "created_at"
            ]}
        )

    async def search_purchase_orders(
        self,
        vendor_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[PurchaseOrder]:
        """Search for purchase orders."""
        params = {"limit": limit, "offset": offset}
        if vendor_id:
            params["vendor_id"] = vendor_id
        if status:
            params["status"] = status

        data = await self._request("GET", "/purchase-orders/search", params=params)
        orders = data.get("orders", [])

        return [
            PurchaseOrder(
                order_id=o.get("order_id", ""),
                vendor_id=o.get("vendor_id", ""),
                order_date=o.get("order_date", ""),
                total_amount=o.get("total_amount", 0.0),
                status=o.get("status", ""),
                created_at=o.get("created_at"),
                additional_data={k: v for k, v in o.items() if k not in [
                    "order_id", "vendor_id", "order_date", "total_amount",
                    "status", "created_at"
                ]}
            )
            for o in orders
        ]

    async def create_purchase_order_csv(self, order_ids: List[str]) -> str:
        """Create CSV file for purchase orders."""
        data = await self._request("POST", "/purchase-orders/csv", data={"order_ids": order_ids})
        return data.get("download_url", "")

    async def get_purchase_order_csv_file(self, csv_id: str) -> str:
        """Get CSV file for purchase orders."""
        data = await self._request("GET", f"/purchase-orders/csv/{csv_id}")
        return data.get("content", "") or data.get("download_url", "")

    # ==================== Vendors (仕入先業者) ====================

    async def create_vendor(self, vendor_data: Dict[str, Any]) -> Vendor:
        """Create a new vendor."""
        data = await self._request("POST", "/vendors", data=vendor_data)
        return Vendor(
            vendor_id=data.get("vendor_id", ""),
            name=data.get("name", ""),
            contact_person=data.get("contact_person"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "vendor_id", "name", "contact_person", "email", "phone",
                "address", "created_at", "updated_at"
            ]}
        )

    async def update_vendor(
        self,
        vendor_id: str,
        update_data: Dict[str, Any]
    ) -> Vendor:
        """Update an existing vendor."""
        data = await self._request("PUT", f"/vendors/{vendor_id}", data=update_data)
        return Vendor(
            vendor_id=vendor_id,
            name=data.get("name", ""),
            contact_person=data.get("contact_person"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "name", "contact_person", "email", "phone", "address",
                "created_at", "updated_at"
            ]}
        )

    async def get_vendor(self, vendor_id: str) -> Vendor:
        """Get vendor details."""
        data = await self._request("GET", f"/vendors/{vendor_id}")
        return Vendor(
            vendor_id=data.get("vendor_id", vendor_id),
            name=data.get("name", ""),
            contact_person=data.get("contact_person"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "name", "contact_person", "email", "phone", "address",
                "created_at", "updated_at"
            ]}
        )

    async def search_vendors(
        self,
        name: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Vendor]:
        """Search for vendors."""
        params = {"limit": limit, "offset": offset}
        if name:
            params["name"] = name

        data = await self._request("GET", "/vendors/search", params=params)
        vendors = data.get("vendors", [])

        return [
            Vendor(
                vendor_id=v.get("vendor_id", ""),
                name=v.get("name", ""),
                contact_person=v.get("contact_person"),
                email=v.get("email"),
                phone=v.get("phone"),
                address=v.get("address"),
                created_at=v.get("created_at"),
                updated_at=v.get("updated_at"),
                additional_data={k: v for k, v in v.items() if k not in [
                    "vendor_id", "name", "contact_person", "email", "phone",
                    "address", "created_at", "updated_at"
                ]}
            )
            for v in vendors
        ]

    # ==================== Partners (協力業者) ====================

    async def create_partner(self, partner_data: Dict[str, Any]) -> Partner:
        """Create a new partner account."""
        data = await self._request("POST", "/partners", data=partner_data)
        return Partner(
            partner_id=data.get("partner_id", ""),
            name=data.get("name", ""),
            company_name=data.get("company_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            role=data.get("role"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "partner_id", "name", "company_name", "email", "phone",
                "role", "created_at", "updated_at"
            ]}
        )

    async def update_partner(
        self,
        partner_id: str,
        update_data: Dict[str, Any]
    ) -> Partner:
        """Update an existing partner account."""
        data = await self._request("PUT", f"/partners/{partner_id}", data=update_data)
        return Partner(
            partner_id=partner_id,
            name=data.get("name", ""),
            company_name=data.get("company_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            role=data.get("role"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "name", "company_name", "email", "phone", "role",
                "created_at", "updated_at"
            ]}
        )

    async def get_partner(self, partner_id: str) -> Partner:
        """Get partner account details."""
        data = await self._request("GET", f"/partners/{partner_id}")
        return Partner(
            partner_id=data.get("partner_id", partner_id),
            name=data.get("name", ""),
            company_name=data.get("company_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            role=data.get("role"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_data={k: v for k, v in data.items() if k not in [
                "name", "company_name", "email", "phone", "role",
                "created_at", "updated_at"
            ]}
        )

    async def search_partners(
        self,
        name: Optional[str] = None,
        company_name: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Partner]:
        """Search for partner accounts."""
        params = {"limit": limit, "offset": offset}
        if name:
            params["name"] = name
        if company_name:
            params["company_name"] = company_name

        data = await self._request("GET", "/partners/search", params=params)
        partners = data.get("partners", [])

        return [
            Partner(
                partner_id=p.get("partner_id", ""),
                name=p.get("name", ""),
                company_name=p.get("company_name"),
                email=p.get("email"),
                phone=p.get("phone"),
                role=p.get("role"),
                created_at=p.get("created_at"),
                updated_at=p.get("updated_at"),
                additional_data={k: v for k, v in p.items() if k not in [
                    "partner_id", "name", "company_name", "email", "phone",
                    "role", "created_at", "updated_at"
                ]}
            )
            for p in partners
        ]

    async def close(self):
        """Close the client session."""
        if self.session and not self.session.closed:
            await self.session.close()


# ==================== Example Usage ====================

async def main():
    """Example usage of Chumonbunjo Cloud client."""

    # Initialize client
    async with ChumonbunjoClient(api_key="your_api_key") as client:
        # Create a customer
        customer = await client.create_customer({
            "name": "田中太郎",
            "email": "tanaka@example.com",
            "phone": "090-1234-5678",
            "address": "東京都渋谷区"
        })
        print(f"Created customer: {customer.customer_id}")

        # Create an ordered contract
        contract = await client.create_ordered_contract({
            "customer_id": customer.customer_id,
            "property_address": "東京都世田谷区〇〇1-2-3",
            "contract_date": "2024-01-15",
            "amount": 50000000
        })
        print(f"Created contract: {contract.contract_id}")

        # Search contracts
        contracts = await client.search_ordered_contracts(
            customer_id=customer.customer_id
        )
        print(f"Found {len(contracts)} contracts")

        # Get quote details
        if contracts:
            quote = await client.get_quote(contract.contract_id)
            print(f"Quote: {quote.quote_id}")


if __name__ == "__main__":
    asyncio.run(main())