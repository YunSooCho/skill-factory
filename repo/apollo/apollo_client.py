"""
Apollo API Client

Sales intelligence and prospecting platform for:
- Account management
- Contact management
- Enrichment for people and organizations
- Search and discover

API Actions (9):
1. アカウントを更新 (Update Account)
2. コンタクトを検索 (Search Contacts)
3. 人物情報のエンリッチメント (Enrich Person)
4. 組織情報のエンリッチメント (Enrich Organization)
5. 人物情報を検索 (Search People)
6. アカウントを検索 (Search Accounts)
7. コンタクトを作成 (Create Contact)
8. コンタクトを更新 (Update Contact)
9. アカウントを作成 (Create Account)

Triggers (3):
- コンタクトが作成されたら (When contact is created)
- コンタクトが更新されたら (When contact is updated)
- アカウントが作成されたら (When account is created)

Authentication: API Key
Base URL: https://api.apollo.io/v1
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Account:
    """Account model"""
    id: Optional[str] = None
    name: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    annual_revenue: Optional[float] = None
    founded_year: Optional[int] = None
    linkedin_url: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Contact:
    """Contact model"""
    id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    title: Optional[str] = None
    organization_id: Optional[str] = None
    organization_name: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class EnrichmentResult:
    """Enrichment result model"""
    id: Optional[str] = None
    type: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, calls_per_second: int = 10):
        self.calls_per_second = calls_per_second
        self.tokens = calls_per_second
        self.last_update = datetime.now()

    async def acquire(self):
        """Acquire a token from the rate limiter"""
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


class ApolloError(Exception):
    """Base exception for Apollo errors"""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}" if status_code else message)


class ApolloClient:
    """
    Apollo API Client

    Example usage:
        ```python
        client = ApolloClient(api_key="your_key")

        Search for contacts
        contacts = await client.search_contacts(first_name="John")

        Enrich person data
        result = await client.enrich_person(email="john@acme.com")

        Create account
        account = await client.create_account(name="Acme Corp")
        ```
    """

    def __init__(self, api_key: str, base_url: str = "https://api.apollo.io/v1"):
        """
        Initialize Apollo client

        Args:
            api_key: Apollo API key
            base_url: API base URL
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._headers = {
            "Content-Type": "application/json",
            "X-Api-Key": api_key
        }
        self._rate_limiter = RateLimiter(calls_per_second=10)

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Apollo API"""
        await self._rate_limiter.acquire()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method=method,
                    url=url,
                    headers=self._headers,
                    json=data,
                    params=params
                ) as response:
                    response_text = await response.text()

                    if response.status == 204:
                        return {"status": "success"}

                    if response.status >= 400:
                        try:
                            error_data = await response.json()
                            error_msg = error_data.get("message", error_data.get("error", "Unknown error"))
                        except:
                            error_msg = response_text if response_text else "HTTP error"
                        raise ApolloError(error_msg, response.status)

                    return await response.json()

            except aiohttp.ClientError as e:
                raise ApolloError(f"Network error: {str(e)}")
            except asyncio.TimeoutError:
                raise ApolloError("Request timeout")

    # Account methods

    async def create_account(self, data: Dict[str, Any]) -> Account:
        """
        アカウントを作成 (Create Account)

        Args:
            data: Account data (name, website, industry, etc.)

        Returns:
            Created Account object
        """
        if not data.get("name"):
            raise ApolloError("Account name is required")

        response = await self._make_request("POST", "/accounts/create", data=data)
        return Account(**response.get("account", {}))

    async def update_account(self, account_id: str, data: Dict[str, Any]) -> Account:
        """
        アカウントを更新 (Update Account)

        Args:
            account_id: Account ID
            data: Update data

        Returns:
            Updated Account object
        """
        data["account_id"] = account_id
        response = await self._make_request("POST", "/accounts/update", data=data)
        return Account(**response.get("account", {}))

    async def search_accounts(self, **params) -> List[Account]:
        """
        アカウントを検索 (Search Accounts)

        Args:
            **params: Search parameters (name, website, industry, etc.)

        Returns:
            List of Account objects
        """
        response = await self._make_request("GET", "/accounts/search", params=params)
        if "data" in response:
            return [Account(**item) for item in response["data"]]
        if "accounts" in response:
            return [Account(**item) for item in response["accounts"]]
        return []

    # Contact methods

    async def create_contact(self, data: Dict[str, Any]) -> Contact:
        """
        コンタクトを作成 (Create Contact)

        Args:
            data: Contact data (first_name, last_name, email, organization_id, etc.)

        Returns:
            Created Contact object
        """
        if not data.get("first_name") or not data.get("last_name"):
            raise ApolloError("Contact first_name and last_name are required")

        response = await self._make_request("POST", "/contacts/create", data=data)
        return Contact(**response.get("contact", {}))

    async def update_contact(self, contact_id: str, data: Dict[str, Any]) -> Contact:
        """
        コンタクトを更新 (Update Contact)

        Args:
            contact_id: Contact ID
            data: Update data

        Returns:
            Updated Contact object
        """
        data["contact_id"] = contact_id
        response = await self._make_request("POST", "/contacts/update", data=data)
        return Contact(**response.get("contact", {}))

    async def search_contacts(self, **params) -> List[Contact]:
        """
        コンタクトを検索 (Search Contacts)

        Args:
            **params: Search parameters (first_name, last_name, email, organization_id, etc.)

        Returns:
            List of Contact objects
        """
        response = await self._make_request("GET", "/contacts/search", params=params)
        if "data" in response:
            return [Contact(**item) for item in response["data"]]
        if "contacts" in response:
            return [Contact(**item) for item in response["contacts"]]
        return []

    async def search_people(self, **params) -> List[Contact]:
        """
        人物情報を検索 (Search People)

        Args:
            **params: Search parameters (name, title, organization_name, etc.)

        Returns:
            List of Contact objects (people)
        """
        response = await self._make_request("GET", "/people/search", params=params)
        if "data" in response:
            return [Contact(**item) for item in response["data"]]
        if "people" in response:
            return [Contact(**item) for item in response["people"]]
        return []

    # Enrichment methods

    async def enrich_person(self, **params) -> EnrichmentResult:
        """
        人物情報のエンリッチメント (Enrich Person)

        Args:
            **params: Enrichment parameters (email, linkedin_url, etc.)

        Returns:
            EnrichmentResult object with enriched data
        """
        response = await self._make_request("POST", "/people/enrich", data=params)
        return EnrichmentResult(
            id=response.get("id"),
            type="person",
            data=response.get("data"),
            confidence_score=response.get("confidence_score")
        )

    async def enrich_organization(self, **params) -> EnrichmentResult:
        """
        組織情報のエンリッチメント (Enrich Organization)

        Args:
            **params: Enrichment parameters (website, linkedin_url, name, etc.)

        Returns:
            EnrichmentResult object with enriched data
        """
        response = await self._make_request("POST", "/organizations/enrich", data=params)
        return EnrichmentResult(
            id=response.get("id"),
            type="organization",
            data=response.get("data"),
            confidence_score=response.get("confidence_score")
        )

    # Webhook handling

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process webhook event

        Triggers:
        - コンタクトが作成されたら (When contact is created)
        - コンタクトが更新されたら (When contact is updated)
        - アカウントが作成されたら (When account is created)

        Args:
            webhook_data: Webhook payload

        Returns:
            Processed event data
        """
        event_type = webhook_data.get("event_type", "unknown")
        entity_type = webhook_data.get("entity_type", "unknown")
        entity_id = webhook_data.get("entity_id")

        return {
            "event_type": event_type,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "data": webhook_data
        }