"""
Google Contact API - Contact Management Client

Supports:
- List Contacts
- Search Contacts
- Get Contact Information
- Get Multiple Contacts
- Create Contact
- Delete Contact
- List Contact Groups
- Get Contact Group Information
- Create Contact Group
- Update Contact Group
- Delete Contact Group
- Add Contact to Group
- Remove Contact from Group
- Handle Webhook (for triggers)
"""

import aiohttp
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Contact:
    """Google Contact object"""
    resource_name: str
    etag: str
    names: List[Dict[str, str]]
    email_addresses: List[Dict[str, str]]
    phone_numbers: List[Dict[str, str]]
    organizations: List[Dict[str, str]]
    birthdays: List[Dict[str, Any]]
    addresses: List[Dict[str, str]]
    urls: List[Dict[str, str]]
    notes: List[Dict[str, str]]
    memberships: List[Dict[str, str]]

    @property
    def display_name(self) -> str:
        """Get the primary display name."""
        if self.names:
            return self.names[0].get("displayName", "")
        return ""

    @property
    def primary_email(self) -> str:
        """Get the primary email address."""
        for email in self.email_addresses:
            if email.get("metadata", {}).get("primary"):
                return email.get("value", "")
        if self.email_addresses:
            return self.email_addresses[0].get("value", "")
        return ""


@dataclass
class ContactGroup:
    """Google Contact Group object"""
    resource_name: str
    etag: str
    group_type: str
    name: str
    member_resource_names: List[str]
    member_count: int
    formatted_name: str


@dataclass
class WebhookEvent:
    """Webhook event object"""
    event_type: str
    timestamp: str
    data: Dict[str, Any]
    contact_resource_name: Optional[str] = None
    group_resource_name: Optional[str] = None


