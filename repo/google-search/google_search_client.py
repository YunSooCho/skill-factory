"""
Google Custom Search API Client

Provides async client for Google Custom Search API with rate limiting.
"""

import aiohttp
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class SearchResult:
    """Single search result"""
    title: str
    snippet: str
    link: str
    display_link: str
    html_title: Optional[str] = None
    html_snippet: Optional[str] = None
    cache_id: Optional[str] = None
    file_format: Optional[str] = None
    image: Optional[Dict[str, Any]] = None


@dataclass
class SearchResponse:
    """Search API response"""
    kind: str
    url: Dict[str, str]
    queries: Dict[str, List[Dict[str, Any]]]
    context: Dict[str, str]
    search_information: Dict[str, Any]
    items: List[SearchResult]
    total_results: int = field(init=False)
    search_time: float = field(init=False)

    def __post_init__(self):
        """Extract commonly used fields"""
        self.total_results = int(self.search_information.get('total_results', 0))
        self.search_time = float(self.search_information.get('search_time', 0.0))


class RateLimiter:
    """Rate limiter for API calls"""

    def __init__(self, max_requests: int = 100, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests: List[datetime] = []
        self.lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Wait until a request can be made"""
        async with self.lock:
            now = datetime.now(timezone.utc)

            # Remove old requests outside the time window
            cutoff = now - timedelta(seconds=self.per_seconds)
            self.requests = [req for req in self.requests if req > cutoff]

            # Check if need to wait
            if len(self.requests) >= self.max_requests:
                oldest_request = sorted(self.requests)[0]
                sleep_time = (oldest_request + timedelta(seconds=self.per_seconds) - now).total_seconds()
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)

            self.requests.append(now)


class GoogleSearchClient:
    """
    Async Google Custom Search API client with rate limiting.

    API Documentation: https://developers.google.com/custom-search/v1/overview

    Requires:
    - API key from https://cloud.google.com/docs/authentication/api-keys
    - Custom Search Engine ID (cx) from https://programmablesearchengine.google.com/
    """

    BASE_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(
        self,
        api_key: str,
        search_engine_id: str,
        max_requests_per_day: int = 100
    ):
        """
        Initialize Google Search client.

        Args:
            api_key: Google Cloud API key
            search_engine_id: Custom Search Engine ID (cx parameter)
            max_requests_per_day: Daily rate limit (default: 100 free tier)
        """
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=max_requests_per_day, per_seconds=86400)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def search(
        self,
        query: str,
        num: int = 10,
        start: int = 1,
        lr: Optional[str] = None,
        safe: str = "off",
        filter: str = "1",
        gl: Optional[str] = None,
        cr: Optional[str] = None,
        dateRestrict: Optional[str] = None,
        exactTerms: Optional[str] = None,
        excludeTerms: Optional[str] = None,
        fileType: Optional[str] = None,
        highRange: Optional[str] = None,
        hq: Optional[str] = None,
        linkSite: Optional[str] = None,
        lowRange: Optional[str] = None,
        orTerms: Optional[str] = None,
        siteSearch: Optional[str] = None,
        siteSearchFilter: Optional[str] = None,
        sort: Optional[str] = None
    ) -> SearchResponse:
        """
        Perform Google search.

        Args:
            query: Search query string
            num: Number of results to return (1-10, default: 10)
            start: Start index for pagination (default: 1)
            lr: Language restrict (e.g., "lang_ja" for Japanese)
            safe: Safe search level ("off", "medium", "high", default: "off")
            filter: Filter duplicates ("1" to filter, default: "1")
            gl: Geolocation of user (e.g., "jp", "us")
            cr: Country restrict (e.g., "countryJP")
            dateRestrict: Date restriction (e.g., "d7" for past 7 days)
            exactTerms: Exact match terms
            excludeTerms: Terms to exclude
            fileType: File type to search (e.g., "pdf", "doc")
            highRange: Numeric search high range
            hq: Additional query terms
            linkSite: Require results from this site
            lowRange: Numeric search low range
            orTerms: Optional terms (any of these)
            siteSearch: Search within specific site
            siteSearchFilter: Site search filter ("e" to include, "i" to exclude)
            sort: Sort results

        Returns:
            SearchResponse with search results

        Raises:
            ValueError: If API returns error
            aiohttp.ClientError: If request fails
        """
        await self.rate_limiter.acquire()

        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": min(num, 10),  # API limit is 10
            "start": start,
            "safe": safe,
            "filter": filter
        }

        # Add optional parameters
        optional_params = {
            "lr": lr,
            "gl": gl,
            "cr": cr,
            "dateRestrict": dateRestrict,
            "exactTerms": exactTerms,
            "excludeTerms": excludeTerms,
            "fileType": fileType,
            "highRange": highRange,
            "hq": hq,
            "linkSite": linkSite,
            "lowRange": lowRange,
            "orTerms": orTerms,
            "siteSearch": siteSearch,
            "siteSearchFilter": siteSearchFilter,
            "sort": sort
        }

        for key, value in optional_params.items():
            if value is not None:
                params[key] = value

        try:
            async with self.session.get(self.BASE_URL, params=params) as response:
                data = await response.json()

                if response.status != 200:
                    error_msg = data.get('error', {}).get('message', 'Unknown error')
                    raise ValueError(f"Google Search API error ({response.status}): {error_msg}")

                # Convert items to SearchResult objects
                items = [SearchResult(**item) for item in data.get('items', [])]

                return SearchResponse(
                    kind=data.get('kind', ''),
                    url=data.get('url', {}),
                    queries=data.get('queries', {}),
                    context=data.get('context', {}),
                    search_information=data.get('searchInformation', {}),
                    items=items
                )

        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"HTTP request failed: {e}")
        except Exception as e:
            raise ValueError(f"API request failed: {e}")


# ==================== Example Usage ====================

async def main():
    """Example usage of Google Search client"""

    # Replace with your actual credentials
    api_key = "your-google-api-key"
    search_engine_id = "your-custom-search-engine-id"

    async with GoogleSearchClient(api_key=api_key, search_engine_id=search_engine_id) as client:
        try:
            # Basic search
            response = await client.search("Python async programming")
            print(f"Found {response.total_results} results in {response.search_time:.2f}s")

            for result in response.items[:3]:
                print(f"\nTitle: {result.title}")
                print(f"URL: {result.link}")
                print(f"Snippet: {result.snippet[:100]}...")

            # Search with more results
            response = await client.search(
                "machine learning",
                num=10,
                gl="us",
                cr="countryUS"
            )
            print(f"\nFound {response.total_results} results about machine learning")

            # Search for PDF files
            response = await client.search(
                "research paper",
                fileType="pdf",
                dateRestrict="d30"  # Past 30 days
            )
            print(f"\nFound {response.total_results} PDF documents from last 30 days")

        except ValueError as e:
            print(f"API Error: {e}")
        except aiohttp.ClientError as e:
            print(f"Connection error: {e}")


if __name__ == "__main__":
    asyncio.run(main())