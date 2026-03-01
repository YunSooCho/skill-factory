"""
Wild Apricot API - Membership Management Client

Supports:
- Contacts and members management
- Events and registrations
- Invoices and payments
- Donations management
"""

import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import os


@dataclass
class Contact:
    """Contact/Member information"""
    contact_id: str
    first_name: str
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    membership_level: Optional[str]
    membership_status: Optional[str]
    renew_date: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Event:
    """Event information"""
    event_id: str
    name: str
    start_date: str
    end_date: str
    location: Optional[str]
    capacity: Optional[int]
    created_at: str
    updated_at: str


@dataclass
class EventRegistration:
    """Event registration information"""
    registration_id: str
    event_id: str
    contact_id: str
    status: str
    registration_date: str
    amount: Optional[float]
    created_at: str
    updated_at: str


@dataclass
class Invoice:
    """Invoice information"""
    invoice_id: str
    contact_id: str
    amount: float
    status: str
    due_date: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Payment:
    """Payment information"""
    payment_id: str
    invoice_id: str
    amount: float
    status: str
    payment_date: str
    created_at: str


@dataclass
class Donation:
    """Donation information"""
    donation_id: str
    contact_id: str
    amount: float
    donation_date: str
    campaign: Optional[str]
    created_at: str


@dataclass
class Refund:
    """Refund information"""
    refund_id: str
    payment_id: str
    amount: float
    status: str
    refund_date: str
    created_at: str