class GoogleContactClient:
    """
    Google Contacts API client for contact management.

    Provides operations for creating, updating, searching, and managing
    contacts and contact groups.

    API Documentation: https://lp.yoom.fun/apps/google-contact
    Requires:
    - Google Cloud project with People API enabled
    - OAuth credentials or service account
    """

    BASE_URL = "https://people.googleapis.com/v1"

    def __init__(
        self,
        access_token: str,
        webhook_secret: Optional[str] = None
    ):
        """
        Initialize Google Contact client.

        Args:
            access_token: OAuth access token
            webhook_secret: Optional secret for webhook signature verification
        """
        self.access_token = access_token
        self.webhook_secret = webhook_secret
        self.session = None
        self._rate_limit_delay = 0.1

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an API request with error handling.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails or returns error
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            async with self.session.request(
                method,
                url,
                params=params,
                json=json_data
            ) as response:
                response_data = await response.json()

                if response.status >= 400:
                    error = response_data.get("error", {})
                    error_message = error.get("message", f"HTTP {response.status} error")
                    raise Exception(f"Google Contact API error: {error_message}")

                return response_data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")

    # ==================== Contact Operations ====================

    async def create_contact(
        self,
        given_name: str,
        family_name: str,
        email_addresses: Optional[List[Dict[str, str]]] = None,
        phone_numbers: Optional[List[Dict[str, str]]] = None,
        organizations: Optional[List[Dict[str, str]]] = None,
        addresses: Optional[List[Dict[str, str]]] = None,
        notes: Optional[str] = None
    ) -> Contact:
        """
        Create a new contact.

        Args:
            given_name: First name
            family_name: Last name
            email_addresses: Optional list of email dicts with 'value' and optional 'type'
            phone_numbers: Optional list of phone dicts with 'value' and optional 'type'
            organizations: Optional list of org dicts with 'name', 'title'
            addresses: Optional list of address dicts
            notes: Optional notes

        Returns:
            Created Contact object

        Raises:
            Exception: If creation fails
        """
        payload = {"names": [{"givenName": given_name, "familyName": family_name}]}

        if email_addresses:
            payload["emailAddresses"] = [
                {"value": e["value"], "type": e.get("type", "other")} for e in email_addresses
            ]

        if phone_numbers:
            payload["phoneNumbers"] = [
                {"value": p["value"], "type": p.get("type", "other")} for p in phone_numbers
            ]

        if organizations:
            payload["organizations"] = [
                {"name": o.get("name", ""), "title": o.get("title", "")} for o in organizations
            ]

        if addresses:
            payload["addresses"] = addresses

        if notes:
            payload["biographies"] = [{"value": notes, "contentType": "TEXT_PLAIN"}]

        response_data = await self._make_request(
            "POST",
            "/people:createContact",
            params={"personFields": "names,emailAddresses,phoneNumbers,organizations,addresses,biographies"},
            json_data=payload
        )

        return self._parse_contact(response_data)

    async def list_contacts(
        self,
        page_size: int = 100,
        page_token: Optional[str] = None,
        request_sync_token: Optional[bool] = None
    ) -> List[Contact]:
        """
        List contacts in the user's directory.

        Args:
            page_size: Number of results per page
            page_token: Page token for pagination
            request_sync_token: Whether to request sync token

        Returns:
            List of Contact objects

        Raises:
            Exception: If request fails
        """
        params = {
            "personFields": "names,emailAddresses,phoneNumbers,organizations,addresses,biographies,memberships",
            "pageSize": page_size
        }

        if page_token:
            params["pageToken"] = page_token
        if request_sync_token:
            params["requestSyncToken"] = "true"

        response_data = await self._make_request(
            "GET",
            "/people/me/connections",
            params=params
        )

        connections = response_data.get("connections", [])

        return [self._parse_contact(c) for c in connections if c]

    async def search_contacts(
        self,
        query: str,
        page_size: int = 20
    ) -> List[Contact]:
        """
        Search for contacts.

        Args:
            query: Search query
            page_size: Number of results

        Returns:
            List of Contact objects

        Raises:
            Exception: If request fails
        """
        params = {
            "query": query,
            "readMask": "names,emailAddresses,phoneNumbers,organizations,addresses,biographies",
            "pageSize": page_size
        }

        response_data = await self._make_request(
            "GET",
            "/people:searchContacts",
            params=params
        )

        results = response_data.get("results", [])
        contacts = []

        for result in results:
            person = result.get("person")
            if person:
                contacts.append(self._parse_contact(person))

        return contacts

    async def get_contact(
        self,
        resource_name: str,
        person_fields: str = None
    ) -> Optional[Contact]:
        """
        Get details of a specific contact.

        Args:
            resource_name: Contact resource name
            person_fields: Comma-separated list of fields to return

        Returns:
            Contact object or None if not found

        Raises:
            Exception: If request fails
        """
        if person_fields is None:
            person_fields = "names,emailAddresses,phoneNumbers,organizations,addresses,biographies,memberships"

        try:
            response_data = await self._make_request(
                "GET",
                f"/{resource_name}",
                params={"personFields": person_fields}
            )

            return self._parse_contact(response_data)

        except Exception:
            return None

    async def get_multiple_contacts(
        self,
        resource_names: List[str]
    ) -> List[Contact]:
        """
        Get multiple contacts at once.

        Args:
            resource_names: List of contact resource names

        Returns:
            List of Contact objects

        Raises:
            Exception: If request fails
        """
        payload = {
            "resourceNames": resource_names,
            "personFields": "names,emailAddresses,phoneNumbers,organizations,addresses,biographies,memberships"
        }

        response_data = await self._make_request(
            "POST",
            "/people:batchGet",
            params={"personFields": "names,emailAddresses,phoneNumbers,organizations,addresses,biographies,memberships"},
            json_data={"resourceNames": resource_names}
        )

        responses = response_data.get("responses", [])
        contacts = []

        for resp in responses:
            person = resp.get("person")
            if person:
                contacts.append(self._parse_contact(person))

        return contacts

    async def delete_contact(self, resource_name: str) -> None:
        """
        Delete a contact.

        Args:
            resource_name: Contact resource name

        Raises:
            Exception: If deletion fails
        """
        await self._make_request(
            "DELETE",
            f"/{resource_name}:deleteContact"
        )

    # ==================== Contact Group Operations ====================

    async def create_contact_group(
        self,
        name: str,
        group_type: str = "USER_CONTACT_GROUP"
    ) -> ContactGroup:
        """
        Create a new contact group.

        Args:
            name: Group name
            group_type: Group type (USER_CONTACT_GROUP, SYSTEM_CONTACT_GROUP)

        Returns:
            Created ContactGroup object

        Raises:
            Exception: If creation fails
            ValueError: If parameters are invalid
        """
        if not name:
            raise ValueError("name is required")

        payload = {
            "contactGroup": {
                "name": name,
                "groupType": group_type
            }
        }

        response_data = await self._make_request(
            "POST",
            "/contactGroups",
            json_data=payload
        )

        group = response_data.get("contactGroup", {})

        return ContactGroup(
            resource_name=group.get("resourceName", ""),
            etag=group.get("etag", ""),
            group_type=group.get("groupType", group_type),
            name=group.get("name", name),
            member_resource_names=group.get("memberResourceNames", []),
            member_count=group.get("memberCount", 0),
            formatted_name=group.get("formattedName", name)
        )

    async def list_contact_groups(
        self,
        page_size: int = 100,
        page_token: Optional[str] = None
    ) -> List[ContactGroup]:
        """
        List contact groups.

        Args:
            page_size: Number of results per page
            page_token: Page token for pagination

        Returns:
            List of ContactGroup objects

        Raises:
            Exception: If request fails
        """
        params = {"pageSize": page_size}

        if page_token:
            params["pageToken"] = page_token

        response_data = await self._make_request(
            "GET",
            "/contactGroups",
            params=params
        )

        groups_list = response_data.get("contactGroups", [])

        return [
            self._parse_contact_group(group)
            for group in groups_list
            if group
        ]

    async def get_contact_group(
        self,
        resource_name: str
    ) -> Optional[ContactGroup]:
        """
        Get details of a specific contact group.

        Args:
            resource_name: Group resource name

        Returns:
            ContactGroup object or None if not found

        Raises:
            Exception: If request fails
        """
        try:
            response_data = await self._make_request(
                "GET",
                f"/contactGroups/{resource_name}",
                params={"maxMembers": 1000}
            )

            return self._parse_contact_group(response_data)

        except Exception:
            return None

    async def update_contact_group(
        self,
        resource_name: str,
        name: Optional[str] = None
    ) -> ContactGroup:
        """
        Update a contact group.

        Args:
            resource_name: Group resource name
            name: New group name

        Returns:
            Updated ContactGroup object

        Raises:
            Exception: If update fails
            ValueError: If resource_name is empty
        """
        if not resource_name:
            raise ValueError("resource_name is required")

        current_group = await self.get_contact_group(resource_name)
        if not current_group:
            raise Exception(f"Group not found: {resource_name}")

        payload = {
            "contactGroup": {
                "resourceName": resource_name,
                ".etag": current_group.etag
            }
        }

        if name:
            payload["contactGroup"]["name"] = name

        response_data = await self._make_request(
            "PUT",
            f"/contactGroups/{resource_name}",
            json_data=payload
        )

        group = response_data.get("contactGroup", {})

        return ContactGroup(
            resource_name=group.get("resourceName", resource_name),
            etag=group.get("etag", ""),
            group_type=group.get("groupType", current_group.group_type),
            name=group.get("name", name or current_group.name),
            member_resource_names=group.get("memberResourceNames", []),
            member_count=group.get("memberCount", current_group.member_count),
            formatted_name=group.get("formattedName", "")
        )

    async def delete_contact_group(self, resource_name: str) -> None:
        """
        Delete a contact group.

        Args:
            resource_name: Group resource name

        Raises:
            Exception: If deletion fails
        """
        await self._make_request(
            "DELETE",
            f"/contactGroups/{resource_name}"
        )

    # ==================== Group Membership Operations ====================

    async def add_contact_to_group(
        self,
        resource_name: str,
        contact_resource_names: List[str]
    ) -> ContactGroup:
        """
        Add contacts to a group.

        Args:
            resource_name: Group resource name
            contact_resource_names: List of contact resource names to add

        Returns:
            Updated ContactGroup object

        Raises:
            Exception: If operation fails
            ValueError: If parameters are invalid
        """
        if not resource_name:
            raise ValueError("resource_name is required")
        if not contact_resource_names:
            raise ValueError("contact_resource_names is required")

        payload = {
            "resourceNamesToAdd": contact_resource_names
        }

        response_data = await self._make_request(
            "POST",
            f"/contactGroups/{resource_name}/members:modify",
            json_data=payload
        )

        group = response_data.get("contactGroup", {})

        return ContactGroup(
            resource_name=group.get("resourceName", resource_name),
            etag=group.get("etag", ""),
            group_type=group.get("groupType", ""),
            name=group.get("name", ""),
            member_resource_names=group.get("memberResourceNames", []),
            member_count=group.get("memberCount", 0),
            formatted_name=group.get("formattedName", "")
        )

    async def remove_contact_from_group(
        self,
        resource_name: str,
        contact_resource_names: List[str]
    ) -> ContactGroup:
        """
        Remove contacts from a group.

        Args:
            resource_name: Group resource name
            contact_resource_names: List of contact resource names to remove

        Returns:
            Updated ContactGroup object

        Raises:
            Exception: If operation fails
            ValueError: If parameters are invalid
        """
        if not resource_name:
            raise ValueError("resource_name is required")
        if not contact_resource_names:
            raise ValueError("contact_resource_names is required")

        payload = {
            "resourceNamesToRemove": contact_resource_names
        }

        response_data = await self._make_request(
            "POST",
            f"/contactGroups/{resource_name}/members:modify",
            json_data=payload
        )

        group = response_data.get("contactGroup", {})

        return ContactGroup(
            resource_name=group.get("resourceName", resource_name),
            etag=group.get("etag", ""),
            group_type=group.get("groupType", ""),
            name=group.get("name", ""),
            member_resource_names=group.get("memberResourceNames", []),
            member_count=group.get("memberCount", 0),
            formatted_name=group.get("formattedName", "")
        )

    # ==================== Helper Methods ====================

    def _parse_contact(self, data: Dict[str, Any]) -> Contact:
        """Parse contact data from API response."""
        return Contact(
            resource_name=data.get("resourceName", ""),
            etag=data.get("etag", ""),
            names=data.get("names", []),
            email_addresses=data.get("emailAddresses", []),
            phone_numbers=data.get("phoneNumbers", []),
            organizations=data.get("organizations", []),
            birthdays=data.get("birthdays", []),
            addresses=data.get("addresses", []),
            urls=data.get("urls", []),
            notes=data.get("biographies", []),
            memberships=data.get("memberships", [])
        )

    def _parse_contact_group(self, data: Dict[str, Any]) -> ContactGroup:
        """Parse contact group data from API response."""
        return ContactGroup(
            resource_name=data.get("resourceName", ""),
            etag=data.get("etag", ""),
            group_type=data.get("groupType", ""),
            name=data.get("name", ""),
            member_resource_names=data.get("memberResourceNames", []),
            member_count=data.get("memberCount", 0),
            formatted_name=data.get("formattedName", "")
        )

    # ==================== Webhook Handling ====================

    async def handle_webhook(
        self,
        payload: bytes,
        signature: Optional[str] = None
    ) -> WebhookEvent:
        """
        Handle incoming webhook events.

        Supported events:
        - contact_created_updated: When a contact is created or updated
        - contact_group_created_updated: When a contact group is created or updated

        Args:
            payload: Raw webhook payload
            signature: Optional signature for verification

        Returns:
            WebhookEvent object

        Raises:
            Exception: If webhook is invalid or verification fails
        """
        # Verify signature if secret is configured
        if self.webhook_secret and signature:
            import hmac
            import hashlib

            expected_signature = hmac.new(
                self.webhook_secret.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(expected_signature, signature):
                raise Exception("Invalid webhook signature")

        try:
            event_data = json.loads(payload.decode("utf-8"))
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid webhook payload: {str(e)}")

        return WebhookEvent(
            event_type=event_data.get("eventType", ""),
            timestamp=event_data.get("timestamp", datetime.utcnow().isoformat()),
            data=event_data.get("data", {}),
            contact_resource_name=event_data.get("contactResourceName"),
            group_resource_name=event_data.get("groupResourceName")
        )

    def verify_webhook_signature(
        self,
        payload: bytes,
        signature: str
    ) -> bool:
        """
        Verify webhook signature.

        Args:
            payload: Raw webhook payload
            signature: Signature to verify

        Returns:
            True if signature is valid, False otherwise
        """
        if not self.webhook_secret:
            return False

        import hmac
        import hashlib

        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)


