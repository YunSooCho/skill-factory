"""
Ninox API Client

This module provides a Python client for interacting with Ninox's low-code database platform.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class NinoxClient:
    """
    Client for Ninox Low-Code Database.

    Ninox provides:
    - Low-code database creation and management
    - Custom forms and workflows
    - RESTful API for data operations
    - Team collaboration features
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.ninox.com/v1",
        timeout: int = 30
    ):
        """
        Initialize the Ninox client.

        Args:
            api_key: Ninox API key
            base_url: Base URL for the Ninox API
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
            return {}

    def list_teams(self) -> List[Dict[str, Any]]:
        """List all accessible teams."""
        return self._request('GET', '/teams')

    def get_team(self, team_id: str) -> Dict[str, Any]:
        """Get team details."""
        return self._request('GET', f'/teams/{team_id}')

    def list_databases(self, team_id: str) -> List[Dict[str, Any]]:
        """List all databases in a team."""
        return self._request('GET', f'/teams/{team_id}/databases')

    def get_database(self, team_id: str, database_id: str) -> Dict[str, Any]:
        """Get database details."""
        return self._request('GET', f'/teams/{team_id}/databases/{database_id}')

    def list_tables(self, team_id: str, database_id: str) -> List[Dict[str, Any]]:
        """List all tables in a database."""
        return self._request('GET', f'/teams/{team_id}/databases/{database_id}/tables')

    def get_table(self, team_id: str, database_id: str, table_id: str) -> Dict[str, Any]:
        """Get table details."""
        return self._request('GET', f'/teams/{team_id}/databases/{database_id}/tables/{table_id}')

    def get_schema(self, team_id: str, database_id: str) -> Dict[str, Any]:
        """Get database schema including all tables and fields."""
        return self._request('GET', f'/teams/{team_id}/databases/{database_id}/schema')

    def list_records(
        self,
        team_id: str,
        database_id: str,
        table_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List records from a table.

        Args:
            team_id: Team ID
            database_id: Database ID
            table_id: Table ID
            limit: Maximum number of records
            offset: Offset for pagination
            sort: Sort field or expression

        Returns:
            List of records
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if sort is not None:
            params['sort'] = sort

        return self._request('GET', f'/teams/{team_id}/databases/{database_id}/tables/{table_id}/records', params=params)

    def get_record(
        self,
        team_id: str,
        database_id: str,
        table_id: str,
        record_id: str
    ) -> Dict[str, Any]:
        """Get a specific record."""
        return self._request('GET', f'/teams/{team_id}/databases/{database_id}/tables/{table_id}/records/{record_id}')

    def create_record(
        self,
        team_id: str,
        database_id: str,
        table_id: str,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new record.

        Args:
            team_id: Team ID
            database_id: Database ID
            table_id: Table ID
            fields: Field values for the new record

        Returns:
            Created record with ID
        """
        return self._request('POST', f'/teams/{team_id}/databases/{database_id}/tables/{table_id}/records', json_data=fields)

    def update_record(
        self,
        team_id: str,
        database_id: str,
        table_id: str,
        record_id: str,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a record.

        Args:
            team_id: Team ID
            database_id: Database ID
            table_id: Table ID
            record_id: Record ID
            fields: Field values to update

        Returns:
            Updated record
        """
        return self._request('PUT', f'/teams/{team_id}/databases/{database_id}/tables/{table_id}/records/{record_id}', json_data=fields)

    def delete_record(
        self,
        team_id: str,
        database_id: str,
        table_id: str,
        record_id: str
    ) -> Dict[str, Any]:
        """Delete a record."""
        return self._request('DELETE', f'/teams/{team_id}/databases/{database_id}/tables/{table_id}/records/{record_id}')

    def create_records(
        self,
        team_id: str,
        database_id: str,
        table_id: str,
        records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create multiple records in batch.

        Args:
            team_id: Team ID
            database_id: Database ID
            table_id: Table ID
            records: List of record objects

        Returns:
            Batch creation response
        """
        return self._request('POST', f'/teams/{team_id}/databases/{database_id}/tables/{table_id}/records/batch', json_data=records)

    def update_records(
        self,
        team_id: str,
        database_id: str,
        table_id: str,
        records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Update multiple records in batch.

        Args:
            team_id: Team ID
            database_id: Database ID
            table_id: Table ID
            records: List of record objects with id field

        Returns:
            Batch update response
        """
        return self._request('PUT', f'/teams/{team_id}/databases/{database_id}/tables/{table_id}/records/batch', json_data=records)

    def delete_records(
        self,
        team_id: str,
        database_id: str,
        table_id: str,
        record_ids: List[str]
    ) -> Dict[str, Any]:
        """Delete multiple records."""
        return self._request('POST', f'/teams/{team_id}/databases/{database_id}/tables/{table_id}/records/batch/delete', json_data=record_ids)

    def query_records(
        self,
        team_id: str,
        database_id: str,
        table_id: str,
        query: str
    ) -> List[Dict[str, Any]]:
        """
        Query records using Ninox query language.

        Args:
            team_id: Team ID
            database_id: Database ID
            table_id: Table ID
            query: Query string

        Returns:
            Query results
        """
        return self._request('GET', f'/teams/{team_id}/databases/{database_id}/tables/{table_id}/query', params={'query': query})

    def count_records(
        self,
        team_id: str,
        database_id: str,
        table_id: str,
        query: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Count records in a table.

        Args:
            team_id: Team ID
            database_id: Database ID
            table_id: Table ID
            query: Optional query string for filtering

        Returns:
            Count result
        """
        params = {}
        if query:
            params['query'] = query

        return self._request('GET', f'/teams/{team_id}/databases/{database_id}/tables/{table_id}/count', params=params)

    def upload_file(
        self,
        team_id: str,
        database_id: str,
        table_id: str,
        record_id: str,
        field_name: str,
        file_path: str,
        file_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a file to a record.

        Args:
            team_id: Team ID
            database_id: Database ID
            table_id: Table ID
            record_id: Record ID
            field_name: Field name to attach file to
            file_path: Path to the file
            file_name: Optional custom filename

        Returns:
            Upload response
        """
        import os

        if file_name is None:
            file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            files = {'file': (file_name, f, 'application/octet-stream')}
            url = f"{self.base_url}/teams/{team_id}/databases/{database_id}/tables/{table_id}/records/{record_id}/files/{field_name}"

            response = requests.post(
                url,
                headers={'Authorization': f'Bearer {self.api_key}'},
                files=files,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

    def create_relationship(
        self,
        team_id: str,
        database_id: str,
        table_id: str,
        record_id: str,
        relation_field: str,
        related_record_id: str
    ) -> Dict[str, Any]:
        """
        Create a relationship between records.

        Args:
            team_id: Team ID
            database_id: Database ID
            table_id: Table ID
            record_id: Record ID
            relation_field: Relation field name
            related_record_id: Related record ID

        Returns:
            Update response
        """
        return self.update_record(
            team_id,
            database_id,
            table_id,
            record_id,
            {relation_field: [{'id': related_record_id}]}
        )

    def get_user_info(self) -> Dict[str, Any]:
        """Get current user information."""
        return self._request('GET', '/whoami')

    def list_webhooks(
        self,
        team_id: str,
        database_id: str
    ) -> List[Dict[str, Any]]:
        """List webhooks for a database."""
        return self._request('GET', f'/teams/{team_id}/databases/{database_id}/webhooks')

    def create_webhook(
        self,
        team_id: str,
        database_id: str,
        table_id: str,
        webhook_url: str,
        events: List[str],
        active: bool = True
    ) -> Dict[str, Any]:
        """
        Create a webhook.

        Args:
            team_id: Team ID
            database_id: Database ID
            table_id: Table ID
            webhook_url: Webhook URL
            events: List of events to monitor (create, update, delete)
            active: Whether webhook is active

        Returns:
            Webhook creation response
        """
        data = {
            'url': webhook_url,
            'tableId': table_id,
            'events': events,
            'active': active
        }
        return self._request('POST', f'/teams/{team_id}/databases/{database_id}/webhooks', json_data=data)

    def delete_webhook(
        self,
        team_id: str,
        database_id: str,
        webhook_id: str
    ) -> Dict[str, Any]:
        """Delete a webhook."""
        return self._request('DELETE', f'/teams/{team_id}/databases/{database_id}/webhooks/{webhook_id}')