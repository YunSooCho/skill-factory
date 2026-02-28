"""
Smaregi Timecard API Client - Japan-based Time Attendance System
"""

import requests
import time
from typing import Optional, Dict, Any, List


class SmaregiTimecardError(Exception):
    """Base exception for Smaregi Timecard"""


class SmaregiTimecardClient:
    BASE_URL = "https://api.smaregi.jp/timecard/v1"

    def __init__(self, access_token: str, contract_id: str, timeout: int = 30):
        """
        Initialize Smaregi Timecard client

        Args:
            access_token: Smaregi API access token
            contract_id: Contract ID (契約ID)
            timeout: Request timeout in seconds
        """
        self.access_token = access_token
        self.contract_id = contract_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Contract-ID': contract_id
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
                raise SmaregiTimecardError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise SmaregiTimecardError(f"Error ({resp.status_code}): {resp.text}")

        if resp.status_code == 204:
            return {}
        return resp.json()

    def _get_params(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Add contract_id to params"""
        if params is None:
            params = {}
        params['contract_id'] = self.contract_id
        return params

    # Timecard Records
    def get_punch_records(self, employee_id: Optional[str] = None,
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get punch/clock-in records

        Args:
            employee_id: Filter by employee ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        """
        self._enforce_rate_limit()
        params = self._get_params()
        if employee_id:
            params['employee_id'] = employee_id
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date

        resp = self.session.get(f"{self.BASE_URL}/punch-records",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_punch_record(self, record_id: str) -> Dict[str, Any]:
        """Get specific punch record details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/punch-records/{record_id}",
                                params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def clock_in(self, employee_id: str, timestamp: Optional[str] = None,
                device_info: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Clock in employee

        Args:
            employee_id: Employee ID
            timestamp: Clock-in time (ISO8601, defaults to now)
            device_info: Optional device/location information
        """
        self._enforce_rate_limit()
        data = {'employee_id': employee_id}
        if timestamp:
            data['timestamp'] = timestamp
        if device_info:
            data['device_info'] = device_info

        resp = self.session.post(f"{self.BASE_URL}/punch-records/clock-in",
                                params=self._get_params(), json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def clock_out(self, employee_id: str, timestamp: Optional[str] = None,
                 clock_in_record_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Clock out employee

        Args:
            employee_id: Employee ID
            timestamp: Clock-out time (ISO8601, defaults to now)
            clock_in_record_id: Paired clock-in record ID
        """
        self._enforce_rate_limit()
        data = {'employee_id': employee_id}
        if timestamp:
            data['timestamp'] = timestamp
        if clock_in_record_id:
            data['clock_in_record_id'] = clock_in_record_id

        resp = self.session.post(f"{self.BASE_URL}/punch-records/clock-out",
                                params=self._get_params(), json=data, timeout=self.timeout)
        return self._handle_response(resp)

    # Daily Work Records
    def get_daily_records(self, employee_id: Optional[str] = None,
                         date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get daily work records

        Args:
            employee_id: Filter by employee ID
            date: Filter by date (YYYY-MM-DD)
        """
        self._enforce_rate_limit()
        params = self._get_params()
        if employee_id:
            params['employee_id'] = employee_id
        if date:
            params['date'] = date

        resp = self.session.get(f"{self.BASE_URL}/daily-records",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_daily_record(self, record_id: str) -> Dict[str, Any]:
        """Get daily work record details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/daily-records/{record_id}",
                                params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def update_daily_record(self, record_id: str, record_data: Dict) -> Dict[str, Any]:
        """Update daily work record (for corrections)"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/daily-records/{record_id}",
                                params=self._get_params(), json=record_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Monthly Records
    def get_monthly_records(self, year: int, month: int,
                           employee_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get monthly work records

        Args:
            year: Year
            month: Month (1-12)
            employee_id: Filter by employee ID
        """
        self._enforce_rate_limit()
        params = self._get_params({
            'year': year,
            'month': month
        })
        if employee_id:
            params['employee_id'] = employee_id

        resp = self.session.get(f"{self.BASE_URL}/monthly-records",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_monthly_record(self, record_id: str) -> Dict[str, Any]:
        """Get monthly work record details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/monthly-records/{record_id}",
                                params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    # Employees
    def get_employees(self) -> Dict[str, Any]:
        """Get list of employees"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees",
                                params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """Get employee details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}",
                                params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    # Requests/Approvals
    def get_leave_requests(self, employee_id: Optional[str] = None,
                          status: Optional[str] = None) -> Dict[str, Any]:
        """
        Get leave requests

        Args:
            employee_id: Filter by employee ID
            status: Filter by status (pending, approved, rejected)
        """
        self._enforce_rate_limit()
        params = self._get_params()
        if employee_id:
            params['employee_id'] = employee_id
        if status:
            params['status'] = status

        resp = self.session.get(f"{self.BASE_URL}/leave-requests",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_leave_request(self, request_data: Dict) -> Dict[str, Any]:
        """Create leave request"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/leave-requests",
                                params=self._get_params(), json=request_data, timeout=self.timeout)
        return self._handle_response(resp)

    def approve_request(self, request_id: str, comment: Optional[str] = None) -> Dict[str, Any]:
        """Approve leave request"""
        self._enforce_rate_limit()
        data = {}
        if comment:
            data['comment'] = comment

        resp = self.session.post(f"{self.BASE_URL}/leave-requests/{request_id}/approve",
                                params=self._get_params(), json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def reject_request(self, request_id: str, reason: str) -> Dict[str, Any]:
        """Reject leave request"""
        self._enforce_rate_limit()
        data = {'reason': reason}
        resp = self.session.post(f"{self.BASE_URL}/leave-requests/{request_id}/reject",
                                params=self._get_params(), json=data, timeout=self.timeout)
        return self._handle_response(resp)