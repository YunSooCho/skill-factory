"""Freshchat Live Chat API Client"""
import requests
from typing import Dict, List, Optional, Any

class FreshchatClient:
    def __init__(self, api_key: str, base_url: str = "https://api.freshchat.com/v2", timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_conversations(self, status: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        params = {'per_page': limit}
        if status:
            params['status'] = status
        result = self._request('GET', '/conversations', params=params)
        return result.get('conversations', [])

    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/conversations/{conversation_id}')

    def send_message(self, conversation_id: str, message: str) -> Dict[str, Any]:
        return self._request('POST', f'/conversations/{conversation_id}/messages', data={
            'message_parts': [{'text': {'content': message}}]
        })

    def get_user(self, user_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/users/{user_id}')

    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/users', data=data)

    def get_groups(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/groups')
        return result.get('groups', [])

    def get_agents(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/agents')
        return result.get('agents', [])