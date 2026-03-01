"""
EmailOctopus API - Email Marketing Client

Supports 9 API Actions:
- Contact operations (create, get, update, delete, search)
- Tag operations (create)
- Automation operations (start for contact)
- Campaign operations (get summary report, get link report)

Triggers:
- 8 webhook triggers for contact and campaign events
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Contact:
    """Contact entity"""
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: str = "subscribed"
    tags: List[str] = None
    created_at: str = ""
    fields: Dict[str, Any] = None


@dataclass
class Tag:
    """Tag entity"""
    id: str
    name: str
    created_at: str = ""


@dataclass
class CampaignSummary:
    """Campaign summary report entity"""
    campaign_id: str
    name: str
    status: str
    recipients: int = 0
    opens: int = 0
    clicks: int = 0
    bounces: int = 0
    unsubscribes: int = 0
    complaints: int = 0


@dataclass
class LinkReport:
    """Campaign link report entity"""
    link_id: str
    url: str
    clicks: int = 0
    unique_clicks: int = 0


class EmailOctopusClient:
    """
    EmailOctopus API client for email marketing.

    API Documentation: https://emailoctopus.com/api-documentation/
    Uses API Key for authentication.
    """

    BASE_URL = "https://emailoctopus.com/api/1.6"

    def __init__(self, api_key: str):
        """
        Initialize EmailOctopus client.

        Args:
            api_key: API token for authentication
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        auth = aiohttp.BasicAuth(self.api_key, "")

        self.session = aiohttp.ClientSession(headers=headers, auth=auth)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle API response"""
        if response.status in (200, 201, 202):
            data = await response.json()
            return data
        else:
            try:
                data = await response.json()
                error_msg = data.get('error', data.get('message', 'Unknown error'))
            except:
                error_msg = f"HTTP {response.status}"
            raise Exception(f"API Error [{response.status}]: {error_msg}")

    # ==================== Contact Operations ====================

    async def create_contact(
        self,
        list_id: str,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        fields: Optional[Dict[str, Any]] = None,
        subscribe: bool = True
    ) -> Contact:
        """Create a new contact in a list"""
        payload = {
            "email_address": email
        }

        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if tags:
            payload["tags"] = tags
        if fields:
            payload["fields"] = fields
        payload["subscribe"] = subscribe

        async with self.session.post(
            f"{self.BASE_URL}/lists/{list_id}/contacts",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            contact_data = data.get("data", {})
            embedded = contact_data.get("data", {})

            return Contact(
                id=str(embedded.get("id", "")),
                email=embedded.get("email_address", email),
                first_name=embedded.get("fields", {}).get("FirstName", ""),
                last_name=embedded.get("fields", {}).get("LastName", ""),
                status=embedded.get("status", "subscribed"),
                tags=embedded.get("tags", []),
                created_at=embedded.get("created_at", ""),
                fields=embedded.get("fields", {})
            )

    async def get_contact(
        self,
        list_id: str,
        contact_id: str
    ) -> Optional[Contact]:
        """Get contact details"""
        async with self.session.get(
            f"{self.BASE_URL}/lists/{list_id}/contacts/{contact_id}"
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)
            embedded = data.get("data", {}).get("data", {})

            return Contact(
                id=str(embedded.get("id", contact_id)),
                email=embedded.get("email_address", ""),
                first_name=embedded.get("fields", {}).get("FirstName", ""),
                last_name=embedded.get("fields", {}).get("LastName", ""),
                status=embedded.get("status", "subscribed"),
                tags=embedded.get("tags", []),
                created_at=embedded.get("created_at", ""),
                fields=embedded.get("fields", {})
            )

    async def search_contact(
        self,
        list_id: str,
        email: str
    ) -> Optional[Contact]:
        """Search for contact by email address in a list"""
        async with self.session.get(
            f"{self.BASE_URL}/lists/{list_id}/contacts",
            params={"email_address": email}
        ) as response:
            data = await self._handle_response(response)
            contacts_data = data.get("data", {}).get("data", [])

            if not contacts_data:
                return None

            contact_data = contacts_data[0]
            return Contact(
                id=str(contact_data.get("id", "")),
                email=contact_data.get("email_address", email),
                first_name=contact_data.get("fields", {}).get("FirstName", ""),
                last_name=contact_data.get("fields", {}).get("LastName", ""),
                status=contact_data.get("status", "subscribed"),
                tags=contact_data.get("tags", []),
                created_at=contact_data.get("created_at", ""),
                fields=contact_data.get("fields", {})
            )

    async def update_contact(
        self,
        list_id: str,
        contact_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        fields: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """Update contact details"""
        payload = {}

        if email:
            payload["email_address"] = email
        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if tags:
            payload["tags"] = tags
        if fields:
            payload["fields"] = fields

        async with self.session.put(
            f"{self.BASE_URL}/lists/{list_id}/contacts/{contact_id}",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            contact_data = data.get("data", {})
            embedded = contact_data.get("data", {})

            return Contact(
                id=str(embedded.get("id", contact_id)),
                email=embedded.get("email_address", email or ""),
                first_name=embedded.get("fields", {}).get("FirstName", first_name or ""),
                last_name=embedded.get("fields", {}).get("LastName", last_name or ""),
                status=embedded.get("status", "subscribed"),
                tags=embedded.get("tags", []),
                created_at=embedded.get("created_at", ""),
                fields=embedded.get("fields", {})
            )

    async def delete_contact(
        self,
        list_id: str,
        contact_id: str
    ) -> bool:
        """Delete a contact"""
        async with self.session.delete(
            f"{self.BASE_URL}/lists/{list_id}/contacts/{contact_id}"
        ) as response:
            if response.status == 404:
                return False
            await self._handle_response(response)
            return True

    # ==================== Tag Operations ====================

    async def create_tag(self, list_id: str, name: str) -> Tag:
        """Create a new tag in a list"""
        payload = {"tag": name}

        async with self.session.post(
            f"{self.BASE_URL}/lists/{list_id}/tags",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            tag_data = data.get("data", {})

            return Tag(
                id=str(tag_data.get("id", "")),
                name=tag_data.get("tag", name),
                created_at=tag_data.get("created_at", "")
            )

    async def get_tags(self, list_id: str) -> List[Tag]:
        """Get all tags in a list"""
        async with self.session.get(
            f"{self.BASE_URL}/lists/{list_id}/tags"
        ) as response:
            data = await self._handle_response(response)
            tags_data = data.get("data", {}).get("data", [])

            return [
                Tag(
                    id=str(t.get("id", "")),
                    name=t.get("tag", ""),
                    created_at=t.get("created_at", "")
                )
                for t in tags_data
            ]

    async def delete_tag(self, list_id: str, tag_id: str) -> bool:
        """Delete a tag"""
        async with self.session.delete(
            f"{self.BASE_URL}/lists/{list_id}/tags/{tag_id}"
        ) as response:
            if response.status == 404:
                return False
            await self._handle_response(response)
            return True

    # ==================== Automation Operations ====================

    async def start_automation_for_contact(
        self,
        automation_id: str,
        contact_id: str,
        list_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Start an automation for a specific contact"""
        payload = {
            "contact_id": contact_id
        }

        if list_id:
            payload["list_id"] = list_id

        async with self.session.post(
            f"{self.BASE_URL}/automations/{automation_id}/actions/trigger",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            return data

    # ==================== Campaign Operations ====================

    async def get_campaign_summary_report(
        self,
        campaign_id: str
    ) -> Optional[CampaignSummary]:
        """Get campaign summary report"""
        async with self.session.get(
            f"{self.BASE_URL}/reports/{campaign_id}/summary"
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)
            report_data = data.get("data", {})

            return CampaignSummary(
                campaign_id=campaign_id,
                name=report_data.get("name", ""),
                status=report_data.get("status", ""),
                recipients=report_data.get("recipients", 0),
                opens=report_data.get("opens", 0),
                clicks=report_data.get("clicks", 0),
                bounces=report_data.get("bounces", 0),
                unsubscribes=report_data.get("unsubscribes", 0),
                complaints=report_data.get("complaints", 0)
            )

    async def get_campaign_link_report(
        self,
        campaign_id: str
    ) -> List[LinkReport]:
        """Get campaign link click report"""
        async with self.session.get(
            f"{self.BASE_URL}/reports/{campaign_id}/links"
        ) as response:
            if response.status == 404:
                return []
            data = await self._handle_response(response)
            links_data = data.get("data", {}).get("data", [])

            return [
                LinkReport(
                    link_id=str(l.get("id", "")),
                    url=l.get("url", ""),
                    clicks=l.get("clicks", 0),
                    unique_clicks=l.get("unique_clicks", 0)
                )
                for l in links_data
            ]


# ==================== Example Usage ====================

async def main():
    """Example usage of EmailOctopus client"""

    # Example configuration - replace with your actual credentials
    api_key = "your_api_key"
    list_id = "your_list_id"

    async with EmailOctopusClient(api_key=api_key) as client:
        # Create contact
        contact = await client.create_contact(
            list_id=list_id,
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            tags=["new-signup"]
        )
        print(f"Contact created: {contact.email}")

        # Get contact
        contact = await client.get_contact(list_id, contact.id)
        print(f"Contact: {contact.first_name} {contact.last_name}")

        # Search contact
        contact = await client.search_contact(list_id, "john@example.com")
        if contact:
            print(f"Found: {contact.email}")

        # Create tag
        tag = await client.create_tag(list_id, "vip-customer")
        print(f"Tag created: {tag.name}")

        # Get campaign summary
        summary = await client.get_campaign_summary_report("campaign_123")
        if summary:
            print(f"Campaign: {summary.name} - {summary.opens} opens")

        # Get link report
        links = await client.get_campaign_link_report("campaign_123")
        print(f"Links: {len(links)}")


if __name__ == "__main__":
    asyncio.run(main())