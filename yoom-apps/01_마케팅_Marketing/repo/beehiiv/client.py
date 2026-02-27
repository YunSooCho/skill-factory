"""
Beehiiv API Client
"""

import requests
from typing import Optional, Dict, Any, List


class BeehiivAPIError(Exception):
    """Base exception for Beehiiv API errors"""
    pass


class BeehiivAuthError(BeehiivAPIError):
    """Authentication error"""
    pass


class BeehiivRateLimitError(BeehiivAPIError):
    """Rate limit exceeded"""
    pass


class BeehiivClient:
    """Beehiiv API Client for newsletter management"""

    BASE_URL = "https://api.beehiiv.com/v2"

    def __init__(self, api_key: str, publication_id: Optional[str] = None):
        """
        Initialize Beehiiv client

        Args:
            api_key: Your Beehiiv API key
            publication_id: Optional publication ID (needed for some endpoints)
        """
        self.api_key = api_key
        self.publication_id = publication_id
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    # ===== Subscriptions =====

    def create_subscription(
        self,
        email: str,
        publication_id: Optional[str] = None,
        ref_code: Optional[str] = None,
        utm_source: Optional[str] = None,
        utm_medium: Optional[str] = None,
        utm_campaign: Optional[str] = None,
        referral_url: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        send_welcome_email: Optional[bool] = None,
        reactivate_if_exists: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Create a new subscription

        Args:
            email: Subscriber email
            publication_id: Publication ID (defaults to instance publication_id)
            ref_code: Referral code
            utm_source: UTM source
            utm_medium: UTM medium
            utm_campaign: UTM campaign
            referral_url: Referral URL
            custom_fields: Custom field key-value pairs
            send_welcome_email: Whether to send welcome email
            reactivate_if_exists: Whether to reactivate if unsubscribed

        Returns:
            API response data
        """
        endpoint = f"{self.BASE_URL}/publications/{publication_id or self.publication_id}/subscriptions"
        payload = {"email": email}

        if ref_code:
            payload["ref_code"] = ref_code
        if utm_source:
            payload["utm_source"] = utm_source
        if utm_medium:
            payload["utm_medium"] = utm_medium
        if utm_campaign:
            payload["utm_campaign"] = utm_campaign
        if referral_url:
            payload["referral_url"] = referral_url
        if custom_fields:
            payload["custom_fields"] = custom_fields
        if send_welcome_email is not None:
            payload["send_welcome_email"] = send_welcome_email
        if reactivate_if_exists is not None:
            payload["reactivate_if_exists"] = reactivate_if_exists

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def get_subscription(
        self,
        subscription_id: str,
        publication_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a subscription by ID

        Args:
            subscription_id: Subscription ID
            publication_id: Publication ID

        Returns:
            Subscription data
        """
        endpoint = f"{self.BASE_URL}/publications/{publication_id or self.publication_id}/subscriptions/{subscription_id}"

        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def get_subscription_by_email(
        self,
        email: str,
        publication_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a subscription by email

        Args:
            email: Subscriber email
            publication_id: Publication ID

        Returns:
            Subscription data
        """
        endpoint = f"{self.BASE_URL}/publications/{publication_id or self.publication_id}/subscriptions"
        params = {"email": email}

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def update_subscription(
        self,
        subscription_id: str,
        publication_id: Optional[str] = None,
        email: Optional[str] = None,
        subscribed: Optional[bool] = None,
        premium: Optional[bool] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Update a subscription

        Args:
            subscription_id: Subscription ID
            publication_id: Publication ID
            email: New email
            subscribed: Subscription status
            premium: Premium status
            custom_fields: Custom field updates

        Returns:
            Updated subscription data
        """
        endpoint = f"{self.BASE_URL}/publications/{publication_id or self.publication_id}/subscriptions/{subscription_id}"
        payload = {}

        if email:
            payload["email"] = email
        if subscribed is not None:
            payload["subscribed"] = subscribed
        if premium is not None:
            payload["premium"] = premium
        if custom_fields:
            payload["custom_fields"] = custom_fields

        try:
            response = self.session.put(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def delete_subscription(
        self,
        subscription_id: str,
        publication_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Delete a subscription

        Args:
            subscription_id: Subscription ID
            publication_id: Publication ID

        Returns:
            API response data
        """
        endpoint = f"{self.BASE_URL}/publications/{publication_id or self.publication_id}/subscriptions/{subscription_id}"

        try:
            response = self.session.delete(endpoint)
            response.raise_for_status()
            return response.json() if response.content else {"success": True}
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def add_tags_to_subscription(
        self,
        subscription_id: str,
        tags: List[str],
        publication_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Add tags to a subscription

        Args:
            subscription_id: Subscription ID
            tags: List of tags to add
            publication_id: Publication ID

        Returns:
            Updated subscription data
        """
        endpoint = f"{self.BASE_URL}/publications/{publication_id or self.publication_id}/subscriptions/{subscription_id}/tags"
        payload = {"tags": tags}

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def list_subscriber_ids(
        self,
        publication_id: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> List[str]:
        """
        List subscriber IDs

        Args:
            publication_id: Publication ID
            limit: Number of IDs to return
            page: Page number

        Returns:
            List of subscriber IDs
        """
        endpoint = f"{self.BASE_URL}/publications/{publication_id or self.publication_id}/subscriptions"
        params = {"fields": "id"}

        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            return [sub["id"] for sub in data.get("data", data.get("subscriptions", []))]
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    # ===== Posts =====

    def get_post(
        self,
        post_id: str,
        publication_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a single post

        Args:
            post_id: Post ID
            publication_id: Publication ID

        Returns:
            Post data
        """
        endpoint = f"{self.BASE_URL}/publications/{publication_id or self.publication_id}/posts/{post_id}"

        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def search_posts(
        self,
        publication_id: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search posts by publication

        Args:
            publication_id: Publication ID
            limit: Number of posts to return
            page: Page number
            status: Filter by status (draft, published, scheduled)

        Returns:
            List of posts
        """
        endpoint = f"{self.BASE_URL}/publications/{publication_id or self.publication_id}/posts"
        params = {}

        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page
        if status:
            params["status"] = status

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("data", data.get("posts", []))
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    # ===== Segments =====

    def retrieve_segments(
        self,
        publication_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all segments

        Args:
            publication_id: Publication ID

        Returns:
            List of segments
        """
        endpoint = f"{self.BASE_URL}/publications/{publication_id or self.publication_id}/segments"

        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            data = response.json()
            return data.get("data", data.get("segments", []))
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def _handle_error(self, error: requests.exceptions.HTTPError):
        """Handle API errors"""
        if error.response.status_code == 401:
            raise BeehiivAuthError("Invalid API key")
        elif error.response.status_code == 429:
            raise BeehiivRateLimitError("Rate limit exceeded")
        elif error.response.status_code == 400:
            raise BeehiivAPIError(f"Invalid request: {error.response.text}")
        elif error.response.status_code == 403:
            raise BeehiivAPIError("Forbidden - insufficient permissions")
        elif error.response.status_code == 404:
            raise BeehiivAPIError("Resource not found")
        else:
            raise BeehiivAPIError(f"HTTP {error.response.status_code}: {error.response.text}")