import requests
from typing import Dict, List, Optional


class LiveagentClient:
    """Client for LiveAgent API - Help Desk & Live Chat Platform"""

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def delete_contact(self, contact_id: str) -> Dict:
        return self._request('DELETE', f'/contacts/{contact_id}')

    def list_tickets(self, **params) -> List[Dict]:
        result = self._request('GET', '/tickets', params=params)
        return result.get('tickets', []) if isinstance(result, dict) else []

    def create_contact_group(self, name: str, **kwargs) -> Dict:
        data = {'name': name, **kwargs}
        return self._request('POST', '/contact_groups', json=data)

    def delete_contact_group(self, group_id: str) -> Dict:
        return self._request('DELETE', f'/contact_groups/{group_id}')

    def create_contact(self, contact_data: Dict) -> Dict:
        return self._request('POST', '/contacts', json=contact_data)

    def update_contact_group(self, group_id: str, data: Dict) -> Dict:
        return self._request('PUT', f'/contact_groups/{group_id}', json=data)

    def list_contacts(self, **params) -> List[Dict]:
        result = self._request('GET', '/contacts', params=params)
        return result.get('contacts', []) if isinstance(result, dict) else []

    def update_contact(self, contact_id: str, data: Dict) -> Dict:
        return self._request('PUT', f'/contacts/{contact_id}', json=data)

    def delete_ticket(self, ticket_id: str) -> Dict:
        return self._request('DELETE', f'/tickets/{ticket_id}')

    def get_ticket(self, ticket_id: str) -> Dict:
        return self._request('GET', f'/tickets/{ticket_id}')

    def list_contact_groups(self) -> List[Dict]:
        result = self._request('GET', '/contact_groups')
        return result.get('contact_groups', []) if isinstance(result, dict) else []

    def get_contact_group(self, group_id: str) -> Dict:
        return self._request('GET', f'/contact_groups/{group_id}')

    def get_contact(self, contact_id: str) -> Dict:
        return self._request('GET', f'/contacts/{contact_id}')