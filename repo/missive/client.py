import requests
from typing import Dict, List, Optional


class MissiveClient:
    """Client for Missive API - Team Email & Chat Platform"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.missiveapp.com"
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

    def create_draft_message(self, **message_data) -> Dict:
        return self._request('POST', '/v1/drafts', json=message_data)

    def create_contacts(self, contacts: List[Dict]) -> Dict:
        return self._request('POST', '/v1/contacts', json={'contacts': contacts})

    def send_message(self, **message_data) -> Dict:
        return self._request('POST', '/v1/messages', json=message_data)

    def get_conversation_messages(self, conversation_id: str) -> List[Dict]:
        result = self._request('GET', f'/v1/conversations/{conversation_id}/messages')
        return result.get('messages', []) if isinstance(result, dict) else []

    def search_contacts(self, query: str) -> List[Dict]:
        result = self._request('GET', '/v1/contacts/search', params={'q': query})
        return result.get('contacts', []) if isinstance(result, dict) else []

    def update_contacts(self, contact_id: str, data: Dict) -> Dict:
        return self._request('PUT', f'/v1/contacts/{contact_id}', json=data)

    def get_conversation_details(self, conversation_id: str) -> Dict:
        return self._request('GET', f'/v1/conversations/{conversation_id}')

    def get_contact_details(self, contact_id: str) -> Dict:
        return self._request('GET', f'/v1/contacts/{contact_id}')

    def get_conversation_list(self, **params) -> List[Dict]:
        result = self._request('GET', '/v1/conversations', params=params)
        return result.get('conversations', []) if isinstance(result, dict) else []

    def create_draft_message_with_attachment(self, content: str, attachment_url: str, **kwargs) -> Dict:
        return self._request('POST', '/v1/drafts', json={
            'content': content,
            'attachment_url': attachment_url,
            **kwargs
        })