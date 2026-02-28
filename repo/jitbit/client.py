"""Jitbit Help Desk API Client"""
import requests
from typing import Dict, List, Optional, Any

class JitbitClient:
    def __init__(self, api_key: str, base_url: str, timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        params = params or {}
        params['apiKey'] = self.api_key
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_ticket(self, ticket_id: int) -> Dict[str, Any]:
        return self._request('GET', f'/GetTicket', params={'id': ticket_id})

    def get_tickets(self, start_date: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        params = {'count': limit}
        if start_date:
            params['startDate'] = start_date
        return self._request('GET', '/GetTickets', params=params)

    def create_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/CreateTicket', data=data)

    def update_ticket(self, ticket_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/UpdateTicket', data={'id': ticket_id, **data})

    def get_categories(self) -> List[Dict[str, Any]]:
        return self._request('GET', '/GetCategories')

    def get_users(self) -> List[Dict[str, Any]]:
        return self._request('GET', '/GetUsers')

    def get_user(self, user_id: int) -> Dict[str, Any]:
        return self._request('GET', '/GetUserInfo', params={'userId': user_id})

    def add_comment(self, ticket_id: int, comment: str) -> Dict[str, Any]:
        return self._request('POST', '/PostComment', data={'id': ticket_id, 'comment': comment})