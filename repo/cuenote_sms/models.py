"""Data models for Cuénote SMS."""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class AddressBook:
    """Address book model."""
    id: str
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    member_count: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SMSDelivery:
    """SMS delivery model."""
    id: str
    subject: str
    status: str
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    total_recipients: Optional[int] = None
    successful_count: Optional[int] = None
    failed_count: Optional[int] = None
    message_body: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PhoneNumberRecipient:
    """Phone number recipient."""
    phone_number: str
    name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)