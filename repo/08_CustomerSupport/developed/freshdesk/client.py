"""Freshdesk Customer Support API Client"""
import requests
from typing import Dict, List, Optional, Any

class FreshdeskClient:
    def __init__(self, api_key: str, domain: str, timeout: int = 30):
        self.api_key = api_key
        self.domain = domain
        self.base_url = f"https://{domain}.freshdesk.com/api/v2"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = (self.api_key, 'X')
        self.session.headers.update({'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json() if response.text else {}

    def get_tickets(self, status: Optional[str] = None, page: int = 1) -> List[Dict[str, Any]]:
        params = {'page': page}
        if status:
            params['status'] = status
        return self._request('GET', '/tickets', params=params)

    def get_ticket(self, ticket_id: int) -> Dict[str, Any]:
        return self._request('GET', f'/tickets/{ticket_id}')

    def create_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/tickets', data=data)

    def update_ticket(self, ticket_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('PUT', f'/tickets/{ticket_id}', data=data)

    def delete_ticket(self, ticket_id: int) -> Dict[str, Any]:
        url = f"{self.base_url}/tickets/{ticket_id}"
        response = self.session.delete(url, timeout=self.timeout)
        response.raise_for_status()
        return {}

    def get_contacts(self, page: int = 1) -> List[Dict[str, Any]]:
        return self._request('GET', '/contacts', params={'page': page})

    def get_contact(self, contact_id: int) -> Dict[str, Any]:
        return self._request('GET', f'/contacts/{contact_id}')

    def create_contact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/contacts', data=data)

    def get_companies(self, page: int = 1) -> List[Dict[str, Any]]:
        return self._request('GET', '/companies', params={'page': page})

    def get_agents(self) -> List[Dict[str, Any]]:
        return self._request('GET', '/agents')

    def get_groups(self) -> List[Dict[str, Any]]:
        return self._request('GET', '/groups')