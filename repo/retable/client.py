"""
Retable API Client

This module provides a Python client for interacting with Retable collaboration platform.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class RetableClient:
    """
    Client for Retable Collaboration Platform.

    Retable provides:
    - Spreadsheet and database management
    - Table operations
    - Row and column management
    - Form creation
    - Team collaboration
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.retable.io/v1",
        timeout: int = 30
    ):
        """
        Initialize the Retable client.

        Args:
            api_key: Retable API key
            base_url: Base URL for the Retable API
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
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

        try:
            return response.json()
        except:
            return response.text if response.text else {}

    def get_workspaces(self) -> List[Dict[str, Any]]:
        """Get all workspaces."""
        return self._request('GET', '/workspaces')

    def get_workspace(self, workspace_id: str) -> Dict[str, Any]:
        """Get workspace details."""
        return self._request('GET', f'/workspaces/{workspace_id}')

    def create_workspace(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new workspace."""
        data = {'name': name}
        if description:
            data['description'] = description

        return self._request('POST', '/workspaces', json_data=data)

    def update_workspace(
        self,
        workspace_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update workspace details."""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description

        return self._request('PUT', f'/workspaces/{workspace_id}', json_data=data)

    def delete_workspace(self, workspace_id: str) -> Dict[str, Any]:
        """Delete a workspace."""
        return self._request('DELETE', f'/workspaces/{workspace_id}')

    def get_projects(self, workspace_id: str) -> List[Dict[str, Any]]:
        """Get all projects in a workspace."""
        return self._request('GET', f'/workspaces/{workspace_id}/projects')

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project details."""
        return self._request('GET', f'/projects/{project_id}')

    def create_project(
        self,
        workspace_id: str,
        name: str,
        description: str = ""
    ) -> Dict[str, Any]:
        """Create a new project."""
        data = {
            'workspace_id': workspace_id,
            'name': name,
            'description': description
        }
        return self._request('POST', '/projects', json_data=data)

    def update_project(
        self,
        project_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update project details."""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description

        return self._request('PUT', f'/projects/{project_id}', json_data=data)

    def delete_project(self, project_id: str) -> Dict[str, Any]:
        """Delete a project."""
        return self._request('DELETE', f'/projects/{project_id}')

    def get_tables(self, project_id: str) -> List[Dict[str, Any]]:
        """Get all tables in a project."""
        return self._request('GET', f'/projects/{project_id}/tables')

    def get_table(self, table_id: str) -> Dict[str, Any]:
        """Get table details."""
        return self._request('GET', f'/tables/{table_id}')

    def create_table(
        self,
        project_id: str,
        name: str,
        description: str = ""
    ) -> Dict[str, Any]:
        """Create a new table."""
        data = {
            'project_id': project_id,
            'name': name,
            'description': description
        }
        return self._request('POST', '/tables', json_data=data)

    def update_table(
        self,
        table_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update table details."""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description

        return self._request('PUT', f'/tables/{table_id}', json_data=data)

    def delete_table(self, table_id: str) -> Dict[str, Any]:
        """Delete a table."""
        return self._request('DELETE', f'/tables/{table_id}')

    def get_columns(self, table_id: str) -> List[Dict[str, Any]]:
        """Get all columns in a table."""
        return self._request('GET', f'/tables/{table_id}/columns')

    def get_column(self, column_id: str) -> Dict[str, Any]:
        """Get column details."""
        return self._request('GET', f'/columns/{column_id}')

    def create_column(
        self,
        table_id: str,
        type: str,
        name: str,
        description: str = "",
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new column."""
        data = {
            'table_id': table_id,
            'type': type,
            'name': name,
            'description': description
        }
        if options:
            data['options'] = options

        return self._request('POST', '/columns', json_data=data)

    def update_column(
        self,
        column_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update column details."""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if options:
            data['options'] = options

        return self._request('PUT', f'/columns/{column_id}', json_data=data)

    def delete_column(self, column_id: str) -> Dict[str, Any]:
        """Delete a column."""
        return self._request('DELETE', f'/columns/{column_id}')

    def get_rows(
        self,
        table_id: str,
        limit: int = 100,
        offset: int = 0,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> Dict[str, Any]:
        """Get rows from a table."""
        params = {
            'limit': limit,
            'offset': offset,
            'sort_order': sort_order
        }
        if sort_by:
            params['sort_by'] = sort_by

        return self._request('GET', f'/tables/{table_id}/rows', params=params)

    def get_row(self, row_id: str) -> Dict[str, Any]:
        """Get a specific row."""
        return self._request('GET', f'/rows/{row_id}')

    def create_row(
        self,
        table_id: str,
        cells: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new row."""
        data = {
            'table_id': table_id,
            'cells': cells
        }
        return self._request('POST', '/rows', json_data=data)

    def update_row(
        self,
        row_id: str,
        cells: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a row."""
        data = {'cells': cells}
        return self._request('PUT', f'/rows/{row_id}', json_data=data)

    def delete_row(self, row_id: str) -> Dict[str, Any]:
        """Delete a row."""
        return self._request('DELETE', f'/rows/{row_id}')

    def batch_create_rows(
        self,
        table_id: str,
        rows: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create multiple rows in a batch."""
        data = {
            'table_id': table_id,
            'rows': rows
        }
        return self._request('POST', '/rows/batch', json_data=data)

    def batch_update_rows(
        self,
        updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Update multiple rows in a batch."""
        data = {'updates': updates}
        return self._request('PUT', '/rows/batch', json_data=data)

    def batch_delete_rows(self, row_ids: List[str]) -> Dict[str, Any]:
        """Delete multiple rows in a batch."""
        data = {'row_ids': row_ids}
        return self._request('DELETE', '/rows/batch', json_data=data)

    def query_rows(
        self,
        table_id: str,
        filter_by: Dict[str, Any],
        limit: int = 100
    ) -> Dict[str, Any]:
        """Query rows with filters."""
        params = {'limit': limit}
        return self._request('POST', f'/tables/{table_id}/rows/query', params=params, json_data=filter_by)

    def get_views(self, table_id: str) -> List[Dict[str, Any]]:
        """Get all views for a table."""
        return self._request('GET', f'/tables/{table_id}/views')

    def get_view(self, view_id: str) -> Dict[str, Any]:
        """Get view details."""
        return self._request('GET', f'/views/{view_id}')

    def create_view(
        self,
        table_id: str,
        type: str,
        name: str,
        filters: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Create a new view."""
        data = {
            'table_id': table_id,
            'type': type,
            'name': name
        }
        if filters:
            data['filters'] = filters
        if sorts:
            data['sorts'] = sorts

        return self._request('POST', '/views', json_data=data)

    def update_view(
        self,
        view_id: str,
        name: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Update view details."""
        data = {}
        if name:
            data['name'] = name
        if filters:
            data['filters'] = filters
        if sorts:
            data['sorts'] = sorts

        return self._request('PUT', f'/views/{view_id}', json_data=data)

    def delete_view(self, view_id: str) -> Dict[str, Any]:
        """Delete a view."""
        return self._request('DELETE', f'/views/{view_id}')

    def get_forms(self, project_id: str) -> List[Dict[str, Any]]:
        """Get all forms in a project."""
        return self._request('GET', f'/projects/{project_id}/forms')

    def get_form(self, form_id: str) -> Dict[str, Any]:
        """Get form details."""
        return self._request('GET', f'/forms/{form_id}')

    def create_form(
        self,
        table_id: str,
        name: str,
        description: str = "",
        fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a new form."""
        data = {
            'table_id': table_id,
            'name': name,
            'description': description
        }
        if fields:
            data['fields'] = fields

        return self._request('POST', '/forms', json_data=data)

    def update_form(
        self,
        form_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Update form details."""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if fields:
            data['fields'] = fields

        return self._request('PUT', f'/forms/{form_id}', json_data=data)

    def delete_form(self, form_id: str) -> Dict[str, Any]:
        """Delete a form."""
        return self._request('DELETE', f'/forms/{form_id}')

    def get_members(self, workspace_id: str) -> List[Dict[str, Any]]:
        """Get all members in a workspace."""
        return self._request('GET', f'/workspaces/{workspace_id}/members')

    def add_member(
        self,
        workspace_id: str,
        email: str,
        role: str = "member"
    ) -> Dict[str, Any]:
        """Add a member to a workspace."""
        data = {
            'workspace_id': workspace_id,
            'email': email,
            'role': role
        }
        return self._request('POST', '/members', json_data=data)

    def update_member(
        self,
        member_id: str,
        role: str
    ) -> Dict[str, Any]:
        """Update member role."""
        data = {'role': role}
        return self._request('PUT', f'/members/{member_id}', json_data=data)

    def remove_member(self, member_id: str) -> Dict[str, Any]:
        """Remove a member from a workspace."""
        return self._request('DELETE', f'/members/{member_id}')

    def upload_file(
        self,
        file_path: str,
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload a file."""
        url = f"{self.base_url}/files/upload"

        with open(file_path, 'rb') as f:
            files = {'file': (filename or file_path, f)}
            headers = {'Authorization': f'Bearer {self.api_key}'}
            response = requests.post(url, files=files, headers=headers, timeout=self.timeout)

        if response.status_code >= 400:
            raise Exception(f"File upload failed: {response.text}")

        return response.json()

    def delete_file(self, file_id: str) -> Dict[str, Any]:
        """Delete a file."""
        return self._request('DELETE', f'/files/{file_id}')