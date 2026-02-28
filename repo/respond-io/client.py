import requests
from typing import Dict, List, Optional


class RespondIoClient:
    """Client for Respond.io API - Customer Messaging Platform"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.respond.io"
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

    def send_message(self, message_data: Dict) -> Dict:
        return self._request('POST', '/v1/message', json=message_data)

    def create_comment(self, conversation_id: str, message: str) -> Dict:
        return self._request('POST', f'/v1/conversations/{conversation_id}/comments', json={'message': message})

    def open_close_conversation(self, conversation_id: str, closed: bool) -> Dict:
        return self._request('POST', f'/v1/conversations/{conversation_id}/status', json={'closed': closed})

    def create_contact(self, contact_data: Dict) -> Dict:
        return self._request('POST', '/v1/contact', json=contact_data)

    def delete_tag_from_contact(self, contact_id: str, tag: str) -> Dict:
        return self._request('DELETE', f'/v1/contacts/{contact_id}/tags/{tag}')

    def assign_conversation(self, conversation_id: str, user_id: str) -> Dict:
        return self._request('POST', f'/v1/conversations/{conversation_id}/assign', json={'user_id': user_id})

    def create_update_contact(self, contact_data: Dict) -> Dict:
        return self._request('POST', '/v1/contact/create_or_update', json=contact_data)

    def update_contact(self, contact_id: str, data: Dict) -> Dict:
        return self._request('POST', f'/v1/contacts/{contact_id}', json=data)

    def search_contacts(self, query: str) -> List[Dict]:
        result = self._request('GET', '/v1/contacts/search', params={'query': query})
        return result.get('results', []) if isinstance(result, dict) else []

    def get_contact(self, contact_id: str) -> Dict:
        return self._request('GET', f'/v1/contacts/{contact_id}')

    def delete_contact(self, contact_id: str) -> Dict:
        return self._request('DELETE', f'/v1/contacts/{contact_id}')

    def add_tag_to_contact(self, contact_id: str, tag: str) -> Dict:
        return self._request('POST', f'/v1/contacts/{contact_id}/tags', json={'tag': tag})