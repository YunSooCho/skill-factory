"""CloudTalk Cloud Phone System API Client"""
import requests
from typing import Dict, List, Optional, Any

class CloudTalkClient:
    def __init__(self, api_key: str, api_id: str, base_url: str = "https://api.cloudtalk.io", timeout: int = 30):
        self.api_key = api_key
        self.api_id = api_id
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'{api_id}:{api_key}', 'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_calls(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/calls/index', params={'limit': limit})
        return result.get('response', {}).get('data', [])

    def get_call(self, call_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/calls/{call_id}')

    def make_call(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/calls/dial', data=data)

    def get_call_recording(self, call_id: str) -> str:
        result = self._request('GET', f'/calls/{call_id}/recording')
        return result.get('response', {}).get('url', '')

    def get_contacts(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/contacts', params={'limit': limit})
        return result.get('response', {}).get('data', [])

    def create_contact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/contacts', data=data)

    def get_agents(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/agents')
        return result.get('response', {}).get('data', [])

    def get_numbers(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/numbers/index')
        return result.get('response', {}).get('data', [])

    def get_statistics(self, start_date: str, end_date: str) -> Dict[str, Any]:
        return self._request('GET', '/statistics', params={'date_from': start_date, 'date_to': end_date})