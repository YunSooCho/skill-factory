"""
Subscription billing and recurring payment service API Client

Category: Payment
API Actions (5):
1. Create Account
2. Get Account
3. Create Subscription
4. Get Subscription
5. List Invoices

Authentication: API Key or OAuth
Base URL: https://api.recurly.com/v2
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class RecurlyResponse:
    """Response model"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: int = 200


@dataclass
class RecurlyRecord:
    """Record model"""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    properties: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        if isinstance(data, dict):
            return cls(
                id=str(data.get('id', '')),
                created_at=datetime.now(),
                updated_at=datetime.now() if data.get('updated_at') else None,
                properties=data
            )
        return cls(id='', created_at=datetime.now(), properties=data)


class RecurlyClient:
    """
    Async client for Subscription billing and recurring payment service

    Usage:
        client = RecurlyClient(api_key="your_api_key")
        result = await client.list_items()
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.api_key = api_key
        self.base_url = base_url or "https://api.recurly.com/v2"
        self.timeout = timeout
        self.max_retries = max_retries
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            headers=self._get_headers()
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get default headers for requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "recurly_client/1.0"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None
    ) -> RecurlyResponse:
        """Make an HTTP request"""
        url = f"{self.base_url}{endpoint}"

        for attempt in range(self.max_retries):
            try:
                headers = self._get_headers()
                if files:
                    headers.pop("Content-Type", None)

                async with self.session.request(
                    method=method,
                    url=url,
                    json=data if not files else None,
                    params=params,
                    data=files if files else None,
                    headers=headers if not files else {k: v for k, v in headers.items() if k != 'Content-Type'}
                ) as response:
                    status_code = response.status
                    content_type = response.headers.get('Content-Type', '')

                    if status_code >= 400:
                        error_text = await response.text()
                        return RecurlyResponse(
                            success=False,
                            error=error_text,
                            status_code=status_code
                        )

                    if 'application/json' in content_type:
                        result_data = await response.json()
                        return RecurlyResponse(
                            success=True,
                            data=result_data,
                            status_code=status_code
                        )
                    else:
                        text_data = await response.text()
                        return RecurlyResponse(
                            success=True,
                            data={'content': text_data},
                            status_code=status_code
                        )

            except aiohttp.ClientError as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Request failed after {self.max_retries} attempts: {e}")
                    return RecurlyResponse(
                        success=False,
                        error=str(e),
                        status_code=500
                    )
                await asyncio.sleep(1 * (attempt + 1))


    async def create_account(self, **kwargs) -> RecurlyResponse:
        """
        Create Account

        Args:
            **kwargs: Additional parameters

        Returns:
            RecurlyResponse
        """
        return await self._request('POST', '/create_account', data=kwargs if kwargs else None)


    async def get_account(self, **kwargs) -> RecurlyResponse:
        """
        Get Account

        Args:
            **kwargs: Additional parameters

        Returns:
            RecurlyResponse
        """
        return await self._request('POST', '/get_account', data=kwargs if kwargs else None)


    async def create_subscription(self, **kwargs) -> RecurlyResponse:
        """
        Create Subscription

        Args:
            **kwargs: Additional parameters

        Returns:
            RecurlyResponse
        """
        return await self._request('POST', '/create_subscription', data=kwargs if kwargs else None)


    async def list_items(
        self,
        limit: int = 100,
        offset: int = 0,
        filters: Optional[Dict[str, Any]] = None
    ) -> RecurlyResponse:
        """
        List items with optional filtering

        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip
            filters: Optional filter criteria

        Returns:
            RecurlyResponse with list of items
        """

        params = {'limit': limit, 'offset': offset, **(filters or {})}
        return await self._request('GET', '/items', params=params)

    async def get_item(self, item_id: str) -> RecurlyResponse:
        """
        Get a single item by ID

        Args:
            item_id: The ID of the item

        Returns:
            RecurlyResponse with item details
        """

        return await self._request('GET', f'/items/{item_id}')

    async def create_item(self, data: Dict[str, Any]) -> RecurlyResponse:
        """
        Create a new item

        Args:
            data: Item data

        Returns:
            RecurlyResponse with created item
        """

        return await self._request('POST', '/items', data=data)

    async def update_item(self, item_id: str, data: Dict[str, Any]) -> RecurlyResponse:
        """
        Update an existing item

        Args:
            item_id: The ID of the item
            data: Updated item data

        Returns:
            RecurlyResponse with updated item
        """

        return await self._request('PUT', f'/items/{item_id}', data=data)

    async def delete_item(self, item_id: str) -> RecurlyResponse:
        """
        Delete an item

        Args:
            item_id: The ID of the item

        Returns:
            RecurlyResponse
        """

        return await self._request('DELETE', f'/items/{item_id}')

    async def health_check(self) -> RecurlyResponse:
        """
        Check API health status

        Returns:
            RecurlyResponse with health status
        """

        return await self._request('GET', '/health')
