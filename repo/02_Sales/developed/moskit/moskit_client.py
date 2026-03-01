"""
Moskit CRM API - Sales Pipeline Management Client

Supports deals, companies, contacts, and activities management.

API Actions (20):
1. Delete Deal
2. Create Deal
3. Get Company
4. Delete Activity
5. Get Activity
6. Search Company
7. Search Contact
8. Search Deal
9. Delete Contact
10. Delete Company
11. Create Activity
12. Create Company
13. Update Activity
14. Create Contact
15. Update Deal
16. Update Contact
17. Update Company
18. Get Deal
19. Search Activity
20. Get Contact
"""

import aiohttp
import asyncio
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Deal:
    """Deal data model"""
    id: Optional[str] = None
    title: str = ""
    value: float = 0.0
    currency: str = "USD"
    pipeline_id: Optional[str] = None
    stage_id: Optional[str] = None
    contact_id: Optional[str] = None
    company_id: Optional[str] = None
    description: str = ""
    expected_close_date: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Company:
    """Company data model"""
    id: Optional[str] = None
    name: str = ""
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Contact:
    """Contact data model"""
    id: Optional[str] = None
    first_name: str = ""
    last_name: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    company_id: Optional[str] = None
    description: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Activity:
    """Activity data model"""
    id: Optional[str] = None
    deal_id: Optional[str] = None
    contact_id: Optional[str] = None
    type: str = ""
    description: str = ""
    date: Optional[str] = None
    duration: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class MoskitClient:
    """
    Moskit CRM API client for sales pipeline management.

    API Documentation: https://app.moskit.com/api/
    Authentication: API Key via header
    Protocol: HTTPS REST API
    """

    BASE_URL = "https://api.moskit.com/v1"
    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 0.5  # seconds between requests

    def __init__(self, api_key: str):
        """Initialize Moskit client"""
        self.api_key = api_key
        self.session = None
        self._last_request_time = 0

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _rate_limit(self):
        """Simple rate limiting"""
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self.RATE_LIMIT_DELAY:
            await asyncio.sleep(self.RATE_LIMIT_DELAY - time_since_last_request)
        self._last_request_time = time.time()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make API request with retry logic and error handling"""
        await self._rate_limit()

        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        url = f"{self.BASE_URL}{endpoint}"

        for attempt in range(self.MAX_RETRIES):
            try:
                async with self.session.request(
                    method,
                    url,
                    params=params,
                    json=json_data,
                    headers=headers
                ) as response:
                    data = await response.json()

                    if response.status in (200, 201, 204):
                        return data if data else {}
                    elif response.status == 401:
                        raise Exception("Invalid API key or unauthorized access")
                    elif response.status == 403:
                        raise Exception("Insufficient permissions")
                    elif response.status == 404:
                        raise Exception("Resource not found")
                    elif response.status == 429:
                        retry_after = int(response.headers.get("Retry-After", 5))
                        await asyncio.sleep(retry_after)
                        continue
                    elif 400 <= response.status < 500:
                        raise Exception(f"Client error: {data.get('message', 'Unknown error')}")
                    else:
                        raise Exception(f"Server error: {response.status} - {data}")

            except aiohttp.ClientError as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise Exception(f"Request failed after {self.MAX_RETRIES} attempts: {str(e)}")
                await asyncio.sleep(2 ** attempt)

    # ==================== Deal Operations ====================

    async def create_deal(self, deal: Deal) -> Deal:
        """Create a new deal (Create Deal)"""
        deal_data = {
            "title": deal.title,
            "value": deal.value,
            "currency": deal.currency,
            "pipeline_id": deal.pipeline_id,
            "stage_id": deal.stage_id,
            "contact_id": deal.contact_id,
            "company_id": deal.company_id,
            "description": deal.description,
            "expected_close_date": deal.expected_close_date
        }

        deal_data = {k: v for k, v in deal_data.items() if v is not None}

        response = await self._request("POST", "/deals", json_data=deal_data)
        return Deal(**response.get("data", {}))

    async def get_deal(self, deal_id: str) -> Deal:
        """Get deal by ID (Get Deal)"""
        response = await self._request("GET", f"/deals/{deal_id}")
        return Deal(**response.get("data", {}))

    async def update_deal(self, deal_id: str, deal: Deal) -> Deal:
        """Update existing deal (Update Deal)"""
        deal_data = {
            "title": deal.title,
            "value": deal.value,
            "currency": deal.currency,
            "stage_id": deal.stage_id,
            "contact_id": deal.contact_id,
            "company_id": deal.company_id,
            "description": deal.description,
            "expected_close_date": deal.expected_close_date
        }

        deal_data = {k: v for k, v in deal_data.items() if v is not None}

        response = await self._request("PUT", f"/deals/{deal_id}", json_data=deal_data)
        return Deal(**response.get("data", {}))

    async def delete_deal(self, deal_id: str) -> bool:
        """Delete deal (Delete Deal)"""
        await self._request("DELETE", f"/deals/{deal_id}")
        return True

    async def search_deals(
        self,
        query: Optional[str] = None,
        pipeline_id: Optional[str] = None,
        stage_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Deal]:
        """Search deals (Search Deal)"""
        params = {"limit": limit}

        if query:
            params["query"] = query
        if pipeline_id:
            params["pipeline_id"] = pipeline_id
        if stage_id:
            params["stage_id"] = stage_id

        response = await self._request("GET", "/deals", params=params)
        deals_data = response.get("data", [])
        return [Deal(**d) for d in deals_data]

    # ==================== Company Operations ====================

    async def create_company(self, company: Company) -> Company:
        """Create a new company (Create Company)"""
        company_data = {
            "name": company.name,
            "website": company.website,
            "industry": company.industry,
            "size": company.size,
            "phone": company.phone,
            "email": company.email,
            "address": company.address,
            "description": company.description
        }

        company_data = {k: v for k, v in company_data.items() if v is not None}

        response = await self._request("POST", "/companies", json_data=company_data)
        return Company(**response.get("data", {}))

    async def get_company(self, company_id: str) -> Company:
        """Get company by ID (Get Company)"""
        response = await self._request("GET", f"/companies/{company_id}")
        return Company(**response.get("data", {}))

    async def update_company(self, company_id: str, company: Company) -> Company:
        """Update existing company (Update Company)"""
        company_data = {
            "name": company.name,
            "website": company.website,
            "industry": company.industry,
            "size": company.size,
            "phone": company.phone,
            "email": company.email,
            "address": company.address,
            "description": company.description
        }

        company_data = {k: v for k, v in company_data.items() if v is not None}

        response = await self._request("PUT", f"/companies/{company_id}", json_data=company_data)
        return Company(**response.get("data", {}))

    async def delete_company(self, company_id: str) -> bool:
        """Delete company (Delete Company)"""
        await self._request("DELETE", f"/companies/{company_id}")
        return True

    async def search_company(
        self,
        query: Optional[str] = None,
        industry: Optional[str] = None,
        limit: int = 50
    ) -> List[Company]:
        """Search companies (Search Company)"""
        params = {"limit": limit}

        if query:
            params["query"] = query
        if industry:
            params["industry"] = industry

        response = await self._request("GET", "/companies", params=params)
        companies_data = response.get("data", [])
        return [Company(**c) for c in companies_data]

    # ==================== Contact Operations ====================

    async def create_contact(self, contact: Contact) -> Contact:
        """Create a new contact (Create Contact)"""
        contact_data = {
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "email": contact.email,
            "phone": contact.phone,
            "job_title": contact.job_title,
            "company_id": contact.company_id,
            "description": contact.description
        }

        contact_data = {k: v for k, v in contact_data.items() if v is not None}

        response = await self._request("POST", "/contacts", json_data=contact_data)
        return Contact(**response.get("data", {}))

    async def get_contact(self, contact_id: str) -> Contact:
        """Get contact by ID (Get Contact)"""
        response = await self._request("GET", f"/contacts/{contact_id}")
        return Contact(**response.get("data", {}))

    async def update_contact(self, contact_id: str, contact: Contact) -> Contact:
        """Update existing contact (Update Contact)"""
        contact_data = {
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "email": contact.email,
            "phone": contact.phone,
            "job_title": contact.job_title,
            "company_id": contact.company_id,
            "description": contact.description
        }

        contact_data = {k: v for k, v in contact_data.items() if v is not None}

        response = await self._request("PUT", f"/contacts/{contact_id}", json_data=contact_data)
        return Contact(**response.get("data", {}))

    async def delete_contact(self, contact_id: str) -> bool:
        """Delete contact (Delete Contact)"""
        await self._request("DELETE", f"/contacts/{contact_id}")
        return True

    async def search_contact(
        self,
        query: Optional[str] = None,
        company_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Contact]:
        """Search contacts (Search Contact)"""
        params = {"limit": limit}

        if query:
            params["query"] = query
        if company_id:
            params["company_id"] = company_id

        response = await self._request("GET", "/contacts", params=params)
        contacts_data = response.get("data", [])
        return [Contact(**c) for c in contacts_data]

    # ==================== Activity Operations ====================

    async def create_activity(self, activity: Activity) -> Activity:
        """Create a new activity (Create Activity)"""
        activity_data = {
            "deal_id": activity.deal_id,
            "contact_id": activity.contact_id,
            "type": activity.type,
            "description": activity.description,
            "date": activity.date,
            "duration": activity.duration
        }

        activity_data = {k: v for k, v in activity_data.items() if v is not None}

        response = await self._request("POST", "/activities", json_data=activity_data)
        return Activity(**response.get("data", {}))

    async def get_activity(self, activity_id: str) -> Activity:
        """Get activity by ID (Get Activity)"""
        response = await self._request("GET", f"/activities/{activity_id}")
        return Activity(**response.get("data", {}))

    async def update_activity(self, activity_id: str, activity: Activity) -> Activity:
        """Update existing activity (Update Activity)"""
        activity_data = {
            "type": activity.type,
            "description": activity.description,
            "date": activity.date,
            "duration": activity.duration
        }

        activity_data = {k: v for k, v in activity_data.items() if v is not None}

        response = await self._request("PUT", f"/activities/{activity_id}", json_data=activity_data)
        return Activity(**response.get("data", {}))

    async def delete_activity(self, activity_id: str) -> bool:
        """Delete activity (Delete Activity)"""
        await self._request("DELETE", f"/activities/{activity_id}")
        return True

    async def search_activity(
        self,
        type: Optional[str] = None,
        deal_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Activity]:
        """Search activities (Search Activity)"""
        params = {"limit": limit}

        if type:
            params["type"] = type
        if deal_id:
            params["deal_id"] = deal_id
        if contact_id:
            params["contact_id"] = contact_id

        response = await self._request("GET", "/activities", params=params)
        activities_data = response.get("data", [])
        return [Activity(**a) for a in activities_data]


# ==================== Example Usage ====================

async def main():
    """Example usage of Moskit client"""

    api_key = "your_moskit_api_key"

    async with MoskitClient(api_key=api_key) as client:
        # Create company
        company = Company(
            name="Example Corp",
            website="https://example.com",
            industry="Technology"
        )
        created_company = await client.create_company(company)
        print(f"Created company: {created_company.name}")

        # Create contact
        contact = Contact(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            company_id=created_company.id
        )
        created_contact = await client.create_contact(contact)
        print(f"Created contact: {created_contact.first_name} {created_contact.last_name}")

        # Create deal
        deal = Deal(
            title="Enterprise License",
            value=50000.0,
            contact_id=created_contact.id,
            company_id=created_company.id
        )
        created_deal = await client.create_deal(deal)
        print(f"Created deal: {created_deal.title}")


if __name__ == "__main__":
    asyncio.run(main())