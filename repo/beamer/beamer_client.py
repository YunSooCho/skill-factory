"""
Beamer API Client

Supports:
- Create Post (Create announcement/changelog post)
"""

import aiohttp
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class Post:
    """Beamer post representation"""
    id: Optional[str] = None
    title: str = ""
    content: str = ""
    category: str = "announcement"
    publish: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    url: Optional[str] = None


@dataclass
class CreatePostResponse:
    """Create post response"""
    post_id: Optional[str] = None
    success: bool = False
    message: str = ""
    url: Optional[str] = None


class BeamerClient:
    """
    Beamer API client for product update and changelog posts.

    API Documentation: https://www.getbeamer.com/api
    Authentication: API Key (Header: Authorization: Bearer {key})
    """

    BASE_URL = "https://www.getbeamer.com/api"

    def __init__(self, api_key: str):
        """
        Initialize Beamer client.

        Args:
            api_key: Beamer API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    # ==================== Post Operations ====================

    async def create_post(
        self,
        title: str,
        content: str,
        category: str = "announcement",
        publish: bool = False,
        html: Optional[str] = None,
        author_name: Optional[str] = None,
        author_email: Optional[str] = None,
        image_url: Optional[str] = None,
        external_url: Optional[str] = None
    ) -> CreatePostResponse:
        """
        Create a new post in Beamer.

        Args:
            title: Post title
            content: Post content (plain text or HTML)
            category: Post category (announcement, new, improvement, fix, comingsoon)
            publish: Whether to publish immediately (default: false)
            html: HTML content (optional, overrides content)
            author_name: Author name (optional)
            author_email: Author email (optional)
            image_url: Featured image URL (optional)
            external_url: External link URL (optional)

        Returns:
            CreatePostResponse with post ID and status

        Raises:
            Exception: If API request fails

        Example:
            response = await client.create_post(
                title="New Feature Released",
                content="We've added...",
                category="new",
                publish=True
            )
        """
        payload: Dict[str, Any] = {
            "title": title,
            "content": content,
            "category": category,
            "publish": publish
        }

        # Optional fields
        if html is not None:
            payload["html"] = html
        if author_name is not None:
            payload["authorName"] = author_name
        if author_email is not None:
            payload["authorEmail"] = author_email
        if image_url is not None:
            payload["image"] = image_url
        if external_url is not None:
            payload["externalUrl"] = external_url

        async with self.session.post(f"{self.BASE_URL}/posts", json=payload) as response:
            data = await response.json()

            if response.status not in (200, 201):
                raise Exception(f"Failed to create post: {data}")

            return CreatePostResponse(
                post_id=data.get("id"),
                success=True,
                message="Post created successfully",
                url=data.get("url")
            )


async def main():
    """Example usage"""
    api_key = "your_beamer_api_key"

    async with BeamerClient(api_key=api_key) as client:
        response = await client.create_post(
            title="New Feature Released",
            content="<p>We've added exciting new features to our platform!</p>",
            category="new",
            publish=True,
            html="<p>We've added exciting new features to our platform!</p>"
        )
        print(f"Post ID: {response.post_id}")
        print(f"Success: {response.success}")
        print(f"URL: {response.url}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())