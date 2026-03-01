"""
Figma REST API Client

This module provides a Python client for interacting with the Figma REST API.
Figma API allows access to design files, components, comments, users, and more.

API Documentation: https://developers.figma.com/docs/rest-api/
"""

import requests
from typing import Optional, Dict, Any, List
import json


class FigmaClient:
    """
    Client for interacting with the Figma REST API.
    """

    BASE_URL = "https://api.figma.com/v1"

    def __init__(self, access_token: str):
        """
        Initialize the Figma client.

        Args:
            access_token: Your Figma personal access token or OAuth token
        """
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "X-Figma-Token": access_token,
            "Content-Type": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a request to the Figma API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
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
                error_msg += f": {error_data.get('message', '')}"
            except:
                error_msg += f": {response.text}"
            raise requests.exceptions.RequestException(error_msg)

        return response.json()

    # File Endpoints

    def get_file(self, file_key: str, version: Optional[str] = None,
                 ids: Optional[List[str]] = None, depth: Optional[int] = None,
                 geometry: Optional[str] = None) -> Dict[str, Any]:
        """
        Get details of a file.

        Args:
            file_key: The key of the file to access
            version: A specific version to fetch
            ids: A list of node IDs to return
            depth: Integer between 1 and 2 (depth of tree traversal)
            geometry: Whether to return geometry data ('paths' or 'true')

        Returns:
            File data including pages and nodes
        """
        params = {}
        if version:
            params['version'] = version
        if ids:
            params['ids'] = ','.join(ids)
        if depth:
            params['depth'] = depth
        if geometry:
            params['geometry'] = geometry

        return self._make_request('GET', f'/files/{file_key}', params=params)

    def get_file_nodes(self, file_key: str, ids: List[str],
                      depth: Optional[int] = None,
                      geometry: Optional[str] = None) -> Dict[str, Any]:
        """
        Getspecific nodes from a file.

        Args:
            file_key: The key of the file to access
            ids: A list of node IDs to fetch
            depth: Integer between 1 and 2
            geometry: Whether to return geometry data ('paths' or 'true')

        Returns:
            Node data for the specified IDs
        """
        params = {'ids': ','.join(ids)}
        if depth:
            params['depth'] = depth
        if geometry:
            params['geometry'] = geometry

        return self._make_request('GET', f'/files/{file_key}/nodes', params=params)

    def get_image(self, file_key: str, ids: List[str],
                  format: str = 'png', scale: float = 1.0,
                  version: Optional[str] = None) -> Dict[str, str]:
        """
        Get image URLs for nodes in a file.

        Args:
            file_key: The key of the file
            ids: A list of node IDs to render
            format: Image format ('png', 'jpg', 'svg', 'pdf')
            scale: Multiplier for image resolution
            version: Specific file version

        Returns:
            Dictionary mapping node IDs to image URLs
        """
        params = {
            'ids': ','.join(ids),
            'format': format,
            'scale': str(scale)
        }
        if version:
            params['version'] = version

        return self._make_request('GET', f'/images/{file_key}', params=params)

    def get_image_figma(self, file_key: str, ids: List[str],
                        version: Optional[str] = None) -> Dict[str, str]:
        """
        Get Figma image URLs for nodes.

        Args:
            file_key: The key of the file
            ids: A list of node IDs
            version: Specific file version

        Returns:
            Dictionary mapping node IDs to Figma image URLs
        """
        params = {'ids': ','.join(ids)}
        if version:
            params['version'] = version

        return self._make_request('GET', f'/images/{file_key}/figma', params=params)

    # Version History Endpoints

    def get_file_versions(self, file_key: str) -> List[Dict[str, Any]]:
        """
        Get version history for a file.

        Args:
            file_key: The key of the file

        Returns:
            List of version data
        """
        response = self._make_request('GET', f'/files/{file_key}/versions')
        return response.get('versions', [])

    # Comment Endpoints

    def get_comments(self, file_key: str) -> List[Dict[str, Any]]:
        """
        Get all comments on a file.

        Args:
            file_key: The key of the file

        Returns:
            List of comment data
        """
        response = self._make_request('GET', f'/files/{file_key}/comments')
        return response.get('comments', [])

    def post_comment(self, file_key: str, message: str,
                    client_meta: Optional[Dict[str, Any]] = None,
                    comment_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Post a comment to a file.

        Args:
            file_key: The key of the file
            message: The comment message text
            client_meta: Position data for the comment
            comment_id: Parent comment ID for replies

        Returns:
            The created comment data
        """
        data = {
            'message': message,
            'client_meta': client_meta
        }
        if comment_id:
            data['comment_id'] = comment_id

        return self._make_request('POST', f'/files/{file_key}/comments', json=data)

    def delete_comment(self, file_key: str, comment_id: str) -> None:
        """
        Delete a comment from a file.

        Args:
            file_key: The key of the file
            comment_id: The ID of the comment to delete
        """
        self._make_request('DELETE', f'/files/{file_key}/comments/{comment_id}')

    # User Endpoints

    def get_me(self) -> Dict[str, Any]:
        """
        Get information about the authenticated user.

        Returns:
            User data
        """
        return self._make_request('GET', '/me')

    def get_users(self, user_ids: List[str]) -> Dict[str, Any]:
        """
        Get information about specific users.

        Args:
            user_ids: List of user IDs to fetch

        Returns:
            User data for the specified IDs
        """
        params = {'ids': ','.join(user_ids)}
        return self._make_request('GET', '/users', params=params)

    # Project Endpoints

    def get_team_projects(self, team_id: str) -> List[Dict[str, Any]]:
        """
        Get all projects for a team.

        Args:
            team_id: The ID of the team

        Returns:
            List of project data
        """
        response = self._make_request('GET', f'/teams/{team_id}/projects')
        return response.get('projects', [])

    def get_project_files(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get all files in a project.

        Args:
            project_id: The ID of the project

        Returns:
            List of file data
        """
        response = self._make_request('GET', f'/projects/{project_id}/files')
        return response.get('files', [])

    # Component Endpoints

    def get_components(self, file_key: str) -> List[Dict[str, Any]]:
        """
        Get all components from a file.

        Args:
            file_key: The key of the file

        Returns:
            List of component data
        """
        response = self._make_request('GET', f'/files/{file_key}/components')
        return response.get('components', [])

    def get_component_sets(self, file_key: str) -> List[Dict[str, Any]]:
        """
        Get all component sets from a file.

        Args:
            file_key: The key of the file

        Returns:
            List of component set data
        """
        response = self._make_request('GET', f'/files/{file_key}/component_sets')
        return response.get('component_sets', [])

    def get_styles(self, file_key: str) -> List[Dict[str, Any]]:
        """
        Get all styles from a file.

        Args:
            file_key: The key of the file

        Returns:
            List of style data
        """
        response = self._make_request('GET', f'/files/{file_key}/styles')
        return response.get('styles', [])

    # Variables Endpoints

    def get_variable_consumers(self, file_key: str,
                                 variable_ids: Optional[List[str]] = None,
                                 mode_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get consumers of variables in a file.

        Args:
            file_key: The key of the file
            variable_ids: Optional list of variable IDs
            mode_ids: Optional list of mode IDs

        Returns:
            Variable consumer data
        """
        params = {}
        if variable_ids:
            params['variable_ids'] = ','.join(variable_ids)
        if mode_ids:
            params['mode_ids'] = ','.join(mode_ids)

        return self._make_request('GET', f'/files/{file_key}/variables/consumers', params=params)

    def get_local_variable_modes(self, file_key: str) -> List[Dict[str, Any]]:
        """
        Get local variable modes for a file.

        Args:
            file_key: The key of the file

        Returns:
            List of variable mode data
        """
        response = self._make_request('GET', f'/files/{file_key}/variables/modes/local')
        return response.get('modes', [])

    def get_library_variable_modes(self) -> List[Dict[str, Any]]:
        """
        Get library variable modes for the user.

        Returns:
            List of variable mode data
        """
        response = self._make_request('GET', '/library/variables/modes')
        return response.get('modes', [])

    # Dev Resources Endpoints

    def get_dev_resources(self, file_key: str) -> Dict[str, Any]:
        """
        Get all developer resources for a file.

        Args:
            file_key: The key of the file

        Returns:
            Dev resource data
        """
        return self._make_request('GET', f'/files/{file_key}/dev_resources')

    def get_dev_resource(self, file_key: str, resource_key: str) -> Dict[str, Any]:
        """
        Get a specific developer resource.

        Args:
            file_key: The key of the file
            resource_key: The key of the resource

        Returns:
            Dev resource data
        """
        return self._make_request('GET', f'/files/{file_key}/dev_resources/{resource_key}')

    # Activity Logs Endpoints

    def get_activity_logs(self, team_id: str, limit: int = 100,
                         start: Optional[str] = None,
                         end: Optional[str] = None,
                         cursor: Optional[str] = None) -> Dict[str, Any]:
        """
        Get activity logs for a team.

        Args:
            team_id: The ID of the team
            limit: Maximum number of logs to return (default: 100)
            start: Start time ISO 8601 format
            end: End time ISO 8601 format
            cursor: Cursor for pagination

        Returns:
            Activity log data
        """
        params = {'limit': str(limit)}
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        if cursor:
            params['cursor'] = cursor

        return self._make_request('GET', f'/teams/{team_id}/activity_logs', params=params)

    # Discovery Endpoints

    def get_text_events(self, team_id: str,
                       since_date: str,
                       until_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get text editing events for a team.

        Args:
            team_id: The ID of the team
            since_date: Start date (YYYY-MM-DD)
            until_date: End date (YYYY-MM-DD)

        Returns:
            Text events data
        """
        params = {'since_date': since_date}
        if until_date:
            params['until_date'] = until_date

        return self._make_request('GET', f'/teams/{team_id}/text_events', params=params)

    # Webhooks Endpoints

    def create_webhook(self, team_id: str, endpoint: str,
                      events: List[str],
                      description: Optional[str] = None,
                      region: str = 'US') -> Dict[str, Any]:
        """
        Create a webhook for a team.

        Args:
            team_id: The ID of the team
            endpoint: The webhook URL to receive events
            events: List of event types (e.g., 'FILE_COMMENT', 'FILE_UPDATE')
            description: Optional webhook description
            region: Data residency region ('US', 'EU')

        Returns:
            Created webhook data
        """
        data = {
            'endpoint': endpoint,
            'team_id': team_id,
            'events': events
        }
        if description:
            data['description'] = description
        if region:
            data['region'] = region

        return self._make_request('POST', '/webhooks', json=data)

    def get_webhooks(self, team_id: str) -> List[Dict[str, Any]]:
        """
        Get all webhooks for a team.

        Args:
            team_id: The ID of the team

        Returns:
            List of webhook data
        """
        params = {'team_id': team_id}
        response = self._make_request('GET', '/webhooks', params=params)
        return response.get('webhooks', [])

    def delete_webhook(self, webhook_id: str) -> None:
        """
        Delete a webhook.

        Args:
            webhook_id: The ID of the webhook to delete
        """
        self._make_request('DELETE', f'/webhooks/{webhook_id}')

    def close(self):
        """
        Close the session.
        """
        self.session.close()