"""Data models for OneSignal."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class Subscription:
    """Push subscription model."""
    id: str
    type: str  # "iOSPush", "AndroidPush", "Email", "SMS"
    device_type: Optional[int] = None
    enabled: bool = True
    session_count: Optional[int] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    device_os: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class User:
    """OneSignal user model."""
    id: str
    identifier: Optional[str] = None
    subscription_count: Optional[int] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Message:
    """Push notification message model."""
    id: str
    app_id: str
    contents: Dict[str, str]
    headings: Optional[Dict[str, str]] = None
    data: Optional[Dict[str, Any]] = None
    included_segments: Optional[List[str]] = None
    target_channel: Optional[str] = None
    status: str = "queued"
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)