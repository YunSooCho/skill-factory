"""
Cybozu API Client - Japanese Business Application Platform (kintone)
"""

import requests
import time
from typing import Optional, Dict, Any


class CybozuError(Exception):
    """Base exception for Cybozu"""


class CybozuClient:
    def __init__(self, subdomain: str, api_token: str, app_id: Optional[str] = None, timeout: int = 30):
        """
        Initialize Cybozu/Kintone client

        Args:
            subdomain: Kintone subdomain (e.g., 'company' from 'company.cybozu.com')
            api_token: API token
            app_id: App ID (optional, can be set per request)
            timeout: Request timeout in seconds
        """
        self.subdomain = subdomain
        self.api_token = api_token
        self.default_app_id = app_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'X-Cybozu-API-Token': api_token,
            'Content-Type': 'application/json'
        })

        self.last_request_time = 0
        self.min_delay = 0.5

    def _enforce_rate_limit(self):
        """Enforce rate limiting"""
        current = time.time()
        elapsed = current - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise CybozuError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise CybozuError(f"Error ({resp.status_code}): {resp.text}")

        return resp.json()

    def get_base_url(self, app_id: Optional[str] = None) -> str:
        """Get base URL for Kintone API"""
        return f"https://{self.subdomain}.cybozu.com/k/v1"

    # Records
    def get_records(self, app_id: Optional[str] = None, query: Optional[str] = None, fields: Optional[list] = None) -> Dict[str, Any]:
        """Get records from an app"""
        self._enforce_rate_limit()
        app = app_id or self.default_app_id
        data = {'app': app}
        if query:
            data['query'] = query
        if fields:
            data['fields'] = fields

        resp = self.session.post(f"{self.get_base_url()}/records.json", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_record(self, record_id: str, app_id: Optional[str] = None) -> Dict[str, Any]:
        """Get a specific record"""
        self._enforce_rate_limit()
        app = app_id or self.default_app_id
        data = {'app': app, 'id': record_id}

        resp = self.session.get(f"{self.get_base_url()}/record.json", params=data, timeout=self.timeout)
        return self._handle_response(resp)

    def add_record(self, record_data: Dict, app_id: Optional[str] = None) -> Dict[str, Any]:
        """Add a record"""
        self._enforce_rate_limit()
        app = app_id or self.default_app_id
        data = {'app': app, 'record': record_data}

        resp = self.session.post(f"{self.get_base_url()}/record.json", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_record(self, record_id: str, record_data: Dict, app_id: Optional[str] = None) -> Dict[str, Any]:
        """Update a record"""
        self._enforce_rate_limit()
        app = app_id or self.default_app_id
        data = {'app': app, 'id': record_id, 'record': record_data}

        resp = self.session.put(f"{self.get_base_url()}/record.json", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_records(self, record_ids: list, app_id: Optional[str] = None) -> Dict[str, Any]:
        """Delete records"""
        self._enforce_rate_limit()
        app = app_id or self.default_app_id
        data = {'app': app, 'ids': record_ids}

        resp = self.session.post(f"{self.get_base_url()}/records.json", json=data, timeout=self.timeout)
        resp = self.session.delete(f"{self.get_base_url()}/records.json", json=data, timeout=self.timeout)
        return self._handle_response(resp)

    # App
    def get_app(self, app_id: Optional[str] = None) -> Dict[str, Any]:
        """Get app information"""
        self._enforce_rate_limit()
        app = app_id or self.default_app_id

        resp = self.session.get(f"{self.get_base_url()}/app.json", params={'id': app}, timeout=self.timeout)
        return self._handle_response(resp)

    def get_form_fields(self, app_id: Optional[str] = None) -> Dict[str, Any]:
        """Get form fields for an app"""
        self._enforce_rate_limit()
        app = app_id or self.default_app_id

        resp = self.session.get(f"{self.get_base_url()}/app/form/fields.json", params={'app': app}, timeout=self.timeout)
        return self._handle_response(resp)

    # Users/Groups
    def get_users(self) -> Dict[str, Any]:
        """Get users"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.get_base_url()}/users.json", timeout=self.timeout)
        return self._handle_response(resp)

    def get_groups(self) -> Dict[str, Any]:
        """Get groups"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.get_base_url()}/groups.json", timeout=self.timeout)
        return self._handle_response(resp)