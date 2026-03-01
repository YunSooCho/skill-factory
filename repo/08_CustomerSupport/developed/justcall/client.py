"""JustCall Cloud Phone System API Client"""
import requests
from typing import Dict, List, Optional, Any

class JustcallClient:
    def __init__(self, api_key: str, api_secret: str, timeout: int = 30):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.justcall.io"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = (self.api_key, self.api_secret)
        self.session.headers.update({'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_call_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/v1/calls', params={'limit': limit})
        return result.get('data', [])

    def get_call(self, call_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/v1/calls/{call_id}')

    def make_call(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/v1/calls/make', data=data)

    def send_sms(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/v1/texts/send', data=data)

    def get_sms_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/v1/texts', params={'limit': limit})
        return result.get('data', [])

    def get_contacts(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/v1/contacts', params={'limit': limit})
        return result.get('data', [])

    def create_contact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/v1/contacts', data=data)

    def get_numbers(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/v1/numbers')
        return result.get('data', [])