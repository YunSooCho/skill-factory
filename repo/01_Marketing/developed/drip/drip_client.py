"""
Drip API - Email Marketing Automation Client

Supports 12 API Actions:
- Subscriber operations (create, retrieve, update)
- Workflow operations (add/remove)
- Campaign subscription operations
- Tag operations (add/remove)
- Email campaign operations

Triggers:
- 21 webhook triggers for subscriber events
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
    tags: List[str] = None
    created_at: str = ""
    updated_at: str = ""
    status: str = "active"


@dataclass
class Campaign:
    """Campaign entity"""
    id: str
    name: str
    status: str
    created_at: str = ""


@dataclass
class Workflow:
    """Workflow entity"""
    id: str
    name: str
    status: str


class DripClient:
    """
    Drip API client for email marketing automation.

    API Documentation: https://developer.drip.com/
    Uses API Token for authentication.
    """

    BASE_URL = "https://api.getdrip.com/v2"

    def __init__(self, api_token: str, account_id: str):
        """
        Initialize Drip client.

        Args:
            api_token: API token for authentication
            account_id: Drip account ID
        """
        self.api_token = api_token
        self.account_id = account_id
        self.session = None
        self._rate_limit_remaining = None
        self._rate_limit_reset = None

    async def __aenter__(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }

        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle API response with rate limiting"""
        # Update rate limit info from headers
        self._rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        self._rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', 0))

        data = await response.json()

        if response.status not in (200, 201, 202, 204):
            error_msg = data.get('errors', [{}])[0].get('message', 'Unknown error')
            raise Exception(f"API Error [{response.status}]: {error_msg}")

        return data

    # ==================== Subscriber Operations ====================

    async def create_subscriber(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        double_optin: bool = False
    ) -> Subscriber:
        """Create a new subscriber"""
        payload = {
            "subscribers": [{
                "email": email,
                "double_optin": double_optin
            }]
        }

        if first_name:
            payload["subscribers"][0]["first_name"] = first_name
        if last_name:
            payload["subscribers"][0]["last_name"] = last_name
        if custom_fields:
            payload["subscribers"][0]["custom_fields"] = custom_fields
        if tags:
            payload["subscribers"][0]["tags"] = tags

        async with self.session.post(
            f"{self.BASE_URL}/{self.account_id}/subscribers",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            sub_data = data.get("subscribers", [{}])[0]

            return Subscriber(
                id=str(sub_data.get("id", "")),
                email=sub_data.get("email", email),
                first_name=sub_data.get("first_name"),
                last_name=sub_data.get("last_name"),
                tags=sub_data.get("tags", []),
                created_at=sub_data.get("created_at", ""),
                updated_at=sub_data.get("updated_at", ""),
                status=sub_data.get("status", "active")
            )

    async def get_subscriber(self, subscriber_id: str) -> Subscriber:
        """Get subscriber information"""
        async with self.session.get(
            f"{self.BASE_URL}/{self.account_id}/subscribers/{subscriber_id}"
        ) as response:
            data = await self._handle_response(response)
            sub_data = data.get("subscribers", [{}])[0]

            return Subscriber(
                id=str(sub_data.get("id", subscriber_id)),
                email=sub_data.get("email", ""),
                first_name=sub_data.get("first_name"),
                last_name=sub_data.get("last_name"),
                tags=sub_data.get("tags", []),
                created_at=sub_data.get("created_at", ""),
                updated_at=sub_data.get("updated_at", ""),
                status=sub_data.get("status", "active")
            )

    async def get_subscriber_by_email(self, email: str) -> Optional[Subscriber]:
        """Get subscriber by email address"""
        async with self.session.get(
            f"{self.BASE_URL}/{self.account_id}/subscribers",
            params={"email": email}
        ) as response:
            data = await self._handle_response(response)
            subscribers = data.get("subscribers", [])

            if not subscribers:
                return None

            sub_data = subscribers[0]
            return Subscriber(
                id=str(sub_data.get("id", "")),
                email=sub_data.get("email", email),
                first_name=sub_data.get("first_name"),
                last_name=sub_data.get("last_name"),
                tags=sub_data.get("tags", []),
                created_at=sub_data.get("created_at", ""),
                updated_at=sub_data.get("updated_at", ""),
                status=sub_data.get("status", "active")
            )

    async def list_subscribers(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        page: int = 1
    ) -> List[Subscriber]:
        """List all subscribers"""
        params = {"per_page": limit, "page": page}
        if status:
            params["status"] = status

        async with self.session.get(
            f"{self.BASE_URL}/{self.account_id}/subscribers",
            params=params
        ) as response:
            data = await self._handle_response(response)
            subscribers_data = data.get("subscribers", [])

            return [
                Subscriber(
                    id=str(s.get("id", "")),
                    email=s.get("email", ""),
                    first_name=s.get("first_name"),
                    last_name=s.get("last_name"),
                    tags=s.get("tags", []),
                    created_at=s.get("created_at", ""),
                    updated_at=s.get("updated_at", ""),
                    status=s.get("status", "active")
                )
                for s in subscribers_data
            ]

    async def update_subscriber(
        self,
        subscriber_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Subscriber:
        """Update subscriber information"""
        payload = {"subscribers": [{}]}
        if email:
            payload["subscribers"][0]["email"] = email
        if first_name:
            payload["subscribers"][0]["first_name"] = first_name
        if last_name:
            payload["subscribers"][0]["last_name"] = last_name
        if custom_fields:
            payload["subscribers"][0]["custom_fields"] = custom_fields

        async with self.session.put(
            f"{self.BASE_URL}/{self.account_id}/subscribers/{subscriber_id}",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            sub_data = data.get("subscribers", [{}])[0]

            return Subscriber(
                id=str(sub_data.get("id", subscriber_id)),
                email=sub_data.get("email", email or ""),
                first_name=sub_data.get("first_name"),
                last_name=sub_data.get("last_name"),
                tags=sub_data.get("tags", []),
                created_at=sub_data.get("created_at", ""),
                updated_at=sub_data.get("updated_at", ""),
                status=sub_data.get("status", "active")
            )

    async def unsubscribe_all(self, subscriber_id: str) -> bool:
        """Unsubscribe subscriber from all mailings"""
        payload = {"subscribers": [{"unsubscribed": True}]}

        async with self.session.put(
            f"{self.BASE_URL}/{self.account_id}/subscribers/{subscriber_id}",
            json=payload
        ) as response:
            await self._handle_response(response)
            return True

    # ==================== Workflow Operations ====================

    async def add_to_workflow(
        self,
        subscriber_id: str,
        workflow_id: str
    ) -> bool:
        """Add subscriber to a workflow"""
        payload = {
            "subscribers": [{
                "id": subscriber_id,
                "workflow_id": workflow_id
            }]
        }

        async with self.session.post(
            f"{self.BASE_URL}/{self.account_id}/workflows/{workflow_id}/subscribers",
            json=payload
        ) as response:
            await self._handle_response(response)
            return True

    async def remove_from_workflow(
        self,
        subscriber_id: str,
        workflow_id: str
    ) -> bool:
        """Remove subscriber from a workflow"""
        async with self.session.delete(
            f"{self.BASE_URL}/{self.account_id}/subscribers/{subscriber_id}/workflows/{workflow_id}"
        ) as response:
            await self._handle_response(response)
            return True

    # ==================== Campaign Operations ====================

    async def subscribe_to_campaign(
        self,
        subscriber_id: str,
        campaign_id: str
    ) -> bool:
        """Subscribe user to an email campaign"""
        payload = {
            "subscribers": [{
                "campaign_id": campaign_id
            }]
        }

        async with self.session.post(
            f"{self.BASE_URL}/{self.account_id}/campaigns/{campaign_id}/subscribers",
            json=payload
        ) as response:
            await self._handle_response(response)
            return True

    async def unsubscribe_from_campaign(
        self,
        subscriber_id: str,
        campaign_id: str
    ) -> bool:
        """Remove subscriber from email campaign"""
        async with self.session.delete(
            f"{self.BASE_URL}/{self.account_id}/campaigns/{campaign_id}/subscribers/{subscriber_id}"
        ) as response:
            await self._handle_response(response)
            return True

    async def get_campaign_subscription(
        self,
        campaign_id: str,
        subscriber_id: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieve campaign subscription for subscriber"""
        async with self.session.get(
            f"{self.BASE_URL}/{self.account_id}/campaigns/{campaign_id}/subscribers/{subscriber_id}"
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)
            return data.get("subscribers", [{}])[0]

    async def list_campaign_subscribers(
        self,
        campaign_id: str,
        status: Optional[str] = None,
        limit: int = 100,
        page: int = 1
    ) -> List[Subscriber]:
        """List all subscribers of a specified campaign"""
        params = {"per_page": limit, "page": page}
        if status:
            params["status"] = status

        async with self.session.get(
            f"{self.BASE_URL}/{self.account_id}/campaigns/{campaign_id}/subscribers",
            params=params
        ) as response:
            data = await self._handle_response(response)
            subscribers_data = data.get("subscribers", [])

            return [
                Subscriber(
                    id=str(s.get("id", "")),
                    email=s.get("email", ""),
                    first_name=s.get("first_name"),
                    last_name=s.get("last_name"),
                    tags=s.get("tags", []),
                    created_at=s.get("created_at", ""),
                    updated_at=s.get("updated_at", ""),
                    status=s.get("status", "active")
                )
                for s in subscribers_data
            ]

    # ==================== Tag Operations ====================

    async def add_tag(
        self,
        subscriber_id: str,
        tag: str
    ) -> bool:
        """Add tag to subscriber"""
        payload = {
            "subscribers": [{
                "tags": [tag]
            }]
        }

        async with self.session.post(
            f"{self.BASE_URL}/{self.account_id}/subscribers/{subscriber_id}/tags",
            json=payload
        ) as response:
            await self._handle_response(response)
            return True

    async def remove_tag(
        self,
        subscriber_id: str,
        tag: str
    ) -> bool:
        """Remove tag from subscriber"""
        async with self.session.delete(
            f"{self.BASE_URL}/{self.account_id}/subscribers/{subscriber_id}/tags/{tag}"
        ) as response:
            await self._handle_response(response)
            return True

    # ==================== Campaign List Operations ====================

    async def list_campaigns(self) -> List[Campaign]:
        """List all campaigns"""
        async with self.session.get(
            f"{self.BASE_URL}/{self.account_id}/campaigns"
        ) as response:
            data = await self._handle_response(response)
            campaigns_data = data.get("campaigns", [])

            return [
                Campaign(
                    id=str(c.get("id", "")),
                    name=c.get("name", ""),
                    status=c.get("status", ""),
                    created_at=c.get("created_at", "")
                )
                for c in campaigns_data
            ]

    async def list_workflows(self) -> List[Workflow]:
        """List all workflows"""
        async with self.session.get(
            f"{self.BASE_URL}/{self.account_id}/workflows"
        ) as response:
            data = await self._handle_response(response)
            workflows_data = data.get("workflows", [])

            return [
                Workflow(
                    id=str(w.get("id", "")),
                    name=w.get("name", ""),
                    status=w.get("status", "")
                )
                for w in workflows_data
            ]


# ==================== Example Usage ====================

async def main():
    """Example usage of Drip client"""

    # Example configuration - replace with your actual credentials
    api_token = "your_api_token"
    account_id = "your_account_id"

    async with DripClient(api_token=api_token, account_id=account_id) as client:
        # Create subscriber
        subscriber = await client.create_subscriber(
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            tags=["new-signup"]
        )
        print(f"Subscriber created: {subscriber.id} - {subscriber.email}")

        # Get subscriber
        subscriber = await client.get_subscriber(subscriber.id)
        print(f"Subscriber: {subscriber.email} - Status: {subscriber.status}")

        # List campaigns
        campaigns = await client.list_campaigns()
        print(f"Campaigns: {len(campaigns)}")

        # Add to workflow
        workflows = await client.list_workflows()
        if workflows:
            await client.add_to_workflow(subscriber.id, workflows[0].id)
            print(f"Added to workflow: {workflows[0].name}")

        # Add tag
        await client.add_tag(subscriber.id, "vip-customer")
        print("Tag added")


if __name__ == "__main__":
    asyncio.run(main())