"""
Canbus API Client

This module provides a Python client for interacting with Canbus business management platform.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class CanbusClient:
    """
    Client for Canbus Business Management Platform.

    Canbus provides:
    - Project management
    - Task tracking and assignment
    - Team collaboration
    - Resource management
    - Reporting and analytics
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.canbus.io/v1",
        timeout: int = 30
    ):
        """
        Initialize the Canbus client.

        Args:
            api_key: Canbus API key
            base_url: Base URL for the Canbus API
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
            return response.text if response.text else {}

    def get_workspaces(self) -> List[Dict[str, Any]]:
        """List all workspaces."""
        return self._request('GET', '/workspaces')

    def get_workspace(self, workspace_id: str) -> Dict[str, Any]:
        """Get workspace details."""
        return self._request('GET', f'/workspaces/{workspace_id}')

    def create_workspace(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new workspace."""
        data = {'name': name}
        if description:
            data['description'] = description

        return self._request('POST', '/workspaces', json_data=data)

    def update_workspace(
        self,
        workspace_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update workspace details."""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description

        return self._request('PATCH', f'/workspaces/{workspace_id}', json_data=data)

    def delete_workspace(self, workspace_id: str) -> Dict[str, Any]:
        """Delete a workspace."""
        return self._request('DELETE', f'/workspaces/{workspace_id}')

    def get_projects(self, workspace_id: str) -> List[Dict[str, Any]]:
        """List all projects in a workspace."""
        return self._request('GET', f'/workspaces/{workspace_id}/projects')

    def get_project(self, workspace_id: str, project_id: str) -> Dict[str, Any]:
        """Get project details."""
        return self._request('GET', f'/workspaces/{workspace_id}/projects/{project_id}')

    def create_project(
        self,
        workspace_id: str,
        name: str,
        description: Optional[str] = None,
        status: str = "active",
        priority: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new project."""
        data = {
            'name': name,
            'status': status
        }

        if description:
            data['description'] = description
        if priority:
            data['priority'] = priority
        if start_date:
            data['startDate'] = start_date
        if end_date:
            data['endDate'] = end_date

        return self._request('POST', f'/workspaces/{workspace_id}/projects', json_data=data)

    def update_project(
        self,
        workspace_id: str,
        project_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update project details."""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if status:
            data['status'] = status
        if priority:
            data['priority'] = priority

        return self._request('PATCH', f'/workspaces/{workspace_id}/projects/{project_id}', json_data=data)

    def delete_project(self, workspace_id: str, project_id: str) -> Dict[str, Any]:
        """Delete a project."""
        return self._request('DELETE', f'/workspaces/{workspace_id}/projects/{project_id}')

    def get_tasks(
        self,
        workspace_id: str,
        project_id: str,
        status: Optional[str] = None,
        assignee: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """List tasks in a project."""
        params = {}
        if status:
            params['status'] = status
        if assignee:
            params['assignee'] = assignee
        if limit:
            params['limit'] = limit

        return self._request('GET', f'/workspaces/{workspace_id}/projects/{project_id}/tasks', params=params)

    def get_task(self, workspace_id: str, project_id: str, task_id: str) -> Dict[str, Any]:
        """Get task details."""
        return self._request('GET', f'/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}')

    def create_task(
        self,
        workspace_id: str,
        project_id: str,
        title: str,
        description: Optional[str] = None,
        status: str = "todo",
        priority: Optional[str] = None,
        assignee_id: Optional[str] = None,
        due_date: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a new task."""
        data = {
            'title': title,
            'status': status
        }

        if description:
            data['description'] = description
        if priority:
            data['priority'] = priority
        if assignee_id:
            data['assigneeId'] = assignee_id
        if due_date:
            data['dueDate'] = due_date
        if tags:
            data['tags'] = tags

        return self._request('POST', f'/workspaces/{workspace_id}/projects/{project_id}/tasks', json_data=data)

    def update_task(
        self,
        workspace_id: str,
        project_id: str,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee_id: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update task details."""
        data = {}
        if title:
            data['title'] = title
        if description:
            data['description'] = description
        if status:
            data['status'] = status
        if priority:
            data['priority'] = priority
        if assignee_id:
            data['assigneeId'] = assignee_id
        if due_date:
            data['dueDate'] = due_date

        return self._request('PATCH', f'/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}', json_data=data)

    def delete_task(self, workspace_id: str, project_id: str, task_id: str) -> Dict[str, Any]:
        """Delete a task."""
        return self._request('DELETE', f'/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}')

    def create_task_comment(
        self,
        workspace_id: str,
        project_id: str,
        task_id: str,
        comment: str,
        author: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a comment to a task."""
        data = {
            'content': comment
        }
        if author:
            data['author'] = author

        return self._request('POST', f'/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}/comments', json_data=data)

    def get_task_comments(self, workspace_id: str, project_id: str, task_id: str) -> List[Dict[str, Any]]:
        """Get comments for a task."""
        return self._request('GET', f'/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}/comments')

    def get_team_members(self, workspace_id: str) -> List[Dict[str, Any]]:
        """List team members in a workspace."""
        return self._request('GET', f'/workspaces/{workspace_id}/members')

    def add_team_member(
        self,
        workspace_id: str,
        email: str,
        role: str = "member"
    ) -> Dict[str, Any]:
        """Add a team member to the workspace."""
        data = {
            'email': email,
            'role': role
        }
        return self._request('POST', f'/workspaces/{workspace_id}/members', json_data=data)

    def remove_team_member(self, workspace_id: str, member_id: str) -> Dict[str, Any]:
        """Remove a team member from the workspace."""
        return self._request('DELETE', f'/workspaces/{workspace_id}/members/{member_id}')

    def get_reports(
        self,
        workspace_id: str,
        project_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get project reports."""
        params = {}
        if project_id:
            params['projectId'] = project_id
        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date

        return self._request('GET', f'/workspaces/{workspace_id}/reports', params=params)

    def get_project_statistics(self, workspace_id: str, project_id: str) -> Dict[str, Any]:
        """Get project statistics."""
        return self._request('GET', f'/workspaces/{workspace_id}/projects/{project_id}/statistics')

    def search_tasks(
        self,
        workspace_id: str,
        query: str,
        project_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for tasks."""
        params = {'query': query}
        if project_id:
            params['projectId'] = project_id

        return self._request('GET', f'/workspaces/{workspace_id}/search/tasks', params=params)

    def get_activity_log(
        self,
        workspace_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get workspace activity log."""
        params = {}
        if limit:
            params['limit'] = limit

        return self._request('GET', f'/workspaces/{workspace_id}/activity', params=params)

    def get_labels(self, workspace_id: str) -> List[Dict[str, Any]]:
        """List labels in workspace."""
        return self._request('GET', f'/workspaces/{workspace_id}/labels')

    def create_label(
        self,
        workspace_id: str,
        name: str,
        color: str
    ) -> Dict[str, Any]:
        """Create a new label."""
        data = {
            'name': name,
            'color': color
        }
        return self._request('POST', f'/workspaces/{workspace_id}/labels', json_data=data)