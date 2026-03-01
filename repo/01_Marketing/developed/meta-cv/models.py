"""Data models for Meta CV."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class ConversionEvent:
    """Conversion event model."""
    event_name: str
    event_time: int
    event_source_url: Optional[str] = None
    user_data: Dict[str, Any] = field(default_factory=dict)
    custom_data: Dict[str, Any] = field(default_factory=dict)
    action_source: str = "website"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversionEventBatch:
    """Batch of conversion events."""
    events: List[ConversionEvent]
    test_event_code: Optional[str] = None
    namespace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)