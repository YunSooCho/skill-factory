"""
Hex API Client

This module provides a Python client for interacting with Hex.
"""

import requests
from typing import Dict, List, Optional, Any
import json


class HexClient:
    """
    Client for Hex Data Platform API.

    Hex provides:
    - Interactive data science notebooks
    - SQL and Python support
    - Data visualization
    - App building
    - Data sharing
    """

    def __init__(
        self,
        api_key: str,
        workspace_id: str,
        base_url: str = "https://app.hex.tech/api/v1",
        timeout: int = 30
    ):
        """Initialize the Hex client."""
        self.api_key = api_key
        self.workspace_id = workspace_id
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
        data=None
    ) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(
            method,
            url,
            params=params,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects in workspace."""
        return self._request('GET', f'/workspace/{self.workspace_id}/projects')

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project details."""
        return self._request('GET', f'/workspace/{self.workspace_id}/projects/{project_id}')

    def create_project(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new project."""
        data = {'name': name}
        if description:
            data['description'] = description
        return self._request('POST', f'/workspace/{self.workspace_id}/projects', data=data)

    def update_project(
        self,
        project_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update a project."""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        return self._request('PATCH', f'/workspace/{self.workspace_id}/projects/{project_id}', data=data)

    def delete_project(self, project_id: str) -> None:
        """Delete a project."""
        self._request('DELETE', f'/workspace/{self.workspace_id}/projects/{project_id}')

    def list_projects_in_folder(self, folder_id: str) -> List[Dict[str, Any]]:
        """List projects in a folder."""
        return self._request('GET', f'/workspace/{self.workspace_id}/folders/{folder_id}/projects')

    def get_logical_id(self, project_id: str) -> str:
        """Get logical ID for a project."""
        project = self.get_project(project_id)
        return project.get('logicalId', project_id)

    def read_project_file(self, project_id: str, path: str) -> Dict[str, Any]:
        """Read a file from project."""
        logical_id = self.get_logical_id(project_id)
        return self._request('GET', f'/workspace/{self.workspace_id}/projects/{logical_id}/file', params={'path': path})

    def write_project_file(
        self,
        project_id: str,
        path: str,
        content: str
    ) -> Dict[str, Any]:
        """Write a file to project."""
        logical_id = self.get_logical_id(project_id)
        return self._request('POST', f'/workspace/{self.workspace_id}/projects/{logical_id}/file', data={'path': path, 'content': content})

    def project_executions(
        self,
        project_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get project execution history."""
        logical_id = self.get_logical_id(project_id)
        return self._request('GET', f'/workspace/{self.workspace_id}/projects/{logical_id}/executions', params={'limit': limit})

    def list_runs(
        self,
        project_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """List project runs."""
        return self.project_executions(project_id, limit)

    def get_run(self, project_id: str, run_id: str) -> Dict[str, Any]:
        """Get details of a specific run."""
        logical_id = self.get_logical_id(project_id)
        return self._request('GET', f'/workspace/{self.workspace_id}/projects/{logical_id}/runs/{run_id}')

    def sync_logic(
        self,
        project_id: str,
        app_file_path: str = "logic/0_project_hex_logic.ts"
    ) -> Dict[str, Any]:
        """Sync logic file to project."""
        logical_id = self.get_logical_id(project_id)
        return self._request('POST', f'/workspace/{self.workspace_id}/projects/{logical_id}/projectFiles/sync', data={'path': app_file_path})

    def enable_project(
        self,
        project_id: str
    ) -> Dict[str, Any]:
        """Enable a project."""
        logical_id = self.get_logical_id(project_id)
        return self._request('POST', f'/workspace/{self.workspace_id}/projects/{logical_id}/enable')

    def list_data_sources(self) -> List[Dict[str, Any]]:
        """List all data sources."""
        return self._request('GET', f'/workspace/{self.workspace_id}/datasources')

    def get_data_source(self, source_id: str) -> Dict[str, Any]:
        """Get data source details."""
        return self._request('GET', f'/workspace/{self.workspace_id}/datasources/{source_id}')

    def create_data_source(
        self,
        name: str,
        source_type: str,
        connection_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new data source."""
        data = {
            'name': name,
            'type': source_type,
            'connectionParams': connection_params
        }
        return self._request('POST', f'/workspace/{self.workspace_id}/datasources', data=data)

    def test_data_source_connection(self, source_id: str) -> Dict[str, Any]:
        """Test data source connection."""
        return self._request('POST', f'/workspace/{self.workspace_id}/datasources/{source_id}/testConnection')

    def update_data_source(
        self,
        source_id: str,
        name: Optional[str] = None,
        connection_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update a data source."""
        data = {}
        if name:
            data['name'] = name
        if connection_params:
            data['connectionParams'] = connection_params
        return self._request('PATCH', f'/workspace/{self.workspace_id}/datasources/{source_id}', data=data)

    def delete_data_source(self, source_id: str) -> None:
        """Delete a data source."""
        self._request('DELETE', f'/workspace/{self.workspace_id}/datasources/{source_id}')

    def list_secrets(self) -> Dict[str, Any]:
        """List all secrets."""
        return self._request('GET', f'/workspace/{self.workspace_id}/secrets')

    def create_secret(
        self,
        name: str,
        value: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new secret."""
        data = {'name': name, 'value': value}
        if description:
            data['description'] = description
        return self._request('POST', f'/workspace/{self.workspace_id}/secrets', data=data)

    def update_secret(
        self,
        secret_name: str,
        value: str
    ) -> Dict[str, Any]:
        """Update a secret."""
        return self._request('PATCH', f'/workspace/{self.workspace_id}/secrets/{secret_name}', data={'value': value})

    def delete_secret(self, secret_name: str) -> None:
        """Delete a secret."""
        self._request('DELETE', f'/workspace/{self.workspace_id}/secrets/{secret_name}')

    def list_schedules(self, project_id: str) -> List[Dict[str, Any]]:
        """List schedules for a project."""
        logical_id = self.get_logical_id(project_id)
        return self._request('GET', f'/workspace/{self.workspace_id}/projects/{logical_id}/schedules')

    def create_schedule(
        self,
        project_id: str,
        cron: str,
        timezone: str = "UTC"
    ) -> Dict[str, Any]:
        """Create a schedule."""
        logical_id = self.get_logical_id(project_id)
        data = {'cron': cron, 'timezone': timezone}
        return self._request('POST', f'/workspace/{self.workspace_id}/projects/{logical_id}/schedules', data=data)

    def delete_schedule(self, project_id: str, schedule_id: str) -> None:
        """Delete a schedule."""
        logical_id = self.get_logical_id(project_id)
        self._request('DELETE', f'/workspace/{self.workspace_id}/projects/{logical_id}/schedules/{schedule_id}')

    def list_app_access(self, project_id: str) -> List[Dict[str, Any]]:
        """List app access permissions."""
        logical_id = self.get_logical_id(project_id)
        return self._request('GET', f'/workspace/{self.workspace_id}/projects/{logical_id}/access')

    def grant_app_access(
        self,
        project_id: str,
        email: str,
        role: str = "viewer"
    ) -> Dict[str, Any]:
        """Grant app access to a user."""
        logical_id = self.get_logical_id(project_id)
        data = {'email': email, 'role': role}
        return self._request('POST', f'/workspace/{self.workspace_id}/projects/{logical_id}/access', data=data)

    def revoke_app_access(self, project_id: str, user_id: str) -> None:
        """Revoke app access from a user."""
        logical_id = self.get_logical_id(project_id)
        self._request('DELETE', f'/workspace/{self.workspace_id}/projects/{logical_id}/access/{user_id}')

    def get_runtime_context(self, run_id: str) -> Dict[str, Any]:
        """Get runtime context for a run."""
        return self._request('GET', f'/workspace/{self.workspace_id}/runs/{run_id}/context')

    def run_sql(
        self,
        project_id: str,
        datasource_id: str,
        sql: str
    ) -> List[Dict[str, Any]]:
        """Run SQL query via Hex."""
        data = {
            'datasourceId': datasource_id,
            'sql': sql
        }
        return self._request('POST', f'/workspace/{self.workspace_id}/executions/sql', data=data)

    def list_variables(self, project_id: str) -> List[Dict[str, Any]]:
        """List project variables."""
        logical_id = self.get_logical_id(project_id)
        return self._request('GET', f'/workspace/{self.workspace_id}/projects/{logical_id}/variables')

    def set_variable(
        self,
        project_id: str,
        variable_id: str,
        value: Any
    ) -> Dict[str, Any]:
        """Set a project variable value."""
        logical_id = self.get_logical_id(project_id)
        return self._request('POST', f'/workspace/{self.workspace_id}/projects/{logical_id}/variables/{variable_id}/set', data={'value': value})