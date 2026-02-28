"""
Klenty API - Sales Engagement Client

Supports 10 API Actions:
- Change Prospect Status to Unsubscribed
- Change Prospect Status to DoNotContact
- List Prospects
- Remove Prospect Tags
- Update Prospect
- Start Cadence
- Create Prospect
- Stop Cadence
- Create Prospect with Tag

Triggers:
- Email Clicked
- Email Opened
- Email Reply
- Prospect Unsubscribed
- Start Cadence
- Cadence First Reply
- Send Prospect
- Email Bounced
- Cadence Completed Without Reply
"""

import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Prospect:
    """Prospect entity"""
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Cadence:
    """Cadence entity"""
    id: str
    name: str
    status: Optional[str] = None
    steps_count: int = 0


class KlentyClientError(Exception):
    """Base exception for Klenty client errors"""
    pass


class KlentyRateLimitError(KlentyClientError):
    """Raised when rate limit is exceeded"""
    pass


class KlentyClient:
    """
    Klenty API client for sales engagement and outreach automation.

    API Documentation: https://developers.klenty.com/
    Uses API Key for authentication via Bearer token.
    """

    BASE_URL = "https://api.klenty.com/api"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize Klenty client.

        Args:
            api_key: API key for authentication
            base_url: Optional custom base URL
        """
        self.api_key = api_key
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None
        self._rate_limit_remaining = 100
        self._rate_limit_reset = 0

        logger = logging.getLogger("klenty")
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
        """Make HTTP request with error handling and rate limiting."""
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

                    if response.status in [200, 201]:
                        result = await response.json()
                        self._logger.debug(f"Response: {result}")
                        return result

                    elif response.status == 204:
                        return {}

                    elif response.status == 401:
                        raise KlentyClientError("Authentication failed")

                    elif response.status == 403:
                        raise KlentyClientError("Forbidden - insufficient permissions")

                    elif response.status == 404:
                        raise KlentyClientError("Resource not found")

                    elif response.status == 422:
                        error_data = await response.json()
                        raise KlentyClientError(
                            f"Validation error: {error_data.get('message', 'Unknown error')}"
                        )

                    elif response.status == 429:
                        await self._handle_rate_limit()
                        retry_count += 1
                        continue

                    else:
                        error_text = await response.text()
                        raise KlentyClientError(
                            f"API error {response.status}: {error_text}"
                        )

            except aiohttp.ClientError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise KlentyClientError(f"Network error: {str(e)}")
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

    async def _handle_rate_limit(self):
        """Handle rate limit by waiting"""
        now = int(datetime.now().timestamp())
        wait_time = max(0, self._rate_limit_reset - now + 1)
        self._logger.warning(f"Rate limited, waiting {wait_time}s")
        await asyncio.sleep(wait_time)

    async def create_prospect(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Prospect:
        """Create a new prospect."""
        data = {"email": email}
        if first_name:
            data["first_name"] = first_name
        if last_name:
            data["last_name"] = last_name
        if phone:
            data["phone"] = phone
        if company:
            data["company"] = company
        if custom_fields:
            data["custom_fields"] = custom_fields

        self._logger.info(f"Creating prospect: {email}")
        result = await self._request("POST", "/prospects", data=data)

        return Prospect(
            id=str(result.get("id", "")),
            email=email,
            first_name=result.get("first_name"),
            last_name=result.get("last_name"),
            phone=result.get("phone"),
            company=result.get("company"),
            custom_fields=result.get("custom_fields"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def create_prospect_with_tag(
        self,
        email: str,
        tags: List[str],
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None
    ) -> Prospect:
        """Create a new prospect with tags."""
        data = {
            "email": email,
            "tags": tags
        }
        if first_name:
            data["first_name"] = first_name
        if last_name:
            data["last_name"] = last_name
        if phone:
            data["phone"] = phone
        if company:
            data["company"] = company

        self._logger.info(f"Creating prospect with tags: {email}, tags={tags}")
        result = await self._request("POST", "/prospects", data=data)

        return Prospect(
            id=str(result.get("id", "")),
            email=email,
            first_name=result.get("first_name"),
            last_name=result.get("last_name"),
            phone=result.get("phone"),
            company=result.get("company"),
            tags=result.get("tags"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def update_prospect(
        self,
        prospect_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Prospect:
        """Update an existing prospect."""
        data = {}
        if first_name is not None:
            data["first_name"] = first_name
        if last_name is not None:
            data["last_name"] = last_name
        if phone is not None:
            data["phone"] = phone
        if company is not None:
            data["company"] = company
        if custom_fields is not None:
            data["custom_fields"] = custom_fields

        self._logger.info(f"Updating prospect {prospect_id}")
        result = await self._request("PUT", f"/prospects/{prospect_id}", data=data)

        return Prospect(
            id=str(result.get("id", "")),
            email=result.get("email", ""),
            first_name=result.get("first_name"),
            last_name=result.get("last_name"),
            phone=result.get("phone"),
            company=result.get("company"),
            custom_fields=result.get("custom_fields"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def list_prospects(
        self,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Prospect]:
        """List all prospects with optional filters."""
        params = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        if tags:
            params["tags"] = ",".join(tags)

        self._logger.info("Listing prospects")
        result = await self._request("GET", "/prospects", params=params)

        prospects = []
        for item in result.get("prospects", []):
            prospects.append(Prospect(
                id=str(item.get("id", "")),
                email=item.get("email", ""),
                first_name=item.get("first_name"),
                last_name=item.get("last_name"),
                phone=item.get("phone"),
                company=item.get("company"),
                status=item.get("status"),
                tags=item.get("tags"),
                custom_fields=item.get("custom_fields"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return prospects

    async def remove_prospect_tags(
        self,
        prospect_id: str,
        tags: List[str]
    ) -> Prospect:
        """Remove specific tags from a prospect."""
        data = {"tags": tags}

        self._logger.info(f"Removing tags from prospect {prospect_id}: {tags}")
        result = await self._request("POST", f"/prospects/{prospect_id}/remove-tags", data=data)

        return Prospect(
            id=str(result.get("id", "")),
            email=result.get("email", ""),
            first_name=result.get("first_name"),
            last_name=result.get("last_name"),
            tags=result.get("tags"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def start_cadence(
        self,
        prospect_id: str,
        cadence_id: str
    ) -> Dict[str, Any]:
        """Add a prospect to a cadence."""
        data = {"prospect_id": prospect_id, "cadence_id": cadence_id}

        self._logger.info(f"Starting cadence {cadence_id} for prospect {prospect_id}")
        result = await self._request("POST", "/cadences/start", data=data)

        return result

    async def stop_cadence(
        self,
        prospect_id: str,
        cadence_id: str
    ) -> Dict[str, Any]:
        """Stop a cadence for a prospect."""
        data = {"prospect_id": prospect_id, "cadence_id": cadence_id}

        self._logger.info(f"Stopping cadence {cadence_id} for prospect {prospect_id}")
        result = await self._request("POST", "/cadences/stop", data=data)

        return result

    async def change_status_unsubscribed(self, prospect_id: str) -> Prospect:
        """Mark prospect as unsubscribed."""
        data = {"status": "unsubscribed"}

        self._logger.info(f"Marking prospect {prospect_id} as unsubscribed")
        result = await self._request("PUT", f"/prospects/{prospect_id}", data=data)

        return Prospect(
            id=str(result.get("id", "")),
            email=result.get("email", ""),
            status=result.get("status"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def change_status_do_not_contact(self, prospect_id: str) -> Prospect:
        """Mark prospect as do not contact."""
        data = {"status": "do_not_contact"}

        self._logger.info(f"Marking prospect {prospect_id} as do not contact")
        result = await self._request("PUT", f"/prospects/{prospect_id}", data=data)

        return Prospect(
            id=str(result.get("id", "")),
            email=result.get("email", ""),
            status=result.get("status"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )