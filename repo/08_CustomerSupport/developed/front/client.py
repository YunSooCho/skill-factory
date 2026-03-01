"""Front Shared Inbox API Client"""
import requests
from typing import Dict, List, Optional, Any

class FrontClient:
    def __init__(self, api_token: str, timeout: int = 30):
        self.api_token = api_token
        self.base_url = "https://api2.frontapp.com/v1"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {api_token}', 'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_conversations(self, status: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        params = {'limit': limit}
        if status:
            params['statuses'] = [status]
        result = self._request('GET', '/conversations', params=params)
        return result.get('_results', [])

    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/conversations/{conversation_id}')

    def send_message(self, conversation_id: str, message: str) -> Dict[str, Any]:
        return self._request('POST', f'/conversations/{conversation_id}/messages', data={
            'body': message,
            'options': {'archive': False}
        })

    def add_comment(self, conversation_id: str, comment: str) -> Dict[str, Any]:
        return self._request('POST', f'/conversations/{conversation_id}/comments', data={
            'body': comment
        })

    def get_inboxes(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/inboxes')
        return result.get('_results', [])

    def get_teams(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/teams')
        return result.get('_results', [])

    def get_teammates(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/teammates')
        return result.get('_results', [])

    def get_channels(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/channels')
        return result.get('_results', [])