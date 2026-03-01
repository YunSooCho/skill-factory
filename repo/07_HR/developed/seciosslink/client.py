"""
SeciossLink API Client - Japanese IAM & SSO Solution
"""

import requests
import time
from typing import Optional, Dict, Any


class SeciossLinkError(Exception):
    """Base exception for SeciossLink"""


class SeciossLinkClient:
    BASE_URL = "https://api.seciossworks.com/v1"

    def __init__(self, api_key: str, organization_id: str, timeout: int = 30):
        """
        Initialize SeciossLink client

        Args:
            api_key: SeciossLink API key
            organization_id: Organization ID
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.organization_id = organization_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Organization-ID': organization_id
        })

        self.last_request_time = 0
        self.min_delay = 0.3

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
                raise SeciossLinkError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise SeciossLinkError(f"Error ({resp.status_code}): {resp.text}")

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
        """Create user"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/users", json=user_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_user(self, user_id: str, user_data: Dict) -> Dict[str, Any]:
        """Update user"""
        self._enforce_rate_limit()
        resp = self.session.put(
            f"{self.BASE_URL}/users/{user_id}",
            json=user_data,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Delete user"""
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.BASE_URL}/users/{user_id}", timeout=self.timeout)
        return self._handle_response(resp)

    # Groups
    def get_groups(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get groups"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/groups", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_group(self, group_data: Dict) -> Dict[str, Any]:
        """Create group"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/groups", json=group_data, timeout=self.timeout)
        return self._handle_response(resp)

    def add_user_to_group(self, group_id: str, user_id: str) -> Dict[str, Any]:
        """Add user to group"""
        self._enforce_rate_limit()
        resp = self.session.post(
            f"{self.BASE_URL}/groups/{group_id}/users/{user_id}",
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def remove_user_from_group(self, group_id: str, user_id: str) -> Dict[str, Any]:
        """Remove user from group"""
        self._enforce_rate_limit()
        resp = self.session.delete(
            f"{self.BASE_URL}/groups/{group_id}/users/{user_id}",
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Roles & Permissions
    def get_roles(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get roles"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/roles", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def assign_role(self, user_id: str, role_id: str) -> Dict[str, Any]:
        """Assign role to user"""
        self._enforce_rate_limit()
        resp = self.session.post(
            f"{self.BASE_URL}/users/{user_id}/roles/{role_id}",
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def revoke_role(self, user_id: str, role_id: str) -> Dict[str, Any]:
        """Revoke role from user"""
        self._enforce_rate_limit()
        resp = self.session.delete(
            f"{self.BASE_URL}/users/{user_id}/roles/{role_id}",
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # SSO Sessions
    def get_sessions(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get active sessions"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/sessions", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def revoke_session(self, session_id: str) -> Dict[str, Any]:
        """Revoke session"""
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.BASE_URL}/sessions/{session_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def revoke_user_sessions(self, user_id: str) -> Dict[str, Any]:
        """Revoke all user sessions"""
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.BASE_URL}/users/{user_id}/sessions", timeout=self.timeout)
        return self._handle_response(resp)

    # Audit Logs
    def get_audit_logs(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get audit logs"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/audit-logs", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Applications (SSO)
    def get_applications(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get SSO applications"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/applications", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def grant_application_access(self, user_id: str, app_id: str) -> Dict[str, Any]:
        """Grant application access to user"""
        self._enforce_rate_limit()
        resp = self.session.post(
            f"{self.BASE_URL}/users/{user_id}/applications/{app_id}",
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def revoke_application_access(self, user_id: str, app_id: str) -> Dict[str, Any]:
        """Revoke application access from user"""
        self._enforce_rate_limit()
        resp = self.session.delete(
            f"{self.BASE_URL}/users/{user_id}/applications/{app_id}",
            timeout=self.timeout
        )
        return self._handle_response(resp)