import requests
from typing import Dict, List, Optional


class FrontClient:
    """
    Client for Front API - Shared Inbox Platform
    """

    def __init__(self, api_token: str):
        """
        Initialize Front client

        Args:
            api_token: Front API token
        """
        self.api_token = api_token
        self.base_url = "https://api2.frontapp.com"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Internal method to make API requests"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def search_conversations(self, q: str, limit: int = 50) -> Dict:
        """Search conversations"""
        params = {'q': q, 'limit': limit}
        return self._request('GET', '/conversations/search', params=params)

    def create_contact(self, data: Dict) -> Dict:
        """Create a new contact"""
        return self._request('POST', '/contacts', json=data)

    def retrieve_message(self, message_id: str) -> Dict:
        """Retrieve a specific message"""
        return self._request('GET', f'/messages/{message_id}')

    def add_links_to_conversation(self, conversation_id: str, data: Dict) -> Dict:
        """Add external links to a conversation"""
        return self._request('POST', f'/conversations/{conversation_id}/links', json=data)

    def get_conversation_last_message(self, conversation_id: str) -> Dict:
        """Get the last message of a conversation"""
        return self._request('GET', f'/conversations/{conversation_id}/last_message')

    def add_tags_to_conversation(self, conversation_id: str, tag_ids: List[str]) -> Dict:
        """Add tags to a conversation"""
        return self._request('POST', f'/conversations/{conversation_id}/tags', json={'tag_ids': tag_ids})

    def send_reply(self, conversation_id: str, data: Dict) -> Dict:
        """Send a reply to a conversation"""
        return self._request('POST', f'/conversations/{conversation_id}/replies', json=data)

    def send_new_message(self, data: Dict) -> Dict:
        """Send a new message"""
        return self._request('POST', '/conversations', json=data)

    def retrieve_contact_by_email(self, email: str) -> Dict:
        """Retrieve contact information by email"""
        return self._request('GET', '/contacts/search', params={'q': email})

    def create_draft_reply(self, conversation_id: str, data: Dict) -> Dict:
        """Create a draft reply"""
        return self._request('POST', f'/conversations/{conversation_id}/drafts', json=data)

    def retrieve_contact(self, contact_id: str) -> Dict:
        """Retrieve contact information"""
        return self._request('GET', f'/contacts/{contact_id}')

    def delete_contact(self, contact_id: str) -> Dict:
        """Delete a contact"""
        return self._request('DELETE', f'/contacts/{contact_id}')

    def add_comment_to_conversation(self, conversation_id: str, body: str) -> Dict:
        """Add a comment to a conversation"""
        return self._request('POST', f'/conversations/{conversation_id}/comments', json={'body': body})

    def update_contact(self, contact_id: str, data: Dict) -> Dict:
        """Update a contact"""
        return self._request('PATCH', f'/contacts/{contact_id}', json=data)

    def create_discussion_conversation(self, data: Dict) -> Dict:
        """Create a discussion conversation"""
        return self._request('POST', '/conversations', json={**data, 'type': 'discussion'})

    def list_inboxes(self) -> Dict:
        """List all inboxes"""
        return self._request('GET', '/inboxes')

    def list_conversation_messages(self, conversation_id: str, limit: int = 50) -> Dict:
        """List messages in a conversation"""
        return self._request('GET', f'/conversations/{conversation_id}/messages', params={'limit': limit})