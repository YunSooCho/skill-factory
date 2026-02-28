"""
Sansan API - Business Card Management Client

Supports 9 API Actions:
- Get Business Card Info (名刺情報の取得)
- Register Business Card Image (名刺画像を登録)
- Get Contact List (コンタクト情報の一覧を取得)
- Get Business Card List (名刺情報の一覧を取得)
- Search Business Cards (名刺情報を検索)
- Get Business Card Image (名刺画像を取得)
- Get Person Info (人物情報を取得)
- Register Business Card Data (名刺データを登録)
- Get Business Card List with Date Range (名刺情報の一覧を取得（期間指定）)

Triggers:
- Business Card Updated (including tags)
- Business Card Updated
- Business Card Registered
- Business Card with Specific Tag Updated
- Contact Registered/Updated
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
    kana_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    company_name: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None
    address: Optional[str] = None
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None
    captured_date: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Contact:
    """Contact entity"""
    id: str
    person_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Person:
    """Person entity"""
    id: str
    name: str
    kana_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None
    company_id: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


class SansanClientError(Exception):
    """Base exception for Sansan client errors"""
    pass


class SansanRateLimitError(SansanClientError):
    """Raised when rate limit is exceeded"""
    pass


class SansanClient:
    """
    Sansan API client for business card management.

    API Documentation: https://researchers Sansan API - https://developers.sansan.com/
    Uses API Key for authentication via Basic Auth.
    """

    BASE_URL = "https://https://api.sansan.com/v1"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize Sansan client.

        Args:
            api_key: API key for authentication
            base_url: Optional custom base URL
        """
        self.api_key = api_key
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None
        self._rate_limit_remaining = 100
        self._rate_limit_reset = 0

        logger = logging.getLogger("sansan")
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
        import base64
        auth_string = base64.b64encode(
            f"{self.api_key}:".encode()
        ).decode()

        headers = {
            "Authorization": f"Basic {auth_string}",
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
                        raise SansanClientError("Authentication failed")

                    elif response.status == 403:
                        raise SansanClientError("Forbidden - insufficient permissions")

                    elif response.status == 404:
                        raise SansanClientError("Resource not found")

                    elif response.status == 422:
                        error_data = await response.json()
                        raise SansanClientError(
                            f"Validation error: {error_data.get('message', 'Unknown error')}"
                        )

                    elif response.status == 429:
                        await self._handle_rate_limit()
                        retry_count += 1
                        continue

                    else:
                        error_text = await response.text()
                        raise SansanClientError(
                            f"API error {response.status}: {error_text}"
                        )

            except aiohttp.ClientError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise SansanClientError(f"Network error: {str(e)}")
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

    async def get_business_card(self, card_id: str) -> BusinessCard:
        """
        Get business card information by ID.

        Args:
            card_id: Business card ID

        Returns:
            Business card object

        Raises:
            SansanClientError: On API errors
        """
        self._logger.info(f"Getting business card {card_id}")
        result = await self._request("GET", f"/businessCards/{card_id}".format(card_id=card_id))

        return BusinessCard(
            id=str(result.get("businessCard", {}).get("cardId", "")),
            name=result.get("businessCard", {}).get("person", {}).get("name", ""),
            kana_name=result.get("businessCard", {}).get("person", {}).get("kanaName"),
            email=result.get("businessCard", {}).get("person", {}).get("email"),
            phone=result.get("businessCard", {}).get("person", {}).get("phone"),
            mobile=result.get("businessCard", {}).get("person", {}).get("mobile"),
            company_name=result.get("businessCard", {}).get("company", {}).get("name"),
            department=result.get("businessCard", {}).get("person", {}).get("department"),
            title=result.get("businessCard", {}).get("person", {}).get("title"),
            address=result.get("businessCard", {}).get("person", {}).get("address"),
            tags=result.get("businessCard", {}).get("tags"),
            image_url=result.get("businessCard", {}).get("imageUrl"),
            captured_date=result.get("businessCard", {}).get("capturedDate"),
            created_at=result.get("businessCard", {}).get("createdAt", ""),
            updated_at=result.get("businessCard", {}).get("updatedAt", "")
        )

    async def get_business_card_list(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[BusinessCard]:
        """
        Get list of business cards.

        Args:
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of business card objects

        Raises:
            SansanClientError: On API errors
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        self._logger.info("Getting business card list")
        result = await self._request("GET", "/businessCards", params=params)

        cards = []
        for item in result.get("data", []):
            card_data = item.get("businessCard", {})
            cards.append(BusinessCard(
                id=str(card_data.get("cardId", "")),
                name=card_data.get("person", {}).get("name", ""),
                kana_name=card_data.get("person", {}).get("kanaName"),
                email=card_data.get("person", {}).get("email"),
                phone=card_data.get("person", {}).get("phone"),
                mobile=card_data.get("person", {}).get("mobile"),
                company_name=card_data.get("company", {}).get("name"),
                department=card_data.get("person", {}).get("department"),
                title=card_data.get("person", {}).get("title"),
                address=card_data.get("person", {}).get("address"),
                tags=card_data.get("tags"),
                image_url=card_data.get("imageUrl"),
                captured_date=card_data.get("capturedDate"),
                created_at=card_data.get("createdAt", ""),
                updated_at=card_data.get("updatedAt", "")
            ))

        return cards

    async def get_business_card_list_by_date(
        self,
        start_date: str,
        end_date: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[BusinessCard]:
        """
        Get business cards within a date range.

        Args:
            start_date: Start date ISO string
            end_date: End date ISO string
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of business card objects

        Raises:
            SansanClientError: On API errors
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "limit": limit,
            "offset": offset
        }

        self._logger.info(f"Getting business cards from {start_date} to {end_date}")
        result = await self._request("GET", "/businessCards", params=params)

        cards = []
        for item in result.get("data", []):
            card_data = item.get("businessCard", {})
            cards.append(BusinessCard(
                id=str(card_data.get("cardId", "")),
                name=card_data.get("person", {}).get("name", ""),
                kana_name=card_data.get("person", {}).get("kanaName"),
                email=card_data.get("person", {}).get("email"),
                phone=card_data.get("person", {}).get("phone"),
                mobile=card_data.get("person", {}).get("mobile"),
                company_name=card_data.get("company", {}).get("name"),
                department=card_data.get("person", {}).get("department"),
                title=card_data.get("person", {}).get("title"),
                address=card_data.get("person", {}).get("address"),
                tags=card_data.get("tags"),
                image_url=card_data.get("imageUrl"),
                captured_date=card_data.get("capturedDate"),
                created_at=card_data.get("createdAt", ""),
                updated_at=card_data.get("updatedAt", "")
            ))

        return cards

    async def search_business_cards(
        self,
        keyword: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[BusinessCard]:
        """
        Search for business cards by keyword.

        Args:
            keyword: Search keyword
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of matching business card objects

        Raises:
            SansanClientError: On API errors
        """
        params = {
            "keyword": keyword,
            "limit": limit,
            "offset": offset
        }

        self._logger.info(f"Searching business cards: {keyword}")
        result = await self._request("GET", "/businessCards/search", params=params)

        cards = []
        for item in result.get("data", []):
            card_data = item.get("businessCard", {})
            cards.append(BusinessCard(
                id=str(card_data.get("cardId", "")),
                name=card_data.get("person", {}).get("name", ""),
                kana_name=card_data.get("person", {}).get("kanaName"),
                email=card_data.get("person", {}).get("email"),
                phone=card_data.get("person", {}).get("phone"),
                mobile=card_data.get("person", {}).get("mobile"),
                company_name=card_data.get("company", {}).get("name"),
                department=card_data.get("person", {}).get("department"),
                title=card_data.get("person", {}).get("title"),
                address=card_data.get("person", {}).get("address"),
                tags=card_data.get("tags"),
                image_url=card_data.get("imageUrl"),
                captured_date=card_data.get("capturedDate"),
                created_at=card_data.get("createdAt", ""),
                updated_at=card_data.get("updatedAt", "")
            ))

        return cards

    async def get_business_card_image(self, card_id: str) -> str:
        """
        Get business card image URL.

        Args:
            card_id: Business card ID

        Returns:
            Image URL string

        Raises:
            SansanClientError: On API errors
        """
        self._logger.info(f"Getting business card image {card_id}")
        result = await self._request("GET", f"/businessCards/{card_id}/image".format(card_id=card_id))

        return result.get("imageUrl", "")

    async def register_business_card_image(
        self,
        image_data: bytes,
        file_name: str
    ) -> BusinessCard:
        """
        Register a new business card from image data.

        Args:
            image_data: Binary image data
            file_name: Name of the file

        Returns:
            Registered business card object

        Raises:
            SansanClientError: On API errors
        """
        import base64

        if not self.session:
            raise SansanClientError("Session not initialized. Use async context manager.")

        encoded_image = base64.b64encode(image_data).decode()

        data = {
            "file_name": file_name,
            "image_data": encoded_image
        }

        self._logger.info(f"Registering business card image: {file_name}")
        result = await self._request("POST", "/businessCards/image", data=data)

        card_data = result.get("businessCard", {})
        return BusinessCard(
            id=str(card_data.get("cardId", "")),
            name=card_data.get("person", {}).get("name", ""),
            kana_name=card_data.get("person", {}).get("kanaName"),
            image_url=card_data.get("imageUrl"),
            created_at=card_data.get("createdAt", ""),
            updated_at=card_data.get("updatedAt", "")
        )

    async def register_business_card_data(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company_name: Optional[str] = None,
        department: Optional[str] = None,
        title: Optional[str] = None,
        address: Optional[str] = None
    ) -> BusinessCard:
        """
        Register a new business card from data.

        Args:
            name: Person name
            email: Email address
            phone: Phone number
            company_name: Company name
            department: Department name
            title: Job title
            address: Address

        Returns:
            Registered business card object

        Raises:
            SansanClientError: On API errors
        """
        data = {
            "person": {
                "name": name
            }
        }
        if email:
            data["person"]["email"] = email
        if phone:
            data["person"]["phone"] = phone
        if department:
            data["person"]["department"] = department
        if title:
            data["person"]["title"] = title
        if address:
            data["person"]["address"] = address
        if company_name:
            data["company"] = {"name": company_name}

        self._logger.info(f"Registering business card data: {name}")
        result = await self._request("POST", "/businessCards", data=data)

        card_data = result.get("businessCard", {})
        return BusinessCard(
            id=str(card_data.get("cardId", "")),
            name=name,
            kana_name=card_data.get("person", {}).get("kanaName"),
            email=card_data.get("person", {}).get("email"),
            phone=card_data.get("person", {}).get("phone"),
            company_name=card_data.get("company", {}).get("name"),
            department=card_data.get("person", {}).get("department"),
            title=card_data.get("person", {}).get("title"),
            address=card_data.get("person", {}).get("address"),
            created_at=card_data.get("createdAt", ""),
            updated_at=card_data.get("updatedAt", "")
        )

    async def get_person_info(self, person_id: str) -> Person:
        """
        Get person information by ID.

        Args:
            person_id: Person ID

        Returns:
            Person object

        Raises:
            SansanClientError: On API errors
        """
        self._logger.info(f"Getting person {person_id}")
        result = await self._request("GET", f"/persons/{person_id}".format(person_id=person_id))

        return Person(
            id=str(result.get("person", {}).get("personId", "")),
            name=result.get("person", {}).get("name", ""),
            kana_name=result.get("person", {}).get("kanaName"),
            email=result.get("person", {}).get("email"),
            phone=result.get("person", {}).get("phone"),
            mobile=result.get("person", {}).get("mobile"),
            department=result.get("person", {}).get("department"),
            title=result.get("person", {}).get("title"),
            company_id=str(result.get("person", {}).get("companyId", "")) if result.get("person", {}).get("companyId") else None,
            created_at=result.get("person", {}).get("createdAt", ""),
            updated_at=result.get("person", {}).get("updatedAt", "")
        )

    async def get_contact_list(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[Contact]:
        """
        Get list of contacts.

        Args:
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of contact objects

        Raises:
            SansanClientError: On API errors
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        self._logger.info("Getting contact list")
        result = await self._request("GET", "/contacts", params=params)

        contacts = []
        for item in result.get("data", []):
            contact_data = item.get("contact", {})
            contacts.append(Contact(
                id=str(contact_data.get("contactId", "")),
                person_id=str(contact_data.get("personId", "")),
                name=contact_data.get("person", {}).get("name", ""),
                email=contact_data.get("person", {}).get("email"),
                phone=contact_data.get("person", {}).get("phone"),
                company_name=contact_data.get("company", {}).get("name"),
                created_at=contact_data.get("createdAt", ""),
                updated_at=contact_data.get("updatedAt", "")
            ))

        return contacts