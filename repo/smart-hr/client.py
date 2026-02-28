"""
SmartHR API Client - Japan-based HR Management System
"""

import requests
import time
from typing import Optional, Dict, Any, List


class SmartHRError(Exception):
    """Base exception for SmartHR"""


class SmartHRClient:
    BASE_URL = "https://api.smarkthr.jp/v1"

    def __init__(self, api_key: str, company_id: str, timeout: int = 30):
        """
        Initialize SmartHR client

        Args:
            api_key: SmartHR API key
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
                raise SmartHRError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise SmartHRError(f"Error ({resp.status_code}): {resp.text}")

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
    def get_employees(self, params: Optional[Dict] = None,
                     page: int = 1, limit: int = 100) -> Dict[str, Any]:
        """Get list of employees"""
        self._enforce_rate_limit()
        params = self._get_params(params or {})
        params['page'] = page
        params['limit'] = limit

        resp = self.session.get(f"{self.BASE_URL}/employees",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """Get employee details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}",
                                params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def create_employee(self, employee_data: Dict) -> Dict[str, Any]:
        """Create an employee"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/employees",
                                params=self._get_params(), json=employee_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_employee(self, employee_id: str, employee_data: Dict) -> Dict[str, Any]:
        """Update employee"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/employees/{employee_id}",
                                params=self._get_params(), json=employee_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Employment Info
    def get_employment_info(self, employee_id: str) -> Dict[str, Any]:
        """Get employment information for employee"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/employment",
                                params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def update_employment_info(self, employee_id: str, employment_data: Dict) -> Dict[str, Any]:
        """Update employment information"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/employees/{employee_id}/employment",
                                params=self._get_params(), json=employment_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Attendance
    def get_attendance_records(self, employee_id: str, year: int, month: int) -> Dict[str, Any]:
        """Get attendance records for employee"""
        self._enforce_rate_limit()
        params = self._get_params({'year': year, 'month': month})
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/attendance",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Leaves
    def get_leave_balances(self, employee_id: str) -> Dict[str, Any]:
        """Get leave balances for employee"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/leave-balances",
                                params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def get_leave_requests(self, employee_id: Optional[str] = None,
                          status: Optional[str] = None) -> Dict[str, Any]:
        """Get leave requests"""
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

    # Documents
    def get_documents(self, employee_id: Optional[str] = None,
                     document_type: Optional[str] = None) -> Dict[str, Any]:
        """Get HR documents"""
        self._enforce_rate_limit()
        params = self._get_params()
        if employee_id:
            params['employee_id'] = employee_id
        if document_type:
            params['document_type'] = document_type

        resp = self.session.get(f"{self.BASE_URL}/documents",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def upload_document(self, document_data: Dict) -> Dict[str, Any]:
        """Upload HR document"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/documents",
                                params=self._get_params(), json=document_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Notifications
    def send_notification(self, notification_data: Dict) -> Dict[str, Any]:
        """Send notification to employees"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/notifications",
                                params=self._get_params(), json=notification_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Workflow
    def get_workflows(self, status: Optional[str] = None) -> Dict[str, Any]:
        """Get workflow approvals"""
        self._enforce_rate_limit()
        params = self._get_params()
        if status:
            params['status'] = status

        resp = self.session.get(f"{self.BASE_URL}/workflows",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def approve_workflow(self, workflow_id: str, comment: Optional[str] = None) -> Dict[str, Any]:
        """Approve workflow"""
        self._enforce_rate_limit()
        data = {}
        if comment:
            data['comment'] = comment

        resp = self.session.post(f"{self.BASE_URL}/workflows/{workflow_id}/approve",
                                params=self._get_params(), json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def reject_workflow(self, workflow_id: str, reason: str) -> Dict[str, Any]:
        """Reject workflow"""
        self._enforce_rate_limit()
        data = {'reason': reason}
        resp = self.session.post(f"{self.BASE_URL}/workflows/{workflow_id}/reject",
                                params=self._get_params(), json=data, timeout=self.timeout)
        return self._handle_response(resp)