"""Data models for DLVR.it."""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Account:
    """Social media account model."""
    id: str
    name: str
    platform: str
    avatar_url: Optional[str] = None
    connected_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Route:
    """Route model (distribution path)."""
    id: str
    name: str
    accounts: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Post:
    """Social media post model."""
    id: str
    content: str
    scheduled_at: Optional[datetime] = None
    posted_at: Optional[datetime] = None
    status: str = "draft"
    metadata: Dict[str, Any] = field(default_factory=dict)