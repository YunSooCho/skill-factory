"""
Google custom search API API Client
General
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
import time


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, max_requests: int = 120, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.time()
            self.requests = [req_time for req_time in self.requests
                            if now - req_time < self.per_seconds]

            if len(self.requests) >= self.max_requests:
                sleep_time = self.per_seconds - (now - self.requests[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    self.requests = []

            self.requests.append(now)


class GoogleSearchClient:
    """
    Google custom search API API client.
    """

    BASE_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self, api_key: str, search_engine_id: Optional[str] = None):
        """
        Initialize GoogleSearchClient API client.

        Args:
            api_key: Your API key
            search_engine_id: Custom Search Engine ID (for Custom Search API)
        """
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=120, per_seconds=60)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API request with error handling and rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data

        Raises:
            Exception: If request fails
        """
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}{endpoint}"

        try:
            async with self.session.request(
                method,
                url,
                headers=self._get_headers(),
                params=params,
                json=json_data
            ) as response:
                try:
                    data = await response.json()
                except:
                    text = await response.text()
                    data = {"raw_response": text}

                if response.status >= 400:
                    error_msg = data.get("error", data.get("message", "Unknown error"))
                    raise Exception(f"GoogleSearchClient API error ({response.status}): {error_msg}")

                return data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during GoogleSearchClient API request: {str(e)}")


    # ==================== API Methods ====================

    async def search(
        self,
        query: str,
        search_type: Optional[str] = None,
        start: int = 1,
        num: int = 10,
        language: str = "ja",
        country: str = "JP",
        sort: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get search results (検索結果を取得).

        Args:
            query: Search query string
            search_type: Type of search (e.g., "image" for images, "news" for news)
            start: Start index for pagination (default: 1)
            num: Number of results to return (default: 10, max: 10 for free tier)
            language: Language code (default: ja)
            country: Country code (default: JP)
            sort: Sort order (e.g., "date" for recent results)

        Returns:
            Search results with title, URL, snippet, and other metadata

        Raises:
            Exception: If request fails
        """
        params = {
            "key": self.api_key,
            "q": query,
            "start": start,
            "num": min(num, 10),
            "hl": language,
            "gl": country
        }

        if self.search_engine_id:
            params["cx"] = self.search_engine_id
        if search_type:
            params["searchType"] = search_type
        if sort:
            params["sort"] = sort

        return await self._request("GET", "", params=params)

