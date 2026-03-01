"""
Teamleader API - Team and Project Management Client

Supports:
- Companies management
- Contacts management
- Deals management
- Invoices management
- Meetings and calls
- Tags management
"""

import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import os


@dataclass
class Company:
    """Company information"""
    company_id: str
    name: str
    vat_number: Optional[str]
    website: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    billing_country: Optional[str]
    status: str
    created_at: str
    updated_at: str


@dataclass
class Contact:
    """Contact information"""
    contact_id: str
    first_name: Optional[str]
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    mobile: Optional[str]
    company_id: Optional[str]
    status: str
    created_at: str
    updated_at: str


@dataclass
class Deal:
    """Deal information"""
    deal_id: str
    title: str
    status: str
    phase: str
    amount: Optional[float]
    currency: Optional[str]
    expected_close_date: Optional[str]
    contact_id: Optional[str]
    company_id: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Invoice:
    """Invoice information"""
    invoice_id: str
    invoice_number: str
    contact_id: str
    company_id: Optional[str]
    amount: float
    currency: str
    status: str
    due_date: Optional[str]
    created_at: str
    updated_at: str


class TeamleaderClient:
    """
    Teamleader API client for team and project management.

    API Documentation: https://lp.yoom.fun/apps/teamleader
    Requires API key from Yoom integration.
    """

    BASE_URL = "https://api.teamleader.eu/v1"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize Teamleader client.

        Args:
            api_key: API key (defaults to YOOM_TEAMLEADER_API_KEY env var)
            base_url: Custom base URL for testing
        """
        self.api_key = api_key or os.environ.get("YOOM_TEAMLEADER_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set YOOM_TEAMLEADER_API_KEY environment variable")

        self.base_url = base_url or self.BASE_URL
        self.session = None
        self._rate_limit_delay = 0.3  # 300ms between requests

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request with rate limiting"""
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async with statement")

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        headers["Content-Type"] = "application/json"

        # Rate limiting
        await asyncio.sleep(self._rate_limit_delay)

        url = f"{self.base_url}{endpoint}"

        async with self.session.request(method, url, headers=headers, **kwargs) as response:
            if response.status == 429:
                retry_after = int(response.headers.get("Retry-After", 2))
                await asyncio.sleep(retry_after)
                return await self._request(method, endpoint, **kwargs)

            if response.status >= 400:
                error_text = await response.text()
                raise Exception(f"API error {response.status}: {error_text}")

            if response.status == 204:
                return {}

            return await response.json()

    # ==================== Company Operations ====================

    async def create_company(self, company_data: Dict[str, Any]) -> Company:
        """Create a new company"""
        data = await self._request("POST", "/companies", json=company_data)

        return Company(
            company_id=data.get("id", ""),
            name=data.get("name", ""),
            vat_number=data.get("vat_number"),
            website=data.get("website"),
            phone=data.get("phone"),
            email=data.get("email"),
            billing_country=data.get("billing_country"),
            status=data.get("status", "active"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def get_company_info(self, company_id: str) -> Company:
        """Get company information"""
        data = await self._request("GET", f"/companies/{company_id}")

        return Company(
            company_id=data.get("id", company_id),
            name=data.get("name", ""),
            vat_number=data.get("vat_number"),
            website=data.get("website"),
            phone=data.get("phone"),
            email=data.get("email"),
            billing_country=data.get("billing_country"),
            status=data.get("status", "active"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def update_company(self, company_id: str, update_data: Dict[str, Any]) -> Company:
        """Update company"""
        data = await self._request("PATCH", f"/companies/{company_id}", json=update_data)

        return Company(
            company_id=data.get("id", company_id),
            name=data.get("name", ""),
            vat_number=data.get("vat_number"),
            website=data.get("website"),
            phone=data.get("phone"),
            email=data.get("email"),
            billing_country=data.get("billing_country"),
            status=data.get("status", "active"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def delete_company(self, company_id: str) -> Dict[str, Any]:
        """Delete company"""
        return await self._request("DELETE", f"/companies/{company_id}")

    async def search_companies(self, **filters) -> List[Company]:
        """Search companies"""
        data = await self._request("GET", "/companies", params=filters)

        companies = []
        for item in data.get("data", []):
            companies.append(Company(
                company_id=item.get("id", ""),
                name=item.get("name", ""),
                vat_number=item.get("vat_number"),
                website=item.get("website"),
                phone=item.get("phone"),
                email=item.get("email"),
                billing_country=item.get("billing_country"),
                status=item.get("status", "active"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return companies

    async def add_tag_to_company(self, company_id: str, tag_id: str) -> Dict[str, Any]:
        """Add tag to company"""
        return await self._request("POST", f"/companies/{company_id}/tags", json={"tag_id": tag_id})

    async def remove_tag_from_company(self, company_id: str, tag_id: str) -> Dict[str, Any]:
        """Remove tag from company"""
        return await self._request("DELETE", f"/companies/{company_id}/tags/{tag_id}")

    # ==================== Contact Operations ====================

    async def create_contact(self, contact_data: Dict[str, Any]) -> Contact:
        """Create a new contact"""
        data = await self._request("POST", "/contacts", json=contact_data)

        return Contact(
            contact_id=data.get("id", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            mobile=data.get("mobile"),
            company_id=data.get("company_id"),
            status=data.get("status", "active"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def get_contact_info(self, contact_id: str) -> Contact:
        """Get contact information"""
        data = await self._request("GET", f"/contacts/{contact_id}")

        return Contact(
            contact_id=data.get("id", contact_id),
            first_name=data.get("first_name"),
            last_name=data.get("last_name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            mobile=data.get("mobile"),
            company_id=data.get("company_id"),
            status=data.get("status", "active"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def update_contact(self, contact_id: str, update_data: Dict[str, Any]) -> Contact:
        """Update contact"""
        data = await self._request("PATCH", f"/contacts/{contact_id}", json=update_data)

        return Contact(
            contact_id=data.get("id", contact_id),
            first_name=data.get("first_name"),
            last_name=data.get("last_name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            mobile=data.get("mobile"),
            company_id=data.get("company_id"),
            status=data.get("status", "active"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """Delete contact"""
        return await self._request("DELETE", f"/contacts/{contact_id}")

    async def search_contacts(self, **filters) -> List[Contact]:
        """Search contacts"""
        data = await self._request("GET", "/contacts", params=filters)

        contacts = []
        for item in data.get("data", []):
            contacts.append(Contact(
                contact_id=item.get("id", ""),
                first_name=item.get("first_name"),
                last_name=item.get("last_name", ""),
                email=item.get("email"),
                phone=item.get("phone"),
                mobile=item.get("mobile"),
                company_id=item.get("company_id"),
                status=item.get("status", "active"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return contacts

    async def contact_link_company(self, contact_id: str, company_id: str) -> Dict[str, Any]:
        """Link contact to company"""
        return await self._request("POST", f"/contacts/{contact_id}/company", json={"company_id": company_id})

    async def add_tag_to_contact(self, contact_id: str, tag_id: str) -> Dict[str, Any]:
        """Add tag to contact"""
        return await self._request("POST", f"/contacts/{contact_id}/tags", json={"tag_id": tag_id})

    async def remove_tag_from_contact(self, contact_id: str, tag_id: str) -> Dict[str, Any]:
        """Remove tag from contact"""
        return await self._request("DELETE", f"/contacts/{contact_id}/tags/{tag_id}")

    # ==================== Deal Operations ====================

    async def create_deal(self, deal_data: Dict[str, Any]) -> Deal:
        """Create a new deal"""
        data = await self._request("POST", "/deals", json=deal_data)

        return Deal(
            deal_id=data.get("id", ""),
            title=data.get("title", ""),
            status=data.get("status", "open"),
            phase=data.get("phase", ""),
            amount=data.get("amount"),
            currency=data.get("currency"),
            expected_close_date=data.get("expected_close_date"),
            contact_id=data.get("contact_id"),
            company_id=data.get("company_id"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def get_deal_info(self, deal_id: str) -> Deal:
        """Get deal information"""
        data = await self._request("GET", f"/deals/{deal_id}")

        return Deal(
            deal_id=data.get("id", deal_id),
            title=data.get("title", ""),
            status=data.get("status", "open"),
            phase=data.get("phase", ""),
            amount=data.get("amount"),
            currency=data.get("currency"),
            expected_close_date=data.get("expected_close_date"),
            contact_id=data.get("contact_id"),
            company_id=data.get("company_id"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def update_deal(self, deal_id: str, update_data: Dict[str, Any]) -> Deal:
        """Update deal"""
        data = await self._request("PATCH", f"/deals/{deal_id}", json=update_data)

        return Deal(
            deal_id=data.get("id", deal_id),
            title=data.get("title", ""),
            status=data.get("status", "open"),
            phase=data.get("phase", ""),
            amount=data.get("amount"),
            currency=data.get("currency"),
            expected_close_date=data.get("expected_close_date"),
            contact_id=data.get("contact_id"),
            company_id=data.get("company_id"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def delete_deal(self, deal_id: str) -> Dict[str, Any]:
        """Delete deal"""
        return await self._request("DELETE", f"/deals/{deal_id}")

    async def search_deals(self, **filters) -> List[Deal]:
        """Search deals"""
        data = await self._request("GET", "/deals", params=filters)

        deals = []
        for item in data.get("data", []):
            deals.append(Deal(
                deal_id=item.get("id", ""),
                title=item.get("title", ""),
                status=item.get("status", "open"),
                phase=item.get("phase", ""),
                amount=item.get("amount"),
                currency=item.get("currency"),
                expected_close_date=item.get("expected_close_date"),
                contact_id=item.get("contact_id"),
                company_id=item.get("company_id"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return deals

    async def move_deal(self, deal_id: str, phase_id: str) -> Deal:
        """Move deal to a new phase"""
        return await self.update_deal(deal_id, {"phase_id": phase_id})

    async def win_deal(self, deal_id: str) -> Deal:
        """Mark deal as won"""
        return await self.update_deal(deal_id, {"status": "won"})

    async def lose_deal(self, deal_id: str, reason: Optional[str] = None) -> Deal:
        """Mark deal as lost"""
        update_data = {"status": "lost"}
        if reason:
            update_data["lost_reason"] = reason
        return await self.update_deal(deal_id, update_data)

    # ==================== Invoice Operations ====================

    async def create_invoice(self, invoice_data: Dict[str, Any]) -> Invoice:
        """Create a new invoice"""
        data = await self._request("POST", "/invoices", json=invoice_data)

        return Invoice(
            invoice_id=data.get("id", ""),
            invoice_number=data.get("invoice_number", ""),
            contact_id=data.get("contact_id", ""),
            company_id=data.get("company_id"),
            amount=data.get("amount", 0.0),
            currency=data.get("currency", "EUR"),
            status=data.get("status", "draft"),
            due_date=data.get("due_date"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def send_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Send invoice to client"""
        return await self._request("POST", f"/invoices/{invoice_id}/send")

    async def download_invoice(self, invoice_id: str) -> bytes:
        """Download invoice PDF"""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = f"{self.base_url}/invoices/{invoice_id}/pdf"

        async with self.session.get(url, headers=headers) as response:
            if response.status >= 400:
                raise Exception(f"Download failed: {response.status}")
            return await response.read()

    # ==================== Meeting and Call Operations ====================

    async def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new meeting/event"""
        return await self._request("POST", "/events", json=event_data)

    async def meeting_schedule(self, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule a meeting"""
        return await self.create_event({"event_type": "meeting", **meeting_data})

    async def add_call(self, call_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a call record"""
        return await self.create_event({"event_type": "call", **call_data})

    # ==================== Webhook Handlers ====================

    async def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming webhook events"""
        event_type = payload.get("event_type")

        return {"status": "acknowledged", "event_type": event_type}