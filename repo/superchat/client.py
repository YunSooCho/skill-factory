import requests
from typing import Dict, List, Optional


class SuperchatClient:
    """Client for Superchat API - Multi-Channel Messaging Platform"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.superchat.de"
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

    def delete_contact(self, contact_id: str) -> Dict:
        return self._request('DELETE', f'/v1/contacts/{contact_id}')

    def search_contact(self, query: str) -> Dict:
        return self._request('GET', '/v1/contacts/search', params={'query': query})

    def update_note(self, note_id: str, content: str) -> Dict:
        return self._request('PUT', f'/v1/notes/{note_id}', json={'content': content})

    def delete_note(self, note_id: str) -> Dict:
        return self._request('DELETE', f'/v1/notes/{note_id}')

    def send_message(self, message_data: Dict) -> Dict:
        return self._request('POST', '/v1/messages', json=message_data)

    def get_note(self, note_id: str) -> Dict:
        return self._request('GET', f'/v1/notes/{note_id}')

    def create_contact(self, contact_data: Dict) -> Dict:
        return self._request('POST', '/v1/contacts', json=contact_data)

    def update_contact(self, contact_id: str, data: Dict) -> Dict:
        return self._request('PUT', f'/v1/contacts/{contact_id}', json=data)

    def send_email(self, email_data: Dict) -> Dict:
        return self._request('POST', '/v1/emails', json=email_data)

    def get_contact(self, contact_id: str) -> Dict:
        return self._request('GET', f'/v1/contacts/{contact_id}')

    def upload_file(self, file_data: Dict) -> Dict:
        return self._request('POST', '/v1/files', json=file_data)

    def create_note(self, note_data: Dict) -> Dict:
        return self._request('POST', '/v1/notes', json=note_data)