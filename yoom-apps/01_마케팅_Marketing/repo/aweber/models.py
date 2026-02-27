"""
AWeber Data Models
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Subscriber:
    """Subscriber Model"""
    id: str
    email: str
    name: Optional[str] = None
    status: str = 'subscribed'
    ad_tracking: Optional[str] = None
    ip_address: Optional[str] = None
    subscription_time: Optional[str] = None

@dataclass
class List:
    """List Model"""
    id: str
    name: str
    description: Optional[str] = None
    total_subscribers: int = 0

@dataclass
class BroadcastOpen:
    """Broadcast Open Model"""
    broadcast_id: str
    opens: int
    unique_opens: int

@dataclass
class BroadcastClick:
    """Broadcast Click Model"""
    broadcast_id: str
    clicks: int
    unique_clicks: int

@dataclass
class BroadcastStatistic:
    """Broadcast Statistic Model"""
    broadcast_id: str
    sent: int
    total_opens: int
    total_clicks: int
    bounces: int
    complaints: int