"""Heartbeat Employee Feedback API Client"""
import requests
from typing import Dict, List, Optional, Any

class HeartbeatClient:
    def __init__(self, api_key: str, base_url: str = "https://api.heartbeat.com/v1", timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def create_survey(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/surveys', data=data)

    def get_surveys(self, status: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        params = {'limit': limit}
        if status:
            params['status'] = status
        result = self._request('GET', '/surveys', params=params)
        return result.get('surveys', [])

    def get_survey(self, survey_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/surveys/{survey_id}')

    def get_responses(self, survey_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', f'/surveys/{survey_id}/responses', params={'limit': limit})
        return result.get('responses', [])

    def create_response(self, survey_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', f'/surveys/{survey_id}/responses', data=data)

    def get_employees(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/employees', params={'limit': limit})
        return result.get('employees', [])

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/employees/{employee_id}')

    def get_pulse(self, start_date: str, end_date: str) -> Dict[str, Any]:
        return self._request('GET', '/pulse', params={'start_date': start_date, 'end_date': end_date})