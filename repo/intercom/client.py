"""Intercom Customer Messaging API Client"""
import requests
from typing import Dict, List, Optional, Any

class IntercomClient:
    def __init__(self, access_token: str, timeout: int = 30):
        self.access_token = access_token
        self.base_url = "https://api.intercom.io"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_messages(self, conversation_id: str) -> List[Dict[str, Any]]:
        return self._request('GET', f'/conversations/{conversation_id}').get('messages', [])

    def send_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/messages', data=data)

    def get_conversations(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self._request('GET', '/conversations', params={'per_page': limit}).get('conversations', [])

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/contacts/{contact_id}')

    def create_contact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/contacts', data=data)

    def get_leads(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self._request('GET', '/contacts', params={'type': 'lead', 'per_page': limit}).get('contacts', [])

    def get_teams(self) -> List[Dict[str, Any]]:
        return self._request('GET', '/teams').get('teams', [])

    def get_admins(self) -> List[Dict[str, Any]]:
        return self._request('GET', '/admins').get('admins', [])