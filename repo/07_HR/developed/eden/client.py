"""
Eden API Client - Employee Engagement Platform
"""

import requests
import time
from typing import Optional, Dict, Any


class EdenError(Exception):
    """Base exception for Eden"""


class EdenClient:
    BASE_URL = "https://api.eden.io/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize Eden client

        Args:
            api_key: Eden API key
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
                raise EdenError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise EdenError(f"Error ({resp.status_code}): {resp.text}")

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

    # Surveys
    def get_surveys(self) -> Dict[str, Any]:
        """Get list of surveys"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/surveys", timeout=self.timeout)
        return self._handle_response(resp)

    def create_survey(self, survey_data: Dict) -> Dict[str, Any]:
        """Create a survey"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/surveys", json=survey_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_survey_results(self, survey_id: str) -> Dict[str, Any]:
        """Get survey results"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/surveys/{survey_id}/results", timeout=self.timeout)
        return self._handle_response(resp)

    # Recognition
    def get_recognitions(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get recognitions"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/recognitions", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_recognition(self, recognition_data: Dict) -> Dict[str, Any]:
        """Create a recognition"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/recognitions", json=recognition_data, timeout=self.timeout)
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
        """Create a goal"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/goals", json=goal_data, timeout=self.timeout)
        return self._handle_response(resp)