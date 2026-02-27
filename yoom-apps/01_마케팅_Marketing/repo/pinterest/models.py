"""
Pinterest Data Models
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class Pin:
    """Pinterest Pin Model"""
    id: str
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    alt_text: Optional[str] = None
    media: Optional[Dict[str, Any]] = None
    board_id: Optional[str] = None
    board_section_id: Optional[str] = None
    created_at: Optional[str] = None
    link: Optional[str] = None
    note: Optional[str] = None
    dominant_color: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Pin':
        return cls(
            id=data.get('id'),
            url=data.get('url'),
            title=data.get('title'),
            description=data.get('description'),
            alt_text=data.get('alt_text'),
            media=data.get('media'),
            board_id=data.get('board_id'),
            board_section_id=data.get('board_section_id'),
            created_at=data.get('created_at'),
            link=data.get('link'),
            note=data.get('note'),
            dominant_color=data.get('dominant_color')
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            **{k: v for k, v in self.__dict__.items() if v is not None}
        }


@dataclass
class Board:
    """Pinterest Board Model"""
    id: str
    name: str
    description: Optional[str] = None
    privacy: Optional[str] = None  # 'public' or 'secret'
    created_at: Optional[str] = None
    counts: Optional[Dict[str, int]] = None
    owner: Optional[str] = None
    image_thumbnail_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Board':
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            privacy=data.get('privacy'),
            created_at=data.get('created_at'),
            counts=data.get('counts'),
            owner=data.get('owner') or (data.get('owner', {}).get('username') if isinstance(data.get('owner'), dict) else None),
            image_thumbnail_url=data.get('image_thumbnail_url')
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            **{k: v for k, v in self.__dict__.items() if v is not None}
        }


@dataclass
class PinCreateRequest:
    """Request to create a pin"""
    board_id: str
    source_url: str
    media_source: Dict[str, Any]
    title: Optional[str] = None
    description: Optional[str] = None
    alt_text: Optional[str] = None
    link: Optional[str] = None
    note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            **{k: v for k, v in self.__dict__.items() if v is not None}
        }


@dataclass
class BoardCreateRequest:
    """Request to create a board"""
    name: str
    description: Optional[str] = None
    privacy: Optional[str] = None  # 'public' or 'secret'

    def to_dict(self) -> Dict[str, Any]:
        return {
            **{k: v for k, v in self.__dict__.items() if v is not None}
        }