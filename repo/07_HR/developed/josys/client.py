"""
Josys API Client - Japanese IT Asset & SaaS Management
"""

import requests
import time
from typing import Optional, Dict, Any


class JosysError(Exception):
    """Base exception for Josys"""


class JosysClient:
    BASE_URL = "https://api.josys.io/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize Josys client

        Args:
            api_key: Josys API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
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
                raise JosysError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise JosysError(f"Error ({resp.status_code}): {resp.text}")

        if resp.status_code == 204:
            return {}
        return resp.json()

    # SaaS Applications
    def get_applications(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of SaaS applications"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/applications", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_application(self, app_id: str) -> Dict[str, Any]:
        """Get application details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/applications/{app_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_application(self, app_data: Dict) -> Dict[str, Any]:
        """Add new SaaS application"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/applications", json=app_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Employees & Assignments
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

    def get_employee_applications(self, employee_id: str) -> Dict[str, Any]:
        """Get applications assigned to employee"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/employees/{employee_id}/applications", timeout=self.timeout)
        return self._handle_response(resp)

    def assign_application(self, employee_id: str, app_id: str) -> Dict[str, Any]:
        """Assign application to employee"""
        self._enforce_rate_limit()
        resp = self.session.post(
            f"{self.BASE_URL}/employees/{employee_id}/applications",
            json={'application_id': app_id},
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def revoke_application(self, employee_id: str, assignment_id: str) -> Dict[str, Any]:
        """Revoke application access"""
        self._enforce_rate_limit()
        resp = self.session.delete(
            f"{self.BASE_URL}/employees/{employee_id}/applications/{assignment_id}",
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Hardware/Assets
    def get_devices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of devices"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/devices", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_device(self, device_id: str) -> Dict[str, Any]:
        """Get device details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/devices/{device_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_device(self, device_data: Dict) -> Dict[str, Any]:
        """Register new device"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/devices", json=device_data, timeout=self.timeout)
        return self._handle_response(resp)

    def assign_device(self, device_id: str, employee_id: str) -> Dict[str, Any]:
        """Assign device to employee"""
        self._enforce_rate_limit()
        resp = self.session.put(
            f"{self.BASE_URL}/devices/{device_id}/assign",
            json={'employee_id': employee_id},
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Usage & Analytics
    def get_usage_stats(self, app_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get application usage statistics"""
        self._enforce_rate_limit()
        params = {'start_date': start_date, 'end_date': end_date}
        resp = self.session.get(f"{self.BASE_URL}/applications/{app_id}/usage", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_license_usage(self, app_id: str) -> Dict[str, Any]:
        """Get license usage for application"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/applications/{app_id}/licenses", timeout=self.timeout)
        return self._handle_response(resp)

    # Alerts & Compliance
    def get_alerts(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get compliance and security alerts"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/alerts", params=params, timeout=self.timeout)
        return self._handle_response(resp)