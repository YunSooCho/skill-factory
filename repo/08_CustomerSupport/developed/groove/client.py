"""Groove Help Desk API Client"""
import requests
from typing import Dict, List, Optional, Any

class GrooveClient:
    def __init__(self, api_token: str, timeout: int = 30):
        self.api_token = api_token
        self.base_url = "https://api.groovehq.com/v1"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = (self.api_token, '')
        self.session.headers.update({'Content-Type': 'application/json'})

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_tickets(self, page: int = 1) -> List[Dict[str, Any]]:
        return self._request('GET', f'/tickets?page={page}')

    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/tickets/{ticket_id}')

    def create_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/tickets', data=data)

    def update_ticket(self, ticket_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('PUT', f'/tickets/{ticket_id}', data=data)

    def send_message(self, ticket_id: str, message: str) -> Dict[str, Any]:
        return self._request('POST', f'/tickets/{ticket_id}/messages', data={'body': message})

    def get_customers(self, page: int = 1) -> List[Dict[str, Any]]:
        return self._request('GET', f'/customers?page={page}')

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/customers/{customer_id}')

    def create_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/customers', data=data)

    def get_folders(self) -> List[Dict[str, Any]]:
        return self._request('GET', '/folders')