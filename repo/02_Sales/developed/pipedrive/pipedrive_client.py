"""
Pipedrive API - Sales CRM Client

Supports 28 API Actions:
- Search Organizations
- Delete Organization
- Update Lead
- Add Organization
- Add File
- Get Products for Deal
- Search Leads
- Create Activity
- Update Person
- Get Lead
- Update Organization
- Create User
- Add Deal
- Get People in Organization
- Add Person
- Update Activity
- Get Organization
- Get Deal
- Search People
- Get Person
- Delete Lead
- Add Note
- Delete Person
- Search Activities
- Update Deal
- Delete Deal
- Get Products
- Create Lead

Triggers:
- Deal Deleted
- Person Updated
- Organization Updated
- Deal Added
- Deal Updated
- Person Deleted
- Person Added
- Organization Deleted
- Organization Added
- Activity Added
"""

import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Person:
    """Person entity"""
    id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    organization_id: Optional[int] = None
    job_title: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Organization:
    """Organization entity"""
    id: int
    name: str
    owner_id: Optional[int] = None
    address: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Deal:
    """Deal entity"""
    id: int
    title: str
    value: float
    currency: str
    stage_id: Optional[int] = None
    person_id: Optional[int] = None
    organization_id: Optional[int] = None
    status: Optional[str] = None
    expected_close_date: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Lead:
    """Lead entity"""
    id: int
    title: str
    person_id: Optional[int] = None
    organization_id: Optional[int] = None
    status: Optional[str] = None
    value: Optional[float] = None
    currency: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Activity:
    """Activity entity"""
    id: int
    type: str
    subject: str
    due_date: Optional[str] = None
    person_id: Optional[int] = None
    deal_id: Optional[int] = None
    note: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Note:
    """Note entity"""
    id: int
    content: str
    person_id: Optional[int] = None
    deal_id: Optional[int] = None
    organization_id: Optional[int] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Product:
    """Product entity"""
    id: int
    name: str
    code: Optional[str] = None
    price: float = 0.0
    currency: str = "USD"
    created_at: str = ""
    updated_at: str = ""


@dataclass
class File:
    """File entity"""
    id: int
    name: str
    url: str
    file_type: Optional[str] = None
    size: int = 0
    created_at: str = ""


class PipedriveClientError(Exception):
    """Base exception for Pipedrive client errors"""
    pass


class PipedriveRateLimitError(PipedriveClientError):
    """Raised when rate limit is exceeded"""
    pass


