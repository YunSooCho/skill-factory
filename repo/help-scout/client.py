import requests
from typing import Dict, List, Optional


class HelpScoutClient:
    """Client for Help Scout API - Customer Support Platform"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.helpscout.net/v2"
        self.session = requests.Session()
        self.session.auth = (api_key, 'X')
        self.session.headers.update({'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def search_conversations(self, query: str, **kwargs) -> Dict:
        params = {'query': query, **kwargs}
        return self._request('GET', '/conversations/search', params=params)

    def update_customer_properties(self, customer_id: str, properties: Dict) -> Dict:
        return self._request('PATCH', f'/customers/{customer_id}', json={'properties': properties})

    def get_user(self, user_id: str) -> Dict:
        return self._request('GET', f'/users/{user_id}')

    def search_customer(self, query: str) -> List[Dict]:
        result = self._request('GET', '/customers', params={'query': query})
        return result.get('_embedded', {}).get('customers', [])

    def create_reply(self, conversation_id: str, text: str) -> Dict:
        return self._request('POST', f'/conversations/{conversation_id}/replies', json={
            'text': text
        })

    def create_customer(self, customer_data: Dict) -> Dict:
        return self._request('POST', '/customers', json=customer_data)

    def get_tag_list(self) -> List[Dict]:
        result = self._request('GET', '/tags')
        return result.get('_embedded', {}).get('tags', [])

    def get_customer(self, customer_id: str) -> Dict:
        return self._request('GET', f'/customers/{customer_id}')

    def get_mailbox_list(self) -> List[Dict]:
        result = self._request('GET', '/mailboxes')
        return result.get('_embedded', {}).get('mailboxes', [])

    def get_company_report(self) -> Dict:
        return self._request('GET', '/reports/company')

    def update_conversation(self, conversation_id: str, data: Dict) -> Dict:
        return self._request('PATCH', f'/conversations/{conversation_id}', json=data)

    def get_customer_properties(self, customer_id: str) -> Dict:
        customer = self.get_customer(customer_id)
        return customer.get('properties', {})

    def add_conversation_note(self, conversation_id: str, text: str) -> Dict:
        return self._request('POST', f'/conversations/{conversation_id}/notes', json={'text': text})

    def create_conversation(self, conversation_data: Dict) -> Dict:
        return self._request('POST', '/conversations', json=conversation_data)

    def update_tags(self, conversation_id: str, tags: List[str]) -> Dict:
        return self._request('PUT', f'/conversations/{conversation_id}/tags', json={'tags': tags})