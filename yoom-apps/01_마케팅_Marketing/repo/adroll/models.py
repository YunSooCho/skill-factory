"""
AdRoll Data Models
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Segment:
    """AdRoll Segment Model"""
    eid: str
    name: str
    type: str  # 'rule', 'upload', 'api'
    status: str
    advertiser: str
    created_at: str
    updated_at: str
    description: Optional[str] = None
    size: Optional[int] = None  # Number of users in segment
    conversion: Optional[float] = None

@dataclass
class SegmentCreateRequest:
    """Request to create a segment"""
    name: str
    type: str  # 'rule', 'upload', 'api'
    description: Optional[str] = None
    rules: Optional[Dict[str, Any]] = None
    advertiser_eid: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            **{k: v for k, v in self.__dict__.items() if v is not None}
        }