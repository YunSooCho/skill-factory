"""
SheetRocks API Client

This module provides a Python client for interacting with SheetRocks spreadsheet platform.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class SheetRocksClient:
    """
    Client for SheetRocks Spreadsheet Platform.

    SheetRocks provides:
    - Spreadsheet management
    - Sheet operations
    - Cell operations
    - Data export/import
    - Sharing and collaboration
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.sheetrocks.io/v1",
        timeout: int = 30
    ):
        """
        Initialize the SheetRocks client.

        Args:
            api_key: SheetRocks API key
            base_url: Base URL for the SheetRocks API
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

    def get_spreadsheets(self) -> List[Dict[str, Any]]:
        """Get all spreadsheets."""
        return self._request('GET', '/spreadsheets')

    def get_spreadsheet(self, spreadsheet_id: str) -> Dict[str, Any]:
        """Get spreadsheet details."""
        return self._request('GET', f'/spreadsheets/{spreadsheet_id}')

    def create_spreadsheet(
        self,
        title: str,
        description: str = ""
    ) -> Dict[str, Any]:
        """Create a new spreadsheet."""
        data = {
            'title': title,
            'description': description
        }
        return self._request('POST', '/spreadsheets', json_data=data)

    def update_spreadsheet(
        self,
        spreadsheet_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update spreadsheet details."""
        data = {}
        if title:
            data['title'] = title
        if description:
            data['description'] = description

        return self._request('PUT', f'/spreadsheets/{spreadsheet_id}', json_data=data)

    def delete_spreadsheet(self, spreadsheet_id: str) -> Dict[str, Any]:
        """Delete a spreadsheet."""
        return self._request('DELETE', f'/spreadsheets/{spreadsheet_id}')

    def duplicate_spreadsheet(
        self,
        spreadsheet_id: str,
        title: str
    ) -> Dict[str, Any]:
        """Duplicate a spreadsheet."""
        data = {'title': title}
        return self._request('POST', f'/spreadsheets/{spreadsheet_id}/duplicate', json_data=data)

    def get_sheets(self, spreadsheet_id: str) -> List[Dict[str, Any]]:
        """Get all sheets in a spreadsheet."""
        return self._request('GET', f'/spreadsheets/{spreadsheet_id}/sheets')

    def get_sheet(self, sheet_id: str) -> Dict[str, Any]:
        """Get sheet details."""
        return self._request('GET', f'/sheets/{sheet_id}')

    def create_sheet(
        self,
        spreadsheet_id: str,
        title: str,
        row_count: int = 1000,
        column_count: int = 26
    ) -> Dict[str, Any]:
        """Create a new sheet."""
        data = {
            'spreadsheet_id': spreadsheet_id,
            'title': title,
            'row_count': row_count,
            'column_count': column_count
        }
        return self._request('POST', '/sheets', json_data=data)

    def update_sheet(
        self,
        sheet_id: str,
        title: Optional[str] = None,
        row_count: Optional[int] = None,
        column_count: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update sheet details."""
        data = {}
        if title:
            data['title'] = title
        if row_count:
            data['row_count'] = row_count
        if column_count:
            data['column_count'] = column_count

        return self._request('PUT', f'/sheets/{sheet_id}', json_data=data)

    def delete_sheet(self, sheet_id: str) -> Dict[str, Any]:
        """Delete a sheet."""
        return self._request('DELETE', f'/sheets/{sheet_id}')

    def get_cells(
        self,
        sheet_id: str,
        range: str
    ) -> Dict[str, Any]:
        """Get cells in a range (e.g., 'A1:D10')."""
        params = {'range': range}
        return self._request('GET', f'/sheets/{sheet_id}/cells', params=params)

    def get_cell(
        self,
        sheet_id: str,
        cell: str
    ) -> Dict[str, Any]:
        """Get a specific cell value (e.g., 'A1')."""
        return self._request('GET', f'/sheets/{sheet_id}/cells/{cell}')

    def update_cell(
        self,
        sheet_id: str,
        cell: str,
        value: Any,
        format: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update a cell value."""
        data = {'value': value}
        if format:
            data['format'] = format

        return self._request('PUT', f'/sheets/{sheet_id}/cells/{cell}', json_data=data)

    def update_cells(
        self,
        sheet_id: str,
        updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Update multiple cells in a batch."""
        data = {'updates': updates}
        return self._request('PUT', f'/sheets/{sheet_id}/cells/batch', json_data=data)

    def get_row(
        self,
        sheet_id: str,
        row_number: int
    ) -> Dict[str, Any]:
        """Get an entire row."""
        return self._request('GET', f'/sheets/{sheet_id}/rows/{row_number}')

    def update_row(
        self,
        sheet_id: str,
        row_number: int,
        values: List[Any]
    ) -> Dict[str, Any]:
        """Update an entire row."""
        data = {'values': values}
        return self._request('PUT', f'/sheets/{sheet_id}/rows/{row_number}', json_data=data)

    def append_row(
        self,
        sheet_id: str,
        values: List[Any]
    ) -> Dict[str, Any]:
        """Append a new row to the sheet."""
        data = {'values': values}
        return self._request('POST', f'/sheets/{sheet_id}/rows', json_data=data)

    def delete_row(
        self,
        sheet_id: str,
        row_number: int
    ) -> Dict[str, Any]:
        """Delete a row."""
        return self._request('DELETE', f'/sheets/{sheet_id}/rows/{row_number}')

    def get_column(
        self,
        sheet_id: str,
        column_letter: str
    ) -> Dict[str, Any]:
        """Get an entire column by letter (e.g., 'A')."""
        return self._request('GET', f'/sheets/{sheet_id}/columns/{column_letter}')

    def update_column(
        self,
        sheet_id: str,
        column_letter: str,
        values: List[Any]
    ) -> Dict[str, Any]:
        """Update an entire column."""
        data = {'values': values}
        return self._request('PUT', f'/sheets/{sheet_id}/columns/{column_letter}', json_data=data)

    def append_column(
        self,
        sheet_id: str,
        values: List[Any]
    ) -> Dict[str, Any]:
        """Append a new column to the sheet."""
        data = {'values': values}
        return self._request('POST', f'/sheets/{sheet_id}/columns', json_data=data)

    def delete_column(
        self,
        sheet_id: str,
        column_letter: str
    ) -> Dict[str, Any]:
        """Delete a column."""
        return self._request('DELETE', f'/sheets/{sheet_id}/columns/{column_letter}')

    def clear_range(
        self,
        sheet_id: str,
        range: str
    ) -> Dict[str, Any]:
        """Clear a range of cells."""
        data = {'range': range}
        return self._request('POST', f'/sheets/{sheet_id}/clear', json_data=data)

    def copy_range(
        self,
        sheet_id: str,
        source_range: str,
        destination: str
    ) -> Dict[str, Any]:
        """Copy a range of cells to another location."""
        data = {
            'source_range': source_range,
            'destination': destination
        }
        return self._request('POST', f'/sheets/{sheet_id}/copy', json_data=data)

    def export_sheet(
        self,
        sheet_id: str,
        format: str = "xlsx",
        range: Optional[str] = None
    ) -> Dict[str, Any]:
        """Export a sheet to a file format."""
        params = {'format': format}
        if range:
            params['range'] = range

        return self._request('GET', f'/sheets/{sheet_id}/export', params=params)

    def import_data(
        self,
        sheet_id: str,
        data: List[List[Any]],
        start_cell: str = "A1"
    ) -> Dict[str, Any]:
        """Import data into a sheet."""
        payload = {
            'data': data,
            'start_cell': start_cell
        }
        return self._request('POST', f'/sheets/{sheet_id}/import', json_data=payload)

    def search(
        self,
        spreadsheet_id: str,
        query: str,
        sheet_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for text in a spreadsheet or sheet."""
        params = {'query': query}
        if sheet_id:
            params['sheet_id'] = sheet_id

        return self._request('GET', f'/spreadsheets/{spreadsheet_id}/search', params=params)

    def add_permission(
        self,
        spreadsheet_id: str,
        email: str,
        role: str = "editor"
    ) -> Dict[str, Any]:
        """Add permission for a user."""
        data = {
            'email': email,
            'role': role
        }
        return self._request('POST', f'/spreadsheets/{spreadsheet_id}/permissions', json_data=data)

    def remove_permission(
        self,
        spreadsheet_id: str,
        permission_id: str
    ) -> Dict[str, Any]:
        """Remove permission."""
        return self._request('DELETE', f'/spreadsheets/{spreadsheet_id}/permissions/{permission_id}')

    def get_permissions(self, spreadsheet_id: str) -> List[Dict[str, Any]]:
        """Get all permissions for a spreadsheet."""
        return self._request('GET', f'/spreadsheets/{spreadsheet_id}/permissions')

    def add_comment(
        self,
        sheet_id: str,
        cell: str,
        text: str
    ) -> Dict[str, Any]:
        """Add a comment to a cell."""
        data = {
            'cell': cell,
            'text': text
        }
        return self._request('POST', f'/sheets/{sheet_id}/comments', json_data=data)

    def get_comments(self, sheet_id: str) -> List[Dict[str, Any]]:
        """Get all comments in a sheet."""
        return self._request('GET', f'/sheets/{sheet_id}/comments')

    def delete_comment(self, sheet_id: str, comment_id: str) -> Dict[str, Any]:
        """Delete a comment."""
        return self._request('DELETE', f'/sheets/{sheet_id}/comments/{comment_id}')

    def add_filter(
        self,
        sheet_id: str,
        range: str,
        criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a filter to a sheet."""
        data = {
            'range': range,
            'criteria': criteria
        }
        return self._request('POST', f'/sheets/{sheet_id}/filters', json_data=data)

    def remove_filter(self, sheet_id: str, filter_id: str) -> Dict[str, Any]:
        """Remove a filter."""
        return self._request('DELETE', f'/sheets/{sheet_id}/filters/{filter_id}')

    def get_version(self) -> Dict[str, Any]:
        """Get API version information."""
        return self._request('GET', '/version')