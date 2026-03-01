"""
Zoho People HR Management API Client

This module provides a Python client for interacting with the Zoho People
HR management system API.
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, date


class ZohoPeopleClient:
    """
    Client for Zoho People HR Management System API.

    Zoho People provides:
    - Employee records management
    - Leave management
    - Attendance tracking
    - Time tracking
    - Performance reviews
    - Payroll integration
    """

    def __init__(
        self,
        auth_token: str,
        organization_id: str,
        base_url: str = "https://people.zoho.com/people/api",
        timeout: int = 30
    ):
        """
        Initialize the Zoho People client.

        Args:
            auth_token: Zoho authentication token
            organization_id: Your organization ID
            base_url: API base URL (default: https://people.zoho.com/people/api)
            timeout: Request timeout in seconds
        """
        self.auth_token = auth_token
        self.organization_id = organization_id
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.params = {
            'authtoken': auth_token,
            'scope': 'peopleapi'
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the Zoho People API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            Response JSON
        """
        url = f"{self.base_url}{endpoint}"
        if data:
            data['organizationId'] = self.organization_id

        response = self.session.request(
            method,
            url,
            params=params,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def get_employees(
        self,
        department: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get list of employees.

        Args:
            department: Filter by department (optional)
            status: Filter by employment status (optional)
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

        return self._request(
            'GET',
            '/forms/P_Employee/getRecords',
            params=params
        )

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """
        Get employee details.

        Args:
            employee_id: Employee ID

        Returns:
            Employee details
        """
        return self._request(
            'GET',
            f'/forms/P_Employee/getRecordById',
            params={'recordId': employee_id}
        )

    def create_employee(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new employee.

        Args:
            data: Employee data including name, email, department, etc.

        Returns:
            Created employee details
        """
        return self._request(
            'POST',
            '/forms/P_Employee/addRecord',
            data=data
        )

    def update_employee(self, employee_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update employee information.

        Args:
            employee_id: Employee ID
            data: Fields to update

        Returns:
            Updated employee details
        """
        data['recordId'] = employee_id
        return self._request(
            'POST',
            '/forms/P_Employee/updateRecord',
            data=data
        )

    def get_attendance(
        self,
        employee_id: str,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Get attendance records.

        Args:
            employee_id: Employee ID
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            List of attendance records
        """
        return self._request(
            'GET',
            '/attendance/getEmployeeAttendance',
            params={
                'employeeId': employee_id,
                'startDate': start_date,
                'endDate': end_date
            }
        )

    def clock_in(
        self,
        employee_id: str,
        timestamp: Optional[str] = None,
        location: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Record clock-in.

        Args:
            employee_id: Employee ID
            timestamp: Clock-in time in ISO format (default: now)
            location: Optional location string

        Returns:
            Clock-in record
        """
        data = {
            'employeeId': employee_id
        }
        if timestamp:
            data['timestamp'] = timestamp
        if location:
            data['location'] = location

        return self._request('POST', '/attendance/clockIn', data=data)

    def clock_out(
        self,
        employee_id: str,
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Record clock-out.

        Args:
            employee_id: Employee ID
            timestamp: Clock-out time in ISO format (default: now)

        Returns:
            Clock-out record
        """
        data = {
            'employeeId': employee_id
        }
        if timestamp:
            data['timestamp'] = timestamp

        return self._request('POST', '/attendance/clockOut', data=data)

    def get_leave_balance(self, employee_id: str) -> Dict[str, Any]:
        """
        Get leave balance for an employee.

        Args:
            employee_id: Employee ID

        Returns:
            Leave balance details
        """
        return self._request(
            'GET',
            '/leave/getLeaveBalance',
            params={'employeeId': employee_id}
        )

    def request_leave(
        self,
        employee_id: str,
        leave_type: str,
        from_date: str,
        to_date: str,
        days: float,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit a leave request.

        Args:
            employee_id: Employee ID
            leave_type: Type of leave
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            days: Number of days
            reason: Reason for leave (optional)

        Returns:
            Leave request details
        """
        data = {
            'employeeId': employee_id,
            'leaveType': leave_type,
            'from': from_date,
            'to': to_date,
            'days': days
        }
        if reason:
            data['reason'] = reason

        return self._request('POST', '/leave/apply', data=data)

    def get_leave_requests(
        self,
        employee_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get leave requests.

        Args:
            employee_id: Filter by employee (optional)
            status: Filter by status (optional)
            limit: Maximum number of results

        Returns:
            List of leave requests
        """
        params = {'limit': limit}
        if employee_id:
            params['employeeId'] = employee_id
        if status:
            params['status'] = status

        return self._request('GET', '/leave/getLeaveRequests', params=params)

    def approve_leave(
        self,
        request_id: str,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Approve a leave request.

        Args:
            request_id: Leave request ID
            comment: Approval comment (optional)

        Returns:
            Updated leave request
        """
        data = {'requestId': request_id, 'status': 'approved'}
        if comment:
            data['comment'] = comment

        return self._request('POST', '/leave/approve', data=data)

    def reject_leave(
        self,
        request_id: str,
        reason: str
    ) -> Dict[str, Any]:
        """
        Reject a leave request.

        Args:
            request_id: Leave request ID
            reason: Reason for rejection

        Returns:
            Updated leave request
        """
        data = {
            'requestId': request_id,
            'status': 'rejected',
            'reason': reason
        }

        return self._request('POST', '/leave/reject', data=data)

    def get_time_logs(
        self,
        employee_id: str,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Get time logs for an employee.

        Args:
            employee_id: Employee ID
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            List of time logs
        """
        return self._request(
            'GET',
            '/time/getTimeLogs',
            params={
                'employeeId': employee_id,
                'startDate': start_date,
                'endDate': end_date
            }
        )

    def create_time_log(
        self,
        employee_id: str,
        project_id: str,
        date: str,
        hours: float,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a time log.

        Args:
            employee_id: Employee ID
            project_id: Project ID
            date: Date in YYYY-MM-DD format
            hours: Hours worked
            description: Work description (optional)

        Returns:
            Created time log
        """
        data = {
            'employeeId': employee_id,
            'projectId': project_id,
            'date': date,
            'hours': hours
        }
        if description:
            data['description'] = description

        return self._request('POST', '/time/createTimeLog', data=data)

    def get_departments(self) -> List[Dict[str, Any]]:
        """
        Get list of departments.

        Returns:
            List of departments
        """
        return self._request('GET', '/forms/Department/getRecords')

    def get_department_employees(self, department_id: str) -> List[Dict[str, Any]]:
        """
        Get employees in a department.

        Args:
            department_id: Department ID

        Returns:
            List of employees
        """
        return self._request(
            'GET',
            f'/forms/Department/{department_id}/getEmployees'
        )

    def get_holidays(self, year: int) -> List[Dict[str, Any]]:
        """
        Get company holidays for a year.

        Args:
            year: Year to get holidays for

        Returns:
            List of holidays
        """
        return self._request(
            'GET',
            '/settings/getHolidays',
            params={'year': year}
        )

    def get_leave_types(self) -> List[Dict[str, Any]]:
        """
        Get configured leave types.

        Returns:
            List of leave types
        """
        return self._request('GET', '/settings/getLeaveTypes')

    def get_employee_documents(self, employee_id: str) -> List[Dict[str, Any]]:
        """
        Get employee documents.

        Args:
            employee_id: Employee ID

        Returns:
            List of documents
        """
        return self._request(
            'GET',
            f'/forms/P_Employee/{employee_id}/getDocuments'
        )

    def upload_document(
        self,
        employee_id: str,
        document_type: str,
        file_url: str
    ) -> Dict[str, Any]:
        """
        Upload a document for an employee.

        Args:
            employee_id: Employee ID
            document_type: Type of document
            file_url: URL of the file to upload

        Returns:
            Document details
        """
        return self._request(
            'POST',
            f'/forms/P_Employee/{employee_id}/uploadDocument',
            data={
                'documentType': document_type,
                'fileUrl': file_url
            }
        )