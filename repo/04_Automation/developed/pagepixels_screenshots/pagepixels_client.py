"""
PagePixels Screenshots - Website Screenshot API

Supports:
- Capture Screenshot
- Capture Screenshot from HTML
- Capture Configured Screenshot
- Real Location Screenshot
- Schedule Screenshot
- AI Analysis Screenshot
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Screenshot:
    """Screenshot representation"""
    id: str
    url: str
    screenshot_url: str
    width: int
    height: int
    status: str
    created_at: str


@dataclass
class ScheduledScreenshot:
    """Scheduled screenshot representation"""
    id: str
    url: str
    schedule: str
    status: str
    next_run: str


class PagePixelsClient:
    """
    PagePixels API client for website screenshots.

    API Documentation: https://api.pagepixels.com
    Requires an API key from PagePixels.
    """

    BASE_URL = "https://api.pagepixels.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize PagePixels client.

        Args:
            api_key: PagePixels API key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def capture_screenshot(
        self,
        url: str,
        width: int = 1920,
        height: int = 1080,
        options: Optional[Dict[str, Any]] = None
    ) -> Screenshot:
        """
        Capture a screenshot of a URL.

        Args:
            url: URL to capture
            width: Screenshot width
            height: Screenshot height
            options: Additional options (full_page, format, etc.)

        Returns:
            Screenshot with screenshot data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "url": url,
                "width": width,
                "height": height
            }

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/screenshots",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"PagePixels error: {data.get('error', 'Unknown error')}")

                return Screenshot(
                    id=data["id"],
                    url=data["url"],
                    screenshot_url=data["screenshot_url"],
                    width=data.get("width", width),
                    height=data.get("height", height),
                    status=data["status"],
                    created_at=data["created_at"]
                )

        except Exception as e:
            raise Exception(f"Failed to capture screenshot: {str(e)}")

    async def capture_screenshot_from_html(
        self,
        html: str,
        width: int = 1920,
        height: int = 1080,
        format: str = "png"
    ) -> Screenshot:
        """
        Capture a screenshot from HTML content.

        Args:
            html: HTML content to render
            width: Screenshot width
            height: Screenshot height
            format: Output format (png, jpg, webp)

        Returns:
            Screenshot with screenshot data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "html": html,
                "width": width,
                "height": height,
                "format": format
            }

            async with self.session.post(
                f"{self.BASE_URL}/screenshots/html",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"PagePixels error: {data.get('error', 'Unknown error')}")

                return Screenshot(
                    id=data["id"],
                    url="",
                    screenshot_url=data["screenshot_url"],
                    width=data.get("width", width),
                    height=data.get("height", height),
                    status=data["status"],
                    created_at=data["created_at"]
                )

        except Exception as e:
            raise Exception(f"Failed to capture screenshot from HTML: {str(e)}")

    async def capture_configured_screenshot(
        self,
        config_id: str,
        url: Optional[str] = None
    ) -> Screenshot:
        """
        Capture screenshot using a pre-configured template.

        Args:
            config_id: Configuration ID
            url: Optional URL override

        Returns:
            Screenshot with screenshot data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"config_id": config_id}

            if url:
                payload["url"] = url

            async with self.session.post(
                f"{self.BASE_URL}/screenshots/configured",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"PagePixels error: {data.get('error', 'Unknown error')}")

                return Screenshot(
                    id=data["id"],
                    url=data.get("url", ""),
                    screenshot_url=data["screenshot_url"],
                    width=data.get("width", 0),
                    height=data.get("height", 0),
                    status=data["status"],
                    created_at=data["created_at"]
                )

        except Exception as e:
            raise Exception(f"Failed to capture configured screenshot: {str(e)}")

    async def real_location_screenshot(
        self,
        url: str,
        location: str,
        width: int = 1920,
        height: int = 1080
    ) -> Screenshot:
        """
        Capture screenshot from specific geographic location.

        Args:
            url: URL to capture
            location: Location code (e.g., us-east, eu-west)
            width: Screenshot width
            height: Screenshot height

        Returns:
            Screenshot with screenshot data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "url": url,
                "location": location,
                "width": width,
                "height": height
            }

            async with self.session.post(
                f"{self.BASE_URL}/screenshots/real-location",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"PagePixels error: {data.get('error', 'Unknown error')}")

                return Screenshot(
                    id=data["id"],
                    url=data["url"],
                    screenshot_url=data["screenshot_url"],
                    width=data.get("width", width),
                    height=data.get("height", height),
                    status=data["status"],
                    created_at=data["created_at"]
                )

        except Exception as e:
            raise Exception(f"Failed to capture real location screenshot: {str(e)}")

    async def schedule_screenshot(
        self,
        url: str,
        schedule: str,
        options: Optional[Dict[str, Any]] = None
    ) -> ScheduledScreenshot:
        """
        Schedule recurring screenshots.

        Args:
            url: URL to capture
            schedule: Cron schedule expression
            options: Additional options

        Returns:
            ScheduledScreenshot with schedule details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "url": url,
                "schedule": schedule
            }

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/screenshots/schedules",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"PagePixels error: {data.get('error', 'Unknown error')}")

                return ScheduledScreenshot(
                    id=data["id"],
                    url=data["url"],
                    schedule=data["schedule"],
                    status=data["status"],
                    next_run=data["next_run"]
                )

        except Exception as e:
            raise Exception(f"Failed to schedule screenshot: {str(e)}")

    async def ai_analysis_screenshot(
        self,
        url: str,
        analysis_type: str = "summary"
    ) -> Dict[str, Any]:
        """
        Capture screenshot and analyze with AI.

        Args:
            url: URL to capture and analyze
            analysis_type: Type of analysis (summary, seo, usability)

        Returns:
            Analysis result with screenshot and AI insights

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "url": url,
                "analysis_type": analysis_type
            }

            async with self.session.post(
                f"{self.BASE_URL}/screenshots/ai-analyze",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"PagePixels error: {data.get('error', 'Unknown error')}")

                return data

        except Exception as e:
            raise Exception(f"Failed to create AI analysis screenshot: {str(e)}")