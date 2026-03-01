"""Missive Team Inbox API Client"""
import requests
from typing import Dict, List, Optional, Any

class MissiveClient:
    def __init__(self, api_token: str, timeout: int = 30):
        self.api_token = api_token
        self.base_url = "https://api.missiveapp.com/v1"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {api_token}', 'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_conversations(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/conversations', params={'limit': limit})
        return result.get('data', [])

    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/conversations/{conversation_id}')

    def send_message(self, conversation_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', f'/conversations/{conversation_id}/messages', data=data)

    def get_tasks(self, conversation_id: str) -> List[Dict[str, Any]]:
        result = self._request('GET', f'/conversations/{conversation_id}/tasks')
        return result.get('data', [])

    def create_task(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/tasks', data=data)

    def get_teams(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/teams')
        return result.get('data', [])

    def get_users(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/users')
        return result.get('data', [])