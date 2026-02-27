"""
Abyssale Data Models
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Format:
    """Image/Video Format Model"""
    type: str  # 'image' or 'video'
    width: int
    height: int
    url: Optional[str] = None
    size: Optional[int] = None

@dataclass
class GeneratedContent:
    """Generated Content Model"""
    id: str
    format_uuid: str
    status: str
    url: Optional[str] = None
    error_message: Optional[str] = None
    formats: List[Format] = field(default_factory=list)

@dataclass
class File:
    """File Model"""
    id: str
    name: str
    url: str
    mime_type: str
    size: int
    created_at: str
    thumbnail_url: Optional[str] = None

@dataclass
class GenerationRequest:
    """Generation Request Model"""
    template_uuid: str
    format_uuid: Optional[str] = None
    elements: Optional[Dict[str, Any]] = None
    asynchronous: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            **{k: v for k, v in self.__dict__.items() if v is not None}
        }