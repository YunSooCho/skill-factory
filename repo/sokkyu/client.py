"""
Sokkyu API Client - Japan-based Rapid HR System
"""

import requests
import time
from typing import Optional, Dict, Any, List


class SokkyuError(Exception):
    """Base exception for Sokkyu"""


class SokkyuClient:
    BASE_URL = "https://api.sokkyu.jp/v1"

    def __init__(self, api_key: str, organization_id: str, timeout: int = 30):
        """
        Initialize Sokkyu client

        Args:
            api_key: Sokkyu API key
            organization_id: Organization ID
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.organization_id = organization_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Organization-ID': organization_id
        })

        self.last_request_time = 0
        self.min_delay = 0.2

    def _enforce_rate_limit(self):
        """Enforce rate limiting"""
        current = time.time()
        elapsed = current - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise SokkyuError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise SokkyuError(f"Error ({resp.status_code}): {resp.text}")

        if resp.status_code == 204:
            return {}
        return resp.json()

    def _get_params(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Add organization_id to params"""
        if params is None:
            params = {}
        params['organization_id'] = self.organization_id
        return params

    # Employees
    def get_employees(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of employees"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees",
                                params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """Get employee details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}",
                                params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def create_employee(self, employee_data: Dict) -> Dict[str, Any]:
        """Create an employee"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/employees",
                                params=self._get_params(), json=employee_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_employee(self, employee_id: str, employee_data: Dict) -> Dict[str, Any]:
        """Update employee"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/employees/{employee_id}",
                                params=self._get_params(), json=employee_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Attendance
    def get_attendance(self, employee_id: str, date: str) -> Dict[str, Any]:
        """Get attendance for employee on specific date"""
        self._enforce_rate_limit()
        params = self._get_params({'date': date})
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/attendance",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def clock_in(self, employee_id: str, timestamp: Optional[str] = None) -> Dict[str, Any]:
        """Clock in employee"""
        self._enforce_rate_limit()
        data = {'employee_id': employee_id}
        if timestamp:
            data['timestamp'] = timestamp

        resp = self.session.post(f"{self.BASE_URL}/attendance/clock-in",
                                params=self._get_params(), json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def clock_out(self, employee_id: str, timestamp: Optional[str] = None) -> Dict[str, Any]:
        """Clock out employee"""
        self._enforce_rate_limit()
        data = {'employee_id': employee_id}
        if timestamp:
            data['timestamp'] = timestamp

        resp = self.session.post(f"{self.BASE_URL}/attendance/clock-out",
                                params=self._get_params(), json=data, timeout=self.timeout)
        return self._handle_response(resp)

    # Leaves
    def get_leave_balances(self, employee_id: str) -> Dict[str, Any]:
        """Get leave balances for employee"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/leave-balances",
                                params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def get_leave_requests(self, employee_id: Optional[str] = None) -> Dict[str, Any]:
        """Get leave requests"""
        self._enforce_rate_limit()
        params = self._get_params()
        if employee_id:
            params['employee_id'] = employee_id

        resp = self.session.get(f"{self.BASE_URL}/leave-requests",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_leave_request(self, request_data: Dict) -> Dict[str, Any]:
        """Create leave request"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/leave-requests",
                                params=self._get_params(), json=request_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Payroll
    def get_payroll_summary(self, year: int, month: int, employee_id: Optional[str] = None) -> Dict[str, Any]:
        """Get payroll summary"""
        self._enforce_rate_limit()
        params = self._get_params({'year': year, 'month': month})
        if employee_id:
            params['employee_id'] = employee_id

        resp = self.session.get(f"{self.BASE_URL}/payroll/summary",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)