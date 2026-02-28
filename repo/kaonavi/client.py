"""
Kaonavi API Client - Japanese HR & Employee Information System
"""

import requests
import time
from typing import Optional, Dict, Any


class KaonaviError(Exception):
    """Base exception for Kaonavi"""


class KaonaviClient:
    BASE_URL = "https://api.ta.kingtime.jp/independent/api/v1"

    def __init__(self, api_key: str, company_code: str, timeout: int = 30):
        """
        Initialize Kaonavi client

        Args:
            api_key: Kaonavi API key
            company_code: Company code
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.company_code = company_code
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
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
                raise KaonaviError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise KaonaviError(f"Error ({resp.status_code}): {resp.text}")

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
        resp = self.session.put(f"{self.BASE_URL}/employees/{employee_id}", json=employee_data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_employee(self, employee_id: str) -> Dict[str, Any]:
        """Delete employee"""
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.BASE_URL}/employees/{employee_id}", timeout=self.timeout)
        return self._handle_response(resp)

    # Departments & Organizations
    def get_departments(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get departments"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/departments", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_department(self, dept_id: str) -> Dict[str, Any]:
        """Get department details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/departments/{dept_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_department(self, dept_data: Dict) -> Dict[str, Any]:
        """Create department"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/departments", json=dept_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Positions & Titles
    def get_positions(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get positions"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/positions", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_position(self, position_id: str) -> Dict[str, Any]:
        """Get position details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/positions/{position_id}", timeout=self.timeout)
        return self._handle_response(resp)

    # Employment Status
    def get_employment_statuses(self) -> Dict[str, Any]:
        """Get employment status types"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employment-statuses", timeout=self.timeout)
        return self._handle_response(resp)

    def update_employment_status(self, employee_id: str, status_data: Dict) -> Dict[str, Any]:
        """Update employee employment status"""
        self._enforce_rate_limit()
        resp = self.session.put(
            f"{self.BASE_URL}/employees/{employee_id}/employment-status",
            json=status_data,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Custom Fields
    def get_custom_fields(self) -> Dict[str, Any]:
        """Get custom field definitions"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/custom-fields", timeout=self.timeout)
        return self._handle_response(resp)

    def update_custom_field(self, employee_id: str, field_id: str, value: Any) -> Dict[str, Any]:
        """Update custom field value"""
        self._enforce_rate_limit()
        resp = self.session.put(
            f"{self.BASE_URL}/employees/{employee_id}/custom-fields/{field_id}",
            json={'value': value},
            timeout=self.timeout
        )
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

    # Reports
    def get_employee_report(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get employee report"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/reports/employees", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_organization_report(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get organization report"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/reports/organizations", params=params, timeout=self.timeout)
        return self._handle_response(resp)