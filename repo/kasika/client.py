"""Kasika Customer Support API Client"""
import requests
from typing import Dict, List, Optional, Any

class KasikaClient:
    def __init__(self, api_key: str, base_url: str = "https://api.kasika.com/v1", timeout: int = 30):
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

    def get_tickets(self, status: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        params = {'limit': limit}
        if status:
            params['status'] = status
        result = self._request('GET', '/tickets', params=params)
        return result.get('tickets', [])

    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/tickets/{ticket_id}')

    def create_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/tickets', data=data)

    def update_ticket(self, ticket_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('PUT', f'/tickets/{ticket_id}', data=data)

    def add_comment(self, ticket_id: str, comment: str) -> Dict[str, Any]:
        return self._request('POST', f'/tickets/{ticket_id}/comments', data={'text': comment})

    def get_customers(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/customers', params={'limit': limit})
        return result.get('customers', [])

    def get_agents(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/agents')
        return result.get('agents', [])