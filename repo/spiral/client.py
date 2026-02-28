"""
Spiral API Client

This module provides a Python client for interacting with Spiral business platform.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class SpiralClient:
    """
    Client for Spiral Business Platform.

    Spiral provides:
    - Customer management
    - Sales tracking
    - Project management
    - Task management
    - Reporting
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.spiralplatform.com/v1",
        timeout: int = 30
    ):
        """Initialize the Spiral client."""
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, params=None, data=None, json_data=None) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, data=data, json=json_data, timeout=self.timeout)
        if response.status_code >= 400:
            error_data = response.json() if response.content else {}
            raise Exception(f"API Error {response.status_code}: {error_data}")
        try:
            return response.json()
        except:
            return response.text if response.text else {}

    def get_customers(self, page: int = 1, per_page: int = 50) -> List[Dict[str, Any]]:
        """Get all customers."""
        params = {'page': page, 'per_page': per_page}
        return self._request('GET', '/customers', params=params)

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details."""
        return self._request('GET', f'/customers/{customer_id}')

    def create_customer(self, name: str, email: Optional[str] = None, phone: Optional[str] = None, company: Optional[str] = None) -> Dict[str, Any]:
        """Create a new customer."""
        data = {'name': name}
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if company:
            data['company'] = company
        return self._request('POST', '/customers', json_data=data)

    def update_customer(self, customer_id: str, name: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]:
        """Update customer details."""
        data = {}
        if name:
            data['name'] = name
        if email:
            data['email'] = email
        return self._request('PUT', f'/customers/{customer_id}', json_data=data)

    def delete_customer(self, customer_id: str) -> Dict[str, Any]:
        """Delete a customer."""
        return self._request('DELETE', f'/customers/{customer_id}')

    def get_projects(self, page: int = 1, per_page: int = 50, customer_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all projects."""
        params = {'page': page, 'per_page': per_page}
        if customer_id:
            params['customer_id'] = customer_id
        return self._request('GET', '/projects', params=params)

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project details."""
        return self._request('GET', f'/projects/{project_id}')

    def create_project(self, name: str, customer_id: str, description: str = "", status: str = "active") -> Dict[str, Any]:
        """Create a new project."""
        data = {'name': name, 'customer_id': customer_id, 'description': description, 'status': status}
        return self._request('POST', '/projects', json_data=data)

    def update_project(self, project_id: str, name: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """Update project details."""
        data = {}
        if name:
            data['name'] = name
        if status:
            data['status'] = status
        return self._request('PUT', f'/projects/{project_id}', json_data=data)

    def delete_project(self, project_id: str) -> Dict[str, Any]:
        """Delete a project."""
        return self._request('DELETE', f'/projects/{project_id}')

    def get_tasks(self, page: int = 1, per_page: int = 50, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all tasks."""
        params = {'page': page, 'per_page': per_page}
        if project_id:
            params['project_id'] = project_id
        return self._request('GET', '/tasks', params=params)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get task details."""
        return self._request('GET', f'/tasks/{task_id}')

    def create_task(self, title: str, project_id: str, description: str = "", status: str = "todo", priority: str = "medium") -> Dict[str, Any]:
        """Create a new task."""
        data = {'title': title, 'project_id': project_id, 'description': description, 'status': status, 'priority': priority}
        return self._request('POST', '/tasks', json_data=data)

    def update_task(self, task_id: str, title: Optional[str] = None, status: Optional[str] = None, priority: Optional[str] = None) -> Dict[str, Any]:
        """Update task details."""
        data = {}
        if title:
            data['title'] = title
        if status:
            data['status'] = status
        if priority:
            data['priority'] = priority
        return self._request('PUT', f'/tasks/{task_id}', json_data=data)

    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete a task."""
        return self._request('DELETE', f'/tasks/{task_id}')

    def get_deals(self, page: int = 1, per_page: int = 50, customer_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all sales deals."""
        params = {'page': page, 'per_page': per_page}
        if customer_id:
            params['customer_id'] = customer_id
        return self._request('GET', '/deals', params=params)

    def get_deal(self, deal_id: str) -> Dict[str, Any]:
        """Get deal details."""
        return self._request('GET', f'/deals/{deal_id}')

    def create_deal(self, title: str, customer_id: str, amount: float, stage: str = "prospect") -> Dict[str, Any]:
        """Create a new deal."""
        data = {'title': title, 'customer_id': customer_id, 'amount': amount, 'stage': stage}
        return self._request('POST', '/deals', json_data=data)

    def update_deal(self, deal_id: str, stage: Optional[str] = None, amount: Optional[float] = None) -> Dict[str, Any]:
        """Update deal details."""
        data = {}
        if stage:
            data['stage'] = stage
        if amount:
            data['amount'] = amount
        return self._request('PUT', f'/deals/{deal_id}', json_data=data)

    def delete_deal(self, deal_id: str) -> Dict[str, Any]:
        """Delete a deal."""
        return self._request('DELETE', f'/deals/{deal_id}')

    def get_reports(self, report_type: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get reports."""
        params = {'type': report_type, 'start_date': start_date, 'end_date': end_date}
        return self._request('GET', '/reports', params=params)

    def get_user_info(self) -> Dict[str, Any]:
        """Get current user information."""
        return self._request('GET', '/user/me')