"""
TeamSpirit HR API Client

This module provides a Python client for interacting with the TeamSpirit HR system API.
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, date


class TeamSpiritClient:
    """
    Client for TeamSpirit HR System API.

    TeamSpirit is a Japanese HR management system featuring:
    - Attendance tracking
    - Leave management
    - Employee information management
    - Work schedule management
    """

    def __init__(
        self,
        api_key: str,
        company_id: str,
        base_url: str = "https://api.teamspirit.com/v1",
        timeout: int = 30
    ):
        """
        Initialize the TeamSpirit client.

        Args:
            api_key: Your TeamSpirit API key
            company_id: Your company ID in TeamSpirit
            base_url: API base URL (default: https://api.teamspirit.com/v1)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.company_id = company_id
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Company-ID': company_id
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the TeamSpirit API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            Response JSON

        Raises:
            requests.RequestException: If request fails
        """
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

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """
        Get employee information.

        Args:
            employee_id: Employee ID

        Returns:
            Employee information including name, department, position, etc.
        """
        return self._request('GET', f'/employees/{employee_id}')

    def list_employees(
        self,
        department: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List employees.

        Args:
            department: Filter by department
            status: Filter by employment status (active, resigned, etc.)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of employees
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        if department:
            params['department'] = department
        if status:
            params['status'] = status

        result = self._request('GET', '/employees', params=params)
        return result.get('employees', [])

    def get_attendance(
        self,
        employee_id: str,
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """
        Get attendance records for an employee.

        Args:
            employee_id: Employee ID
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            Attendance records with clock-in/out times, work hours, etc.
        """
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        return self._request('GET', f'/employees/{employee_id}/attendance', params=params)

    def clock_in(
        self,
        employee_id: str,
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Record clock-in for an employee.

        Args:
            employee_id: Employee ID
            timestamp: Clock-in time in ISO format (default: current time)

        Returns:
            Clock-in record
        """
        data = {}
        if timestamp:
            data['timestamp'] = timestamp

        return self._request('POST', f'/employees/{employee_id}/clock-in', data=data)

    def clock_out(
        self,
        employee_id: str,
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Record clock-out for an employee.

        Args:
            employee_id: Employee ID
            timestamp: Clock-out time in ISO format (default: current time)

        Returns:
            Clock-out record
        """
        data = {}
        if timestamp:
            data['timestamp'] = timestamp

        return self._request('POST', f'/employees/{employee_id}/clock-out', data=data)

    def request_leave(
        self,
        employee_id: str,
        leave_type: str,
        start_date: str,
        end_date: str,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit a leave request.

        Args:
            employee_id: Employee ID
            leave_type: Type of leave (annual, sick, personal, etc.)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            reason: Reason for leave (optional)

        Returns:
            Leave request details
        """
        data = {
            'leave_type': leave_type,
            'start_date': start_date,
            'end_date': end_date
        }
        if reason:
            data['reason'] = reason

        return self._request('POST', f'/employees/{employee_id}/leave-requests', data=data)

    def get_leave_balance(self, employee_id: str) -> Dict[str, Any]:
        """
        Get leave balance for an employee.

        Args:
            employee_id: Employee ID

        Returns:
            Leave balance details including remaining days for each leave type
        """
        return self._request('GET', f'/employees/{employee_id}/leave-balance')

    def list_leave_requests(
        self,
        employee_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List leave requests.

        Args:
            employee_id: Filter by employee (optional)
            status: Filter by status (pending, approved, rejected)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of leave requests
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        if employee_id:
            params['employee_id'] = employee_id
        if status:
            params['status'] = status

        result = self._request('GET', '/leave-requests', params=params)
        return result.get('leave_requests', [])

    def approve_leave_request(
        self,
        request_id: str,
        approver_id: str,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Approve a leave request.

        Args:
            request_id: Leave request ID
            approver_id: Approver's employee ID
            comment: Approval comment (optional)

        Returns:
            Updated leave request
        """
        data = {
            'action': 'approve',
            'approver_id': approver_id
        }
        if comment:
            data['comment'] = comment

        return self._request('POST', f'/leave-requests/{request_id}/action', data=data)

    def reject_leave_request(
        self,
        request_id: str,
        approver_id: str,
        reason: str
    ) -> Dict[str, Any]:
        """
        Reject a leave request.

        Args:
            request_id: Leave request ID
            approver_id: Approver's employee ID
            reason: Reason for rejection

        Returns:
            Updated leave request
        """
        data = {
            'action': 'reject',
            'approver_id': approver_id,
            'reason': reason
        }

        return self._request('POST', f'/leave-requests/{request_id}/action', data=data)

    def get_departments(self) -> List[Dict[str, Any]]:
        """
        Get list of departments.

        Returns:
            List of departments with IDs and names
        """
        result = self._request('GET', '/departments')
        return result.get('departments', [])

    def get_department_employees(self, department_id: str) -> List[Dict[str, Any]]:
        """
        Get employees in a department.

        Args:
            department_id: Department ID

        Returns:
            List of employees in the department
        """
        result = self._request('GET', f'/departments/{department_id}/employees')
        return result.get('employees', [])

    def get_work_schedule(
        self,
        employee_id: str,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Get work schedule for an employee.

        Args:
            employee_id: Employee ID
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            List of scheduled work days with shifts
        """
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        result = self._request('GET', f'/employees/{employee_id}/schedule', params=params)
        return result.get('schedule', [])

    def update_employee(
        self,
        employee_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update employee information.

        Args:
            employee_id: Employee ID
            data: Fields to update (e.g., name, department, position)

        Returns:
            Updated employee information
        """
        return self._request('PUT', f'/employees/{employee_id}', data=data)