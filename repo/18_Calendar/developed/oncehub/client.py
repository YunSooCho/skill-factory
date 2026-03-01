"""
OnceHub Integration API Client

This module provides a Python client for interacting with oncehub.
"""

import requests
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class OnceHubClient:
    """
    Client for oncehub API integration.

    Provides comprehensive access to oncehub's functionality.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        access_token: Optional[str] = None,
        base_url: str = "https://api.oncehub.com/v2",
        timeout: int = 30
    ):
        """Initialize the OnceHubClient client."""
        self.api_key = api_key
        self.access_token = access_token
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def _request_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        if self.api_key:
            headers['X-API-Key'] = self.api_key
        elif self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'

        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request."""
        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method,
            url,
            headers=self._request_headers(),
            params=params,
            data=data,
            json=json_data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request."""
        return self._request('GET', endpoint, params=params)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make POST request."""
        return self._request('POST', endpoint, data=data, json_data=json_data)

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make PUT request."""
        return self._request('PUT', endpoint, data=data, json_data=json_data)

    def patch(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make PATCH request."""
        return self._request('PATCH', endpoint, data=data, json_data=json_data)

    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make DELETE request."""
        return self._request('DELETE', endpoint, params=params)

    def get_status(self) -> Dict[str, Any]:
        """Get API status."""
        return self.get('/status')

    def list_resources(self, **kwargs) -> List[Dict[str, Any]]:
        """List resources with optional filtering."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        result = self.get('/resources', params=params)
        return result.get('items', result.get('data', []))

    def get_resource(self, resource_id: str) -> Dict[str, Any]:
        """Get specific resource by ID."""
        return self.get(f'/resources/{resource_id}')

    def create_resource(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new resource."""
        return self.post('/resources', json_data=data)

    def update_resource(
        self,
        resource_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update resource."""
        return self.put(f'/resources/{resource_id}', json_data=data)

    def delete_resource(self, resource_id: str) -> Dict[str, Any]:
        """Delete resource."""
        return self.delete(f'/resources/{resource_id}')

    def search(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """Search resources."""
        params = {'q': query, **kwargs}
        result = self.get('/search', params=params)
        return result.get('items', result.get('data', []))

    def batch_create(
        self,
        items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create multiple resources."""
        return self.post('/batch', json_data={'items': items})

    def batch_update(
        self,
        updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Update multiple resources."""
        return self.patch('/batch', json_data={'updates': updates})

    def batch_delete(self, resource_ids: List[str]) -> Dict[str, Any]:
        """Delete multiple resources."""
        return self.post('/batch/delete', json_data={'ids': resource_ids})

    def get_webhooks(self) -> List[Dict[str, Any]]:
        """Get list of webhooks."""
        result = self.get('/webhooks')
        return result.get('webhooks', result.get('data', []))

    def create_webhook(
        self,
        url: str,
        events: List[str],
        **kwargs
    ) -> Dict[str, Any]:
        """Create webhook."""
        data = {
            'url': url,
            'events': events,
            **kwargs
        }
        return self.post('/webhooks', json_data=data)

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete webhook."""
        return self.delete(f'/webhooks/{webhook_id}')

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        return self.get('/account')

    def get_usage_stats(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Get usage statistics."""
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        return self.get('/usage', params=params)
