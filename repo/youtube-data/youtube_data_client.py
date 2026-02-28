"""
YouTube Data API Client
Comprehensive YouTube API for videos, channels, playlists, comments
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List, BinaryIO
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


class YoutubeDataClient:
    """
    YouTube Data API v3 client.

    Rate Limit: 100 units per 100 seconds per user
    """

    BASE_URL = "https://youtube.googleapis.com/youtube/v3"

    def __init__(self, api_key: str, access_token: Optional[str] = None):
        """
        Initialize YouTube Data API client.

        Args:
            api_key: YouTube Data API key
            access_token: OAuth 2.0 access token for write operations
        """
        self.api_key = api_key
        self.access_token = access_token
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
        headers = {
            "Accept": "application/json"
        }
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[BinaryIO] = None
    ) -> Dict[str, Any]:
        """
        Make API request with error handling and rate limiting.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data
            data: Binary data for file uploads

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
                json=json_data,
                data=data
            ) as response:
                try:
                    data_ = await response.json()
                except:
                    text = await response.text()
                    data_ = {"raw_response": text}

                if response.status >= 400:
                    error_msg = data_.get("error", {}).get("message", data_.get("error", "Unknown error"))
                    raise Exception(f"YouTube API error ({response.status}): {error_msg}")

                return data_

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during YouTube API request: {str(e)}")

    # ==================== Channel ====================

    async def get_channel_info(
        self,
        channel_id: Optional[str] = None,
        username: Optional[str] = None,
        part: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get channel information.

        Args:
            channel_id: Channel ID
            username: Channel username
            part: List of parts to include (snippet, contentDetails, statistics, etc.)

        Returns:
            Channel information

        Raises:
            Exception: If request fails or neither channel_id nor username is provided
        """
        if not channel_id and not username:
            raise ValueError("Either channel_id or username must be provided")

        params = {
            "part": ",".join(part) if part else "snippet,contentDetails,statistics"
        }

        if channel_id:
            params["id"] = channel_id
        else:
            params["forUsername"] = username

        response = await self._request("GET", "/channels", params=params)
        return response.get("items", [])

    async def get_channel_videos(
        self,
        channel_id: str,
        max_results: int = 50,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get videos from a channel.

        Args:
            channel_id: Channel ID
            max_results: Maximum number of results (1-50)
            page_token: Page token for pagination

        Returns:
            List of videos

        Raises:
            Exception: If request fails
        """
        # First get channel's upload playlist
        channel = await self.get_channel_info(channel_id, part=["contentDetails"])
        if not channel:
            raise Exception("Channel not found")

        upload_playlist_id = channel[0]["contentDetails"]["relatedPlaylists"]["uploads"]

        # Get videos from playlist
        return await self.get_playlist_videos(upload_playlist_id, max_results, page_token)

    # ==================== Videos ====================

    async def search_videos(
        self,
        query: str,
        max_results: int = 25,
        order: str = "relevance",
        video_duration: Optional[str] = None,
        channel_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for videos.

        Args:
            query: Search query
            max_results: Maximum number of results (1-50)
            order: Sort order (date, rating, relevance, title, videoCount, viewCount)
            video_duration: Filter by duration (any, long, medium, short)
            channel_id: Filter by channel ID

        Returns:
            Search results

        Raises:
            Exception: If request fails
        """
        params = {
            "q": query,
            "part": "snippet",
            "type": "video",
            "maxResults": max_results,
            "order": order
        }

        if video_duration:
            params["videoDuration"] = video_duration
        if channel_id:
            params["channelId"] = channel_id

        return await self._request("GET", "/search", params=params)

    async def get_video_stats(
        self,
        video_ids: List[str],
        part: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get video statistics.

        Args:
            video_ids: List of video IDs
            part: List of parts to include (snippet, contentDetails, statistics, etc.)

        Returns:
            Video statistics

        Raises:
            Exception: If request fails
        """
        params = {
            "id": ",".join(video_ids),
            "part": ",".join(part) if part else "snippet,statistics"
        }

        response = await self._request("GET", "/videos", params=params)
        return response.get("items", [])

    async def upload_video(
        self,
        video_file: BinaryIO,
        title: str,
        description: str,
        tags: Optional[List[str]] = None,
        privacy_status: str = "private"
    ) -> Dict[str, Any]:
        """
        Upload a video to YouTube.

        Args:
            video_file: Video file object
            title: Video title
            description: Video description
            tags: Optional list of tags
            privacy_status: Privacy status (public, private, unlisted)

        Returns:
            Uploaded video data

        Raises:
            Exception: If request fails or no access token provided
        """
        if not self.access_token:
            raise ValueError("Access token required for upload operations")

        metadata = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or []
            },
            "status": {
                "privacyStatus": privacy_status
            }
        }

        # Initialize upload session
        init_response = await self._request(
            "POST",
            "/videos?uploadType=resumable&part=snippet,status",
            json_data=metadata
        )

        upload_url = init_response.get("url")
        if not upload_url:
            raise Exception("Failed to initialize upload session")

        # Upload video file
        async with self.session.put(upload_url, data=video_file) as response:
            if response.status >= 400:
                raise Exception(f"Upload failed: {await response.text()}")

            return await response.json()

    # ==================== Comments ====================

    async def get_comment_threads(
        self,
        video_id: str,
        max_results: int = 20,
        page_token: Optional[str] = None,
        order: str = "relevance"
    ) -> Dict[str, Any]:
        """
        Get comment threads for a video.

        Args:
            video_id: Video ID
            max_results: Maximum number of results (1-100)
            page_token: Page token for pagination
            order: Sort order (relevance, time)

        Returns:
            Comment threads

        Raises:
            Exception: If request fails
        """
        params = {
            "part": "snippet,replies",
            "videoId": video_id,
            "maxResults": max_results,
            "order": order
        }

        if page_token:
            params["pageToken"] = page_token

        return await self._request("GET", "/commentThreads", params=params)

    async def reply_to_comment(
        self,
        parent_comment_id: str,
        text: str
    ) -> Dict[str, Any]:
        """
        Reply to a comment.

        Args:
            parent_comment_id: Parent comment ID
            text: Reply text

        Returns:
            Created comment data

        Raises:
            Exception: If request fails or no access token provided
        """
        if not self.access_token:
            raise ValueError("Access token required for comment operations")

        return await self._request(
            "POST",
            "/comments?part=snippet",
            json_data={
                "snippet": {
                    "parentId": parent_comment_id,
                    "textOriginal": text
                }
            }
        )

    # ==================== Playlists ====================

    async def create_playlist(
        self,
        title: str,
        description: str,
        privacy_status: str = "private"
    ) -> Dict[str, Any]:
        """
        Create a playlist.

        Args:
            title: Playlist title
            description: Playlist description
            privacy_status: Privacy status (public, private, unlisted)

        Returns:
            Created playlist data

        Raises:
            Exception: If request fails or no access token provided
        """
        if not self.access_token:
            raise ValueError("Access token required for playlist operations")

        return await self._request(
            "POST",
            "/playlists?part=snippet,status",
            json_data={
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": privacy_status
                }
            }
        )

    async def add_to_playlist(
        self,
        playlist_id: str,
        video_id: str,
        position: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Add a video to a playlist.

        Args:
            playlist_id: Playlist ID
            video_id: Video ID
            position: Position in playlist (optional)

        Returns:
            Playlist item data

        Raises:
            Exception: If request fails or no access token provided
        """
        if not self.access_token:
            raise ValueError("Access token required for playlist operations")

        data = {
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }

        if position is not None:
            data["snippet"]["position"] = position

        return await self._request(
            "POST",
            "/playlistItems?part=snippet",
            json_data=data
        )

    async def get_playlist_videos(
        self,
        playlist_id: str,
        max_results: int = 50,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get videos from a playlist.

        Args:
            playlist_id: Playlist ID
            max_results: Maximum number of results (1-50)
            page_token: Page token for pagination

        Returns:
            Playlist videos

        Raises:
            Exception: If request fails
        """
        params = {
            "part": "snippet,contentDetails",
            "playlistId": playlist_id,
            "maxResults": max_results
        }

        if page_token:
            params["pageToken"] = page_token

        return await self._request("GET", "/playlistItems", params=params)

    # ==================== Captions ====================

    async def get_captions(
        self,
        video_id: str,
        part: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get captions for a video.

        Args:
            video_id: Video ID
            part: List of parts to include (id, snippet)

        Returns:
            Caption information

        Raises:
            Exception: If request fails
        """
        params = {
            "videoId": video_id,
            "part": ",".join(part) if part else "id,snippet"
        }

        response = await self._request("GET", "/captions", params=params)
        return response.get("items", [])

    async def download_caption(self, caption_id: str, tfmt: str = "srt") -> str:
        """
        Download caption text.

        Args:
            caption_id: Caption ID
            tfmt: Format (srt, vtt)

        Returns:
            Caption text

        Raises:
            Exception: If request fails
        """
        params = {"tfmt": tfmt}

        # Get caption download URL
        caption_info = await self._request(
            "GET",
            f"/captions/{caption_id}",
            params=params
        )

        return caption_info

    # ==================== Webhook Handling ====================

    def handle_webhook(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle YouTube webhook events.

        Supported events:
        - Comment posted
        - New video uploaded with keyword
        - New video in channel

        Args:
            event_data: Webhook event data

        Returns:
            Processed event data

        Raises:
            Exception: If event data is invalid
        """
        if not event_data:
            raise ValueError("Invalid webhook event data")

        event_data["processed_at"] = datetime.utcnow().isoformat()

        # Determine event type and category
        if "video_id" in event_data:
            event_type = event_data.get("event_type", "video_published")
            if event_type == "comment_posted":
                event_data["category"] = "comment"
            elif "keyword" in event_data and event_type == "video_published":
                event_data["category"] = "keyword_match"
            else:
                event_data["category"] = "video"
        else:
            event_data["category"] = "unknown"

        return event_data