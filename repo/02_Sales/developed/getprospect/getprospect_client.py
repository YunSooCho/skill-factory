"""
Getprospect API - Lead Enrichment Client

Supports 13 API Actions:
- Create Contact
- Find Email
- Add Contacts to List
- Get Company by Name
- Verify Email Address
- Get Company by ID
- Get Lists
- Update Contact
- Search Contact
- Search by Email
- Create Company
- List Property
- Get Contact

Triggers:
- New Contact
"""

import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Contact:
    """Contact entity"""
    id: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    linkedin: Optional[str] = None
    phone: Optional[str] = None
    confidence: Optional[int] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Company:
    """Company entity"""
    id: str
    name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class EmailVerification:
    """Email verification result"""
    email: str
    valid: bool
    score: Optional[int] = None
    reason: Optional[str] = None


@dataclass
class ListInfo:
    """List entity"""
    id: str
    name: str
    contact_count: int = 0
    created_at: str = ""


class GetprospectClientError(Exception):
    """Base exception for Getprospect client errors"""
    pass


class GetprospectRateLimitError(GetprospectClientError):
    """Raised when rate limit is exceeded"""
    pass


class GetprospectClient:
    """
    Getprospect API client for lead enrichment and email verification.

    API Documentation: https://docs.getprospect.com/
    Uses API Key for authentication via Bearer token.
    """

    BASE_URL = "https://api.getprospect.com/public/v1"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize Getprospect client.

        Args:
            api_key: API key for authentication
            base_url: Optional custom base URL
        """
        self.api_key = api_key
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None
        self._rate_limit_remaining = 100
        self._rate_limit_reset = 0

        logger = logging.getLogger("getprospect")
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
                        raise GetprospectClientError("Authentication failed")

                    elif response.status == 403:
                        raise GetprospectClientError("Forbidden - insufficient permissions")

                    elif response.status == 404:
                        raise GetprospectClientError("Resource not found")

                    elif response.status == 422:
                        error_data = await response.json()
                        raise GetprospectClientError(
                            f"Validation error: {error_data.get('message', 'Unknown error')}"
                        )

                    elif response.status == 429:
                        await self._handle_rate_limit()
                        retry_count += 1
                        continue

                    else:
                        error_text = await response.text()
                        raise GetprospectClientError(
                            f"API error {response.status}: {error_text}"
                        )

            except aiohttp.ClientError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise GetprospectClientError(f"Network error: {str(e)}")
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

    async def create_contact(
        self,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        company: Optional[str] = None,
        job_title: Optional[str] = None,
        linkedin: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Contact:
        """Create a new contact."""
        data = {
            "first_name": first_name,
            "last_name": last_name
        }
        if email:
            data["email"] = email
        if company:
            data["company"] = company
        if job_title:
            data["job_title"] = job_title
        if linkedin:
            data["linkedin"] = linkedin
        if phone:
            data["phone"] = phone

        self._logger.info(f"Creating contact: {first_name} {last_name}")
        result = await self._request("POST", "/contacts", data=data)

        return Contact(
            id=str(result.get("id", "")),
            first_name=first_name,
            last_name=last_name,
            email=result.get("email"),
            company=result.get("company"),
            job_title=result.get("job_title"),
            linkedin=result.get("linkedin"),
            phone=result.get("phone"),
            confidence=result.get("confidence"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def get_contact(self, contact_id: str) -> Contact:
        """Get a contact by ID."""
        self._logger.info(f"Getting contact {contact_id}")
        result = await self._request("GET", f"/contacts/{contact_id}".format(contact_id=contact_id))

        return Contact(
            id=str(result.get("id", "")),
            first_name=result.get("first_name", ""),
            last_name=result.get("last_name", ""),
            email=result.get("email"),
            company=result.get("company"),
            job_title=result.get("job_title"),
            linkedin=result.get("linkedin"),
            phone=result.get("phone"),
            confidence=result.get("confidence"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def update_contact(
        self,
        contact_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        job_title: Optional[str] = None
    ) -> Contact:
        """Update an existing contact."""
        data = {}
        if first_name is not None:
            data["first_name"] = first_name
        if last_name is not None:
            data["last_name"] = last_name
        if email is not None:
            data["email"] = email
        if company is not None:
            data["company"] = company
        if job_title is not None:
            data["job_title"] = job_title

        self._logger.info(f"Updating contact {contact_id}")
        result = await self._request("PUT", f"/contacts/{contact_id}".format(contact_id=contact_id), data=data)

        return Contact(
            id=str(result.get("id", "")),
            first_name=result.get("first_name", ""),
            last_name=result.get("last_name", ""),
            email=result.get("email"),
            company=result.get("company"),
            job_title=result.get("job_title"),
            linkedin=result.get("linkedin"),
            phone=result.get("phone"),
            confidence=result.get("confidence"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def search_contact(
        self,
        query: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Contact]:
        """Search for contacts."""
        params = {
            "q": query,
            "limit": limit,
            "offset": offset
        }

        self._logger.info(f"Searching contacts: {query}")
        result = await self._request("GET", "/contacts/search", params=params)

        contacts = []
        for item in result.get("data", []):
            contacts.append(Contact(
                id=str(item.get("id", "")),
                first_name=item.get("first_name", ""),
                last_name=item.get("last_name", ""),
                email=item.get("email"),
                company=item.get("company"),
                job_title=item.get("job_title"),
                linkedin=item.get("linkedin"),
                phone=item.get("phone"),
                confidence=item.get("confidence"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return contacts

    async def search_by_email(self, email: str) -> Optional[Contact]:
        """Find contact by email address."""
        self._logger.info(f"Searching contact by email: {email}")
        result = await self._request("GET", f"/contacts/email/{email}".format(email=email))

        if not result or "data" not in result:
            return None

        data = result["data"]
        return Contact(
            id=str(data.get("id", "")),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            email=data.get("email"),
            company=data.get("company"),
            job_title=data.get("job_title"),
            linkedin=data.get("linkedin"),
            phone=data.get("phone"),
            confidence=data.get("confidence"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def find_email(
        self,
        first_name: str,
        last_name: str,
        company: str
    ) -> Optional[EmailVerification]:
        """Find email address for a person."""
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "company": company
        }

        self._logger.info(f"Finding email for {first_name} {last_name} at {company}")
        result = await self._request("POST", "/emails/find", data=data)

        if not result or "data" not in result:
            return None

        data_obj = result["data"]
        return EmailVerification(
            email=data_obj.get("email", ""),
            valid=data_obj.get("valid", False),
            score=data_obj.get("score"),
            reason=data_obj.get("reason")
        )

    async def verify_email(self, email: str) -> EmailVerification:
        """Verify an email address."""
        self._logger.info(f"Verifying email: {email}")
        result = await self._request("POST", "/emails/verify", data={"email": email})

        data_obj = result.get("data", {})
        return EmailVerification(
            email=email,
            valid=data_obj.get("valid", False),
            score=data_obj.get("score"),
            reason=data_obj.get("reason")
        )

    async def create_company(
        self,
        name: str,
        domain: Optional[str] = None,
        industry: Optional[str] = None,
        size: Optional[str] = None,
        location: Optional[str] = None
    ) -> Company:
        """Create a new company."""
        data = {"name": name}
        if domain:
            data["domain"] = domain
        if industry:
            data["industry"] = industry
        if size:
            data["size"] = size
        if location:
            data["location"] = location

        self._logger.info(f"Creating company: {name}")
        result = await self._request("POST", "/companies", data=data)

        return Company(
            id=str(result.get("id", "")),
            name=result.get("name", ""),
            domain=result.get("domain"),
            industry=result.get("industry"),
            size=result.get("size"),
            location=result.get("location"),
            website=result.get("website"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def get_company_by_id(self, company_id: str) -> Company:
        """Get a company by ID."""
        self._logger.info(f"Getting company {company_id}")
        result = await self._request("GET", f"/companies/{company_id}".format(company_id=company_id))

        return Company(
            id=str(result.get("id", "")),
            name=result.get("name", ""),
            domain=result.get("domain"),
            industry=result.get("industry"),
            size=result.get("size"),
            location=result.get("location"),
            website=result.get("website"),
            created_at=result.get("created_at", ""),
            updated_at=result.get("updated_at", "")
        )

    async def get_company_by_name(self, name: str) -> Optional[Company]:
        """Get a company by name."""
        self._logger.info(f"Getting company by name: {name}")
        result = await self._request("GET", f"/companies/name/{name}".format(name=name))

        if not result or "data" not in result:
            return None

        data_obj = result["data"]
        return Company(
            id=str(data_obj.get("id", "")),
            name=data_obj.get("name", ""),
            domain=data_obj.get("domain"),
            industry=data_obj.get("industry"),
            size=data_obj.get("size"),
            location=data_obj.get("location"),
            website=data_obj.get("website"),
            created_at=data_obj.get("created_at", ""),
            updated_at=data_obj.get("updated_at", "")
        )

    async def get_lists(self, limit: int = 50, offset: int = 0) -> List[ListInfo]:
        """Get all lists."""
        params = {"limit": limit, "offset": offset}

        self._logger.info("Getting lists")
        result = await self._request("GET", "/lists", params=params)

        lists_obj = []
        for item in result.get("data", []):
            lists_obj.append(ListInfo(
                id=str(item.get("id", "")),
                name=item.get("name", ""),
                contact_count=item.get("contact_count", 0),
                created_at=item.get("created_at", "")
            ))

        return lists_obj

    async def add_contacts_to_list(
        self,
        list_id: str,
        contact_ids: List[str]
    ) -> Dict[str, Any]:
        """Add contacts to a list."""
        data = {
            "list_id": list_id,
            "contact_ids": contact_ids
        }

        self._logger.info(f"Adding {len(contact_ids)} contacts to list {list_id}")
        return await self._request("POST", "/lists/add-contacts", data=data)

    async def list_properties(self) -> Dict[str, Any]:
        """List available contact properties."""
        self._logger.info("Getting contact properties")
        return await self._request("GET", "/properties")