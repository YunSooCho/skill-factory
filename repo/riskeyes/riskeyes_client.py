"""
Riskeyes API - Risk Intelligence Client

Supports:
- Get web article count
- Get blog article count
- Get newspaper article count
"""

import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import os


@dataclass
class ArticleCountResult:
    """Article count result"""
    query: str
    source_type: str
    total_count: int
    recent_count: int  # Last 7 days
    monthly_counts: Dict[str, int]
    sentiment_analysis: Optional[Dict[str, Any]]
    last_updated: str


class RiskeyesClient:
    """
    Riskeyes API client for risk intelligence and media monitoring.

    API Documentation: https://lp.yoom.fun/apps/riskeyes
    Requires API key from Yoom integration.
    """

    BASE_URL = "https://api.riskeyes.com/v1"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize Riskeyes client.

        Args:
            api_key: API key (defaults to YOOM_RISKEYES_API_KEY env var)
            base_url: Custom base URL for testing
        """
        self.api_key = api_key or os.environ.get("YOOM_RISKEYES_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set YOOM_RISKEYES_API_KEY environment variable")

        self.base_url = base_url or self.BASE_URL
        self.session = None
        self._rate_limit_delay = 0.5  # 500ms between requests

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request with rate limiting"""
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async with statement")

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        headers["Content-Type"] = "application/json"

        # Rate limiting
        await asyncio.sleep(self._rate_limit_delay)

        url = f"{self.base_url}{endpoint}"

        async with self.session.request(method, url, headers=headers, **kwargs) as response:
            if response.status == 429:
                retry_after = int(response.headers.get("Retry-After", 5))
                await asyncio.sleep(retry_after)
                return await self._request(method, endpoint, **kwargs)

            if response.status >= 400:
                error_text = await response.text()
                raise Exception(f"API error {response.status}: {error_text}")

            if response.status == 204:
                return {}

            return await response.json()

    # ==================== Web Article Operations ====================

    async def get_web_article_count(
        self,
        query: str,
        date_range: Optional[str] = "30d",
        include_sentiment: bool = False
    ) -> ArticleCountResult:
        """
        Get web article count for a query.

        Args:
            query: Search query string
            date_range: Date range ('7d', '30d', '90d', '1y')
            include_sentiment: Whether to include sentiment analysis

        Returns:
            ArticleCountResult with web article statistics

        Raises:
            ValueError: If query is empty
            Exception: If API request fails
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        params = {
            "query": query.strip(),
            "date_range": date_range,
            "sentiment": include_sentiment
        }

        data = await self._request("GET", "/articles/web/count", params=params)

        return ArticleCountResult(
            query=data.get("query", query),
            source_type="web",
            total_count=data.get("total_count", 0),
            recent_count=data.get("recent_count", 0),
            monthly_counts=data.get("monthly_counts", {}),
            sentiment_analysis=data.get("sentiment_analysis"),
            last_updated=data.get("last_updated", datetime.now(timezone.utc).isoformat())
        )

    # ==================== Blog Article Operations ====================

    async def get_blog_article_count(
        self,
        query: str,
        date_range: Optional[str] = "30d",
        include_sentiment: bool = False
    ) -> ArticleCountResult:
        """
        Get blog article count for a query.

        Args:
            query: Search query string
            date_range: Date range ('7d', '30d', '90d', '1y')
            include_sentiment: Whether to include sentiment analysis

        Returns:
            ArticleCountResult with blog article statistics

        Raises:
            ValueError: If query is empty
            Exception: If API request fails
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        params = {
            "query": query.strip(),
            "date_range": date_range,
            "sentiment": include_sentiment
        }

        data = await self._request("GET", "/articles/blog/count", params=params)

        return ArticleCountResult(
            query=data.get("query", query),
            source_type="blog",
            total_count=data.get("total_count", 0),
            recent_count=data.get("recent_count", 0),
            monthly_counts=data.get("monthly_counts", {}),
            sentiment_analysis=data.get("sentiment_analysis"),
            last_updated=data.get("last_updated", datetime.now(timezone.utc).isoformat())
        )

    # ==================== Newspaper Article Operations ====================

    async def get_newspaper_article_count(
        self,
        query: str,
        date_range: Optional[str] = "30d",
        include_sentiment: bool = False,
        regions: Optional[List[str]] = None
    ) -> ArticleCountResult:
        """
        Get newspaper article count for a query.

        Args:
            query: Search query string
            date_range: Date range ('7d', '30d', '90d', '1y')
            include_sentiment: Whether to include sentiment analysis
            regions: Optional list of regions to filter by

        Returns:
            ArticleCountResult with newspaper article statistics

        Raises:
            ValueError: If query is empty
            Exception: If API request fails
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        params = {
            "query": query.strip(),
            "date_range": date_range,
            "sentiment": include_sentiment
        }

        if regions:
            params["regions"] = ",".join(regions)

        data = await self._request("GET", "/articles/newspaper/count", params=params)

        return ArticleCountResult(
            query=data.get("query", query),
            source_type="newspaper",
            total_count=data.get("total_count", 0),
            recent_count=data.get("recent_count", 0),
            monthly_counts=data.get("monthly_counts", {}),
            sentiment_analysis=data.get("sentiment_analysis"),
            last_updated=data.get("last_updated", datetime.now(timezone.utc).isoformat())
        )

    # ==================== Batch Operations ====================

    async def batch_get_article_counts(
        self,
        queries: List[str],
        source_types: List[str] = None,
        date_range: str = "30d"
    ) -> Dict[str, Any]:
        """
        Batch get article counts for multiple queries.

        Args:
            queries: List of search queries
            source_types: List of source types ('web', 'blog', 'newspaper')
            date_range: Date range for all queries

        Returns:
            Dictionary with batch results

        Raises:
            ValueError: If queries list is empty
            Exception: If API request fails
        """
        if not queries:
            raise ValueError("Queries list cannot be empty")

        if source_types is None:
            source_types = ["web", "blog", "newspaper"]

        payload = {
            "queries": queries,
            "source_types": source_types,
            "date_range": date_range
        }

        return await self._request("POST", "/articles/batch-count", json=payload)