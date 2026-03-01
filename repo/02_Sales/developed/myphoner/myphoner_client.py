"""
Myphoner API - Lead Management Client

Supports 8 API Actions:
- Mark Loser
- List Columns
- Create Lead
- Get Lead
- Mark Winner
- Search Leads
- Update Lead
- Mark Callback

Triggers:
- Lead Marked as Winner
- Lead Marked as Loser
- Lead Archive
- Lead Marked as Callback
"""

import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Lead:
    """Lead entity"""
    id: str
    list_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    loser_reason: Optional[str] = None
    winner_reason: Optional[str] = None
    callback_time: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Column:
    """Column entity"""
    id: str
    list_id: str
    name: str
    position: int


class MyphonerClientError(Exception):
    """Base exception for Myphoner client errors"""
    pass


class MyphonerRateLimitError(MyphonerClientError):
    """Raised when rate limit is exceeded"""
    pass


class MyphonerClient:
    """
    Myphoner API client for lead management.

    API Documentation: https://help.myphoner.com/api/
    Uses API Key for authentication via Bearer token.
    """

    BASE_URL = "https://api.myphoner.com"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize Myphoner client.

        Args:
            api_key: API key for authentication
            base_url: Optional custom base URL
        """
        self.api_key = api_key
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None
        self._rate_limit_remaining = 100
        self._rate_limit_reset = 0

        logger = logging.getLogger("myphoner")
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
            MyphonerClientError: On API errors
            MyphonerRateLimitError: On rate limit exceeded
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
                        raise MyphonerClientError("Authentication failed")

                    elif response.status == 403:
                        raise MyphonerClientError("Forbidden - insufficient permissions")

                    elif response.status == 404:
                        raise MyphonerClientError("Resource not found")

                    elif response.status == 422:
                        error_data = await response.json()
                        raise MyphonerClientError(
                            f"Validation error: {error_data.get('errors', 'Unknown error')}"
                        )

                    elif response.status == 429:
                        await self._handle_rate_limit()
                        retry_count += 1
                        continue

                    else:
                        error_text = await response.text()
                        raise MyphonerClientError(
                            f"API error {response.status}: {error_text}"
                        )

            except aiohttp.ClientError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise MyphonerClientError(f"Network error: {str(e)}")
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

    async def create_lead(
        self,
        list_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Lead:
        """
        Create a new lead in Myphoner.

        Args:
            list_id: ID of the list to add lead to
            name: Lead name
            email: Lead email
            phone: Lead phone
            company: Lead company
            custom_fields: Custom field values

        Returns:
            Created lead object

        Raises:
            MyphonerClientError: On API errors
        """
        data = {"list_id": list_id}
        if name:
            data["name"] = name
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if company:
            data["company"] = company
        if custom_fields:
            data["custom_fields"] = custom_fields

        self._logger.info(f"Creating lead in list {list_id}")
        result = await self._request("POST", "/leads", data=data)

        return Lead(
            id=str(result.get("id", "")),
            list_id=list_id,
            name=result.get("name"),
            email=result.get("email"),
            phone=result.get("phone"),
            company=result.get("company"),
            custom_fields=result.get("custom_fields"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def get_lead(self, lead_id: str) -> Lead:
        """
        Get a lead by ID.

        Args:
            lead_id: ID of the lead

        Returns:
            Lead object

        Raises:
            MyphonerClientError: On API errors
        """
        self._logger.info(f"Getting lead {lead_id}")
        result = await self._request("GET", f"/leads/{lead_id}")

        return Lead(
            id=str(result.get("id", "")),
            list_id=str(result.get("list_id", "")),
            name=result.get("name"),
            email=result.get("email"),
            phone=result.get("phone"),
            company=result.get("company"),
            status=result.get("status"),
            loser_reason=result.get("loser_reason"),
            winner_reason=result.get("winner_reason"),
            callback_time=result.get("callback_time"),
            custom_fields=result.get("custom_fields"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def update_lead(
        self,
        lead_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Lead:
        """
        Update an existing lead.

        Args:
            lead_id: ID of the lead to update
            name: New name
            email: New email
            phone: New phone
            company: New company
            custom_fields: New custom field values

        Returns:
            Updated lead object

        Raises:
            MyphonerClientError: On API errors
        """
        data = {}
        if name is not None:
            data["name"] = name
        if email is not None:
            data["email"] = email
        if phone is not None:
            data["phone"] = phone
        if company is not None:
            data["company"] = company
        if custom_fields is not None:
            data["custom_fields"] = custom_fields

        self._logger.info(f"Updating lead {lead_id}")
        result = await self._request("PUT", f"/leads/{lead_id}", data=data)

        return Lead(
            id=str(result.get("id", "")),
            list_id=str(result.get("list_id", "")),
            name=result.get("name"),
            email=result.get("email"),
            phone=result.get("phone"),
            company=result.get("company"),
            custom_fields=result.get("custom_fields"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def search_leads(
        self,
        list_id: str,
        query: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Lead]:
        """
        Search leads in a list.

        Args:
            list_id: ID of the list to search
            query: Search query
            status: Filter by status
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of matching leads

        Raises:
            MyphonerClientError: On API errors
        """
        params = {
            "list_id": list_id,
            "limit": limit,
            "offset": offset
        }
        if query:
            params["q"] = query
        if status:
            params["status"] = status

        self._logger.info(f"Searching leads in list {list_id}")
        result = await self._request("GET", "/leads", params=params)

        leads = []
        for item in result.get("leads", []):
            leads.append(Lead(
                id=str(item.get("id", "")),
                list_id=list_id,
                name=item.get("name"),
                email=item.get("email"),
                phone=item.get("phone"),
                company=item.get("company"),
                status=item.get("status"),
                loser_reason=item.get("loser_reason"),
                winner_reason=item.get("winner_reason"),
                callback_time=item.get("callback_time"),
                custom_fields=item.get("custom_fields"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return leads

    async def mark_winner(
        self,
        lead_id: str,
        reason: Optional[str] = None
    ) -> Lead:
        """
        Mark a lead as winner.

        Args:
            lead_id: ID of the lead
            reason: Optional reason for winning

        Returns:
            Updated lead object

        Raises:
            MyphonerClientError: On API errors
        """
        data = {"status": "winner"}
        if reason:
            data["winner_reason"] = reason

        self._logger.info(f"Marking lead {lead_id} as winner")
        result = await self._request("PUT", f"/leads/{lead_id}", data=data)

        return Lead(
            id=str(result.get("id", "")),
            list_id=str(result.get("list_id", "")),
            name=result.get("name"),
            email=result.get("email"),
            phone=result.get("phone"),
            company=result.get("company"),
            status=result.get("status"),
            winner_reason=result.get("winner_reason"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def mark_loser(
        self,
        lead_id: str,
        reason: Optional[str] = None
    ) -> Lead:
        """
        Mark a lead as loser.

        Args:
            lead_id: ID of the lead
            reason: Optional reason for losing

        Returns:
            Updated lead object

        Raises:
            MyphonerClientError: On API errors
        """
        data = {"status": "loser"}
        if reason:
            data["loser_reason"] = reason

        self._logger.info(f"Marking lead {lead_id} as loser")
        result = await self._request("PUT", f"/leads/{lead_id}", data=data)

        return Lead(
            id=str(result.get("id", "")),
            list_id=str(result.get("list_id", "")),
            name=result.get("name"),
            email=result.get("email"),
            phone=result.get("phone"),
            company=result.get("company"),
            status=result.get("status"),
            loser_reason=result.get("loser_reason"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def mark_callback(
        self,
        lead_id: str,
        callback_time: str
    ) -> Lead:
        """
        Mark a lead for callback.

        Args:
            lead_id: ID of the lead
            callback_time: ISO datetime string for callback

        Returns:
            Updated lead object

        Raises:
            MyphonerClientError: On API errors
        """
        data = {
            "status": "callback",
            "callback_time": callback_time
        }

        self._logger.info(f"Marking lead {lead_id} for callback at {callback_time}")
        result = await self._request("PUT", f"/leads/{lead_id}", data=data)

        return Lead(
            id=str(result.get("id", "")),
            list_id=str(result.get("list_id", "")),
            name=result.get("name"),
            email=result.get("email"),
            phone=result.get("phone"),
            company=result.get("company"),
            status=result.get("status"),
            callback_time=result.get("callback_time"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def list_columns(self, list_id: str) -> List[Column]:
        """
        List columns in a list.

        Args:
            list_id: ID of the list

        Returns:
            List of columns

        Raises:
            MyphonerClientError: On API errors
        """
        self._logger.info(f"Listing columns for list {list_id}")
        result = await self._request("GET", f"/lists/{list_id}/columns")

        columns = []
        for item in result.get("columns", []):
            columns.append(Column(
                id=str(item.get("id", "")),
                list_id=list_id,
                name=item.get("name", ""),
                position=item.get("position", 0)
            ))

        return columns