class PipedriveClient:
    """
    Pipedrive API client for sales CRM.

    API Documentation: https://developers.pipedrive.com/docs/api/v1/
    Uses API Token for authentication via Basic Auth.
    """

    BASE_URL = "https://{company_domain}.pipedrive.com/api/v1"

    def __init__(self, api_token: str, company_domain: str):
        """
        Initialize Pipedrive client.

        Args:
            api_token: API token
            company_domain: Company domain (e.g., 'yourcompany' for yourcompany.pipedrive.com)
        """
        self.api_token = api_token
        self.company_domain = company_domain
        self.base_url = self.BASE_URL.format(company_domain=company_domain)
        self.session: Optional[aiohttp.ClientSession] = None
        self._rate_limit_remaining = 100
        self._rate_limit_reset = 0

        logger = logging.getLogger("pipedrive")
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
            f"{self.api_token}:".encode()
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
                        if result.get("success", False):
                            return result.get("data", {})
                        else:
                            raise PipedriveClientError(
                                result.get("error", "Unknown API error")
                            )

                    elif response.status == 204:
                        return {}

                    elif response.status == 401:
                        raise PipedriveClientError("Authentication failed")

                    elif response.status == 403:
                        raise PipedriveClientError("Forbidden - insufficient permissions")

                    elif response.status == 404:
                        raise PipedriveClientError("Resource not found")

                    elif response.status == 422:
                        error_data = await response.json()
                        raise PipedriveClientError(
                            f"Validation error: {error_data.get('error', 'Unknown error')}"
                        )

                    elif response.status == 429:
                        await self._handle_rate_limit()
                        retry_count += 1
                        continue

                    else:
                        error_text = await response.text()
                        raise PipedriveClientError(
                            f"API error {response.status}: {error_text}"
                        )

            except aiohttp.ClientError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise PipedriveClientError(f"Network error: {str(e)}")
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

    async def add_person(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        organization_id: Optional[int] = None,
        job_title: Optional[str] = None
    ) -> Person:
        """Add a new person."""
        data = {"name": name}
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if organization_id:
            data["org_id"] = organization_id
        if job_title:
            data["job_title"] = job_title

        self._logger.info(f"Adding person: {name}")
        result = await self._request("POST", "/persons", data=data)

        return Person(
            id=int(result.get("id", 0)),
            name=name,
            email=result.get("email"),
            phone=result.get("phone"),
            organization_id=result.get("org_id"),
            job_title=result.get("job_title"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def get_person(self, person_id: int) -> Person:
        """Get a person by ID."""
        self._logger.info(f"Getting person {person_id}")
        result = await self._request("GET", f"/persons/{person_id}".format(person_id=person_id))

        return Person(
            id=int(result.get("id", 0)),
            name=result.get("name", ""),
            email=result.get("email"),
            phone=result.get("phone"),
            organization_id=result.get("org_id"),
            job_title=result.get("job_title"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def update_person(
        self,
        person_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        job_title: Optional[str] = None
    ) -> Person:
        """Update a person."""
        data = {}
        if name is not None:
            data["name"] = name
        if email is not None:
            data["email"] = email
        if phone is not None:
            data["phone"] = phone
        if job_title is not None:
            data["job_title"] = job_title

        self._logger.info(f"Updating person {person_id}")
        result = await self._request("PUT", f"/persons/{person_id}".format(person_id=person_id), data=data)

        return Person(
            id=int(result.get("id", 0)),
            name=result.get("name", ""),
            email=result.get("email"),
            phone=result.get("phone"),
            organization_id=result.get("org_id"),
            job_title=result.get("job_title"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def delete_person(self, person_id: int) -> None:
        """Delete a person."""
        self._logger.info(f"Deleting person {person_id}")
        await self._request("DELETE", f"/persons/{person_id}".format(person_id=person_id))

    async def search_people(
        self,
        term: str,
        limit: int = 50,
        start: int = 0
    ) -> List[Person]:
        """Search for people."""
        params = {
            "term": term,
            "limit": limit,
            "start": start
        }

        self._logger.info(f"Searching people: {term}")
        result = await self._request("GET", "/persons/search", params=params)

        people = []
        for item in result.get("items", []):
            data = item.get("item", {})
            people.append(Person(
                id=int(data.get("id", 0)),
                name=data.get("name", ""),
                email=data.get("email"),
                phone=data.get("phone"),
                organization_id=data.get("org_id"),
                job_title=data.get("job_title"),
                created_at=data.get("add_time", ""),
                updated_at=data.get("update_time", "")
            ))

        return people

    async def get_people_in_organization(self, org_id: int) -> List[Person]:
        """Get all people in an organization."""
        self._logger.info(f"Getting people for organization {org_id}")
        result = await self._request("GET", f"/organizations/{org_id}/persons".format(org_id=org_id))

        people = []
        for item in result.get("data", []):
            people.append(Person(
                id=int(item.get("id", 0)),
                name=item.get("name", ""),
                email=item.get("email"),
                phone=item.get("phone"),
                organization_id=org_id,
                job_title=item.get("job_title"),
                created_at=item.get("add_time", ""),
                updated_at=item.get("update_time", "")
            ))

        return people

    async def add_organization(
        self,
        name: str,
        owner_id: Optional[int] = None,
        address: Optional[str] = None
    ) -> Organization:
        """Add a new organization."""
        data = {"name": name}
        if owner_id:
            data["owner_id"] = owner_id
        if address:
            data["address"] = address

        self._logger.info(f"Adding organization: {name}")
        result = await self._request("POST", "/organizations", data=data)

        return Organization(
            id=int(result.get("id", 0)),
            name=name,
            owner_id=result.get("owner_id"),
            address=result.get("address"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def get_organization(self, org_id: int) -> Organization:
        """Get an organization by ID."""
        self._logger.info(f"Getting organization {org_id}")
        result = await self._request("GET", f"/organizations/{org_id}".format(org_id=org_id))

        return Organization(
            id=int(result.get("id", 0)),
            name=result.get("name", ""),
            owner_id=result.get("owner_id"),
            address=result.get("address"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def update_organization(
        self,
        org_id: int,
        name: Optional[str] = None,
        owner_id: Optional[int] = None,
        address: Optional[str] = None
    ) -> Organization:
        """Update an organization."""
        data = {}
        if name is not None:
            data["name"] = name
        if owner_id is not None:
            data["owner_id"] = owner_id
        if address is not None:
            data["address"] = address

        self._logger.info(f"Updating organization {org_id}")
        result = await self._request("PUT", f"/organizations/{org_id}".format(org_id=org_id), data=data)

        return Organization(
            id=int(result.get("id", 0)),
            name=result.get("name", ""),
            owner_id=result.get("owner_id"),
            address=result.get("address"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def delete_organization(self, org_id: int) -> None:
        """Delete an organization."""
        self._logger.info(f"Deleting organization {org_id}")
        await self._request("DELETE", f"/organizations/{org_id}".format(org_id=org_id))

    async def search_organizations(
        self,
        term: str,
        limit: int = 50,
        start: int = 0
    ) -> List[Organization]:
        """Search for organizations."""
        params = {
            "term": term,
            "limit": limit,
            "start": start
        }

        self._logger.info(f"Searching organizations: {term}")
        result = await self._request("GET", "/organizations/search", params=params)

        orgs = []
        for item in result.get("items", []):
            data = item.get("item", {})
            orgs.append(Organization(
                id=int(data.get("id", 0)),
                name=data.get("name", ""),
                owner_id=data.get("owner_id"),
                address=data.get("address"),
                created_at=data.get("add_time", ""),
                updated_at=data.get("update_time", "")
            ))

        return orgs

    async def add_deal(
        self,
        title: str,
        value: float,
        currency: str,
        person_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        stage_id: Optional[int] = None
    ) -> Deal:
        """Add a new deal."""
        data = {
            "title": title,
            "value": value,
            "currency": currency
        }
        if person_id:
            data["person_id"] = person_id
        if organization_id:
            data["org_id"] = organization_id
        if stage_id:
            data["stage_id"] = stage_id

        self._logger.info(f"Adding deal: {title}")
        result = await self._request("POST", "/deals", data=data)

        return Deal(
            id=int(result.get("id", 0)),
            title=title,
            value=value,
            currency=currency,
            person_id=result.get("person_id"),
            organization_id=result.get("org_id"),
            stage_id=result.get("stage_id"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def get_deal(self, deal_id: int) -> Deal:
        """Get a deal by ID."""
        self._logger.info(f"Getting deal {deal_id}")
        result = await self._request("GET", f"/deals/{deal_id}".format(deal_id=deal_id))

        return Deal(
            id=int(result.get("id", 0)),
            title=result.get("title", ""),
            value=float(result.get("value", 0)),
            currency=result.get("currency", ""),
            person_id=result.get("person_id"),
            organization_id=result.get("org_id"),
            stage_id=result.get("stage_id"),
            status=result.get("status"),
            expected_close_date=result.get("expected_close_date"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def update_deal(
        self,
        deal_id: int,
        title: Optional[str] = None,
        value: Optional[float] = None,
        stage_id: Optional[int] = None,
        person_id: Optional[int] = None,
        organization_id: Optional[int] = None
    ) -> Deal:
        """Update a deal."""
        data = {}
        if title is not None:
            data["title"] = title
        if value is not None:
            data["value"] = value
        if stage_id is not None:
            data["stage_id"] = stage_id
        if person_id is not None:
            data["person_id"] = person_id
        if organization_id is not None:
            data["org_id"] = organization_id

        self._logger.info(f"Updating deal {deal_id}")
        result = await self._request("PUT", f"/deals/{deal_id}".format(deal_id=deal_id), data=data)

        return Deal(
            id=int(result.get("id", 0)),
            title=result.get("title", ""),
            value=float(result.get("value", 0)),
            currency=result.get("currency", ""),
            person_id=result.get("person_id"),
            organization_id=result.get("org_id"),
            stage_id=result.get("stage_id"),
            status=result.get("status"),
            expected_close_date=result.get("expected_close_date"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def delete_deal(self, deal_id: int) -> None:
        """Delete a deal."""
        self._logger.info(f"Deleting deal {deal_id}")
        await self._request("DELETE", f"/deals/{deal_id}".format(deal_id=deal_id))

    async def create_activity(
        self,
        type: str,
        subject: str,
        due_date: Optional[str] = None,
        person_id: Optional[int] = None,
        deal_id: Optional[int] = None,
        note: Optional[str] = None
    ) -> Activity:
        """Create a new activity."""
        data = {
            "type": type,
            "subject": subject
        }
        if due_date:
            data["due_date"] = due_date
        if person_id:
            data["person_id"] = person_id
        if deal_id:
            data["deal_id"] = deal_id
        if note:
            data["note"] = note

        self._logger.info(f"Creating activity: {subject}")
        result = await self._request("POST", "/activities", data=data)

        return Activity(
            id=int(result.get("id", 0)),
            type=type,
            subject=subject,
            due_date=result.get("due_date"),
            person_id=result.get("person_id"),
            deal_id=result.get("deal_id"),
            note=result.get("note"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def update_activity(
        self,
        activity_id: int,
        subject: Optional[str] = None,
        due_date: Optional[str] = None,
        note: Optional[str] = None
    ) -> Activity:
        """Update an activity."""
        data = {}
        if subject is not None:
            data["subject"] = subject
        if due_date is not None:
            data["due_date"] = due_date
        if note is not None:
            data["note"] = note

        self._logger.info(f"Updating activity {activity_id}")
        result = await self._request("PUT", f"/activities/{activity_id}".format(activity_id=activity_id), data=data)

        return Activity(
            id=int(result.get("id", 0)),
            type=result.get("type", ""),
            subject=result.get("subject", ""),
            due_date=result.get("due_date"),
            person_id=result.get("person_id"),
            deal_id=result.get("deal_id"),
            note=result.get("note"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def search_activities(
        self,
        user_id: Optional[int] = None,
        type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        start: int = 0
    ) -> List[Activity]:
        """Search for activities."""
        params = {"limit": limit, "start": start}
        if user_id:
            params["user_id"] = user_id
        if type:
            params["type"] = type
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        self._logger.info("Searching activities")
        result = await self._request("GET", "/activities", params=params)

        activities = []
        for item in result.get("data", []):
            activities.append(Activity(
                id=int(item.get("id", 0)),
                type=item.get("type", ""),
                subject=item.get("subject", ""),
                due_date=item.get("due_date"),
                person_id=item.get("person_id"),
                deal_id=item.get("deal_id"),
                note=item.get("note"),
                created_at=item.get("add_time", ""),
                updated_at=item.get("update_time", "")
            ))

        return activities

    async def add_note(
        self,
        content: str,
        person_id: Optional[int] = None,
        deal_id: Optional[int] = None,
        organization_id: Optional[int] = None
    ) -> Note:
        """Add a new note."""
        data = {"content": content}
        if person_id:
            data["person_id"] = person_id
        if deal_id:
            data["deal_id"] = deal_id
        if organization_id:
            data["org_id"] = organization_id

        self._logger.info("Adding note")
        result = await self._request("POST", "/notes", data=data)

        return Note(
            id=int(result.get("id", 0)),
            content=content,
            person_id=result.get("person_id"),
            deal_id=result.get("deal_id"),
            organization_id=result.get("org_id"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def create_lead(
        self,
        title: str,
        person_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        value: Optional[float] = None,
        currency: Optional[str] = None
    ) -> Lead:
        """Create a new lead."""
        data = {"title": title}
        if person_id:
            data["person_id"] = person_id
        if organization_id:
            data["organization_id"] = organization_id
        if value is not None:
            data["value"] = value
        if currency:
            data["currency"] = currency

        self._logger.info(f"Creating lead: {title}")
        result = await self._request("POST", "/leads", data=data)

        return Lead(
            id=int(result.get("id", 0)),
            title=title,
            person_id=result.get("person_id"),
            organization_id=result.get("organization_id"),
            status=result.get("status"),
            value=result.get("value"),
            currency=result.get("currency"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def get_lead(self, lead_id: int) -> Lead:
        """Get a lead by ID."""
        self._logger.info(f"Getting lead {lead_id}")
        result = await self._request("GET", f"/leads/{lead_id}".format(lead_id=lead_id))

        return Lead(
            id=int(result.get("id", 0)),
            title=result.get("title", ""),
            person_id=result.get("person_id"),
            organization_id=result.get("organization_id"),
            status=result.get("status"),
            value=result.get("value"),
            currency=result.get("currency"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def update_lead(
        self,
        lead_id: int,
        title: Optional[str] = None,
        person_id: Optional[int] = None,
        value: Optional[float] = None
    ) -> Lead:
        """Update a lead."""
        data = {}
        if title is not None:
            data["title"] = title
        if person_id is not None:
            data["person_id"] = person_id
        if value is not None:
            data["value"] = value

        self._logger.info(f"Updating lead {lead_id}")
        result = await self._request("PUT", f"/leads/{lead_id}".format(lead_id=lead_id), data=data)

        return Lead(
            id=int(result.get("id", 0)),
            title=result.get("title", ""),
            person_id=result.get("person_id"),
            organization_id=result.get("organization_id"),
            status=result.get("status"),
            value=result.get("value"),
            currency=result.get("currency"),
            created_at=result.get("add_time", ""),
            updated_at=result.get("update_time", "")
        )

    async def delete_lead(self, lead_id: int) -> None:
        """Delete a lead."""
        self._logger.info(f"Deleting lead {lead_id}")
        await self._request("DELETE", f"/leads/{lead_id}".format(lead_id=lead_id))

    async def search_leads(
        self,
        term: str,
        limit: int = 50,
        start: int = 0
    ) -> List[Lead]:
        """Search for leads."""
        params = {
            "term": term,
            "limit": limit,
            "start": start
        }

        self._logger.info(f"Searching leads: {term}")
        result = await self._request("GET", "/leads/search", params=params)

        leads = []
        for item in result.get("items", []):
            data = item.get("item", {})
            leads.append(Lead(
                id=int(data.get("id", 0)),
                title=data.get("title", ""),
                person_id=data.get("person_id"),
                organization_id=data.get("organization_id"),
                status=data.get("status"),
                value=data.get("value"),
                currency=data.get("currency"),
                created_at=data.get("add_time", ""),
                updated_at=data.get("update_time", "")
            ))

        return leads

    async def create_user(
        self,
        name: str,
        email: str
    ) -> Dict[str, Any]:
        """Create a new user."""
        data = {
            "name": name,
            "email": email
        }

        self._logger.info(f"Creating user: {name}")
        result = await self._request("POST", "/users", data=data)
        return result

    async def add_file(
        self,
        file_title: str,
        file_url: str,
        deal_id: Optional[int] = None,
        person_id: Optional[int] = None
    ) -> File:
        """Add a file."""
        data = {
            "file_title": file_title,
            "file_url": file_url
        }
        if deal_id:
            data["deal_id"] = deal_id
        if person_id:
            data["person_id"] = person_id

        self._logger.info(f"Adding file: {file_title}")
        result = await self._request("POST", "/files", data=data)

        return File(
            id=int(result.get("id", 0)),
            name=result.get("file_title", ""),
            url=result.get("file_url", ""),
            file_type=result.get("file_type"),
            created_at=result.get("add_time", "")
        )

    async def get_products_for_deal(self, deal_id: int) -> List[Product]:
        """Get products for a deal."""
        self._logger.info(f"Getting products for deal {deal_id}")
        result = await self._request("GET", f"/deals/{deal_id}/products".format(deal_id=deal_id))

        products = []
        for item in result.get("data", []):
            product_data = item.get("product", {})
            products.append(Product(
                id=int(product_data.get("id", 0)),
                name=product_data.get("name", ""),
                code=product_data.get("code"),
                price=float(product_data.get("price", 0)),
                currency=product_data.get("currency", "USD"),
                created_at=product_data.get("add_time", ""),
                updated_at=product_data.get("update_time", "")
            ))

        return products

    async def get_products(self, limit: int = 50, start: int = 0) -> List[Product]:
        """Get all products."""
        params = {"limit": limit, "start": start}

        self._logger.info("Getting products")
        result = await self._request("GET", "/products", params=params)

        products = []
        for item in result.get("data", []):
            products.append(Product(
                id=int(item.get("id", 0)),
                name=item.get("name", ""),
                code=item.get("code"),
                price=float(item.get("price", 0)),
                currency=item.get("currency", "USD"),
                created_at=item.get("add_time", ""),
                updated_at=item.get("update_time", "")
            ))

        return products