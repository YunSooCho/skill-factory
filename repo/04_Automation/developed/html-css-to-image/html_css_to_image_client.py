"""
HTML-CSS-to-Image - HTML to Image Generation API

Supports:
- Create Image
- Get Image
- Delete Image
- Get Account Usage
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class GeneratedImage:
    """Generated image representation"""
    id: str
    url: str
    width: int
    height: int


@dataclass
class AccountUsage:
    """Account usage statistics"""
    images_generated: int
    credits_remaining: int
    credits_used: int


class HtmlCssToImageClient:
    """
    HTML-CSS-to-Image API client for converting HTML/CSS to images.

    API Documentation: https://docs.htmlcsstoimage.com
    Requires an API key from HTML-CSS-to-Image.
    """

    BASE_URL = "https://hcti.io/v1"

    def __init__(self, user_id: str, api_key: str):
        """
        Initialize HTML-CSS-to-Image client.

        Args:
            user_id: Your user ID
            api_key: API key
        """
        self.user_id = user_id
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Basic {self._get_auth()}"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_auth(self) -> str:
        """Get basic auth string"""
        import base64
        credentials = f"{self.user_id}:{self.api_key}"
        return base64.b64encode(credentials.encode()).decode()

    async def create_image(
        self,
        html: str,
        css: Optional[str] = None,
        width: int = 800,
        height: int = 600
    ) -> GeneratedImage:
        """
        Create an image from HTML/CSS.

        Args:
            html: HTML content
            css: Optional CSS content
            width: Image width
            height: Image height

        Returns:
            GeneratedImage with image URL

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "html": html,
                "width": width,
                "height": height
            }

            if css:
                payload["css"] = css

            async with self.session.post(
                f"{self.BASE_URL}/image",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"HTML-CSS-to-Image error: {data.get('error', 'Unknown error')}")

                return GeneratedImage(
                    id=data.get("id", ""),
                    url=data["url"],
                    width=data.get("width", width),
                    height=data.get("height", height)
                )

        except Exception as e:
            raise Exception(f"Failed to create image: {str(e)}")

    async def get_image(self, image_id: str) -> GeneratedImage:
        """
        Get details of a generated image.

        Args:
            image_id: Image ID

        Returns:
            GeneratedImage with image details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/image/{image_id}"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"HTML-CSS-to-Image error: {data.get('error', 'Unknown error')}")

                return GeneratedImage(
                    id=data["id"],
                    url=data["url"],
                    width=data.get("width", 0),
                    height=data.get("height", 0)
                )

        except Exception as e:
            raise Exception(f"Failed to get image: {str(e)}")

    async def delete_image(self, image_id: str) -> bool:
        """
        Delete a generated image.

        Args:
            image_id: Image ID

        Returns:
            True if successful

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.delete(
                f"{self.BASE_URL}/image/{image_id}"
            ) as response:
                if response.status != 204:
                    data = await response.json()
                    raise Exception(f"HTML-CSS-to-Image error: {data.get('error', 'Unknown error')}")

                return True

        except Exception as e:
            raise Exception(f"Failed to delete image: {str(e)}")

    async def get_account_usage(self) -> AccountUsage:
        """
        Get account usage statistics.

        Returns:
            AccountUsage with usage data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/usage"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"HTML-CSS-to-Image error: {data.get('error', 'Unknown error')}")

                return AccountUsage(
                    images_generated=data.get("images_generated", 0),
                    credits_remaining=data.get("credits_remaining", 0),
                    credits_used=data.get("credits_used", 0)
                )

        except Exception as e:
            raise Exception(f"Failed to get account usage: {str(e)}")