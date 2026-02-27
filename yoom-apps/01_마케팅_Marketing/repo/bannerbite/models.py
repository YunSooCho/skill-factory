"""
BannerBite Data Models
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Project:
    """Project Model"""
    id: str
    name: str
    status: str
    created_at: str
    updated_at: str

@dataclass
class Bite:
    """Bite Model"""
    id: str
    project_id: str
    name: str
    media_type: str
    status: str
    url: Optional[str] = None

@dataclass
class Media:
    """Media Model"""
    id: str
    type: str
    url: str
    thumbnail_url: Optional[str] = None