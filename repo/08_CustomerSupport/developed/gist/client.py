"""Gist Communication Platform API Client"""
import requests
from typing import Dict, List, Optional, Any

class GistClient:
    def __init__(self, api_key: str, base_url: str = "https://api.gist.com/v1", timeout: int = 30):
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

    def get_messages(self, conversation_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', f'/conversations/{conversation_id}/messages', params={'limit': limit})
        return result.get('messages', [])

    def send_message(self, conversation_id: str, message: str) -> Dict[str, Any]:
        return self._request('POST', f'/conversations/{conversation_id}/messages', data={'text': message})

    def get_conversations(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/conversations', params={'limit': limit})
        return result.get('conversations', [])

    def get_user(self, user_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/users/{user_id}')

    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/users', data=data)

    def get_teams(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/teams')
        return result.get('teams', [])