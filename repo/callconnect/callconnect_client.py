"""
CallConnect API Client

CallConnect provides call management and customer tracking services.

Supports:
- 顧客を検索 (Search Customers)
- 通話履歴を検索 (Search Call History)
- 顧客の取得 (Get Customer)
- 顧客を作成 (Create Customer)
- 顧客を削除 (Delete Customer)
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Customer:
    """Customer object"""
    id: str
    name: str
    phone: Optional[str]
    email: Optional[str]
    company: Optional[str]
    notes: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class CallRecord:
    """Call record object"""
    id: str
    customer_id: str
    phone_number: str
    direction: str  # inbound, outbound
    duration: int  # seconds
    status: str  # completed, missed, voicemail
    recording_url: Optional[str]
    started_at: str
    ended_at: str


@dataclass
class CustomerSearchResult:
    """Customer search result"""
    customers: List[Customer]
    total_count: int
    page: int
    page_size: int


@dataclass
class CallHistory:
    """Call history object"""
    calls: List[CallRecord]
    total_count: int
    page: int
    page_size: int


class CallConnectAPIClient:
    """
    CallConnect API client for call management and customer tracking.

    Authentication: API Key
    Base URL: https://api.callconnect.jp
    """

    BASE_URL = "https://api.callconnect.jp/v1"

    def __init__(self, api_key: str):
        """
        Initialize CallConnect API client.

        Args:
            api_key: CallConnect API key
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
        Make HTTP request to CallConnect API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        url = f"{self.BASE_URL}{endpoint}"

        async with self.session.request(
            method,
            url,
            params=params,
            json=json_data
        ) as response:
            data = await response.json()

            if response.status not in [200, 201, 204]:
                raise Exception(f"CallConnect API error ({response.status}): {data}")

            return data

    async def _request_with_retry(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data
            max_retries: Maximum number of retries
            retry_delay: Delay between retries in seconds

        Returns:
            Response data as dictionary

        Raises:
            Exception: If all retries fail
        """
        last_error = None

        for attempt in range(max_retries):
            try:
                return await self._request(method, endpoint, params, json_data)
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (attempt + 1))

        raise last_error if last_error else Exception("Request failed after retries")

    # ==================== Customers ====================

    async def create_customer(
        self,
        name: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        notes: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Customer:
        """
        Create a new customer.

        顧客を作成

        Args:
            name: Customer name
            phone: Phone number
            email: Email address
            company: Company name
            notes: Notes about the customer
            metadata: Additional metadata

        Returns:
            Customer object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {"name": name}

        if phone:
            json_data["phone"] = phone
        if email:
            json_data["email"] = email
        if company:
            json_data["company"] = company
        if notes:
            json_data["notes"] = notes
        if metadata:
            json_data["metadata"] = metadata

        data = await self._request_with_retry("POST", "/customers", json_data=json_data)

        now = datetime.utcnow().isoformat()
        return Customer(
            id=data.get("id", ""),
            name=data.get("name", name),
            phone=data.get("phone"),
            email=data.get("email"),
            company=data.get("company"),
            notes=data.get("notes"),
            created_at=data.get("created_at", now),
            updated_at=data.get("updated_at", now)
        )

    async def get_customer(self, customer_id: str) -> Customer:
        """
        Get a customer by ID.

        顧客の取得

        Args:
            customer_id: Customer ID

        Returns:
            Customer object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request_with_retry("GET", f"/customers/{customer_id}")

        return Customer(
            id=data.get("id", customer_id),
            name=data.get("name", ""),
            phone=data.get("phone"),
            email=data.get("email"),
            company=data.get("company"),
            notes=data.get("notes"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def search_customers(
        self,
        query: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        page: int = 1,
        page_size: int = 50
    ) -> CustomerSearchResult:
        """
        Search for customers.

        顧客を検索

        Args:
            query: General search query (searches name, email, phone)
            phone: Filter by phone number
            email: Filter by email address
            company: Filter by company name
            page: Page number (1-indexed)
            page_size: Number of results per page

        Returns:
            CustomerSearchResult object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"page": page, "page_size": page_size}

        if query:
            params["q"] = query
        if phone:
            params["phone"] = phone
        if email:
            params["email"] = email
        if company:
            params["company"] = company

        data = await self._request_with_retry("GET", "/customers", params=params)

        customers_data = data.get("customers", [])
        customers = [
            Customer(
                id=c.get("id", ""),
                name=c.get("name", ""),
                phone=c.get("phone"),
                email=c.get("email"),
                company=c.get("company"),
                notes=c.get("notes"),
                created_at=c.get("created_at", ""),
                updated_at=c.get("updated_at", "")
            )
            for c in customers_data
        ]

        return CustomerSearchResult(
            customers=customers,
            total_count=data.get("total_count", len(customers)),
            page=data.get("page", page),
            page_size=data.get("page_size", page_size)
        )

    async def update_customer(
        self,
        customer_id: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        notes: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Customer:
        """
        Update a customer.

        Args:
            customer_id: Customer ID
            name: New name
            phone: New phone number
            email: New email address
            company: New company name
            notes: New notes
            metadata: Metadata to update

        Returns:
            Updated Customer object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        json_data = {}

        if name:
            json_data["name"] = name
        if phone:
            json_data["phone"] = phone
        if email:
            json_data["email"] = email
        if company:
            json_data["company"] = company
        if notes:
            json_data["notes"] = notes
        if metadata:
            json_data["metadata"] = metadata

        data = await self._request_with_retry(
            "PUT",
            f"/customers/{customer_id}",
            json_data=json_data
        )

        return Customer(
            id=data.get("id", customer_id),
            name=data.get("name", ""),
            phone=data.get("phone"),
            email=data.get("email"),
            company=data.get("company"),
            notes=data.get("notes"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", datetime.utcnow().isoformat())
        )

    async def delete_customer(self, customer_id: str) -> bool:
        """
        Delete a customer.

        顧客を削除

        Args:
            customer_id: Customer ID

        Returns:
            True if deleted successfully

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        await self._request_with_retry("DELETE", f"/customers/{customer_id}")
        return True

    # ==================== Call History ====================

    async def search_call_history(
        self,
        customer_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        direction: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        page: int = 1,
        page_size: int = 50
    ) -> CallHistory:
        """
        Search call history.

        通話履歴を検索

        Args:
            customer_id: Filter by customer ID
            phone_number: Filter by phone number
            direction: Filter by direction (inbound, outbound)
            status: Filter by status (completed, missed, voicemail)
            date_from: Filter by date from (ISO 8601 format)
            date_to: Filter by date to (ISO 8601 format)
            page: Page number (1-indexed)
            page_size: Number of results per page

        Returns:
            CallHistory object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        params = {"page": page, "page_size": page_size}

        if customer_id:
            params["customer_id"] = customer_id
        if phone_number:
            params["phone_number"] = phone_number
        if direction:
            params["direction"] = direction
        if status:
            params["status"] = status
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to

        data = await self._request_with_retry("GET", "/calls/search", params=params)

        calls_data = data.get("calls", [])
        calls = [
            CallRecord(
                id=c.get("id", ""),
                customer_id=c.get("customer_id", ""),
                phone_number=c.get("phone_number", ""),
                direction=c.get("direction", ""),
                duration=c.get("duration", 0),
                status=c.get("status", ""),
                recording_url=c.get("recording_url"),
                started_at=c.get("started_at", ""),
                ended_at=c.get("ended_at", "")
            )
            for c in calls_data
        ]

        return CallHistory(
            calls=calls,
            total_count=data.get("total_count", len(calls)),
            page=data.get("page", page),
            page_size=data.get("page_size", page_size)
        )

    async def get_call_record(self, call_id: str) -> CallRecord:
        """
        Get a call record by ID.

        Args:
            call_id: Call record ID

        Returns:
            CallRecord object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        data = await self._request_with_retry("GET", f"/calls/{call_id}")

        return CallRecord(
            id=data.get("id", call_id),
            customer_id=data.get("customer_id", ""),
            phone_number=data.get("phone_number", ""),
            direction=data.get("direction", ""),
            duration=data.get("duration", 0),
            status=data.get("status", ""),
            recording_url=data.get("recording_url"),
            started_at=data.get("started_at", ""),
            ended_at=data.get("ended_at", "")
        )

    async def search_customers_by_phone(self, phone: str) -> List[Customer]:
        """
        Search customers by phone number.

        Args:
            phone: Phone number to search

        Returns:
            List of Customer objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns error
        """
        result = await self.search_customers(phone=phone, page_size=100)
        return result.customers


# ==================== Webhook Support ====================

class CallConnectWebhookHandler:
    """
    CallConnect webhook handler for processing incoming events.

    Supported webhook events:
    - Webhookを受信したら (Webhook Received)
    """

    @staticmethod
    def parse_webhook_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and validate webhook payload.

        Args:
            payload: Raw webhook payload

        Returns:
            Parsed event data with event_type and data

        Raises:
            ValueError: If payload is invalid
        """
        event_type = payload.get("event", payload.get("event_type", ""))

        return {
            "event_type": event_type,
            "timestamp": payload.get("timestamp", datetime.utcnow().isoformat()),
            "data": payload.get("data", {})
        }

    @staticmethod
    def handle_call_received(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming call webhook event"""
        return {
            "call_id": payload.get("call_id"),
            "phone_number": payload.get("phone_number"),
            "direction": payload.get("direction", "inbound"),
            "customer_id": payload.get("customer_id"),
            "timestamp": payload.get("timestamp")
        }

    @staticmethod
    def handle_call_completed(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle call completed webhook event"""
        return {
            "call_id": payload.get("call_id"),
            "customer_id": payload.get("customer_id"),
            "phone_number": payload.get("phone_number"),
            "duration": payload.get("duration"),
            "status": payload.get("status"),
            "recording_url": payload.get("recording_url"),
            "timestamp": payload.get("timestamp")
        }

    @staticmethod
    def handle_customer_created(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer created webhook event"""
        return {
            "customer_id": payload.get("customer_id"),
            "name": payload.get("name"),
            "phone": payload.get("phone"),
            "email": payload.get("email"),
            "timestamp": payload.get("timestamp")
        }


# ==================== Example Usage ====================

async def main():
    """Example usage of CallConnect API client"""

    api_key = "your_callconnect_api_key"

    async with CallConnectAPIClient(api_key=api_key) as client:
        # Create a customer
        customer = await client.create_customer(
            name="山田太郎",
            phone="+8190123456789",
            email="yamada@example.com",
            company="テスト株式会社",
            notes="重要な顧客"
        )
        print(f"Created customer: {customer.id}")

        # Get customer
        customer = await client.get_customer(customer.id)
        print(f"Got customer: {customer.name}")

        # Search customers
        result = await client.search_customers(query="山田", page_size=10)
        print(f"Found {result.total_count} customers")

        # Search call history
        history = await client.search_call_history(
            customer_id=customer.id,
            page_size=20
        )
        print(f"Found {history.total_count} call records")

        # Update customer
        updated = await client.update_customer(
            customer.id,
            notes="VIP顧客",
            email="yamada.vip@example.com"
        )
        print(f"Updated customer: {updated.notes}")

        # Search by phone
        customers = await client.search_customers_by_phone("+8190123456789")
        print(f"Found {len(customers)} customers by phone")


if __name__ == "__main__":
    asyncio.run(main())