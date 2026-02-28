"""
Google Meet conferencing API Client
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
                            if now - req_time < self.per_seconds}

            if len(self.requests) >= self.max_requests:
                sleep_time = self.per_seconds - (now - self.requests[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    self.requests = []

            self.requests.append(now)


class GoogleMeetClient:
    """
    Google Meet conferencing API client.
    """

    BASE_URL = "https://meet.googleapis.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize GoogleMeetClient API client.

        Args:
            api_key: Your API key
        """
        self.api_key = api_key
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
                    raise Exception(f"GoogleMeetClient API error ({response.status}): {error_msg}")

                return data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during GoogleMeetClient API request: {str(e)}")


    # ==================== API Methods ====================

    async def create_meeting_space(
        self,
        name: Optional[str] = None,
        access_type: str = "anyone",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create meeting space (会議スペースを作成).

        Args:
            name: Meeting space name
            access_type: Access type (anyone, trusted_domains, invited_only)
            **kwargs: Additional fields

        Returns:
            Created meeting space data

        Raises:
            Exception: If request fails
        """
        data = {
            "name": name,
            "access_type": access_type,
            **kwargs
        }
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("POST", "/spaces", json_data=data)

    async def list_meetings(
        self,
        page_size: int = 100,
        page_token: Optional[str] = None,
        filter_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get meeting information list (会議情報の一覧を取得).

        Args:
            page_size: Number of results per page (default: 100)
            page_token: Token for pagination
            filter_by: Filter meetings (e.g., "upcoming", "past")

        Returns:
            List of meetings

        Raises:
            Exception: If request fails
        """
        params = {
            "pageSize": min(page_size, 100)
        }
        if page_token:
            params["pageToken"] = page_token
        if filter_by:
            params["filter"] = filter_by

        return await self._request("GET", "/conferences", params=params)

    async def get_meeting(self, conference_code: str) -> Dict[str, Any]:
        """
        Get specific meeting information (特定の会議情報を取得).

        Args:
            conference_code: Conference code or meeting ID

        Returns:
            Meeting information

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/conferences/{conference_code}")

    async def get_meeting_space_details(self, space_name: str) -> Dict[str, Any]:
        """
        Get meeting space details (会議スペースの詳細を取得).

        Args:
            space_name: Space name

        Returns:
            Meeting space details

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/spaces/{space_name}")

    async def get_participants(
        self,
        conference_code: str,
        page_size: int = 100,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get meeting participants list (会議の参加者一覧を取得).

        Args:
            conference_code: Conference code or meeting ID
            page_size: Number of results per page (default: 100)
            page_token: Token for pagination

        Returns:
            List of participants

        Raises:
            Exception: If request fails
        """
        params = {
            "pageSize": min(page_size, 100)
        }
        if page_token:
            params["pageToken"] = page_token

        return await self._request("GET", f"/conferences/{conference_code}/participants", params=params)

    async def get_transcription(self, conference_code: str) -> Dict[str, Any]:
        """
        Get transcription information (文字起こし情報を取得).

        Args:
            conference_code: Conference code or meeting ID

        Returns:
            Transcription data

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/conferences/{conference_code}/transcripts")

    async def get_recording_info(self, conference_code: str) -> Dict[str, Any]:
        """
        Get recording information (レコーディング情報を取得).

        Args:
            conference_code: Conference code or meeting ID

        Returns:
            Recording metadata and download URLs

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/conferences/{conference_code}/recordings")