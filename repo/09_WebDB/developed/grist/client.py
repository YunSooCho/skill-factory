"""
Grist API Client

This module provides a Python client for interacting with Grist's spreadsheet-database platform.
"""

import requests
from typing import Dict, List, Optional, Any, Union
import json
from datetime import datetime


class GristClient:
    """
    Client for Grist Spreadsheet-Database Platform.

    Grist provides:
    - Spreadsheet-like interface with database functionality
    - Programmable data models
    - Real-time collaboration
    - RESTful API for data operations
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://docs.getgrist.com/api",
        api_version: str = "v1",
        timeout: int = 30
    ):
        """
        Initialize the Grist client.

        Args:
            api_key: Grist API key
            base_url: Base URL for the Grist API
            api_version: API version
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = f"{base_url}/{api_version}".rstrip('/')
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        params=None,
        data=None,
        json_data=None
    ) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(
            method,
            url,
            params=params,
            data=data,
            json=json_data,
            timeout=self.timeout
        )

        if response.status_code >= 400:
            error_data = response.json() if response.content else {}
            raise Exception(f"API Error {response.status_code}: {error_data}")

        return response.json()

    def list_docs(self) -> List[Dict[str, Any]]:
        """List all accessible documents."""
        return self._request('GET', '/docs')

    def get_doc(self, doc_id: str) -> Dict[str, Any]:
        """Get document details."""
        return self._request('GET', f'/docs/{doc_id}')

    def create_doc(self, name: str, is_workspace: bool = False) -> Dict[str, Any]:
        """
        Create a new document.

        Args:
            name: Document name
            is_workspace: Whether to create as workspace

        Returns:
            Document creation response
        """
        data = {
            'name': name,
            'isWorkspace': is_workspace
        }
        return self._request('POST', '/docs', json_data=data)

    def update_doc(self, doc_id: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Update document details."""
        data = {}
        if name is not None:
            data['name'] = name

        return self._request('PATCH', f'/docs/{doc_id}', json_data=data)

    def delete_doc(self, doc_id: str) -> Dict[str, Any]:
        """Delete a document."""
        return self._request('DELETE', f'/docs/{doc_id}')

    def list_tables(self, doc_id: str) -> List[Dict[str, Any]]:
        """List all tables in a document."""
        return self._request('GET', f'/docs/{doc_id}/tables')

    def get_table(self, doc_id: str, table_id: str) -> Dict[str, Any]:
        """Get table details."""
        return self._request('GET', f'/docs/{doc_id}/tables/{table_id}')

    def get_columns(self, doc_id: str, table_id: str) -> List[Dict[str, Any]]:
        """Get column definitions for a table."""
        return self._request('GET', f'/docs/{doc_id}/tables/{table_id}/columns')

    def list_records(
        self,
        doc_id: str,
        table_id: str,
        filter: Optional[Dict[str, Any]] = None,
        sort: Optional[List[Dict[str, Any]]] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        List records from a table.

        Args:
            doc_id: Document ID
            table_id: Table ID
            filter: Filter conditions
            sort: Sort specifications
            limit: Maximum number of records

        Returns:
            List of records
        """
        params = {}
        if filter is not None:
            params['filter'] = json.dumps(filter)
        if sort is not None:
            params['sort'] = json.dumps(sort)
        if limit is not None:
            params['limit'] = limit

        return self._request('GET', f'/docs/{doc_id}/tables/{table_id}/records', params=params)

    def get_record(self, doc_id: str, table_id: str, record_id: int) -> Dict[str, Any]:
        """Get a specific record."""
        return self._request('GET', f'/docs/{doc_id}/tables/{table_id}/records/{record_id}')

    def create_record(
        self,
        doc_id: str,
        table_id: str,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new record.

        Args:
            doc_id: Document ID
            table_id: Table ID
            fields: Field values for the new record

        Returns:
            Created record with ID
        """
        data = {
            'fields': fields
        }
        return self._request('POST', f'/docs/{doc_id}/tables/{table_id}/records', json_data=data)

    def create_records(
        self,
        doc_id: str,
        table_id: str,
        records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create multiple records in batch.

        Args:
            doc_id: Document ID
            table_id: Table ID
            records: List of records with fields

        Returns:
            Batch creation response
        """
        return self._request('POST', f'/docs/{doc_id}/tables/{table_id}/records', json_data={'records': records})

    def update_record(
        self,
        doc_id: str,
        table_id: str,
        record_id: int,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a record.

        Args:
            doc_id: Document ID
            table_id: Table ID
            record_id: Record ID
            fields: Field values to update

        Returns:
            Updated record
        """
        data = {
            'fields': fields
        }
        return self._request('PATCH', f'/docs/{doc_id}/tables/{table_id}/records/{record_id}', json_data=data)

    def update_records(
        self,
        doc_id: str,
        table_id: str,
        records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Update multiple records in batch.

        Args:
            doc_id: Document ID
            table_id: Table ID
            records: List of records with id and fields

        Returns:
            Batch update response
        """
        data = {'records': records}
        return self._request('POST', f'/docs/{doc_id}/tables/{table_id}/records', json_data=data)

    def delete_record(self, doc_id: str, table_id: str, record_id: int) -> Dict[str, Any]:
        """Delete a record."""
        return self._request('DELETE', f'/docs/{doc_id}/tables/{table_id}/records/{record_id}')

    def delete_records(
        self,
        doc_id: str,
        table_id: str,
        record_ids: List[int]
    ) -> Dict[str, Any]:
        """Delete multiple records."""
        return self._request('POST', f'/docs/{doc_id}/tables/{table_id}/records/delete', json_data={'ids': record_ids})

    def apply_formula(
        self,
        doc_id: str,
        table_id: str,
        col_id: str,
        formula: str
    ) -> Dict[str, Any]:
        """
        Apply a formula to a column.

        Args:
            doc_id: Document ID
            table_id: Table ID
            col_id: Column ID
            formula: Formula expression

        Returns:
            Column update response
        """
        data = {
            'colId': col_id,
            'formula': formula
        }
        return self._request('POST', f'/docs/{doc_id}/tables/{table_id}/columns', json_data=data)

    def add_column(
        self,
        doc_id: str,
        table_id: str,
        col_id: str,
        type: str = "Text",
        formula: Optional[str] = None,
        is_visible: bool = True
    ) -> Dict[str, Any]:
        """
        Add a new column to a table.

        Args:
            doc_id: Document ID
            table_id: Table ID
            col_id: Column ID
            type: Column type (Text, Numeric, Date, Bool, etc.)
            formula: Optional formula for computed column
            is_visible: Whether column is visible

        Returns:
            Column creation response
        """
        data = {
            'colId': col_id,
            'type': type,
            'isVisible': is_visible
        }

        if formula is not None:
            data['formula'] = formula

        return self._request('POST', f'/docs/{doc_id}/tables/{table_id}/columns', json_data=data)

    def create_table(
        self,
        doc_id: str,
        table_id: str,
        columns: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create a new table.

        Args:
            doc_id: Document ID
            table_id: Table ID
            columns: List of column definitions

        Returns:
            Table creation response
        """
        data = {
            'tables': [{
                'id': table_id,
                'columns': columns
            }]
        }
        return self._request('POST', f'/docs/{doc_id}/tables', json_data=data)

    def query(
        self,
        doc_id: str,
        table_id: str,
        filter_str: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Query records with options.

        Args:
            doc_id: Document ID
            table_id: Table ID
            filter_str: Filter string
            sort: Sort specification
            limit: Maximum results

        Returns:
            Query results
        """
        params = {'limit': limit}
        if filter_str:
            params['filter'] = filter_str
        if sort:
            params['sort'] = sort

        return self._request('GET', f'/docs/{doc_id}/tables/{table_id}/records', params=params)

    def get_access_permissions(self, doc_id: str) -> Dict[str, Any]:
        """Get access permissions for a document."""
        return self._request('GET', f'/docs/{doc_id}/access')

    def set_access_permissions(
        self,
        doc_id: str,
        users: Optional[List[Dict[str, Any]]] = None,
        rules: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Set access permissions for a document."""
        data = {}
        if users is not None:
            data['users'] = users
        if rules is not None:
            data['rules'] = rules

        return self._request('PUT', f'/docs/{doc_id}/access', json_data=data)

    def get_user_profile(self) -> Dict[str, Any]:
        """Get current user profile."""
        return self._request('GET', '/profile')

    def get_workspaces(self) -> List[Dict[str, Any]]:
        """List all workspaces."""
        return self._request('GET', '/docs')