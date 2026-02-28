"""Notion Customer Support Integration API Client"""
import requests
from typing import Dict, List, Optional, Any

class NotionCustomercsClient:
    def __init__(self, integration_token: str, database_id: str, timeout: int = 30):
        self.integration_token = integration_token
        self.database_id = database_id
        self.base_url = "https://api.notion.com/v1"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {integration_token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        })

    def _request(self, method: str, endpoint: str, params=None, data=None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def query_database(self, filter_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        data = {}
        if filter_data:
            data['filter'] = filter_data
        return self._request('POST', f'/databases/{self.database_id}/query', data=data)

    def get_page(self, page_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/pages/{page_id}')

    def create_page(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data['parent'] = {'database_id': self.database_id}
        return self._request('POST', '/pages', data=data)

    def update_page(self, page_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('PATCH', f'/pages/{page_id}', data=data)

    def append_block(self, block_id: str, children: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self._request('PATCH', f'/blocks/{block_id}/children', data={'children': children})

    def get_page_children(self, page_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/blocks/{page_id}/children')

    def search(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/search', data=query_data)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/users/{user_id}')