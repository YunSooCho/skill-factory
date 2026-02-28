import requests
from typing import Dict, List, Optional


class FreshserviceClient:
    """
    Client for Freshservice API - IT Service Management Platform
    """

    def __init__(self, domain: str, api_key: str):
        """
        Initialize Freshservice client

        Args:
            domain: Your Freshservice domain (e.g., 'yourcompany.freshservice.com')
            api_key: Your Freshservice API key
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

    def update_time_entry(self, entry_id: int, data: Dict) -> Dict:
        """Update a time entry"""
        return self._request('PUT', f'/time_entries/{entry_id}', json={'time_entry': data})

    def delete_conversation(self, conversation_id: int) -> Dict:
        """Delete a conversation"""
        return self._request('DELETE', f'/conversations/{conversation_id}')

    def update_requester(self, requester_id: int, data: Dict) -> Dict:
        """Update a requester"""
        return self._request('PUT', f'/requesters/{requester_id}', json={'requester': data})

    def create_time_entry(self, entry_data: Dict) -> Dict:
        """Create a time entry"""
        return self._request('POST', '/time_entries', json={'time_entry': entry_data})

    def list_time_entries(self, ticket_id: Optional[int] = None) -> List[Dict]:
        """List time entries"""
        params = {'ticket_id': ticket_id} if ticket_id else {}
        result = self._request('GET', '/time_entries', params=params)
        return result.get('time_entries', []) if isinstance(result, dict) else []

    def delete_time_entry(self, entry_id: int) -> Dict:
        """Delete a time entry"""
        return self._request('DELETE', f'/time_entries/{entry_id}')

    def get_task(self, task_id: int) -> Dict:
        """Get a task by ID"""
        return self._request('GET', f'/tasks/{task_id}')

    def get_requester(self, requester_id: int) -> Dict:
        """Get a requester by ID"""
        return self._request('GET', f'/requesters/{requester_id}')

    def delete_ticket(self, ticket_id: int) -> Dict:
        """Delete a ticket"""
        return self._request('DELETE', f'/tickets/{ticket_id}')

    def create_requester(self, data: Dict) -> Dict:
        """Create a requester"""
        return self._request('POST', '/requesters', json={'requester': data})

    def create_task(self, task_data: Dict) -> Dict:
        """Create a task"""
        return self._request('POST', '/tasks', json={'task': task_data})

    def search_requesters(self, query: str) -> List[Dict]:
        """Search requesters"""
        result = self._request('GET', '/requesters/search', params={'name': query})
        return result if isinstance(result, list) else []

    def list_conversations(self, ticket_id: int) -> List[Dict]:
        """List conversations for a ticket"""
        return self._request('GET', f'/tickets/{ticket_id}/conversations')

    def update_ticket(self, ticket_id: int, data: Dict) -> Dict:
        """Update a ticket"""
        return self._request('PUT', f'/tickets/{ticket_id}', json={'ticket': data})

    def get_time_entry(self, entry_id: int) -> Dict:
        """Get a time entry by ID"""
        return self._request('GET', f'/time_entries/{entry_id}')

    def delete_task(self, task_id: int) -> Dict:
        """Delete a task"""
        return self._request('DELETE', f'/tasks/{task_id}')

    def search_agents(self, query: str) -> List[Dict]:
        """Search agents"""
        result = self._request('GET', '/agents/search', params={'name': query})
        return result if isinstance(result, list) else []

    def list_tasks(self, ticket_id: Optional[int] = None) -> List[Dict]:
        """List tasks"""
        params = {'ticket_id': ticket_id} if ticket_id else {}
        result = self._request('GET', '/tasks', params=params)
        return result.get('tasks', []) if isinstance(result, dict) else []

    def get_ticket(self, ticket_id: int) -> Dict:
        """Get a ticket by ID"""
        return self._request('GET', f'/tickets/{ticket_id}')

    def delete_requester(self, requester_id: int) -> Dict:
        """Delete a requester"""
        return self._request('DELETE', f'/requesters/{requester_id}')

    def update_agent(self, agent_id: int, data: Dict) -> Dict:
        """Update an agent"""
        return self._request('PUT', f'/agents/{agent_id}', json={'agent': data})

    def search_tickets(self, query: str) -> List[Dict]:
        """Search tickets"""
        result = self._request('GET', '/tickets/search', params={'query': query})
        return result if isinstance(result, list) else []

    def update_task(self, task_id: int, data: Dict) -> Dict:
        """Update a task"""
        return self._request('PUT', f'/tasks/{task_id}', json={'task': data})

    def create_reply(self, ticket_id: int, body: str, **kwargs) -> Dict:
        """Create a reply to a ticket"""
        data = {'body': body, 'body_html': f'<p>{body}</p>'}
        data.update(kwargs)
        return self._request('POST', f'/tickets/{ticket_id}/reply', json={'body': data})

    def create_agent(self, data: Dict) -> Dict:
        """Create an agent"""
        return self._request('POST', '/agents', json={'agent': data})