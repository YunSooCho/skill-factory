import requests
from typing import Dict, List, Optional


class HelpwiseClient:
    """Client for Helpwise API - Shared Inbox Platform"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://app.helpwise.io/api"
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def search_conversations(self, query: str) -> List[Dict]:
        result = self._request('GET', '/conversations/search', params={'q': query})
        return result.get('conversations', [])

    def create_contact(self, contact_data: Dict) -> Dict:
        return self._request('POST', '/contacts', json=contact_data)

    def get_overall_report(self) -> Dict:
        return self._request('GET', '/reports/overall')

    def update_contact(self, contact_id: str, data: Dict) -> Dict:
        return self._request('PUT', f'/contacts/{contact_id}', json=data)

    def search_contact(self, query: str) -> List[Dict]:
        result = self._request('GET', '/contacts/search', params={'q': query})
        return result.get('contacts', [])

    def get_conversation(self, conversation_id: str) -> Dict:
        return self._request('GET', f'/conversations/{conversation_id}')

    def remove_tags_conversations(self, conversation_ids: List[str], tag: str) -> Dict:
        return self._request('POST', '/conversations/remove_tags', json={
            'conversation_ids': conversation_ids,
            'tag': tag
        })

    def get_contact(self, contact_id: str) -> Dict:
        return self._request('GET', f'/contacts/{contact_id}')

    def apply_tags_conversations(self, conversation_ids: List[str], tag: str) -> Dict:
        return self._request('POST', '/conversations/apply_tags', json={
            'conversation_ids': conversation_ids,
            'tag': tag
        })