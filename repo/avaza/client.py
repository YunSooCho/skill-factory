"""
Avaza API Client - Business Management
"""

import requests
import time
from typing import Optional, Dict, Any, List


class AvazaError(Exception):
    """Base exception for Avaza errors"""
    pass


class AvazaRateLimitError(AvazaError):
    """Rate limit exceeded"""
    pass


class AvazaAuthenticationError(AvazaError):
    """Authentication failed"""
    pass


class AvazaClient:
    """Client for Avaza Business Management API"""

    BASE_URL = "https://api.avaza.com/api"

    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        self.min_delay = 0.1
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        current_time = time.time()
        if (current_time - self.last_request_time) < self.min_delay:
            time.sleep(self.min_delay - (current_time - self.last_request_time))
        self.last_request_time = time.time()

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        if response.status_code == 429:
            raise AvazaRateLimitError("Rate limit exceeded")
        if response.status_code == 401:
            raise AvazaAuthenticationError("Authentication failed")
        if response.status_code >= 400:
            raise AvazaError(f"API error ({response.status_code}): {response.text}")
        return response.json()

    def get_projects(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            response = self.session.get(f"{self.BASE_URL}/Project", timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AvazaError(f"Request failed: {str(e)}")

    def get_project(self, project_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            response = self.session.get(f"{self.BASE_URL}/Project/{project_id}", timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AvazaError(f"Request failed: {str(e)}")

    def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            response = self.session.post(f"{self.BASE_URL}/Project", json=project_data, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AvazaError(f"Request failed: {str(e)}")

    def update_project(self, project_id: str, project_data: Dict[str, Any]) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            response = self.session.put(f"{self.BASE_URL}/Project/{project_id}", json=project_data, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AvazaError(f"Request failed: {str(e)}")

    def get_tasks(self, project_id: Optional[str] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        params = {}
        if project_id:
            params['ProjectId'] = project_id
        try:
            response = self.session.get(f"{self.BASE_URL}/Task", params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AvazaError(f"Request failed: {str(e)}")

    def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            response = self.session.post(f"{self.BASE_URL}/Task", json=task_data, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AvazaError(f"Request failed: {str(e)}")

    def get_time_entries(self, start_date: str, end_date: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            response = self.session.get(f"{self.BASE_URL}/TimeEntry", params={
                'StartDate': start_date, 'EndDate': end_date
            }, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AvazaError(f"Request failed: {str(e)}")

    def create_time_entry(self, time_entry_data: Dict[str, Any]) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            response = self.session.post(f"{self.BASE_URL}/TimeEntry", json=time_entry_data, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AvazaError(f"Request failed: {str(e)}")

    def get_users(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            response = self.session.get(f"{self.BASE_URL}/User", timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AvazaError(f"Request failed: {str(e)}")

    def get_clients(self) -> Dict[str, Any]:
        self._enforce_rate_limit()
        try:
            response = self.session.get(f"{self.BASE_URL}/Client", timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AvazaError(f"Request failed: {str(e)}")