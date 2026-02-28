"""
Lead generation platform API Client
Sales
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
import time


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, max_requests: int = 120, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.time()
            self.requests = [req_time for req_time in self.requests
                            if now - req_time < self.per_seconds]

            if len(self.requests) >= self.max_requests:
                sleep_time = self.per_seconds - (now - self.requests[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    self.requests = []

            self.requests.append(now)


class SasukeLeadClient:
    """
    Lead generation platform API client.
    """

    BASE_URL = "https://api.sasukelead.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize SasukeLeadClient API client.

        Args:
            api_key: Your API key
        """
        self.api_key = api_key
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=120, per_seconds=60)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API request with error handling and rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data

        Raises:
            Exception: If request fails
        """
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}{endpoint}"

        try:
            async with self.session.request(
                method,
                url,
                headers=self._get_headers(),
                params=params,
                json=json_data
            ) as response:
                try:
                    data = await response.json()
                except:
                    text = await response.text()
                    data = {"raw_response": text}

                if response.status >= 400:
                    error_msg = data.get("error", data.get("message", "Unknown error"))
                    raise Exception(f"SasukeLeadClient API error ({response.status}): {error_msg}")

                return data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during SasukeLeadClient API request: {str(e)}")


    # ==================== API Methods ====================

    async def register_customer(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Register customer information (顧客情報を登録).

        Args:
            name: Customer name
            email: Customer email
            phone: Customer phone number
            company: Company name
            **kwargs: Additional custom fields

        Returns:
            Created customer data

        Raises:
            Exception: If request fails
        """
        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "company": company,
            **kwargs
        }
        # Filter out None values
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("POST", "/customers", json_data=data)

    async def update_customer(
        self,
        customer_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update customer information (顧客情報を修正).

        Args:
            customer_id: Customer ID to update
            name: Customer name
            email: Customer email
            phone: Customer phone number
            company: Company name
            **kwargs: Additional custom fields

        Returns:
            Updated customer data

        Raises:
            Exception: If request fails
        """
        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "company": company,
            **kwargs
        }
        # Filter out None values
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("PUT", f"/customers/{customer_id}", json_data=data)

    async def delete_customer(self, customer_id: str) -> Dict[str, Any]:
        """
        Delete customer information (顧客情報を削除).

        Args:
            customer_id: Customer ID to delete

        Returns:
            Deletion confirmation

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/customers/{customer_id}")

    async def search_customers(
        self,
        query: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search customer information (顧客情報を検索).

        Args:
            query: General search query
            email: Search by email
            name: Search by name
            limit: Maximum results (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of matching customers

        Raises:
            Exception: If request fails
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        if query:
            params["q"] = query
        if email:
            params["email"] = email
        if name:
            params["name"] = name

        return await self._request("GET", "/customers/search", params=params)

    async def get_customers_by_save_number(
        self,
        save_number: str,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get customer information list by save number (顧客情報の一覧を取得（保存番号による取得）).

        Args:
            save_number: Save number to filter by
            limit: Maximum results (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of customers with matching save number

        Raises:
            Exception: If request fails
        """
        params = {
            "save_number": save_number,
            "limit": limit,
            "offset": offset
        }

        return await self._request("GET", "/customers", params=params)

    async def register_lead_source(
        self,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Register lead source (リードソースを登録).

        Args:
            name: Lead source name
            description: Lead source description
            **kwargs: Additional custom fields

        Returns:
            Created lead source data

        Raises:
            Exception: If request fails
        """
        data = {
            "name": name,
            "description": description,
            **kwargs
        }
        # Filter out None values
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("POST", "/lead-sources", json_data=data)

    async def update_lead_source(
        self,
        source_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update lead source (リードソースを修正).

        Args:
            source_id: Lead source ID to update
            name: Lead source name
            description: Lead source description
            **kwargs: Additional custom fields

        Returns:
            Updated lead source data

        Raises:
            Exception: If request fails
        """
        data = {
            "name": name,
            "description": description,
            **kwargs
        }
        # Filter out None values
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("PUT", f"/lead-sources/{source_id}", json_data=data)

    async def delete_lead_source(self, source_id: str) -> Dict[str, Any]:
        """
        Delete lead source (リードソースを削除).

        Args:
            source_id: Lead source ID to delete

        Returns:
            Deletion confirmation

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/lead-sources/{source_id}")

    async def register_history_group(
        self,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Register history group (履歴グループを登録).

        Args:
            name: History group name
            description: History group description
            **kwargs: Additional custom fields

        Returns:
            Created history group data

        Raises:
            Exception: If request fails
        """
        data = {
            "name": name,
            "description": description,
            **kwargs
        }
        # Filter out None values
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("POST", "/history-groups", json_data=data)

    async def update_history_group(
        self,
        group_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update history group (履歴グループを修正).

        Args:
            group_id: History group ID to update
            name: History group name
            description: History group description
            **kwargs: Additional custom fields

        Returns:
            Updated history group data

        Raises:
            Exception: If request fails
        """
        data = {
            "name": name,
            "description": description,
            **kwargs
        }
        # Filter out None values
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("PUT", f"/history-groups/{group_id}", json_data=data)

    async def delete_history_group(self, group_id: str) -> Dict[str, Any]:
        """
        Delete history group (履歴グループを削除).

        Args:
            group_id: History group ID to delete

        Returns:
            Deletion confirmation

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/history-groups/{group_id}")

