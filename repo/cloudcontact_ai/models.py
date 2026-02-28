"""
 CloudContact AI API Models
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class Contact:
    """Contact model"""

    id: str
    phone: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    company: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    opted_in: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> "Contact":
        """Create Contact from API response"""
        return cls(
            id=data.get("id", data.get("contact_id", "")),
            phone=data.get("phone", ""),
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            name=data.get("name"),
            company=data.get("company"),
            tags=data.get("tags", []) or [],
            custom_fields=data.get("custom_fields", {}) or {},
            opted_in=data.get("opted_in", False),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


@dataclass
class SMSMessage:
    """SMS Message model"""

    id: str
    campaign_id: Optional[str]
    phone: str
    message: str
    status: str
    sent_at: Optional[str]
    delivered_at: Optional[str]
    failed_at: Optional[str]
    error_code: Optional[str]
    error_message: Optional[str]
    segments: int = 1

    @classmethod
    def from_api_response(cls, data: dict) -> "SMSMessage":
        """Create SMSMessage from API response"""
        return cls(
            id=data.get("id", data.get("message_id", "")),
            campaign_id=data.get("campaign_id"),
            phone=data.get("phone", ""),
            message=data.get("message", ""),
            status=data.get("status", ""),
            sent_at=data.get("sent_at"),
            delivered_at=data.get("delivered_at"),
            failed_at=data.get("failed_at"),
            error_code=data.get("error_code"),
            error_message=data.get("error_message"),
            segments=data.get("segments", 1),
        )


@dataclass
class Campaign:
    """SMS Campaign model"""

    id: str
    name: str
    message: str
    status: str
    total_recipients: int = 0
    sent_count: int = 0
    delivered_count: int = 0
    failed_count: int = 0
    created_at: Optional[str] = None
    scheduled_at: Optional[str]
    sent_at: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> "Campaign":
        """Create Campaign from API response"""
        return cls(
            id=data.get("id", data.get("campaign_id", "")),
            name=data.get("name", ""),
            message=data.get("message", ""),
            status=data.get("status", ""),
            total_recipients=data.get("total_recipients", 0),
            sent_count=data.get("sent_count", 0),
            delivered_count=data.get("delivered_count", 0),
            failed_count=data.get("failed_count", 0),
            created_at=data.get("created_at"),
            scheduled_at=data.get("scheduled_at"),
            sent_at=data.get("sent_at"),
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

        # Handle both array and paginated response formats
        if isinstance(data, list):
            items_data = {"contacts": data, "total": len(data)}
        elif "items" in data:
            items_data = data
        elif "contacts" in data:
            items_data = {"items": data["contacts"], **{k: v for k, v in data.items() if k != "contacts"}}
        elif isinstance(data, dict) and "id" in data:
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


@dataclass
class SMSListResponse:
    """Paginated SMS list response"""

    items: List[SMSMessage]
    total: int = 0
    page: int = 1
    per_page: int = 25
    total_pages: int = 1

    @classmethod
    def from_api_response(cls, data: dict) -> "SMSListResponse":
        """Create SMSListResponse from API response"""
        items = []
        items_data = data

        # Handle both array and paginated response formats
        if isinstance(data, list):
            items_data = {"messages": data, "total": len(data)}
        elif "items" in data:
            items_data = data
        elif "messages" in data:
            items_data = {"items": data["messages"], **{k: v for k, v in data.items() if k != "messages"}}
        elif isinstance(data, dict) and "id" in data:
            # Single message wrapped in list
            items_data = {"items": [data], "total": 1}

        items = [SMSMessage.from_api_response(item) for item in items_data.get("items", items_data if isinstance(items_data, list) else [])]

        return cls(
            items=items,
            total=int(items_data.get("total", len(items))),
            page=int(items_data.get("page", 1)),
            per_page=int(items_data.get("per_page", len(items) or 25)),
            total_pages=int(items_data.get("total_pages", 1)),
        )