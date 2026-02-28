"""
YouTube API Client
YouTube channel analytics and reporting
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import time


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, max_requests: int = 100, per_seconds: int = 100):
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


class YoutubeClient:
    """
    YouTube Data API client for channel analytics.

    Rate Limit: 100 units per 100 seconds per user
    """

    BASE_URL = "https://youtube.googleapis.com/youtube/v3"

    def __init__(self, api_key: str):
        """
        Initialize YouTube API client.

        Args:
            api_key: YouTube Data API key
        """
        self.api_key = api_key
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=100, per_seconds=100)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            "Accept": "application/json"
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
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails or returns error
        """
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}{endpoint}"
        final_params = params or {}
        final_params["key"] = self.api_key

        try:
            async with self.session.request(
                method,
                url,
                headers=self._get_headers(),
                params=final_params,
                json=json_data
            ) as response:
                try:
                    data = await response.json()
                except:
                    text = await response.text()
                    data = {"raw_response": text}

                if response.status >= 400:
                    error_msg = data.get("error", {}).get("message", data.get("error", "Unknown error"))
                    raise Exception(f"YouTube API error ({response.status}): {error_msg}")

                return data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during YouTube API request: {str(e)}")

    # ==================== Channel Reports ====================

    async def get_channel_report(
        self,
        channel_id: Optional[str] = None,
        metrics: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        dimensions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get channel analytics report.

        Args:
            channel_id: Channel ID
            metrics: List of metrics (views, estimatedMinutesWatched, subscribersGained, etc.)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            dimensions: List of dimensions (day, deviceType, etc.)

        Returns:
            Channel analytics report

        Raises:
            Exception: If request fails
        """
        params = {
            "ids": f"channel=={channel_id}" if channel_id else "channel==MINE",
            "metrics": ",".join(metrics) if metrics else "views,estimatedMinutesWatched,subscribersGained,subscribersLost"
        }

        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if dimensions:
            params["dimensions"] = ",".join(dimensions)

        return await self._request("GET", "/reports", params=params)