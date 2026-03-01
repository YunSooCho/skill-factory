"""
 Big Mailer API Models
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class ContactField:
    """Custom contact field model"""

    key: str
    name: str
    type: str
    required: bool = False
    options: Optional[List[str]] = None
    default_value: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> "ContactField":
        """Create ContactField from API response"""
        return cls(
            key=data.get("key", ""),
            name=data.get("name", ""),
            type=data.get("type", "text"),
            required=data.get("required", False),
            options=data.get("options"),
            default_value=data.get("default_value"),
        )


@dataclass
class Contact:
    """Contact model"""

    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: str = "active"
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    lists: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> "Contact":
        """Create Contact from API response"""
        return cls(
            id=data.get("id", data.get("contact_id", "")),
            email=data.get("email", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            name=data.get("name"),
            phone=data.get("phone"),
            company=data.get("company"),
            status=data.get("status", "active"),
            custom_fields=data.get("custom_fields", {}) or {},
            tags=data.get("tags", []) or [],
            lists=data.get("lists", []) or [],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
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
            items_data = {"items": data, "total": len(data)}
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
class FieldListResponse:
    """Field list response"""

    items: List[ContactField]
    total: int = 0

    @classmethod
    def from_api_response(cls, data: dict) -> "FieldListResponse":
        """Create FieldListResponse from API response"""
        items = []

        # Handle both array and wrapped response formats
        if isinstance(data, list):
            items_data = data
        elif "items" in data:
            items_data = data["items"]
        elif "fields" in data:
            items_data = data["fields"]
        else:
            items_data = []

        items = [ContactField.from_api_response(item) for item in items_data]

        return cls(
            items=items,
            total=len(items) or int(data.get("total", len(items))),
        )