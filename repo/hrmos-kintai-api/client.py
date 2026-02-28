"""
HRmos Kintai API - Attendance Management API
"""

import requests
import time
from typing import Optional, Dict, Any


class HRmosKintaiError(Exception):
    """Base exception for HRmos Kintai"""


class HRmosKintaiClient:
    BASE_URL = "https://api.hrmos.co/kintai/v1"

    def __init__(self, access_token: str, company_id: str, timeout: int = 30):
        """
        Initialize HRmos Kintai client

        Args:
            access_token: OAuth access token
            company_id: Company ID
            timeout: Request timeout in seconds
        """
        self.access_token = access_token
        self.company_id = company_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Company-ID': company_id
        })

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
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise HRmosKintaiError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise HRmosKintaiError(f"Error ({resp.status_code}): {resp.text}")

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

    # Attendance
    def get_attendance(self, employee_id: str, date: str) -> Dict[str, Any]:
        """Get attendance for specific date"""
        self._enforce_rate_limit()
        params = {'date': date}
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/attendance", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_attendance_records(self, employee_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get attendance records for date range"""
        self._enforce_rate_limit()
        params = {'start_date': start_date, 'end_date': end_date}
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/attendance/records", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Clock In/Out
    def clock_in(self, employee_id: str, timestamp: Optional[str] = None, note: Optional[str] = None) -> Dict[str, Any]:
        """Clock in"""
        self._enforce_rate_limit()
        data = {}
        if timestamp:
            data['timestamp'] = timestamp
        if note:
            data['note'] = note
        resp = self.session.post(f"{self.BASE_URL}/employees/{employee_id}/clock-in", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def clock_out(self, employee_id: str, timestamp: Optional[str] = None, note: Optional[str] = None) -> Dict[str, Any]:
        """Clock out"""
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
        """Get work records"""
        self._enforce_rate_limit()
        params = {'start_date': start_date, 'end_date': end_date}
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/work-records", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Leave Requests
    def get_leave_requests(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get leave requests"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/leave-requests", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_leave_request(self, request_data: Dict) -> Dict[str, Any]:
        """Create leave request"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/leave-requests", json=request_data, timeout=self.timeout)
        return self._handle_response(resp)

    def approve_leave_request(self, request_id: str) -> Dict[str, Any]:
        """Approve leave request"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/leave-requests/{request_id}/approve", timeout=self.timeout)
        return self._handle_response(resp)

    # Overtime
    def get_overtime_requests(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get overtime requests"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/overtime-requests", params=params, timeout=self.timeout)
        return self._handle_response(resp)