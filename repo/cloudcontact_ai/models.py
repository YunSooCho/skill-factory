"""
Data models for CloudContact AI API integration.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Contact:
    """Contact data model for CloudContact AI."""

    id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    external_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Contact":
        """Create Contact from API response dict."""
        return cls(
            id=data.get("id") or data.get("Id"),
            first_name=data.get("first_name") or data.get("FirstName"),
            last_name=data.get("last_name") or data.get("LastName"),
            phone=data.get("phone") or data.get("Phone"),
            email=data.get("email") or data.get("Email"),
            external_id=data.get("external_id") or data.get("ExternalId"),
            created_at=data.get("created_at") or data.get("CreatedAt"),
            updated_at=data.get("updated_at") or data.get("UpdatedAt"),
        )


@dataclass
class SMSMessage:
    """SMS Message data model."""

    id: Optional[str] = None
    message: Optional[str] = None
    to: Optional[str] = None
    status: Optional[str] = None
    campaign_id: Optional[str] = None
    campaign_title: Optional[str] = None
    segments: Optional[int] = None
    total_price: Optional[float] = None
    created_at: Optional[str] = None
    custom_data: Optional[str] = None
    external_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SMSMessage":
        """Create SMSMessage from API response dict."""
        return cls(
            id=data.get("id") or data.get("Id"),
            message=data.get("message") or data.get("Message"),
            to=data.get("to") or data.get("To"),
            status=data.get("message_status") or data.get("MessageStatus") or data.get("status"),
            campaign_id=data.get("campaign_id") or data.get("CampaignId"),
            campaign_title=data.get("campaign_title") or data.get("CampaignTitle"),
            segments=data.get("segments") or data.get("Segments"),
            total_price=data.get("total_price") or data.get("TotalPrice"),
            created_at=data.get("created_at") or data.get("CreatedAt"),
            custom_data=data.get("custom_data") or data.get("CustomData"),
            external_id=data.get("external_id") or data.get("ExternalId"),
        )


@dataclass
class Campaign:
    """Campaign data model."""

    id: Optional[str] = None
    title: Optional[str] = None
    message: Optional[str] = None
    campaign_type: Optional[str] = None
    scheduled_timestamp: Optional[str] = None
    scheduled_timezone: Optional[str] = None
    created_at: Optional[str] = None
    status: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Campaign":
        """Create Campaign from API response dict."""
        return cls(
            id=data.get("id") or data.get("Id"),
            title=data.get("title") or data.get("Title"),
            message=data.get("message") or data.get("Message"),
            campaign_type=data.get("campaign_type") or data.get("CampaignType"),
            scheduled_timestamp=data.get("scheduled_timestamp") or data.get("ScheduledTimestamp"),
            scheduled_timezone=data.get("scheduled_timezone") or data.get("ScheduledTimezone"),
            created_at=data.get("created_at") or data.get("CreatedAt"),
            status=data.get("status") or data.get("Status"),
        )


@dataclass
class ContactSearchResult:
    """Contact search result model."""

    contacts: List[Contact] = field(default_factory=list)
    total_count: int = 0
    page: int = 1
    page_size: int = 50

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactSearchResult":
        """Create ContactSearchResult from API response."""
        contacts = []
        if "contacts" in data:
            contacts = [Contact.from_dict(c) for c in data["contacts"]]
        elif "items" in data:
            contacts = [Contact.from_dict(c) for c in data["items"]]

        return cls(
            contacts=contacts,
            total_count=data.get("total_count") or data.get("totalCount", 0),
            page=data.get("page", 1),
            page_size=data.get("page_size") or data.get("pageSize", 50),
        )