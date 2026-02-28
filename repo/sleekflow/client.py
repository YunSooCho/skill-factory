import requests
from typing import Dict, List, Optional


class SleekflowClient:
    """Client for Sleekflow API - Messaging Platform for Business"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sleekflow.io"
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

    def search_contacts(self, query: str) -> List[Dict]:
        result = self._request('GET', '/v1/contacts/search', params={'query': query})
        return result.get('contacts', []) if isinstance(result, dict) else []

    def add_or_update_contact(self, contact_data: Dict) -> Dict:
        return self._request('POST', '/v1/contacts', json=contact_data)

    def send_message_via_channel(self, channel_id: str, message_data: Dict) -> Dict:
        return self._request('POST', f'/v1/channels/{channel_id}/messages', json=message_data)

    def create_staff(self, staff_data: Dict) -> Dict:
        return self._request('POST', '/v1/staff', json=staff_data)

    def get_conversation_analysis_data(self, conversation_id: str) -> Dict:
        return self._request('GET', f'/v1/conversations/{conversation_id}/analytics')