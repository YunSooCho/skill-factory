"""ChatPlus Chat Platform API Client"""
import requests
from typing import Dict, List, Optional, Any

class ChatPlusClient:
    def __init__(self, api_key: str, base_url: str = "https://api.chatplus.io/v1", timeout: int = 30):
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

    def get_messages(self, chat_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', f'/chats/{chat_id}/messages', params={'limit': limit})
        return result.get('messages', [])

    def send_message(self, chat_id: str, message: str) -> Dict[str, Any]:
        return self._request('POST', f'/chats/{chat_id}/messages', data={'text': message})

    def get_chats(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/chats', params={'limit': limit})
        return result.get('chats', [])

    def get_user(self, user_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/users/{user_id}')

    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/users', data=data)

    def get_agents(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/agents')
        return result.get('agents', [])

    def get_statistics(self, start_date: str, end_date: str) -> Dict[str, Any]:
        return self._request('GET', '/statistics', params={'start_date': start_date, 'end_date': end_date})