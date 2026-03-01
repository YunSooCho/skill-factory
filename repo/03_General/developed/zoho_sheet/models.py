"""
 Zoho Sheet API Models
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class Cell:
    """Cell model for Zoho Sheet"""

    row_index: int
    column_index: int
    value: Any = None
    formula: Optional[str] = None
    note: Optional[str] = None
    style: Optional[Dict] = None

    @classmethod
    def from_api_response(cls, data: dict) -> "Cell":
        """Create Cell from API response"""
        return cls(
            row_index=int(data.get("row_index", data.get("row", 0))),
            column_index=int(data.get("column_index", data.get("column", 0))),
            value=data.get("value"),
            formula=data.get("formula"),
            note=data.get("note"),
            style=data.get("style"),
        )


@dataclass
class Record:
    """Record model (row) for Zoho Sheet"""

    row_index: int
    cells: List[Any] = field(default_factory=list)
    row_data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api_response(cls, data: dict) -> "Record":
        """Create Record from API response"""
        return cls(
            row_index=int(data.get("row_index", data.get("row", 0))),
            cells=data.get("cells", []) or [],
            row_data=data.get("row_data", data.get("data", {})) or {},
        )


@dataclass
class Worksheet:
    """Worksheet model for Zoho Sheet"""

    worksheet_id: str
    workbook_id: str
    name: str
    row_count: int = 0
    column_count: int = 0
    created_at: Optional[str] = None
    modified_at: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> "Worksheet":
        """Create Worksheet from API response"""
        return cls(
            worksheet_id=data.get("worksheet_id", data.get("id", "")),
            workbook_id=data.get("workbook_id", data.get("workbook", "")),
            name=data.get("name", ""),
            row_count=int(data.get("row_count", 0)),
            column_count=int(data.get("column_count", 0)),
            created_at=data.get("created_time") or data.get("created_at"),
            modified_at=data.get("modified_time") or data.get("modified_at"),
        )


@dataclass
class Workbook:
    """Workbook model for Zoho Sheet"""

    workbook_id: str
    name: str
    owner_name: Optional[str] = None
    owner_email: Optional[str] = None
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    status: str = "active"
    is_trashed: bool = False
    worksheet_count: int = 0

    @classmethod
    def from_api_response(cls, data: dict) -> "Workbook":
        """Create Workbook from API response"""
        return cls(
            workbook_id=data.get("workbook_id", data.get("workbook_id", data.get("id", ""))),
            name=data.get("workbook_name", data.get("name", "")),
            owner_name=data.get("owner_name"),
            owner_email=data.get("owner_email"),
            created_at=data.get("created_time") or data.get("created_at"),
            modified_at=data.get("modified_time") or data.get("modified_at"),
            status=data.get("status", "active"),
            is_trashed=data.get("is_trashed", data.get("deleted", False)),
            worksheet_count=int(data.get("worksheet_count", 0)),
        )


@dataclass
class WorkbookListResponse:
    """Workbook list response"""

    items: List[Workbook]
    total: int = 0

    @classmethod
    def from_api_response(cls, data: dict) -> "WorkbookListResponse":
        """Create WorkbookListResponse from API response"""
        items = []

        if isinstance(data, list):
            items = [Workbook.from_api_response(item) for item in data]
        elif isinstance(data, dict):
            if "workbooks" in data:
                items = [Workbook.from_api_response(item) for item in data["workbooks"]]
            elif "items" in data:
                items = [Workbook.from_api_response(item) for item in data["items"]]
            elif "list" in data:
                items = [Workbook.from_api_response(item) for item in data["list"]]
            elif isinstance(data, dict) and "workbook_id" in data:
                items = [Workbook.from_api_response(data)]

        return cls(
            items=items,
            total=len(items),
        )


@dataclass
class WorksheetListResponse:
    """Worksheet list response"""

    items: List[Worksheet]
    total: int = 0

    @classmethod
    def from_api_response(cls, data: dict) -> "WorksheetListResponse":
        """Create WorksheetListResponse from API response"""
        items = []

        if isinstance(data, list):
            items = [Worksheet.from_api_response(item) for item in data]
        elif isinstance(data, dict):
            if "worksheets" in data:
                items = [Worksheet.from_api_response(item) for item in data["worksheets"]]
            elif "items" in data:
                items = [Worksheet.from_api_response(item) for item in data["items"]]
            elif "list" in data:
                items = [Worksheet.from_api_response(item) for item in data["list"]]
            elif isinstance(data, dict) and "worksheet_id" in data:
                items = [Worksheet.from_api_response(data)]

        return cls(
            items=items,
            total=len(items),
        )


@dataclass
class RecordListResponse:
    """Record list response"""

    items: List[Record]
    total: int = 0
    worksheet_id: str = ""

    @classmethod
    def from_api_response(cls, data: dict) -> "RecordListResponse":
        """Create RecordListResponse from API response"""
        items = []
        worksheet_id = ""

        if isinstance(data, list):
            items = [Record.from_api_response({"row_index": i, "cells": row}) for i, row in enumerate(data)]
        elif isinstance(data, dict):
            worksheet_id = data.get("worksheet_id", data.get("sheet_id", ""))
            if "records" in data:
                items = [Record.from_api_response(item) for item in data["records"]]
            elif "rows" in data:
                items = [Record.from_api_response(item) for item in data["rows"]]
            elif "items" in data:
                items = [Record.from_api_response(item) for item in data["items"]]
            elif "cells" in data:
                # Cell range response
                items = [Record.from_api_response({"cells": data["cells"]})]
            elif isinstance(data, dict):
                items = [Record.from_api_response(data)]

        return cls(
            items=items,
            total=len(items),
            worksheet_id=worksheet_id,
        )