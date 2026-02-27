"""
ActiveCampaign API - CRM and Marketing Automation Client

Supports 16 API Actions:
- Account operations (create, update, get, delete)
- Contact operations (create, get, update, delete, list, search)
- Contact-List operations (add/remove)
- Deal operations
- Automation operations
- Notes operations
- Contact scores

Triggers:
- Deal created
- Contact added
- Contact created
- Contact custom field value created
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Account:
    """Account entity"""
    id: str
    name: str
    account_url: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Contact:
    """Contact entity"""
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""
    score: int = 0


@dataclass
class Deal:
    """Deal/transaction entity"""
    id: str
    contact_id: str
    value: float
    currency: str
    stage: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Note:
    """Note entity"""
    id: str
    contact_id: str
    note: str
    created_at: str = ""


class ActiveCampaignClient:
    """
    ActiveCampaign API client for CRM and marketing automation.

    API Documentation: https://developers.activecampaign.com/
    Uses API Key or OAuth for authentication.
    """

    BASE_URL = "https://your-account.api-us1.com/api/3"

    def __init__(self, api_url: str, api_key: str, access_token: Optional[str] = None):
        """
        Initialize ActiveCampaign client.

        Args:
            api_url: Your account API URL (e.g., https://account.api-us1.com/api/3)
            api_key: API key for authentication
            access_token: Optional OAuth access token
        """
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.access_token = access_token
        self.session = None

    async def __aenter__(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        else:
            headers["Api-Token"] = self.api_key

        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    # ==================== Account Operations ====================

    async def create_account(
        self,
        name: str,
        account_url: Optional[str] = None
    ) -> Account:
        """Create a new account"""
        payload = {"account": {"name": name}}
        if account_url:
            payload["account"]["accountUrl"] = account_url

        async with self.session.post(
            f"{self.api_url}/accounts",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in (200, 201):
                raise Exception(f"Failed to create account: {data}")

            account_data = data.get("account", {})
            return Account(
                id=str(account_data.get("id", "")),
                name=account_data.get("name", name),
                account_url=account_data.get("accountUrl"),
                created_at=account_data.get("cdate", ""),
                updated_at=account_data.get("mdate", "")
            )

    async def get_account(self, account_id: str) -> Account:
        """Get account details"""
        async with self.session.get(
            f"{self.api_url}/accounts/{account_id}"
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Failed to get account: {data}")

            account_data = data.get("account", {})
            return Account(
                id=str(account_data.get("id", account_id)),
                name=account_data.get("name", ""),
                account_url=account_data.get("accountUrl"),
                created_at=account_data.get("cdate", ""),
                updated_at=account_data.get("mdate", "")
            )

    async def update_account(
        self,
        account_id: str,
        name: Optional[str] = None,
        account_url: Optional[str] = None
    ) -> Account:
        """Update an account"""
        payload = {"account": {}}
        if name:
            payload["account"]["name"] = name
        if account_url:
            payload["account"]["accountUrl"] = account_url

        async with self.session.put(
            f"{self.api_url}/accounts/{account_id}",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Failed to update account: {data}")

            account_data = data.get("account", {})
            return Account(
                id=str(account_data.get("id", account_id)),
                name=account_data.get("name", name or ""),
                account_url=account_data.get("accountUrl", ""),
                created_at=account_data.get("cdate", ""),
                updated_at=account_data.get("mdate", "")
            )

    async def delete_account(self, account_id: str) -> bool:
        """Delete an account"""
        async with self.session.delete(
            f"{self.api_url}/accounts/{account_id}"
        ) as response:
            return response.status == 200

    # ==================== Contact Operations ====================

    async def create_contact(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Contact:
        """Create a new contact"""
        payload = {"contact": {"email": email}}
        if first_name:
            payload["contact"]["firstName"] = first_name
        if last_name:
            payload["contact"]["lastName"] = last_name
        if phone:
            payload["contact"]["phone"] = phone

        async with self.session.post(
            f"{self.api_url}/contacts",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in (200, 201):
                raise Exception(f"Failed to create contact: {data}")

            contact_data = data.get("contact", {})
            return Contact(
                id=str(contact_data.get("id", "")),
                email=contact_data.get("email", email),
                first_name=contact_data.get("firstName"),
                last_name=contact_data.get("lastName"),
                phone=contact_data.get("phone"),
                created_at=contact_data.get("cdate", ""),
                updated_at=contact_data.get("mdate", ""),
                score=contact_data.get("score", 0)
            )

    async def get_contact(self, contact_id: str) -> Contact:
        """Get contact details"""
        async with self.session.get(
            f"{self.api_url}/contacts/{contact_id}"
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Failed to get contact: {data}")

            contact_data = data.get("contact", {})
            return Contact(
                id=str(contact_data.get("id", contact_id)),
                email=contact_data.get("email", ""),
                first_name=contact_data.get("firstName"),
                last_name=contact_data.get("lastName"),
                phone=contact_data.get("phone"),
                created_at=contact_data.get("cdate", ""),
                updated_at=contact_data.get("mdate", ""),
                score=contact_data.get("score", 0)
            )

    async def search_contacts(
        self,
        email: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 20
    ) -> List[Contact]:
        """Search or list contacts"""
        params: Dict[str, Any] = {"limit": limit}

        if email:
            params["email"] = email
        elif query:
            params["query"] = query

        async with self.session.get(
            f"{self.api_url}/contacts",
            params=params
        ) as response:
            data = await response.json()

            if response.status != 200:
                raise Exception(f"Failed to search contacts: {data}")

            contacts_data = data.get("contacts", [])
            return [
                Contact(
                    id=str(c.get("id", "")),
                    email=c.get("email", ""),
                    first_name=c.get("firstName"),
                    last_name=c.get("lastName"),
                    phone=c.get("phone"),
                    created_at=c.get("cdate", ""),
                    updated_at=c.get("mdate", ""),
                    score=c.get("score", 0)
                )
                for c in contacts_data
            ]

    async def delete_contact(self, contact_id: str) -> bool:
        """Delete a contact"""
        async with self.session.delete(
            f"{self.api_url}/contacts/{contact_id}"
        ) as response:
            return response.status == 200

    async def link_contact_account(
        self,
        contact_id: str,
        account_id: str
    ) -> bool:
        """Link a contact to an account"""
        payload = {
            "accountContact": {
                "contact": str(contact_id),
                "account": str(account_id)
            }
        }

        async with self.session.post(
            f"{self.api_url}/accountContacts",
            json=payload
        ) as response:
            data = await response.json()
            return response.status in (200, 201)

    # ==================== Contact List Operations ====================

    async def add_contact_to_list(
        self,
        contact_id: str,
        list_id: str
    ) -> bool:
        """Add contact to a list"""
        payload = {
            "listContact": {
                "list": str(list_id),
                "contact": str(contact_id),
                "status": 1
            }
        }

        async with self.session.post(
            f"{self.api_url}/listContacts",
            json=payload
        ) as response:
            return response.status in (200, 201)

    async def remove_contact_from_list(
        self,
        contact_id: str,
        list_id: str
    ) -> bool:
        """Remove contact from a list"""
        async with self.session.delete(
            f"{self.api_url}/listContacts/{contact_id}",
            params={"list": list_id}
        ) as response:
            return response.status == 200

    # ==================== Deal Operations ====================

    async def create_deal(
        self,
        contact_id: str,
        value: float,
        currency: str = "USD",
        stage: Optional[str] = None
    ) -> Deal:
        """Create a new deal"""
        payload = {
            "deal": {
                "contact": str(contact_id),
                "value": float(value),
                "currency": str(currency)
            }
        }

        if stage:
            payload["deal"]["stage"] = str(stage)

        async with self.session.post(
            f"{self.api_url}/deals",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in (200, 201):
                raise Exception(f"Failed to create deal: {data}")

            deal_data = data.get("deal", {})
            return Deal(
                id=str(deal_data.get("id", "")),
                contact_id=str(deal_data.get("contact", contact_id)),
                value=float(deal_data.get("value", value)),
                currency=deal_data.get("currency", currency),
                stage=deal_data.get("stage"),
                created_at=deal_data.get("cdate", ""),
                updated_at=deal_data.get("mdate", "")
            )

    # ==================== Automation Operations ====================

    async def add_contact_to_automation(
        self,
        contact_id: str,
        automation_id: str
    ) -> bool:
        """Add contact to an automation"""
        payload = {
            "contactAutomation": {
                "contact": str(contact_id),
                "automation": str(automation_id)
            }
        }

        async with self.session.post(
            f"{self.api_url}/contactAutomations",
            json=payload
        ) as response:
            return response.status in (200, 201)

    # ==================== Note Operations ====================

    async def add_note(
        self,
        contact_id: str,
        note: str
    ) -> Note:
        """Add a note to a contact"""
        payload = {
            "note": {
                "contact": str(contact_id),
                "note": str(note)
            }
        }

        async with self.session.post(
            f"{self.api_url}/notes",
            json=payload
        ) as response:
            data = await response.json()

            if response.status not in (200, 201):
                raise Exception(f"Failed to add note: {data}")

            note_data = data.get("note", {})
            return Note(
                id=str(note_data.get("id", "")),
                contact_id=str(note_data.get("contact", contact_id)),
                note=note_data.get("note", note),
                created_at=note_data.get("cdate", "")
            )

    # ==================== Contact Score ====================

    async def get_contact_score(self, contact_id: str) -> int:
        """Get contact score"""
        contact = await self.get_contact(contact_id)
        return contact.score


# ==================== Example Usage ====================

async def main():
    """Example usage of ActiveCampaign client"""

    # Example configuration - replace with your actual credentials
    api_url = "https://your-account.api-us1.com/api/3"
    api_key = "your_api_key"

    async with ActiveCampaignClient(api_url=api_url, api_key=api_key) as client:
        # Create account
        account = await client.create_account(
            name="Example Corp",
            account_url="https://example.com"
        )
        print(f"Account created: {account.id} - {account.name}")

        # Create contact
        contact = await client.create_contact(
            email="john@example.com",
            first_name="John",
            last_name="Doe"
        )
        print(f"Contact created: {contact.id} - {contact.email}")

        # Link contact to account
        await client.link_contact_account(contact.id, account.id)
        print(f"Linked contact {contact.id} to account {account.id}")

        # Create deal
        deal = await client.create_deal(
            contact_id=contact.id,
            value=1000.0,
            currency="USD"
        )
        print(f"Deal created: {deal.id} - ${deal.value}")

        # Add note
        note = await client.add_note(contact.id, "Initial contact made")
        print(f"Note added: {note.note}")

        # Get contact score
        score = await client.get_contact_score(contact.id)
        print(f"Contact score: {score}")


if __name__ == "__main__":
    asyncio.run(main())