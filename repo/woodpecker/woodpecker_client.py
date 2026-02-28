"""
Woodpecker API Client
Cold email automation and prospect management

API Documentation: https://woodpecker.co/help/api/
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import time


@dataclass
class Prospect:
    """Prospect data model"""
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    website: Optional[str] = None
    title: Optional[str] = None
    industry: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


@dataclass
class BlackListEntry:
    """Blacklist entry data model"""
    email: str
    reason: Optional[str] = None
    added_at: Optional[str] = None


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, max_requests: int = 120, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.time()
            # Remove old requests outside the time window
            self.requests = [req_time for req_time in self.requests
                            if now - req_time < self.per_seconds]

            if len(self.requests) >= self.max_requests:
                sleep_time = self.per_seconds - (now - self.requests[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    self.requests = []

            self.requests.append(now)


class WoodpeckerClient:
    """
    Woodpecker API client for cold email automation.

    API Documentation: https://woodpecker.co/help/api/
    Rate Limit: 120 requests per 60 seconds
    """

    BASE_URL = "https://api.woodpecker.co/v1"

    def __init__(self, api_key: str):
        """
        Initialize Woodpecker API client.

        Args:
            api_key: Your Woodpecker API key
        """
        self.api_key = api_key
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=120, per_seconds=60)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API request with error handling and rate limiting.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails or returns error
        """
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}{endpoint}"

        try:
            async with self.session.request(
                method,
                url,
                headers=self._get_headers(),
                params=params,
                json=json_data
            ) as response:
                data = await response.json()

                if response.status >= 400:
                    error_msg = data.get("error", data.get("message", "Unknown error"))
                    raise Exception(f"Woodpecker API error ({response.status}): {error_msg}")

                return data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during Woodpecker API request: {str(e)}")

    # ==================== Prospect Management ====================

    async def add_prospects(
        self,
        prospects: List[Prospect],
        campaign_id: str,
        skip_duplicates: bool = True
    ) -> Dict[str, Any]:
        """
        Add prospects to a campaign.

        Args:
            prospects: List of Prospect objects
            campaign_id: Campaign ID to add prospects to
            skip_duplicates: Skip duplicate emails (default: True)

        Returns:
            Response with added prospects info

        Raises:
            Exception: If request fails
        """
        prospect_data = []
        for prospect in prospects:
            data = {"email": prospect.email}
            if prospect.first_name:
                data["first_name"] = prospect.first_name
            if prospect.last_name:
                data["last_name"] = prospect.last_name
            if prospect.company:
                data["company"] = prospect.company
            if prospect.website:
                data["website"] = prospect.website
            if prospect.title:
                data["title"] = prospect.title
            if prospect.industry:
                data["industry"] = prospect.industry
            if prospect.city:
                data["city"]
                data["city"] = prospect.city
            if prospect.state:
                data["state"] = prospect.state
            if prospect.country:
                data["country"] = prospect.country

            prospect_data.append(data)

        return await self._request(
            "POST",
            f"/campaign/{campaign_id}/prospects",
            json_data={
                "prospects": prospect_data,
                "skip_duplicates": skip_duplicates
            }
        )

    async def update_prospects(self, prospects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update prospect information.

        Args:
            prospects: List of prospect update data with 'id' field

        Returns:
            Response with updated prospects info

        Raises:
            Exception: If request fails
        """
        return await self._request(
            "PUT",
            "/prospects/batch",
            json_data={"prospects": prospects}
        )

    async def delete_prospect(self, prospect_id: str) -> Dict[str, Any]:
        """
        Delete a prospect.

        Args:
            prospect_id: ID of the prospect to delete

        Returns:
            Response confirming deletion

        Raises:
            Exception: If request fails
        """
        return await self._request(
            "DELETE",
            f"/prospects/{prospect_id}"
        )

    async def search_prospects(
        self,
        query: Optional[str] = None,
        campaign_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Search prospects with filters.

        Args:
            query: Search query (email, name, company)
            campaign_id: Filter by campaign ID
            status: Filter by status (active, replied, interested, etc.)
            limit: Maximum number of results (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of prospect data

        Raises:
            Exception: If request fails
        """
        params = {"limit": limit, "offset": offset}

        if query:
            params["q"] = query
        if campaign_id:
            params["campaign_id"] = campaign_id
        if status:
            params["status"] = status

        response = await self._request("GET", "/prospects", params=params)
        return response.get("prospects", [])

    # ==================== Blacklist Management ====================

    async def add_black_list(self, emails: List[str], reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Add emails to blacklist.

        Args:
            emails: List of email addresses to blacklist
            reason: Optional reason for blacklisting

        Returns:
            Response with added blacklist entries

        Raises:
            Exception: If request fails
        """
        data = {"emails": emails}
        if reason:
            data["reason"] = reason

        return await self._request(
            "POST",
            "/blacklist",
            json_data=data
        )

    async def list_black_list(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List blacklisted emails.

        Args:
            limit: Maximum number of results (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of blacklist entries

        Raises:
            Exception: If request fails
        """
        params = {"limit": limit, "offset": offset}
        response = await self._request("GET", "/blacklist", params=params)
        return response.get("blacklist", [])

    async def delete_black_list(self, email: str) -> Dict[str, Any]:
        """
        Remove email from blacklist.

        Args:
            email: Email address to remove from blacklist

        Returns:
            Response confirming removal

        Raises:
            Exception: If request fails
        """
        return await self._request(
            "DELETE",
            f"/blacklist/{email}"
        )

    # ==================== Webhook Handling ====================

    def handle_webhook(self, event_data: Dict[str, Any], signature: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle webhook events from Woodpecker.

        Supported events:
        - prospect_bounce
        - clicked_link
        - campaign_sent
        - task_completed
        - prospect_replied
        - prospect_not_interested
        - task_ignored
        - prospect_interested
        - prospect_later
        - prospect_blacklisted
        - prospect_opt_out
        - email_opened
        - prospect_saved
        - prospect_non_responsive
        - new_task

        Args:
            event_data: Webhook event data
            signature: Optional webhook signature for verification

        Returns:
            Processed event data

        Raises:
            Exception: If event data is invalid
        """
        if not event_data or "event" not in event_data:
            raise ValueError("Invalid webhook event data: missing 'event' field")

        event_type = event_data["event"]
        event_data["processed_at"] = datetime.utcnow().isoformat()

        # Process based on event type
        if event_type == "prospect_bounce":
            event_data["category"] = "bounce"
        elif event_type == "clicked_link":
            event_data["category"] = "engagement"
        elif event_type == "campaign_sent":
            event_data["category"] = "campaign"
        elif event_type == "task_completed":
            event_data["category"] = "task"
        elif event_type == "prospect_replied":
            event_data["category"] = "engagement"
        elif event_type in ("prospect_not_interested", "prospect_interested"):
            event_data["category"] = "interest"
        elif event_type == "prospect_later":
            event_data["category"] = "timing"
        elif event_type == "prospect_blacklisted":
            event_data["category"] = "blacklist"
        elif event_type == "prospect_opt_out":
            event_data["category"] = "opt_out"
        elif event_type == "email_opened":
            event_data["category"] = "engagement"
        elif event_type == "prospect_saved":
            event_data["category"] = "saved"
        elif event_type == "prospect_non_responsive":
            event_data["category"] = "non_responsive"
        elif event_type == "new_task":
            event_data["category"] = "task"

        return event_data