"""
Rakuro API Client - Japanese HR Management System
"""

import requests
import time
from typing import Optional, Dict, Any


class RakuroError(Exception):
    """Base exception for Rakuro"""


class RakuroClient:
    BASE_URL = "https://api.rakuro.jp/v1"

    def __init__(self, api_key: str, tenant_id: str, timeout: int = 30):
        """
        Initialize Rakuro client

        Args:
            api_key: Rakuro API key
            tenant_id: Tenant ID
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.tenant_id = tenant_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Tenant-ID': tenant_id
        })

        self.last_request_time = 0
        self.min_delay = 0.3

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
                raise RakuroError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise RakuroError(f"Error ({resp.status_code}): {resp.text}")

        if resp.status_code == 204:
            return {}
        return resp.json()

    # Employees
    def get_employees(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of employees"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """Get employee details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_employee(self, employee_data: Dict) -> Dict[str, Any]:
        """Create employee"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/employees", json=employee_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_employee(self, employee_id: str, employee_data: Dict) -> Dict[str, Any]:
        """Update employee"""
        self._enforce_rate_limit()
        resp = self.session.put(
            f"{self.BASE_URL}/employees/{employee_id}",
            json=employee_data,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Departments
    def get_departments(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get departments"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/departments", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Attendance
    def get_attendance(self, employee_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get attendance records"""
        self._enforce_rate_limit()
        params = {'start_date': start_date, 'end_date': end_date}
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/attendance",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Time Off
    def get_time_off_requests(self, employee_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get time off requests"""
        self._enforce_rate_limit()
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/time-off",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def create_time_off_request(self, employee_id: str, request_data: Dict) -> Dict[str, Any]:
        """Create time off request"""
        self._enforce_rate_limit()
        resp = self.session.post(
            f"{self.BASE_URL}/employees/{employee_id}/time-off",
            json=request_data,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Payroll
    def get_payroll(self, year: int, month: int) -> Dict[str, Any]:
        """Get payroll data"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(f"{self.BASE_URL}/payroll", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_employee_payroll(self, employee_id: str, year: int, month: int) -> Dict[str, Any]:
        """Get employee payroll"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/payroll",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Reports
    def get_employee_report(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get employee report"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/reports/employees", params=params, timeout=self.timeout)
        return self._handle_response(resp)