import requests
from typing import Dict, List, Optional, Any


class ChatbotClient:
    """
    Client for Chatbot API - Conversational AI Platform
    """

    def __init__(self, api_key: str, base_url: str = "https://api.chatbot.com"):
        """
        Initialize Chatbot client

        Args:
            api_key: Chatbot API key
            base_url: Base URL for Chatbot API
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Internal method to make API requests

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional arguments

        Returns:
            Response data
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def delete_entity(self, entity_id: str) -> Dict:
        """Delete an entity"""
        return self._request('DELETE', f'/v1/entities/{entity_id}')

    def create_user(self, user_data: Dict) -> Dict:
        """Create a new user"""
        return self._request('POST', '/v1/users', json=user_data)

    def update_segment(self, segment_id: str, data: Dict) -> Dict:
        """Update a segment"""
        return self._request('PUT', f'/v1/segments/{segment_id}', json=data)

    def search_conversations(self, query: str, limit: int = 50) -> List[Dict]:
        """Search conversations"""
        result = self._request('GET', '/v1/conversations/search', params={'q': query, 'limit': limit})
        return result.get('conversations', [])

    def delete_segment(self, segment_id: str) -> Dict:
        """Delete a segment"""
        return self._request('DELETE', f'/v1/segments/{segment_id}')

    def list_entities(self, limit: int = 50) -> List[Dict]:
        """List all entities"""
        result = self._request('GET', '/v1/entities', params={'limit': limit})
        return result.get('entities', [])

    def get_entity(self, entity_id: str) -> Dict:
        """Get a specific entity"""
        return self._request('GET', f'/v1/entities/{entity_id}')

    def list_users(self, limit: int = 50) -> List[Dict]:
        """List all users"""
        result = self._request('GET', '/v1/users', params={'limit': limit})
        return result.get('users', [])

    def delete_user(self, user_id: str) -> Dict:
        """Delete a user"""
        return self._request('DELETE', f'/v1/users/{user_id}')

    def get_user(self, user_id: str) -> Dict:
        """Get a specific user"""
        return self._request('GET', f'/v1/users/{user_id}')

    def update_entity(self, entity_id: str, data: Dict) -> Dict:
        """Update an entity"""
        return self._request('PUT', f'/v1/entities/{entity_id}', json=data)

    def update_user(self, user_id: str, data: Dict) -> Dict:
        """Update a user"""
        return self._request('PUT', f'/v1/users/{user_id}', json=data)

    def add_users_to_segment(self, segment_id: str, user_ids: List[str]) -> Dict:
        """Add users to a segment"""
        return self._request('POST', f'/v1/segments/{segment_id}/users', json={'userIds': user_ids})

    def create_segment(self, name: str, conditions: List[Dict]) -> Dict:
        """Create a new segment"""
        return self._request('POST', '/v1/segments', json={'name': name, 'conditions': conditions})

    def list_segments(self, limit: int = 50) -> List[Dict]:
        """List all segments"""
        result = self._request('GET', '/v1/segments', params={'limit': limit})
        return result.get('segments', [])