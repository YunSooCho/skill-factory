"""
Doppio - PDF and Screenshot Generation API

Supports:
- Create URL from Template
- Create PDF from HTML
- Create PDF from URL
- Create Screenshot from URL
- Create Screenshot from HTML
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class GeneratedPDF:
    """Generated PDF representation"""
    url: str
    size: int
    pages: int


@dataclass
class GeneratedScreenshot:
    """Generated screenshot representation"""
    url: str
    width: int
    height: int


@dataclass
class GeneratedURL:
    """Generated URL from template"""
    url: str
    expires_at: str


class DoppioClient:
    """
    Doppio API client for PDF and screenshot generation.

    API Documentation: https://doppio.sh/docs/api
    Requires an API key from Doppio.
    """

    BASE_URL = "https://api.doppio.sh/v1"

    def __init__(self, api_key: str):
        """
        Initialize Doppio client.

        Args:
            api_key: Doppio API key
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

    async def create_pdf_from_html(
        self,
        html: str,
        filename: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> GeneratedPDF:
        """
        Create a PDF from HTML content.

        Args:
            html: HTML content to convert
            filename: Output filename (optional)
            options: Additional options (format, margin, etc.)

        Returns:
            GeneratedPDF with PDF details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"html": html}

            if filename:
                payload["filename"] = filename

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/pdf/from-html",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Doppio API error: {data.get('error', 'Unknown error')}")

                return GeneratedPDF(
                    url=data["url"],
                    size=data.get("size", 0),
                    pages=data.get("pages", 0)
                )

        except Exception as e:
            raise Exception(f"Failed to create PDF from HTML: {str(e)}")

    async def create_pdf_from_url(
        self,
        url: str,
        filename: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> GeneratedPDF:
        """
        Create a PDF from a URL.

        Args:
            url: URL to convert to PDF
            filename: Output filename (optional)
            options: Additional options (format, margin, etc.)

        Returns:
            GeneratedPDF with PDF details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"url": url}

            if filename:
                payload["filename"] = filename

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/pdf/from-url",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Doppio API error: {data.get('error', 'Unknown error')}")

                return GeneratedPDF(
                    url=data["url"],
                    size=data.get("size", 0),
                    pages=data.get("pages", 0)
                )

        except Exception as e:
            raise Exception(f"Failed to create PDF from URL: {str(e)}")

    async def create_screenshot_from_url(
        self,
        url: str,
        width: int = 1200,
        height: int = 800,
        options: Optional[Dict[str, Any]] = None
    ) -> GeneratedScreenshot:
        """
        Create a screenshot from a URL.

        Args:
            url: URL to screenshot
            width: Screenshot width in pixels
            height: Screenshot height in pixels
            options: Additional options (format, full_page, etc.)

        Returns:
            GeneratedScreenshot with screenshot details

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
                f"{self.BASE_URL}/screenshot/from-url",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Doppio API error: {data.get('error', 'Unknown error')}")

                return GeneratedScreenshot(
                    url=data["url"],
                    width=data.get("width", width),
                    height=data.get("height", height)
                )

        except Exception as e:
            raise Exception(f"Failed to create screenshot from URL: {str(e)}")

    async def create_screenshot_from_html(
        self,
        html: str,
        width: int = 1200,
        height: int = 800,
        options: Optional[Dict[str, Any]] = None
    ) -> GeneratedScreenshot:
        """
        Create a screenshot from HTML content.

        Args:
            html: HTML content to screenshot
            width: Screenshot width in pixels
            height: Screenshot height in pixels
            options: Additional options (format, etc.)

        Returns:
            GeneratedScreenshot with screenshot details

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

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/screenshot/from-html",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Doppio API error: {data.get('error', 'Unknown error')}")

                return GeneratedScreenshot(
                    url=data["url"],
                    width=data.get("width", width),
                    height=data.get("height", height)
                )

        except Exception as e:
            raise Exception(f"Failed to create screenshot from HTML: {str(e)}")

    async def create_url_from_template(
        self,
        template_id: str,
        data: Dict[str, Any],
        expires_in_hours: int = 24
    ) -> GeneratedURL:
        """
        Create a URL from a template.

        Args:
            template_id: Template ID to use
            data: Data to fill in template
            expires_in_hours: URL expiry time in hours

        Returns:
            GeneratedURL with URL details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "template_id": template_id,
                "data": data,
                "expires_in_hours": expires_in_hours
            }

            async with self.session.post(
                f"{self.BASE_URL}/template/url",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Doppio API error: {data.get('error', 'Unknown error')}")

                return GeneratedURL(
                    url=data["url"],
                    expires_at=data["expires_at"]
                )

        except Exception as e:
            raise Exception(f"Failed to create URL from template: {str(e)}")