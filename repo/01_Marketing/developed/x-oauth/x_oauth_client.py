"""
X OAuth API Client
Twitter/X API client for social media integration
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import time


@dataclass
class Post:
    """Post data model"""
    text: str
    media_ids: Optional[List[str]] = None
    reply_to_id: Optional[str] = None


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, max_requests: int = 300, per_seconds: int = 900):
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


class XOauthClient:
    """
    X (Twitter) OAuth API client.

    Rate Limit: 300 requests per 15 minutes (900 seconds)
    """

    BASE_URL = "https://api.twitter.com/2"

    def __init__(self, access_token: str):
        """
        Initialize X OAuth API client.

        Args:
            access_token: OAuth 2.0 access token
        """
        self.access_token = access_token
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=300, per_seconds=900)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with access token"""
        return {
            "Authorization": f"Bearer {self.access_token}",
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
                    error_msg = data.get("error", data.get("detail", "Unknown error"))
                    if "errors" in data:
                        errors = data["errors"]
                        if isinstance(errors, list) and len(errors) > 0:
                            error_msg = errors[0].get("message", error_msg)
                    raise Exception(f"X API error ({response.status}): {error_msg}")

                return data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during X API request: {str(e)}")

    # ==================== User Info ====================

    async def get_user_info(self, username: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get user information.

        Args:
            username: Twitter username (without @)
            user_id: User ID

        Returns:
            User information

        Raises:
            Exception: If request fails or neither username nor user_id is provided
        """
        if not username and not user_id:
            raise ValueError("Either username or user_id must be provided")

        params = {}
        if username:
            params["user.fields"] = "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            endpoint = f"/users/by/username/{username}"
        else:
            params["user.fields"] = "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            endpoint = f"/users/{user_id}"

        return await self._request("GET", endpoint, params=params)

    # ==================== Posts ====================

    async def create_post(self, post: Post) -> Dict[str, Any]:
        """
        Create a new tweet.

        Args:
            post: Post object with text and optional media/reply info

        Returns:
            Created tweet data

        Raises:
            Exception: If request fails
        """
        data = {"text": post.text}

        if post.media_ids:
            data["media"] = {"media_ids": post.media_ids}
        if post.reply_to_id:
            data["reply_settings"] = "mentionedUsers"
            data["in_reply_to_tweet_id"] = post.reply_to_id

        return await self._request("POST", "/tweets", json_data=data)

    async def delete_post(self, tweet_id: str) -> Dict[str, Any]:
        """
        Delete a tweet.

        Args:
            tweet_id: ID of the tweet to delete

        Returns:
            Response confirming deletion

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/tweets/{tweet_id}")

    async def get_user_posts(
        self,
        user_id: str,
        max_results: int = 100,
        pagination_token: Optional[str] = None,
        exclude: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get user's timeline tweets.

        Args:
            user_id: User ID
            max_results: Maximum number of results (5-100)
            pagination_token: Pagination token for next page
            exclude: List of tweet types to exclude (e.g., ['retweets', 'replies'])

        Returns:
            Timeline tweets

        Raises:
            Exception: If request fails
        """
        params = {
            "max_results": max_results,
            "tweet.fields": "created_at,entities,id,in_reply_to_user_id,lang,public_metrics,referenced_tweets,source,text"
        }

        if pagination_token:
            params["pagination_token"] = pagination_token
        if exclude:
            params["exclude"] = ",".join(exclude)

        return await self._request("GET", f"/users/{user_id}/tweets", params=params)

    async def get_mentions(
        self,
        user_id: str,
        max_results: int = 100,
        pagination_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get mentions for a user.

        Args:
            user_id: User ID
            max_results: Maximum number of results (5-100)
            pagination_token: Pagination token for next page

        Returns:
            Mention tweets

        Raises:
            Exception: If request fails
        """
        params = {
            "max_results": max_results,
            "tweet.fields": "created_at,entities,id,in_reply_to_user_id,lang,public_metrics,referenced_tweets,source,text"
        }

        if pagination_token:
            params["pagination_token"] = pagination_token

        return await self._request("GET", f"/users/{user_id}/mentions", params=params)

    # ==================== Webhook Handling ====================

    def handle_webhook(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle webhook events from X.

        Supported events:
        - Tweet created

        Args:
            event_data: Webhook event data

        Returns:
            Processed event data

        Raises:
            Exception: If event data is invalid
        """
        if not event_data or "tweet_create_events" not in event_data:
            raise ValueError("Invalid webhook event data")

        event_data["processed_at"] = datetime.utcnow().isoformat()
        event_data["category"] = "tweet_created"

        return event_data