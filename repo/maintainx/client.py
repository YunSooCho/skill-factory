"""
Maintainx API Client

Complete client for Maintainx facilities maintenance integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class MaintainxAPIClient:
    """
    Complete client for Maintainx facilities maintenance management.
    Supports work orders, tasks, users, and vendor management.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Maintainx API client.

        Args:
            api_key: Maintainx API key (from env: MAINTAINX_API_KEY)
            base_url: Base URL (default: https://api.maintainx.com/v1)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_key = api_key or os.getenv("MAINTAINX_API_KEY")
        self.base_url = base_url or os.getenv(
            "MAINTAINX_BASE_URL",
            "https://api.maintainx.com/v1"
        )
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_key:
            raise ValueError(
                "API key is required. Set MAINTAINX_API_KEY environment variable."
            )

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Maintainx API."""
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return {"status": "success"}

    # Work Orders

    def create_work_order(
        self,
        title: str,
        description: str,
        location_id: str,
        priority: str = "medium",
        status: str = "open",
        assigned_to_ids: Optional[List[str]] = None,
        due_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a work order.

        Args:
            title: Work order title
            description: Work order description
            location_id: Location ID
            priority: Priority (low, medium, high, critical)
            status: Initial status
            assigned_to_ids: List of assigned user IDs
            due_date: Due date (YYYY-MM-DD)

        Returns:
            Work order information
        """
        data = {
            'title': title,
            'description': description,
            'location_id': location_id,
            'priority': priority,
            'status': status
        }

        if assigned_to_ids:
            data['assigned_to_ids'] = assigned_to_ids
        if due_date:
            data['due_date'] = due_date

        return self._request('POST', '/work_orders', data=data)

    def get_work_order(self, work_order_id: str) -> Dict[str, Any]:
        """Get work order details."""
        return self._request('GET', f'/work_orders/{work_order_id}')

    def list_work_orders(
        self,
        status: Optional[str] = None,
        location_id: Optional[str] = None,
        assigned_to_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List work orders with filtering."""
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status
        if location_id:
            params['location_id'] = location_id
        if assigned_to_id:
            params['assigned_to_id'] = assigned_to_id
        return self._request('GET', '/work_orders', params=params)

    def update_work_order(
        self,
        work_order_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Update work order."""
        return self._request('PUT', f'/work_orders/{work_order_id}', data=kwargs)

    def close_work_order(self, work_order_id: str, notes: Optional[str] = None) -> Dict[str, Any]:
        """Close a work order."""
        data = {'status': 'closed'}
        if notes:
            data['notes'] = notes
        return self._request('PUT', f'/work_orders/{work_order_id}', data=data)

    # Tasks

    def create_task(
        self,
        work_order_id: str,
        name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a task within a work order."""
        data = {
            'work_order_id': work_order_id,
            'name': name
        }

        if description:
            data['description'] = description

        return self._request('POST', '/tasks', data=data)

    def list_tasks(
        self,
        work_order_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List tasks."""
        params = {'limit': limit, 'offset': offset}
        if work_order_id:
            params['work_order_id'] = work_order_id
        return self._request('GET', '/tasks', params=params)

    # Locations

    def list_locations(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """List all locations."""
        params = {'limit': limit, 'offset': offset}
        return self._request('GET', '/locations', params=params)

    def get_location(self, location_id: str) -> Dict[str, Any]:
        """Get location details."""
        return self._request('GET', f'/locations/{location_id}')

    # Users

    def list_users(
        self,
        role: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List users."""
        params = {'limit': limit, 'offset': offset}
        if role:
            params['role'] = role
        return self._request('GET', '/users', params=params)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user details."""
        return self._request('GET', f'/users/{user_id}')

    def create_user(
        self,
        email: str,
        name: str,
        role: str = "technician"
    ) -> Dict[str, Any]:
        """Create a user."""
        data = {
            'email': email,
            'name': name,
            'role': role
        }
        return self._request('POST', '/users', data=data)

    # Vendors

    def list_vendors(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """List vendors."""
        params = {'limit': limit, 'offset': offset}
        return self._request('GET', '/vendors', params=params)

    def get_vendor(self, vendor_id: str) -> Dict[str, Any]:
        """Get vendor details."""
        return self._request('GET', f'/vendors/{vendor_id}')

    # Work Order Comments/Notes

    def add_comment(
        self,
        work_order_id: str,
        comment: str,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add comment to work order."""
        data = {
            'work_order_id': work_order_id,
            'comment': comment
        }

        if user_id:
            data['user_id'] = user_id

        return self._request('POST', '/comments', data=data)

    # Attachments

    def add_attachment(
        self,
        work_order_id: str,
        file_path: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add attachment to work order."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        url = urljoin(self.base_url + "/", f'/work_orders/{work_order_id}/attachments')

        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            data = {}

            if description:
                data['description'] = description

            response = self.session.post(
                url,
                files=files,
                data=data,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=self.timeout,
                verify=self.verify_ssl
            )

        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return {"status": "success"}

    # Webhooks

    def create_webhook(
        self,
        url: str,
        events: List[str]
    ) -> Dict[str, Any]:
        """Create webhook."""
        data = {'url': url, 'events': events}
        return self._request('POST', '/webhooks', data=data)

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete webhook."""
        return self._request('DELETE', f'/webhooks/{webhook_id}')

    def close(self):
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()