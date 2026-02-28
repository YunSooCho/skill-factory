import requests
from typing import Dict, List, Optional


class FreshchatClient:
    """
    Client for Freshchat API - Customer Messaging Platform
    """

    def __init__(self, api_key: str, app_id: str, base_url: str = "https://api.freshchat.com"):
        """
        Initialize Freshchat client

        Args:
            api_key: Freshchat API key
            app_id: Freshchat Application ID
            base_url: Base URL for Freshchat API
        """
        self.api_key = api_key
        self.app_id = app_id
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Internal method to make API requests"""
        url = f"{self.base_url}/v2/{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def create_user(self, user_data: Dict) -> Dict:
        """Create a new user"""
        return self._request('POST', 'users', json=user_data)

    def get_report(self, report_id: str) -> Dict:
        """Get a report"""
        return self._request('GET', f'reports/{report_id}')

    def send_message_to_conversation(self, conversation_id: str, message: Dict) -> Dict:
        """Send a message to a conversation"""
        return self._request('POST', f'conversations/{conversation_id}/messages', json=message)

    def download_report_file(self, report_id: str) -> bytes:
        """Download a report file"""
        url = f"{self.base_url}/v2/reports/{report_id}/download"
        response = self.session.get(url)
        response.raise_for_status()
        return response.content

    def list_conversation_messages(self, conversation_id: str, limit: int = 50) -> List[Dict]:
        """List messages in a conversation"""
        result = self._request('GET', f'conversations/{conversation_id}/messages', params={'limit': limit})
        return result.get('messages', [])

    def search_user(self, query: str) -> List[Dict]:
        """Search users"""
        result = self._request('GET', 'users/search', params={'q': query})
        return result.get('users', [])

    def generate_raw_data_report(self, report_config: Dict) -> Dict:
        """Generate a raw data report"""
        return self._request('POST', 'reports/generate', json=report_config)

    def list_agents(self) -> List[Dict]:
        """List all agents"""
        result = self._request('GET', 'agents')
        return result.get('agents', [])

    def create_conversation(self, conversation_data: Dict) -> Dict:
        """Create a new conversation"""
        return self._request('POST', 'conversations', json=conversation_data)

    def update_user(self, user_id: str, data: Dict) -> Dict:
        """Update a user"""
        return self._request('PUT', f'users/{user_id}', json=data)