# ==================== Example Usage ====================

async def main():
    """Example usage of Google Contact client"""

    # Replace with your actual OAuth access token
    ACCESS_TOKEN = "your_oauth_access_token"

    async with GoogleContactClient(access_token=ACCESS_TOKEN) as client:
        try:
            # List contacts
            contacts = await client.list_contacts(page_size=20)
            print(f"Found {len(contacts)} contacts")
            for contact in contacts[:3]:
                print(f"  - {contact.display_name} ({contact.primary_email})")

            # Search contacts
            results = await client.search_contacts("John", page_size=10)
            print(f"\nSearch results: {len(results)}")
            for contact in results:
                print(f"  - {contact.display_name}")

            # Create a contact
            new_contact = await client.create_contact(
                given_name="Jane",
                family_name="Doe",
                email_addresses=[{"value": "jane@example.com", "type": "work"}],
                phone_numbers=[{"value": "+1234567890", "type": "mobile"}]
            )
            print(f"\nCreated contact: {new_contact.display_name}")
            print(f"Resource name: {new_contact.resource_name}")

            # Get specific contact
            if contacts:
                contact = await client.get_contact(contacts[0].resource_name)
                print(f"\nContact details: {contact.display_name}")
                print(f"Emails: {[e['value'] for e in contact.email_addresses]}")

            # Create a contact group
            new_group = await client.create_contact_group(
                name="My Team",
                group_type="USER_CONTACT_GROUP"
            )
            print(f"\nCreated group: {new_group.name}")
            print(f"Resource name: {new_group.resource_name}")

            # Add contact to group
            if contacts:
                updated_group = await client.add_contact_to_group(
                    resource_name=new_group.resource_name,
                    contact_resource_names=[contacts[0].resource_name]
                )
                print(f"Added contact to group. Members: {updated_group.member_count}")

            # Remove contact from group
            if contacts:
                updated_group = await client.remove_contact_from_group(
                    resource_name=new_group.resource_name,
                    contact_resource_names=[contacts[0].resource_name]
                )
                print(f"Removed contact from group. Members: {updated_group.member_count}")

            # Get multiple contacts
            if len(contacts) >= 2:
                resource_names = [c.resource_name for c in contacts[:2]]
                multiple = await client.get_multiple_contacts(resource_names)
                print(f"\nGot {len(multiple)} contacts")

            # Update group
            updated_group = await client.update_contact_group(
                resource_name=new_group.resource_name,
                name="Updated Team"
            )
            print(f"\nUpdated group name: {updated_group.name}")

            # Cleanup
            await client.delete_contact_group(new_group.resource_name)
            print("Deleted group")

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())