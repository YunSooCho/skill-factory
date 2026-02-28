"""
Caspio API Client

This module provides a Python client for interacting with Caspio's REST API.
"""

import requests
from typing import Dict, List, Optional, Any
import json


class CaspioClient:
    """
    Client for Caspio Cloud Database API.

    Caspio provides:
    - Low-code database platform
    - REST API for data operations
    - Visual app builders
    - DataPages and forms
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        account_id: str,
        base_url: str = "https://c1.caspio.com/rest/v1",
        timeout: int = 30
    ):
        """Initialize the Caspio client."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.account_id = account_id
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.access_token = None

    def authenticate(self) -> str:
        """Authenticate and get access token."""
        auth_url = f"{self.base_url}/oauth/token"
        response = requests.post(
            auth_url,
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        token_data = response.json()
        self.access_token = token_data['access_token']
        self.session.headers.update({
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        return self.access_token

    def _request(
        self,
        method: str,
        endpoint: str,
        params=None,
        data=None,
        headers=None
    ) -> Any:
        """Make an authenticated request to the API."""
        if not self.access_token:
            self.authenticate()

        url = f"{self.base_url}{endpoint}"
        request_headers = dict(self.session.headers)
        if headers:
            request_headers.update(headers)

        response = self.session.request(
            method,
            url,
            params=params,
            json=data,
            headers=request_headers,
            timeout=self.timeout
        )

        if response.status_code == 401:
            self.authenticate()
            request_headers['Authorization'] = f'Bearer {self.access_token}'
            response = self.session.request(
                method,
                url,
                params=params,
                json=data,
                headers=request_headers,
                timeout=self.timeout
            )

        response.raise_for_status()

        if response.status_code == 204:
            return None
        elif response.headers.get('Content-Type', '').startswith('application/json'):
            return response.json()
        else:
            return response.text

    def list_tables(self, account_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all tables."""
        aid = account_id or self.account_id
        return self._request('GET', f'/v1/tables/{aid}')

    def get_table(
        self,
        account_id: str,
        table_name: str
    ) -> Dict[str, Any]:
        """Get table details."""
        return self._request('GET', f'/v1/tables/{account_id}/{table_name}')

    def describe_table(
        self,
        account_id: str,
        table_name: str
    ) -> Dict[str, Any]:
        """Get table schema and column information."""
        return self._request('GET', f'/v1/tables/{account_id}/{table_name}/describe')

    def create_table(
        self,
        account_id: str,
        table_name: str,
        columns: List[Dict[str, Any]],
        primary_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new table."""
        data = {
            'TableName': table_name,
            'Columns': columns
        }
        if primary_key:
            data['PrimaryKey'] = primary_key
        return self._request('POST', f'/v1/tables/{account_id}', data=data)

    def delete_table(self, account_id: str, table_name: str) -> None:
        """Delete a table."""
        self._request('DELETE', f'/v1/tables/{account_id}/{table_name}')

    def get_rows(
        self,
        account_id: str,
        table_name: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get rows from a table."""
        endpoint = f'/v1/tables/{account_id}/{table_name}'
        # For POST-based query
        if params and 'q.where' in params:
            return self._request('POST', endpoint, data=params)
        return self._request('GET', endpoint, params=params)

    def get_row(
        self,
        account_id: str,
        table_name: str,
        row_id: str
    ) -> Dict[str, Any]:
        """Get a single row by ID."""
        return self._request('GET', f'/v1/tables/{account_id}/{table_name}/{row_id}')

    def insert_row(
        self,
        account_id: str,
        table_name: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Insert a new row."""
        return self._request('POST', f'/v1/tables/{account_id}/{table_name}', data=data)

    def update_row(
        self,
        account_id: str,
        table_name: str,
        row_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a row."""
        return self._request('PUT', f'/v1/tables/{account_id}/{table_name}/{row_id}', data=data)

    def delete_row(
        self,
        account_id: str,
        table_name: str,
        row_id: str
    ) -> None:
        """Delete a row."""
        self._request('DELETE', f'/v1/tables/{account_id}/{table_name}/{row_id}')

    def batch_insert(
        self,
        account_id: str,
        table_name: str,
        rows: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Insert multiple rows."""
        return self._request('POST', f'/v1/tables/{account_id}/{table_name}/batch', data=rows)

    def batch_update(
        self,
        account_id: str,
        table_name: str,
        updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Update multiple rows."""
        return self._request('PUT', f'/v1/tables/{account_id}/{table_name}/batch', data=updates)

    def batch_delete(
        self,
        account_id: str,
        table_name: str,
        row_ids: List[str]
    ) -> None:
        """Delete multiple rows."""
        self._request('DELETE', f'/v1/tables/{account_id}/{table_name}/batch', data=row_ids)

    def query(
        self,
        account_id: str,
        table_name: str,
        where_clause: str,
        select_fields: Optional[str] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Query table with SQL-like syntax."""
        data = {'q.where': where_clause}
        if select_fields:
            data['q.select'] = select_fields
        if order_by:
            data['q.orderBy'] = order_by
        if limit is not None:
            data['q.limit'] = str(limit)
        if offset is not None:
            data['q.offset'] = str(offset)

        return self._request('POST', f'/v1/tables/{account_id}/{table_name}', data=data)

    def search(
        self,
        account_id: str,
        table_name: str,
        search_field: str,
        search_value: str
    ) -> List[Dict[str, Any]]:
        """Search for records."""
        where_clause = f"{search_field} = '{search_value}'"
        return self.query(account_id, table_name, where_clause)

    def get_datapages(
        self,
        account_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all DataPages."""
        aid = account_id or self.account_id
        return self._request('GET', f'/v1/datapages/{aid}')

    def get_datapage(
        self,
        account_id: str,
        datapage_id: str
    ) -> Dict[str, Any]:
        """Get DataPage details."""
        return self._request('GET', f'/v1/datapages/{account_id}/{datapage_id}')

    def get_datapage_data(
        self,
        account_id: str,
        datapage_id: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get data from a DataPage."""
        return self._request('GET', f'/v1/datapages/{account_id}/{datapage_id}/data', params=params)

    def submit_datapage(
        self,
        account_id: str,
        datapage_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Submit data to a DataPage form."""
        return self._request('POST', f'/v1/datapages/{account_id}/{datapage_id}/data', data=data)

    def list_views(self, account_id: str) -> List[Dict[str, Any]]:
        """List all views."""
        return self._request('GET', f'/v1/views/{account_id}')

    def get_view(
        self,
        account_id: str,
        view_name: str
    ) -> List[Dict[str, Any]]:
        """Get view data."""
        return self._request('GET', f'/v1/views/{account_id}/{view_name}')

    def list_triggers(self, account_id: str) -> List[Dict[str, Any]]:
        """List all triggers."""
        return self._request('GET', f'/v1/triggers/{account_id}')

    def execute_trigger(
        self,
        account_id: str,
        trigger_id: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a trigger."""
        return self._request('POST', f'/v1/triggers/{account_id}/{trigger_id}/execute', data=params)

    def create_view(
        self,
        account_id: str,
        view_name: str,
        source_table: str,
        query: str
    ) -> Dict[str, Any]:
        """Create a new view."""
        data = {
            'ViewName': view_name,
            'SourceTable': source_table,
            'Query': query
        }
        return self._request('POST', f'/v1/views/{account_id}', data=data)

    def delete_view(
        self,
        account_id: str,
        view_name: str
    ) -> None:
        """Delete a view."""
        self._request('DELETE', f'/v1/views/{account_id}/{view_name}')

    def import_data(
        self,
        account_id: str,
        table_name: str,
        import_file: str,
        mapping: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Import data from file."""
        data = {
            'ImportFile': import_file,
            'Mapping': mapping or {}
        }
        return self._request('POST', f'/v1/tables/{account_id}/{table_name}/import', data=data)

    def export_data(
        self,
        account_id: str,
        table_name: str,
        format: str = 'csv',
        params: Optional[Dict[str, Any]] = None
    ) -> str:
        """Export data from a table."""
        headers = {'Accept': f'text/{format}'}
        return self._request(
            'GET',
            f'/v1/tables/{account_id}/{table_name}',
            params=params,
            headers=headers
        )

    def get_file(
        self,
        account_id: str,
        table_name: str,
        row_id: str,
        field_name: str
    ) -> bytes:
        """Get file from a file field."""
        url = f"{self.base_url}/v1/tables/{account_id}/{table_name}/{row_id}/{field_name}"
        response = self.session.get(url, headers={'Authorization': f'Bearer {self.access_token}'})
        response.raise_for_status()
        return response.content

    def upload_file(
        self,
        account_id: str,
        table_name: str,
        row_id: str,
        field_name: str,
        file_path: str
    ) -> Dict[str, Any]:
        """Upload a file to a file field."""
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f)}
            url = f"{self.base_url}/v1/tables/{account_id}/{table_name}/{row_id}/{field_name}"
            response = self.session.post(
                url,
                files=files,
                headers={'Authorization': f'Bearer {self.access_token}'}
            )
            response.raise_for_status()
            return response.json()

    def list_stored_procedures(self, account_id: str) -> List[Dict[str, Any]]:
        """List stored procedures."""
        return self._request('GET', f'/v1/storedprocedures/{account_id}')

    def execute_stored_procedure(
        self,
        account_id: str,
        procedure_name: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a stored procedure."""
        data = parameters or {}
        return self._request('POST', f'/v1/storedprocedures/{account_id}/{procedure_name}', data=data)

    def get_api_usage(self) -> Dict[str, Any]:
        """Get API usage statistics."""
        return self._request('GET', '/v1/usage')