"""Help Scout Customer Support API Client"""
import requests
from typing import Dict, List, Optional, Any

class HelpScoutClient:
    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.base_url = "https://api.helpscout.net/v2"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = (self.api_key, 'X')
        self.session.headers.update({'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json() if response.text else {}

    def get_conversations(self, status: Optional[str] = None, page: int = 1) -> List[Dict[str, Any]]:
        params = {'page': page}
        if status:
            params['status'] = status
        return self._request('GET', '/conversations', params=params).get('_embedded', {}).get('conversations', [])

    def get_conversation(self, conversation_id: int) -> Dict[str, Any]:
        return self._request('GET', f'/conversations/{conversation_id}')

    def create_conversation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/conversations', data=data)

    def get_mailboxes(self) -> List[Dict[str, Any]]:
        return self._request('GET', '/mailboxes').get('_embedded', {}).get('mailboxes', [])

    def get_customers(self, page: int = 1) -> List[Dict[str, Any]]:
        return self._request('GET', '/customers', params={'page': page}).get('_embedded', {}).get('customers', [])

    def get_customer(self, customer_id: int) -> Dict[str, Any]:
        return self._request('GET', f'/customers/{customer_id}')

    def create_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/customers', data=data)

    def get_threads(self, conversation_id: int) -> List[Dict[str, Any]]:
        return self._request('GET', f'/conversations/{conversation_id}/threads').get('_embedded', {}).get('threads', [])