"""
Podio API Client

This module provides a Python client for interacting with Podio web database and collaboration platform.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class PodioClient:
    """
    Client for Podio Web Database Platform.

    Podio provides:
    - Work apps and item management
    - Task management with assignments
    - Comments and collaboration
    - App search and filtering
    - Workspace organization
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        username: str,
        password: str,
        base_url: str = "https://api.podio.com",
        timeout: int = 30
    ):
        """
        Initialize the Podio client.

        Args:
            client_id: Podio OAuth client ID
            client_secret: Podio OAuth client secret
            username: Podio username/email
            password: Podio password
            base_url: Base URL for the Podio API
            timeout: Request timeout in seconds
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

        self.session = requests.Session()
        self._access_token = None
        self._refresh_token = None
        self._token_expires_at = None

        # Authenticate
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Podio and get access token."""
        auth_url = "https://podio.com/oauth/token"
        data = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password
        }

        response = requests.post(auth_url, data=data, timeout=self.timeout)
        if response.status_code != 200:
            raise Exception(f"Authentication failed: {response.text}")

        token_data = response.json()
        self._access_token = token_data['access_token']
        self._refresh_token = token_data.get('refresh_token')
        self._token_expires_at = datetime.now().timestamp() + token_data.get('expires_in', 3600)

        self.session.headers.update({
            'Authorization': f'Bearer {self._access_token}',
            'Content-Type': 'application/json'
        })

    def _ensure_authenticated(self):
        """Ensure we have a valid access token."""
        if self._token_expires_at and datetime.now().timestamp() >= self._token_expires_at - 300:
            if self._refresh_token:
                self._refresh_access_token()
            else:
                self._authenticate()

    def _refresh_access_token(self):
        """Refresh the access token using refresh token."""
        refresh_url = "https://podio.com/oauth/token"
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self._refresh_token
        }

        response = requests.post(refresh_url, data=data, timeout=self.timeout)
        if response.status_code != 200:
            raise Exception(f"Token refresh failed: {response.text}")

        token_data = response.json()
        self._access_token = token_data['access_token']
        self._refresh_token = token_data.get('refresh_token')
        self._token_expires_at = datetime.now().timestamp() + token_data.get('expires_in', 3600)

        self.session.headers.update({
            'Authorization': f'Bearer {self._access_token}'
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
        self._ensure_authenticated()
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

    def get_workspaces(self) -> List[Dict[str, Any]]:
        """List all workspaces."""
        return self._request('GET', '/space')

    def get_workspace(self, space_id: int) -> Dict[str, Any]:
        """Get workspace details."""
        return self._request('GET', f'/space/{space_id}')

    def get_workspace_apps(self, space_id: int) -> List[Dict[str, Any]]:
        """List all apps in a workspace."""
        return self._request('GET', f'/app/space/{space_id}')

    def search_apps(self, query: str) -> List[Dict[str, Any]]:
        """Search for apps across all workspaces."""
        params = {'query': query}
        return self._request('GET', '/app/search', params=params)

    def get_app(self, app_id: int) -> Dict[str, Any]:
        """Get app details."""
        return self._request('GET', f'/app/{app_id}')

    def get_app_fields(self, app_id: int) -> List[Dict[str, Any]]:
        """Get all fields in an app."""
        return self._request('GET', f'/app/{app_id}/fields')

    def get_app_items(
        self,
        app_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all items in an app."""
        params = {}
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        if sort_by:
            params['sort_by'] = sort_by

        return self._request('GET', f'/item/app/{app_id}/', params=params)

    def filter_items(
        self,
        app_id: int,
        filters: Dict[str, Any],
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Filter items in an app based on criteria."""
        params = {}
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset

        return self._request('POST', f'/item/app/{app_id}/filter/', params=params, json_data=filters)

    def get_item(self, item_id: int) -> Dict[str, Any]:
        """Get item details."""
        return self._request('GET', f'/item/{item_id}')

    def add_item(
        self,
        app_id: int,
        fields: Dict[str, Any],
        external_id: Optional[str] = None,
        create_reference: Optional[bool] = True
    ) -> Dict[str, Any]:
        """Add a new item to an app."""
        data = {
            'fields': fields,
            'create_reference': create_reference
        }
        if external_id:
            data['external_id'] = external_id

        return self._request('POST', f'/item/app/{app_id}/', json_data=data)

    def update_item(
        self,
        item_id: int,
        fields: Dict[str, Any],
        revision: Optional[int] = None,
        silent: bool = False
    ) -> Dict[str, Any]:
        """Update an existing item."""
        data = {
            'fields': fields,
            'silent': silent
        }
        if revision:
            data['revision'] = revision

        return self._request('PUT', f'/item/{item_id}', json_data=data)

    def delete_item(self, item_id: int, silent: bool = True) -> Dict[str, Any]:
        """Delete an item."""
        params = {'silent': silent}
        return self._request('DELETE', f'/item/{item_id}', params=params)

    def clone_item(
        self,
        item_id: int,
        app_id: Optional[int] = None,
        hook: bool = False,
        silent: bool = False
    ) -> Dict[str, Any]:
        """Clone an item."""
        data = {'hook': hook, 'silent': silent}
        if app_id:
            data['app'] = app_id

        return self._request('POST', f'/item/{item_id}/clone', json_data=data)

    def get_item_comments(self, item_id: int) -> List[Dict[str, Any]]:
        """Get all comments on an item."""
        return self._request('GET', f'/comment/item/{item_id}')

    def get_comment(self, comment_id: int) -> Dict[str, Any]:
        """Get comment details."""
        return self._request('GET', f'/comment/{comment_id}')

    def add_comment(
        self,
        item_id: int,
        text: str,
        external_id: Optional[str] = None,
        file_ids: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """Add a comment to an item."""
        data = {
            'value': text,
            'text': text
        }
        if external_id:
            data['external_id'] = external_id
        if file_ids:
            data['file_ids'] = file_ids

        return self._request('POST', f'/comment/item/{item_id}', json_data=data)

    def update_comment(
        self,
        comment_id: int,
        text: str
    ) -> Dict[str, Any]:
        """Update a comment."""
        data = {
            'value': text,
            'text': text
        }
        return self._request('PUT', f'/comment/{comment_id}', json_data=data)

    def delete_comment(self, comment_id: int) -> Dict[str, Any]:
        """Delete a comment."""
        return self._request('DELETE', f'/comment/{comment_id}')

    def get_task(self, task_id: int) -> Dict[str, Any]:
        """Get task details."""
        return self._request('GET', f'/task/{task_id}')

    def get_tasks(
        self,
        space_id: Optional[int] = None,
        organization_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """List tasks."""
        params = {}
        if space_id:
            params['space'] = space_id
        if organization_id:
            params['org'] = organization_id

        return self._request('GET', '/task/', params=params)

    def create_task(
        self,
        text: str,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        responsible: Optional[int] = None,
        private: bool = False,
        space_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create a new task."""
        data = {
            'text': text,
            'private': private
        }
        if description:
            data['description'] = description
        if due_date:
            data['due_date'] = due_date
        if responsible:
            data['responsible'] = responsible
        if space_id:
            data['space'] = space_id

        return self._request('POST', '/task/', json_data=data)

    def update_task(
        self,
        task_id: int,
        text: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        status: Optional[str] = None,
        private: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update a task."""
        data = {}
        if text:
            data['text'] = text
        if description:
            data['description'] = description
        if due_date:
            data['due_date'] = due_date
        if status:
            data['status'] = status
        if private is not None:
            data['private'] = private

        return self._request('PUT', f'/task/{task_id}', json_data=data)

    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """Delete a task."""
        return self._request('DELETE', f'/task/{task_id}')

    def assign_task(
        self,
        task_id: int,
        user_id: int,
        text: Optional[str] = None
    ) -> Dict[str, Any]:
        """Assign a task to a user."""
        data = {'responsible': user_id}
        if text:
            data['text'] = text

        return self._request('PUT', f'/task/{task_id}', json_data=data)

    def complete_task(self, task_id: int) -> Dict[str, Any]:
        """Mark a task as completed."""
        return self._request('POST', f'/task/{task_id}/complete')

    def incomplete_task(self, task_id: int) -> Dict[str, Any]:
        """Mark a task as incomplete."""
        return self._request('POST', f'/task/{task_id}/incomplete')

    def create_task_label(
        self,
        task_id: int,
        text: str,
        color: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a label for a task."""
        data = {'text': text}
        if color:
            data['color'] = color

        return self._request('POST', f'/task/{task_id}/label/', json_data=data)

    def get_relationships(
        self,
        app_id: int,
        item_id: int,
        field_id: int
    ) -> List[Dict[str, Any]]:
        """Get related items."""
        return self._request('GET', f'/item/{item_id}/relationship/{field_id}')

    def get_organization(self, org_id: int) -> Dict[str, Any]:
        """Get organization details."""
        return self._request('GET', f'/org/{org_id}')

    def get_organizations(self) -> List[Dict[str, Any]]:
        """List all organizations."""
        return self._request('GET', '/org')

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get user details."""
        return self._request('GET', f'/user/{user_id}')

    def get_current_user(self) -> Dict[str, Any]:
        """Get current user details."""
        return self._request('GET', '/user/status')

    def get_activity_stream(
        self,
        object_type: str,
        object_id: int,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get activity stream for an object."""
        params = {}
        if limit:
            params['limit'] = limit

        return self._request('GET', f'/stream/{object_type}/{object_id}/', params=params)