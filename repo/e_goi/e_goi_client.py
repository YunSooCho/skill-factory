"""
E-goi API - Multi-channel Marketing Automation Client

Supports 14 API Actions:
- Contact operations (create, update, get, search, delete)
- List operations (create, delete, list)
- Tag operations (create, list)
- Campaign operations (send to contact, send to segment, list)
- Segment operations (list)

Triggers:
- 7 webhook triggers for email events
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
    phone: Optional[str] = None
    tags: List[str] = None
    status: str = "active"
    created_at: str = ""


@dataclass
class List:
    """Mailing list entity"""
    id: str
    name: str
    subscriber_count: int = 0
    created_at: str = ""


@dataclass
class Tag:
    """Tag entity"""
    id: str
    name: str
    created_at: str = ""


@dataclass
class Campaign:
    """Campaign entity"""
    id: str
    name: str
    status: str
    type: str
    created_at: str = ""


@dataclass
class Segment:
    """Segment entity"""
    id: str
    name: str
    list_id: str
    conditions: List[Dict[str, Any]] = None


class EGoiClient:
    """
    E-goi API client for multi-channel marketing automation.

    API Documentation: https://apihelp.e-goi.com/
    Uses API Key for authentication.
    """

    BASE_URL = "https://api.e-goi.com/v2"

    def __init__(self, api_key: str):
        """
        Initialize E-goi client.

        Args:
            api_key: API token for authentication
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "APIKey": self.api_key
        }

        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle API response"""
        data = await response.json()

        if response.status not in (200, 201, 202, 204):
            error_msg = data.get('error', {}).get('message', 'Unknown error')
            raise Exception(f"API Error [{response.status}]: {error_msg}")

        return data

    # ==================== Contact Operations ====================

    async def create_contact(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        tags: Optional[List[str]] = None,
        list_id: Optional[str] = None,
        status: str = "active"
    ) -> Contact:
        """Create a new contact"""
        payload = {
            "email": email,
            "status": status
        }

        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if phone:
            payload["phone"] = phone
        if tags:
            payload["tags"] = tags
        if list_id:
            payload["list_id"] = list_id

        async with self.session.post(
            f"{self.BASE_URL}/contacts",
            json=payload
        ) as response:
            data = await self._handle_response(response)

            return Contact(
                id=str(data.get("id", "")),
                email=data.get("email", email),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                phone=data.get("phone"),
                tags=data.get("tags", []),
                status=data.get("status", status),
                created_at=data.get("created_at", "")
            )

    async def get_contact(self, contact_id: str) -> Optional[Contact]:
        """Get contact details"""
        async with self.session.get(
            f"{self.BASE_URL}/contacts/{contact_id}"
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)

            return Contact(
                id=str(data.get("id", contact_id)),
                email=data.get("email", ""),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                phone=data.get("phone"),
                tags=data.get("tags", []),
                status=data.get("status", "active"),
                created_at=data.get("created_at", "")
            )

    async def search_contacts(
        self,
        query: Optional[str] = None,
        list_id: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 100
    ) -> List[Contact]:
        """Search contacts"""
        params: Dict[str, Any] = {"limit": limit}

        if query:
            params["search"] = query
        if list_id:
            params["list_id"] = list_id
        if tag:
            params["tag"] = tag

        async with self.session.get(
            f"{self.BASE_URL}/contacts",
            params=params
        ) as response:
            data = await self._handle_response(response)
            contacts_data = data.get("data", [])

            return [
                Contact(
                    id=str(c.get("id", "")),
                    email=c.get("email", ""),
                    first_name=c.get("first_name"),
                    last_name=c.get("last_name"),
                    phone=c.get("phone"),
                    tags=c.get("tags", []),
                    status=c.get("status", "active"),
                    created_at=c.get("created_at", "")
                )
                for c in contacts_data
            ]

    async def update_contacts(
        self,
        contact_ids: List[str],
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[Contact]:
        """Update multiple contacts"""
        payload: Dict[str, Any] = {"contact_ids": contact_ids}

        if email:
            payload["email"] = email
        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if phone:
            payload["phone"] = phone
        if tags:
            payload["tags"] = tags

        async with self.session.put(
            f"{self.BASE_URL}/contacts",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            contacts_data = data.get("data", [])

            return [
                Contact(
                    id=str(c.get("id", "")),
                    email=c.get("email", email or ""),
                    first_name=c.get("first_name"),
                    last_name=c.get("last_name"),
                    phone=c.get("phone"),
                    tags=c.get("tags", []),
                    status=c.get("status", "active"),
                    created_at=c.get("created_at", "")
                )
                for c in contacts_data
            ]

    async def delete_contacts(self, contact_ids: List[str]) -> bool:
        """Delete multiple contacts"""
        payload = {"contact_ids": contact_ids}

        async with self.session.post(
            f"{self.BASE_URL}/contacts/delete",
            json=payload
        ) as response:
            await self._handle_response(response)
            return True

    # ==================== List Operations ====================

    async def create_list(
        self,
        name: str,
        description: Optional[str] = None
    ) -> List:
        """Create a new mailing list"""
        payload = {"name": name}
        if description:
            payload["description"] = description

        async with self.session.post(
            f"{self.BASE_URL}/lists",
            json=payload
        ) as response:
            data = await self._handle_response(response)

            return List(
                id=str(data.get("id", "")),
                name=data.get("name", name),
                subscriber_count=data.get("subscriber_count", 0),
                created_at=data.get("created_at", "")
            )

    async def get_lists(self) -> List[List]:
        """Get all mailing lists"""
        async with self.session.get(
            f"{self.BASE_URL}/lists"
        ) as response:
            data = await self._handle_response(response)
            lists_data = data.get("data", [])

            return [
                List(
                    id=str(l.get("id", "")),
                    name=l.get("name", ""),
                    subscriber_count=l.get("subscriber_count", 0),
                    created_at=l.get("created_at", "")
                )
                for l in lists_data
            ]

    async def delete_list(self, list_id: str) -> bool:
        """Delete a mailing list"""
        async with self.session.delete(
            f"{self.BASE_URL}/lists/{list_id}"
        ) as response:
            await self._handle_response(response)
            return True

    # ==================== Tag Operations ====================

    async def create_tag(self, name: str) -> Tag:
        """Create a new tag"""
        payload = {"name": name}

        async with self.session.post(
            f"{self.BASE_URL}/tags",
            json=payload
        ) as response:
            data = await self._handle_response(response)

            return Tag(
                id=str(data.get("id", "")),
                name=data.get("name", name),
                created_at=data.get("created_at", "")
            )

    async def list_tags(self) -> List[Tag]:
        """List all tags"""
        async with self.session.get(
            f"{self.BASE_URL}/tags"
        ) as response:
            data = await self._handle_response(response)
            tags_data = data.get("data", [])

            return [
                Tag(
                    id=str(t.get("id", "")),
                    name=t.get("name", ""),
                    created_at=t.get("created_at", "")
                )
                for t in tags_data
            ]

    async def delete_tag(self, tag_id: str) -> bool:
        """Delete a tag"""
        async with self.session.delete(
            f"{self.BASE_URL}/tags/{tag_id}"
        ) as response:
            await self._handle_response(response)
            return True

    # ==================== Campaign Operations ====================

    async def campaign_list(self) -> List[Campaign]:
        """List all campaigns"""
        async with self.session.get(
            f"{self.BASE_URL}/campaigns"
        ) as response:
            data = await self._handle_response(response)
            campaigns_data = data.get("data", [])

            return [
                Campaign(
                    id=str(c.get("id", "")),
                    name=c.get("name", ""),
                    status=c.get("status", ""),
                    type=c.get("type", ""),
                    created_at=c.get("created_at", "")
                )
                for c in campaigns_data
            ]

    async def send_email_to_contact(
        self,
        campaign_id: str,
        contact_id: str
    ) -> Dict[str, Any]:
        """Send email campaign to a specific contact"""
        payload = {
            "campaign_id": campaign_id,
            "contact_id": contact_id
        }

        async with self.session.post(
            f"{self.BASE_URL}/campaigns/send/contact",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            return data

    async def send_email_to_segment(
        self,
        campaign_id: str,
        segment_id: str
    ) -> Dict[str, Any]:
        """Send email campaign to a segment"""
        payload = {
            "campaign_id": campaign_id,
            "segment_id": segment_id
        }

        async with self.session.post(
            f"{self.BASE_URL}/campaigns/send/segment",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            return data

    # ==================== Segment Operations ====================

    async def segment_list(self, list_id: Optional[str] = None) -> List[Segment]:
        """List all segments"""
        params = {}
        if list_id:
            params["list_id"] = list_id

        async with self.session.get(
            f"{self.BASE_URL}/segments",
            params=params
        ) as response:
            data = await self._handle_response(response)
            segments_data = data.get("data", [])

            return [
                Segment(
                    id=str(s.get("id", "")),
                    name=s.get("name", ""),
                    list_id=str(s.get("list_id", "")),
                    conditions=s.get("conditions", [])
                )
                for s in segments_data
            ]


# ==================== Example Usage ====================

async def main():
    """Example usage of E-goi client"""

    # Example configuration - replace with your actual credentials
    api_key = "your_api_key"

    async with EGoiClient(api_key=api_key) as client:
        # Create list
        mailing_list = await client.create_list(
            name="Newsletter Subscribers"
        )
        print(f"List created: {mailing_list.name}")

        # Create contact
        contact = await client.create_contact(
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            list_id=mailing_list.id
        )
        print(f"Contact created: {contact.email}")

        # Get contact
        contact = await client.get_contact(contact.id)
        print(f"Contact: {contact.first_name} {contact.last_name}")

        # Create tag
        tag = await client.create_tag("vip")
        print(f"Tag created: {tag.name}")

        # List campaigns
        campaigns = await client.campaign_list()
        print(f"Campaigns: {len(campaigns)}")

        # List segments
        segments = await client.segment_list()
        print(f"Segments: {len(segments)}")


if __name__ == "__main__":
    asyncio.run(main())