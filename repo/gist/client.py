import requests
from typing import Dict, List, Optional


class GistClient:
    """
    Client for Gist API - Customer Engagement Platform
    """

    def __init__(self, api_key: str, base_url: str = "https://api.gist.com"):
        """
        Initialize Gist client

        Args:
            api_key: Gist API key
            base_url: Base URL for Gist API
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Internal method to make API requests"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def remove_tag_from_contacts(self, tag: str, contact_ids: List[str]) -> Dict:
        """Remove a tag from multiple contacts"""
        return self._request('POST', '/v1/tags/remove', json={
            'tag': tag,
            'contact_ids': contact_ids
        })

    def unsubscribe_contact_from_campaign(self, contact_id: str, campaign_id: str) -> Dict:
        """Unsubscribe contact from a campaign"""
        return self._request('POST', f'/v1/contacts/{contact_id}/unsubscribe', json={
            'campaign_id': campaign_id
        })

    def delete_contact(self, contact_id: str) -> Dict:
        """Delete a contact"""
        return self._request('DELETE', f'/v1/contacts/{contact_id}')

    def tag_contacts(self, tag: str, contact_ids: List[str]) -> Dict:
        """Tag multiple contacts"""
        return self._request('POST', '/v1/tags/apply', json={
            'tag': tag,
            'contact_ids': contact_ids
        })

    def create_or_update_contact(self, contact_data: Dict) -> Dict:
        """Create or update a contact"""
        return self._request('POST', '/v1/contacts', json=contact_data)

    def search_contact(self, query: str) -> List[Dict]:
        """Search for contacts"""
        result = self._request('GET', '/v1/contacts/search', params={'q': query})
        return result.get('contacts', [])

    def get_contact(self, contact_id: str) -> Dict:
        """Get a specific contact"""
        return self._request('GET', f'/v1/contacts/{contact_id}')

    def subscribe_contact_to_campaign(self, contact_id: str, campaign_id: str) -> Dict:
        """Subscribe contact to a campaign"""
        return self._request('POST', f'/v1/contacts/{contact_id}/subscribe', json={
            'campaign_id': campaign_id
        })