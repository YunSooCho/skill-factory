"""
Airtable OAuth API Client

This module provides a Python client for interacting with Airtable
using OAuth 2.0 authentication for secure access.
"""

import requests
from typing import Dict, List, Optional, Any
import json
import base64
import hashlib
import secrets
from urllib.parse import urlencode


class AirtableOAuthClient:
    """
    Client for Airtable OAuth 2.0 integration.

    Provides OAuth 2.0 authentication and access to Airtable bases.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        base_url: str = "https://api.airtable.com/v0",
        timeout: int = 30
    ):
        """Initialize the Airtable OAuth client."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None

    def get_authorization_url(
        self,
        state: Optional[str] = None,
        scopes: Optional[List[str]] = None
    ) -> str:
        """Generate OAuth authorization URL."""
        if state is None:
            state = secrets.token_urlsafe(32)

        if scopes is None:
            scopes = ['data.records:read', 'data.records:write', 'schema.bases:read']

        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(scopes),
            'state': state
        }

        auth_url = "https://airtable.com/oauth2/v1/authorize"
        return f"{auth_url}?{urlencode(params)}"

    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token."""
        response = requests.post(
            "https://airtable.com/oauth2/v1/token",
            data={
                'grant_type': 'authorization_code',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': code,
                'redirect_uri': self.redirect_uri
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        token_data = response.json()

        self.access_token = token_data.get('access_token')
        self.refresh_token = token_data.get('refresh_token')

        return token_data

    def refresh_access_token(self) -> Dict[str, Any]:
        """Refresh access token using refresh token."""
        if not self.refresh_token:
            raise ValueError("No refresh token available")

        response = requests.post(
            "https://airtable.com/oauth2/v1/token",
            data={
                'grant_type': 'refresh_token',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': self.refresh_token
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        token_data = response.json()

        self.access_token = token_data.get('access_token')
        if 'refresh_token' in token_data:
            self.refresh_token = token_data['refresh_token']

        return token_data

    def set_access_token(self, access_token: str):
        """Set access token directly (for already authenticated sessions)."""
        self.access_token = access_token

    def set_refresh_token(self, refresh_token: str):
        """Set refresh token directly."""
        self.refresh_token = refresh_token

    def _request_headers(self) -> Dict[str, str]:
        """Get request headers with OAuth token."""
        if not self.access_token:
            raise ValueError("No access token. Please authenticate first.")
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def get_bases(self) -> List[Dict[str, Any]]:
        """Get list of accessible bases."""
        response = requests.get(
            f"{self.base_url}/meta/bases",
            headers=self._request_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json().get('bases', [])

    def get_base(self, base_id: str) -> Dict[str, Any]:
        """Get base details."""
        response = requests.get(
            f"{self.base_url}/meta/bases/{base_id}",
            headers=self._request_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def get_tables(self, base_id: str) -> List[Dict[str, Any]]:
        """Get tables in a base."""
        response = requests.get(
            f"{self.base_url}/meta/bases/{base_id}/tables",
            headers=self._request_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json().get('tables', [])

    def get_records(
        self,
        base_id: str,
        table_id: str,
        max_records: int = 100,
        page_size: int = 100,
        sort: Optional[List[Dict[str, str]]] = None,
        filter_by_formula: Optional[str] = None,
        view: Optional[str] = None,
        offset: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get records from a table."""
        params = {'maxRecords': max_records, 'pageSize': page_size}
        if sort:
            params['sort'] = json.dumps(sort)
        if filter_by_formula:
            params['filterByFormula'] = filter_by_formula
        if view:
            params['view'] = view
        if offset:
            params['offset'] = offset

        response = requests.get(
            f"{self.base_url}/{base_id}/{table_id}",
            headers=self._request_headers(),
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def get_record(self, base_id: str, table_id: str, record_id: str) -> Dict[str, Any]:
        """Get a single record."""
        response = requests.get(
            f"{self.base_url}/{base_id}/{table_id}/{record_id}",
            headers=self._request_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def create_record(
        self,
        base_id: str,
        table_id: str,
        fields: Dict[str, Any],
        typecast: bool = False
    ) -> Dict[str, Any]:
        """Create a new record."""
        data = {'fields': fields, 'typecast': typecast}
        response = requests.post(
            f"{self.base_url}/{base_id}/{table_id}",
            headers=self._request_headers(),
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def update_record(
        self,
        base_id: str,
        table_id: str,
        record_id: str,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a record (partial update)."""
        data = {'fields': fields}
        response = requests.patch(
            f"{self.base_url}/{base_id}/{table_id}/{record_id}",
            headers=self._request_headers(),
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def replace_record(
        self,
        base_id: str,
        table_id: str,
        record_id: str,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Replace all fields in a record."""
        data = {'fields': fields}
        response = requests.put(
            f"{self.base_url}/{base_id}/{table_id}/{record_id}",
            headers=self._request_headers(),
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def delete_record(self, base_id: str, table_id: str, record_id: str) -> Dict[str, Any]:
        """Delete a record."""
        response = requests.delete(
            f"{self.base_url}/{base_id}/{table_id}/{record_id}",
            headers=self._request_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def create_records(
        self,
        base_id: str,
        table_id: str,
        records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create multiple records (batch)."""
        data = {'records': records, 'typecast': True}
        response = requests.post(
            f"{self.base_url}/{base_id}/{table_id}",
            headers=self._request_headers(),
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def update_records(
        self,
        base_id: str,
        table_id: str,
        records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Update multiple records (batch)."""
        data = {'records': records}
        response = requests.patch(
            f"{self.base_url}/{base_id}/{table_id}",
            headers=self._request_headers(),
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def delete_records(
        self,
        base_id: str,
        table_id: str,
        record_ids: List[str]
    ) -> Dict[str, Any]:
        """Delete multiple records (batch)."""
        params = {'records': record_ids}
        response = requests.delete(
            f"{self.base_url}/{base_id}/{table_id}",
            headers=self._request_headers(),
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def upload_attachment(
        self,
        base_id: str,
        table_id: str,
        record_id: str,
        field_name: str,
        file_path: str
    ) -> Dict[str, Any]:
        """Upload an attachment to a record."""
        record = self.get_record(base_id, table_id, record_id)
        existing_attachments = record['fields'].get(field_name, [])

        with open(file_path, 'rb') as f:
            files = {'file': f}
            upload_response = requests.post(
                f"https://content.airtable.com/v0/{base_id}/{table_id}/{record_id}",
                headers={'Authorization': f'Bearer {self.access_token}'},
                files=files,
                timeout=self.timeout
            )

        upload_response.raise_for_status()
        attachment_data = upload_response.json()

        existing_attachments.append(attachment_data)
        return self.update_record(base_id, table_id, record_id, {field_name: existing_attachments})

    def query(
        self,
        base_id: str,
        table_id: str,
        max_records: int = 100,
        fields: Optional[List[str]] = None,
        sort: Optional[List[Dict[str, str]]] = None,
        formula: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Query records with advanced filtering."""
        result = self.get_records(
            base_id,
            table_id,
            max_records=max_records,
            sort=sort,
            filter_by_formula=formula
        )
        return result.get('records', [])

    def get_schema(self, base_id: str) -> Dict[str, Any]:
        """Get base schema including tables and fields."""
        response = requests.get(
            f"{self.base_url}/meta/bases/{base_id}/tables",
            headers=self._request_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()