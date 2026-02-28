"""
King of Time API Client - Japanese Time & Attendance System
"""

import requests
import time
from typing import Optional, Dict, Any
from datetime import datetime


class KingOfTimeError(Exception):
    """Base exception for King of Time"""


class KingOfTimeClient:
    BASE_URL = "https://api.ta.kingtime.jp/independent/api/v1"

    def __init__(self, api_token: str, company_code: str, timeout: int = 30):
        """
        Initialize King of Time client

        Args:
            api_token: King of Time API token
            company_code: Company code
            timeout: Request timeout in seconds
        """
        self.api_token = api_token
        self.company_code = company_code
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
            'X-Company-Code': company_code
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
                raise KingOfTimeError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise KingOfTimeError(f"Error ({resp.status_code}): {resp.text}")

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

    # Daily Attendance
    def get_daily_attendance(self, employee_id: str, date: str) -> Dict[str, Any]:
        """Get daily attendance record"""
        self._enforce_rate_limit()
        params = {'date': date}
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/daily-attendance",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def update_daily_attendance(self, employee_id: str, date: str, data: Dict) -> Dict[str, Any]:
        """Update daily attendance"""
        self._enforce_rate_limit()
        params = {'date': date}
        resp = self.session.put(
            f"{self.BASE_URL}/employees/{employee_id}/daily-attendance",
            params=params,
            json=data,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Clock In/Out
    def clock_in(self, employee_id: str, timestamp: Optional[str] = None) -> Dict[str, Any]:
        """Clock in"""
        self._enforce_rate_limit()
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        resp = self.session.post(
            f"{self.BASE_URL}/employees/{employee_id}/clock-in",
            json={'timestamp': timestamp},
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def clock_out(self, employee_id: str, timestamp: Optional[str] = None) -> Dict[str, Any]:
        """Clock out"""
        self._enforce_rate_limit()
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        resp = self.session.post(
            f"{self.BASE_URL}/employees/{employee_id}/clock-out",
            json={'timestamp': timestamp},
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Monthly Attendance
    def get_monthly_attendance(self, employee_id: str, year: int, month: int) -> Dict[str, Any]:
        """Get monthly attendance"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/monthly-attendance",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Time Off Requests
    def get_time_off_requests(self, employee_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get time off requests"""
        self._enforce_rate_limit()
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/time-off-requests",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def create_time_off_request(self, employee_id: str, request_data: Dict) -> Dict[str, Any]:
        """Create time off request"""
        self._enforce_rate_limit()
        resp = self.session.post(
            f"{self.BASE_URL}/employees/{employee_id}/time-off-requests",
            json=request_data,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def approve_time_off_request(self, request_id: str) -> Dict[str, Any]:
        """Approve time off request"""
        self._enforce_rate_limit()
        resp = self.session.put(
            f"{self.BASE_URL}/time-off-requests/{request_id}/approve",
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def reject_time_off_request(self, request_id: str, reason: str) -> Dict[str, Any]:
        """Reject time off request"""
        self._enforce_rate_limit()
        resp = self.session.put(
            f"{self.BASE_URL}/time-off-requests/{request_id}/reject",
            json={'reason': reason},
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Overtime
    def get_overtime_records(self, employee_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get overtime records"""
        self._enforce_rate_limit()
        params = {'start_date': start_date, 'end_date': end_date}
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/overtime",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Schedule
    def get_schedule(self, employee_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get schedule"""
        self._enforce_rate_limit()
        params = {'start_date': start_date, 'end_date': end_date}
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/schedule",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def update_schedule(self, employee_id: str, schedule_data: Dict) -> Dict[str, Any]:
        """Update schedule"""
        self._enforce_rate_limit()
        resp = self.session.put(
            f"{self.BASE_URL}/employees/{employee_id}/schedule",
            json=schedule_data,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Work Locations
    def get_work_locations(self) -> Dict[str, Any]:
        """Get work locations"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/work-locations", timeout=self.timeout)
        return self._handle_response(resp)