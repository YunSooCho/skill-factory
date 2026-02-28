"""
Insightful API Client - Employee Productivity & Analytics Platform
"""

import requests
import time
from typing import Optional, Dict, Any


class InsightfulError(Exception):
    """Base exception for Insightful"""


class InsightfulClient:
    BASE_URL = "https://api.insightful.io/v1"

    def __init__(self, api_key: str, workspace_id: str, timeout: int = 30):
        """
        Initialize Insightful client

        Args:
            api_key: Insightful API key
            workspace_id: Workspace ID
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.workspace_id = workspace_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Workspace-ID': workspace_id
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
                raise InsightfulError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise InsightfulError(f"Error ({resp.status_code}): {resp.text}")

        if resp.status_code == 204:
            return {}
        return resp.json()

    def _get_params(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Add workspace_id to params"""
        if params is None:
            params = {}
        params['workspace_id'] = self.workspace_id
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

    # Productivity
    def get_productivity_data(self, start_date: str, end_date: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get productivity data"""
        self._enforce_rate_limit()
        request_params = self._get_params(params)
        request_params['start_date'] = start_date
        request_params['end_date'] = end_date
        resp = self.session.get(f"{self.BASE_URL}/productivity", params=request_params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_employee_productivity(self, employee_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get productivity for specific employee"""
        self._enforce_rate_limit()
        params = self._get_params({'start_date': start_date, 'end_date': end_date})
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/productivity", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Activity
    def get_activity_logs(self, start_date: str, end_date: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get activity logs"""
        self._enforce_rate_limit()
        request_params = self._get_params(params)
        request_params['start_date'] = start_date
        request_params['end_date'] = end_date
        resp = self.session.get(f"{self.BASE_URL}/activity", params=request_params, timeout=self.timeout)
        return self._handle_response(resp)

    # Apps & Websites
    def get_app_usage(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get app usage analytics"""
        self._enforce_rate_limit()
        params = self._get_params({'start_date': start_date, 'end_date': end_date})
        resp = self.session.get(f"{self.BASE_URL}/analytics/apps", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_website_usage(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get website usage analytics"""
        self._enforce_rate_limit()
        params = self._get_params({'start_date': start_date, 'end_date': end_date})
        resp = self.session.get(f"{self.BASE_URL}/analytics/websites", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Reports
    def get_reports(self) -> Dict[str, Any]:
        """Get available reports"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/reports", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def get_report(self, report_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get specific report"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/reports/{report_id}", params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    # Projects
    def get_projects(self) -> Dict[str, Any]:
        """Get projects"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/projects", params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)