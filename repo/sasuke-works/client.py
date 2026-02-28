"""
Sasuke Works API Client

This module provides a Python client for interacting with Sasuke Works business platform.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class SasukeWorksClient:
    """
    Client for Sasuke Works Business Platform.

    Sasuke Works provides:
    - Customer management
    - Project tracking
    - Task management
    - Time tracking
    - Invoice management
    - Reporting
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.sasukeworks.com/v1",
        timeout: int = 30
    ):
        """
        Initialize the Sasuke Works client.

        Args:
            api_key: Sasuke Works API key
            base_url: Base URL for the Sasuke Works API
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

    def get_clients(
        self,
        page: int = 1,
        per_page: int = 50
    ) -> List[Dict[str, Any]]:
        """Get all clients."""
        params = {
            'page': page,
            'per_page': per_page
        }
        return self._request('GET', '/clients', params=params)

    def get_client(self, client_id: str) -> Dict[str, Any]:
        """Get client details."""
        return self._request('GET', f'/clients/{client_id}')

    def create_client(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        company_name: Optional[str] = None,
        tax_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new client."""
        data = {'name': name}

        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if address:
            data['address'] = address
        if company_name:
            data['company_name'] = company_name
        if tax_id:
            data['tax_id'] = tax_id
        if notes:
            data['notes'] = notes

        return self._request('POST', '/clients', json_data=data)

    def update_client(
        self,
        client_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] None = None,
        company_name: Optional[str] None = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update client details."""
        data = {}
        if name:
            data['name'] = name
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if address:
            data['address'] = address
        if company_name:
            data['company_name'] = company_name
        if notes:
            data['notes'] = notes

        return self._request('PUT', f'/clients/{client_id}', json_data=data)

    def delete_client(self, client_id: str) -> Dict[str, Any]:
        """Delete a client."""
        return self._request('DELETE', f'/clients/{client_id}')

    def get_projects(
        self,
        page: int = 1,
        per_page: int = 50,
        client_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all projects."""
        params = {
            'page': page,
            'per_page': per_page
        }
        if client_id:
            params['client_id'] = client_id
        if status:
            params['status'] = status

        return self._request('GET', '/projects', params=params)

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project details."""
        return self._request('GET', f'/projects/{project_id}')

    def create_project(
        self,
        name: str,
        client_id: str,
        description: str = "",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        budget: Optional[float] = None,
        status: str = "active"
    ) -> Dict[str, Any]:
        """Create a new project."""
        data = {
            'name': name,
            'client_id': client_id,
            'status': status,
            'description': description
        }

        if start_date:
            data['start_date'] = start_date
        if end_date:
            data['end_date'] = end_date
        if budget:
            data['budget'] = budget

        return self._request('POST', '/projects', json_data=data)

    def update_project(
        self,
        project_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        budget: Optional[float] = None
    ) -> Dict[str, Any]:
        """Update project details."""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if status:
            data['status'] = status
        if start_date:
            data['start_date'] = start_date
        if end_date:
            data['end_date'] = end_date
        if budget:
            data['budget'] = budget

        return self._request('PUT', f'/projects/{project_id}', json_data=data)

    def delete_project(self, project_id: str) -> Dict[str, Any]:
        """Delete a project."""
        return self._request('DELETE', f'/projects/{project_id}')

    def get_tasks(
        self,
        page: int = 1,
        per_page: int = 50,
        project_id: Optional[str] = None,
        status: Optional[str] = None,
        assignee_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all tasks."""
        params = {
            'page': page,
            'per_page': per_page
        }
        if project_id:
            params['project_id'] = project_id
        if status:
            params['status'] = status
        if assignee_id:
            params['assignee_id'] = assignee_id

        return self._request('GET', '/tasks', params=params)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get task details."""
        return self._request('GET', f'/tasks/{task_id}')

    def create_task(
        self,
        title: str,
        project_id: str,
        description: str = "",
        status: str = "todo",
        priority: str = "medium",
        assignee_id: Optional[str] = None,
        due_date: Optional[str] = None,
        estimated_hours: Optional[float] = None
    ) -> Dict[str, Any]:
        """Create a new task."""
        data = {
            'title': title,
            'project_id': project_id,
            'status': status,
            'priority': priority,
            'description': description
        }

        if assignee_id:
            data['assignee_id'] = assignee_id
        if due_date:
            data['due_date'] = due_date
        if estimated_hours:
            data['estimated_hours'] = estimated_hours

        return self._request('POST', '/tasks', json_data=data)

    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee_id: Optional[str] = None,
        due_date: Optional[str] = None,
        estimated_hours: Optional[float] = None
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
            data['assignee_id'] = assignee_id
        if due_date:
            data['due_date'] = due_date
        if estimated_hours:
            data['estimated_hours'] = estimated_hours

        return self._request('PUT', f'/tasks/{task_id}', json_data=data)

    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete a task."""
        return self._request('DELETE', f'/tasks/{task_id}')

    def get_time_entries(
        self,
        page: int = 1,
        per_page: int = 50,
        project_id: Optional[str] = None,
        task_id: Optional[str] = None,
        user_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all time entries."""
        params = {
            'page': page,
            'per_page': per_page
        }
        if project_id:
            params['project_id'] = project_id
        if task_id:
            params['task_id'] = task_id
        if user_id:
            params['user_id'] = user_id
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date

        return self._request('GET', '/time-entries', params=params)

    def create_time_entry(
        self,
        project_id: str,
        description: str,
        duration: float,
        date: str,
        task_id: Optional[str] = None,
        billable: bool = True
    ) -> Dict[str, Any]:
        """Create a new time entry."""
        data = {
            'project_id': project_id,
            'description': description,
            'duration': duration,
            'date': date,
            'billable': billable
        }

        if task_id:
            data['task_id'] = task_id

        return self._request('POST', '/time-entries', json_data=data)

    def update_time_entry(
        self,
        entry_id: str,
        description: Optional[str] = None,
        duration: Optional[float] = None,
        date: Optional[str] = None,
        task_id: Optional[str] = None,
        billable: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update time entry details."""
        data = {}
        if description:
            data['description'] = description
        if duration:
            data['duration'] = duration
        if date:
            data['date'] = date
        if task_id:
            data['task_id'] = task_id
        if billable is not None:
            data['billable'] = billable

        return self._request('PUT', f'/time-entries/{entry_id}', json_data=data)

    def delete_time_entry(self, entry_id: str) -> Dict[str, Any]:
        """Delete a time entry."""
        return self._request('DELETE', f'/time-entries/{entry_id}')

    def get_invoices(
        self,
        page: int = 1,
        per_page: int = 50,
        client_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all invoices."""
        params = {
            'page': page,
            'per_page': per_page
        }
        if client_id:
            params['client_id'] = client_id
        if status:
            params['status'] = status

        return self._request('GET', '/invoices', params=params)

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Get invoice details."""
        return self._request('GET', f'/invoices/{invoice_id}')

    def create_invoice(
        self,
        client_id: str,
        project_id: str,
        invoice_number: str,
        issue_date: str,
        due_date: str,
        items: List[Dict[str, Any]],
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new invoice."""
        data = {
            'client_id': client_id,
            'project_id': project_id,
            'invoice_number': invoice_number,
            'issue_date': issue_date,
            'due_date': due_date,
            'items': items
        }

        if notes:
            data['notes'] = notes

        return self._request('POST', '/invoices', json_data=data)

    def update_invoice(
        self,
        invoice_id: str,
        status: Optional[str] = None,
        paid_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update invoice status."""
        data = {}
        if status:
            data['status'] = status
        if paid_date:
            data['paid_date'] = paid_date

        return self._request('PUT', f'/invoices/{invoice_id}', json_data=data)

    def delete_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Delete an invoice."""
        return self._request('DELETE', f'/invoices/{invoice_id}')

    def get_team_members(
        self,
        page: int = 1,
        per_page: int = 50
    ) -> List[Dict[str, Any]]:
        """Get all team members."""
        params = {
            'page': page,
            'per_page': per_page
        }
        return self._request('GET', '/team', params=params)

    def add_team_member(
        self,
        email: str,
        name: str,
        role: str = "member"
    ) -> Dict[str, Any]:
        """Add a team member."""
        data = {
            'email': email,
            'name': name,
            'role': role
        }
        return self._request('POST', '/team', json_data=data)

    def update_team_member(
        self,
        member_id: str,
        role: Optional[str] = None,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update team member details."""
        data = {}
        if role:
            data['role'] = role
        if name:
            data['name'] = name

        return self._request('PUT', f'/team/{member_id}', json_data=data)

    def remove_team_member(self, member_id: str) -> Dict[str, Any]:
        """Remove a team member."""
        return self._request('DELETE', f'/team/{member_id}')

    def get_reports(
        self,
        report_type: str,
        start_date: str,
        end_date: str,
        project_id: Optional[str] = None,
        client_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get reports."""
        params = {
            'type': report_type,
            'start_date': start_date,
            'end_date': end_date
        }
        if project_id:
            params['project_id'] = project_id
        if client_id:
            params['client_id'] = client_id

        return self._request('GET', '/reports', params=params)

    def get_user_info(self) -> Dict[str, Any]:
        """Get current user information."""
        return self._request('GET', '/user/me')