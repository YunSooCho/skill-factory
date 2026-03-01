"""
Coda API - Document Collaboration Platform Client

Supports:
- Delete Row
- Add Row
- Get Row
- Create Page
- Add Permission
- Update Row
- Search Row
Plus webhooks for: Row Created, Row Updated
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import json


@dataclass
class Row:
    """Coda table row"""
    id: str
    cells: Dict[str, Any]
    created_at: str
    updated_at: str


@dataclass
class Page:
    """Coda page"""
    id: str
    name: str
    title: str
    browser_link: str
    created_at: str
    updated_at: str


@dataclass
class Permission:
    """Coda permission"""
    type: str
    access: str
    email: Optional[str]
    group_id: Optional[str]


@dataclass
class RowResponse:
    """Row operation response"""
    success: bool
    row: Optional[Row]
    message: str


@dataclass
class PageResponse:
    """Page operation response"""
    success: bool
    page: Optional[Page]
    message: str


@dataclass
class PermissionResponse:
    """Permission operation response"""
    success: bool
    message: str


@dataclass
class SearchResponse:
    """Search results response"""
    results: List[Row]
    total: int
    query: str


class CodaAPIClient:
    """
    Coda API client for document collaboration.

    API Documentation: https://coda.io/developers/apis/
    """

    BASE_URL = "https://coda.io/apis/v1"

    def __init__(self, api_token: str):
        """
        Initialize Coda API client.

        Args:
            api_token: Coda API token from coda.io/account
        """
        self.api_token = api_token
        self.session = None

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self._get_headers())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def delete_row(
        self,
        doc_id: str,
        table_id: str,
        row_id: str
    ) -> RowResponse:
        """
        Delete a row from a table.

        Args:
            doc_id: Document ID
            table_id: Table ID
            row_id: Row ID to delete

        Returns:
            RowResponse with operation result

        Raises:
            ValueError: If required IDs are missing
            aiohttp.ClientError: If request fails
        """
        if not all([doc_id, table_id, row_id]):
            raise ValueError("doc_id, table_id, and row_id are required")

        url = f"{self.BASE_URL}/docs/{doc_id}/tables/{table_id}/rows/{row_id}"

        async with self.session.delete(url) as response:
            if response.status == 204:
                return RowResponse(success=True, row=None, message="Row deleted successfully")
            else:
                data = await response.json()
                error_msg = data.get("message", str(data))
                return RowResponse(success=False, row=None, message=error_msg)

    async def add_row(
        self,
        doc_id: str,
        table_id: str,
        cells: Dict[str, Any],
        key_columns: Optional[List[str]] = None
    ) -> RowResponse:
        """
        Add a row to a table.

        Args:
            doc_id: Document ID
            table_id: Table ID
            cells: Dictionary of column values
            key_columns: Optional list of key columns for upsert

        Returns:
            RowResponse with created row

        Raises:
            ValueError: If required IDs or cells are missing
            aiohttp.ClientError: If request fails
        """
        if not doc_id or not table_id:
            raise ValueError("doc_id and table_id are required")
        if not cells:
            raise ValueError("cells cannot be empty")

        url = f"{self.BASE_URL}/docs/{doc_id}/tables/{table_id}/rows"

        payload = {"rows": [{"cells": cells}]}

        if key_columns:
            payload["keyColumns"] = key_columns

        async with self.session.post(url, json=payload) as response:
            data = await response.json()

            if response.status in [200, 201]:
                row_data = data.get("items", [{}])[0] if data.get("items") else {}
                row = Row(
                    id=row_data.get("id", ""),
                    cells=row_data.get("cells", {}),
                    created_at=row_data.get("createdAt", ""),
                    updated_at=row_data.get("updatedAt", "")
                )
                return RowResponse(success=True, row=row, message="Row created successfully")
            else:
                error_msg = data.get("message", str(data))
                return RowResponse(success=False, row=None, message=error_msg)

    async def get_row(
        self,
        doc_id: str,
        table_id: str,
        row_id: str,
        use_column_names: bool = False
    ) -> RowResponse:
        """
        Get a specific row from a table.

        Args:
            doc_id: Document ID
            table_id: Table ID
            row_id: Row ID
            use_column_names: Use column names instead of IDs (default: False)

        Returns:
            RowResponse with row data

        Raises:
            ValueError: If required IDs are missing
            aiohttp.ClientError: If request fails
        """
        if not all([doc_id, table_id, row_id]):
            raise ValueError("doc_id, table_id, and row_id are required")

        params = {"useColumnNames": str(use_column_names).lower()}
        url = f"{self.BASE_URL}/docs/{doc_id}/tables/{table_id}/rows/{row_id}"

        async with self.session.get(url, params=params) as response:
            data = await response.json()

            if response.status == 200:
                row_data = data
                row = Row(
                    id=row_data.get("id", ""),
                    cells=row_data.get("cells", {}),
                    created_at=row_data.get("createdAt", ""),
                    updated_at=row_data.get("updatedAt", "")
                )
                return RowResponse(success=True, row=row, message="Row retrieved successfully")
            else:
                error_msg = data.get("message", str(data))
                return RowResponse(success=False, row=None, message=error_msg)

    async def create_page(
        self,
        doc_id: str,
        title: str,
        parent_id: Optional[str] = None,
        predecessor_id: Optional[str] = None
    ) -> PageResponse:
        """
        Create a new page in a document.

        Args:
            doc_id: Document ID
            title: Page title
            parent_id: Optional parent page ID
            predecessor_id: Optional predecessor page ID (for ordering)

        Returns:
            PageResponse with created page

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If request fails
        """
        if not doc_id:
            raise ValueError("doc_id is required")
        if not title:
            raise ValueError("title is required")

        url = f"{self.BASE_URL}/docs/{doc_id}/pages"

        payload = {"title": title}

        if parent_id:
            payload["parent"] = {"id": parent_id, "type": "page"}
        if predecessor_id:
            payload["predecessor"] = {"id": predecessor_id, "type": "page"}

        async with self.session.post(url, json=payload) as response:
            data = await response.json()

            if response.status in [200, 201]:
                page_data = data
                page = Page(
                    id=page_data.get("id", ""),
                    name=page_data.get("name", ""),
                    title=page_data.get("title", ""),
                    browser_link=page_data.get("browserLink", ""),
                    created_at=page_data.get("createdAt", ""),
                    updated_at=page_data.get("updatedAt", "")
                )
                return PageResponse(success=True, page=page, message="Page created successfully")
            else:
                error_msg = data.get("message", str(data))
                return PageResponse(success=False, page=None, message=error_msg)

    async def add_permission(
        self,
        doc_id: str,
        permission_type: str,
        access_level: str,
        email: Optional[str] = None,
        group_id: Optional[str] = None
    ) -> PermissionResponse:
        """
        Add a permission to a document.

        Args:
            doc_id: Document ID
            permission_type: Type ('user', 'group')
            access_level: Access level ('read', 'write', 'admin', 'edit')
            email: User email (for user type)
            group_id: Group ID (for group type)

        Returns:
            PermissionResponse with operation result

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If request fails
        """
        if not doc_id:
            raise ValueError("doc_id is required")
        if not permission_type:
            raise ValueError("permission_type is required")
        if not access_level:
            raise ValueError("access_level is required")
        if permission_type == "user" and not email:
            raise ValueError("email is required for user permission")
        if permission_type == "group" and not group_id:
            raise ValueError("group_id is required for group permission")

        url = f"{self.BASE_URL}/docs/{doc_id}/acl/list"

        payload = {"acl": []}

        if permission_type == "user":
            payload["acl"].append({
                "type": "user",
                "email": email,
                "permission": access_level
            })
        elif permission_type == "group":
            payload["acl"].append({
                "type": "group",
                "groupId": group_id,
                "permission": access_level
            })

        async with self.session.post(url, json=payload) as response:
            if response.status in [200, 201]:
                return PermissionResponse(success=True, message="Permission added successfully")
            else:
                data = await response.json()
                error_msg = data.get("message", str(data))
                return PermissionResponse(success=False, message=error_msg)

    async def update_row(
        self,
        doc_id: str,
        table_id: str,
        row_id: str,
        cells: Dict[str, Any],
        key_columns: Optional[List[str]] = None
    ) -> RowResponse:
        """
        Update a row in a table.

        Args:
            doc_id: Document ID
            table_id: Table ID
            row_id: Row ID
            cells: Dictionary of column values to update
            key_columns: Optional list of key columns

        Returns:
            RowResponse with updated row

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If request fails
        """
        if not all([doc_id, table_id, row_id]):
            raise ValueError("doc_id, table_id, and row_id are required")
        if not cells:
            raise ValueError("cells cannot be empty")

        url = f"{self.BASE_URL}/docs/{doc_id}/tables/{table_id}/rows/{row_id}"

        payload = {"cells": cells}

        if key_columns:
            payload["keyColumns"] = key_columns

        async with self.session.patch(url, json=payload) as response:
            data = await response.json()

            if response.status == 200:
                row_data = data
                row = Row(
                    id=row_data.get("id", ""),
                    cells=row_data.get("cells", {}),
                    created_at=row_data.get("createdAt", ""),
                    updated_at=row_data.get("updatedAt", "")
                )
                return RowResponse(success=True, row=row, message="Row updated successfully")
            else:
                error_msg = data.get("message", str(data))
                return RowResponse(success=False, row=None, message=error_msg)

    async def search_row(
        self,
        doc_id: str,
        table_id: str,
        query: str,
        use_column_names: bool = False,
        limit: int = 100
    ) -> SearchResponse:
        """
        Search for rows in a table.

        Args:
            doc_id: Document ID
            table_id: Table ID
            query: Search query string
            use_column_names: Use column names instead of IDs
            limit: Maximum results (default: 100)

        Returns:
            SearchResponse with matching rows

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If request fails
        """
        if not doc_id or not table_id:
            raise ValueError("doc_id and table_id are required")
        if not query:
            raise ValueError("query cannot be empty")

        params = {
            "query": query,
            "useColumnNames": str(use_column_names).lower(),
            "limit": limit
        }

        url = f"{self.BASE_URL}/docs/{doc_id}/tables/{table_id}/rows"

        async with self.session.get(url, params=params) as response:
            data = await response.json()

            if response.status == 200:
                rows = [
                    Row(
                        id=row.get("id", ""),
                        cells=row.get("cells", {}),
                        created_at=row.get("createdAt", ""),
                        updated_at=row.get("updatedAt", "")
                    )
                    for row in data.get("items", [])
                ]

                return SearchResponse(
                    results=rows,
                    total=len(rows),
                    query=query
                )
            else:
                error_msg = data.get("message", str(data))
                raise Exception(f"Coda Search Row error: {error_msg}")

    def verify_webhook(self, payload: Dict[str, Any], signature: str, secret: str) -> bool:
        """
        Verify webhook signature.

        Args:
            payload: Webhook payload
            signature: Signature from webhook headers
            secret: Webhook secret

        Returns:
            bool: True if signature is valid
        """
        import hmac
        import hashlib

        payload_str = json.dumps(payload, separators=(',', ':'), sort_keys=True)
        expected_signature = hmac.new(
            secret.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)

    def parse_webhook_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse webhook event payload.

        Args:
            payload: Webhook payload

        Returns:
            Dict with event details
        """
        event_type = payload.get("type", "")
        event_data = payload.get("data", {})

        result = {
            "event_type": event_type,
            "event_id": payload.get("id", ""),
            "timestamp": payload.get("timestamp", ""),
            "data": event_data
        }

        # Parse specific event types
        if event_type == "doc.rowCreated":
            result["row"] = event_data.get("row", {})
        elif event_type == "doc.rowUpdated":
            result["row"] = event_data.get("row", {})
            result["changes"] = event_data.get("changes", {})

        return result


async def main():
    """Example usage"""
    api_token = "your-api-token-here"

    async with CodaAPIClient(api_token) as client:
        # Add a row
        row_result = await client.add_row(
            doc_id="doc-abc123",
            table_id="table-xyz789",
            cells={
                "Name": "John Doe",
                "Email": "john@example.com",
                "Status": "Active"
            }
        )

        if row_result.success:
            print(f"Row created: {row_result.row.id}")

        # Get a row
        get_result = await client.get_row(
            doc_id="doc-abc123",
            table_id="table-xyz789",
            row_id="row-123",
            use_column_names=True
        )

        if get_result.success:
            print(f"Row data: {get_result.row.cells}")

        # Search rows
        search_result = await client.search_row(
            doc_id="doc-abc123",
            table_id="table-xyz789",
            query="John"
        )

        print(f"Found {search_result.total} rows")

        # Create a page
        page_result = await client.create_page(
            doc_id="doc-abc123",
            title="New Section"
        )

        if page_result.success:
            print(f"Page created: {page_result.page.id}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())