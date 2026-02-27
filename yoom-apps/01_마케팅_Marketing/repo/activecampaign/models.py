"""
ActiveCampaign Data Models
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Account:
    """Account Model"""
    id: str
    name: str
    account_url: Optional[str] = None
    created_timestamp: Optional[str] = None
    updated_timestamp: Optional[str] = None

@dataclass
class Contact:
    """Contact Model"""
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    created_timestamp: Optional[str] = None
    updated_timestamp: Optional[str] = None

@dataclass
class Deal:
    """Deal Model"""
    id: str
    contact: str
    value: float
    currency: str
    title: str
    status: str
    stage: str
    owner: Optional[str] = None
    created_timestamp: Optional[str] = None
    updated_timestamp: Optional[str] = None

@dataclass
class Automation:
    """Automation Model"""
    id: str
    name: str
    status: str

@dataclass
class List:
    """List Model"""
    id: str
    name: str
    subscription_count: int = 0

@dataclass
class Note:
    """Note Model"""
    id: str
    note: str
    relid: str  # related contact ID
    created_timestamp: str

@dataclass
class ContactScore:
    """Contact Score Model"""
    id: str
    contact: str
    score: int
    created_timestamp: str

@dataclass
class AccountContact:
    """Account-Contact Relationship Model"""
    account: str
    contact: str
    job_title: Optional[str] = None

@dataclass
class ContactField:
    """Contact Field Model"""
    id: str
    title: str
    value_type: str
    field_type: str
    value: Optional[str] = None