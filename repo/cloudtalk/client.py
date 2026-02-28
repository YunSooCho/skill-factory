import requests
from typing import Dict, List, Optional


class CloudtalkClient:
    """
    Client for Cloudtalk API - Cloud Phone System
    """

    def __init__(self, api_key: str, base_url: str = "https://api.cloudtalk.io"):
        """
        Initialize Cloudtalk client

        Args:
            api_key: Cloudtalk API key
            base_url: Base URL for Cloudtalk API
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
        return response.json()

    def create_contact(self, contact_data: Dict) -> Dict:
        """Create a new contact"""
        return self._request('POST', '/contacts', json=contact_data)

    def send_sms(self, phone_number: str, message: str, **kwargs) -> Dict:
        """Send an SMS message"""
        data = {'to': phone_number, 'body': message}
        data.update(kwargs)
        return self._request('POST', '/sms/send', json=data)

    def search_contact(self, query: str) -> List[Dict]:
        """Search contacts"""
        result = self._request('GET', '/contacts/search', params={'q': query})
        return result.get('results', [])

    def delete_contact(self, contact_id: str) -> Dict:
        """Delete a contact"""
        return self._request('DELETE', f'/contacts/{contact_id}')

    def update_contact(self, contact_id: str, data: Dict) -> Dict:
        """Update a contact"""
        return self._request('PUT', f'/contacts/{contact_id}', json=data)

    def get_contact(self, contact_id: str) -> Dict:
        """Get a specific contact"""
        return self._request('GET', f'/contacts/{contact_id}')