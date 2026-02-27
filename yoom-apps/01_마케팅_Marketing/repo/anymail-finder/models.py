"""
Anymail Finder Data Models
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Person:
    """Person Model"""
    first_name: str
    last_name: str
    position: Optional[str] = None
    company: Optional[str] = None

@dataclass
class EmailResult:
    """Email Result Model"""
    email: str
    confidence: float
    source: Optional[str] = None

@dataclass
class EmailValidation:
    """Email Validation Model"""
    email: str
    is_deliverable: bool
    is_valid_format: bool
    score: float
    description: Optional[str] = None