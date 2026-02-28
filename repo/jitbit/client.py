import requests
from typing import Dict, List, Optional


class JitbitClient:
    """Client for Jitbit API - Help Desk Platform"""

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

    def list_tickets(self, **params) -> List[Dict]:
        result = self._request('GET', '/tickets', params=params)
        return result if isinstance(result, list) else []

    def list_users(self) -> List[Dict]:
        result = self._request('GET', '/users')
        return result if isinstance(result, list) else []

    def attach_file_to_ticket(self, ticket_id: str, file_data: Dict) -> Dict:
        return self._request('POST', f'/tickets/{ticket_id}/attachments', json=file_data)

    def create_user(self, user_data: Dict) -> Dict:
        return self._request('POST', '/users', json=user_data)

    def create_ticket(self, ticket_data: Dict) -> Dict:
        return self._request('POST', '/tickets', json=ticket_data)

    def get_ticket(self, ticket_id: str) -> Dict:
        return self._request('GET', f'/tickets/{ticket_id}')

    def create_kb_article(self, article_data: Dict) -> Dict:
        return self._request('POST', '/knowledgebase', json=article_data)

    def search_tickets(self, query: str) -> List[Dict]:
        result = self._request('GET', '/tickets/search', params={'query': query})
        return result if isinstance(result, list) else []