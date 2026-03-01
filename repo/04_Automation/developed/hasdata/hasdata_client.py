"""
Hasdata - Web Scraping and Search API

Supports:
- Search Google Maps Location
- Scrape Google SERP
- Scrape Web Page
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class SERPResult:
    """Search Engine Result Page result"""
    query: str
    organic_results: List[Dict[str, Any]]
    ads: List[Dict[str, Any]]


@dataclass
class ScrapedContent:
    """Scraped web page content"""
    url: str
    title: str
    content: str
    html: Optional[str]


@dataclass
class MapsResult:
    """Google Maps search result"""
    query: str
    places: List[Dict[str, Any]]


class HasdataClient:
    """
    Hasdata API client for web scraping and search.

    API Documentation: https://hasdata.com/docs
    Requires an API key from Hasdata.
    """

    BASE_URL = "https://api.hasdata.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Hasdata client.

        Args:
            api_key: Hasdata API key
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

    async def scrape_web_page(
        self,
        url: str,
        options: Optional[Dict[str, Any]] = None
    ) -> ScrapedContent:
        """
        Scrape content from a web page.

        Args:
            url: URL to scrape
            options: Additional options (render_js, timeout, etc.)

        Returns:
            ScrapedContent with page data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {"url": url}

            if options:
                payload.update(options)

            async with self.session.post(
                f"{self.BASE_URL}/scrape",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Hasdata error: {data.get('error', 'Unknown error')}")

                return ScrapedContent(
                    url=data["url"],
                    title=data.get("title", ""),
                    content=data.get("content", ""),
                    html=data.get("html")
                )

        except Exception as e:
            raise Exception(f"Failed to scrape web page: {str(e)}")

    async def scrape_google_serp(
        self,
        query: str,
        country: str = "us",
        language: str = "en",
        num_results: int = 10
    ) -> SERPResult:
        """
        Scrape Google Search Engine Result Page.

        Args:
            query: Search query
            country: Country code
            language: Language code
            num_results: Number of results to retrieve

        Returns:
            SERPResult with search results

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "query": query,
                "country": country,
                "language": language,
                "num_results": num_results
            }

            async with self.session.post(
                f"{self.BASE_URL}/serp/google",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Hasdata error: {data.get('error', 'Unknown error')}")

                return SERPResult(
                    query=data["query"],
                    organic_results=data.get("organic_results", []),
                    ads=data.get("ads", [])
                )

        except Exception as e:
            raise Exception(f"Failed to scrape Google SERP: {str(e)}")

    async def search_google_maps(
        self,
        query: str,
        location: Optional[str] = None,
        limit: int = 20
    ) -> MapsResult:
        """
        Search Google Maps for locations.

        Args:
            query: Search query
            location: Geographic location to search in
            limit: Maximum number of results

        Returns:
            MapsResult with place data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "query": query,
                "limit": limit
            }

            if location:
                payload["location"] = location

            async with self.session.post(
                f"{self.BASE_URL}/maps/search",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Hasdata error: {data.get('error', 'Unknown error')}")

                return MapsResult(
                    query=data["query"],
                    places=data.get("places", [])
                )

        except Exception as e:
            raise Exception(f"Failed to search Google Maps: {str(e)}")