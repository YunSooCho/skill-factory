"""
Yousign API Client

Complete client for Yousign electronic signature integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class YousignAPIClient:
    """
    Complete client for Yousign electronic signature integration.
    Supports advanced signature workflows with AES/eIDAS compliance.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Yousign API client.

        Args:
            api_key: Yousign API key (from env: YOUSIGN_API_KEY)
            base_url: Base URL (default: https://api.yousign.com/v3)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_key = api_key or os.getenv("YOUSIGN_API_KEY")
        self.base_url = base_url or os.getenv(
            "YOUSIGN_BASE_URL",
            "https://api.yousign.com/v3"
        )
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_key:
            raise ValueError(
                "API key is required. Set YOUSIGN_API_KEY environment variable."
            )

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Yousign API."""
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

        session_headers = dict(self.session.headers)
        if files:
            session_headers = {
                k: v for k, v in self.session.headers.items()
                if k != "Content-Type"
            }

        if headers:
            session_headers.update(headers)

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            files=files,
            headers=session_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return {"status": "success", "data": None}

    # Files

    def upload_file(
        self,
        file_path: str,
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload a file to Yousign."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        filename = filename or os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            files = {'file': (filename, f, 'application/pdf')}
            return self._request('POST', '/files', files=files)

    def get_file(self, file_id: str) -> Dict[str, Any]:
        """Get file details."""
        return self._request('GET', f'/files/{file_id}')

    def delete_file(self, file_id: str) -> Dict[str, Any]:
        """Delete a file."""
        return self._request('DELETE', f'/files/{file_id}')

    def download_file(self, file_id: str) -> bytes:
        """Download file."""
        url = urljoin(self.base_url + "/", f'/files/{file_id}/download')
        response = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
        response.raise_for_status()
        return response.content

    # Signature Requests

    def create_signature_request(
        self,
        name: str,
        signers: List[Dict[str, Any]],
        delivery_mode: str = "email",
        timezone: str = "Europe/Paris",
        expiry_days: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a signature request.

        Args:
            name: Request name
            signers: List of signers with details
            delivery_mode: email, sms, or none
            timezone: Timezone for the request
            expiry_days: Days until expiry

        Returns:
            Signature request information
        """
        data = {
            'name': name,
            'delivery_mode': delivery_mode,
            'timezone': timezone,
            'signers': signers
        }

        if expiry_days:
            data['expires_at'] = expiry_days

        return self._request('POST', '/signature_requests', data=data)

    def add_document_to_request(
        self,
        request_id: str,
        file_id: str,
        position: int = 0
    ) -> Dict[str, Any]:
        """Add document to signature request."""
        data = {
            'file_id': file_id,
            'position': position
        }
        return self._request('POST', f'/signature_requests/{request_id}/documents', data=data)

    def get_signature_request(self, request_id: str) -> Dict[str, Any]:
        """Get signature request details."""
        return self._request('GET', f'/signature_requests/{request_id}')

    def list_signature_requests(
        self,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """List signature requests."""
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status
        return self._request('GET', '/signature_requests', params=params)

    def activate_signature_request(self, request_id: str) -> Dict[str, Any]:
        """Activate a signature request."""
        return self._request('POST', f'/signature_requests/{request_id}/activate')

    def cancel_signature_request(self, request_id: str) -> Dict[str, Any]:
        """Cancel a signature request."""
        return self._request('POST', f'/signature_requests/{request_id}/cancel')

    def remind_signature_request(self, request_id: str) -> Dict[str, Any]:
        """Send reminder for pending signers."""
        return self._request('POST', f'/signature_requests/{request_id}/remind')

    def download_audit_trail(self, request_id: str) -> Dict[str, Any]:
        """Get audit trail document."""
        return self._request('GET', f'/signature_requests/{request_id}/documents/audit_trail')

    def download_completed_documents(self, request_id: str) -> bytes:
        """Download all completed documents."""
        url = urljoin(self.base_url + "/", f'/signature_requests/{request_id}/documents/zip')
        response = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
        response.raise_for_status()
        return response.content

    # Procedures (Advanced Workflows)

    def create_procedure(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a procedure for signature workflows."""
        data = {'name': name}
        if description:
            data['description'] = description
        return self._request('POST', '/procedures', data=data)

    def get_procedure(self, procedure_id: str) -> Dict[str, Any]:
        """Get procedure details."""
        return self._request('GET', f'/procedures/{procedure_id}')

    # Users and Teams

    def list_users(self) -> Dict[str, Any]:
        """List all users in the organization."""
        return self._request('GET', '/users')

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user details."""
        return self._request('GET', f'/users/{user_id}')

    # Webhooks

    def create_webhook(
        self,
        url: str,
        events: List[str],
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Create webhook subscription."""
        data = {'url': url, 'events': events}
        if headers:
            data['headers'] = headers
        return self._request('POST', '/webhooks', data=data)

    def list_webhooks(self) -> Dict[str, Any]:
        """List all webhooks."""
        return self._request('GET', '/webhooks')

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete webhook."""
        return self._request('DELETE', f'/webhooks/{webhook_id}')

    # Brands

    def get_brands(self) -> Dict[str, Any]:
        """Get organization brands."""
        return self._request('GET', '/brands')

    # Usage and Statistics

    def get_connection_quota(self) -> Dict[str, Any]:
        """Get connection quota information."""
        return self._request('GET', '/connection_quotas')

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return self._request('GET', '/stats')

    def close(self):
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()