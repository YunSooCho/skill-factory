"""
Akashi API Client - Japanese Attendance & HR Management
"""

import requests
import time
from typing import Optional, Dict, Any, List


class AkashiError(Exception):
    """Base exception for Akashi"""

class AkashiRateLimitError(AkashiError):
    """Rate limit exceeded"""

class AkashiAuthenticationError(AkashiError):
    """Authentication failed"""

class AkashiClient:
    BASE_URL = "https://api.akashi.co.jp/v1"

    def __init__(self, api_key: str, company_id: str, timeout: int = 30):
        """
        Initialize Akashi client

        Args:
            api_key: Akashi API key
            company_id: Company ID
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.company_id = company_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Company-ID': company_id
        })

        # Rate limiting
        self.last_request_time = 0
        self.min_delay = 0.5

    def _enforce_rate_limit(self):
        """Enforce rate limiting"""
        current = time.time()
        elapsed = current - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if resp.status_code == 429:
            raise AkashiRateLimitError("Rate limit exceeded")
        if resp.status_code == 401 or resp.status_code == 403:
            raise AkashiAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise AkashiError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise AkashiError(f"Error ({resp.status_code}): {resp.text}")

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

    def add_employee(self, employee_data: Dict) -> Dict[str, Any]:
        """Add a new employee"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/employees", json=employee_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_employee(self, employee_id: str, employee_data: Dict) -> Dict[str, Any]:
        """Update employee information"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/employees/{employee_id}", json=employee_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Attendance Records
    def get_attendance(self, employee_id: str, date: str) -> Dict[str, Any]:
        """Get attendance record for specific date"""
        self._enforce_rate_limit()
        params = {'date': date}
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/attendance", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_attendance_records(self, employee_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get attendance records for a date range"""
        self._enforce_rate_limit()
        params = {'start_date': start_date, 'end_date': end_date}
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/attendance/records", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Clock In/Out
    def clock_in(self, employee_id: str, timestamp: Optional[str] = None, note: Optional[str] = None) -> Dict[str, Any]:
        """Clock in an employee"""
        self._enforce_rate_limit()
        data = {}
        if timestamp:
            data['timestamp'] = timestamp
        if note:
            data['note'] = note
        resp = self.session.post(f"{self.BASE_URL}/employees/{employee_id}/clock-in", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def clock_out(self, employee_id: str, timestamp: Optional[str] = None, note: Optional[str] = None) -> Dict[str, Any]:
        """Clock out an employee"""
        self._enforce_rate_limit()
        data = {}
        if timestamp:
            data['timestamp'] = timestamp
        if note:
            data['note'] = note
        resp = self.session.post(f"{self.BASE_URL}/employees/{employee_id}/clock-out", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    # Work Records
    def get_work_records(self, employee_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get work records for a date range"""
        self._enforce_rate_limit()
        params = {'start_date': start_date, 'end_date': end_date}
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/work-records", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Leave Requests
    def get_leave_requests(self, employee_id: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """Get leave requests"""
        self._enforce_rate_limit()
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        if status:
            params['status'] = status
        resp = self.session.get(f"{self.BASE_URL}/leave-requests", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_leave_request(self, request_data: Dict) -> Dict[str, Any]:
        """Create a leave request"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/leave-requests", json=request_data, timeout=self.timeout)
        return self._handle_response(resp)

    def approve_leave_request(self, request_id: str) -> Dict[str, Any]:
        """Approve a leave request"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/leave-requests/{request_id}/approve", timeout=self.timeout)
        return self._handle_response(resp)

    def reject_leave_request(self, request_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Reject a leave request"""
        self._enforce_rate_limit()
        data = {}
        if reason:
            data['reason'] = reason
        resp = self.session.put(f"{self.BASE_URL}/leave-requests/{request_id}/reject", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    # Overtime Requests
    def get_overtime_requests(self, employee_id: Optional[str] = None) -> Dict[str, Any]:
        """Get overtime requests"""
        self._enforce_rate_limit()
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        resp = self.session.get(f"{self.BASE_URL}/overtime-requests", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Departments
    def get_departments(self) -> Dict[str, Any]:
        """Get list of departments"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/departments", timeout=self.timeout)
        return self._handle_response(resp)