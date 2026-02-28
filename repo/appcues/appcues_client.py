"""
Appcues API Client

User onboarding and product adoption platform for creating
guided tours, checklists, and in-app experiences.

API Actions (estimated 8-12):
1. Create Flow
2. Update Flow
3. Get Flow
4. List Flows
5. Create User Event
6. Get User Profile
7. Create Checklist
8. Launch Experience

Triggers (estimated 3-5):
- User Completes Flow
- User Starts Flow
- User Dismisses Flow
- Checklist Item Completed

Authentication: API Key (Account ID + Secret)
Base URL: https://api.appcues.com/v1
Documentation: https://docs.appcues.com/
Rate Limiting: 1000 requests per hour
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class Flow:
    """Flow model (guided tour or experience)"""
    id: str
    name: str
    flow_type: str
    state: str
    created_at: str
    updated_at: str
    published_at: Optional[str] = None
    is_published: bool = False


@dataclass
class User:
    """User profile model"""
    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None
    created_at: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Event:
    """User event model"""
    event_name: str
    user_id: str
    timestamp: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Checklist:
    """Checklist model"""
    id: str
    name: str
    position: int
    items: List[Dict[str, Any]] = field(default_factory=list)
    created_at: Optional[str] = None


class AppcuesClient:
    """
    Appcues API client for user onboarding.

    Supports: Flows, Users, Events, Checklists
    Rate limit: 1000 requests/hour
    """

    BASE_URL = "https://api.appcues.com/v1"
    RATE_LIMIT = 1000  # requests per hour

    def __init__(self, account_id: str, api_key: str):
        """
        Initialize Appcues client.

        Args:
            account_id: Your Appcues account ID
            api_key: Your Appcues API key (secret)
        """
        self.account_id = account_id
        self.api_key = api_key
        self.session = None
        self._auth_header = f"Basic {self._encode_auth(account_id, api_key)}"
        self._request_count = 0
        self._request_window_start = datetime.now()
        self._headers = {
            "Authorization": self._auth_header,
            "Content-Type": "application/json"
        }

    def _encode_auth(self, account_id: str, api_key: str) -> str:
        """Encode credentials for Basic Auth"""
        import base64
        credentials = f"{account_id}:{api_key}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return encoded

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _check_rate_limit(self):
        """Check and enforce rate limiting"""
        now = datetime.now()
        time_window = (now - self._request_window_start).total_seconds()

        if time_window >= 3600:
            self._request_count = 0
            self._request_window_start = now

        if self._request_count >= self.RATE_LIMIT:
            wait_time = 3600 - int(time_window)
            if wait_time > 0:
                await asyncio.sleep(wait_time)
                self._request_count = 0
                self._request_window_start = datetime.now()

        self._request_count += 1

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make API request with rate limiting"""
        await self._check_rate_limit()

        url = f"{self.BASE_URL}/{self.account_id}{endpoint}"

        async with self.session.request(
            method,
            url,
            headers=self._headers,
            json=data,
            params=params
        ) as response:
            try:
                result = await response.json()
            except:
                result = {}

            if response.status not in [200, 201]:
                raise Exception(
                    f"Appcues API error: {response.status} - {result}"
                )

            return result

    # ==================== Flow Operations ====================

    async def create_flow(
        self,
        name: str,
        flow_type: str = "tour",
        state: str = "draft"
    ) -> Flow:
        """Create a new flow"""
        data = {
            "name": name,
            "flowType": flow_type,
            "state": state
        }
        response = await self._make_request("POST", "/flows", data=data)
        return Flow(**response)

    async def get_flow(self, flow_id: str) -> Flow:
        """Get flow by ID"""
        response = await self._make_request("GET", f"/flows/{flow_id}")
        return Flow(**response)

    async def update_flow(
        self,
        flow_id: str,
        **fields
    ) -> Flow:
        """Update a flow"""
        response = await self._make_request("PUT", f"/flows/{flow_id}", data=fields)
        return Flow(**response)

    async def list_flows(
        self,
        state: Optional[str] = None,
        limit: int = 100
    ) -> List[Flow]:
        """List all flows"""
        params = {}
        if state:
            params["state"] = state

        response = await self._make_request("GET", "/flows", params=params)
        flows = response.get("flows", [])
        return [Flow(**f) for f in flows[:limit]]

    # ==================== User Operations ====================

    async def get_user_profile(self, user_id: str) -> User:
        """Get user profile"""
        response = await self._make_request("GET", f"/users/{user_id}")
        return User(
            user_id=user_id,
            email=response.get("email"),
            name=response.get("name"),
            created_at=response.get("createdAt"),
            properties=response.get("profile", {}),
            meta=response.get("meta", {})
        )

    async def update_user_profile(
        self,
        user_id: str,
        **properties
    ) -> bool:
        """Update user profile properties"""
        await self._make_request("PUT", f"/users/{user_id}", data=properties)
        return True

    async def create_user_event(
        self,
        user_id: str,
        event_name: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a user event for segmentation"""
        data = {
            "user_id": user_id,
            "name": event_name,
            "properties": properties or {}
        }
        response = await self._make_request("POST", "/user-events", data=data)
        return response

    async def launch_experience(
        self,
        user_id: str,
        flow_id: str
    ) -> bool:
        """Launch an experience (flow) for a specific user"""
        data = {
            "user_id": user_id,
            "flow_id": flow_id
        }
        await self._make_request("POST", "/experiences/launch", data=data)
        return True

    # ==================== Checklist Operations ====================

    async def create_checklist(
        self,
        name: str,
        items: List[Dict[str, Any]],
        position: int = 0
    ) -> Checklist:
        """Create a checklist"""
        data = {
            "name": name,
            "items": items,
            "position": position
        }
        response = await self._make_request("POST", "/checklists", data=data)
        return Checklist(**response)

    async def get_checklist(self, checklist_id: str) -> Checklist:
        """Get checklist by ID"""
        response = await self._make_request("GET", f"/checklists/{checklist_id}")
        return Checklist(**response)

    # ==================== Webhook Handling ====================

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle webhook events from Appcues"""
        event_type = webhook_data.get("type", "unknown")
        user_id = webhook_data.get("userId")
        flow_id = webhook_data.get("flowId")

        return {
            "event_type": event_type,
            "user_id": user_id,
            "flow_id": flow_id,
            "raw_data": webhook_data
        }


async def main():
    """Example usage"""
    account_id = "your_account_id"
    api_key = "your_api_key"

    async with AppcuesClient(account_id, api_key) as client:
        # List flows
        flows = await client.list_flows(state="published")
        print(f"Found {len(flows)} published flows")

        # Create a user event
        await client.create_user_event(
            user_id="user_123",
            event_name="signed_up",
            properties={"source": "organic"}
        )

if __name__ == "__main__":
    asyncio.run(main())