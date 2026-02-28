"""
Callconnect API Client

Phone call management platform.

API Actions (5):
1. 顧客を検索 (Search Customers)
2. 通話履歴を検索 (Search Call History)
3. 顧客の取得 (Get Customer)
4. 顧客を作成 (Create Customer)
5. 顧客を削除 (Delete Customer)

Triggers (1):
- Webhookを受信したら (When webhook is received)
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Customer:
    id: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class CallHistory:
    id: Optional[str] = None
    customer_id: Optional[str] = None
    phone: Optional[str] = None
    duration: Optional[int] = None
    direction: Optional[str] = None
    status: Optional[str] = None
    started_at: Optional[str] = None
    ended_at: Optional[str] = None


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


class CallconnectError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}" if status_code else message)


class CallconnectClient:
    """Callconnect API Client"""

    def __init__(self, api_key: str, base_url: str = "https://api.callconnect.jp/v1"):
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
                        raise CallconnectError(error_msg, response.status)
                    return await response.json()
            except aiohttp.ClientError as e:
                raise CallconnectError(f"Network error: {str(e)}")

    # Customer methods
    async def create_customer(self, data: Dict[str, Any]) -> Customer:
        """
        顧客を作成 (Create Customer)

        Args:
            data: Customer data (name, phone, email, company, etc.)

        Returns:
            Customer object
        """
        if not data.get("name"):
            raise CallconnectError("Customer name is required")
        response = await self._make_request("POST", "/customers", data=data)
        return Customer(**response)

    async def get_customer(self, customer_id: str) -> Customer:
        """
        顧客の取得 (Get Customer)

        Args:
            customer_id: Customer ID

        Returns:
            Customer object
        """
        response = await self._make_request("GET", f"/customers/{customer_id}")
        return Customer(**response)

    async def delete_customer(self, customer_id: str) -> Dict[str, str]:
        """
        顧客を削除 (Delete Customer)

        Args:
            customer_id: Customer ID

        Returns:
            Deletion status
        """
        await self._make_request("DELETE", f"/customers/{customer_id}")
        return {"status": "deleted", "customer_id": customer_id}

    async def search_customers(self, **params) -> List[Customer]:
        """
        顧客を検索 (Search Customers)

        Args:
            **params: Search parameters (name, phone, email, company, etc.)

        Returns:
            List of Customer objects
        """
        response = await self._make_request("GET", "/customers", params=params)
        if "data" in response:
            return [Customer(**item) for item in response["data"]]
        if "customers" in response:
            return [Customer(**item) for item in response["customers"]]
        return []

    # Call history methods
    async def search_call_history(self, **params) -> List[CallHistory]:
        """
        通話履歴を検索 (Search Call History)

        Args:
            **params: Search parameters (customer_id, phone, start_date, end_date, etc.)

        Returns:
            List of CallHistory objects
        """
        response = await self._make_request("GET", "/calls/history", params=params)
        if "data" in response:
            return [CallHistory(**item) for item in response["data"]]
        if "calls" in response:
            return [CallHistory(**item) for item in response["calls"]]
        return []

    # Webhook handling
    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process webhook event - Webhookを受信したら

        Args:
            webhook_data: Webhook payload

        Returns:
            Processed event data
        """
        event_type = webhook_data.get("event_type", "unknown")
        call_id = webhook_data.get("call_id")
        customer_id = webhook_data.get("customer_id")

        return {
            "event_type": event_type,
            "call_id": call_id,
            "customer_id": customer_id,
            "data": webhook_data
        }