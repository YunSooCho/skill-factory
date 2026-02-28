"""LiveAgent Help Desk API Client"""
import requests
from typing import Dict, List, Optional, Any

class LiveagentClient:
    def __init__(self, api_key: str, base_url: str, timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'Accept': 'application/json'})

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_tickets(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/tickets', params={'limit': limit})
        return result.get('response', [])

    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        result = self._request('GET', f'/tickets/{ticket_id}')
        return result.get('response', {})

    def create_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self._request('POST', '/tickets', data=data)
        return result.get('response', {})

    def update_ticket(self, ticket_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self._request('PUT', f'/tickets/{ticket_id}', data=data)
        return result.get('response', {})

    def add_message(self, ticket_id: str, message: str) -> Dict[str, Any]:
        result = self._request('POST', f'/tickets/{ticket_id}/messages', data={'message': message})
        return result.get('response', {})

    def get_customers(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/customers', params={'limit': limit})
        return result.get('response', [])

    def get_agents(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/agents')
        return result.get('response', [])