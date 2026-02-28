"""
YouTube Data API Actions implementation.
"""
import requests
import time
from typing import Optional, List, Dict, Any
from .exceptions import (
    YoutubeDataError,
    YoutubeDataAuthenticationError,
    YoutubeDataRateLimitError,
    YoutubeDataNotFoundError,
    YoutubeDataValidationError,
)


class YoutubeDataActions:
    """API actions for YouTube Data API integration."""

    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key: Optional[str] = None, timeout: int = 30):
        """
        Initialize API client.

        Args:
            api_key: YouTube Data API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()

        # Rate limiting configuration
        self.last_request_time = 0
        self.min_request_interval = 0.1
        self.rate_limit_remaining = 10000

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        retry_on_rate_limit: bool = True,
    ) -> Dict[str, Any]:
        """Make authenticated request with rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)

        url = f"{self.BASE_URL}{endpoint}"

        # Add API key to params
        if params is None:
            params = {}
        params["key"] = self.api_key

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self.timeout,
            )
            self.last_request_time = time.time()

            if response.status_code == 401:
                error_data = response.json() if response.text else {}
                raise YoutubeDataAuthenticationError(
                    message=error_data.get("error", {}).get("message", "Authentication failed"),
                    status_code=401,
                    response=error_data,
                )
            elif response.status_code == 404:
                raise YoutubeDataNotFoundError(
                    message="Resource not found", status_code=404
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(method, endpoint, params, json_data, False)
                raise YoutubeDataRateLimitError(
                    message="Rate limit exceeded", status_code=429
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise YoutubeDataError(
                    message=error_data.get("error", {}).get("message", f"API Error: {response.status_code}"),
                    status_code=response.status_code,
                    response=error_data,
                )

            return response.json()

        except requests.Timeout:
            raise YoutubeDataError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise YoutubeDataError(f"Request failed: {str(e)}")

    # API Actions

    def get_video_details(self, video_id: str, part: str = "snippet,statistics") -> Dict[str, Any]:
        """
        Get video details by ID.

        Args:
            video_id: YouTube video ID
            part: Response parts (snippet, statistics, contentDetails, etc.)

        Returns:
            Video details
        """
        return self._make_request("GET", "/videos", params={"id": video_id, "part": part})

    def get_channel_details(self, channel_id: str = None, username: str = None, part: str = "snippet,statistics") -> Dict[str, Any]:
        """
        Get channel details.

        Args:
            channel_id: Channel ID (optional)
            username: Channel username (forHandle parameter) (optional)
            part: Response parts

        Returns:
            Channel details
        """
        params = {"part": part}
        if channel_id:
            params["id"] = channel_id
        elif username:
            params["forHandle"] = username

        return self._make_request("GET", "/channels", params=params)

    def list_videos(self, playlist_id: str, max_results: int = 10, page_token: str = None) -> Dict[str, Any]:
        """
        List videos from a playlist.

        Args:
            playlist_id: Playlist ID
            max_results: Maximum number of results
            page_token: Pagination token

        Returns:
            List of videos
        """
        params = {
            "playlistId": playlist_id,
            "maxResults": max_results,
            "part": "snippet,contentDetails"
        }
        if page_token:
            params["pageToken"] = page_token

        return self._make_request("GET", "/playlistItems", params=params)

    def get_analytics(self, ids: str, metrics: str, start_date: str, end_date: str, dimensions: str = None) -> Dict[str, Any]:
        """
        Get YouTube analytics data.

        Args:
            ids: Channel or video IDs (e.g., channel==UC...)
            metrics: Metrics to retrieve (e.g., views,estimatedMinutesWatched)
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            dimensions: Optional dimensions (e.g., day)

        Returns:
            Analytics data
        """
        params = {
            "ids": ids,
            "metrics": metrics,
            "startDate": start_date,
            "endDate": end_date,
            "part": "snippet"
        }
        if dimensions:
            params["dimensions"] = dimensions

        return self._make_request("GET", "/reports", params=params)

    def list_channel_videos(self, channel_id: str, max_results: int = 10, order: str = "date") -> Dict[str, Any]:
        """
        List videos from a channel (requires playlist ID from uploads playlist).

        Args:
            channel_id: Channel ID
            max_results: Maximum number of results
            order: Ordering (date, rating, relevance, title, viewCount)

        Returns:
            Channel videos
        """
        # First get the uploads playlist ID from channel
        channel_data = self.get_channel_details(channel_id=channel_id, part="contentDetails")

        # Extract uploads playlist ID from response
        uploads_id = channel_data.get("items", [{}])[0].get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")

        if not uploads_id:
            raise YoutubeDataNotFoundError("Could not find uploads playlist for channel")

        return self.list_videos(uploads_id, max_results=max_results)

    def search_videos(self, query: str, max_results: int = 10, order: str = "relevance") -> Dict[str, Any]:
        """
        Search for videos.

        Args:
            query: Search query
            max_results: Maximum number of results
            order: Ordering (date, rating, relevance, title, viewCount)

        Returns:
            Search results
        """
        params = {
            "q": query,
            "maxResults": max_results,
            "order": order,
            "part": "snippet",
            "type": "video"
        }

        return self._make_request("GET", "/search", params=params)

    def close(self):
        """Close the session."""
        self.session.close()