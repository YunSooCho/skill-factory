"""
Rd Station API Data Models.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class Lead:
    """Rd Station lead data model."""
    uuid: str
    email: str
    name: Optional[str] = None
    phone: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    website: Optional[str] = None
    linkedin: Optional[str] = None
    custom_attributes: Dict[str, Any] = field(default_factory=dict)
    converted_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Lead":
        """Create Lead from API response."""
        return cls(
            uuid=data.get("uuid", ""),
            email=data.get("email", ""),
            name=data.get("name"),
            phone=data.get("phone"),
            title=data.get("title"),
            company=data.get("company_name"),
            website=data.get("website"),
            linkedin=data.get("linkedin"),
            custom_attributes=data.get("custom_attributes", {}),
            converted_at=data.get("converted_at"),
        )


@dataclass
class Conversion:
    """Rd Station conversion data model."""
    conversion_uuid: str
    event_identifier: str
    lead_email: str
    value: Optional[float] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Conversion":
        """Create Conversion from API response."""
        return cls(
            conversion_uuid=data.get("uuid", ""),
            event_identifier=data.get("event_identifier", ""),
            lead_email=data.get("lead", {}).get("email", ""),
            value=data.get("amount"),
            status=data.get("status"),
            created_at=data.get("created_at"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class LeadList:
    """Rd Station lead list data model."""
    uuid: str
    name: str
    leads_count: int
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LeadList":
        """Create LeadList from API response."""
        return cls(
            uuid=data.get("uuid", ""),
            name=data.get("name", ""),
            leads_count=data.get("leads_count", 0),
            created_at=data.get("created_at"),
        )