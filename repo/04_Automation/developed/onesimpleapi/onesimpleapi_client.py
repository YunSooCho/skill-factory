"""
OneSimpleAPI - Utility API

Supports:
- Expand Short URL
- Get Image EXIF and GPS
- Generate Website Screenshot
- Email Address Validation
- Get Spotify Profile
- Get Exchange Rate
- Get Meta Tag and SEO Data
- Generate QR Code
- Convert Webpage to PDF
- Edit Image
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ExpandedURL:
    """Expanded URL result"""
    original: str
    expanded: str
    title: str


@dataclass
class EmailValidation:
    """Email validation result"""
    email: str
    is_valid: bool
    is_deliverable: bool
    score: float


@dataclass
class ExchangeRate:
    """Exchange rate result"""
    base_currency: str
    target_currency: str
    rate: float
    date: str


@dataclass
class SEOData:
    """SEO data result"""
    url: str
    title: str
    description: str
    keywords: list
    og_tags: Dict[str, str]


class OnesimpleapiClient:
    """
    OneSimpleAPI client for various utility operations.

    API Documentation: https://onesimpleapi.com/api
    Requires an API key from OneSimpleAPI.
    """

    BASE_URL = "https://api.onesimpleapi.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize OneSimpleAPI client.

        Args:
            api_key: OneSimpleAPI key
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def expand_short_url(self, short_url: str) -> ExpandedURL:
        """
        Expand a shortened URL.

        Args:
            short_url: Shortened URL to expand

        Returns:
            ExpandedURL with expanded URL

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "apiKey": self.api_key,
                "url": short_url
            }

            async with self.session.get(
                f"{self.BASE_URL}/expand",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200 or not data.get("success"):
                    raise Exception(f"OneSimpleAPI error: {data.get('error', 'Unknown error')}")

                return ExpandedURL(
                    original=data.get("original", short_url),
                    expanded=data["expanded"],
                    title=data.get("title", "")
                )

        except Exception as e:
            raise Exception(f"Failed to expand URL: {str(e)}")

    async def validate_email(self, email: str) -> EmailValidation:
        """
        Validate an email address.

        Args:
            email: Email to validate

        Returns:
            EmailValidation with validation result

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "apiKey": self.api_key,
                "email": email
            }

            async with self.session.get(
                f"{self.BASE_URL}/email/validate",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200 or not data.get("success"):
                    raise Exception(f"OneSimpleAPI error: {data.get('error', 'Unknown error')}")

                return EmailValidation(
                    email=data["email"],
                    is_valid=data.get("is_valid", False),
                    is_deliverable=data.get("is_deliverable", False),
                    score=data.get("score", 0.0)
                )

        except Exception as e:
            raise Exception(f"Failed to validate email: {str(e)}")

    async def get_exchange_rate(
        self,
        base: str = "USD",
        target: str = "EUR"
    ) -> ExchangeRate:
        """
        Get current exchange rate.

        Args:
            base: Base currency code
            target: Target currency code

        Returns:
            ExchangeRate with rate data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "apiKey": self.api_key,
                "base": base,
                "target": target
            }

            async with self.session.get(
                f"{self.BASE_URL}/exchange",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200 or not data.get("success"):
                    raise Exception(f"OneSimpleAPI error: {data.get('error', 'Unknown error')}")

                return ExchangeRate(
                    base_currency=data["base"],
                    target_currency=data["target"],
                    rate=data["rate"],
                    date=data.get("date", "")
                )

        except Exception as e:
            raise Exception(f"Failed to get exchange rate: {str(e)}")

    async def generate_qr_code(
        self,
        content: str,
        size: int = 200,
        format: str = "png"
    ) -> str:
        """
        Generate a QR code.

        Args:
            content: Content to encode
            size: QR code size in pixels
            format: Output format (png, svg, jpg)

        Returns:
            URL of generated QR code

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "apiKey": self.api_key,
                "content": content,
                "size": size,
                "format": format
            }

            async with self.session.get(
                f"{self.BASE_URL}/qr/generate",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200 or not data.get("success"):
                    raise Exception(f"OneSimpleAPI error: {data.get('error', 'Unknown error')}")

                return data["url"]

        except Exception as e:
            raise Exception(f"Failed to generate QR code: {str(e)}")

    async def generate_screenshot(
        self,
        url: str,
        width: int = 1200,
        height: int = 800
    ) -> str:
        """
        Generate a website screenshot.

        Args:
            url: Website URL
            width: Screenshot width
            height: Screenshot height

        Returns:
            URL of screenshot

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "apiKey": self.api_key,
                "url": url,
                "width": width,
                "height": height
            }

            async with self.session.get(
                f"{self.BASE_URL}/screenshot",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200 or not data.get("success"):
                    raise Exception(f"OneSimpleAPI error: {data.get('error', 'Unknown error')}")

                return data["url"]

        except Exception as e:
            raise Exception(f"Failed to generate screenshot: {str(e)}")

    async def convert_to_pdf(self, url: str) -> str:
        """
        Convert a webpage to PDF.

        Args:
            url: Webpage URL

        Returns:
            URL of generated PDF

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "apiKey": self.api_key,
                "url": url
            }

            async with self.session.get(
                f"{self.BASE_URL}/pdf/generate",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200 or not data.get("success"):
                    raise Exception(f"OneSimpleAPI error: {data.get('error', 'Unknown error')}")

                return data["url"]

        except Exception as e:
            raise Exception(f"Failed to convert to PDF: {str(e)}")

    async def get_seo_data(self, url: str) -> SEOData:
        """
        Get SEO metadata from a webpage.

        Args:
            url: Webpage URL

        Returns:
            SEOData with SEO information

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "apiKey": self.api_key,
                "url": url
            }

            async with self.session.get(
                f"{self.BASE_URL}/seo",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200 or not data.get("success"):
                    raise Exception(f"OneSimpleAPI error: {data.get('error', 'Unknown error')}")

                return SEOData(
                    url=data["url"],
                    title=data.get("title", ""),
                    description=data.get("description", ""),
                    keywords=data.get("keywords", []),
                    og_tags=data.get("og_tags", {})
                )

        except Exception as e:
            raise Exception(f"Failed to get SEO data: {str(e)}")