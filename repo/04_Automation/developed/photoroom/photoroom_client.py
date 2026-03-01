"""
Photoroom - Image Background Removal API

Supports:
- Remove Background
- Set Background
- Change Background Color
- Generate Background
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ProcessedImage:
    """Processed image result"""
    url: str
    width: int
    height: int
    format: str


class PhotoroomClient:
    """
    Photoroom API client for image background processing.

    API Documentation: https://docs.photoroom.com/api
    Requires an API key from Photoroom.
    """

    BASE_URL = "https://sdk.photoroom.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Photoroom client.

        Args:
            api_key: Photoroom API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"X-Photoroom-Api-Key": self.api_key}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def remove_background(
        self,
        image_url: str,
        format: str = "png"
    ) -> ProcessedImage:
        """
        Remove background from an image.

        Args:
            image_url: URL of input image
            format: Output format (png, jpg)

        Returns:
            ProcessedImage with result

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "imageFileUrl": image_url,
                "format": format
            }

            async with self.session.post(
                f"{self.BASE_URL}/remove-background",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Photoroom error: {data.get('error', 'Unknown error')}")

                return ProcessedImage(
                    url=data.get("imageUrl", ""),
                    width=data.get("width", 0),
                    height=data.get("height", 0),
                    format=format
                )

        except Exception as e:
            raise Exception(f"Failed to remove background: {str(e)}")

    async def set_background(
        self,
        image_url: str,
        background_url: str,
        format: str = "png"
    ) -> ProcessedImage:
        """
        Set a new background for an image.

        Args:
            image_url: URL of input image
            background_url: URL of background image
            format: Output format (png, jpg)

        Returns:
            ProcessedImage with result

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "imageFileUrl": image_url,
                "backgroundImageUrl": background_url,
                "format": format
            }

            async with self.session.post(
                f"{self.BASE_URL}/replace-background",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Photoroom error: {data.get('error', 'Unknown error')}")

                return ProcessedImage(
                    url=data.get("imageUrl", ""),
                    width=data.get("width", 0),
                    height=data.get("height", 0),
                    format=format
                )

        except Exception as e:
            raise Exception(f"Failed to set background: {str(e)}")

    async def change_background_color(
        self,
        image_url: str,
        color: str,
        format: str = "png"
    ) -> ProcessedImage:
        """
        Change background color of an image.

        Args:
            image_url: URL of input image
            color: Hex color code (e.g., "#FF0000")
            format: Output format (png, jpg)

        Returns:
            ProcessedImage with result

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "imageFileUrl": image_url,
                "backgroundColor": color,
                "format": format
            }

            async with self.session.post(
                f"{self.BASE_URL}/replace-background-color",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Photoroom error: {data.get('error', 'Unknown error')}")

                return ProcessedImage(
                    url=data.get("imageUrl", ""),
                    width=data.get("width", 0),
                    height=data.get("height", 0),
                    format=format
                )

        except Exception as e:
            raise Exception(f"Failed to change background color: {str(e)}")

    async def generate_background(
        self,
        image_url: str,
        background_type: str = "studio",
        format: str = "png"
    ) -> ProcessedImage:
        """
        Generate a new background using AI.

        Args:
            image_url: URL of input image
            background_type: Type of background (studio, outdoor, abstract)
            format: Output format (png, jpg)

        Returns:
            ProcessedImage with result

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "imageFileUrl": image_url,
                "backgroundType": background_type,
                "format": format
            }

            async with self.session.post(
                f"{self.BASE_URL}/generate-background",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Photoroom error: {data.get('error', 'Unknown error')}")

                return ProcessedImage(
                    url=data.get("imageUrl", ""),
                    width=data.get("width", 0),
                    height=data.get("height", 0),
                    format=format
                )

        except Exception as e:
            raise Exception(f"Failed to generate background: {str(e)}")