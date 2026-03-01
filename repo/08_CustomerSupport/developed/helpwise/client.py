"""Helpwise Shared Inbox API Client"""
import requests
from typing import Dict, List, Optional, Any

class HelpwiseClient:
    def __init__(self, api_key: str, base_url: str = "https://app.helpwise.io/api", timeout: int = 30):
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

    def get_inboxes(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/inboxes')
        return result.get('inboxes', [])

    def get_conversations(self, inbox_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', f'/inboxes/{inbox_id}/conversations', params={'limit': limit})
        return result.get('conversations', [])

    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/conversations/{conversation_id}')

    def send_reply(self, conversation_id: str, message: str) -> Dict[str, Any]:
        return self._request('POST', f'/conversations/{conversation_id}/reply', data={'message': message})

    def create_note(self, conversation_id: str, note: str) -> Dict[str, Any]:
        return self._request('POST', f'/conversations/{conversation_id}/notes', data={'note': note})

    def assign_conversation(self, conversation_id: str, assignee_id: str) -> Dict[str, Any]:
        return self._request('POST', f'/conversations/{conversation_id}/assign', data={'assignee_id': assignee_id})

    def get_labels(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/labels')
        return result.get('labels', [])

    def add_label(self, conversation_id: str, label_id: str) -> Dict[str, Any]:
        return self._request('POST', f'/conversations/{conversation_id}/labels', data={'label_id': label_id})

    def get_team_members(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/team')
        return result.get('team', [])