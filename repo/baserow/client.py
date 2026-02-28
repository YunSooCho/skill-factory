"""
Baserow API Client

This module provides a Python client for interacting with Baserow's API.
"""

import requests
from typing import Dict, List, Optional, Any
import json


class BaserowClient:
    """
    Client for Baserow Database API.

    Baserow provides:
    - Open-source no-code database
    - Self-hosting capabilities
    - REST API for data operations
    - Airtable-like interface
    """

    def __init__(
        self,
        api_token: str,
        base_url: str = "https://api.baserow.io/api",
        timeout: int = 30
    ):
        """Initialize the Baserow client."""
        self.api_token = api_token
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Token {api_token}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def list_applications(self) -> List[Dict[str, Any]]:
        """List all applications (groups)."""
        result = self._request('GET', '/applications/')
        return result

    def get_database(self, database_id: int) -> Dict[str, Any]:
        """Get database details."""
        result = self._request('GET', f'/database/tables/database/{database_id}/')
        return result

    def list_tables(self, database_id: int) -> List[Dict[str, Any]]:
        """List tables in a database."""
        result = self._request('GET', f'/database/tables/database/{database_id}/')
        return result

    def get_table(self, table_id: int) -> Dict[str, Any]:
        """Get table details."""
        result = self._request('GET', f'/database/tables/{table_id}/')
        return result

    def create_table(
        self,
        database_id: int,
        name: str,
        data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Create a new table."""
        payload = {
            'name': name,
            'database_id': database_id
        }
        if data:
            payload['data'] = data
        return self._request('POST', f'/database/tables/database/{database_id}/', data=payload)

    def update_table(
        self,
        table_id: int,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update a table."""
        payload = {}
        if name:
            payload['name'] = name
        return self._request('PATCH', f'/database/tables/{table_id}/', data=payload)

    def delete_table(self, table_id: int) -> None:
        """Delete a table."""
        self._request('DELETE', f'/database/tables/{table_id}/')

    def list_rows(
        self,
        table_id: int,
        page: int = 1,
        size: int = 100,
        search: Optional[str] = None,
        user_field_names: bool = True
    ) -> Dict[str, Any]:
        """List rows in a table."""
        params = {
            'page': page,
            'size': size,
            'user_field_names': user_field_names
        }
        if search:
            params['search'] = search
        return self._request('GET', f'/database/rows/table/{table_id}/', params=params)

    def get_row(self, table_id: int, row_id: int) -> Dict[str, Any]:
        """Get a single row."""
        return self._request('GET', f'/database/rows/table/{table_id}/{row_id}/')

    def create_row(
        self,
        table_id: int,
        data: Dict[str, Any],
        user_field_names: bool = True,
        before_row_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create a new row."""
        payload = {
            'user_field_names': user_field_names
        }
        if before_row_id:
            payload['before'] = before_row_id
        payload.update(data)
        return self._request('POST', f'/database/rows/table/{table_id}/', data=payload)

    def update_row(
        self,
        table_id: int,
        row_id: int,
        data: Dict[str, Any],
        user_field_names: bool = True
    ) -> Dict[str, Any]:
        """Update a row."""
        payload = {
            'user_field_names': user_field_names
        }
        payload.update(data)
        return self._request('PATCH', f'/database/rows/table/{table_id}/{row_id}/', data=payload)

    def delete_row(self, table_id: int, row_id: int) -> None:
        """Delete a row."""
        self._request('DELETE', f'/database/rows/table/{table_id}/{row_id}/')

    def batch_create_rows(
        self,
        table_id: int,
        rows: List[Dict[str, Any]],
        user_field_names: bool = True
    ) -> List[Dict[str, Any]]:
        """Batch create rows."""
        payload = {
            'user_field_names': user_field_names,
            'items': rows
        }
        return self._request('POST', f'/database/rows/table/{table_id}/batch/', data=payload)

    def batch_update_rows(
        self,
        table_id: int,
        items: List[Dict[str, Any]],
        user_field_names: bool = True
    ) -> List[Dict[str, Any]]:
        """Batch update rows."""
        payload = {
            'user_field_names': user_field_names,
            'items': items
        }
        return self._request('PATCH', f'/database/rows/table/{table_id}/batch/', data=payload)

    def batch_delete_rows(self, table_id: int, row_ids: List[int]) -> None:
        """Batch delete rows."""
        payload = {'items': row_ids}
        self._request('POST', f'/database/rows/table/{table_id}/batch-delete/', data=payload)

    def list_views(self, table_id: int) -> List[Dict[str, Any]]:
        """List views for a table."""
        result = self._request('GET', f'/database/views/table/{table_id}/')
        return result

    def get_view(self, view_id: int) -> Dict[str, Any]:
        """Get view details."""
        return self._request('GET', f'/database/views/{view_id}/')

    def create_view(
        self,
        table_id: int,
        type: str,
        name: str,
        filter_type: str = "AND",
        filters: Optional[List[Dict[str, Any]]] = None,
        sortings: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Create a new view."""
        payload = {
            'table_id': table_id,
            'type': type,
            'name': name,
            'filter_type': filter_type
        }
        if filters:
            payload['filters'] = filters
        if sortings:
            payload['sortings'] = sortings
        return self._request('POST', f'/database/views/table/{table_id}/', data=payload)

    def update_view(
        self,
        view_id: int,
        name: Optional[str] = None,
        filter_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update a view."""
        payload = {}
        if name:
            payload['name'] = name
        if filter_type:
            payload['filter_type'] = filter_type
        return self._request('PATCH', f'/database/views/{view_id}/', data=payload)

    def delete_view(self, view_id: int) -> None:
        """Delete a view."""
        self._request('DELETE', f'/database/views/{view_id}/')

    def list_fields(self, table_id: int) -> List[Dict[str, Any]]:
        """List fields in a table."""
        result = self._request('GET', f'/database/fields/table/{table_id}/')
        return result

    def get_field(self, field_id: int) -> Dict[str, Any]:
        """Get field details."""
        result = self._request('GET', f'/database/fields/{field_id}/')
        return result

    def create_field(
        self,
        table_id: int,
        type: str,
        name: str,
        primary: bool = False,
        read_only: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a new field."""
        payload = {
            'table_id': table_id,
            'type': type,
            'name': name,
            'primary': primary,
            'read_only': read_only
        }
        payload.update(kwargs)
        return self._request('POST', f'/database/fields/table/{table_id}/', data=payload)

    def update_field(
        self,
        field_id: int,
        name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Update a field."""
        payload = {}
        if name:
            payload['name'] = name
        payload.update(kwargs)
        return self._request('PATCH', f'/database/fields/{field_id}/', data=payload)

    def delete_field(self, field_id: int) -> None:
        """Delete a field."""
        self._request('DELETE', f'/database/fields/{field_id}/')

    def upload_file_via_url(
        self,
        url: str
    ) -> Dict[str, Any]:
        """Upload a file from a URL."""
        payload = {'url': url}
        return self._request('POST', '/database/files/upload-via-url/', data=payload)

    def upload_file(
        self,
        file_path: str
    ) -> Dict[str, Any]:
        """Upload a file directly."""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            headers = {'Authorization': f'Token {self.api_token}'}
            response = requests.post(
                f"{self.base_url}/database/files/upload-file/",
                files=files,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

    def filter_rows(
        self,
        table_id: int,
        filters: List[Dict[str, Any]],
        user_field_names: bool = True
    ) -> List[Dict[str, Any]]:
        """Filter rows with advanced filtering."""
        return self.list_rows(
            table_id,
            user_field_names=user_field_names,
            **{f['field']: f['value'] for f in filters}
        )

    def search_rows(
        self,
        table_id: int,
        search_query: str,
        user_field_names: bool = True
    ) -> List[Dict[str, Any]]:
        """Search rows by query."""
        result = self.list_rows(
            table_id,
            search=search_query,
            user_field_names=user_field_names
        )
        return result.get('results', [])

    def get_rows_by_view(
        self,
        view_id: int,
        page: int = 1,
        size: int = 100,
        user_field_names: bool = True
    ) -> Dict[str, Any]:
        """Get rows filtered by a view."""
        params = {
            'page': page,
            'size': size,
            'user_field_names': user_field_names
        }
        return self._request('GET', f'/database/views/{view_id}/results/', params=params)

    def create_link_row_field(
        self,
        table_id: int,
        name: str,
        linked_table_id: int,
        has_related_field: bool = True
    ) -> Dict[str, Any]:
        """Create a link row field to another table."""
        return self.create_field(
            table_id,
            type='link_row',
            name=name,
            link_row_table_id=linked_table_id,
            has_related_field=has_related_field
        )

    def create_lookup_field(
        self,
        table_id: int,
        name: str,
        through_field_id: int,
        target_field_id: int
    ) -> Dict[str, Any]:
        """Create a lookup field."""
        return self.create_field(
            table_id,
            type='lookup',
            name=name,
            through_field_id=through_field_id,
            target_field_id=target_field_id
        )

    def create_formula_field(
        self,
        table_id: int,
        name: str,
        formula: str
    ) -> Dict[str, Any]:
        """Create a formula field."""
        return self.create_field(
            table_id,
            type='formula',
            name=name,
            formula=formula
        )

    def get_gallery_view(self, view_id: int) -> Dict[str, Any]:
        """Get gallery view details."""
        return self._request('GET', f'/database/views/gallery/{view_id}/')

    def get_calendar_view(self, view_id: int, from_date: str, to_date: str) -> Dict[str, Any]:
        """Get calendar view results."""
        params = {'from_date': from_date, 'to_date': to_date}
        return self._request('GET', f'/database/views/calendar/{view_id}/results/', params=params)

    def get_kanban_view(self, view_id: int) -> Dict[str, Any]:
        """Get kanban view results."""
        return self._request('GET', f'/database/views/kanban/{view_id}/results/')

    def get_grid_view(self, view_id: int) -> Dict[str, Any]:
        """Get grid view results."""
        return self._request('GET', f'/database/views/grid/{view_id}/results/')