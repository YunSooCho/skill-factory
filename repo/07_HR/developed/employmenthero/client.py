"""
Employment Hero API Client - HR & Payroll Platform
"""

import requests
import time
from typing import Optional, Dict, Any


class EmploymentHeroError(Exception):
    """Base exception for Employment Hero"""


class EmploymentHeroClient:
    BASE_URL = "https://api.employmenthero.com/v1"

    def __init__(self, api_key: str, business_id: str, timeout: int = 30):
        """
        Initialize Employment Hero client

        Args:
            api_key: Employment Hero API key
            business_id: Business ID
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.business_id = business_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Business-ID': business_id
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
                raise EmploymentHeroError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise EmploymentHeroError(f"Error ({resp.status_code}): {resp.text}")

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
        """Create an employee"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/employees", json=employee_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_employee(self, employee_id: str, employee_data: Dict) -> Dict[str, Any]:
        """Update employee"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/employees/{employee_id}", json=employee_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Pay Items
    def get_pay_items(self) -> Dict[str, Any]:
        """Get pay items"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/pay_items", timeout=self.timeout)
        return self._handle_response(resp)

    # Leave Requests
    def get_leave_requests(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get leave requests"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/leave_requests", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_leave_request(self, request_data: Dict) -> Dict[str, Any]:
        """Create leave request"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/leave_requests", json=request_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Pay Slips
    def get_pay_slips(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get pay slips"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/pay_slips", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Payroll
    def get_payroll(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get payroll data"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/payroll", params=params, timeout=self.timeout)
        return self._handle_response(resp)