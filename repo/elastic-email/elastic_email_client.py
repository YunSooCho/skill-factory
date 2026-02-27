"""
Elastic Email API - Email Marketing and Transactional Email Client

Supports 9 API Actions (Delete List skipped):
- Contact operations (add, get, update, delete, list)
- List operations (add, get, update, get all)

Triggers:
- No triggers supported
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
    status: str = "active"
    lists: List[str] = None
    created_at: str = ""


@dataclass
class ContactList:
    """Mailing list entity"""
    id: str
    name: str
    description: Optional[str] = None
    subscriber_count: int = 0
    created_at: str = ""


class ElasticEmailClient:
    """
    Elastic Email API client for email marketing and transactional emails.

    API Documentation: https://elasticemail.com/developers/api-documentation/
    Uses API Key for authentication.
    """

    BASE_URL = "https://api.elasticemail.com/v4"

    def __init__(self, api_key: str):
        """
        Initialize Elastic Email client.

        Args:
            api_key: API token for authentication
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-ElasticEmail-ApiKey": self.api_key
        }

        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle API response"""
        if response.status in (200, 201, 202, 204):
            if response.status == 204:
                return {}
            data = await response.json()
            return data
        else:
            try:
                data = await response.json()
                error_msg = data.get('message', 'Unknown error')
            except:
                error_msg = f"HTTP {response.status}"
            raise Exception(f"API Error [{response.status}]: {error_msg}")

    # ==================== Contact Operations ====================

    async def add_contact(
        self,
        email: str,
        list_ids: Optional[List[str]] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        status: str = "active",
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """Add a new contact"""
        payload = {
            "email": email,
            "status": status
        }

        if list_ids:
            payload["lists"] = list_ids
        if first_name:
            payload["firstName"] = first_name
        if last_name:
            payload["lastName"] = last_name
        if custom_fields:
            payload["customFields"] = custom_fields

        async with self.session.post(
            f"{self.BASE_URL}/contacts",
            json=payload
        ) as response:
            data = await self._handle_response(response)

            return Contact(
                id=str(data.get("id", "")),
                email=data.get("email", email),
                first_name=data.get("firstName"),
                last_name=data.get("lastName"),
                status=data.get("status", status),
                lists=[str(l) for l in data.get("lists", [])],
                created_at=data.get("createdAt", "")
            )

    async def get_contact(self, contact_id: str) -> Optional[Contact]:
        """Get contact details by ID"""
        async with self.session.get(
            f"{self.BASE_URL}/contacts/{contact_id}"
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)

            return Contact(
                id=str(data.get("id", contact_id)),
                email=data.get("email", ""),
                first_name=data.get("firstName"),
                last_name=data.get("lastName"),
                status=data.get("status", "active"),
                lists=[str(l) for l in data.get("lists", [])],
                created_at=data.get("createdAt", "")
            )

    async def get_contact_by_email(self, email: str) -> Optional[Contact]:
        """Get contact by email address"""
        async with self.session.get(
            f"{self.BASE_URL}/contacts",
            params={"email": email}
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)
            contacts = data.get("contacts", [])

            if not contacts:
                return None

            contact_data = contacts[0]
            return Contact(
                id=str(contact_data.get("id", "")),
                email=contact_data.get("email", email),
                first_name=contact_data.get("firstName"),
                last_name=contact_data.get("lastName"),
                status=contact_data.get("status", "active"),
                lists=[str(l) for l in contact_data.get("lists", [])],
                created_at=contact_data.get("createdAt", "")
            )

    async def update_contact(
        self,
        contact_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        status: Optional[str] = None,
        list_ids: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """Update contact details"""
        payload: Dict[str, Any] = {}

        if email is not None:
            payload["email"] = email
        if first_name is not None:
            payload["firstName"] = first_name
        if last_name is not None:
            payload["lastName"] = last_name
        if status is not None:
            payload["status"] = status
        if list_ids is not None:
            payload["lists"] = list_ids
        if custom_fields is not None:
            payload["customFields"] = custom_fields

        async with self.session.put(
            f"{self.BASE_URL}/contacts/{contact_id}",
            json=payload
        ) as response:
            data = await self._handle_response(response)

            return Contact(
                id=str(data.get("id", contact_id)),
                email=data.get("email", email or ""),
                first_name=data.get("firstName"),
                last_name=data.get("lastName"),
                status=data.get("status", status or "active"),
                lists=[str(l) for l in data.get("lists", [])],
                created_at=data.get("createdAt", "")
            )

    async def delete_contact(self, contact_id: str) -> bool:
        """Delete a contact"""
        async with self.session.delete(
            f"{self.BASE_URL}/contacts/{contact_id}"
        ) as response:
            await self._handle_response(response)
            return True

    async def list_contacts(
        self,
        list_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Contact]:
        """List contacts"""
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset
        }

        if list_id:
            params["listId"] = list_id

        async with self.session.get(
            f"{self.BASE_URL}/contacts",
            params=params
        ) as response:
            data = await self._handle_response(response)
            contacts_data = data.get("contacts", [])

            return [
                Contact(
                    id=str(c.get("id", "")),
                    email=c.get("email", ""),
                    first_name=c.get("firstName"),
                    last_name=c.get("lastName"),
                    status=c.get("status", "active"),
                    lists=[str(l) for l in c.get("lists", [])],
                    created_at=c.get("createdAt", "")
                )
                for c in contacts_data
            ]

    # ==================== List Operations ====================

    async def add_list(
        self,
        name: str,
        description: Optional[str] = None
    ) -> ContactList:
        """Create a new mailing list"""
        payload = {"name": name}
        if description:
            payload["description"] = description

        async with self.session.post(
            f"{self.BASE_URL}/lists",
            json=payload
        ) as response:
            data = await self._handle_response(response)

            return ContactList(
                id=str(data.get("id", "")),
                name=data.get("name", name),
                description=data.get("description"),
                subscriber_count=data.get("subscriberCount", 0),
                created_at=data.get("createdAt", "")
            )

    async def get_list(self, list_id: str) -> Optional[ContactList]:
        """Get list details by ID"""
        async with self.session.get(
            f"{self.BASE_URL}/lists/{list_id}"
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)

            return ContactList(
                id=str(data.get("id", list_id)),
                name=data.get("name", ""),
                description=data.get("description"),
                subscriber_count=data.get("subscriberCount", 0),
                created_at=data.get("createdAt", "")
            )

    async def get_lists(self) -> List[ContactList]:
        """Get all mailing lists"""
        async with self.session.get(
            f"{self.BASE_URL}/lists"
        ) as response:
            data = await self._handle_response(response)
            lists_data = data.get("lists", [])

            return [
                ContactList(
                    id=str(l.get("id", "")),
                    name=l.get("name", ""),
                    description=l.get("description"),
                    subscriber_count=l.get("subscriberCount", 0),
                    created_at=l.get("createdAt", "")
                )
                for l in lists_data
            ]

    async def update_list(
        self,
        list_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> ContactList:
        """Update list details"""
        payload: Dict[str, Any] = {}

        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description

        async with self.session.put(
            f"{self.BASE_URL}/lists/{list_id}",
            json=payload
        ) as response:
            data = await self._handle_response(response)

            return ContactList(
                id=str(data.get("id", list_id)),
                name=data.get("name", name or ""),
                description=data.get("description"),
                subscriber_count=data.get("subscriberCount", 0),
                created_at=data.get("createdAt", "")
            )


# ==================== Example Usage ====================

async def main():
    """Example usage of Elastic Email client"""

    # Example configuration - replace with your actual credentials
    api_key = "your_api_key"

    async with ElasticEmailClient(api_key=api_key) as client:
        # Create a list
        mailing_list = await client.add_list(
            name="Newsletter Subscribers",
            description="Weekly newsletter recipients"
        )
        print(f"List created: {mailing_list.name} (ID: {mailing_list.id})")

        # Add contact
        contact = await client.add_contact(
            email="john@example.com",
            list_ids=[mailing_list.id],
            first_name="John",
            last_name="Doe"
        )
        print(f"Contact created: {contact.email}")

        # Get contact
        contact = await client.get_contact(contact.id)
        print(f"Contact: {contact.first_name} {contact.last_name}")

        # List contacts
        contacts = await client.list_contacts(list_id=mailing_list.id)
        print(f"Contacts in list: {len(contacts)}")

        # Update contact
        contact = await client.update_contact(
            contact_id=contact.id,
            first_name="Janet"
        )
        print(f"Updated contact: {contact.first_name}")


if __name__ == "__main__":
    asyncio.run(main())