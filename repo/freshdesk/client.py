import requests
from typing import Dict, List, Optional


class FreshdeskClient:
    """
    Client for Freshdesk API - Customer Support Platform
    """

    def __init__(self, domain: str, api_key: str):
        """
        Initialize Freshdesk client

        Args:
            domain: Your Freshdesk domain (e.g., 'yourcompany.freshdesk.com')
            api_key: Your Freshdesk API key
        """
        self.domain = domain
        self.api_key = api_key
        self.base_url = f"https://{domain.rstrip('/')}/api/v2"
        self.session = requests.Session()
        self.session.auth = (api_key, 'X')
        self.session.headers.update({'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Internal method to make API requests"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def create_ticket(self, ticket_data: Dict) -> Dict:
        """Create a new ticket"""
        return self._request('POST', '/tickets', json={'ticket': ticket_data})

    def update_ticket(self, ticket_id: int, data: Dict) -> Dict:
        """Update a ticket"""
        return self._request('PUT', f'/tickets/{ticket_id}', json={'ticket': data})

    def search_companies(self, query: str) -> List[Dict]:
        """Search companies"""
        result = self._request('GET', '/companies/search', params={'name': query})
        return result if isinstance(result, list) else []

    def update_contact(self, contact_id: int, data: Dict) -> Dict:
        """Update a contact"""
        return self._request('PUT', f'/contacts/{contact_id}', json={'contact': data})

    def get_company(self, company_id: int) -> Dict:
        """Get a company by ID"""
        return self._request('GET', f'/companies/{company_id}')

    def delete_company(self, company_id: int) -> Dict:
        """Delete a company"""
        return self._request('DELETE', f'/companies/{company_id}')

    def delete_contact(self, contact_id: int) -> Dict:
        """Delete a contact"""
        return self._request('DELETE', f'/contacts/{contact_id}')

    def list_ticket_conversations(self, ticket_id: int) -> List[Dict]:
        """List conversations for a ticket"""
        return self._request('GET', f'/tickets/{ticket_id}/conversations')

    def get_ticket(self, ticket_id: int) -> Dict:
        """Get a ticket by ID"""
        return self._request('GET', f'/tickets/{ticket_id}')

    def add_note_to_ticket(self, ticket_id: int, note: str, **kwargs) -> Dict:
        """Add a note to a ticket"""
        data = {'body': note, 'body_html': f'<p>{note}</p>', 'private': True}
        data.update(kwargs)
        return self._request('POST', f'/tickets/{ticket_id}/notes', json={'body': data})

    def update_company(self, company_id: int, data: Dict) -> Dict:
        """Update a company"""
        return self._request('PUT', f'/companies/{company_id}', json={'company': data})

    def delete_ticket(self, ticket_id: int) -> Dict:
        """Delete a ticket"""
        return self._request('DELETE', f'/tickets/{ticket_id}')

    def get_latest_ticket_conversation(self, ticket_id: int) -> List[Dict]:
        """Get latest conversation for a ticket"""
        convs = self.list_ticket_conversations(ticket_id)
        return convs[-1:] if convs else []

    def create_company(self, data: Dict) -> Dict:
        """Create a company"""
        return self._request('POST', '/companies', json={'company': data})

    def get_contact(self, contact_id: int) -> Dict:
        """Get a contact by ID"""
        return self._request('GET', f'/contacts/{contact_id}')

    def reply_to_ticket(self, ticket_id: int, body: str, **kwargs) -> Dict:
        """Reply to a ticket"""
        data = {'body': body, 'body_html': f'<p>{body}</p>'}
        data.update(kwargs)
        return self._request('POST', f'/tickets/{ticket_id}/reply', json={'body': data})

    def create_contact(self, contact_data: Dict) -> Dict:
        """Create a contact"""
        return self._request('POST', '/contacts', json={'contact': contact_data})

    def search_contacts(self, query: str) -> List[Dict]:
        """Search contacts"""
        result = self._request('GET', '/contacts/search', params={'name': query})
        return result if isinstance(result, list) else []