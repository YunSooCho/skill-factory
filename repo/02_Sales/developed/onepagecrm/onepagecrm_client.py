"""
OnepageCRM API - Simple CRM Client

Supports deals, contacts, companies, notes, and actions management.

API Actions (13):
1. Search Deals
2. Create Contact
3. Get Company
4. Get Deal
5. Update Contact
6. Create Deal
7. Search Companies
8. Create Note
9. Create Action
10. Search Contacts
11. Get Contact
12. Update Deal
13. Update Company
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
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    value: float = 0.0
    currency: str = "USD"
    probability: int = 50
    status: str = "open"
    expected_close: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Contact:
    """Contact data model"""
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    title: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    background: str = ""
    star: bool = False
    linked_in: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Company:
    """Company data model"""
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    website: Optional[str] = None
    address: Dict[str, Any] = field(default_factory=dict)
    phone: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Note:
    """Note data model"""
    id: Optional[int] = None
    contact_id: int
    description: str = ""
    created_at: Optional[str] = None


@dataclass
class Action:
    """Action/Task data model"""
    id: Optional[int] = None
    contact_id: int
    deal_id: Optional[int] = None
    description: str = ""
    status: str = "open"
    due_date: Optional[str] = None
    assigned_to: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class OnepageCRMClient:
    """
    OnepageCRM API client for simple CRM management.

    API Documentation: https://www.onepagecrm.com/api/
    Authentication: API Key via header
    Protocol: HTTPS REST API
    """

    BASE_URL = "https://app.onepagecrm.com/api/v3"
    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 0.5  # seconds between requests

    def __init__(self, user_id: str, api_key: str):
        """
        Initialize OnepageCRM client.

        Args:
            user_id: Your OnepageCRM user ID
            api_key: Your OnepageCRM API key
        """
        self.user_id = user_id
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
            "X-OnePageCRM-UID": self.user_id,
            "X-OnePageCRM-Key": self.api_key,
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
                        raise Exception("Invalid API credentials or unauthorized access")
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
            "deal": {
                "name": deal.name,
                "description": deal.description,
                "value": deal.value,
                "currency": deal.currency,
                "probability": deal.probability,
                "status": deal.status,
                "expected_close": deal.expected_close
            }
        }

        response = await self._request("POST", "/deals.json", json_data=deal_data)
        return Deal(**self._map_deal_data(response.get("deal", {})))

    async def get_deal(self, deal_id: int) -> Deal:
        """Get deal by ID (Get Deal)"""
        response = await self._request("GET", f"/deals/{deal_id}.json")
        return Deal(**self._map_deal_data(response.get("deal", {})))

    async def update_deal(self, deal_id: int, deal: Deal) -> Deal:
        """Update existing deal (Update Deal)"""
        deal_data = {
            "deal": {
                "name": deal.name,
                "description": deal.description,
                "value": deal.value,
                "currency": deal.currency,
                "probability": deal.probability,
                "status": deal.status,
                "expected_close": deal.expected_close
            }
        }

        response = await self._request("PUT", f"/deals/{deal_id}.json", json_data=deal_data)
        return Deal(**self._map_deal_data(response.get("deal", {})))

    async def search_deals(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        per_page: int = 50
    ) -> List[Deal]:
        """Search deals (Search Deals)"""
        params = {"page": page, "per_page": per_page}

        if query:
            params["q"] = query
        if status:
            params["s/status"] = status

        response = await self._request("GET", "/deals.json", params=params)
        deals_data = response.get("data", {}).get("deals", [])
        return [Deal(**self._map_deal_data(d)) for d in deals_data]

    def _map_deal_data(self, data: Dict) -> Dict:
        """Map OnepageCRM deal data to our Deal model"""
        return {
            "id": data.get("id"),
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "value": float(data.get("value", 0.0)),
            "currency": data.get("currency", "USD"),
            "probability": int(data.get("probability", 50)),
            "status": data.get("status", "open"),
            "expected_close": data.get("expected_close"),
            "created_at": data.get("created_at"),
            "updated_at": data.get("updated_at")
        }

    # ==================== Contact Operations ====================

    async def create_contact(self, contact: Contact) -> Contact:
        """Create a new contact (Create Contact)"""
        contact_data = {
            "contact": {
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "title": contact.title,
                "company_name": contact.company_name,
                "phones": [
                    {"phone_number": contact.phone, "type": "work"},
                    {"phone_number": contact.mobile, "type": "mobile"}
                ] if contact.phone or contact.mobile else [],
                "emails": [{"email": contact.email, "type": "work"}] if contact.email else [],
                "background": contact.background,
                "star": contact.star,
                "urls": [
                    {"url": contact.linked_in, "type": "LinkedIn"},
                    {"url": contact.facebook, "type": "Facebook"},
                    {"url": contact.twitter, "type": "Twitter"}
                ] if contact.linked_in or contact.facebook or contact.twitter else []
            }
        }

        response = await self._request("POST", "/contacts.json", json_data=contact_data)
        return Contact(**self._map_contact_data(response.get("contact", {})))

    async def get_contact(self, contact_id: int) -> Contact:
        """Get contact by ID (Get Contact)"""
        response = await self._request("GET", f"/contacts/{contact_id}.json")
        return Contact(**self._map_contact_data(response.get("contact", {})))

    async def update_contact(self, contact_id: int, contact: Contact) -> Contact:
        """Update existing contact (Update Contact)"""
        contact_data = {
            "contact": {
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "title": contact.title,
                "company_name": contact.company_name,
                "phones": [
                    {"phone_number": contact.phone, "type": "work"},
                    {"phone_number": contact.mobile, "type": "mobile"}
                ] if contact.phone or contact.mobile else [],
                "emails": [{"email": contact.email, "type": "work"}] if contact.email else [],
                "background": contact.background,
                "star": contact.star
            }
        }

        response = await self._request("PUT", f"/contacts/{contact_id}.json", json_data=contact_data)
        return Contact(**self._map_contact_data(response.get("contact", {})))

    async def search_contacts(
        self,
        query: Optional[str] = None,
        company_name: Optional[str] = None,
        page: int = 1,
        per_page: int = 50
    ) -> List[Contact]:
        """Search contacts (Search Contacts)"""
        params = {"page": page, "per_page": per_page}

        if query:
            params["q"] = query
        if company_name:
            params["s/company_name"] = company_name

        response = await self._request("GET", "/contacts.json", params=params)
        contacts_data = response.get("data", {}).get("contacts", [])
        return [Contact(**self._map_contact_data(c)) for c in contacts_data]

    def _map_contact_data(self, data: Dict) -> Dict:
        """Map OnepageCRM contact data to our Contact model"""
        phones = data.get("phones", [])
        emails = data.get("emails", [])
        urls = data.get("urls", [])

        return {
            "id": data.get("id"),
            "first_name": data.get("first_name", ""),
            "last_name": data.get("last_name", ""),
            "title": data.get("title"),
            "company_name": data.get("company_name"),
            "email": emails[0]["email"] if emails else None,
            "phone": next((p["phone_number"] for p in phones if p.get("type") == "work"), None),
            "mobile": next((p["phone_number"] for p in phones if p.get("type") == "mobile"), None),
            "background": data.get("background", ""),
            "star": data.get("star", False),
            "linked_in": next((u["url"] for u in urls if u.get("type") == "LinkedIn"), None),
            "facebook": next((u["url"] for u in urls if u.get("type") == "Facebook"), None),
            "twitter": next((u["url"] for u in urls if u.get("type") == "Twitter"), None),
            "created_at": data.get("created_at"),
            "updated_at": data.get("updated_at")
        }

    # ==================== Company Operations ====================

    async def get_company(self, company_id: int) -> Company:
        """Get company by ID (Get Company)"""
        response = await self._request("GET", f"/companies/{company_id}.json")
        return Company(**self._map_company_data(response.get("company", {})))

    async def update_company(self, company_id: int, company: Company) -> Company:
        """Update existing company (Update Company)"""
        company_data = {
            "company": {
                "name": company.name,
                "description": company.description,
                "website": company.website,
                "phone": company.phone
            }
        }

        response = await self._request("PUT", f"/companies/{company_id}.json", json_data=company_data)
        return Company(**self._map_company_data(response.get("company", {})))

    async def search_companies(
        self,
        query: Optional[str] = None,
        page: int = 1,
        per_page: int = 50
    ) -> List[Company]:
        """Search companies (Search Companies)"""
        params = {"page": page, "per_page": per_page}

        if query:
            params["q"] = query

        response = await self._request("GET", "/companies.json", params=params)
        companies_data = response.get("data", {}).get("companies", [])
        return [Company(**self._map_company_data(c)) for c in companies_data]

    def _map_company_data(self, data: Dict) -> Dict:
        """Map OnepageCRM company data to our Company model"""
        return {
            "id": data.get("id"),
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "website": data.get("website"),
            "address": data.get("address", {}),
            "phone": data.get("phone"),
            "created_at": data.get("created_at"),
            "updated_at": data.get("updated_at")
        }

    # ==================== Note Operations ====================

    async def create_note(self, note: Note) -> Note:
        """Create a new note (Create Note)"""
        note_data = {
            "note": {
                "contact_id": note.contact_id,
                "description": note.description
            }
        }

        response = await self._request("POST", "/notes.json", json_data=note_data)
        return Note(**response.get("note", {}))

    # ==================== Action Operations ====================

    async def create_action(self, action: Action) -> Action:
        """Create a new action (Create Action)"""
        action_data = {
            "action": {
                "contact_id": action.contact_id,
                "deal_id": action.deal_id,
                "description": action.description,
                "status": action.status,
                "due_date": action.due_date,
                "assigned_to": action.assigned_to
            }
        }

        response = await self._request("POST", "/actions.json", json_data=action_data)
        return Action(**response.get("action", {}))


# ==================== Example Usage ====================

async def main():
    """Example usage of OnepageCRM client"""

    user_id = "your_user_id"
    api_key = "your_onepagecrm_api_key"

    async with OnepageCRMClient(user_id=user_id, api_key=api_key) as client:
        # Create contact
        contact = Contact(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            company_name="Example Corp"
        )
        created_contact = await client.create_contact(contact)
        print(f"Created contact: {created_contact.first_name} {created_contact.last_name}")

        # Create deal
        deal = Deal(
            name="Software License",
            value=50000.0,
            status="open"
        )
        created_deal = await client.create_deal(deal)
        print(f"Created deal: {created_deal.name}")

        # Create note
        note = Note(
            contact_id=created_contact.id,
            description="Initial discussion completed"
        )
        created_note = await client.create_note(note)
        print(f"Created note: {created_note.id}")


if __name__ == "__main__":
    asyncio.run(main())