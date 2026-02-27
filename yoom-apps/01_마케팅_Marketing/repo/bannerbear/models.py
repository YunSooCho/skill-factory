"""
Bannerbear Data Models
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class ImageDetail:
    """Image Detail Model"""
    uid: str
    status: str
    image_url: Optional[str] = None

@dataclass
class VideoDetail:
    """Video Detail Model"""
    uid: str
    status: str
    video_url: Optional[str] = None

@dataclass
class MovieDetail:
    """Movie Detail Model"""
    uid: str
    status: str
    movie_mp4_url: Optional[str] = None

@dataclass
class ScreenshotDetail:
    """Screenshot Detail Model"""
    uid: str
    status: str
    image_url: Optional[str] = None

@dataclass
class Collection:
    """Collection Model"""
    uid: str
    name: str
    status: str

@dataclass
class FileData:
    """File Data Model"""
    uid: str
    filename: str
    url: str
    mime_type: str
    size: int