"""
Beamer API - User Engagement & Notification Platform Client

Supports:
- Create Post
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class PostTranslation:
    """Post translation data"""
    title: str
    content: str
    language: str
    category: Optional[str] = None
    link_url: Optional[str] = None
    link_text: Optional[str] = None
    images: Optional[List[str]] = None


@dataclass
class Post:
    """Post response from Beamer API"""
    id: str
    date: str
    due_date: Optional[str]
    published: bool
    pinned: bool
    show_in_widget: bool
    show_in_standalone: bool
    category: str
    boosted_announcement: Optional[str]
    translations: List[PostTranslation]
    filter: Optional[str]
    filter_url: Optional[str]
    filter_user_id: Optional[str]
    auto_open: bool
    edition_date: str
    feedback_enabled: bool
    reactions_enabled: bool
    views: int
    unique_views: int
    clicks: int
    feedbacks: int
    positive_reactions: int
    neutral_reactions: int
    negative_reactions: int


@dataclass
class PostCreation:
    """Data for creating a new post"""
    title: List[str]
    content: List[str]
    category: Optional[str] = None
    publish: bool = True
    archive: bool = False
    pinned: bool = False
    show_in_widget: bool = True
    show_in_standalone: bool = True
    boosted_announcement: Optional[str] = None
    link_url: Optional[List[str]] = None
    link_text: Optional[List[str]] = None
    links_in_new_window: bool = True
    date: Optional[str] = None
    due_date: Optional[str] = None
    language: Optional[List[str]] = None
    filter: Optional[str] = None
    filter_user_id: Optional[str] = None
    filter_url: Optional[str] = None
    enable_feedback: bool = True
    enable_reactions: bool = True
    enable_social_share: bool = True
    auto_open: bool = False
    send_push_notification: bool = True
    user_email: Optional[str] = None
    fixed_boosted_announcement: bool = False


class BeamerAPIClient:
    """
    Beamer API client for user engagement and notification platform.

    API Documentation: https://www.getbeamer.com/api
    Authentication: API Key via 'Beamer-Api-Key' header

    Rate Limits:
    - 30 requests per second (paid accounts)
    - Monthly limits: Free=1,000, Starter=2,000, Pro=20,000, Scale=100,000
    """

    BASE_URL = "https://api.getbeamer.com/v0"

    def __init__(self, api_key: str):
        """
        Initialize Beamer API client.

        Args:
            api_key: Your Beamer API key from Settings > API
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with API key authentication"""
        return {
            "Beamer-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def _parse_post(self, data: Dict[str, Any]) -> Post:
        """Parse post data from API response"""
        translations = []
        for t in data.get("translations", []):
            translations.append(PostTranslation(
                title=t.get("title", ""),
                content=t.get("content", ""),
                language=t.get("language", ""),
                category=t.get("category"),
                link_url=t.get("linkUrl"),
                link_text=t.get("linkText"),
                images=t.get("images", [])
            ))

        return Post(
            id=data.get("id", ""),
            date=data.get("date", ""),
            due_date=data.get("dueDate"),
            published=data.get("published") == "true",
            pinned=data.get("pinned") == "true",
            show_in_widget=data.get("showInWidget") == "true",
            show_in_standalone=data.get("showInStandalone") == "true",
            category=data.get("category", ""),
            boosted_announcement=data.get("boostedAnnouncement"),
            translations=translations,
            filter=data.get("filter"),
            filter_url=data.get("filterUrl"),
            filter_user_id=data.get("filterUserId"),
            auto_open=data.get("autoOpen") == "true",
            edition_date=data.get("editionDate", ""),
            feedback_enabled=data.get("feedbackEnabled") == "true",
            reactions_enabled=data.get("reactionsEnabled") == "true",
            views=int(data.get("views", 0)),
            unique_views=int(data.get("uniqueViews", 0)),
            clicks=int(data.get("clicks", 0)),
            feedbacks=int(data.get("feedbacks", 0)),
            positive_reactions=int(data.get("positiveReactions", 0)),
            neutral_reactions=int(data.get("neutralReactions", 0)),
            negative_reactions=int(data.get("negativeReactions", 0))
        )

    async def create_post(self, post_data: PostCreation) -> Post:
        """
        Create a new post.

        Args:
            post_data: PostCreation object with post details

        Returns:
            Post object with created post information

        Raises:
            ValueError: If required fields are missing
            aiohttp.ClientError: If request fails
            Exception: If API returns an error

        Note:
            - All content fields (title, content, language) are arrays to support multiple translations
            - When using multiple translations, keep the same order for all arrays
            - Multiple translations require Starter plan or higher
        """
        if not post_data.title or not post_data.content:
            raise ValueError("title and content are required")

        # Prepare request body
        body = {
            "title": post_data.title,
            "content": post_data.content,
            "publish": post_data.publish,
            "archive": post_data.archive,
            "pinned": post_data.pinned,
            "showInWidget": post_data.show_in_widget,
            "showInStandalone": post_data.show_in_standalone,
            "linksInNewWindow": post_data.links_in_new_window,
            "enableFeedback": post_data.enable_feedback,
            "enableReactions": post_data.enable_reactions,
            "enableSocialShare": post_data.enable_social_share,
            "autoOpen": post_data.auto_open,
            "sendPushNotification": post_data.send_push_notification
        }

        # Optional fields
        if post_data.category:
            body["category"] = post_data.category
        if post_data.boosted_announcement:
            body["boostedAnnouncement"] = post_data.boosted_announcement
        if post_data.link_url:
            body["linkUrl"] = post_data.link_url
        if post_data.link_text:
            body["linkText"] = post_data.link_text
        if post_data.date:
            body["date"] = post_data.date
        if post_data.due_date:
            body["dueDate"] = post_data.due_date
        if post_data.language:
            body["language"] = post_data.language
        if post_data.filter:
            body["filter"] = post_data.filter
        if post_data.filter_user_id:
            body["filterUserId"] = post_data.filter_user_id
        if post_data.filter_url:
            body["filterUrl"] = post_data.filter_url
        if post_data.user_email:
            body["userEmail"] = post_data.user_email
        if post_data.fixed_boosted_announcement:
            body["fixedBoostedAnnouncement"] = post_data.fixed_boosted_announcement

        async with self.session.post(
            f"{self.BASE_URL}/posts",
            headers=self._get_headers(),
            json=body
        ) as response:
            data = await response.json()

            if response.status == 201:
                return self._parse_post(data)
            elif response.status == 401:
                raise Exception("Authentication failed: Invalid API key")
            elif response.status == 403:
                raise Exception("Forbidden: Not allowed to access this resource")
            elif response.status == 429:
                raise Exception("Rate limit exceeded: Monthly API request limit reached")
            elif response.status == 500:
                raise Exception("Internal server error: Something went wrong on Beamer's side")
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    async def get_posts(
        self,
        filter: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        category: Optional[str] = None,
        published: Optional[bool] = None,
        max_results: Optional[int] = None,
        page: Optional[int] = None
    ) -> List[Post]:
        """
        Get existing posts from your account.

        Args:
            filter: Segmentation filter (Pro plan or higher)
            date_from: Date to start from (ISO-8601 format)
            date_to: Date to end at (ISO-8601 format)
            category: Category to filter by
            published: Filter by published status
            max_results: Maximum results (max 10)
            page: Page number for pagination

        Returns:
            List of Post objects

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        params = {}

        if filter:
            params["filter"] = filter
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        if category:
            params["category"] = category
        if published is not None:
            params["published"] = str(published).lower()
        if max_results:
            params["maxResults"] = str(max_results)
        if page:
            params["page"] = str(page)

        async with self.session.get(
            f"{self.BASE_URL}/posts",
            headers=self._get_headers(),
            params=params
        ) as response:
            data = await response.json()

            if response.status == 200:
                return [self._parse_post(post_data) for post_data in data]
            elif response.status == 401:
                raise Exception("Authentication failed: Invalid API key")
            elif response.status == 403:
                raise Exception("Forbidden: Not allowed to access this resource")
            elif response.status == 429:
                raise Exception("Rate limit exceeded: Monthly API request limit reached")
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    async def get_post_by_id(self, post_id: str) -> Post:
        """
        Get a specific post by ID.

        Args:
            post_id: ID of the post to retrieve

        Returns:
            Post object with post details

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        async with self.session.get(
            f"{self.BASE_URL}/posts/{post_id}",
            headers=self._get_headers()
        ) as response:
            data = await response.json()

            if response.status == 200:
                return self._parse_post(data)
            elif response.status == 404:
                raise Exception(f"Post not found: {post_id}")
            elif response.status == 401:
                raise Exception("Authentication failed: Invalid API key")
            elif response.status == 403:
                raise Exception("Forbidden: Not allowed to access this resource")
            elif response.status == 429:
                raise Exception("Rate limit exceeded: Monthly API request limit reached")
            else:
                raise Exception(f"API error (status {response.status}): {data}")

    async def delete_post(self, post_id: str) -> bool:
        """
        Delete a post by ID.

        Args:
            post_id: ID of the post to delete

        Returns:
            True if successful

        Raises:
            aiohttp.ClientError: If request fails
            Exception: If API returns an error
        """
        async with self.session.delete(
            f"{self.BASE_URL}/posts/{post_id}",
            headers=self._get_headers()
        ) as response:
            if response.status == 204:
                return True
            elif response.status == 404:
                raise Exception(f"Post not found: {post_id}")
            elif response.status == 401:
                raise Exception("Authentication failed: Invalid API key")
            elif response.status == 403:
                raise Exception("Forbidden: Not allowed to access this resource")
            elif response.status == 429:
                raise Exception("Rate limit exceeded: Monthly API request limit reached")
            else:
                data = await response.text()
                raise Exception(f"API error (status {response.status}): {data}")

    async def ping(self) -> Dict[str, str]:
        """
        Ping the API to test authentication.

        Returns:
            Dictionary with API status (e.g., {"name": "Your Product Name"})

        Raises:
            Exception: If authentication fails
        """
        async with self.session.post(
            f"{self.BASE_URL}/ping",
            headers=self._get_headers()
        ) as response:
            data = await response.json()

            if response.status == 200:
                return data
            elif response.status == 401:
                raise Exception("Authentication failed: Invalid API key")
            else:
                raise Exception(f"API error (status {response.status}): {data}")


# ==================== Example Usage ====================

async def main():
    """Example usage of Beamer API client"""

    # Replace with your actual API key from https://app.getbeamer.com/settings
    api_key = "your_beamer_api_key_here"

    async with BeamerAPIClient(api_key=api_key) as client:
        # Test connection
        try:
            status = await client.ping()
            print(f"Connected to Beamer product: {status.get('name', 'Unknown')}")
        except Exception as e:
            print(f"Connection failed: {e}")
            return

        # Create a simple post (single language)
        post_data = PostCreation(
            title=["New Feature Announcement"],
            content=["We're excited to announce our new feature!"],
            category="new",
            publish=True,
            language=["EN"]
        )

        try:
            post = await client.create_post(post_data)
            print(f"Created post ID: {post.id}")
            print(f"Published: {post.published}")
            print(f"Category: {post.category}")
        except Exception as e:
            print(f"Failed to create post: {e}")

        # Create post with multiple translations
        post_data_multilang = PostCreation(
            title=["Nouvelle fonctionnalité", "Nueva característica", "New feature"],
            content=[
                "Nous sommes ravis d'annoncer notre nouvelle fonctionnalité!",
                "¡Estamos emocionados de anunciar nuestra nueva característica!",
                "We're excited to announce our new feature!"
            ],
            category="new",
            publish=True,
            language=["FR", "ES", "EN"],
            link_url=["https://example.com/features"],
            link_text=["En savoir plus", "Más información", "Learn more"]
        )

        try:
            post = await client.create_post(post_data_multilang)
            print(f"Created multilingual post ID: {post.id}")
            print(f"Translations: {len(post.translations)}")
        except Exception as e:
            print(f"Failed to create multilingual post: {e}")

        # Get posts
        try:
            posts = await client.get_posts(published=True, max_results=5)
            print(f"Retrieved {len(posts)} published posts")
            for p in posts:
                print(f"  - {p.id}: {post.translations[0].title if post.translations else 'No title'}")
        except Exception as e:
            print(f"Failed to get posts: {e}")


if __name__ == "__main__":
    asyncio.run(main())