import requests
from typing import Dict, List, Optional


class GrooveClient:
    """Client for Groove API - Customer Support Platform"""

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.groovehq.com"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def update_ticket_state(self, ticket_id: str, state: str) -> Dict:
        return self._request('PUT', f'/v1/tickets/{ticket_id}/state', json={'state': state})

    def get_customer(self, customer_id: str) -> Dict:
        return self._request('GET', f'/v1/customers/{customer_id}')

    def create_ticket(self, ticket_data: Dict) -> Dict:
        return self._request('POST', '/v1/tickets', json=ticket_data)

    def search_ticket(self, q: str) -> List[Dict]:
        result = self._request('GET', '/v1/tickets', params={'q': q})
        return result.get('tickets', [])

    def create_message(self, ticket_id: str, message_data: Dict) -> Dict:
        return self._request('POST', f'/v1/tickets/{ticket_id}/messages', json=message_data)

    def get_ticket(self, ticket_id: str) -> Dict:
        return self._request('GET', f'/v1/tickets/{ticket_id}')