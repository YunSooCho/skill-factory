"""
YukyuNote Vacation Management API Client

This module provides a Python client for interacting with the YukyuNote
vacation management system API.
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, date


class YukyuNoteClient:
    """
    Client for YukyuNote Vacation Management System API.

    YukyuNote provides:
    - Paid leave tracking
    - Vacation request management
    - Leave balance calculation
    - Approval workflows
    - Time-off calendar
    """

    def __init__(
        self,
        api_key: str,
        company_id: str,
        base_url: str = "https://api.yukyu-note.jp/v1",
        timeout: int = 30
    ):
        """
        Initialize the YukyuNote client.

        Args:
            api_key: Your YukyuNote API key
            company_id: Your company ID
            base_url: API base URL (default: https://api.yukyu-note.jp/v1)
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
        Make an authenticated request to the API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            Response JSON
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

    def get_leave_balance(self, employee_id: str) -> Dict[str, Any]:
        """
        Get leave balance for an employee.

        Args:
            employee_id: Employee ID

        Returns:
            Leave balance including paid leave, sick leave, etc.
        """
        return self._request('GET', f'/employees/{employee_id}/leave-balance')

    def get_leave_history(
        self,
        employee_id: str,
        year: Optional[int] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get leave history for an employee.

        Args:
            employee_id: Employee ID
            year: Filter by year (default: current year)
            limit: Maximum number of results

        Returns:
            List of leave records
        """
        params = {'limit': limit}
        if year:
            params['year'] = year

        result = self._request('GET', f'/employees/{employee_id}/leave-history', params=params)
        return result.get('records', [])

    def request_leave(
        self,
        employee_id: str,
        leave_type: str,
        start_date: str,
        end_date: str,
        reason: Optional[str] = None,
        hours: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Submit a leave request.

        Args:
            employee_id: Employee ID
            leave_type: Type of leave (paid, sick, personal, etc.)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            reason: Reason for leave (optional)
            hours: Specific hours if taking half-day (optional)

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
        if hours:
            data['hours'] = hours

        return self._request('POST', f'/employees/{employee_id}/leave-requests', data=data)

    def get_leave_request(self, request_id: str) -> Dict[str, Any]:
        """
        Get leave request details.

        Args:
            request_id: Leave request ID

        Returns:
            Leave request details
        """
        return self._request('GET', f'/leave-requests/{request_id}')

    def list_leave_requests(
        self,
        employee_id: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List leave requests.

        Args:
            employee_id: Filter by employee (optional)
            status: Filter by status (pending, approved, rejected)
            start_date: Filter from date (YYYY-MM-DD)
            end_date: Filter to date (YYYY-MM-DD)
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
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date

        result = self._request('GET', '/leave-requests', params=params)
        return result.get('requests', [])

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

    def cancel_leave_request(
        self,
        request_id: str,
        employee_id: str,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cancel a leave request.

        Args:
            request_id: Leave request ID
            employee_id: Requester's employee ID
            reason: Reason for cancellation (optional)

        Returns:
            Updated leave request
        """
        data = {'employee_id': employee_id}
        if reason:
            data['reason'] = reason

        return self._request('POST', f'/leave-requests/{request_id}/cancel', data=data)

    def get_leave_types(self) -> List[Dict[str, Any]]:
        """
        Get available leave types.

        Returns:
            List of leave types
        """
        result = self._request('GET', '/leave-types')
        return result.get('types', [])

    def get_calendar(
        self,
        start_date: str,
        end_date: str,
        department: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get leave calendar.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            department: Filter by department (optional)

        Returns:
            List of leave entries for the period
        """
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        if department:
            params['department'] = department

        result = self._request('GET', '/calendar', params=params)
        return result.get('entries', [])

    def get_employee_summary(self, employee_id: str, year: int) -> Dict[str, Any]:
        """
        Get employee leave summary for a year.

        Args:
            employee_id: Employee ID
            year: Year to summarize

        Returns:
            Leave summary with total days taken, remaining, etc.
        """
        return self._request('GET', f'/employees/{employee_id}/summary', params={'year': year})

    def get_department_summary(
        self,
        department_id: str,
        year: int
    ) -> Dict[str, Any]:
        """
        Get department leave summary.

        Args:
            department_id: Department ID
            year: Year to summarize

        Returns:
            Department leave statistics
        """
        return self._request(
            'GET',
            f'/departments/{department_id}/summary',
            params={'year': year}
        )

    def get_public_holidays(self, year: int) -> List[Dict[str, Any]]:
        """
        Get public holidays for a year.

        Args:
            year: Year to get holidays for

        Returns:
            List of public holidays
        """
        result = self._request('GET', '/public-holidays', params={'year': year})
        return result.get('holidays', [])

    def update_leave_balance(
        self,
        employee_id: str,
        adjustment: float,
        reason: str
    ) -> Dict[str, Any]:
        """
        Manually adjust leave balance (admin only).

        Args:
            employee_id: Employee ID
            adjustment: Amount to adjust (positive or negative)
            reason: Reason for adjustment

        Returns:
            Updated leave balance
        """
        data = {
            'adjustment': adjustment,
            'reason': reason
        }

        return self._request(
            'POST',
            f'/employees/{employee_id}/adjust-balance',
            data=data
        )

    def get_employees(self) -> List[Dict[str, Any]]:
        """
        List all employees.

        Returns:
            List of employees
        """
        result = self._request('GET', '/employees')
        return result.get('employees', [])

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """
        Get employee details.

        Args:
            employee_id: Employee ID

        Returns:
            Employee details
        """
        return self._request('GET', f'/employees/{employee_id}')