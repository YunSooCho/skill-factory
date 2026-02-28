"""
 RD Station API Models
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class EventType(str, Enum):
    """RD Station event types"""

    CONVERSION = "CONVERSION"
    SALES_NEW_BUSSINESS = "SALES_NEW_BUSINESS"
    SALES_OPPORTUNITY = "SALES_OPPORTUNITY"
    SALES_WON = "SALES_WON"
    MARKETING_QUALIFIED_LEAD = "MARKETING_QUALIFIED_LEAD"
    LIFECYCLE_STAGE = "LIFECYCLE_STAGE"


@dataclass
class Contact:
    """Contact model for RD Station"""

    uuid: str
    email: str
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    personal_phone: Optional[str] = None
    website: Optional[str] = None
    linkedin: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    bio: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    lifecycle_stage: Optional[str] = None
    lead_source: Optional[str] = None
    funnel_stage: Optional[str] = None
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    converted_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> "Contact":
        """Create Contact from API response"""
        return cls(
            uuid=data.get("uuid", data.get("id", "")),
            email=data.get("email", ""),
            name=data.get("name"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            job_title=data.get("job_title"),
            company=data.get("company"),
            phone=data.get("phone"),
            mobile=data.get("mobile", data.get("mobile_phone")),
            personal_phone=data.get("personal_phone"),
            website=data.get("website"),
            linkedin=data.get("linkedin"),
            facebook=data.get("facebook"),
            twitter=data.get("twitter"),
            city=data.get("city"),
            state=data.get("state"),
            country=data.get("country"),
            bio=data.get("bio"),
            tags=data.get("tags", []) or [],
            lifecycle_stage=data.get("lifecycle_stage"),
            lead_source=data.get("lead_source"),
            funnel_stage=data.get("funnel_stage"),
            custom_fields=data.get("custom_fields", {}) or data.get("fields", {}) or {},
            converted_at=data.get("converted_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


@dataclass
class ConversionEvent:
    """Conversion Event model for RD Station"""

    uuid: str
    event_type: str
    event_identifier: str
    channel: str
    funnel_name: Optional[str] = None
    revenue: Optional[float] = None
    currency: str = "USD"
    conversion_at: Optional[str] = None
    client_tracking_id: Optional[str] = None
    lead_uuid: Optional[str] = None
    lead_email: Optional[str] = None
    url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api_response(cls, data: dict) -> "ConversionEvent":
        """Create ConversionEvent from API response"""
        return cls(
            uuid=data.get("uuid", data.get("id", "")),
            event_type=data.get("event_type", data.get("event", "")),
            event_identifier=data.get(
                "event_identifier", data.get("event_identifier_name", "")
            ),
            channel=data.get("channel", ""),
            funnel_name=data.get("funnel_name"),
            revenue=float(data["revenue"]) if data.get("revenue") else None,
            currency=data.get("currency", "USD"),
            conversion_at=data.get("conversion_at", data.get("created_at")),
            client_tracking_id=data.get(
                "client_tracking_id", data.get("client_tracking_id")
            ),
            lead_uuid=data.get("lead_uuid", data.get("lead_id")),
            lead_email=data.get("lead_email", data.get("email")),
            url=data.get("url"),
            metadata=data.get("metadata", {}) or data.get("extra_data", {}) or {},
        )


@dataclass
class ContactListResponse:
    """Paginated Contact list response"""

    items: List[Contact]
    total: int = 0
    page: int = 1
    per_page: int = 25
    total_pages: int = 1

    @classmethod
    def from_api_response(cls, data: dict) -> "ContactListResponse":
        """Create ContactListResponse from API response"""
        items = []
        items_data = data

        # Handle different response formats
        if isinstance(data, list):
            items_data = {"contacts": data, "total": len(data)}
        elif "items" in data:
            items_data = data
        elif "contacts" in data:
            items_data = {"items": data["contacts"], **{k: v for k, v in data.items() if k != "contacts"}}
        elif isinstance(data, dict) and "uuid" in data:
            # Single contact wrapped in list
            items_data = {"items": [data], "total": 1}

        items = [Contact.from_api_response(item) for item in items_data.get("items", items_data if isinstance(items_data, list) else [])]

        return cls(
            items=items,
            total=int(items_data.get("total", len(items))),
            page=int(items_data.get("page", 1)),
            per_page=int(items_data.get("per_page", len(items) or 25)),
            total_pages=int(items_data.get("total_pages", 1)),
        )