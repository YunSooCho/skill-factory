"""
Printbahn API - Business Card Search Client

Supports 2 API Actions:
- Search Business Card (Single)
- Search Business Cards (Multiple)

Triggers:
- None
"""

import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BusinessCard:
    """Business card entity"""
    id: str
    name: str
    organization: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    address: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: str = ""
    updated_at: str = ""


class PrintbahnClientError(Exception):
    """Base exception for Printbahn client errors"""
    pass


class PrintbahnRateLimitError(PrintbahnClientError):
    """Raised when rate limit is exceeded"""
    pass


class PrintbahnClient:
    """
    Printbahn API client for business card management.

    API Documentation: contact Printbahn for API access
    Uses API Key for authentication via Bearer token.
    """

    BASE_URL = "https://api.printbahn.com/v1"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize Printbahn client.

        Args:
            api_key: API key for authentication
            base_url: Optional custom base URL
        """
        self.api_key = api_key
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None
        self._rate_limit_remaining = 100
        self._rate_limit_reset = 0

        logger = logging.getLogger("printbahn")
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        self._logger = logger

    async def __aenter__(self):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=timeout
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request with error handling and rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response data as dictionary

        Raises:
            PrintbahnClientError: On API errors
            PrintbahnRateLimitError: On rate limit exceeded
        """
        await self._check_rate_limit()

        url = f"{self.base_url}{endpoint}"

        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                self._logger.debug(f"Request: {method} {url}")
                if data:
                    self._logger.debug(f"Data: {data}")

                async with self.session.request(
                    method,
                    url,
                    json=data,
                    params=params
                ) as response:
                    await self._update_rate_limit(response)

                    if response.status == 200 or response.status == 201:
                        result = await response.json()
                        self._logger.debug(f"Response: {result}")
                        return result

                    elif response.status == 204:
                        self._logger.debug("Response: No Content")
                        return {}

                    elif response.status == 401:
                        raise PrintbahnClientError("Authentication failed")

                    elif response.status == 403:
                        raise PrintbahnClientError("Forbidden - insufficient permissions")

                    elif response.status == 404:
                        raise PrintbahnClientError("Resource not found")

                    elif response.status == 422:
                        error_data = await response.json()
                        raise PrintbahnClientError(
                            f"Validation error: {error_data.get('message', 'Unknown error')}"
                        )

                    elif response.status == 429:
                        await self._handle_rate_limit()
                        retry_count += 1
                        continue

                    else:
                        error_text = await response.text()
                        raise PrintbahnClientError(
                            f"API error {response.status}: {error_text}"
                        )

            except aiohttp.ClientError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise PrintbahnClientError(f"Network error: {str(e)}")
                await asyncio.sleep(2 ** retry_count)

    async def _check_rate_limit(self):
        """Check if rate limit allows request"""
        if self._rate_limit_remaining <= 1:
            now = int(datetime.now().timestamp())
            if now < self._rate_limit_reset:
                wait_time = self._rate_limit_reset - now
                self._logger.warning(f"Rate limit reached, waiting {wait_time}s")
                await asyncio.sleep(wait_time)

    async def _update_rate_limit(self, response: aiohttp.ClientResponse):
        """Update rate limit info from response headers"""
        remaining = response.headers.get("X-RateLimit-Remaining")
        reset = response.headers.get("X-RateLimit-Reset")

        if remaining:
            self._rate_limit_remaining = int(remaining)
        if reset:
            self._rate_limit_reset = int(reset)

        self._logger.debug(
            f"Rate limit: {self._rate_limit_remaining} remaining, "
            f"resets at {self._rate_limit_reset}"
        )

    async def _handle_rate_limit(self):
        """Handle rate limit by waiting"""
        now = int(datetime.now().timestamp())
        wait_time = max(0, self._rate_limit_reset - now + 1)
        self._logger.warning(f"Rate limited, waiting {wait_time}s")
        await asyncio.sleep(wait_time)

    async def search_business_card(
        self,
        email: Optional[str] = None,
        name: Optional[str] = None,
        organization: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Optional[BusinessCard]:
        """
        Search for a business card (single result).

        Args:
            email: Email address to search
            name: Name to search
            organization: Organization name to search
            phone: Phone number to search

        Returns:
            Business card object if found, None otherwise

        Raises:
            PrintbahnClientError: On API errors
        """
        params = {}
        if email:
            params["email"] = email
        if name:
            params["name"] = name
        if organization:
            params["organization"] = organization
        if phone:
            params["phone"] = phone

        if not params:
            raise PrintbahnClientError("At least one search parameter is required")

        self._logger.info(f"Searching for business card with params: {list(params.keys())}")
        result = await self._request("GET", "/business-cards/search", params=params)

        if not result or "business_card" not in result:
            return None

        card_data = result["business_card"]
        return BusinessCard(
            id=str(card_data.get("id", "")),
            name=card_data.get("name", ""),
            organization=card_data.get("organization"),
            department=card_data.get("department"),
            title=card_data.get("title"),
            email=card_data.get("email"),
            phone=card_data.get("phone"),
            mobile=card_data.get("mobile"),
            address=card_data.get("address"),
            tags=card_data.get("tags"),
            created_at=card_data.get("created_at", ""),
            updated_at=card_data.get("updated_at", "")
        )

    async def search_business_cards(
        self,
        email: Optional[str] = None,
        name: Optional[str] = None,
        organization: Optional[str] = None,
        phone: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[BusinessCard]:
        """
        Search for business cards (multiple results).

        Args:
            email: Email address to filter
            name: Name to search (partial match)
            organization: Organization name to search
            phone: Phone number to search
            tags: List of tags to filter
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of business card objects

        Raises:
            PrintbahnClientError: On API errors
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        if email:
            params["email"] = email
        if name:
            params["name"] = name
        if organization:
            params["organization"] = organization
        if phone:
            params["phone"] = phone
        if tags:
            params["tags"] = ",".join(tags)

        if not any([email, name, organization, phone, tags]):
            raise PrintbahnClientError("At least one search parameter is required")

        self._logger.info(f"Searching for business cards with params: {list(params.keys())}")
        result = await self._request("GET", "/business-cards", params=params)

        cards = []
        for card_data in result.get("business_cards", []):
            cards.append(BusinessCard(
                id=str(card_data.get("id", "")),
                name=card_data.get("name", ""),
                organization=card_data.get("organization"),
                department=card_data.get("department"),
                title=card_data.get("title"),
                email=card_data.get("email"),
                phone=card_data.get("phone"),
                mobile=card_data.get("mobile"),
                address=card_data.get("address"),
                tags=card_data.get("tags"),
                created_at=card_data.get("created_at", ""),
                updated_at=card_data.get("updated_at", "")
            ))

        return cards