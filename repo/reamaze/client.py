import requests
from typing import Dict, List, Optional


class ReamazeClient:
    """Client for Reamaze API - Customer Support Platform"""

    def __init__(self, brand_slug: str, login: str, api_token: str):
        self.brand_slug = brand_slug
        self.login = login
        self.api_token = api_token
        self.base_url = f"https://{brand_slug}.reamaze.io"
        self.session = requests.Session()
        self.session.auth = (login, api_token)
        self.session.headers.update({'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def create_conversation(self, conversation_data: Dict) -> Dict:
        return self._request('POST', '/api/v1/conversations', json=conversation_data)

    def create_contact(self, contact_data: Dict) -> Dict:
        return self._request('POST', '/api/v1/contacts', json=contact_data)

    def search_conversations(self, query: str, **params) -> List[Dict]:
        all_params = {'q': query, **params}
        result = self._request('GET', '/api/v1/conversations/search', params=all_params)
        return result if isinstance(result, list) else []

    def update_contact(self, contact_id: str, data: Dict) -> Dict:
        return self._request('PUT', f'/api/v1/contacts/{contact_id}', json=data)

    def create_message(self, conversation_id: str, message_data: Dict) -> Dict:
        return self._request('POST', f'/api/v1/conversations/{conversation_id}/messages', json=message_data)

    def search_messages(self, query: str) -> List[Dict]:
        result = self._request('GET', '/api/v1/messages/search', params={'q': query})
        return result if isinstance(result, list) else []

    def search_contacts(self, query: str) -> List[Dict]:
        result = self._request('GET', '/api/v1/contacts/search', params={'q': query})
        return result if isinstance(result, list) else []