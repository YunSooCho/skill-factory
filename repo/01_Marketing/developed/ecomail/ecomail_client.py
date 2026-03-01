"""
Ecomail API - Email Marketing Client

Supports 9 API Actions:
- Subscriber operations (create, get, update, delete, search)
- Contact search
- Campaign statistics
- Transactional email statistics

Triggers:
- 3 webhook triggers for email events
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Subscriber:
    """Subscriber entity"""
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: str = "active"
    tags: List[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class CampaignStats:
    """Campaign statistics entity"""
    campaign_id: str
    name: str
    sent: int = 0
    opens: int = 0
    clicks: int = 0
    bounces: int = 0
    unsubscribes: int = 0


@dataclass
class EmailStats:
    """Transactional email statistics entity"""
    total_sent: int = 0
    delivered: int = 0
    opens: int = 0
    clicks: int = 0
    bounces: int = 0


class EcomailClient:
    """
    Ecomail API client for email marketing.

    API Documentation: https://ecomailapp.com/api/
    Uses API Key for authentication.
    """

    BASE_URL = "https://app.ecomailapp.cz/public/api/v2"

    def __init__(self, api_key: str):
        """
        Initialize Ecomail client.

        Args:
            api_key: API token for authentication
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "key": self.api_key
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
            error_msg = data.get('message', 'Unknown error')
            raise Exception(f"API Error [{response.status}]: {error_msg}")

        return data

    # ==================== Subscriber Operations ====================

    async def create_subscriber(
        self,
        email: str,
        list_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        phone: Optional[str] = None,
        gender: Optional[str] = None
    ) -> Subscriber:
        """Create a new subscriber in a list"""
        payload = {
            "subscriber": {
                "email": email
            }
        }

        if first_name:
            payload["subscriber"]["first_name"] = first_name
        if last_name:
            payload["subscriber"]["last_name"] = last_name
        if tags:
            payload["subscriber"]["tags"] = tags
        if phone:
            payload["subscriber"]["phone"] = phone
        if gender:
            payload["subscriber"]["gender"] = gender

        async with self.session.post(
            f"{self.BASE_URL}/lists/{list_id}/subscribe",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            sub_data = data.get("subscriber", {})

            return Subscriber(
                id=str(sub_data.get("id", "")),
                email=sub_data.get("email", email),
                first_name=sub_data.get("first_name"),
                last_name=sub_data.get("last_name"),
                status=sub_data.get("status", "active"),
                tags=sub_data.get("tags", []),
                created_at=sub_data.get("created_at", ""),
                updated_at=sub_data.get("updated_at", "")
            )

    async def get_subscriber_detail(self, subscriber_id: str) -> Optional[Subscriber]:
        """Get subscriber details by ID"""
        async with self.session.get(
            f"{self.BASE_URL}/subscribers/{subscriber_id}"
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)
            sub_data = data.get("subscriber", {})

            return Subscriber(
                id=str(sub_data.get("id", subscriber_id)),
                email=sub_data.get("email", ""),
                first_name=sub_data.get("first_name"),
                last_name=sub_data.get("last_name"),
                status=sub_data.get("status", "active"),
                tags=sub_data.get("tags", []),
                created_at=sub_data.get("created_at", ""),
                updated_at=sub_data.get("updated_at", "")
            )

    async def get_subscriber_from_list(
        self,
        list_id: str,
        subscriber_email: str
    ) -> Optional[Subscriber]:
        """Get subscriber from specific list by email"""
        async with self.session.get(
            f"{self.BASE_URL}/lists/{list_id}/subscribers/{subscriber_email}"
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)
            sub_data = data.get("subscriber", {})

            return Subscriber(
                id=str(sub_data.get("id", "")),
                email=sub_data.get("email", subscriber_email),
                first_name=sub_data.get("first_name"),
                last_name=sub_data.get("last_name"),
                status=sub_data.get("status", "active"),
                tags=sub_data.get("tags", []),
                created_at=sub_data.get("created_at", ""),
                updated_at=sub_data.get("updated_at", "")
            )

    async def update_subscriber(
        self,
        subscriber_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        phone: Optional[str] = None
    ) -> Subscriber:
        """Update subscriber details"""
        payload: Dict[str, Any] = {}

        if email:
            payload["email"] = email
        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if tags:
            payload["tags"] = tags
        if phone:
            payload["phone"] = phone

        async with self.session.put(
            f"{self.BASE_URL}/subscribers/{subscriber_id}",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            sub_data = data.get("subscriber", {})

            return Subscriber(
                id=str(sub_data.get("id", subscriber_id)),
                email=sub_data.get("email", email or ""),
                first_name=sub_data.get("first_name"),
                last_name=sub_data.get("last_name"),
                status=sub_data.get("status", "active"),
                tags=sub_data.get("tags", []),
                created_at=sub_data.get("created_at", ""),
                updated_at=sub_data.get("updated_at", "")
            )

    async def delete_subscriber(self, subscriber_id: str) -> bool:
        """Delete a subscriber"""
        async with self.session.delete(
            f"{self.BASE_URL}/subscribers/{subscriber_id}"
        ) as response:
            if response.status == 404:
                return False
            await self._handle_response(response)
            return True

    async def search_subscribers(
        self,
        email: Optional[str] = None,
        list_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Subscriber]:
        """Search subscribers"""
        url = f"{self.BASE_URL}/subscribers"
        params: Dict[str, Any] = {"limit": limit}

        if email:
            params["email"] = email
        if list_id:
            url = f"{self.BASE_URL}/lists/{list_id}/subscribers"

        async with self.session.get(url, params=params) as response:
            data = await self._handle_response(response)
            subscribers_data = data.get("subscribers", [])

            return [
                Subscriber(
                    id=str(s.get("id", "")),
                    email=s.get("email", ""),
                    first_name=s.get("first_name"),
                    last_name=s.get("last_name"),
                    status=s.get("status", "active"),
                    tags=s.get("tags", []),
                    created_at=s.get("created_at", ""),
                    updated_at=s.get("updated_at", "")
                )
                for s in subscribers_data
            ]

    async def search_contact(self, query: str) -> List[Subscriber]:
        """Search contacts by query"""
        async with self.session.get(
            f"{self.BASE_URL}/contacts",
            params={"search": query}
        ) as response:
            data = await self._handle_response(response)
            contacts_data = data.get("contacts", [])

            return [
                Subscriber(
                    id=str(c.get("id", "")),
                    email=c.get("email", ""),
                    first_name=c.get("first_name"),
                    last_name=c.get("last_name"),
                    status=c.get("status", "active"),
                    tags=c.get("tags", []),
                    created_at=c.get("created_at", ""),
                    updated_at=c.get("updated_at", "")
                )
                for c in contacts_data
            ]

    # ==================== Campaign Statistics ====================

    async def get_campaign_stats(
        self,
        campaign_id: str
    ) -> Optional[CampaignStats]:
        """Get campaign statistics"""
        async with self.session.get(
            f"{self.BASE_URL}/campaigns/{campaign_id}/stats"
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)

            return CampaignStats(
                campaign_id=str(data.get("campaign_id", campaign_id)),
                name=data.get("name", ""),
                sent=data.get("sent", 0),
                opens=data.get("opens", 0),
                clicks=data.get("clicks", 0),
                bounces=data.get("bounces", 0),
                unsubscribes=data.get("unsubscribes", 0)
            )

    # ==================== Transactional Email Statistics ====================

    async def get_transactional_email_stats(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> EmailStats:
        """Get transactional email statistics"""
        params: Dict[str, Any] = {}

        if start_date:
            params["from"] = start_date
        if end_date:
            params["to"] = end_date

        async with self.session.get(
            f"{self.BASE_URL}/transactional/stats",
            params=params
        ) as response:
            data = await self._handle_response(response)

            return EmailStats(
                total_sent=data.get("total_sent", 0),
                delivered=data.get("delivered", 0),
                opens=data.get("opens", 0),
                clicks=data.get("clicks", 0),
                bounces=data.get("bounces", 0)
            )


# ==================== Example Usage ====================

async def main():
    """Example usage of Ecomail client"""

    # Example configuration - replace with your actual credentials
    api_key = "your_api_key"
    list_id = "your_list_id"

    async with EcomailClient(api_key=api_key) as client:
        # Create subscriber
        subscriber = await client.create_subscriber(
            email="john@example.com",
            list_id=list_id,
            first_name="John",
            last_name="Doe",
            tags=["new-signup"]
        )
        print(f"Subscriber created: {subscriber.email}")

        # Get subscriber detail
        subscriber = await client.get_subscriber_detail(subscriber.id)
        print(f"Subscriber: {subscriber.first_name} {subscriber.last_name}")

        # Search subscribers
        subscribers = await client.search_subscribers(list_id=list_id)
        print(f"Found {len(subscribers)} subscribers")

        # Get campaign stats
        stats = await client.get_campaign_stats("campaign_123")
        if stats:
            print(f"Campaign '{stats.name}': {stats.opens} opens")

        # Get transactional email stats
        email_stats = await client.get_transactional_email_stats()
        print(f"Transactional emails sent: {email_stats.total_sent}")


if __name__ == "__main__":
    asyncio.run(main())