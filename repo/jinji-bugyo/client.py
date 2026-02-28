"""
Jinji-Bugyo API Client - Japanese Payroll & HR System
"""

import requests
import time
from typing import Optional, Dict, Any


class JinjiBugyoError(Exception):
    """Base exception for Jinji-Bugyo"""


class JinjiBugyoClient:
    BASE_URL = "https://api.jinji-bugyo.com/v1"

    def __init__(self, api_key: str, company_id: str, timeout: int = 30):
        """
        Initialize Jinji-Bugyo client

        Args:
            api_key: Jinji-Bugyo API key
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
                raise JinjiBugyoError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise JinjiBugyoError(f"Error ({resp.status_code}): {resp.text}")

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

    # Payroll
    def get_payroll(self, year: int, month: int) -> Dict[str, Any]:
        """Get payroll data for year/month"""
        self._enforce_rate_limit()
        params = self._get_params({'year': year, 'month': month})
        resp = self.session.get(f"{self.BASE_URL}/payroll", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_employee_payroll(self, employee_id: str, year: int, month: int) -> Dict[str, Any]:
        """Get payroll for specific employee"""
        self._enforce_rate_limit()
        params = self._get_params({'year': year, 'month': month})
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/payroll", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Salary
    def get_salary_records(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get salary records"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/salary", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def update_salary(self, employee_id: str, salary_data: Dict) -> Dict[str, Any]:
        """Update employee salary"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/employees/{employee_id}/salary", params=self._get_params(), json=salary_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Deductions
    def get_deductions(self, employee_id: str) -> Dict[str, Any]:
        """Get deductions for employee"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/deductions", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    # Allowances
    def get_allowances(self, employee_id: str) -> Dict[str, Any]:
        """Get allowances for employee"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/allowances", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    # Bonuses
    def create_bonus(self, bonus_data: Dict) -> Dict[str, Any]:
        """Create bonus payment"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/bonuses", params=self._get_params(), json=bonus_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Social Insurance
    def get_social_insurance(self, employee_id: str) -> Dict[str, Any]:
        """Get social insurance info for employee"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/social-insurance", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)