class WildApricotClient:
    """
    Wild Apricot API client for membership management.

    API Documentation: https://lp.yoom.fun/apps/wild-apricot
    Requires API key from Yoom integration.
    """

    BASE_URL = "https://api.wildapricot.org/v2"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, account_id: Optional[str] = None):
        """
        Initialize Wild Apricot client.

        Args:
            api_key: API key (defaults to YOOM_WILDAPRICOT_API_KEY env var)
            base_url: Custom base URL for testing
            account_id: Wild Apricot account ID
        """
        self.api_key = api_key or os.environ.get("YOOM_WILDAPRICOT_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set YOOM_WILDAPRICOT_API_KEY environment variable")

        self.account_id = account_id or os.environ.get("YOOM_WILDAPRICOT_ACCOUNT_ID")
        if not self.account_id:
            raise ValueError("Account ID must be provided or set YOOM_WILDAPRICOT_ACCOUNT_ID environment variable")

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

        url = f"{self.base_url}/accounts/{self.account_id}{endpoint}"

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

    # ==================== Contact Operations ====================

    async def create_contact(self, contact_data: Dict[str, Any]) -> Contact:
        """Create a new contact/member"""
        data = await self._request("POST", "/contacts", json=contact_data)

        return Contact(
            contact_id=data.get("Id", ""),
            first_name=data.get("FirstName", ""),
            last_name=data.get("LastName", ""),
            email=data.get("Email"),
            phone=data.get("Phone"),
            membership_level=data.get("MembershipLevel"),
            membership_status=data.get("MembershipStatus"),
            renew_date=data.get("RenewDate"),
            created_at=data.get("Created", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("LastModified", datetime.now(timezone.utc).isoformat())
        )

    async def update_contact(self, contact_id: str, update_data: Dict[str, Any]) -> Contact:
        """Update contact"""
        data = await self._request("PUT", f"/contacts/{contact_id}", json=[update_data])

        return Contact(
            contact_id=data[0].get("Id", contact_id),
            first_name=data[0].get("FirstName", ""),
            last_name=data[0].get("LastName", ""),
            email=data[0].get("Email"),
            phone=data[0].get("Phone"),
            membership_level=data[0].get("MembershipLevel"),
            membership_status=data[0].get("MembershipStatus"),
            renew_date=data[0].get("RenewDate"),
            created_at=data[0].get("Created", ""),
            updated_at=data[0].get("LastModified", "")
        )

    async def search_contacts(self, **filters) -> List[Contact]:
        """Search contacts"""
        data = await self._request("GET", "/contacts", params=filters)

        contacts = []
        for item in data.get("Contacts", []):
            contacts.append(Contact(
                contact_id=item.get("Id", ""),
                first_name=item.get("FirstName", ""),
                last_name=item.get("LastName", ""),
                email=item.get("Email"),
                phone=item.get("Phone"),
                membership_level=item.get("MembershipLevel"),
                membership_status=item.get("MembershipStatus"),
                renew_date=item.get("RenewDate"),
                created_at=item.get("Created", ""),
                updated_at=item.get("LastModified", "")
            ))

        return contacts

    async def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """Delete contact"""
        return await self._request("DELETE", f"/contacts/{contact_id}")

    # ==================== Event Operations ====================

    async def search_events(self, **filters) -> List[Event]:
        """Search events"""
        data = await self._request("GET", "/events", params=filters)

        events = []
        for item in data.get("Events", []):
            events.append(Event(
                event_id=item.get("Id", ""),
                name=item.get("Name", ""),
                start_date=item.get("StartDate", ""),
                end_date=item.get("EndDate", ""),
                location=item.get("Location"),
                capacity=item.get("Capacity"),
                created_at=item.get("Created", ""),
                updated_at=item.get("LastModified", "")
            ))

        return events

    # ==================== Event Registration Operations ====================

    async def create_event_registration(self, registration_data: Dict[str, Any]) -> EventRegistration:
        """Create event registration"""
        data = await self._request("POST", "/eventregistrations", json=registration_data)

        return EventRegistration(
            registration_id=data.get("Id", ""),
            event_id=data.get("EventId", ""),
            contact_id=data.get("ContactId", ""),
            status=data.get("RegistrationStatus", ""),
            registration_date=data.get("RegistrationDate", ""),
            amount=data.get("Amount"),
            created_at=data.get("Created", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("LastModified", datetime.now(timezone.utc).isoformat())
        )

    async def update_event_registration(self, registration_id: str, update_data: Dict[str, Any]) -> EventRegistration:
        """Update event registration"""
        data = await self._request("PUT", f"/eventregistrations/{registration_id}", json=[update_data])

        return EventRegistration(
            registration_id=data[0].get("Id", registration_id),
            event_id=data[0].get("EventId", ""),
            contact_id=data[0].get("ContactId", ""),
            status=data[0].get("RegistrationStatus", ""),
            registration_date=data[0].get("RegistrationDate", ""),
            amount=data[0].get("Amount"),
            created_at=data[0].get("Created", ""),
            updated_at=data[0].get("LastModified", "")
        )

    async def search_event_registrations(self, **filters) -> List[EventRegistration]:
        """Search event registrations"""
        data = await self._request("GET", "/eventregistrations", params=filters)

        registrations = []
        for item in data.get("Registrations", []):
            registrations.append(EventRegistration(
                registration_id=item.get("Id", ""),
                event_id=item.get("EventId", ""),
                contact_id=item.get("ContactId", ""),
                status=item.get("RegistrationStatus", ""),
                registration_date=item.get("RegistrationDate", ""),
                amount=item.get("Amount"),
                created_at=item.get("Created", ""),
                updated_at=item.get("LastModified", "")
            ))

        return registrations

    async def delete_event_registration(self, registration_id: str) -> Dict[str, Any]:
        """Delete event registration"""
        return await self._request("DELETE", f"/eventregistrations/{registration_id}")

    # ==================== Invoice Operations ====================

    async def search_invoices(self, **filters) -> List[Invoice]:
        """Search invoices"""
        data = await self._request("GET", "/invoices", params=filters)

        invoices = []
        for item in data.get("Invoices", []):
            invoices.append(Invoice(
                invoice_id=item.get("Id", ""),
                contact_id=item.get("ContactId", ""),
                amount=item.get("Amount", 0.0),
                status=item.get("Status", ""),
                due_date=item.get("DueDate"),
                created_at=item.get("Created", ""),
                updated_at=item.get("LastModified", "")
            ))

        return invoices

    # ==================== Payment Operations ====================

    async def search_payments(self, **filters) -> List[Payment]:
        """Search payments"""
        data = await self._request("GET", "/payments", params=filters)

        payments = []
        for item in data.get("Payments", []):
            payments.append(Payment(
                payment_id=item.get("Id", ""),
                invoice_id=item.get("InvoiceId", ""),
                amount=item.get("Amount", 0.0),
                status=item.get("Status", ""),
                payment_date=item.get("PaymentDate", ""),
                created_at=item.get("Created", "")
            ))

        return payments

    # ==================== Refund Operations ====================

    async def search_refunds(self, **filters) -> List[Refund]:
        """Search refunds"""
        data = await self._request("GET", "/refunds", params=filters)

        refunds = []
        for item in data.get("Refunds", []):
            refunds.append(Refund(
                refund_id=item.get("Id", ""),
                payment_id=item.get("PaymentId", ""),
                amount=item.get("Amount", 0.0),
                status=item.get("Status", ""),
                refund_date=item.get("RefundDate", ""),
                created_at=item.get("Created", "")
            ))

        return refunds

    # ==================== Donation Operations ====================

    async def search_donations(self, **filters) -> List[Donation]:
        """Search donations"""
        data = await self._request("GET", "/donations", params=filters)

        donations = []
        for item in data.get("Donations", []):
            donations.append(Donation(
                donation_id=item.get("Id", ""),
                contact_id=item.get("ContactId", ""),
                amount=item.get("Amount", 0.0),
                donation_date=item.get("DonationDate", ""),
                campaign=item.get("Campaign"),
                created_at=item.get("Created", "")
            ))

        return donations

    # ==================== Webhook Handlers ====================

    async def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming webhook events"""
        event_type = payload.get("event_type")

        return {"status": "acknowledged", "event_type": event_type}