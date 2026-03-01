"""
Glide REST API Client

This module provides a Python client for interacting with the Glide API.
Glide is a no-code platform for building apps from data sources like Google Sheets.

Base URL: https://api.glideapps.com
"""

import requests
from typing import Optional, Dict, Any, List
import json


class GlideClient:
    """
    Client for interacting with the Glide API.
    """

    BASE_URL = "https://api.glideapps.com"

    def __init__(self, api_key: str):
        """
        Initialize the Glide client.

        Args:
            api_key: Your Glide API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a request to the Glide API.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests.request

        Returns:
            JSON response data

        Raises:
            requests.exceptions.RequestException: On API errors
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.request(method, url, **kwargs)

        if response.status_code >= 400:
            error_msg = f"API Error {response.status_code}"
            try:
                error_data = response.json()
                error_msg += f": {error_data.get('error', {}).get('message', response.text)}"
            except:
                error_msg += f": {response.text}"
            raise requests.exceptions.RequestException(error_msg)

        return response.json()

    # Table Operations

    def list_rows(self, app_id: str, table_name: str,
                  limit: int = 100, offset: int = 0,
                  sort_by: Optional[str] = None,
                  order: str = 'asc') -> Dict[str, Any]:
        """
        List rows from a table.

        Args:
            app_id: The ID of the Glide app
            table_name: The name of the table
            limit: Maximum number of rows to return
            offset: Number of rows to skip
            sort_by: Column name to sort by
            order: Sort order ('asc' or 'desc')

        Returns:
            List of rows
        """
        params = {'limit': limit, 'offset': offset, 'order': order}
        if sort_by:
            params['sortBy'] = sort_by

        return self._make_request(
            'GET',
            f'/api/{app_id}/tables/{table_name}/rows',
            params=params
        )

    def get_row(self, app_id: str, table_name: str, row_id: str) -> Dict[str, Any]:
        """
        Get a specific row from a table.

        Args:
            app_id: The ID of the Glide app
            table_name: The name of the table
            row_id: The ID of the row

        Returns:
            Row data
        """
        return self._make_request(
            'GET',
            f'/api/{app_id}/tables/{table_name}/rows/{row_id}'
        )

    def create_row(self, app_id: str, table_name: str,
                   row_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new row in a table.

        Args:
            app_id: The ID of the Glide app
            table_name: The name of the table
            row_data: Dictionary of column names and values

        Returns:
            Created row data
        """
        return self._make_request(
            'POST',
            f'/api/{app_id}/tables/{table_name}/rows',
            json=row_data
        )

    def update_row(self, app_id: str, table_name: str, row_id: str,
                   row_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a row in a table.

        Args:
            app_id: The ID of the Glide app
            table_name: The name of the table
            row_id: The ID of the row
            row_data: Dictionary of column names and values to update

        Returns:
            Updated row data
        """
        return self._make_request(
            'PATCH',
            f'/api/{app_id}/tables/{table_name}/rows/{row_id}',
            json=row_data
        )

    def delete_row(self, app_id: str, table_name: str, row_id: str) -> None:
        """
        Delete a row from a table.

        Args:
            app_id: The ID of the Glide app
            table_name: The name of the table
            row_id: The ID of the row to delete
        """
        self._make_request(
            'DELETE',
            f'/api/{app_id}/tables/{table_name}/rows/{row_id}'
        )

    def bulk_create_rows(self, app_id: str, table_name: str,
                         rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple rows in a table.

        Args:
            app_id: The ID of the Glide app
            table_name: The name of the table
            rows: List of row data dictionaries

        Returns:
            Created row data
        """
        return self._make_request(
            'POST',
            f'/api/{app_id}/tables/{table_name}/rows/bulk',
            json={'rows': rows}
        )

    def bulk_update_rows(self, app_id: str, table_name: str,
                         updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update multiple rows in a table.

        Args:
            app_id: The ID of the Glide app
            table_name: The name of the table
            updates: List of update objects, each with 'rowID' and row data

        Returns:
            Updated row data
        """
        return self._make_request(
            'PATCH',
            f'/api/{app_id}/tables/{table_name}/rows/bulk',
            json={'updates': updates}
        )

    def bulk_delete_rows(self, app_id: str, table_name: str,
                         row_ids: List[str]) -> Dict[str, Any]:
        """
        Delete multiple rows from a table.

        Args:
            app_id: The ID of the Glide app
            table_name: The name of the table
            row_ids: List of row IDs to delete

        Returns:
            Delete response
        """
        return self._make_request(
            'POST',
            f'/api/{app_id}/tables/{table_name}/rows/bulk/delete',
            json={'rowIDs': row_ids}
        )

    # Query Operations

    def query_rows(self, app_id: str, table_name: str,
                   filters: Optional[List[Dict[str, Any]]] = None,
                   join_type: str = 'and',
                   limit: int = 100) -> Dict[str, Any]:
        """
        Query rows from a table with filters.

        Args:
            app_id: The ID of the Glide app
            table_name: The name of the table
            filters: List of filter objects with 'column', 'operator', 'value'
            join_type: How to combine filters ('and' or 'or')
            limit: Maximum number of rows to return

        Returns:
            Query results
        """
        payload = {'join': join_type, 'limit': limit}
        if filters:
            payload['filters'] = filters

        return self._make_request(
            'POST',
            f'/api/{app_id}/tables/{table_name}/rows/query',
            json=payload
        )

    # File Operations

    def upload_file(self, app_id: str, file_path: str,
                    file_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file to Glide.

        Args:
            app_id: The ID of the Glide app
            file_path: Path to the file to upload
            file_name: Optional custom file name

        Returns:
            File upload result with file URL
        """
        import os

        if not file_name:
            file_name = os.path.basename(file_path)

        files = {'file': (file_name, open(file_path, 'rb'))}

        response = self._make_request(
            'POST',
            f'/api/{app_id}/files/upload',
            files=files
        )

        files['file'][1].close()
        return response

    # App Operations

    def get_app_info(self, app_id: str) -> Dict[str, Any]:
        """
        Get information about a Glide app.

        Args:
            app_id: The ID of the Glide app

        Returns:
            App information
        """
        return self._make_request('GET', f'/api/{app_id}')

    def list_tables(self, app_id: str) -> List[Dict[str, Any]]:
        """
        List all tables in a Glide app.

        Args:
            app_id: The ID of the Glide app

        Returns:
            List of table information
        """
        response = self._make_request('GET', f'/api/{app_id}/tables')
        return response.get('tables', [])

    def get_table_schema(self, app_id: str, table_name: str) -> Dict[str, Any]:
        """
        Get the schema of a table.

        Args:
            app_id: The ID of the Glide app
            table_name: The name of the table

        Returns:
            Table schema with columns and types
        """
        return self._make_request(
            'GET',
            f'/api/{app_id}/tables/{table_name}/schema'
        )

    # Action Operations

    def trigger_action(self, app_id: str, action_id: str,
                       params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Trigger a custom action in a Glide app.

        Args:
            app_id: The ID of the Glide app
            action_id: The ID of the action to trigger
            params: Optional parameters for the action

        Returns:
            Action execution result
        """
        payload = {}
        if params:
            payload['params'] = params

        return self._make_request(
            'POST',
            f'/api/{app_id}/actions/{action_id}',
            json=payload
        )

    def close(self):
        """
        Close the session.
        """
        self.session.close()