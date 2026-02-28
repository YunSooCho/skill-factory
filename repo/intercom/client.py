import requests
from typing import Dict, List, Optional


class IntercomClient:
    """Client for Intercom API - Customer Communication Platform"""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.intercom.io"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def search_articles(self, query: str) -> Dict:
        return self._request('POST', '/articles/search', json={'query': query})

    def import_data_source(self, url: str) -> Dict:
        return self._request('POST', '/data_sources/import', json={'url': url})

    def reply_to_conversation(self, conversation_id: str, message_type: str, body: str) -> Dict:
        return self._request('POST', f'/conversations/{conversation_id}/reply', json={
            'message_type': message_type,
            'body': body
        })

    def note_to_contact(self, contact_id: str, body: str) -> Dict:
        return self._request('POST', '/contacts/notes', json={'contact_id': contact_id, 'body': body})

    def send_event(self, event_name: str, user_id: str, **kwargs) -> Dict:
        data = {'event_name': event_name, 'user_id': user_id, **kwargs}
        return self._request('POST', '/events', json=data)

    def list_conversations(self, **params) -> Dict:
        return self._request('GET', '/conversations', params=params)

    def delete_contact(self, contact_id: str) -> Dict:
        return self._request('DELETE', f'/contacts/{contact_id}')

    def list_contacts(self, **params) -> Dict:
        return self._request('GET', '/contacts', params=params)

    def update_ticket(self, ticket_id: str, data: Dict) -> Dict:
        return self._request('PUT', f'/tickets/{ticket_id}', json=data)

    def create_message(self, message_data: Dict) -> Dict:
        return self._request('POST', '/messages', json=message_data)

    def create_or_update_tag(self, name: str, **kwargs) -> Dict:
        data = {'name': name, **kwargs}
        return self._request('POST', '/tags', json=data)

    def search_companies(self, query: str) -> Dict:
        return self._request('POST', '/companies/search', json={'query': query})

    def assign_conversation(self, conversation_id: str, assignee_id: str) -> Dict:
        return self._request('POST', f'/conversations/{conversation_id}/parts', json={
            'part_type': 'assignment',
            'assignee_id': assignee_id
        })

    def get_article(self, article_id: str) -> Dict:
        return self._request('GET', f'/articles/{article_id}')

    def add_translated_article(self, article_id: str, translations: Dict) -> Dict:
        return self._request('POST', f'/articles/{article_id}/translations', json=translations)

    def update_article(self, article_id: str, data: Dict) -> Dict:
        return self._request('PUT', f'/articles/{article_id}', json=data)

    def create_conversation(self, conversation_data: Dict) -> Dict:
        return self._request('POST', '/conversations', json=conversation_data)

    def create_ticket(self, ticket_data: Dict) -> Dict:
        return self._request('POST', '/tickets', json=ticket_data)

    def tag_contact(self, contact_id: str, tag_ids: List[str]) -> Dict:
        return self._request('POST', f'/contacts/{contact_id}/tags', json={'tag_ids': tag_ids})

    def get_conversation(self, conversation_id: str) -> Dict:
        return self._request('GET', f'/conversations/{conversation_id}')

    def search_contacts(self, query: str) -> Dict:
        return self._request('POST', '/contacts/search', json={'query': query})

    def list_teams(self) -> Dict:
        return self._request('GET', '/teams')

    def get_contact(self, contact_id: str) -> Dict:
        return self._request('GET', f'/contacts/{contact_id}')

    def delete_tag(self, tag_id: str) -> Dict:
        return self._request('DELETE', f'/tags/{tag_id}')

    def get_company(self, company_id: str) -> Dict:
        return self._request('GET', f'/companies/{company_id}')

    def get_ticket(self, ticket_id: str) -> Dict:
        return self._request('GET', f'/tickets/{ticket_id}')

    def list_admins(self) -> Dict:
        return self._request('GET', '/admins')

    def tag_company(self, company_id: str, tag_ids: List[str]) -> Dict:
        return self._request('POST', f'/companies/{company_id}/tags', json={'tag_ids': tag_ids})

    def list_articles(self, **params) -> Dict:
        return self._request('GET', '/articles', params=params)

    def update_contact(self, contact_id: str, data: Dict) -> Dict:
        return self._request('PUT', f'/contacts/{contact_id}', json=data)

    def create_contact(self, contact_data: Dict) -> Dict:
        return self._request('POST', '/contacts', json=contact_data)

    def create_article(self, article_data: Dict) -> Dict:
        return self._request('POST', '/articles', json=article_data)

    def get_conversation_last_message(self, conversation_id: str) -> Dict:
        conv = self.get_conversation(conversation_id)
        return conv.get('conversation_message', {})

    def create_ticket_type(self, data: Dict) -> Dict:
        return self._request('POST', '/ticket_types', json=data)

    def untag_contact(self, contact_id: str, tag_id: str) -> Dict:
        return self._request('DELETE', f'/contacts/{contact_id}/tags/{tag_id}')

    def create_or_update_company(self, data: Dict) -> Dict:
        return self._request('POST', '/companies', json=data)