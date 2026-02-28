"""
SerpApi Client Implementation - Search API
"""

import requests
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class RateLimiter:
    max_requests: int = 100
    time_window: int = 60
    requests: list = None

    def __post_init__(self):
        if self.requests is None:
            self.requests = []

    def wait_if_needed(self):
        now = time.time()
        self.requests = [r for r in self.requests if now - r < self.time_window]

        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
                self.requests = []

        self.requests.append(now)


class SerpApiError(Exception):
    pass


class APIError(SerpApiError):
    pass


class SerpApiClient:
    """SerpApi Client - Real-time Google, Bing, YouTube, and other search APIs"""

    BASE_URL = "https://serpapi.com"

    def __init__(self, api_key: str, timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limiter = RateLimiter(max_requests=100, time_window=60)
        self.session = requests.Session()

    def _make_request(self, engine: str, params: Dict[str, Any]) -> Dict[str, Any]:
        self.rate_limiter.wait_if_needed()
        params['api_key'] = self.api_key
        params['source'] = 'python'
        url = f"{self.BASE_URL}/search"
        last_error = None

        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)

                if response.status_code >= 500:
                    raise APIError(f"Server error: {response.status_code}")

                response.raise_for_status()

                result = response.json()

                if result.get('error'):
                    raise APIError(result['error'])

                return result

            except requests.Timeout:
                last_error = f"Request timeout after {self.timeout} seconds"
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise APIError(last_error)
            except requests.RequestException as e:
                last_error = str(e)
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise APIError(f"Request failed: {last_error}")

        raise APIError(f"Max retries exceeded: {last_error}")

    def google_search(self, query: str, num: int = 10, **kwargs) -> Dict[str, Any]:
        """Get Google search results"""
        if not query:
            raise APIError("query is required")

        params = {
            "engine": "google",
            "q": query,
            "num": num
        }
        params.update(kwargs)
        return self._make_request("google", params)

    def bing_search(self, query: str, count: int = 10, **kwargs) -> Dict[str, Any]:
        """Get Bing search results"""
        if not query:
            raise APIError("query is required")

        params = {
            "engine": "bing",
            "q": query,
            "count": count
        }
        params.update(kwargs)
        return self._make_request("bing", params)

    def youtube_search(self, query: str, sp: str = "", **kwargs) -> Dict[str, Any]:
        """Get YouTube search results"""
        if not query:
            raise APIError("query is required")

        params = {
            "engine": "youtube",
            "search_query": query
        }
        if sp:
            params['sp'] = sp
        params.update(kwargs)
        return self._make_request("youtube", params)

    def google_maps_search(self, query: str, type: str = "search", **kwargs) -> Dict[str, Any]:
        """Get Google Maps search results"""
        if not query:
            raise APIError("query is required")

        params = {
            "engine": "google_maps",
            "q": query,
            "type": type
        }
        params.update(kwargs)
        return self._make_request("google_maps", params)

    def google_local_search(self, q: str, **kwargs) -> Dict[str, Any]:
        """Get Google Local search results"""
        return self.google_maps_search(q, type="place", **kwargs)

    def google_images_search(self, q: str, tbm: str = "isch", **kwargs) -> Dict[str, Any]:
        """Get Google Images search results"""
        if not q:
            raise APIError("q is required")

        params = {
            "engine": "google",
            "q": q,
            "tbm": tbm
        }
        params.update(kwargs)
        return self._make_request("google_images", params)

    def google_news_search(self, q: str, **kwargs) -> Dict[str, Any]:
        """Get Google News search results"""
        if not q:
            raise APIError("q is required")

        params = {
            "engine": "google_news",
            "q": q
        }
        params.update(kwargs)
        return self._make_request("google_news", params)

    def google_finance_search(self, q: str, **kwargs) -> Dict[str, Any]:
        """Get Google Finance search results"""
        if not q:
            raise APIError("q is required")

        params = {
            "engine": "google_finance",
            "q": q
        }
        params.update(kwargs)
        return self._make_request("google_finance", params)

    def google_autocomplete(self, q: str, **kwargs) -> Dict[str, Any]:
        """Get Google search keyword suggestions (Autocomplete)"""
        if not q:
            raise APIError("q is required")

        params = {
            "engine": "google_autocomplete",
            "q": q
        }
        params.update(kwargs)
        return self._make_request("google_autocomplete", params)

    def baidu_search(self, q: str, **kwargs) -> Dict[str, Any]:
        """Get Baidu search results"""
        if not q:
            raise APIError("q is required")

        params = {
            "engine": "baidu",
            "q": q
        }
        params.update(kwargs)
        return self._make_request("baidu", params)

    def yelp_search(self, find_desc: str, find_loc: str, **kwargs) -> Dict[str, Any]:
        """Get Yelp search results"""
        if not find_desc or not find_loc:
            raise APIError("find_desc and find_loc are required")

        params = {
            "engine": "yelp",
            "find_desc": find_desc,
            "find_loc": find_loc
        }
        params.update(kwargs)
        return self._make_request("yelp", params)

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()