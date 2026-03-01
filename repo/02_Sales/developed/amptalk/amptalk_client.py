"""
Amptalk API Client

Conversation analysis and call summarization platform for:
- Call summaries
- Analytics and insights
- User management
- Call search and retrieval

API Actions (5):
1. 通話の要約を取得 (Get Call Summary)
2. 分析情報を取得 (Get Analytics Info)
3. ユーザーの一覧を取得 (List Users)
4. 通話を検索 (Search Calls)
5. 通話を取得 (Get Call)

Triggers (1):
- 通話が完了したら (When call is completed)

Authentication: API Key
Base URL: https://api.amptalk.com/v1
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class User:
    """User model"""
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Call:
    """Call model"""
    id: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[int] = None
    status: Optional[str] = None
    user_id: Optional[str] = None
    created_at: Optional[str] = None
    ended_at: Optional[str] = None


@dataclass
class CallSummary:
    """Call summary model"""
    call_id: Optional[str] = None
    summary: Optional[str] = None
    key_points: List[str] = None
    action_items: List[str] = None
    sentiment: Optional[str] = None
    topics: List[str] = None

    def __post_init__(self):
        if self.key_points is None:
            self.key_points = []
        if self.action_items is None:
            self.action_items = []
        if self.topics is None:
            self.topics = []


@dataclass
class Analytics:
    """Analytics model"""
    total_calls: Optional[int] = None
    total_duration: Optional[int] = None
    average_duration: Optional[float] = None
    sentiment_breakdown: Optional[Dict[str, int]] = None
    top_topics: List[str] = None

    def __post_init__(self):
        if self.top_topics is None:
            self.top_topics = []


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, calls_per_second: int = 10):
        self.calls_per_second = calls_per_second
        self.tokens = calls_per_second
        self.last_update = datetime.now()

    async def acquire(self):
        """Acquire a token from the rate limiter"""
        now = datetime.now()
        elapsed = (now - self.last_update).total_seconds()
        self.tokens = min(self.calls_per_second, self.tokens + elapsed * self.calls_per_second)
        self.last_update = now

        if self.tokens < 1:
            sleep_time = (1 - self.tokens) / self.calls_per_second
            await asyncio.sleep(sleep_time)
            self.tokens = self.calls_per_second
        else:
            self.tokens -= 1


class AmptalkError(Exception):
    """Base exception for Amptalk errors"""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}" if status_code else message)


class AmptalkClient:
    """
    Amptalk API Client

    Example usage:
        ```python
        client = AmptalkClient(api_key="your_key")

        # List users
        users = await client.list_users()

        # Get call summary
        summary = await client.get_call_summary(call_id="call_123")

        # Search calls
        calls = await client.search_calls(user_id="user_123")
        ```
    """

    def __init__(self, api_key: str, base_url: str = "https://api.amptalk.com/v1"):
        """
        Initialize Amptalk client

        Args:
            api_key: Amptalk API key
            base_url: API base URL
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self._rate_limiter = RateLimiter(calls_per_second=10)

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Amptalk API"""
        await self._rate_limiter.acquire()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method=method,
                    url=url,
                    headers=self._headers,
                    json=data,
                    params=params
                ) as response:
                    response_text = await response.text()

                    if response.status == 204:
                        return {"status": "success"}

                    if response.status >= 400:
                        try:
                            error_data = await response.json()
                            error_msg = error_data.get("message", error_data.get("error", "Unknown error"))
                        except:
                            error_msg = response_text if response_text else "HTTP error"
                        raise AmptalkError(error_msg, response.status)

                    return await response.json()

            except aiohttp.ClientError as e:
                raise AmptalkError(f"Network error: {str(e)}")
            except asyncio.TimeoutError:
                raise AmptalkError("Request timeout")

    async def get_call_summary(self, call_id: str) -> CallSummary:
        """
        通話の要約を取得 (Get Call Summary)

        Args:
            call_id: Call ID

        Returns:
            CallSummary object with summary, key points, action items, etc.
        """
        response = await self._make_request("GET", f"/calls/{call_id}/summary")
        return CallSummary(
            call_id=response.get("call_id"),
            summary=response.get("summary"),
            key_points=response.get("key_points", []),
            action_items=response.get("action_items", []),
            sentiment=response.get("sentiment"),
            topics=response.get("topics", [])
        )

    async def get_analytics(self, **params) -> Analytics:
        """
        分析情報を取得 (Get Analytics Info)

        Args:
            **params: Analytics parameters (start_date, end_date, user_id, etc.)

        Returns:
            Analytics object with call statistics and insights
        """
        response = await self._make_request("GET", "/analytics", params=params)
        return Analytics(
            total_calls=response.get("total_calls"),
            total_duration=response.get("total_duration"),
            average_duration=response.get("average_duration"),
            sentiment_breakdown=response.get("sentiment_breakdown"),
            top_topics=response.get("top_topics", [])
        )

    async def list_users(self, **params) -> List[User]:
        """
        ユーザーの一覧を取得 (List Users)

        Args:
            **params: Query parameters (limit, offset, etc.)

        Returns:
            List of User objects
        """
        response = await self._make_request("GET", "/users", params=params)
        if "data" in response:
            return [User(**item) for item in response["data"]]
        if "users" in response:
            return [User(**item) for item in response["users"]]
        return []

    async def search_calls(self, **params) -> List[Call]:
        """
        通話を検索 (Search Calls)

        Args:
            **params: Search parameters (user_id, start_date, end_date, status, etc.)

        Returns:
            List of Call objects
        """
        response = await self._make_request("GET", "/calls", params=params)
        if "data" in response:
            return [Call(**item) for item in response["data"]]
        if "calls" in response:
            return [Call(**item) for item in response["calls"]]
        return []

    async def get_call(self, call_id: str) -> Call:
        """
        通話を取得 (Get Call)

        Args:
            call_id: Call ID

        Returns:
            Call object
        """
        response = await self._make_request("GET", f"/calls/{call_id}")
        return Call(**response)

    # Webhook handling

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process webhook event - 通話が完了したら (When call is completed)

        Args:
            webhook_data: Webhook payload

        Returns:
            Processed event data
        """
        event_type = webhook_data.get("event_type", "unknown")
        call_id = webhook_data.get("call_id")

        return {
            "event_type": event_type,
            "call_id": call_id,
            "data": webhook_data
        }