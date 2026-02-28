"""
DB-Nolimit API Client

This module provides a Python client for interacting with DB-Nolimit.
"""

import requests
from typing import Dict, List, Optional, Any
import json


class DBNolimitClient:
    """
    Client for DB-Nolimit Database API.

    DB-Nolimit provides:
    - Unlimited storage capacity
    - Flexible schema design
    - High-performance querying
    - Data indexing
    - Real-time updates
    """

    def __init__(
        self,
        api_key: str,
        endpoint: str,
        timeout: int = 30
    ):
        """Initialize the DB-Nolimit client."""
        self.api_key = api_key
        self.endpoint = endpoint.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })

    def _request(
        self,
        method: str,
        path: str,
        params=None,
        data=None,
        headers=None
    ) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.endpoint}{path}"
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
        response.raise_for_status()
        return response.json()

    def list_databases(self) -> List[Dict[str, Any]]:
        """List all databases."""
        result = self._request('GET', '/databases')
        return result.get('databases', [])

    def create_database(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new database."""
        data = {'name': name}
        if description:
            data['description'] = description
        return self._request('POST', '/databases', data=data)

    def get_database(self, db_name: str) -> Dict[str, Any]:
        """Get database details."""
        return self._request('GET', f'/databases/{db_name}')

    def delete_database(self, db_name: str) -> None:
        """Delete a database."""
        self._request('DELETE', f'/databases/{db_name}')

    def list_tables(self, db_name: str) -> List[Dict[str, Any]]:
        """List tables in a database."""
        result = self._request('GET', f'/databases/{db_name}/tables')
        return result.get('tables', [])

    def create_table(
        self,
        db_name: str,
        table_name: str,
        schema: Optional[Dict[str, Any]] = None,
        indexes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a new table."""
        data = {'name': table_name}
        if schema:
            data['schema'] = schema
        if indexes:
            data['indexes'] = indexes
        return self._request('POST', f'/databases/{db_name}/tables', data=data)

    def get_table(self, db_name: str, table_name: str) -> Dict[str, Any]:
        """Get table details."""
        return self._request('GET', f'/databases/{db_name}/tables/{table_name}')

    def delete_table(self, db_name: str, table_name: str) -> None:
        """Delete a table."""
        self._request('DELETE', f'/databases/{db_name}/tables/{table_name}')

    def insert(
        self,
        db_name: str,
        table_name: str,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Insert a single record."""
        return self._request('POST', f'/databases/{db_name}/tables/{table_name}/insert', data=record)

    def insert_many(
        self,
        db_name: str,
        table_name: str,
        records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Insert multiple records."""
        return self._request('POST', f'/databases/{db_name}/tables/{table_name}/insert/many', data=records)

    def find(
        self,
        db_name: str,
        table_name: str,
        query: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        offset: int = 0,
        sort: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Find records with optional filters."""
        params = {'limit': limit, 'offset': offset}
        if query:
            params['query'] = json.dumps(query)
        if sort:
            params['sort'] = json.dumps(sort)
        result = self._request('GET', f'/databases/{db_name}/tables/{table_name}/find', params=params)
        return result.get('records', [])

    def find_one(
        self,
        db_name: str,
        table_name: str,
        query: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Find a single record."""
        result = self.find(db_name, table_name, query=query, limit=1)
        return result[0] if result else None

    def get(
        self,
        db_name: str,
        table_name: str,
        record_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get a record by ID."""
        try:
            return self._request('GET', f'/databases/{db_name}/tables/{table_name}/{record_id}')
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def update(
        self,
        db_name: str,
        table_name: str,
        record_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a record by ID."""
        return self._request('PUT', f'/databases/{db_name}/tables/{table_name}/{record_id}', data=updates)

    def update_many(
        self,
        db_name: str,
        table_name: str,
        query: Dict[str, Any],
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update multiple records matching query."""
        data = {'query': query, 'updates': updates}
        return self._request('POST', f'/databases/{db_name}/tables/{table_name}/update/many', data=data)

    def delete(
        self,
        db_name: str,
        table_name: str,
        record_id: str
    ) -> None:
        """Delete a record by ID."""
        self._request('DELETE', f'/databases/{db_name}/tables/{table_name}/{record_id}')

    def delete_many(
        self,
        db_name: str,
        table_name: str,
        query: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Delete multiple records matching query."""
        return self._request('POST', f'/databases/{db_name}/tables/{table_name}/delete/many', data=query)

    def count(
        self,
        db_name: str,
        table_name: str,
        query: Optional[Dict[str, Any]] = None
    ) -> int:
        """Count records matching query."""
        params = {}
        if query:
            params['query'] = json.dumps(query)
        result = self._request('GET', f'/databases/{db_name}/tables/{table_name}/count', params=params)
        return result.get('count', 0)

    def aggregate(
        self,
        db_name: str,
        table_name: str,
        pipeline: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Run aggregation pipeline."""
        return self._request('POST', f'/databases/{db_name}/tables/{table_name}/aggregate', data=pipeline)

    def create_index(
        self,
        db_name: str,
        table_name: str,
        index_name: str,
        fields: List[str],
        unique: bool = False
    ) -> Dict[str, Any]:
        """Create an index."""
        data = {
            'name': index_name,
            'fields': fields,
            'unique': unique
        }
        return self._request('POST', f'/databases/{db_name}/tables/{table_name}/indexes', data=data)

    def list_indexes(self, db_name: str, table_name: str) -> List[Dict[str, Any]]:
        """List indexes."""
        result = self._request('GET', f'/databases/{db_name}/tables/{table_name}/indexes')
        return result.get('indexes', [])

    def drop_index(self, db_name: str, table_name: str, index_name: str) -> None:
        """Drop an index."""
        self._request('DELETE', f'/databases/{db_name}/tables/{table_name}/indexes/{index_name}')

    def transaction(self, operations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute multiple operations atomically."""
        return self._request('POST', '/transactions', data=operations)

    def backup_database(self, db_name: str) -> Dict[str, Any]:
        """Create backup of database."""
        return self._request('POST', f'/databases/{db_name}/backup')

    def restore_database(self, db_name: str, backup_id: str) -> Dict[str, Any]:
        """Restore database from backup."""
        data = {'backup_id': backup_id}
        return self._request('POST', f'/databases/{db_name}/restore', data=data)

    def get_stats(self, db_name: str) -> Dict[str, Any]:
        """Get database statistics."""
        return self._request('GET', f'/databases/{db_name}/stats')

    def export_data(
        self,
        db_name: str,
        table_name: str,
        format: str = 'json'
    ) -> str:
        """Export table data."""
        return self._request('GET', f'/databases/{db_name}/tables/{table_name}/export', params={'format': format})

    def import_data(
        self,
        db_name: str,
        table_name: str,
        format: str,
        data: Any
    ) -> Dict[str, Any]:
        """Import data into table."""
        return self._request('POST', f'/databases/{db_name}/tables/{table_name}/import', data={'format': format, 'data': data})

    def search(
        self,
        db_name: str,
        table_name: str,
        search_term: str,
        fields: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Full-text search."""
        params = {'query': search_term}
        if fields:
            params['fields'] = json.dumps(fields)
        result = self._request('GET', f'/databases/{db_name}/tables/{table_name}/search', params=params)
        return result.get('results', [])