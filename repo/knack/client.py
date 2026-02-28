"""
Knack API Client

This module provides a Python client for interacting with Knack.
"""

import requests
from typing import Dict, List, Optional, Any
import json


class KnackClient:
    """
    Client for Knack REST API.

    Knack provides:
    - Online database applications
    - Custom interfaces
    - Workflows and automation
    - API access
    - User permissions
    """

    def __init__(
        self,
        app_id: str,
        api_key: str,
        base_url: str = "https://api.knack.com/v1",
        timeout: int = 30
    ):
        """Initialize the Knack client."""
        self.app_id = app_id
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'X-Knack-Application-Id': app_id,
            'X-Knack-REST-API-Key': api_key,
            'Content-Type': 'application/json',
            'Knack-Application-Id': app_id
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        params=None,
        data=None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
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
        response.raise_for_status()

        if response.text:
            return response.json()
        return {}

    def get_objects(self) -> List[Dict[str, Any]]:
        """Get all objects in the application."""
        response = self._request('GET', '/objects')
        return response.get('objects', [])

    def get_object(self, object_key: str) -> Dict[str, Any]:
        """Get object details."""
        return self._request('GET', f'/objects/{object_key}')

    def get_records(
        self,
        object_key: str,
        rows_per_page: int = 100,
        page: int = 1,
        filters: Optional[List[Dict[str, Any]]] = None,
        format: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get records from an object."""
        params = {'rows_per_page': rows_per_page, 'page': page}
        if format:
            params['format'] = format

        url = f'/objects/{object_key}/records'
        if filters:
            payload = {'filters': filters}
            return self._request('POST', url, data=payload)

        return self._request('GET', url, params=params)

    def get_all_records(
        self,
        object_key: str,
        format: Optional[str] = None,
        sort_field: Optional[str] = None,
        sort_order: str = "asc"
    ) -> List[Dict[str, Any]]:
        """Get all records with pagination."""
        all_records = []
        page = 1
        total_pages = 1

        while page <= total_pages:
            response = self.get_records(
                object_key,
                rows_per_page=1000,
                page=page,
                format=format
            )

            records = response.get('records', [])
            all_records.extend(records)

            total_records = response.get('total_records', 0)
            total_pages = (total_records + 999) // 1000
            page += 1

        return all_records

    def get_record(
        self,
        object_key: str,
        record_id: str
    ) -> Dict[str, Any]:
        """Get a single record."""
        return self._request('GET', f'/objects/{object_key}/records/{record_id}')

    def create_record(
        self,
        object_key: str,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new record."""
        return self._request('POST', f'/objects/{object_key}/records', data=record)

    def update_record(
        self,
        object_key: str,
        record_id: str,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a record."""
        return self._request('PUT', f'/objects/{object_key}/records/{record_id}', data=record)

    def delete_record(
        self,
        object_key: str,
        record_id: str
    ) -> Dict[str, Any]:
        """Delete a record."""
        return self._request('DELETE', f'/objects/{object_key}/records/{record_id}')

    def search_records(
        self,
        object_key: str,
        field_key: str,
        search_term: str
    ) -> List[Dict[str, Any]]:
        """Search records by field value."""
        response = self.get_records(
            object_key,
            filters=[{
                'field': field_key,
                'operator': 'contains',
                'value': search_term
            }]
        )
        return response.get('records', [])

    def get_views(self, object_key: str) -> List[Dict[str, Any]]:
        """Get all views for an object."""
        return self.get_object(object_key).get('views', [])

    def get_view(
        self,
        object_key: str,
        view_keys: List[str]
    ) -> Dict[str, Any]:
        """Get specific views."""
        url = f'/objects/{object_key}/views'
        return self._request('GET', url, params={'view_keys': ','.join(view_keys)})

    def upload_file(
        self,
        object_key: str,
        file_path: str,
        field_key: str,
        record_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload a file to Knack."""
        with open(file_path, 'rb') as f:
            files = {'files': f}
            url = self.base_url + f'/objects/{object_key}/files'
            response = requests.post(
                url,
                files=files,
                headers={
                    'X-Knack-Application-Id': self.app_id,
                    'X-Knack-REST-API-Key': self.api_key,
                    'Knack-Application-Id': self.app_id
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

    def download_file(self, file_url: str) -> bytes:
        """Download a file from Knack."""
        response = requests.get(
            file_url,
            headers={
                'X-Knack-Application-Id': self.app_id,
                'X-Knack-REST-API-Key': self.api_key
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.content

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user details."""
        return self._request('GET', f'/users/{user_id}')

    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        response = self._request('GET', '/users')
        return response.get('users', [])

    def get_scene(self, scene_key: str) -> Dict[str, Any]:
        """Get scene details."""
        return self._request('GET', f'/scenes/{scene_key}')

    def get_scenes(self) -> List[Dict[str, Any]]:
        """Get all scenes."""
        response = self._request('GET', '/scenes')
        return response.get('scenes', [])

    def get_account(self) -> Dict[str, Any]:
        """Get account details."""
        return self._request('GET', '/account')

    def create_user(
        self,
        object_key: str,
        user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new user."""
        return self.create_record(object_key, user_data)

    def login(
        self,
        object_key: str,
        email: str,
        password: str
    ) -> Dict[str, Any]:
        """Login a user."""
        data = {
            'email': email,
            'password': password
        }
        return self._request('POST', f'/objects/{object_key}/records/login', data=data)

    def logout(self, session_key: str) -> Dict[str, Any]:
        """Logout a user."""
        headers = {'Authorization': session_key}
        return self._request('POST', '/logout', headers=headers)

    def reset_password(
        self,
        object_key: str,
        email_field: str,
        email: str
    ) -> Dict[str, Any]:
        """Reset user password."""
        data = {
            'email': email,
            'email_field': email_field
        }
        return self._request('POST', f'/objects/{object_key}/records/password/reset', data=data)

    def get_webhooks(self) -> List[Dict[str, Any]]:
        """Get all webhooks."""
        response = self._request('GET', '/webhooks')
        return response.get('webhooks', [])

    def trigger_webhook(
        self,
        object_key: str,
        record_id: str
    ) -> Dict[str, Any]:
        """Trigger webhook for a record."""
        return self._request('POST', f'/objects/{object_key}/records/{record_id}/webhooks')

    def get_connections(self) -> List[Dict[str, Any]]:
        """Get all connections."""
        response = self._request('GET', '/connections')
        return response.get('connections', [])

    def search_all(
        self,
        search_term: str,
        object_keys: Optional[List[str]] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Search across multiple objects."""
        results = {}

        objects = self.get_objects()
        target_objects = [
            obj for obj in objects
            if not object_keys or obj.get('key') in object_keys
        ]

        for obj in target_objects:
            obj_key = obj.get('key')
            try:
                records = self.get_records(
                    obj_key,
                    filters=[{
                        'operator': 'contains',
                        'field': 'name',
                        'value': search_term
                    }]
                )
                if records.get('records'):
                    results[obj_key] = records['records']
            except Exception:
                continue

        return results

    def batch_create(
        self,
        object_key: str,
        records: List[Dict[str, Any]],
        batch_size: int = 50
    ) -> List[Dict[str, Any]]:
        """Batch create records."""
        results = []
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            for record in batch:
                results.append(self.create_record(object_key, record))
        return results

    def batch_update(
        self,
        object_key: str,
        updates: List[Dict[str, Any]],
        batch_size: int = 50
    ) -> List[Dict[str, Any]]:
        """Batch update records."""
        results = []
        for i in range(0, len(updates), batch_size):
            batch = updates[i:i + batch_size]
            for update in batch:
                record_id = update.pop('id')
                results.append(self.update_record(object_key, record_id, update))
        return results

    def batch_delete(
        self,
        object_key: str,
        record_ids: List[str],
        batch_size: int = 50
    ) -> List[Dict[str, Any]]:
        """Batch delete records."""
        results = []
        for i in range(0, len(record_ids), batch_size):
            batch = record_ids[i:i + batch_size]
            for record_id in batch:
                results.append(self.delete_record(object_key, record_id))
        return results

    def get_form(self, form_key: str) -> Dict[str, Any]:
        """Get form details."""
        return self._request('GET', f'/forms/{form_key}')

    def submit_form(
        self,
        form_key: str,
        form_data: Dict[str, Any],
        api_key_for_submission: Optional[str] = None
    ) -> Dict[str, Any]:
        """Submit a form."""
        headers = {}
        if api_key_for_submission:
            headers = {
                'X-Knack-REST-API-Key': api_key_for_submission
            }

        return self._request('POST', f'/forms/{form_key}', data=form_data, headers=headers)