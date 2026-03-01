"""Chatbot Platform API Client"""
import requests
from typing import Dict, List, Optional, Any

class ChatbotClient:
    def __init__(self, api_key: str, base_url: str = "https://api.chatbot.com/v1", timeout: int = 30):
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

    def send_message(self, bot_id: str, message: str, user_id: str) -> Dict[str, Any]:
        return self._request('POST', f'/bots/{bot_id}/messages', data={'message': message, 'user_id': user_id})

    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/conversations/{conversation_id}')

    def get_conversations(self, limit: int = 100) -> List[Dict[str, Any]]:
        result = self._request('GET', '/conversations', params={'limit': limit})
        return result.get('conversations', [])

    def get_bot(self, bot_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/bots/{bot_id}')

    def get_bots(self) -> List[Dict[str, Any]]:
        result = self._request('GET', '/bots')
        return result.get('bots', [])

    def get_intents(self, bot_id: str) -> List[Dict[str, Any]]:
        result = self._request('GET', f'/bots/{bot_id}/intents')
        return result.get('intents', [])

    def create_intent(self, bot_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', f'/bots/{bot_id}/intents', data=data)

    def train_bot(self, bot_id: str) -> Dict[str, Any]:
        return self._request('POST', f'/bots/{bot_id}/train')