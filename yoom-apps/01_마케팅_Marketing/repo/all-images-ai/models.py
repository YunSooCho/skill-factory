"""
All Images AI Data Models
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class ImageGeneration:
    """Image Generation Model"""
    id: str
    prompt: str
    status: str
    created_at: str
    images: List[str] = field(default_factory=list)
    error_message: Optional[str] = None

@dataclass
class Image:
    """Generated Image Model"""
    id: str
    url: str
    width: int
    height: int
    type: str
    size: int