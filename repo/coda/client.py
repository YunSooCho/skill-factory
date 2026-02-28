"""
Coda API Client

This module provides a Python client for interacting with Coda's API.
"""

import requests
from typing import Dict, List, Optional, Any, Iterator
import time


class CodaClient:
    """
    Client for Coda API.

    Coda provides:
    - Documents as databases
    - Tables with formulas
    - Buttons and automation
    - Real-time collaboration
    - Flexible data structures
    """

    def __init__(
        self,
        api_token: str,
        base_url: str = "https://coda.io/apis/v1",
        timeout: int = 30
    ):
        """Initialize the Coda client."""
        self.api_token = api_token
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        params=None,
        data=None
    ) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(
            method,
            url,
            params=params,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def list_docs(
        self,
        query: Optional[str] = None,
        limit: int = 100,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """List documents."""
        params = {'limit': limit}
        if query:
            params['query'] = query
        if page_token:
            params['pageToken'] = page_token
        return self._request('GET', '/docs', params=params)

    def get_doc(self, doc_id: str) -> Dict[str, Any]:
        """Get document details."""
        return self._request('GET', f'/docs/{doc_id}')

    def create_doc(
        self,
        title: str,
        folder_id: Optional[str] = None,
        source_doc_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new document."""
        data = {'title': title}
        if folder_id:
            data['folderId'] = folder_id
        if source_doc_id:
            data['sourceDocId'] = source_doc_id
        return self._request('POST', '/docs', data=data)

    def update_doc(
        self,
        doc_id: str,
        title: Optional[str] = None,
        folder_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update document."""
        data = {}
        if title:
            data['title'] = title
        if folder_id:
            data['folderId'] = folder_id
        return self._request('PUT', f'/docs/{doc_id}', data=data)

    def delete_doc(self, doc_id: str) -> None:
        """Delete document."""
        self._request('DELETE', f'/docs/{doc_id}')

    def list_tables(self, doc_id: str) -> List[Dict[str, Any]]:
        """List tables in a document."""
        result = self._request('GET', f'/docs/{doc_id}/tables')
        return result.get('items', [])

    def get_table(self, doc_id: str, table_id: str) -> Dict[str, Any]:
        """Get table details."""
        return self._request('GET', f'/docs/{doc_id}/tables/{table_id}')

    def get_table_schema(self, doc_id: str, table_id: str) -> Dict[str, Any]:
        """Get table schema."""
        return self._request('GET', f'/docs/{doc_id}/tables/{table_id}/schema')

    def list_rows(
        self,
        doc_id: str,
        table_id: str,
        limit: int = 100,
        query: Optional[str] = None,
        sort_by: Optional[str] = None,
        visible_only: bool = None,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """List rows in a table."""
        params = {'limit': limit}
        if query:
            params['query'] = query
        if sort_by:
            params['sortBy'] = sort_by
        if visible_only is not None:
            params['visibleOnly'] = visible_only
        if page_token:
            params['pageToken'] = page_token
        return self._request('GET', f'/docs/{doc_id}/tables/{table_id}/rows', params=params)

    def get_row(self, doc_id: str, table_id: str, row_id: str) -> Dict[str, Any]:
        """Get a single row."""
        return self._request('GET', f'/docs/{doc_id}/tables/{table_id}/rows/{row_id}')

    def create_row(
        self,
        doc_id: str,
        table_id: str,
        cells: Optional[List[Dict[str, Any]]] = None,
        key_column: Optional[str] = None,
        rows: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Create a new row."""
        data = {}
        if cells:
            data['cells'] = cells
        if key_column:
            data['keyColumn'] = key_column
        if rows:
            data['rows'] = rows
        return self._request('POST', f'/docs/{doc_id}/tables/{table_id}/rows', data=data)

    def update_row(
        self,
        doc_id: str,
        table_id: str,
        row_id: str,
        cells: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Update a row."""
        data = {'cells': cells}
        return self._request('PUT', f'/docs/{doc_id}/tables/{table_id}/rows/{row_id}', data=data)

    def delete_row(self, doc_id: str, table_id: str, row_id: str) -> None:
        """Delete a row."""
        self._request('DELETE', f'/docs/{doc_id}/tables/{table_id}/rows/{row_id}')

    def batch_create_rows(
        self,
        doc_id: str,
        table_id: str,
        rows: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create multiple rows."""
        data = {'rows': rows}
        return self._request('POST', f'/docs/{doc_id}/tables/{table_id}/rows', data=data)

    def batch_update_rows(
        self,
        doc_id: str,
        table_id: str,
        updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Update multiple rows."""
        data = {'rows': updates}
        return self._request('PUT', f'/docs/{doc_id}/tables/{table_id}/rows', data=data)

    def batch_delete_rows(
        self,
        doc_id: str,
        table_id: str,
        row_ids: List[str]
    ) -> Dict[str, Any]:
        """Delete multiple rows."""
        data = {'rowIds': row_ids}
        return self._request('POST', f'/docs/{doc_id}/tables/{table_id}/rows/delete', data=data)

    def list_columns(
        self,
        doc_id: str,
        table_id: str
    ) -> List[Dict[str, Any]]:
        """List columns in a table."""
        result = self._request('GET', f'/docs/{doc_id}/tables/{table_id}/columns')
        return result.get('items', [])

    def get_column(
        self,
        doc_id: str,
        table_id: str,
        column_id: str
    ) -> Dict[str, Any]:
        """Get column details."""
        return self._request('GET', f'/docs/{doc_id}/tables/{table_id}/columns/{column_id}')

    def create_column(
        self,
        doc_id: str,
        table_id: str,
        name: str,
        type: str = "text",
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new column."""
        data = {
            'name': name,
            'type': type
        }
        if options:
            data['options'] = options
        return self._request('POST', f'/docs/{doc_id}/tables/{table_id}/columns', data=data)

    def update_column(
        self,
        doc_id: str,
        table_id: str,
        column_id: str,
        name: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update a column."""
        data = {}
        if name:
            data['name'] = name
        if options:
            data['options'] = options
        return self._request('PUT', f'/docs/{doc_id}/tables/{table_id}/columns/{column_id}', data=data)

    def delete_column(
        self,
        doc_id: str,
        table_id: str,
        column_id: str
    ) -> None:
        """Delete a column."""
        self._request('DELETE', f'/docs/{doc_id}/tables/{table_id}/columns/{column_id}')

    def list_pages(self, doc_id: str) -> List[Dict[str, Any]]:
        """List pages in a document."""
        result = self._request('GET', f'/docs/{doc_id}/pages')
        return result.get('items', [])

    def get_page(self, doc_id: str, page_id: str) -> Dict[str, Any]:
        """Get page details."""
        return self._request('GET', f'/docs/{doc_id}/pages/{page_id}')

    def publish_doc(
        self,
        doc_id: str,
        share_link_expiration: Optional[str] = None,
        folder_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Publish a document."""
        data = {}
        if share_link_expiration:
            data['shareLinkExpiration'] = share_link_expiration
        if folder_id:
            data['folderId'] = folder_id
        return self._request('PUT', f'/docs/{doc_id}/publish', data=data)

    def unpublish_doc(self, doc_id: str) -> None:
        """Unpublish a document."""
        self._request('DELETE', f'/docs/{doc_id}/publish')

    def push_button(
        self,
        doc_id: str,
        table_id: str,
        row_id: str,
        button_id: str
    ) -> Dict[str, Any]:
        """Push/trigger a button."""
        return self._request('POST', f'/docs/{doc_id}/tables/{table_id}/rows/{row_id}/buttons/{button_id}')

    def create_formula(
        self,
        doc_id: str,
        table_id: str,
        name: str,
        formula: str
    ) -> Dict[str, Any]:
        """Create a formula column."""
        return self.create_column(
            doc_id,
            table_id,
            name,
            type="formula",
            options={'formula': formula}
        )

    def create_lookup(
        self,
        doc_id: str,
        table_id: str,
        name: str,
        relationship: str,
        target_column: str
    ) -> Dict[str, Any]:
        """Create a lookup column."""
        return self.create_column(
            doc_id,
            table_id,
            name,
            type="lookup",
            options={
                'relationship': relationship,
                'targetColumn': target_column
            }
        )

    def create_rollup(
        self,
        doc_id: str,
        table_id: str,
        name: str,
        relationship: str,
        aggregation: str
    ) -> Dict[str, Any]:
        """Create a rollup column."""
        return self.create_column(
            doc_id,
            table_id,
            name,
            type="rollup",
            options={
                'relationship': relationship,
                'aggregation': aggregation
            }
        )

    def list_buttons(
        self,
        doc_id: str,
        table_id: str
    ) -> List[Dict[str, Any]]:
        """List buttons in a table."""
        columns = self.list_columns(doc_id, table_id)
        buttons = [col for col in columns if col.get('type') == 'button']
        return buttons

    def search_docs(
        self,
        query: str,
        limit: int = 20
    ) -> Dict[str, Any]:
        """Search documents."""
        return self.list_docs(query=query, limit=limit)

    def get_all_rows(
        self,
        doc_id: str,
        table_id: str,
        max_rows: Optional[int] = None
    ) -> Iterator[Dict[str, Any]]:
        """Get all rows with pagination."""
        page_token = None
        total_rows = 0

        while True:
            result = self.list_rows(doc_id, table_id, page_token=page_token)
            rows = result.get('items', [])

            for row in rows:
                if max_rows and total_rows >= max_rows:
                    return
                yield row
                total_rows += 1

            page_token = result.get('nextPageToken')
            if not page_token:
                break

    def import_csv(
        self,
        doc_id: str,
        table_id: str,
        data: str,
        import_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Import CSV data to a table."""
        data_payload = {
            'data': data,
            'format': 'csv'
        }
        if import_options:
            data_payload['importOptions'] = import_options
        return self._request('POST', f'/docs/{doc_id}/tables/{table_id}/import', data=data_payload)

    def list_views(
        self,
        doc_id: str,
        table_id: str
    ) -> List[Dict[str, Any]]:
        """List views for a table."""
        result = self._request('GET', f'/docs/{doc_id}/tables/{table_id}/views')
        return result.get('items', [])

    def get_view(
        self,
        doc_id: str,
        table_id: str,
        view_id: str
    ) -> Dict[str, Any]:
        """Get view details."""
        return self._request('GET', f'/docs/{doc_id}/tables/{table_id}/views/{view_id}')

    def get_view_rows(
        self,
        doc_id: str,
        table_id: str,
        view_id: str,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get rows filtered by a view."""
        return self.list_rows(
            doc_id,
            table_id,
            limit=limit,
            query=f'view:"{view_id}"'
        )