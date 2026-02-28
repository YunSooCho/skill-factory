"""
AITable API Client

This module provides a Python client for interacting with AITable's database API.
"""

import requests
from typing import Dict, List, Optional, Any
import json


class AITableClient:
    """
    Client for AITable Database API.

    AITable provides:
    - Spreadsheet-database hybrid functionality
    - AI-powered data analysis
    - REST API for data operations
    - Real-time collaboration
    """

    def __init__(
        self,
        api_token: str,
        base_url: str = "https://aitable.ai/api/v1",
        timeout: int = 30
    ):
        """Initialize the AITable client."""
        self.api_token = api_token
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_spaces(self) -> List[Dict[str, Any]]:
        """Get list of spaces."""
        result = self._request('GET', '/spaces')
        return result.get('data', {}).get('spaces', [])

    def get_space(self, space_id: str) -> Dict[str, Any]:
        """Get space details."""
        result = self._request('GET', f'/spaces/{space_id}')
        return result.get('data', {})

    def get_bases(self, space_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of bases."""
        if space_id:
            result = self._request('GET', f'/spaces/{space_id}/bases')
        else:
            result = self._request('GET', '/bases')
        return result.get('data', {}).get('bases', [])

    def get_base(self, base_id: str) -> Dict[str, Any]:
        """Get base details."""
        result = self._request('GET', f'/bases/{base_id}')
        return result.get('data', {})

    def get_tables(self, base_id: str) -> List[Dict[str, Any]]:
        """Get tables in a base."""
        result = self._request('GET', f'/bases/{base_id}/tables')
        return result.get('data', {}).get('tables', [])

    def get_table(self, base_id: str, table_id: str) -> Dict[str, Any]:
        """Get table details."""
        result = self._request('GET', f'/bases/{base_id}/tables/{table_id}')
        return result.get('data', {})

    def get_schema(self, base_id: str, table_id: str) -> Dict[str, Any]:
        """Get table schema."""
        result = self._request('GET', f'/bases/{base_id}/tables/{table_id}/schema')
        return result.get('data', {})

    def get_records(
        self,
        base_id: str,
        table_id: str,
        page_size: int = 100,
        view_id: Optional[str] = None,
        sort: Optional[List[Dict[str, str]]] = None,
        filter_by_formula: Optional[str] = None,
        fields: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get records from a table."""
        params = {'pageSize': page_size, ' pageNum': 1}
        if view_id:
            params['viewId'] = view_id
        if sort:
            params['sort'] = json.dumps(sort)
        if filter_by_formula:
            params['filterByFormula'] = filter_by_formula
        if fields:
            params['fields'] = json.dumps(fields)

        records = []
        has_more = True

        while has_more:
            result = self._request('GET', f'/bases/{base_id}/tables/{table_id}/records', params=params)
            data = result.get('data', {})
            records.extend(data.get('records', []))
            has_more = data.get('hasMore', False)
            params['pageNum'] += 1

        return records

    def get_record(self, base_id: str, table_id: str, record_id: str) -> Dict[str, Any]:
        """Get a single record."""
        result = self._request('GET', f'/bases/{base_id}/tables/{table_id}/records/{record_id}')
        return result.get('data', {})

    def create_record(
        self,
        base_id: str,
        table_id: str,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new record."""
        data = {'fields': fields}
        result = self._request('POST', f'/bases/{base_id}/tables/{table_id}/records', data=data)
        return result.get('data', {})

    def update_record(
        self,
        base_id: str,
        table_id: str,
        record_id: str,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a record."""
        data = {'fields': fields}
        result = self._request('PUT', f'/bases/{base_id}/tables/{table_id}/records/{record_id}', data=data)
        return result.get('data', {})

    def delete_record(self, base_id: str, table_id: str, record_id: str) -> Dict[str, Any]:
        """Delete a record."""
        result = self._request('DELETE', f'/bases/{base_id}/tables/{table_id}/records/{record_id}')
        return result.get('data', {})

    def batch_create_records(
        self,
        base_id: str,
        table_id: str,
        records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create multiple records (batch)."""
        data = {'records': records}
        result = self._request('POST', f'/bases/{base_id}/tables/{table_id}/records/batch', data=data)
        return result.get('data', {}).get('records', [])

    def batch_update_records(
        self,
        base_id: str,
        table_id: str,
        records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Update multiple records (batch)."""
        data = {'records': records}
        result = self._request('PUT', f'/bases/{base_id}/tables/{table_id}/records/batch', data=data)
        return result.get('data', {}).get('records', [])

    def batch_delete_records(
        self,
        base_id: str,
        table_id: str,
        record_ids: List[str]
    ) -> Dict[str, Any]:
        """Delete multiple records (batch)."""
        data = {'recordIds': record_ids}
        result = self._request('POST', f'/bases/{base_id}/tables/{table_id}/records/batch/delete', data=data)
        return result.get('data', {})

    def get_views(self, base_id: str, table_id: str) -> List[Dict[str, Any]]:
        """Get views for a table."""
        result = self._request('GET', f'/bases/{base_id}/tables/{table_id}/views')
        return result.get('data', {}).get('views', [])

    def get_fields(self, base_id: str, table_id: str) -> List[Dict[str, Any]]:
        """Get fields for a table."""
        result = self._request('GET', f'/bases/{base_id}/tables/{table_id}/fields')
        return result.get('data', {}).get('fields', [])

    def create_field(
        self,
        base_id: str,
        table_id: str,
        name: str,
        type: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new field in a table."""
        data = {
            'name': name,
            'type': type
        }
        if options:
            data['options'] = options
        result = self._request('POST', f'/bases/{base_id}/tables/{table_id}/fields', data=data)
        return result.get('data', {})

    def update_field(
        self,
        base_id: str,
        table_id: str,
        field_id: str,
        name: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update a field."""
        data = {}
        if name:
            data['name'] = name
        if options:
            data['options'] = options
        result = self._request('PUT', f'/bases/{base_id}/tables/{table_id}/fields/{field_id}', data=data)
        return result.get('data', {})

    def delete_field(self, base_id: str, table_id: str, field_id: str) -> Dict[str, Any]:
        """Delete a field."""
        result = self._request('DELETE', f'/bases/{base_id}/tables/{table_id}/fields/{field_id}')
        return result.get('data', {})

    def upload_attachment(
        self,
        base_id: str,
        table_id: str,
        record_id: str,
        field_id: str,
        file_path: str
    ) -> Dict[str, Any]:
        """Upload an attachment to a record."""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            headers = {'Authorization': f'Bearer {self.api_token}'}
            response = requests.post(
                f"{self.base_url}/bases/{base_id}/tables/{table_id}/records/{record_id}/fields/{field_id}/attachments",
                files=files,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

    def get_collaborators(self, base_id: str) -> List[Dict[str, Any]]:
        """Get collaborators for a base."""
        result = self._request('GET', f'/bases/{base_id}/collaborators')
        return result.get('data', {}).get('collaborators', [])

    def add_collaborator(
        self,
        base_id: str,
        email: str,
        role: str = 'editor'
    ) -> Dict[str, Any]:
        """Add a collaborator to a base."""
        data = {'email': email, 'role': role}
        result = self._request('POST', f'/bases/{base_id}/collaborators', data=data)
        return result.get('data', {})

    def remove_collaborator(self, base_id: str, user_id: str) -> Dict[str, Any]:
        """Remove a collaborator from a base."""
        result = self._request('DELETE', f'/bases/{base_id}/collaborators/{user_id}')
        return result.get('data', {})

    def query_by_formula(
        self,
        base_id: str,
        table_id: str,
        formula: str,
        page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """Query records by formula."""
        return self.get_records(base_id, table_id, page_size=page_size, filter_by_formula=formula)

    def search_records(
        self,
        base_id: str,
        table_id: str,
        query: str,
        fields: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Search records by text."""
        params = {'query': query}
        if fields:
            params['fields'] = json.dumps(fields)
        result = self._request('GET', f'/bases/{base_id}/tables/{table_id}/records/search', params=params)
        return result.get('data', {}).get('records', [])

    def get_webhooks(self, base_id: str) -> List[Dict[str, Any]]:
        """Get webhooks for a base."""
        result = self._request('GET', f'/bases/{base_id}/webhooks')
        return result.get('data', {}).get('webhooks', [])

    def create_webhook(
        self,
        base_id: str,
        table_id: str,
        url: str,
        events: List[str]
    ) -> Dict[str, Any]:
        """Create a webhook."""
        data = {
            'tableId': table_id,
            'url': url,
            'events': events
        }
        result = self._request('POST', f'/bases/{base_id}/webhooks', data=data)
        return result.get('data', {})

    def delete_webhook(self, base_id: str, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook."""
        result = self._request('DELETE', f'/bases/{base_id}/webhooks/{webhook_id}')
        return result.get('data', {})

    def create_form(
        self,
        base_id: str,
        table_id: str,
        name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a form view."""
        data = {'name': name, 'type': 'form'}
        if description:
            data['description'] = description
        result = self._request('POST', f'/bases/{base_id}/tables/{table_id}/views', data=data)
        return result.get('data', {})

    def get_form_entries(self, form_id: str) -> List[Dict[str, Any]]:
        """Get form submissions."""
        result = self._request('GET', f'/forms/{form_id}/entries')
        return result.get('data', {}).get('entries', [])