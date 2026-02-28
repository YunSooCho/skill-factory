"""
MoneyForward Admina API Client - Japanese Cloud Accounting & HR
"""

import requests
import time
from typing import Optional, Dict, Any


class MoneyForwardAdminaError(Exception):
    """Base exception for MoneyForward Admina"""


class MoneyForwardAdminaClient:
    BASE_URL = "https://invoice.moneyforward.com/api/v2"

    def __init__(self, api_key: str, company_id: str, timeout: int = 30):
        """
        Initialize MoneyForward Admina client

        Args:
            api_key: MoneyForward Admina API key
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
            'X-Tenant-ID': company_id
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
                raise MoneyForwardAdminaError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise MoneyForwardAdminaError(f"Error ({resp.status_code}): {resp.text}")

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

    def create_department(self, dept_data: Dict) -> Dict[str, Any]:
        """Create department"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/departments", json=dept_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Payroll
    def get_payroll(self, year: int, month: int) -> Dict[str, Any]:
        """Get payroll"""
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

    # Approval Flows
    def get_approval_requests(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get approval requests"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/approval-requests", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def approve_request(self, request_id: str, comment: Optional[str] = None) -> Dict[str, Any]:
        """Approve request"""
        self._enforce_rate_limit()
        data = {'status': 'approved'}
        if comment:
            data['comment'] = comment
        resp = self.session.put(
            f"{self.BASE_URL}/approval-requests/{request_id}",
            json=data,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def reject_request(self, request_id: str, reason: str) -> Dict[str, Any]:
        """Reject request"""
        self._enforce_rate_limit()
        resp = self.session.put(
            f"{self.BASE_URL}/approval-requests/{request_id}",
            json={'status': 'rejected', 'comment': reason},
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Time Off
    def get_time_off(self, employee_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get time off records"""
        self._enforce_rate_limit()
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/time-off",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def request_time_off(self, employee_id: str, time_off_data: Dict) -> Dict[str, Any]:
        """Request time off"""
        self._enforce_rate_limit()
        resp = self.session.post(
            f"{self.BASE_URL}/employees/{employee_id}/time-off",
            json=time_off_data,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Expenses
    def get_expenses(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get expenses"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/expenses", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_expense(self, expense_data: Dict) -> Dict[str, Any]:
        """Create expense"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/expenses", json=expense_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_employee_expenses(self, employee_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get employee expenses"""
        self._enforce_rate_limit()
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/expenses",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Invoices
    def get_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get invoices"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/invoices", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        """Create invoice"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/invoices", json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Reports
    def get_payroll_report(self, year: int, month: int) -> Dict[str, Any]:
        """Get payroll report"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(f"{self.BASE_URL}/reports/payroll", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_expense_report(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get expense report"""
        self._enforce_rate_limit()
        params = {'start_date': start_date, 'end_date': end_date}
        resp = self.session.get(f"{self.BASE_URL}/reports/expenses", params=params, timeout=self.timeout)
        return self._handle_response(resp)