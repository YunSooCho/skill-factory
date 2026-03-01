"""
 Elastic Email API Models
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class Contact:
    """Contact model for Elastic Email"""

    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    status: str = "active"
    lists: List[str] = field(default_factory=list)
    fields: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> "Contact":
        """Create Contact from API response"""
        # Handle different response formats
        email = data.get("email", "")
        contact_id = data.get("id", "")

        return cls(
            id=contact_id,
            email=email,
            first_name=data.get("firstName") or data.get("first_name"),
            last_name=data.get("lastName") or data.get("last_name"),
            name=data.get("name"),
            status=data.get("status", "active"),
            lists=data.get("lists", []) or data.get("listNames", []) or [],
            fields=data.get("fields", {}) or data.get("customFields", {}) or {},
            created_at=data.get("created_at") or data.get("created"),
            updated_at=data.get("updated_at") or data.get("updated"),
        )


@dataclass
class EmailList:
    """Email List model for Elastic Email"""

    id: str
    name: str
    description: Optional[str] = None
    status: str = "active"
    contact_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> "EmailList":
        """Create EmailList from API response"""
        return cls(
            id=data.get("id", data.get("publicListID", "")),
            name=data.get("name", ""),
            description=data.get("description"),
            status=data.get("status", "active"),
            contact_count=int(data.get("contactCount") or data.get("subscriber_count") or 0),
            created_at=data.get("created_at") or data.get("created"),
            updated_at=data.get("updated_at") or data.get("updated"),
        )


@dataclass
class ContactListResponse:
    """Paginated Contact list response"""

    items: List[Contact]
    total: int = 0
    page: int = 1
    limit: int = 25

    @classmethod
    def from_api_response(cls, data: List[Dict] or Dict) -> "ContactListResponse":
        """Create ContactListResponse from API response"""
        items = []

        if isinstance(data, list):
            items = [Contact.from_api_response(item) for item in data]
            total = len(items)
            page = 1
            limit = len(items)
        elif isinstance(data, dict):
            if "data" in data:
                items = [Contact.from_api_response(item) for item in data["data"]]
                total = int(data.get("total", len(items)))
                page = int(data.get("page", 1))
                limit = int(data.get("limit", len(items) or 25))
            elif "contacts" in data:
                items = [Contact.from_api_response(item) for item in data["contacts"]]
                total = int(data.get("total", len(items)))
                page = int(data.get("page", 1))
                limit = int(data.get("limit", len(items) or 25))
            else:
                # Single contact returned
                items = [Contact.from_api_response(data)]
                total = len(items)
                page = 1
                limit = len(items)
        else:
            return cls(items=[])

        return cls(
            items=items,
            total=total,
            page=page,
            limit=limit,
        )


@dataclass
class EmailListListResponse:
    """Email List list response"""

    items: List[EmailList]
    total: int = 0

    @classmethod
    def from_api_response(cls, data: List[Dict] or Dict) -> "EmailListListResponse":
        """Create EmailListListResponse from API response"""
        items = []

        if isinstance(data, list):
            items = [EmailList.from_api_response(item) for item in data]
            total = len(items)
        elif isinstance(data, dict):
            if "data" in data:
                items = [EmailList.from_api_response(item) for item in data["data"]]
                total = int(data.get("total", len(items)))
            elif "lists" in data:
                items = [EmailList.from_api_response(item) for item in data["lists"]]
                total = int(data.get("total", len(items)))
            else:
                # Single list returned
                items = [EmailList.from_api_response(data)]
                total = len(items)
        else:
            return cls(items=[])

        return cls(
            items=items,
            total=total,
        )