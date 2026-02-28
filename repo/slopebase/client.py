"""
Slopebase API Client

This module provides a Python client for interacting with Slopebase database platform.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class SlopebaseClient:
    """
    Client for Slopebase Database Platform.

    Slopebase provides:
    - Database management
    - Table operations
    - Record management
    - Query and filtering
    - User management
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.slopebase.com/v1",
        timeout: int = 30
    ):
        """Initialize the Slopebase client."""
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

    def get_databases(self) -> List[Dict[str, Any]]:
        """Get all databases."""
        return self._request('GET', '/databases')

    def get_database(self, database_id: str) -> Dict[str, Any]:
        """Get database details."""
        return self._request('GET', f'/databases/{database_id}')

    def create_database(self, name: str, description: str = "") -> Dict[str, Any]:
        """Create a new database."""
        data = {'name': name, 'description': description}
        return self._request('POST', '/databases', json_data=data)

    def update_database(self, database_id: str, name: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """Update database details."""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        return self._request('PUT', f'/databases/{database_id}', json_data=data)

    def delete_database(self, database_id: str) -> Dict[str, Any]:
        """Delete a database."""
        return self._request('DELETE', f'/databases/{database_id}')

    def get_tables(self, database_id: str) -> List[Dict[str, Any]]:
        """Get all tables in a database."""
        return self._request('GET', f'/databases/{database_id}/tables')

    def get_table(self, table_id: str) -> Dict[str, Any]:
        """Get table details."""
        return self._request('GET', f'/tables/{table_id}')

    def create_table(self, database_id: str, name: str, schema: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a new table."""
        data = {'database_id': database_id, 'name': name, 'schema': schema}
        return self._request('POST', '/tables', json_data=data)

    def delete_table(self, table_id: str) -> Dict[str, Any]:
        """Delete a table."""
        return self._request('DELETE', f'/tables/{table_id}')

    def get_records(self, table_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get records from a table."""
        params = {'limit': limit, 'offset': offset}
        return self._request('GET', f'/tables/{table_id}/records', params=params)

    def get_record(self, table_id: str, record_id: str) -> Dict[str, Any]:
        """Get a specific record."""
        return self._request('GET', f'/tables/{table_id}/records/{record_id}')

    def create_record(self, table_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record."""
        payload = {'table_id': table_id, 'data': data}
        return self._request('POST', '/records', json_data=payload)

    def update_record(self, table_id: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record."""
        return self._request('PUT', f'/tables/{table_id}/records/{record_id}', json_data=data)

    def delete_record(self, table_id: str, record_id: str) -> Dict[str, Any]:
        """Delete a record."""
        return self._request('DELETE', f'/tables/{table_id}/records/{record_id}')

    def query_records(self, table_id: str, query: Dict[str, Any], limit: int = 100) -> Dict[str, Any]:
        """Query records with filters."""
        params = {'limit': limit}
        return self._request('POST', f'/tables/{table_id}/query', params=params, json_data=query)

    def batch_create_records(self, table_id: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple records in batch."""
        data = {'table_id': table_id, 'records': records}
        return self._request('POST', '/records/batch', json_data=data)

    def batch_update_records(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update multiple records in batch."""
        data = {'updates': updates}
        return self._request('PUT', '/records/batch', json_data=data)

    def batch_delete_records(self, record_ids: List[str]) -> Dict[str, Any]:
        """Delete multiple records in batch."""
        data = {'record_ids': record_ids}
        return self._request('DELETE', '/records/batch', json_data=data)

    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        return self._request('GET', '/users')

    def create_user(self, email: str, name: str, role: str = "member") -> Dict[str, Any]:
        """Create a new user."""
        data = {'email': email, 'name': name, 'role': role}
        return self._request('POST', '/users', json_data=data)

    def update_user(self, user_id: str, role: Optional[str] = None) -> Dict[str, Any]:
        """Update user details."""
        data = {}
        if role:
            data['role'] = role
        return self._request('PUT', f'/users/{user_id}', json_data=data)

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Delete a user."""
        return self._request('DELETE', f'/users/{user_id}')