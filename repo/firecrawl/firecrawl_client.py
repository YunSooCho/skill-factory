"""
Firecrawl - Web Scraping and Crawling API

Supports:
- Run Crawl
- Run Scraping
- Get Crawl Job Details
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class CrawlJob:
    """Crawl job representation"""
    job_id: str
    status: str
    start_url: str
    created_at: str
    pages_crawled: int


@dataclass
class ScrapeResult:
    """Scrape result"""
    url: str
    content: str
    markdown: str
    metadata: Dict[str, Any]


@dataclass
class CrawlResult:
    """Crawl result with all scraped pages"""
    job_id: str
    status: str
    results: List[ScrapeResult]
    total_pages: int


class FirecrawlClient:
    """
    Firecrawl API client for web scraping and crawling.

    API Documentation: https://docs.firecrawl.dev
    Requires an API key from Firecrawl.
    """

    BASE_URL = "https://api.firecrawl.dev/v1"

    def __init__(self, api_key: str):
        """
        Initialize Firecrawl client.

        Args:
            api_key: Firecrawl API key
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

    async def run_scrape(
        self,
        url: str,
        formats: Optional[List[str]] = None,
        timeout: int = 30000
    ) -> ScrapeResult:
        """
        Scrape a single URL.

        Args:
            url: URL to scrape
            formats: Output formats (markdown, html, etc.)
            timeout: Timeout in milliseconds

        Returns:
            ScrapeResult with scraped content

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "url": url,
                "timeout": timeout
            }

            if formats:
                payload["formats"] = formats

            async with self.session.post(
                f"{self.BASE_URL}/scrape",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Firecrawl error: {data.get('error', 'Unknown error')}")

                return ScrapeResult(
                    url=data["url"],
                    content=data.get("content", ""),
                    markdown=data.get("markdown", ""),
                    metadata=data.get("metadata", {})
                )

        except Exception as e:
            raise Exception(f"Failed to scrape URL: {str(e)}")

    async def run_crawl(
        self,
        url: str,
        limit: int = 100,
        formats: Optional[List[str]] = None
    ) -> CrawlJob:
        """
        Start a crawl job on a URL.

        Args:
            url: Starting URL for crawl
            limit: Maximum number of pages to crawl
            formats: Output formats

        Returns:
            CrawlJob with job details

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "url": url,
                "limit": limit
            }

            if formats:
                payload["formats"] = formats

            async with self.session.post(
                f"{self.BASE_URL}/crawl",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Firecrawl error: {data.get('error', 'Unknown error')}")

                return CrawlJob(
                    job_id=data["job_id"],
                    status=data["status"],
                    start_url=data["start_url"],
                    created_at=data["created_at"],
                    pages_crawled=data.get("pages_crawled", 0)
                )

        except Exception as e:
            raise Exception(f"Failed to start crawl: {str(e)}")

    async def get_crawl_job(self, job_id: str) -> CrawlResult:
        """
        Get details of a crawl job.

        Args:
            job_id: Crawl job ID

        Returns:
            CrawlResult with job details and results

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/crawl/{job_id}"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Firecrawl error: {data.get('error', 'Unknown error')}")

                results = [
                    ScrapeResult(
                        url=result.get("url", ""),
                        content=result.get("content", ""),
                        markdown=result.get("markdown", ""),
                        metadata=result.get("metadata", {})
                    )
                    for result in data.get("data", [])
                ]

                return CrawlResult(
                    job_id=data["job_id"],
                    status=data["status"],
                    results=results,
                    total_pages=data.get("total_pages", len(results))
                )

        except Exception as e:
            raise Exception(f"Failed to get crawl job: {str(e)}")