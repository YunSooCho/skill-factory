"""
 Zoho Writer API Models
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Document:
    """Document model for Zoho Writer"""

    document_id: str
    name: str
    owner_name: Optional[str] = None
    owner_email: Optional[str] = None
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    last_modified_by: Optional[str] = None
    description: Optional[str] = None
    status: str = "active"
    is_trashed: bool = False
    is_favorite: bool = False
    url: Optional[str] = None
    download_url: Optional[str] = None
    format: Optional[str] = None
    language: str = "en"
    word_count: int = 0
    page_count: int = 0

    @classmethod
    def from_api_response(cls, data: dict) -> "Document":
        """Create Document from API response"""
        return cls(
            document_id=data.get("document_id", data.get("docId", data.get("id", ""))),
            name=data.get("document_name", data.get("name", data.get("docName", ""))),
            owner_name=data.get("owner_name"),
            owner_email=data.get("owner_email"),
            created_at=data.get("created_time") or data.get("createdAt"),
            modified_at=data.get("modified_time") or data.get("modifiedAt"),
            last_modified_by=data.get("last_modified_by"),
            description=data.get("description"),
            status=data.get("status", "active"),
            is_trashed=data.get("is_trashed", data.get("deleted", False)),
            is_favorite=data.get("is_favorite", data.get("favorite", False)),
            url=data.get("url") or data.get("document_url"),
            download_url=data.get("download_url"),
            format=data.get("format", data.get("documentType", "docx")),
            language=data.get("language", "en"),
            word_count=int(data.get("word_count", data.get("wordCount", 0))),
            page_count=int(data.get("page_count", data.get("pageCount", 0))),
        )


@dataclass
class Template:
    """Template model for Zoho Writer"""

    template_id: str
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None
    preview_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    format: str = "docx"

    @classmethod
    def from_api_response(cls, data: dict) -> "Template":
        """Create Template from API response"""
        return cls(
            template_id=data.get("template_id", data.get("templateId", data.get("id", ""))),
            name=data.get("template_name", data.get("name", "")),
            category=data.get("category"),
            description=data.get("description"),
            created_at=data.get("created_time") or data.get("createdAt"),
            preview_url=data.get("preview_url") or data.get("url"),
            thumbnail_url=data.get("thumbnail_url"),
            format=data.get("format", "docx"),
        )


@dataclass
class DocumentMetrics:
    """Document metrics model"""

    document_id: str
    word_count: int = 0
    character_count: int = 0
    character_count_no_spaces: int = 0
    paragraph_count: int = 0
    line_count: int = 0
    page_count: int = 0
    reading_time_minutes: int = 0

    @classmethod
    def from_api_response(cls, data: dict) -> "DocumentMetrics":
        """Create DocumentMetrics from API response"""
        return cls(
            document_id=data.get("document_id", data.get("documentId", data.get("id", ""))),
            word_count=int(data.get("word_count", data.get("wordCount", 0))),
            character_count=int(data.get("character_count", data.get("characterCount", 0))),
            character_count_no_spaces=int(
                data.get("character_count_no_spaces", data.get("characterCountWithoutSpaces", 0))
            ),
            paragraph_count=int(data.get("paragraph_count", data.get("paragraphCount", 0))),
            line_count=int(data.get("line_count", data.get("lineCount", 0))),
            page_count=int(data.get("page_count", data.get("pageCount", 0))),
            reading_time_minutes=int(data.get("reading_time", data.get("readingTime", 0))),
        )


@dataclass
class DocumentListResponse:
    """Document list response"""

    items: List[Document]
    total: int = 0

    @classmethod
    def from_api_response(cls, data: dict) -> "DocumentListResponse":
        """Create DocumentListResponse from API response"""
        items = []

        if isinstance(data, list):
            items = [Document.from_api_response(item) for item in data]
        elif isinstance(data, dict):
            if "documents" in data:
                items = [Document.from_api_response(item) for item in data["documents"]]
            elif "items" in data:
                items = [Document.from_api_response(item) for item in data["items"]]
            elif "list" in data:
                items = [Document.from_api_response(item) for item in data["list"]]
            elif isinstance(data, dict) and "document_id" in data:
                items = [Document.from_api_response(data)]

        return cls(
            items=items,
            total=len(items),
        )


@dataclass
class TemplateListResponse:
    """Template list response"""

    items: List[Template]
    total: int = 0

    @classmethod
    def from_api_response(cls, data: dict) -> "TemplateListResponse":
        """Create TemplateListResponse from API response"""
        items = []

        if isinstance(data, list):
            items = [Template.from_api_response(item) for item in data]
        elif isinstance(data, dict):
            if "templates" in data:
                items = [Template.from_api_response(item) for item in data["templates"]]
            elif "items" in data:
                items = [Template.from_api_response(item) for item in data["items"]]
            elif "list" in data:
                items = [Template.from_api_response(item) for item in data["list"]]
            elif isinstance(data, dict) and "template_id" in data:
                items = [Template.from_api_response(data)]

        return cls(
            items=items,
            total=len(items),
        )


@dataclass
class WebhookEvent:
    """Webhook event model for Zoho Writer"""

    event_id: str
    event_type: str
    document_id: str
    document_name: str
    trigger_time: str
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_webhook(cls, data: dict) -> "WebhookEvent":
        """Create WebhookEvent from webhook payload"""
        return cls(
            event_id=data.get("event_id", data.get("id", "")),
            event_type=data.get("event_type", data.get("type", "")),
            document_id=data.get("document_id", data.get("docId", "")),
            document_name=data.get("document_name", data.get("docName", "")),
            trigger_time=data.get("timestamp") or data.get("time"),
            data=data.get("data", {}) or {},
        )