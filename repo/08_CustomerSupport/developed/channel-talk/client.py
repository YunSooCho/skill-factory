"""
Channel Talk Customer Messaging API Client

This module provides a Python client for interacting with the Channel Talk
customer messaging platform API.
"""

import requests
from typing import Dict, List, Optional, Any


class ChannelTalkClient:
    """
    Client for Channel Talk Customer Messaging Platform API.

    Channel Talk provides:
    - Live chat
    - Messaging
    - Team inbox
    - Chatbot automation
    - Customer profiles
    - Analytics
    """

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        base_url: str = "https://api.channel.io",
        timeout: int = 30
    ):
        """Initialize the Channel Talk client."""
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {secret_key}',
            'X-Api-Key': api_key,
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_messages(self, chat_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get messages from a chat."""
        result = self._request('GET', f'/v3/chats/{chat_id}/messages', params={'limit': limit})
        return result.get('messages', [])

    def send_message(self, chat_id: str, message: str, sender_id: str) -> Dict[str, Any]:
        """Send a message to a chat."""
        return self._request('POST', f'/v3/chats/{chat_id}/messages', data={
            'text': message,
            'senderId': sender_id
        })

    def get_chats(
        self,
        state: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """List chats."""
        params = {'limit': limit, 'offset': offset}
        if state:
            params['state'] = state
        result = self._request('GET', '/v3/chats', params=params)
        return result.get('chats', [])

    def get_chat(self, chat_id: str) -> Dict[str, Any]:
        """Get chat details."""
        return self._request('GET', f'/v3/chats/{chat_id}')

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user details."""
        return self._request('GET', f'/v3/users/{user_id}')

    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user."""
        return self._request('POST', '/v3/users', data=data)

    def update_user(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user information."""
        return self._request('PUT', f'/v3/users/{user_id}', data=data)

    def get_user_tags(self, user_id: str) -> List[str]:
        """Get user tags."""
        result = self._request('GET', f'/v3/users/{user_id}/tags')
        return result.get('tags', [])

    def add_user_tags(self, user_id: str, tags: List[str]) -> Dict[str, Any]:
        """Add tags to user."""
        return self._request('POST', f'/v3/users/{user_id}/tags', data={'tags': tags})

    def remove_user_tags(self, user_id: str, tags: List[str]) -> Dict[str, Any]:
        """Remove tags from user."""
        return self._request('DELETE', f'/v3/users/{user_id}/tags', data={'tags': tags})

    def get_teams(self) -> List[Dict[str, Any]]:
        """Get list of teams."""
        result = self._request('GET', '/v3/teams')
        return result.get('teams', [])

    def get_managers(self, team_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of managers."""
        params = {}
        if team_id:
            params['teamId'] = team_id
        result = self._request('GET', '/v3/managers', params=params)
        return result.get('managers', [])

    def get_manager(self, manager_id: str) -> Dict[str, Any]:
        """Get manager details."""
        return self._request('GET', f'/v3/managers/{manager_id}')

    def get_campaigns(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get marketing campaigns."""
        result = self._request('GET', '/v3/campaigns', params={'limit': limit})
        return result.get('campaigns', [])

    def get_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign details."""
        return self._request('GET', f'/v3/campaigns/{campaign_id}/statistics')

    def send_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Send a campaign."""
        return self._request('POST', f'/v3/campaigns/{campaign_id}/send')

    def get_plugin_configs(self) -> List[Dict[str, Any]]:
        """Get plugin configurations."""
        result = self._request('GET', '/v3/plugins')
        return result.get('plugins', [])

    def get_statistics(
        self,
        start_date: str,
        end_date: str,
        by: str = "day"
    ) -> Dict[str, Any]:
        """Get channel statistics."""
        return self._request('GET', '/v3/channels/statistics', params={
            'since': start_date,
            'until': end_date,
            'by': by
        })

    def search_messages(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search messages."""
        result = self._request('GET', '/v3/messages/search', params={'query': query, 'limit': limit})
        return result.get('messages', [])