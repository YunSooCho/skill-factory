"""
Diffbot - Web Page and Article Extraction API

Supports:
- Extract Article
- Extract Main Image
- Extract Discussion
- Analyze Web Page
- Extract Product Data
- Extract Video Information
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class ArticleExtraction:
    """Article extraction response"""
    title: str
    author: str
    html: str
    text: str
    date: str
    images: List[str]
    tags: List[str]
    sentiment: float
    url: str


@dataclass
class MainImage:
    """Main image extraction response"""
    url: str
    caption: str
    height: int
    width: int


@dataclass
class Discussion:
    """Discussion extraction response"""
    title: str
    posts: List[Dict[str, Any]]
    url: str


@dataclass
class WebPageAnalysis:
    """Web page analysis response"""
    title: str
    type: str
    lang: str
    author: str
    estimatedDate: str
    objects: List[Dict[str, Any]]
    url: str


@dataclass
class ProductData:
    """Product data extraction response"""
    title: str
    description: str
    price: float
    currency: str
    availability: str
    images: List[str]
    url: str


@dataclass
class VideoInfo:
    """Video information extraction response"""
    title: str
    description: str
    duration: int
    url: str
    thumbnail: str
    embedUrl: str


class DiffbotClient:
    """
    Diffbot API client for web page and content extraction.

    API Documentation: https://www.diffbot.com/dev/docs/
    Requires an API token from Diffbot.
    """

    BASE_URL = "https://api.diffbot.com/v3"

    def __init__(self, api_token: str):
        """
        Initialize Diffbot client.

        Args:
            api_token: Diffbot API token
        """
        self.api_token = api_token
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_url(self, endpoint: str) -> str:
        """Get full URL for endpoint"""
        return f"{self.BASE_URL}/{endpoint}"

    # ==================== Article Extraction ====================

    async def extract_article(
        self,
        url: str,
        timeout: int = 30
    ) -> ArticleExtraction:
        """
        Extract article content from a web page.

        Args:
            url: Web page URL to extract article from
            timeout: Request timeout in seconds

        Returns:
            ArticleExtraction with article data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "token": self.api_token,
                "url": url,
                "timeout": timeout
            }

            async with self.session.get(
                self._get_url("article"),
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200 or "error" in data:
                    raise Exception(f"Diffbot API error: {data.get('error', 'Unknown error')}")

                obj = data.get("objects", [{}])[0]

                return ArticleExtraction(
                    title=obj.get("title", ""),
                    author=obj.get("author", ""),
                    html=obj.get("html", ""),
                    text=obj.get("text", ""),
                    date=obj.get("date", ""),
                    images=[img.get("url", "") for img in obj.get("images", [])],
                    tags=obj.get("tags", []),
                    sentiment=obj.get("sentiment", 0.0),
                    url=obj.get("pageUrl", url)
                )

        except Exception as e:
            raise Exception(f"Failed to extract article: {str(e)}")

    # ==================== Main Image ====================

    async def extract_main_image(
        self,
        url: str,
        max_size: Optional[int] = None
    ) -> MainImage:
        """
        Extract main image from a web page.

        Args:
            url: Web page URL
            max_size: Maximum image size in bytes (optional)

        Returns:
            MainImage with image data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "token": self.api_token,
                "url": url
            }

            if max_size:
                params["maxSize"] = max_size

            async with self.session.get(
                self._get_url("image"),
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200 or "error" in data:
                    raise Exception(f"Diffbot API error: {data.get('error', 'Unknown error')}")

                obj = data.get("objects", [{}])[0]

                return MainImage(
                    url=obj.get("url", ""),
                    caption=obj.get("caption", ""),
                    height=obj.get("height", 0),
                    width=obj.get("width", 0)
                )

        except Exception as e:
            raise Exception(f"Failed to extract main image: {str(e)}")

    # ==================== Discussion Extraction ====================

    async def extract_discussion(
        self,
        url: str,
        count: int = 10
    ) -> Discussion:
        """
        Extract discussion forum content.

        Args:
            url: Discussion forum URL
            count: Number of posts to retrieve

        Returns:
            Discussion with forum data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "token": self.api_token,
                "url": url,
                "count": count
            }

            async with self.session.get(
                self._get_url("discussion"),
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200 or "error" in data:
                    raise Exception(f"Diffbot API error: {data.get('error', 'Unknown error')}")

                obj = data.get("objects", [{}])[0]

                return Discussion(
                    title=obj.get("title", ""),
                    posts=obj.get("posts", []),
                    url=obj.get("pageUrl", url)
                )

        except Exception as e:
            raise Exception(f"Failed to extract discussion: {str(e)}")

    # ==================== Web Page Analysis ====================

    async def analyze_web_page(
        self,
        url: str,
        mode: str = "auto"
    ) -> WebPageAnalysis:
        """
        Analyze a web page and extract structured data.

        Args:
            url: Web page URL
            mode: Analysis mode (auto, article, product, image, etc.)

        Returns:
            WebPageAnalysis with page data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "token": self.api_token,
                "url": url,
                "mode": mode
            }

            async with self.session.get(
                self._get_url("analyze"),
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200 or "error" in data:
                    raise Exception(f"Diffbot API error: {data.get('error', 'Unknown error')}")

                obj = data.get("objects", [{}])[0]

                return WebPageAnalysis(
                    title=obj.get("title", ""),
                    type=obj.get("type", ""),
                    lang=obj.get("lang", ""),
                    author=obj.get("author", ""),
                    estimatedDate=obj.get("estimatedDate", ""),
                    objects=obj.get("objects", []),
                    url=obj.get("pageUrl", url)
                )

        except Exception as e:
            raise Exception(f"Failed to analyze web page: {str(e)}")

    # ==================== Product Data ====================

    async def extract_product_data(
        self,
        url: str,
        language: str = "en"
    ) -> ProductData:
        """
        Extract product data from an e-commerce page.

        Args:
            url: Product page URL
            language: Language code (default: en)

        Returns:
            ProductData with product information

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "token": self.api_token,
                "url": url,
                "language": language
            }

            async with self.session.get(
                self._get_url("product"),
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200 or "error" in data:
                    raise Exception(f"Diffbot API error: {data.get('error', 'Unknown error')}")

                obj = data.get("objects", [{}])[0]
                offer = obj.get("offerPriceDetails", [{}])[0] if obj.get("offerPriceDetails") else {}

                return ProductData(
                    title=obj.get("title", ""),
                    description=obj.get("description", ""),
                    price=offer.get("price", 0.0),
                    currency=offer.get("currency", "USD"),
                    availability=obj.get("availability", ""),
                    images=[img.get("url", "") for img in obj.get("images", [])],
                    url=obj.get("pageUrl", url)
                )

        except Exception as e:
            raise Exception(f"Failed to extract product data: {str(e)}")

    # ==================== Video Information ====================

    async def extract_video_info(
        self,
        url: str
    ) -> VideoInfo:
        """
        Extract video information from a video page.

        Args:
            url: Video page URL

        Returns:
            VideoInfo with video details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {
                "token": self.api_token,
                "url": url
            }

            async with self.session.get(
                self._get_url("video"),
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200 or "error" in data:
                    raise Exception(f"Diffbot API error: {data.get('error', 'Unknown error')}")

                obj = data.get("objects", [{}])[0]

                return VideoInfo(
                    title=obj.get("title", ""),
                    description=obj.get("description", ""),
                    duration=obj.get("duration", 0),
                    url=obj.get("url", ""),
                    thumbnail=obj.get("thumbnail", ""),
                    embedUrl=obj.get("embedUrl", "")
                )

        except Exception as e:
            raise Exception(f"Failed to extract video info: {str(e)}")