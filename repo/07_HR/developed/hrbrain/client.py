"""
HRBrain API Client - Japanese HR Management Platform
"""

import requests
import time
from typing import Optional, Dict, Any


class HRBrainError(Exception):
    """Base exception for HRBrain"""


class HRBrainClient:
    BASE_URL = "https://api.hrbrain.co.jp/v1"

    def __init__(self, api_key: str, company_id: str, timeout: int = 30):
        """
        Initialize HRBrain client

        Args:
            api_key: HRBrain API key
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
                raise HRBrainError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise HRBrainError(f"Error ({resp.status_code}): {resp.text}")

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

    # Performance
    def get_performances(self, employee_id: Optional[str] = None) -> Dict[str, Any]:
        """Get performance records"""
        self._enforce_rate_limit()
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        resp = self.session.get(f"{self.BASE_URL}/performances", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_performance(self, performance_data: Dict) -> Dict[str, Any]:
        """Create performance record"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/performances", json=performance_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Training
    def get_trainings(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get training records"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/trainings", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_training(self, training_data: Dict) -> Dict[str, Any]:
        """Create training record"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/trainings", json=training_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Goals
    def get_goals(self, employee_id: Optional[str] = None) -> Dict[str, Any]:
        """Get goals"""
        self._enforce_rate_limit()
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        resp = self.session.get(f"{self.BASE_URL}/goals", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_goal(self, goal_data: Dict) -> Dict[str, Any]:
        """Create goal"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/goals", json=goal_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Surveys
    def get_surveys(self) -> Dict[str, Any]:
        """Get surveys"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/surveys", timeout=self.timeout)
        return self._handle_response(resp)