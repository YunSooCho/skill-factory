"""
Data models for Pinterest API integration.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class PinterestPin:
    """Pinterest Pin data model."""

    id: str
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    board_id: Optional[str] = None
    board_url: Optional[str] = None
    media: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    link: Optional[str] = None
    alt_text: Optional[str] = None
    dominant_color: Optional[str] = None
    note: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PinterestPin":
        """Create PinterestPin from API response dict."""
        return cls(
            id=data.get("id"),
            url=data.get("url"),
            title=data.get("title"),
            description=data.get("description"),
            board_id=data.get("board_id"),
            board_url=data.get("board_url"),
            media=data.get("media"),
            created_at=data.get("created_at"),
            link=data.get("link"),
            alt_text=data.get("alt_text"),
            dominant_color=data.get("dominant_color"),
            note=data.get("note"),
        )


@dataclass
class PinterestBoard:
    """Pinterest Board data model."""

    id: str
    name: str
    url: str
    description: Optional[str] = None
    pin_count: Optional[int] = None
    follower_count: Optional[int] = None
    media: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    privacy: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PinterestBoard":
        """Create PinterestBoard from API response dict."""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            url=data.get("url"),
            description=data.get("description"),
            pin_count=data.get("pin_count"),
            follower_count=data.get("follower_count"),
            media=data.get("media"),
            created_at=data.get("created_at"),
            privacy=data.get("privacy"),
        )


@dataclass
class PinterestPaginatedResponse:
    """Paginated response model."""

    items: List[Any]
    page_size: int
    bookmark: Optional[str] = None

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], item_class: type
    ) -> "PinterestPaginatedResponse":
        """Create paginated response from API response."""
        items = [item_class.from_dict(item) for item in data.get("items", [])]
        return cls(
            items=items,
            page_size=data.get("page_size", 0),
            bookmark=data.get("bookmark"),
        )