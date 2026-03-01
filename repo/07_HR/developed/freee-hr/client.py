"""
freee HR API Client - Japanese Cloud HR Platform
"""

import requests
import time
from typing import Optional, Dict, Any


class FreeeHRError(Exception):
    """Base exception for freee HR"""


class FreeeHRClient:
    BASE_URL = "https://api.freee.co.jp/hr/api/v1"

    def __init__(self, access_token: str, company_id: str, timeout: int = 30):
        """
        Initialize freee HR client

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
            'Content-Type': 'application/json'
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
                raise FreeeHRError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise FreeeHRError(f"Error ({resp.status_code}): {resp.text}")

        if resp.status_code == 204:
            return {}
        return resp.json()

    def _get_params(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Add company_id to params"""
        if params is None:
            params = {}
        params['company_id'] = self.company_id
        return params

    # Employees
    def get_employees(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of employees"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """Get employee details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def create_employee(self, employee_data: Dict) -> Dict[str, Any]:
        """Create an employee"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/employees", params=self._get_params(), json=employee_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_employee(self, employee_id: str, employee_data: Dict) -> Dict[str, Any]:
        """Update employee"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/employees/{employee_id}", params=self._get_params(), json=employee_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Work Types
    def get_work_types(self) -> Dict[str, Any]:
        """Get work types"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/work_types", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    # Departments
    def get_departments(self) -> Dict[str, Any]:
        """Get departments"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/departments", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    # Leave Types
    def get_leave_types(self) -> Dict[str, Any]:
        """Get leave types"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/leave_types", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    # Time Off Requests
    def get_time_off_requests(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get time off requests"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/time_off_requests", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def create_time_off_request(self, request_data: Dict) -> Dict[str, Any]:
        """Create time off request"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/time_off_requests", params=self._get_params(), json=request_data, timeout=self.timeout)
        return self._handle_response(resp)

    def approve_time_off_request(self, request_id: str) -> Dict[str, Any]:
        """Approve time off request"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/time_off_requests/{request_id}/approve", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)