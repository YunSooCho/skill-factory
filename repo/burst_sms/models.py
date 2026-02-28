"""Data models for BurstSMS."""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Message:
    """SMS message model."""
    message_id: str
    to: str
    from_number: str
    body: str
    status: str
    created_at: Optional[datetime] = None
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    cost: Optional[float] = None
    segments: Optional[int] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SendMessageRequest:
    """Request to send SMS."""
    to: str
    from_number: str
    body: str
    schedule: Optional[str] = None
    reference: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MessageListResponse:
    """Response for message list."""
    messages: List[Message]
    total: int
    page: int
    page_size: int