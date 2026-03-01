"""Data models for Gender API."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class GenderPrediction:
    """Gender prediction result."""
    gender: str  # "male", "female", or "unknown"
    probability: float
    count: int
    name: str
    country_code: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AccountStats:
    """Account usage statistics."""
    total_requests: int
    remaining_requests: int
    billing_cycle_start: Optional[datetime] = None
    billing_cycle_end: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CountryOrigin:
    """Country of origin for a name."""
    name: str
    country_code: str
    probability: float
    count: int
    metadata: Dict[str, Any] = field(default_factory=dict)