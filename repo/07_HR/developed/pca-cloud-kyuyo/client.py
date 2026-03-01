"""
PCA Cloud Kyuyo API Client - Japanese Payroll System
"""

import requests
import time
from typing import Optional, Dict, Any


class PcaCloudKyuyoError(Exception):
    """Base exception for PCA Cloud Kyuyo"""


class PcaCloudKyuyoClient:
    BASE_URL = "https://api-cloud.pc-cloud.jp/payslip/v2"

    def __init__(self, api_key: str, company_code: str, timeout: int = 30):
        """
        Initialize PCA Cloud Kyuyo client

        Args:
            api_key: PCA Cloud Kyuyo API key
            company_code: Company code
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.company_code = company_code
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
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
                raise PcaCloudKyuyoError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise PcaCloudKyuyoError(f"Error ({resp.status_code}): {resp.text}")

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

    # Pay Slips
    def get_payslips(self, year: int, month: int) -> Dict[str, Any]:
        """Get payslips"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(f"{self.BASE_URL}/payslips", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_payslip(self, employee_id: str, year: int, month: int) -> Dict[str, Any]:
        """Get employee payslip"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/payslip",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def download_payslip_pdf(self, employee_id: str, year: int, month: int) -> bytes:
        """Download payslip PDF"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/payslip/pdf",
            params=params,
            timeout=self.timeout
        )
        if resp.status_code != 200:
            raise PcaCloudKyuyoError(f"Failed to download PDF: {resp.status_code}")
        return resp.content

    # Salaries
    def get_salaries(self, year: int, month: int) -> Dict[str, Any]:
        """Get salary records"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(f"{self.BASE_URL}/salaries", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def update_salary(self, employee_id: str, salary_data: Dict) -> Dict[str, Any]:
        """Update salary"""
        self._enforce_rate_limit()
        resp = self.session.put(
            f"{self.BASE_URL}/employees/{employee_id}/salary",
            json=salary_data,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Deductions & Allowances
    def get_deductions(self, employee_id: str, year: int, month: int) -> Dict[str, Any]:
        """Get deductions"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/deductions",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def get_allowances(self, employee_id: str, year: int, month: int) -> Dict[str, Any]:
        """Get allowances"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/allowances",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Bonuses
    def get_bonuses(self, year: int, season: Optional[int] = None) -> Dict[str, Any]:
        """Get bonus records"""
        self._enforce_rate_limit()
        params = {'year': year}
        if season:
            params['season'] = season
        resp = self.session.get(f"{self.BASE_URL}/bonuses", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_bonus(self, bonus_data: Dict) -> Dict[str, Any]:
        """Create bonus"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/bonuses", json=bonus_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Social Insurance & Taxes
    def get_social_insurance(self, employee_id: str, year: int, month: int) -> Dict[str, Any]:
        """Get social insurance"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/social-insurance",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def get_taxes(self, employee_id: str, year: int, month: int) -> Dict[str, Any]:
        """Get taxes"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(
            f"{self.BASE_URL}/employees/{employee_id}/taxes",
            params=params,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Reports
    def get_payroll_report(self, year: int, month: int) -> Dict[str, Any]:
        """Get payroll report"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(f"{self.BASE_URL}/reports/payroll", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Closing
    def close_month(self, year: int, month: int) -> Dict[str, Any]:
        """Close payroll month"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.post(f"{self.BASE_URL}/payroll/close", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_closing_status(self, year: int, month: int) -> Dict[str, Any]:
        """Get closing status"""
        self._enforce_rate_limit()
        params = {'year': year, 'month': month}
        resp = self.session.get(f"{self.BASE_URL}/payroll/closing-status", params=params, timeout=self.timeout)
        return self._handle_response(resp)