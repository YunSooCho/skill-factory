"""
Buffer API Client

Supports:
- Create Update
- Get Updates
- Update Post
- Delete Post
- Get Profiles
- Schedule Post
- Get Analytics
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Profile:
    """Social media profile"""
    id: Optional[str] = None
    service: Optional[str] = None
    type: Optional[str] = None
    service_username: Optional[str] = None
    avatar_url: Optional[str] = None
    formatted_username: Optional[str] = None
    connected: bool = True


@dataclass
class Update:
    """Social media update/post"""
    id: Optional[str] = None
    text: Optional[str] = None
    media: List[Dict[str, Any]] = None
    profile_id: Optional[str] = None
    profile_service: Optional[str] = None
    scheduled_at: Optional[str] = None
    sent_at: Optional[str] = None
    status: Optional[str] = None
    statistics: Dict[str, int] = None

    def __post_init__(self):
        if self.media is None:
            self.media = []
        if self.statistics is None:
            self.statistics = {}


@dataclass
class UpdateAnalytics:
    """Update analytics data"""
    update_id: Optional[str] = None
    likes: int = 0
    shares: int = 0
    comments: int = 0
    clicks: int = 0
    reach: int = 0
    impressions: int = 0


class BufferClient:
    """
    Buffer API client for social media management and scheduling.

    Authentication: API Token (Header: Authorization: Bearer {api_token})
    Base URL: https://api.bufferapp.com/v2
    """

    BASE_URL = "https://api.bufferapp.com/v2"

    def __init__(self, api_token: str):
        """
        Initialize Buffer client.

        Args:
            api_token: Buffer API token
        """
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling and rate limiting"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201, 202, 204):
                if response.status_code == 204:
                    return {}
                data = response.json()
                return data
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid API token")
            elif response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Please retry later.")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Profiles ====================

    def get_profiles(self) -> List[Profile]:
        """
        Get all connected social media profiles.

        Returns:
            List of Profile objects
        """
        result = self._request("GET", "/profiles")
        return [self._parse_profile(p) for p in result.get("profiles", [])]

    # ==================== Updates/Posts ====================

    def create_update(
        self,
        text: str,
        profile_ids: List[str],
        media: Optional[List[Dict[str, Any]]] = None,
        scheduled_at: Optional[str] = None,
        now: bool = False
    ) -> Update:
        """
        Create a new social media update/post.

        Args:
            text: Post text content
            profile_ids: List of profile IDs to post to
            media: Media attachments (photos, videos)
            scheduled_at: Scheduled datetime (ISO format)
            now: Post immediately

        Returns:
            Update object
        """
        if not text:
            raise ValueError("Post text is required")
        if not profile_ids:
            raise ValueError("At least one profile ID is required")

        payload: Dict[str, Any] = {
            "text": text,
            "profile_ids": profile_ids
        }

        if media:
            payload["media"] = media
        if scheduled_at:
            payload["scheduled_at"] = scheduled_at
        if now:
            payload["now"] = True

        result = self._request("POST", "/updates/create", json=payload)
        return self._parse_update(result.get("updates", [{}])[0] if result.get("updates") else result)

    def get_updates(
        self,
        profile_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20
    ) -> List[Update]:
        """
        Get updates (posts) for profiles.

        Args:
            profile_id: Filter by profile ID
            status: Filter by status (pending, sent, etc.)
            limit: Number of results

        Returns:
            List of Update objects
        """
        params: Dict[str, Any] = {"limit": limit}

        if profile_id:
            params["profile_id"] = profile_id
        if status:
            params["status"] = status

        result = self._request("GET", "/profiles/updates", params=params)
        return [self._parse_update(u) for u in result.get("updates", [])]

    def update_post(
        self,
        update_id: str,
        text: Optional[str] = None,
        media: Optional[List[Dict[str, Any]]] = None,
        scheduled_at: Optional[str] = None,
        now: Optional[bool] = None
    ) -> Update:
        """
        Update an existing scheduled post.

        Args:
            update_id: Update ID
            text: Updated post text
            media: Updated media
            scheduled_at: Reschedule datetime
            now: Post immediately instead of scheduled

        Returns:
            Updated Update object
        """
        if not update_id:
            raise ValueError("Update ID is required")

        payload: Dict[str, Any] = {}

        if text:
            payload["text"] = text
        if media:
            payload["media"] = media
        if scheduled_at:
            payload["scheduled_at"] = scheduled_at
        if now is not None:
            payload["now"] = now

        result = self._request("POST", f"/updates/{update_id}/update", json=payload)
        return self._parse_update(result)

    def delete_post(self, update_id: str) -> Dict[str, Any]:
        """
        Delete a scheduled or sent post.

        Args:
            update_id: Update ID

        Returns:
            Deletion response
        """
        if not update_id:
            raise ValueError("Update ID is required")

        return self._request("POST", f"/updates/{update_id}/destroy")

    # ==================== Scheduling ====================

    def schedule_post(
        self,
        text: str,
        profile_ids: List[str],
        schedule_time: str,
        media: Optional[List[Dict[str, Any]]] = None
    ) -> Update:
        """
        Schedule a social media post.

        Args:
            text: Post text
            profile_ids: Profile IDs to post to
            schedule_time: Scheduled datetime (ISO format)
            media: Media attachments

        Returns:
            Scheduled Update object
        """
        return self.create_update(
            text=text,
            profile_ids=profile_ids,
            media=media,
            scheduled_at=schedule_time
        )

    def shuffle_schedules(self, profile_id: str) -> Dict[str, Any]:
        """
        Shuffle the posting schedule for a profile.

        Args:
            profile_id: Profile ID

        Returns:
            Shuffle response
        """
        if not profile_id:
            raise ValueError("Profile ID is required")

        return self._request("POST", f"/profiles/{profile_id}/updates/shuffle")

    # ==================== Analytics ====================

    def get_update_analytics(self, update_id: str) -> UpdateAnalytics:
        """
        Get analytics for a specific update/post.

        Args:
            update_id: Update ID

        Returns:
            UpdateAnalytics object
        """
        if not update_id:
            raise ValueError("Update ID is required")

        result = self._request("GET", f"/updates/{update_id}/analytics")
        return self._parse_analytics(result)

    def get_profile_analytics(self, profile_id: str) -> Dict[str, Any]:
        """
        Get analytics for a profile.

        Args:
            profile_id: Profile ID

        Returns:
            Profile analytics data
        """
        if not profile_id:
            raise ValueError("Profile ID is required")

        return self._request("GET", f"/profiles/{profile_id}/analytics")

    # ==================== Helper Methods ====================

    def _parse_profile(self, data: Dict[str, Any]) -> Profile:
        """Parse profile data from API response"""
        return Profile(
            id=data.get("id"),
            service=data.get("service"),
            type=data.get("service_type"),
            service_username=data.get("service_username"),
            avatar_url=data.get("avatar_https"),
            formatted_username=data.get("formatted_username"),
            connected=data.get("formatted_service_username") is not None
        )

    def _parse_update(self, data: Dict[str, Any]) -> Update:
        """Parse update data from API response"""
        return Update(
            id=data.get("id"),
            text=data.get("text"),
            media=data.get("media", []),
            profile_id=data.get("profile_id"),
            profile_service=data.get("profile_service"),
            scheduled_at=data.get("scheduled_at"),
            sent_at=data.get("sent_at"),
            status=data.get("status"),
            statistics=data.get("statistics", {})
        )

    def _parse_analytics(self, data: Dict[str, Any]) -> UpdateAnalytics:
        """Parse analytics data from API response"""
        return UpdateAnalytics(
            update_id=data.get("id"),
            likes=data.get("likes", 0),
            shares=data.get("shares", 0),
            comments=data.get("comments", 0),
            clicks=data.get("clicks", 0),
            reach=data.get("reach", 0),
            impressions=data.get("impressions", 0)
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_token = "your_buffer_api_token"

    client = BufferClient(api_token=api_token)

    try:
        # Get all profiles
        profiles = client.get_profiles()
        print(f"Profiles: {len(profiles)}")
        for p in profiles:
            print(f"  - {p.service}: {p.formatted_username}")

        if profiles:
            profile_id = profiles[0].id

            # Create a post
            update = client.create_update(
                text="Hello from Buffer API! 🚀 #socialmedia",
                profile_ids=[profile_id],
                media=[],
                now=True
            )
            print(f"\nPost created: {update.id}")
            print(f"Text: {update.text}")
            print(f"Status: {update.status}")

            # Schedule a post
            scheduled = client.schedule_post(
                text="Scheduled post for tomorrow! 📅",
                profile_ids=[profile_id],
                schedule_time="2024-12-31T10:00:00Z"
            )
            print(f"\nPost scheduled: {scheduled.scheduled_at}")

            # Get updates
            updates = client.get_updates(profile_id=profile_id, limit=5)
            print(f"\nRecent updates: {len(updates)}")
            for u in updates:
                print(f"  - {u.text[:50]}... ({u.status})")

            # Get analytics
            if updates:
                analytics = client.get_update_analytics(updates[0].id)
                print(f"\nAnalytics for post {updates[0].id}:")
                print(f"  Likes: {analytics.likes}")
                print(f"  Shares: {analytics.shares}")
                print(f"  Comments: {analytics.comments}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()