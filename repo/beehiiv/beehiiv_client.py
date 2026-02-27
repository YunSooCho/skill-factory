"""
Beehiiv API Client

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

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import time


@dataclass
class Subscription:
    """Beehiiv subscription representation"""
    id: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None
    created: Optional[int] = None
    subscription_tier: Optional[str] = None
    premium_tiers: List[str] = None
    custom_fields: List[Dict[str, Any]] = None
    tags: List[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    referral_code: Optional[str] = None

    def __post_init__(self):
        if self.premium_tiers is None:
            self.premium_tiers = []
        if self.custom_fields is None:
            self.custom_fields = []
        if self.tags is None:
            self.tags = []


@dataclass
class Post:
    """Beehiiv post representation"""
    id: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    published: Optional[int] = None
    created: Optional[int] = None
    thumbnail_url: Optional[str] = None


@dataclass
class Segment:
    """Beehiiv segment representation"""
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    subscriber_count: Optional[int] = None


class BeehiivClient:
    """
    Beehiiv API client for newsletter and subscription management.

    API Documentation: https://developers.beehiiv.com
    Authentication: API Key (Header: Authorization: Bearer {key})
    Base URL: https://api.beehiiv.com/v2
    """

    BASE_URL = "https://api.beehiiv.com/v2"

    def __init__(self, api_key: str, publication_id: str):
        """
        Initialize Beehiiv client.

        Args:
            api_key: Beehiiv API key
            publication_id: Publication ID (format: pub_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
        """
        self.api_key = api_key
        self.publication_id = publication_id
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        self.last_rate_limit_reset = 0
        self.remaining_requests = 1000

    def _handle_rate_limits(self, response: requests.Response) -> None:
        """Handle rate limiting from response headers"""
        self.remaining_requests = int(response.headers.get("X-RateLimit-Remaining", self.remaining_requests))
        limit = int(response.headers.get("X-RateLimit-Limit", 1000))

        if self.remaining_requests < 10:
            reset_time = int(response.headers.get("X-RateLimit-Reset", time.time()))
            sleep_time = max(reset_time - time.time(), 1)
            if sleep_time > 0:
                time.sleep(sleep_time)

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a request to Beehiiv API with error handling and retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            **kwargs: Additional arguments for requests

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails after retries
        """
        max_retries = 3
        base_url = kwargs.pop('base_url', self.BASE_URL)

        for attempt in range(max_retries):
            url = f"{base_url}{endpoint}"

            try:
                response = self.session.request(method, url, **kwargs)

                self._handle_rate_limits(response)

                if response.status_code in (200, 201, 204):
                    if response.status_code == 204:
                        return {}
                    data = response.json()
                    return data.get('data', data)
                elif response.status_code == 429:
                    # Rate limit exceeded, wait and retry
                    retry_after = int(response.headers.get("Retry-After", 2))
                    time.sleep(retry_after)
                    continue
                elif response.status_code == 401:
                    raise Exception(f"Authentication failed: Invalid API key")
                elif response.status_code == 404:
                    raise Exception(f"Resource not found: {endpoint}")
                elif response.status_code >= 500:
                    # Server error, retry
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    else:
                        raise Exception(f"Server error: {response.status_code}")
                else:
                    error_data = response.json() if response.content else {}
                    raise Exception(f"API error {response.status_code}: {error_data}")

            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    raise Exception(f"Request failed: {str(e)}")

        raise Exception("Request failed after maximum retries")

    # ==================== Subscription Operations ====================

    def create_subscription(
        self,
        email: str,
        reactivate_existing: bool = False,
        send_welcome_email: bool = False,
        custom_fields: Optional[List[Dict[str, Any]]] = None,
        utm_source: Optional[str] = None,
        utm_medium: Optional[str] = None,
        utm_campaign: Optional[str] = None,
        utm_term: Optional[str] = None,
        utm_content: Optional[str] = None,
        referring_site: Optional[str] = None,
        referral_code: Optional[str] = None,
        tier: Optional[str] = None,
        premium_tiers: Optional[List[str]] = None,
        premium_tier_ids: Optional[List[str]] = None,
        stripe_customer_id: Optional[str] = None,
        double_opt_override: Optional[str] = None,
        automation_ids: Optional[List[str]] = None
    ) -> Subscription:
        """
        Create a new subscription for the publication.

        Args:
            email: Email address of the subscriber
            reactivate_existing: Reactivate if previously unsubscribed
            send_welcome_email: Send welcome email to new subscriber
            custom_fields: List of custom fields [{"name": "field_name", "value": "field_value"}]
            utm_source: UTM source parameter
            utm_medium: UTM medium parameter
            utm_campaign: UTM campaign parameter
            utm_term: UTM term parameter
            utm_content: UTM content parameter
            referring_site: Referring website
            referral_code: Referral code for credit
            tier: Subscription tier ("free" or "premium")
            premium_tiers: List of premium tier names
            premium_tier_ids: List of premium tier IDs
            stripe_customer_id: Stripe customer ID
            double_opt_override: Override double opt-in ("on", "off", "not_set")
            automation_ids: List of automation IDs to enroll subscriber

        Returns:
            Subscription object

        Raises:
            Exception: If API request fails
        """
        if not email:
            raise ValueError("Email is required")

        payload: Dict[str, Any] = {
            "email": email,
            "reactivate_existing": reactivate_existing,
            "send_welcome_email": send_welcome_email
        }

        # Add optional fields
        optional_params = {
            "custom_fields": custom_fields,
            "utm_source": utm_source,
            "utm_medium": utm_medium,
            "utm_campaign": utm_campaign,
            "utm_term": utm_term,
            "utm_content": utm_content,
            "referring_site": referring_site,
            "referral_code": referral_code,
            "tier": tier,
            "premium_tiers": premium_tiers,
            "premium_tier_ids": premium_tier_ids,
            "stripe_customer_id": stripe_customer_id,
            "double_opt_override": double_opt_override,
            "automation_ids": automation_ids
        }

        for key, value in optional_params.items():
            if value is not None:
                payload[key] = value

        data = self._request(
            "POST",
            f"/publications/{self.publication_id}/subscriptions",
            json=payload
        )

        return self._parse_subscription(data)

    def get_subscription_by_id(self, subscription_id: str) -> Subscription:
        """
        Retrieve a subscription by its ID.

        Args:
            subscription_id: Subscription ID

        Returns:
            Subscription object
        """
        data = self._request(
            "GET",
            f"/publications/{self.publication_id}/subscriptions/{subscription_id}"
        )

        return self._parse_subscription(data)

    def get_subscription_by_email(self, email: str) -> Subscription:
        """
        Retrieve a subscription by email address.

        Args:
            email: Email address

        Returns:
            Subscription object
        """
        if not email:
            raise ValueError("Email is required")

        data = self._request(
            "GET",
            f"/publications/{self.publication_id}/subscriptions/email/{email}"
        )

        return self._parse_subscription(data)

    def update_subscription(
        self,
        subscription_id: str,
        update_payload: Dict[str, Any]
    ) -> Subscription:
        """
        Update a subscription by ID.

        Args:
            subscription_id: Subscription ID
            update_payload: Dictionary of fields to update
                Can include: tier, premium_tiers, premium_tier_ids, custom_fields, etc.

        Returns:
            Updated Subscription object
        """
        data = self._request(
            "PUT",
            f"/publications/{self.publication_id}/subscriptions/{subscription_id}",
            json=update_payload
        )

        return self._parse_subscription(data)

    def delete_subscription(self, subscription_id: str) -> None:
        """
        Delete a subscription.

        Args:
            subscription_id: Subscription ID
        """
        self._request(
            "DELETE",
            f"/publications/{self.publication_id}/subscriptions/{subscription_id}"
        )

    def add_tags_to_subscription(
        self,
        subscription_id: str,
        tags: List[str]
    ) -> Subscription:
        """
        Add tags to a subscription.

        Args:
            subscription_id: Subscription ID
            tags: List of tag names to add

        Returns:
            Updated Subscription object
        """
        if not tags:
            raise ValueError("At least one tag is required")

        # Get current subscription
        current = self.get_subscription_by_id(subscription_id)
        current_tags = current.tags or []

        # Merge tags without duplicates
        merged_tags = list(set(current_tags + tags))

        # Update subscription with merged tags
        return self.update_subscription(subscription_id, {"tags": merged_tags})

    def list_subscriber_ids(
        self,
        limit: int = 100,
        offset: int = 0,
        status: Optional[str] = None
    ) -> List[str]:
        """
        List all subscriber IDs for the publication.

        Args:
            limit: Number of results to return (max 1000)
            offset: Number of results to skip
            status: Filter by status ("active", "pending", etc.)

        Returns:
            List of subscription IDs
        """
        params = {"limit": min(limit, 1000), "offset": offset}

        if status:
            params["status"] = status

        data = self._request(
            "GET",
            f"/publications/{self.publication_id}/subscriptions",
            params=params
        )

        # Extract subscription IDs from data
        if isinstance(data, list):
            return [sub.get("id") for sub in data if sub.get("id")]
        elif isinstance(data, dict) and "data" in data:
            return [sub.get("id") for sub in data["data"] if sub.get("id")]

        return []

    # ==================== Post Operations ====================

    def get_post(self, post_id: str) -> Post:
        """
        Retrieve a single post by ID.

        Args:
            post_id: Post ID

        Returns:
            Post object
        """
        data = self._request(
            "GET",
            f"/publications/{self.publication_id}/posts/{post_id}"
        )

        return self._parse_post(data)

    def search_posts(
        self,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None
    ) -> List[Post]:
        """
        Search for posts in the publication.

        Args:
            limit: Number of results to return (max 100)
            offset: Number of results to skip
            status: Filter by status ("draft", "scheduled", "sent", etc.)

        Returns:
            List of Post objects
        """
        params = {"limit": min(limit, 100), "offset": offset}

        if status:
            params["status"] = status

        data = self._request(
            "GET",
            f"/publications/{self.publication_id}/posts",
            params=params
        )

        posts = []
        if isinstance(data, list):
            for post_data in data:
                posts.append(self._parse_post(post_data))
        elif isinstance(data, dict) and "data" in data:
            for post_data in data["data"]:
                posts.append(self._parse_post(post_data))

        return posts

    # ==================== Segment Operations ====================

    def get_segments(self) -> List[Segment]:
        """
        Retrieve all segments for the publication.

        Returns:
            List of Segment objects
        """
        data = self._request(
            "GET",
            f"/publications/{self.publication_id}/segments"
        )

        segments = []
        if isinstance(data, list):
            for segment_data in data:
                segments.append(self._parse_segment(segment_data))
        elif isinstance(data, dict) and "data" in data:
            for segment_data in data["data"]:
                segments.append(self._parse_segment(segment_data))

        return segments

    # ==================== Webhook Operations ====================

    def verify_webhook(self, signature: str, payload: bytes, webhook_secret: str) -> bool:
        """
        Verify a webhook signature.

        Args:
            signature: Signature from X-Signature header
            payload: Raw webhook payload bytes
            webhook_secret: Your webhook secret

        Returns:
            True if signature is valid
        """
        import hmac
        import hashlib

        expected_signature = hmac.new(
            webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    # ==================== Helper Methods ====================

    def _parse_subscription(self, data: Dict[str, Any]) -> Subscription:
        """Parse subscription data from API response"""
        return Subscription(
            id=data.get("id"),
            email=data.get("email"),
            status=data.get("status"),
            created=data.get("created"),
            subscription_tier=data.get("subscription_tier"),
            premium_tiers=data.get("subscription_premium_tier_names", []),
            custom_fields=data.get("custom_fields", []),
            tags=data.get("tags", []),
            utm_source=data.get("utm_source"),
            utm_medium=data.get("utm_medium"),
            utm_campaign=data.get("utm_campaign"),
            referral_code=data.get("referral_code")
        )

    def _parse_post(self, data: Dict[str, Any]) -> Post:
        """Parse post data from API response"""
        return Post(
            id=data.get("id"),
            title=data.get("title"),
            subtitle=data.get("subtitle"),
            content=data.get("content"),
            status=data.get("status"),
            published=data.get("published"),
            created=data.get("created"),
            thumbnail_url=data.get("thumbnail_url")
        )

    def _parse_segment(self, data: Dict[str, Any]) -> Segment:
        """Parse segment data from API response"""
        return Segment(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            subscriber_count=data.get("subscriber_count")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_beehiiv_api_key"
    publication_id = "pub_00000000-0000-0000-0000-000000000000"

    client = BeehiivClient(api_key=api_key, publication_id=publication_id)

    try:
        # Create a subscription
        subscription = client.create_subscription(
            email="test@example.com",
            custom_fields=[
                {"name": "First Name", "value": "John"},
                {"name": "Last Name", "value": "Doe"}
            ],
            utm_source="website",
            utm_medium="form",
            send_welcome_email=True
        )
        print(f"Created subscription: {subscription.id} - {subscription.email}")

        # Get subscription by ID
        fetched = client.get_subscription_by_id(subscription.id)
        print(f"Fetched subscription: {fetched.email} - Status: {fetched.status}")

        # Add tags
        tagged = client.add_tags_to_subscription(subscription.id, ["VIP", "Early Adopter"])
        print(f"Tags after adding: {tagged.tags}")

        # Search posts
        posts = client.search_posts(limit=10)
        print(f"Found {len(posts)} posts")

        # Get segments
        segments = client.get_segments()
        print(f"Found {len(segments)} segments")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()