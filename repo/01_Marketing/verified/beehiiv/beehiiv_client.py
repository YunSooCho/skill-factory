"""
Beehiiv API - Newsletter Platform Client

Supports:
- Add Tags to Subscription
- Create Subscription
- Retrieve Subscription by ID
- Update Subscription
- Retrieve a Single Post
- List Subscriber Ids
- Retrieve Segments
- Delete Subscription
- Search Posts by Publication
- Retrieve Subscription by Email
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class Subscription:
    """Subscription object from Beehiiv API"""
    id: str
    email: str
    status: str
    created: int
    subscription_tier: str
    subscription_premium_tier_names: List[str] = field(default_factory=list)
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_channel: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_term: Optional[str] = None
    utm_content: Optional[str] = None
    referring_site: Optional[str] = None
    referral_code: Optional[str] = None
    custom_fields: List[Dict[str, Any]] = field(default_factory=list)
    stripe_customer_id: Optional[str] = None


@dataclass
class Post:
    """Post object from Beehiiv API"""
    id: str
    title: str
    subtitle: Optional[str]
    status: str
    published_date: Optional[int]
    thumbnail_url: Optional[str]
    slug: str = ""
    content: Optional[str] = None
    engagement_score: Optional[int] = None


@dataclass
class Segment:
    """Segment object from Beehiiv API"""
    id: str
    name: str
    description: Optional[str]
    count: int
    created: int


@dataclass
class SubscriptionCreateRequest:
    """Request for creating a subscription"""
    email: str
    reactivate_existing: bool = False
    send_welcome_email: bool = False
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_term: Optional[str] = None
    utm_content: Optional[str] = None
    referring_site: Optional[str] = None
    referral_code: Optional[str] = None
    custom_fields: Optional[List[Dict[str, str]]] = None
    double_opt_override: Optional[str] = None  # "on", "off", "not_set"
    tier: Optional[str] = None  # "free", "premium"
    premium_tiers: Optional[List[str]] = None
    premium_tier_ids: Optional[List[str]] = None
    stripe_customer_id: Optional[str] = None
    automation_ids: Optional[List[str]] = None


@dataclass
class SubscriptionUpdateRequest:
    """Request for updating a subscription"""
    email: Optional[str] = None
    tier: Optional[str] = None
    premium_tiers: Optional[List[str]] = None
    premium_tier_ids: Optional[List[str]] = None
    custom_fields: Optional[List[Dict[str, str]]] = None
    status: Optional[str] = None


class BeehiivAPIClient:
    """
    Beehiiv API client for newsletter platform management.

    API Documentation: https://developers.beehiiv.com
    Authentication: Bearer token via Authorization header

    Rate Limits: See https://developers.beehiiv.com/welcome/rate-limiting
    """

    BASE_URL = "https://api.beehiiv.com/v2"

    def __init__(self, api_key: str, publication_id: str):
        """
        Initialize Beehiiv API client.

        Args:
            api_key: Your Beehiiv API key (Bearer token)
            publication_id: The publication ID (format: pub_xxxxxxxxxxxxxxxxx)
        """
        self.api_key = api_key
        self.publication_id = publication_id
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with Bearer token authentication"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _parse_subscription(self, data: Dict[str, Any]) -> Subscription:
        """Parse subscription data from API response"""
        return Subscription(
            id=data.get("id", ""),
            email=data.get("email", ""),
            status=data.get("status", ""),
            created=int(data.get("created", 0)),
            subscription_tier=data.get("subscription_tier", "free"),
            subscription_premium_tier_names=data.get("subscription_premium_tier_names", []),
            utm_source=data.get("utm_source"),
            utm_medium=data.get("utm_medium"),
            utm_channel=data.get("utm_channel"),
            utm_campaign=data.get("utm_campaign"),
            utm_term=data.get("utm_term"),
            utm_content=data.get("utm_content"),
            referring_site=data.get("referring_site"),
            referral_code=data.get("referral_code"),
            custom_fields=data.get("custom_fields", []),
            stripe_customer_id=data.get("stripe_customer_id")
        )

    # ==================== Subscription Operations ====================

    async def create_subscription(self, request: SubscriptionCreateRequest) -> Subscription:
        """
        Create a new subscription.

        Args:
            request: SubscriptionCreateRequest with subscription details

        Returns:
            Subscription object with created subscription data

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        url = f"{self.BASE_URL}/publications/{self.publication_id}/subscriptions"

        body = {
            "email": request.email,
            "reactivate_existing": request.reactivate_existing,
            "send_welcome_email": request.send_welcome_email
        }

        # Optional fields
        if request.utm_source:
            body["utm_source"] = request.utm_source
        if request.utm_medium:
            body["utm_medium"] = request.utm_medium
        if request.utm_campaign:
            body["utm_campaign"] = request.utm_campaign
        if request.utm_term:
            body["utm_term"] = request.utm_term
        if request.utm_content:
            body["utm_content"] = request.utm_content
        if request.referring_site:
            body["referring_site"] = request.referring_site
        if request.referral_code:
            body["referral_code"] = request.referral_code
        if request.custom_fields:
            body["custom_fields"] = request.custom_fields
        if request.double_opt_override:
            body["double_opt_override"] = request.double_opt_override
        if request.tier:
            body["tier"] = request.tier
        if request.premium_tiers:
            body["premium_tiers"] = request.premium_tiers
        if request.premium_tier_ids:
            body["premium_tier_ids"] = request.premium_tier_ids
        if request.stripe_customer_id:
            body["stripe_customer_id"] = request.stripe_customer_id
        if request.automation_ids:
            body["automation_ids"] = request.automation_ids

        async with self.session.post(url, headers=self._get_headers(), json=body) as response:
            data = await response.json()

            if response.status == 200 or response.status == 201:
                return self._parse_subscription(data.get("data", {}))
            elif response.status == 400:
                raise Exception(f"Bad Request: {data}")
            elif response.status == 404:
                raise Exception("Publication not found")
            elif response.status == 429:
                raise Exception("Rate limit exceeded")
            elif response.status == 500:
                raise Exception(f"Internal Server Error: {data}")
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    async def get_subscription_by_id(self, subscription_id: str) -> Subscription:
        """
        Retrieve a subscription by ID.

        Args:
            subscription_id: ID of the subscription

        Returns:
            Subscription object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        url = f"{self.BASE_URL}/publications/{self.publication_id}/subscriptions/{subscription_id}"

        async with self.session.get(url, headers=self._get_headers()) as response:
            data = await response.json()

            if response.status == 200:
                return self._parse_subscription(data.get("data", {}))
            elif response.status == 404:
                raise Exception(f"Subscription not found: {subscription_id}")
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    async def get_subscription_by_email(self, email: str) -> Subscription:
        """
        Retrieve a subscription by email.

        Args:
            email: Email address of the subscription

        Returns:
            Subscription object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        url = f"{self.BASE_URL}/publications/{self.publication_id}/subscriptions/get-by-email"
        params = {"email": email}

        async with self.session.get(url, headers=self._get_headers(), params=params) as response:
            data = await response.json()

            if response.status == 200:
                return self._parse_subscription(data.get("data", {}))
            elif response.status == 404:
                raise Exception(f"Subscription not found: {email}")
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    async def list_subscriptions(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List subscriptions for the publication.

        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip
            status: Filter by subscription status (e.g., "active", "subscribed")

        Returns:
            Dictionary with 'data' list and 'results' total count

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        url = f"{self.BASE_URL}/publications/{self.publication_id}/subscriptions"
        params = {}

        if limit:
            params["limit"] = str(limit)
        if offset:
            params["offset"] = str(offset)
        if status:
            params["status"] = status

        async with self.session.get(url, headers=self._get_headers(), params=params) as response:
            data = await response.json()

            if response.status == 200:
                subscriptions = [
                    self._parse_subscription(sub_data)
                    for sub_data in data.get("data", [])
                ]
                return {
                    "data": subscriptions,
                    "results": data.get("results", len(subscriptions))
                }
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    async def list_subscriber_ids(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        List subscriber IDs (lightweight endpoint for getting IDs only).

        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            Dictionary with subscriber IDs and count

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        url = f"{self.BASE_URL}/publications/{self.publication_id}/subscriptions"
        params = {}

        if limit:
            params["limit"] = str(limit)
        if offset:
            params["offset"] = str(offset)
        # Only request minimal fields by not using expand parameters

        async with self.session.get(url, headers=self._get_headers(), params=params) as response:
            data = await response.json()

            if response.status == 200:
                ids = [sub.get("id") for sub in data.get("data", [])]
                return {
                    "data": ids,
                    "results": data.get("results", len(ids))
                }
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    async def update_subscription(
        self,
        subscription_id: str,
        request: SubscriptionUpdateRequest
    ) -> Subscription:
        """
        Update a subscription by ID.

        Args:
            subscription_id: ID of the subscription to update
            request: SubscriptionUpdateRequest with update details

        Returns:
            Updated Subscription object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        url = f"{self.BASE_URL}/publications/{self.publication_id}/subscriptions/{subscription_id}"

        body = {}

        # Add only provided fields
        if request.email is not None:
            body["email"] = request.email
        if request.tier is not None:
            body["tier"] = request.tier
        if request.premium_tiers is not None:
            body["premium_tiers"] = request.premium_tiers
        if request.premium_tier_ids is not None:
            body["premium_tier_ids"] = request.premium_tier_ids
        if request.custom_fields is not None:
            body["custom_fields"] = request.custom_fields
        if request.status is not None:
            body["status"] = request.status

        async with self.session.put(url, headers=self._get_headers(), json=body) as response:
            data = await response.json()

            if response.status == 200:
                return self._parse_subscription(data.get("data", {}))
            elif response.status == 404:
                raise Exception(f"Subscription not found: {subscription_id}")
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    async def update_subscription_by_email(
        self,
        email: str,
        request: SubscriptionUpdateRequest
    ) -> Subscription:
        """
        Update a subscription by email.

        Args:
            email: Email of the subscription to update
            request: SubscriptionUpdateRequest with update details

        Returns:
            Updated Subscription object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        url = f"{self.BASE_URL}/publications/{self.publication_id}/subscriptions/update-by-email"

        body = {"email": email}

        # Add update fields
        if request.tier is not None:
            body["tier"] = request.tier
        if request.premium_tiers is not None:
            body["premium_tiers"] = request.premium_tiers
        if request.premium_tier_ids is not None:
            body["premium_tier_ids"] = request.premium_tier_ids
        if request.custom_fields is not None:
            body["custom_fields"] = request.custom_fields
        if request.status is not None:
            body["status"] = request.status

        async with self.session.put(url, headers=self._get_headers(), json=body) as response:
            data = await response.json()

            if response.status == 200:
                return self._parse_subscription(data.get("data", {}))
            elif response.status == 404:
                raise Exception(f"Subscription not found: {email}")
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    async def delete_subscription(self, subscription_id: str) -> bool:
        """
        Delete a subscription.

        Args:
            subscription_id: ID of the subscription to delete

        Returns:
            True if successful

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        url = f"{self.BASE_URL}/publications/{self.publication_id}/subscriptions/{subscription_id}"

        async with self.session.delete(url, headers=self._get_headers()) as response:
            if response.status == 204:
                return True
            elif response.status == 404:
                raise Exception(f"Subscription not found: {subscription_id}")
            else:
                data = await response.text()
                raise Exception(f"API error (status {response.status}): {data}")

    async def add_tags_to_subscription(
        self,
        subscription_id: str,
        tags: List[str]
    ) -> Dict[str, Any]:
        """
        Add tags to a subscription.

        Args:
            subscription_id: ID of the subscription
            tags: List of tag names to add

        Returns:
            Updated subscription data

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error

        Note:
            This requires the Subscription Tags endpoint
        """
        url = f"{self.BASE_URL}/publications/{self.publication_id}/subscription_tags"

        body = {
            "subscription_id": subscription_id,
            "tags": tags
        }

        async with self.session.post(url, headers=self._get_headers(), json=body) as response:
            data = await response.json()

            if response.status == 200 or response.status == 201:
                return data
            elif response.status == 404:
                raise Exception(f"Subscription or publication not found")
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    # ==================== Post Operations ====================

    async def list_posts(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List posts for the publication.

        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip
            status: Filter by status (e.g., "confirmed", "draft", "scheduled")

        Returns:
            Dictionary with 'data' list and 'results' total count

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        url = f"{self.BASE_URL}/publications/{self.publication_id}/posts"
        params = {}

        if limit:
            params["limit"] = str(limit)
        if offset:
            params["offset"] = str(offset)
        if status:
            params["status"] = status

        async with self.session.get(url, headers=self._get_headers(), params=params) as response:
            data = await response.json()

            if response.status == 200:
                return {
                    "data": data.get("data", []),
                    "results": data.get("results", 0)
                }
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    async def get_post_by_id(self, post_id: str) -> Post:
        """
        Retrieve a single post by ID.

        Args:
            post_id: ID of the post

        Returns:
            Post object

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        url = f"{self.BASE_URL}/publications/{self.publication_id}/posts/{post_id}"

        async with self.session.get(url, headers=self._get_headers()) as response:
            data = await response.json()

            if response.status == 200:
                post_data = data.get("data", {})
                return Post(
                    id=post_data.get("id", ""),
                    title=post_data.get("title", ""),
                    subtitle=post_data.get("subtitle"),
                    status=post_data.get("status", ""),
                    published_date=post_data.get("published_date"),
                    thumbnail_url=post_data.get("thumbnail_url"),
                    slug=post_data.get("slug", ""),
                    content=post_data.get("content"),
                    engagement_score=post_data.get("engagement_score")
                )
            elif response.status == 404:
                raise Exception(f"Post not found: {post_id}")
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    async def search_posts(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Search posts by publication.

        Args:
            query: Search query string
            status: Filter by status
            limit: Maximum number of results

        Returns:
            Dictionary with matching posts

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        url = f"{self.BASE_URL}/publications/{self.publication_id}/posts"
        params = {}

        if query:
            params["query"] = query
        if status:
            params["status"] = status
        if limit:
            params["limit"] = str(limit)

        async with self.session.get(url, headers=self._get_headers(), params=params) as response:
            data = await response.json()

            if response.status == 200:
                return {
                    "data": data.get("data", []),
                    "results": data.get("results", 0)
                }
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    # ==================== Segment Operations ====================

    async def list_segments(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Retrieve segments for the publication.

        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            Dictionary with 'data' list of segments

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        url = f"{self.BASE_URL}/publications/{self.publication_id}/segments"
        params = {}

        if limit:
            params["limit"] = str(limit)
        if offset:
            params["offset"] = str(offset)

        async with self.session.get(url, headers=self._get_headers(), params=params) as response:
            data = await response.json()

            if response.status == 200:
                segments = []
                for seg_data in data.get("data", []):
                    segments.append(Segment(
                        id=seg_data.get("id", ""),
                        name=seg_data.get("name", ""),
                        description=seg_data.get("description"),
                        count=seg_data.get("count", 0),
                        created=int(seg_data.get("created", 0))
                    ))
                return {
                    "data": segments,
                    "results": data.get("results", len(segments))
                }
            else:
                raise Exception(f"API error (status {response.status}): {data}")


# ==================== Example Usage ====================

async def main():
    """Example usage of Beehiiv API client"""

    # Replace with your actual credentials
    api_key = "your_beehiiv_api_key_here"
    publication_id = "pub_your_publication_id_here"

    async with BeehiivAPIClient(api_key=api_key, publication_id=publication_id) as client:
        # Create subscription
        create_request = SubscriptionCreateRequest(
            email="subscriber@example.com",
            send_welcome_email=True,
            utm_source="website",
            utm_medium="organic",
            custom_fields=[
                {"name": "First Name", "value": "John"},
                {"name": "Last Name", "value": "Doe"}
            ]
        )

        try:
            subscription = await client.create_subscription(create_request)
            print(f"Created subscription: {subscription.id}")
            print(f"Email: {subscription.email}")
            print(f"Status: {subscription.status}")
        except Exception as e:
            print(f"Failed to create subscription: {e}")

        # Get subscription by email
        try:
            sub = await client.get_subscription_by_email("subscriber@example.com")
            print(f"Found subscription: {sub.id}")
        except Exception as e:
            print(f"Failed to get subscription: {e}")

        # List subscriptions
        try:
            result = await client.list_subscriptions(limit=10)
            print(f"Total subscriptions: {result['results']}")
            for sub in result["data"][:3]:
                print(f"  - {sub.email}: {sub.status}")
        except Exception as e:
            print(f"Failed to list subscriptions: {e}")

        # List subscriber IDs (lightweight)
        try:
            result = await client.list_subscriber_ids(limit=10)
            print(f"Subscriber IDs: {result['data']}")
        except Exception as e:
            print(f"Failed to list subscriber IDs: {e}")

        # Update subscription
        try:
            update_request = SubscriptionUpdateRequest(tier="premium")
            updated = await client.update_subscription(subscription.id, update_request)
            print(f"Updated subscription tier: {updated.subscription_tier}")
        except Exception as e:
            print(f"Failed to update subscription: {e}")

        # Add tags to subscription
        try:
            result = await client.add_tags_to_subscription(subscription.id, ["VIP", "Early Adopter"])
            print(f"Added tags to subscription")
        except Exception as e:
            print(f"Failed to add tags: {e}")

        # List posts
        try:
            result = await client.list_posts(limit=5)
            print(f"Total posts: {result['results']}")
        except Exception as e:
            print(f"Failed to list posts: {e}")

        # Search posts
        try:
            result = await client.search_posts(query="newsletter", status="confirmed", limit=10)
            print(f"Found {result['results']} matching posts")
        except Exception as e:
            print(f"Failed to search posts: {e}")

        # List segments
        try:
            result = await client.list_segments()
            print(f"Total segments: {result['results']}")
            for seg in result["data"]:
                print(f"  - {seg.name}: {seg.count} subscribers")
        except Exception as e:
            print(f"Failed to list segments: {e}")

        # Delete subscription
        try:
            success = await client.delete_subscription(subscription.id)
            if success:
                print("Subscription deleted successfully")
        except Exception as e:
            print(f"Failed to delete subscription: {e}")


if __name__ == "__main__":
    asyncio.run(main())