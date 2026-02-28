"""
YouTube Data API Data Models.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Video:
    """YouTube video data model."""
    video_id: str
    title: str
    description: str
    channel_id: str
    channel_title: str
    published_at: str
    thumbnail_url: Optional[str] = None
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    duration: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Video":
        """Create Video from API response."""
        snippet = data.get("snippet", {})
        statistics = data.get("statistics", {})

        # Get best thumbnail
        thumbnails = snippet.get("thumbnails", {})
        thumbnail_url = (
            thumbnails.get("maxres", {}).get("url") or
            thumbnails.get("standard", {}).get("url") or
            thumbnails.get("high", {}).get("url") or
            thumbnails.get("default", {}).get("url")
        )

        return cls(
            video_id=data.get("id", ""),
            title=snippet.get("title", ""),
            description=snippet.get("description", ""),
            channel_id=snippet.get("channelId", ""),
            channel_title=snippet.get("channelTitle", ""),
            published_at=snippet.get("publishedAt", ""),
            thumbnail_url=thumbnail_url,
            view_count=int(statistics.get("viewCount", 0)),
            like_count=int(statistics.get("likeCount", 0)),
            comment_count=int(statistics.get("commentCount", 0)),
            duration=data.get("contentDetails", {}).get("duration"),
            tags=snippet.get("tags", []),
        )


@dataclass
class Channel:
    """YouTube channel data model."""
    channel_id: str
    title: str
    description: str
    custom_url: Optional[str] = None
    published_at: Optional[str] = None
    thumbnail_url: Optional[str] = None
    subscriber_count: int = 0
    video_count: int = 0
    view_count: int = 0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Channel":
        """Create Channel from API response."""
        snippet = data.get("snippet", {})
        statistics = data.get("statistics", {})

        # Get best thumbnail
        thumbnails = snippet.get("thumbnails", {})
        thumbnail_url = (
            thumbnails.get("default", {}).get("url") or
            thumbnails.get("medium", {}).get("url") or
            thumbnails.get("high", {}).get("url")
        )

        return cls(
            channel_id=data.get("id", ""),
            title=snippet.get("title", ""),
            description=snippet.get("description", ""),
            custom_url=snippet.get("customUrl"),
            published_at=snippet.get("publishedAt"),
            thumbnail_url=thumbnail_url,
            subscriber_count=int(statistics.get("subscriberCount", 0)),
            video_count=int(statistics.get("videoCount", 0)),
            view_count=int(statistics.get("viewCount", 0)),
        )


@dataclass
class AnalyticsReport:
    """YouTube analytics report data model."""
    rows: List[List[Any]]
    column_headers: List[Dict[str, str]]
    total_results: int = 0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AnalyticsReport":
        """Create AnalyticsReport from API response."""
        headers = data.get("columnHeaders", [])
        rows = data.get("rows", [])

        return cls(
            rows=rows,
            column_headers=headers,
            total_results=len(rows),
        )


@dataclass
class VideoSearchResult:
    """YouTube search result data model."""
    video_id: str
    title: str
    description: str
    channel_id: str
    channel_title: str
    published_at: str
    thumbnail_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VideoSearchResult":
        """Create VideoSearchResult from API response."""
        snippet = data.get("snippet", {})
        id_obj = data.get("id", {})

        # Get best thumbnail
        thumbnails = snippet.get("thumbnails", {})
        thumbnail_url = (
            thumbnails.get("high", {}).get("url") or
            thumbnails.get("medium", {}).get("url") or
            thumbnails.get("default", {}).get("url")
        )

        return cls(
            video_id=id_obj.get("videoId", ""),
            title=snippet.get("title", ""),
            description=snippet.get("description", ""),
            channel_id=snippet.get("channelId", ""),
            channel_title=snippet.get("channelTitle", ""),
            published_at=snippet.get("publishedAt", ""),
            thumbnail_url=thumbnail_url,
        )