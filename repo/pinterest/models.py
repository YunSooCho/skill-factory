"""
 Pinterest API Models
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Pin:
    """Pinterest Pin model"""

    id: str
    link: Optional[str]
    title: Optional[str]
    description: Optional[str]
    dominant_color: Optional[str]
    alt_text: Optional[str]
    board_id: str
    board_section_id: Optional[str]
    board_url: Optional[str]
    created_at: Optional[str]
    media: Optional[dict]
    media_source: Optional[dict]
    parent_pin_id: Optional[str]
    note: Optional[str]
    url: Optional[str]

    @classmethod
    def from_api_response(cls, data: dict) -> "Pin":
        """Create Pin from API response"""
        return cls(
            id=data.get("id"),
            link=data.get("link"),
            title=data.get("title"),
            description=data.get("description"),
            dominant_color=data.get("dominant_color"),
            alt_text=data.get("alt_text"),
            board_id=data.get("board_id"),
            board_section_id=data.get("board_section_id"),
            board_url=data.get("board_url"),
            created_at=data.get("created_at"),
            media=data.get("media"),
            media_source=data.get("media_source"),
            parent_pin_id=data.get("parent_pin_id"),
            note=data.get("note"),
            url=data.get("url"),
        )


@dataclass
class Board:
    """Pinterest Board model"""

    id: str
    name: str
    description: Optional[str]
    owner: Optional[dict]
    privacy: Optional[str]
    created_at: Optional[str]
    counts: Optional[dict]
    image_cover_url: Optional[str]
    image_cover_thumbnail_url: Optional[str]
    pins: Optional[List[dict]]

    @classmethod
    def from_api_response(cls, data: dict) -> "Board":
        """Create Board from API response"""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            owner=data.get("owner"),
            privacy=data.get("privacy"),
            created_at=data.get("created_at"),
            counts=data.get("counts"),
            image_cover_url=data.get("image_cover_url"),
            image_cover_thumbnail_url=data.get("image_cover_thumbnail_url"),
            pins=data.get("pins"),
        )


@dataclass
class PinListResponse:
    """Paginated Pin list response"""

    items: List[Pin]
    bookmark: Optional[str] = None
    has_next: bool = False

    @classmethod
    def from_api_response(cls, data: dict) -> "PinListResponse":
        """Create PinListResponse from API response"""
        items = [Pin.from_api_response(item) for item in data.get("items", [])]
        return cls(
            items=items,
            bookmark=data.get("bookmark"),
            has_next=bool(data.get("bookmark")),
        )


@dataclass
class BoardListResponse:
    """Paginated Board list response"""

    items: List[Board]
    bookmark: Optional[str] = None
    has_next: bool = False

    @classmethod
    def from_api_response(cls, data: dict) -> "BoardListResponse":
        """Create BoardListResponse from API response"""
        items = [Board.from_api_response(item) for item in data.get("items", [])]
        return cls(
            items=items,
            bookmark=data.get("bookmark"),
            has_next=bool(data.get("bookmark")),
        )


@dataclass
class WebhookEvent:
    """Pinterest Webhook event model"""

    event_id: str
    event_type: str
    event_data: dict
    timestamp: str

    @classmethod
    def from_webhook(cls, data: dict) -> "WebhookEvent":
        """Create WebhookEvent from webhook payload"""
        return cls(
            event_id=data.get("event_id", ""),
            event_type=data.get("event_type", ""),
            event_data=data.get("event_data", {}),
            timestamp=data.get("event_time", ""),
        )