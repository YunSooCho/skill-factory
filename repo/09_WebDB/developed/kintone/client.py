"""
Kintone API Client

This module provides a Python client for interacting with Kintone.
"""

import requests
from typing import Dict, List, Optional, Any
import json


class KintoneClient:
    """
    Client for Kintone REST API.

    Kintone provides:
    - Custom business apps
    - Database functionality
    - Process management
    - Notifications
    - Customization
    """

    def __init__(
        self,
        domain: str,
        api_token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 30
    ):
        """Initialize the Kintone client."""
        self.domain = domain.rstrip('/')
        self.api_token = api_token
        self.username = username
        self.password = password
        self.timeout = timeout
        self.session = requests.Session()

        self.session.headers.update({
            'Content-Type': 'application/json'
        })

        if api_token:
            self.session.headers['X-Cybozu-API-Token'] = api_token
        if username and password:
            self.session.auth = (username, password)

    def _request(
        self,
        method: str,
        endpoint: str,
        params=None,
        data=None,
        headers=None
    ) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"https://{self.domain}.kintone.com/k/v1{endpoint}"
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

    def get_record(
        self,
        app: int,
        id: int
    ) -> Dict[str, Any]:
        """Get a single record."""
        params = {'app': app, 'id': id}
        return self._request('GET', '/record', params=params)

    def get_records(
        self,
        app: int,
        query: str = "",
        fields: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get multiple records."""
        params = {
            'app': app,
            'query': query,
            'totalCount': 'true'
        }
        if fields:
            params['fields'] = json.dumps(fields)

        all_records = []
        current_offset = offset

        while True:
            params['query'] = f"{query} offset {current_offset} limit {limit}"
            response = self._request('GET', '/records', params=params)

            records = response.get('records', [])
            all_records.extend(records)

            if len(records) < limit:
                break

            current_offset += limit

        return {
            'records': all_records,
            'totalCount': len(all_records)
        }

    def add_record(
        self,
        app: int,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a single record."""
        data = {'app': app, 'record': record}
        return self._request('POST', '/record', data=data)

    def add_records(
        self,
        app: int,
        records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Add multiple records (up to 100)."""
        data = {'app': app, 'records': records}
        return self._request('POST', '/records', data=data)

    def update_record(
        self,
        app: int,
        id: int,
        record: Dict[str, Any],
        revision: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update a single record."""
        data = {'app': app, 'id': id, 'record': record}
        if revision:
            data['revision'] = revision
        return self._request('PUT', '/record', data=data)

    def update_records(
        self,
        app: int,
        records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Update multiple records (up to 100)."""
        data = {'app': app, 'records': records}
        return self._request('PUT', '/records', data=data)

    def delete_records(
        self,
        app: int,
        ids: List[int]
    ) -> Dict[str, Any]:
        """Delete multiple records (up to 100)."""
        data = {'app': app, 'ids': ids}
        return self._request('DELETE', '/records', data=data)

    def delete_record(
        self,
        app: int,
        id: int
    ) -> Dict[str, Any]:
        """Delete a single record."""
        data = {'app': app, 'id': id}
        return self._request('DELETE', '/record', data=data)

    def update_record_status(
        self,
        app: int,
        id: int,
        action: str,
        assignee: Optional[str] = None,
        revision: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update record status (workflow)."""
        data = {'app': app, 'id': id, 'action': action}
        if assignee:
            data['assignee'] = assignee
        if revision:
            data['revision'] = revision
        return self._request('PUT', '/record/status', data=data)

    def update_records_status(
        self,
        app: int,
        ids: List[int],
        action: str,
        assignee: Optional[str] = None,
        revision: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update multiple records status (workflow)."""
        data = {'app': app, 'ids': ids, 'action': action}
        if assignee:
            data['assignee'] = assignee
        if revision:
            data['revision'] = revision
        return self._request('PUT', '/records/status', data=data)

    def get_app(
        self,
        id: int
    ) -> Dict[str, Any]:
        """Get app details."""
        params = {'id': id}
        return self._request('GET', '/app', params=params)

    def get_apps(
        self,
        name: Optional[str] = None,
        code: Optional[str] = None,
        space_ids: Optional[List[int]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get list of apps."""
        params = {}
        if name:
            params['name'] = name
        if code:
            params['code'] = code
        if space_ids:
            params['spaceIds'] = json.dumps(space_ids)
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset

        response = self._request('GET', '/apps', params=params)
        return response.get('apps', [])

    def get_form_fields(
        self,
        app: int,
        lang: str = "default"
    ) -> Dict[str, Any]:
        """Get form fields."""
        params = {'app': app, 'lang': lang}
        return self._request('GET', '/app/form/fields', params=params)

    def get_form_layout(
        self,
        app: int,
        lang: str = "default"
    ) -> Dict[str, Any]:
        """Get form layout."""
        params = {'app': app, 'lang': lang}
        return self._request('GET', '/app/form/layout', params=params)

    def get_views(
        self,
        app: int,
        lang: str = "default"
    ) -> Dict[str, Any]:
        """Get app views."""
        params = {'app': app, 'lang': lang}
        return self._request('GET', '/app/views', params=params)

    def update_view_settings(
        self,
        app: int,
        view_id: str,
        view_settings: Dict[str, Any],
        revision: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update view settings."""
        data = {
            'app': app,
            'view_id': view_id,
            'view_settings': view_settings
        }
        if revision:
            data['revision'] = revision
        return self._request('PUT', '/app/views', data=data)

    def get_general_settings(self, app: str) -> Dict[str, Any]:
        """Get general settings."""
        params = {'app': app}
        return self._request('GET', '/app/settings', params=params)

    def update_general_settings(
        self,
        app: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        icon: Optional[Dict[str, Any]] = None,
        theme: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update general settings."""
        data = {'app': app}
        settings = {}
        if name:
            settings['name'] = name
        if description:
            settings['description'] = description
        if icon:
            settings['icon'] = icon
        if theme:
            settings['theme'] = theme
        data['settings'] = settings
        return self._request('PUT', '/app/settings', data=data)

    def get_acl(self, app: str) -> Dict[str, Any]:
        """Get access control list."""
        params = {'app': app}
        return self._request('GET', '/app/acl', params=params)

    def update_acl(
        self,
        app: str,
        rights: List[Dict[str, Any]],
        revision: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update access control list."""
        data = {
            'app': app,
            'rights': rights
        }
        if revision:
            data['revision'] = revision
        return self._request('PUT', '/app/acl', data=data)

    def get_field_acl(self, app: str) -> Dict[str, Any]:
        """Get field-level ACL."""
        params = {'app': app}
        return self._request('GET', '/app/acl/field', params=params)

    def update_field_acl(
        self,
        app: str,
        rights: List[Dict[str, Any]],
        revision: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update field-level ACL."""
        data = {
            'app': app,
            'rights': rights
        }
        if revision:
            data['revision'] = revision
        return self._request('PUT', '/app/acl/field', data=data)

    def get_space(self, id: int) -> Dict[str, Any]:
        """Get space details."""
        params = {'id': id}
        return self._request('GET', '/space', params=params)

    def get_spaces(
        self,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get list of spaces."""
        params = {'limit': limit}
        response = self._request('GET', '/space', params=params)
        return response.get('spaces', [])

    def add_comment(
        self,
        app: int,
        record: int,
        comment: Dict[str, Any],
        mentions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Add a comment to a record."""
        data = {
            'app': app,
            'record': record,
            'comment': comment
        }
        if mentions:
            data['mentions'] = mentions
        return self._request('POST', '/record/comment', data=data)

    def get_comments(
        self,
        app: int,
        record: int,
        order: str = "asc"
    ) -> List[Dict[str, Any]]:
        """Get comments for a record."""
        params = {'app': app, 'record': record, 'order': order}
        response = self._request('GET', '/record/comments', params=params)
        return response.get('comments', [])

    def delete_comment(
        self,
        app: int,
        record: int,
        comment: str
    ) -> Dict[str, Any]:
        """Delete a comment."""
        data = {'app': app, 'record': record, 'comment': comment}
        return self._request('DELETE', '/record/comment', data=data)

    def bulk_get_records(
        self,
        app: int,
        ids: List[int]
    ) -> Dict[str, Any]:
        """Get multiple records by IDs."""
        data = {'app': app, 'ids': ids}
        return self._request('GET', '/records', params=data)

    def upload_file(
        self,
        file_path: str,
        content_type: str = "application/octet-stream"
    ) -> str:
        """Upload a file to Kintone."""
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f, content_type)}
            headers = {'X-Cybozu-API-Token': self.api_token}
            response = requests.post(
                f"https://{self.domain}.kintone.com/k/v1/file",
                files=files,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()['fileKey']

    def download_file(self, file_key: str) -> bytes:
        """Download a file from Kintone."""
        headers = {'X-Cybozu-API-Token': self.api_token}
        response = requests.get(
            f"https://{self.domain}.kintone.com/k/v1/file",
            params={'fileKey': file_key},
            headers=headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.content

    def get_api_users(self) -> List[Dict[str, Any]]:
        """Get API users."""
        return self._request('GET', '/users')

    def get_api_user(self, code: str) -> Dict[str, Any]:
        """Get API user by code."""
        params = {'code': code}
        return self._request('GET', '/user', params=params)

    def get_organizations(
        self,
        code: Optional[str] = None,
        name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get organizations."""
        params = {}
        if code:
            params['code'] = code
        if name:
            params['name'] = name
        response = self._request('GET', '/organizations', params=params)
        return response.get('organizations', [])

    def get_users_in_group(self, code: str) -> List[Dict[str, Any]]:
        """Get users in a group."""
        params = {'code': code}
        response = self._request('GET', '/users', params=params)
        return response.get('users', [])

    def update_assignees(
        self,
        app: int,
        id: int,
        assignees: List[str],
        revision: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update assignees for a record."""
        data = {
            'app': app,
            'id': id,
            'assignees': assignees
        }
        if revision:
            data['revision'] = revision
        return self._request('PUT', '/record/assignees', data=data)

    def calculate_request_hash(self, url: str, method: str, headers: Dict[str, str]) -> str:
        """Calculate hash for request signing (for custom authentication)."""
        import hashlib
        import hmac

        api_key = self.api_token or f"{self.username}:{self.password}"

        payload = f"{method}\n{url}\n"
        for key in sorted(headers.keys()):
            payload += f"{key}:{headers[key]}\n"

        signature = hmac.new(
            api_key.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return signature