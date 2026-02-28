"""
Hennge API Client - Cloud Authentication & Identity Management
"""

import requests
import time
from typing import Optional, Dict, Any


class HenngeError(Exception):
    """Base exception for Hennge"""


class HenngeClient:
    BASE_URL = "https://api.hennge.com/v1"

    def __init__(self, api_key: str, tenant_id: str, timeout: int = 30):
        """
        Initialize Hennge client

        Args:
            api_key: Hennge API key
            tenant_id: Tenant ID
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.tenant_id = tenant_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Tenant-ID': tenant_id
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
                raise HenngeError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise HenngeError(f"Error ({resp.status_code}): {resp.text}")

        if resp.status_code == 204:
            return {}
        return resp.json()

    # Users
    def get_users(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of users"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/users", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/users/{user_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_user(self, user_data: Dict) -> Dict[str, Any]:
        """Create a user"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/users", json=user_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_user(self, user_id: str, user_data: Dict) -> Dict[str, Any]:
        """Update user"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/users/{user_id}", json=user_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Groups
    def get_groups(self) -> Dict[str, Any]:
        """Get groups"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/groups", timeout=self.timeout)
        return self._handle_response(resp)

    def create_group(self, group_data: Dict) -> Dict[str, Any]:
        """Create a group"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/groups", json=group_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Authentication
    def get_user_status(self, user_id: str) -> Dict[str, Any]:
        """Get user authentication status"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/users/{user_id}/status", timeout=self.timeout)
        return self._handle_response(resp)

    # Audit Logs
    def get_audit_logs(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get audit logs"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/audit-logs", params=params, timeout=self.timeout)
        return self._handle_response(resp)