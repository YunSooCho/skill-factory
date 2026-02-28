import requests
from typing import Dict, List, Optional


class RelationClient:
    """Client for Relation API - Japanese Customer Support Platform"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.relation.jp"
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def update_address_customer(self, customer_id: str, data: Dict) -> Dict:
        return self._request('PUT', f'/v1/address_book/{customer_id}', json=data)

    def register_address_customer(self, customer_data: Dict) -> Dict:
        return self._request('POST', '/v1/address_book', json=customer_data)

    def get_ticket_details(self, ticket_id: str) -> Dict:
        return self._request('GET', f'/v1/tickets/{ticket_id}')

    def create_ticket_from_memo(self, memo: str, **kwargs) -> Dict:
        data = {'memo': memo, **kwargs}
        return self._request('POST', '/v1/tickets', json=data)

    def search_address_customers(self, query: str) -> List[Dict]:
        result = self._request('GET', '/v1/address_book/search', params={'q': query})
        return result.get('customers', [])

    def update_ticket_status(self, ticket_id: str, status: str) -> Dict:
        return self._request('PUT', f'/v1/tickets/{ticket_id}/status', json={'status': status})

    def add_memo_to_ticket(self, ticket_id: str, memo: str) -> Dict:
        return self._request('POST', f'/v1/tickets/{ticket_id}/memos', json={'memo': memo})

    def delete_address_customer(self, customer_id: str) -> Dict:
        return self._request('DELETE', f'/v1/address_book/{customer_id}')

    def list_tickets_by_status(self, status: str) -> List[Dict]:
        result = self._request('GET', '/v1/tickets', params={'status': status})
        return result.get('tickets', [])