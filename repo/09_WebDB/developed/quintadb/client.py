"""
QuintaDB API Client

This module provides a Python client for interacting with QuintaDB database platform.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class QuintaDBClient:
    """
    Client for QuintaDB Database Platform.

    QuintaDB provides:
    - Database management
    - Table operations
    - Record management
    - Form creation
    - User management
    """

    def __init__(
        self,
        api_token: str,
        base_url: str = "https://quintadb.com",
        timeout: int = 30
    ):
        """
        Initialize the QuintaDB client.

        Args:
            api_token: QuintaDB API token
            base_url: Base URL for the QuintaDB API
            timeout: Request timeout in seconds
        """
        self.api_token = api_token
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
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

        # Add API token to params or data
        if params is None:
            params = {}
        params['api_token'] = self.api_token

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

        try:
            return response.json()
        except:
            return response.text if response.text else {}

    def get_databases(self) -> Dict[str, Any]:
        """Get all databases."""
        return self._request('GET', '/databases.json')

    def get_database(self, database_id: int) -> Dict[str, Any]:
        """Get database details."""
        return self._request('GET', f'/databases/{database_id}.json')

    def get_database_tables(self, database_id: int) -> Dict[str, Any]:
        """Get all tables in a database."""
        return self._request('GET', f'/databases/{database_id}/tables.json')

    def get_table(self, table_id: int) -> Dict[str, Any]:
        """Get table details."""
        return self._request('GET', f'/tables/{table_id}.json')

    def get_table_fields(self, table_id: int) -> Dict[str, Any]:
        """Get all fields in a table."""
        return self._request('GET', f'/tables/{table_id}/fields.json')

    def get_field(self, field_id: int) -> Dict[str, Any]:
        """Get field details."""
        return self._request('GET', f'/fields/{field_id}.json')

    def create_field(
        self,
        table_id: int,
        type: str,
        label: str,
        position: Optional[int] = None,
        required: Optional[bool] = None,
        options: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new field."""
        data = {
            'type': type,
            'label': label
        }
        if position is not None:
            data['position'] = position
        if required is not None:
            data['required'] = required
        if options:
            data['options'] = options

        return self._request('POST', f'/tables/{table_id}/fields.json', json_data=data)

    def update_field(
        self,
        field_id: int,
        label: Optional[str] = None,
        required: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update field properties."""
        data = {}
        if label:
            data['label'] = label
        if required is not None:
            data['required'] = required

        return self._request('PUT', f'/fields/{field_id}.json', json_data=data)

    def delete_field(self, field_id: int) -> Dict[str, Any]:
        """Delete a field."""
        return self._request('DELETE', f'/fields/{field_id}.json')

    def get_records(
        self,
        table_id: int,
        per_page: int = 100,
        page: int = 1
    ) -> Dict[str, Any]:
        """Get records from a table."""
        params = {
            'per_page': per_page,
            'page': page
        }
        return self._request('GET', f'/tables/{table_id}/records.json', params=params)

    def get_record(self, record_id: int, table_id: int) -> Dict[str, Any]:
        """Get a specific record."""
        return self._request('GET', f'/tables/{table_id}/records/{record_id}.json')

    def create_record(
        self,
        table_id: int,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new record."""
        return self._request('POST', f'/tables/{table_id}/records.json', json_data=record)

    def update_record(
        self,
        record_id: int,
        table_id: int,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a record."""
        return self._request('PUT', f'/tables/{table_id}/records/{record_id}.json', json_data=record)

    def delete_record(self, record_id: int, table_id: int) -> Dict[str, Any]:
        """Delete a record."""
        return self._request('DELETE', f'/tables/{table_id}/records/{record_id}.json')

    def filter_records(
        self,
        table_id: int,
        query: str,
        per_page: int = 100
    ) -> Dict[str, Any]:
        """Filter records based on query."""
        params = {
            'query': query,
            'per_page': per_page
        }
        return self._request('GET', f'/tables/{table_id}/records/filter.json', params=params)

    def search_records(
        self,
        table_id: int,
        query: str,
        per_page: int = 100
    ) -> Dict[str, Any]:
        """Search records."""
        params = {
            'query': query,
            'per_page': per_page
        }
        return self._request('GET', f'/tables/{table_id}/records/search.json', params=params)

    def get_count(self, table_id: int) -> Dict[str, Any]:
        """Get record count for a table."""
        return self._request('GET', f'/tables/{table_id}/records/count.json')

    def get_views(self, table_id: int) -> Dict[str, Any]:
        """Get all views for a table."""
        return self._request('GET', f'/tables/{table_id}/views.json')

    def get_view(self, view_id: int) -> Dict[str, Any]:
        """Get view details."""
        return self._request('GET', f'/views/{view_id}.json')

    def get_view_records(
        self,
        table_id: int,
        view_id: int,
        per_page: int = 100,
        page: int = 1
    ) -> Dict[str, Any]:
        """Get records from a specific view."""
        params = {
            'per_page': per_page,
            'page': page
        }
        return self._request('GET', f'/tables/{table_id}/views/{view_id}/records.json', params=params)

    def create_view(
        self,
        table_id: int,
        name: str,
        view_type: str = "table",
        column_ids: Optional[str] = None,
        conditions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new view."""
        data = {
            'name': name,
            'type': view_type
        }
        if column_ids:
            data['column_ids'] = column_ids
        if conditions:
            data['conditions'] = conditions

        return self._request('POST', f'/tables/{table_id}/views.json', json_data=data)

    def update_view(
        self,
        view_id: int,
        name: Optional[str] = None,
        conditions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update view properties."""
        data = {}
        if name:
            data['name'] = name
        if conditions:
            data['conditions'] = conditions

        return self._request('PUT', f'/views/{view_id}.json', json_data=data)

    def delete_view(self, view_id: int) -> Dict[str, Any]:
        """Delete a view."""
        return self._request('DELETE', f'/views/{view_id}.json')

    def get_forms(self) -> Dict[str, Any]:
        """Get all forms."""
        return self._request('GET', '/forms.json')

    def get_form(self, form_id: int) -> Dict[str, Any]:
        """Get form details."""
        return self._request('GET', f'/forms/{form_id}.json')

    def create_form(
        self,
        table_id: int,
        name: str,
        description: str = ""
    ) -> Dict[str, Any]:
        """Create a new form."""
        data = {
            'table_id': table_id,
            'name': name,
            'description': description
        }
        return self._request('POST', '/forms.json', json_data=data)

    def update_form(
        self,
        form_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update form properties."""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description

        return self._request('PUT', f'/forms/{form_id}.json', json_data=data)

    def delete_form(self, form_id: int) -> Dict[str, Any]:
        """Delete a form."""
        return self._request('DELETE', f'/forms/{form_id}.json')

    def get_users(self) -> Dict[str, Any]:
        """Get all users."""
        return self._request('GET', '/users.json')

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get user details."""
        return self._request('GET', f'/users/{user_id}.json')

    def create_user(
        self,
        email: str,
        name: str,
        role: str = "user"
    ) -> Dict[str, Any]:
        """Create a new user."""
        data = {
            'email': email,
            'name': name,
            'role': role
        }
        return self._request('POST', '/users.json', json_data=data)

    def update_user(
        self,
        user_id: int,
        name: Optional[str] = None,
        role: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update user properties."""
        data = {}
        if name:
            data['name'] = name
        if role:
            data['role'] = role

        return self._request('PUT', f'/users/{user_id}.json', json_data=data)

    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Delete a user."""
        return self._request('DELETE', f'/users/{user_id}.json')

    def get_roles(self) -> Dict[str, Any]:
        """Get all roles."""
        return self._request('GET', '/roles.json')

    def get_role(self, role_id: int) -> Dict[str, Any]:
        """Get role details."""
        return self._request('GET', f'/roles/{role_id}.json')

    def upload_file(
        self,
        file_path: str,
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload a file."""
        with open(file_path, 'rb') as f:
            files = {'file': (filename or file_path, f)}
            return self._request('POST', '/files.json', data={'api_token': self.api_token}, files=files)

    def get_file(self, file_id: int) -> Dict[str, Any]:
        """Get file information."""
        return self._request('GET', f'/files/{file_id}.json')

    def delete_file(self, file_id: int) -> Dict[str, Any]:
        """Delete a file."""
        return self._request('DELETE', f'/files/{file_id}.json')

    def get_database_statistics(self, database_id: int) -> Dict[str, Any]:
        """Get database statistics."""
        return self._request('GET', f'/databases/{database_id}/statistics.json')

    def get_table_statistics(self, table_id: int) -> Dict[str, Any]:
        """Get table statistics."""
        return self._request('GET', f'/tables/{table_id}/statistics.json')