"""
ClickUp API Client - Project Management
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime


class ClickUpError(Exception):
    """Base exception for ClickUp errors"""
    pass


class ClickUpClient:
    """Client for ClickUp API"""

    BASE_URL = "https://api.clickup.com/api/v2"

    def __init__(self, api_key: str):
        """
        Initialize ClickUp client

        Args:
            api_key: ClickUp API key
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request(self, method: str, endpoint: str, json_data: Optional[Dict] = None,
                      params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to ClickUp API"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ClickUpError(f"API request failed: {str(e)}") from e

    # Task Operations

    def create_task(self, list_id: str, name: str, **kwargs) -> Dict[str, Any]:
        """
        Create a task

        Args:
            list_id: List ID
            name: Task name
            **kwargs: Additional task fields

        Returns:
            Created task data
        """
        task_data = {"name": name}
        task_data.update(kwargs)
        return self._make_request("POST", f"/list/{list_id}/task", json_data=task_data)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get a task by ID"""
        return self._make_request("GET", f"/task/{task_id}")

    def get_tasks(self, list_id: str, **kwargs) -> Dict[str, Any]:
        """Get all tasks in a list"""
        return self._make_request("GET", f"/list/{list_id}/task", params=kwargs)

    def search_tasks(self, workspace_id: str, **kwargs) -> Dict[str, Any]:
        """Search tasks in workspace"""
        params = {"team_id": workspace_id}
        params.update(kwargs)
        return self._make_request("GET", "/team/task/search", params=params)

    def search_tasks_by_status(self, workspace_id: str, status: str, **kwargs) -> Dict[str, Any]:
        """Search tasks by status"""
        return self.search_tasks(workspace_id, statuses=[status], **kwargs)

    def search_tasks_by_custom_field(self, workspace_id: str, field_name: str, 
                                      field_value: Any, **kwargs) -> Dict[str, Any]:
        """Search tasks by custom field"""
        custom_tasks = [{"field": field_name, "operator": "=", "value": field_value}]
        return self.search_tasks(workspace_id, custom_tasks=custom_tasks, **kwargs)

    def update_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """Update a task"""
        return self._make_request("PUT", f"/task/{task_id}", json_data=kwargs)

    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete a task"""
        return self._make_request("DELETE", f"/task/{task_id}")

    # Comment Operations

    def add_comment(self, task_id: str, comment_text: str, comment_id: Optional[str] = None) -> Dict[str, Any]:
        """Add comment to task"""
        comment_data = {"comment_text": comment_text}
        if comment_id:
            comment_data["comment_id"] = comment_id
        return self._make_request("POST", f"/task/{task_id}/comment", json_data=comment_data)

    # File Operations

    def upload_attachment(self, task_id: str, file_path: str) -> Dict[str, Any]:
        """Upload file attachment to task"""
        with open(file_path, 'rb') as f:
            files = {"file": f}
            return self._make_request("POST", f"/task/{task_id}/attachment", json_data=None)

    # Custom Field Operations

    def get_custom_fields(self, list_id: str) -> Dict[str, Any]:
        """Get custom fields for a list"""
        return self._make_request("GET", f"/list/{list_id}/field")

    def add_label_custom_field(self, task_id: str, field_name: str, field_value: str) -> Dict[str, Any]:
        """Add label type custom field value to task"""
        return self.update_task(
            task_id,
            custom_fields=[{
                "id": field_name,
                "type": "label",
                "value": field_value
            }]
        )

    # Webhook/Trigger Setup

    def create_webhook(self, list_id: str, webhook_url: str, events: List[str]) -> Dict[str, Any]:
        """Create webhook for list"""
        webhook_data = {
            "endpoint": webhook_url,
            "events": events
        }
        return self._make_request("POST", f"/list/{list_id}/webhook", json_data=webhook_data)

    def close(self):
        """Close session"""
        self.session.close()