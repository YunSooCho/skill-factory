"""
Tabidoo API Client

This module provides a Python client for interacting with Tabidoo database platform.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class TabidooClient:
    """
    Client for Tabidoo Database Platform.

    Tabidoo provides:
    - Table management
    - Row operations
    - Column operations
    - Query and filtering
    - Form creation
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.tabidoo.io/v1",
        timeout: int = 30
    ):
        """Initialize the Tabidoo client."""
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, params=None, data=None, json_data=None) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, data=data, json=json_data, timeout=self.timeout)
        if response.status_code >= 400:
            error_data = response.json() if response.content else {}
            raise Exception(f"API Error {response.status_code}: {error_data}")
        try:
            return response.json()
        except:
            return response.text if response.text else {}

    def get_tables(self) -> List[Dict[str, Any]]:
        """Get all tables."""
        return self._request('GET', '/tables')

    def get_table(self, table_id: str) -> Dict[str, Any]:
        """Get table details."""
        return self._request('GET', f'/tables/{table_id}')

    def create_table(self, name: str, columns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a new table."""
        data = {'name': name, 'columns': columns}
        return self._request('POST', '/tables', json_data=data)

    def update_table(self, table_id: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Update table details."""
        data = {}
        if name:
            data['name'] = name
        return self._request('PUT', f'/tables/{table_id}', json_data=data)

    def delete_table(self, table_id: str) -> Dict[str, Any]:
        """Delete a table."""
        return self._request('DELETE', f'/tables/{table_id}')

    def get_rows(self, table_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get rows from a table."""
        params = {'limit': limit, 'offset': offset}
        return self._request('GET', f'/tables/{table_id}/rows', params=params)

    def get_row(self, table_id: str, row_id: str) -> Dict[str, Any]:
        """Get a specific row."""
        return self._request('GET', f'/tables/{table_id}/rows/{row_id}')

    def create_row(self, table_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new row."""
        return self._request('POST', f'/tables/{table_id}/rows', json_data=data)

    def update_row(self, table_id: str, row_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a row."""
        return self._request('PUT', f'/tables/{table_id}/rows/{row_id}', json_data=data)

    def delete_row(self, table_id: str, row_id: str) -> Dict[str, Any]:
        """Delete a row."""
        return self._request('DELETE', f'/tables/{table_id}/rows/{row_id}')

    def query_rows(self, table_id: str, filter_by: Dict[str, Any], limit: int = 100) -> Dict[str, Any]:
        """Query rows with filters."""
        params = {'limit': limit}
        return self._request('POST', f'/tables/{table_id}/query', params=params, json_data=filter_by)

    def batch_create_rows(self, table_id: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple rows in batch."""
        data = {'rows': rows}
        return self._request('POST', f'/tables/{table_id}/rows/batch', json_data=data)

    def get_columns(self, table_id: str) -> List[Dict[str, Any]]:
        """Get all columns in a table."""
        return self._request('GET', f'/tables/{table_id}/columns')

    def add_column(self, table_id: str, name: str, type: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add a new column."""
        data = {'name': name, 'type': type}
        if options:
            data['options'] = options
        return self._request('POST', f'/tables/{table_id}/columns', json_data=data)

    def update_column(self, table_id: str, column_id: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Update column details."""
        data = {}
        if name:
            data['name'] = name
        return self._request('PUT', f'/tables/{table_id}/columns/{column_id}', json_data=data)

    def delete_column(self, table_id: str, column_id: str) -> Dict[str, Any]:
        """Delete a column."""
        return self._request('DELETE', f'/tables/{table_id}/columns/{column_id}')

    def get_forms(self, table_id: str) -> List[Dict[str, Any]]:
        """Get all forms for a table."""
        return self._request('GET', f'/tables/{table_id}/forms')

    def create_form(self, table_id: str, name: str, fields: List[str]) -> Dict[str, Any]:
        """Create a new form."""
        data = {'table_id': table_id, 'name': name, 'fields': fields}
        return self._request('POST', '/forms', json_data=data)

    def update_form(self, form_id: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Update form details."""
        data = {}
        if name:
            data['name'] = name
        return self._request('PUT', f'/forms/{form_id}', json_data=data)

    def delete_form(self, form_id: str) -> Dict[str, Any]:
        """Delete a form."""
        return self._request('DELETE', f'/forms/{form_id}')