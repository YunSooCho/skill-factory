"""
Data models for service integration.
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class BaseModel:
    """Base data model for all responses."""
    id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**{{k: v for k, v in data.items() if k in cls.__annotations__}})
