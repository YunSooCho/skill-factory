"""
Cloud phone system API Client
Sales
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


class ZoomPhoneClient:
    """
    Cloud phone system API client.
    """

    BASE_URL = "https://api.zoom.us/v2/phone"

    def __init__(self, api_key: str):
        """
        Initialize ZoomPhoneClient API client.

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
                    raise Exception(f"ZoomPhoneClient API error ({response.status}): {error_msg}")

                return data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during ZoomPhoneClient API request: {str(e)}")


    # ==================== API Methods ====================

    async def get_call_logs(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page_size: int = 30,
        next_page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get call log list (コールログの一覧を取得).

        Args:
            from_date: Start date (YYYY-MM-DD format)
            to_date: End date (YYYY-MM-DD format)
            page_size: Number of records per page (default: 30, max: 300)
            next_page_token: Token for pagination

        Returns:
            List of call logs

        Raises:
            Exception: If request fails
        """
        params = {
            "page_size": min(page_size, 300)
        }
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if next_page_token:
            params["next_page_token"] = next_page_token

        return await self._request("GET", "/call_logs", params=params)

    async def get_call_log_details(self, call_id: str) -> Dict[str, Any]:
        """
        Get call log details (コールログの詳細を取得).

        Args:
            call_id: Call log ID

        Returns:
            Detailed call log information

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/call_logs/{call_id}")

    async def get_call_recording_info(self, call_id: str) -> Dict[str, Any]:
        """
        Get call recording information (通話のレコーディング情報を取得).

        Args:
            call_id: Call ID

        Returns:
            Recording metadata and download URL

        Raises:
            Exception: If request fails
        """
        return await self._request("GET", f"/call_logs/{call_id}/recordings")

    async def download_recording_file(self, call_id: str, download_path: str) -> Dict[str, Any]:
        """
        Download recording file (レコーディングファイルをダウンロード).

        Args:
            call_id: Call ID or recording ID
            download_path: Local path to save the recording file

        Returns:
            Download result with file path

        Raises:
            Exception: If request fails
        """
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}/call_logs/{call_id}/recordings/download"

        try:
            async with self.session.get(
                url,
                headers=self._get_headers()
            ) as response:
                if response.status >= 400:
                    error_text = await response.text()
                    raise Exception(f"ZoomPhoneClient API error ({response.status}): {error_text}")

                # Save the file
                with open(download_path, 'wb') as f:
                    f.write(await response.read())

                return {
                    "status": "success",
                    "call_id": call_id,
                    "download_path": download_path,
                    "file_size": len(await response.read())
                }

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during download: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during recording download: {str(e)}")

