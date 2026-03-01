"""
Reply API - Email Outreach Client

Supports:
- Campaigns management
- Contacts management
- Prospect tracking
"""

import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import os


@dataclass
class Contact:
    """Contact information"""
    contact_id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    company: Optional[str]
    status: str
    created_at: str
    updated_at: str


@dataclass
class Campaign:
    """Campaign information"""
    campaign_id: str
    name: str
    status: str
    total_prospects: int
    active_prospects: int
    completed_prospects: int
    created_at: str
    updated_at: str


class ReplyClient:
    """
    Reply.io API client for email outreach automation.

    API Documentation: https://lp.yoom.fun/apps/reply_io
    Requires API key from Yoom integration.
    """

    BASE_URL = "https://api.reply.io/v1"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize Reply.io client.

        Args:
            api_key: API key (defaults to YOOM_REPLY_IO_API_KEY env var)
            base_url: Custom base URL for testing
        """
        self.api_key = api_key or os.environ.get("YOOM_REPLY_IO_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set YOOM_REPLY_IO_API_KEY environment variable")

        self.base_url = base_url or self.BASE_URL
        self.session = None
        self._rate_limit_delay = 0.4  # 400ms between requests

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

    # ==================== Contact Operations ====================

    async def create_or_update_contact(self, contact_data: Dict[str, Any]) -> Contact:
        """Create or update a contact"""
        data = await self._request("POST", "/contacts", json=contact_data)

        return Contact(
            contact_id=data.get("id", ""),
            email=data.get("email", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            company=data.get("company"),
            status=data.get("status", "active"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def get_contact(self, contact_id: str) -> Contact:
        """Get contact by ID"""
        data = await self._request("GET", f"/contacts/{contact_id}")

        return Contact(
            contact_id=data.get("id", contact_id),
            email=data.get("email", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            company=data.get("company"),
            status=data.get("status", "active"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def list_contacts(self, **filters) -> List[Contact]:
        """List contacts with optional filters"""
        data = await self._request("GET", "/contacts", params=filters)

        contacts = []
        for item in data.get("data", []):
            contacts.append(Contact(
                contact_id=item.get("id", ""),
                email=item.get("email", ""),
                first_name=item.get("first_name"),
                last_name=item.get("last_name"),
                company=item.get("company"),
                status=item.get("status", "active"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return contacts

    async def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """Delete contact"""
        return await self._request("DELETE", f"/contacts/{contact_id}")

    # ==================== Campaign Operations ====================

    async def list_campaigns(self, **filters) -> List[Campaign]:
        """List campaigns with optional filters"""
        data = await self._request("GET", "/campaigns", params=filters)

        campaigns = []
        for item in data.get("data", []):
            campaigns.append(Campaign(
                campaign_id=item.get("id", ""),
                name=item.get("name", ""),
                status=item.get("status", "active"),
                total_prospects=item.get("total_prospects", 0),
                active_prospects=item.get("active_prospects", 0),
                completed_prospects=item.get("completed_prospects", 0),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return campaigns

    async def get_campaign(self, campaign_id: str) -> Campaign:
        """Get campaign by ID"""
        data = await self._request("GET", f"/campaigns/{campaign_id}")

        return Campaign(
            campaign_id=data.get("id", campaign_id),
            name=data.get("name", ""),
            status=data.get("status", "active"),
            total_prospects=data.get("total_prospects", 0),
            active_prospects=data.get("active_prospects", 0),
            completed_prospects=data.get("completed_prospects", 0),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def add_contact_to_campaign(
        self,
        contact_id: str,
        campaign_id: str
    ) -> Dict[str, Any]:
        """Add contact to a campaign"""
        data = {
            "contact_id": contact_id,
            "campaign_id": campaign_id
        }
        return await self._request("POST", f"/campaigns/{campaign_id}/contacts", json=data)

    async def delete_contact_from_campaign(
        self,
        contact_id: str,
        campaign_id: str
    ) -> Dict[str, Any]:
        """Delete contact from a campaign"""
        return await self._request("DELETE", f"/campaigns/{campaign_id}/contacts/{contact_id}")

    # ==================== Prospect Operations ====================

    async def mark_contact_as_replied(
        self,
        contact_id: str,
        campaign_id: str
    ) -> Dict[str, Any]:
        """Mark contact as replied"""
        return await self._request(
            "POST",
            f"/campaigns/{campaign_id}/prospects/{contact_id}/replied"
        )

    async def mark_contact_as_finished(
        self,
        contact_id: str,
        campaign_id: str,
        status: Optional[str] = "finished"
    ) -> Dict[str, Any]:
        """Mark contact as finished"""
        data = {"status": status}
        return await self._request(
            "POST",
            f"/campaigns/{campaign_id}/prospects/{contact_id}/finish",
            json=data
        )

    # ==================== Webhook Handlers ====================

    async def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming webhook events"""
        event_type = payload.get("event_type")

        if event_type == "prospect_finished":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "inbox_category_set":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "new_email_opened":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "new_emails_sent":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "new_email_replied":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "new_person_opt_out":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "new_link_clicked":
            return {"status": "acknowledged", "event_type": event_type}
        else:
            return {"status": "acknowledged", "event_type": event_type}