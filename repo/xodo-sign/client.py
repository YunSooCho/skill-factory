"""
Xodo-Sign API Client

Complete client for Xodo-Sign electronic signature integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class XodoSignAPIClient:
    """
    Complete client for Xodo-Sign electronic signature integration.
    Supports PDF signing, document management, and workflow automation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Xodo-Sign API client.

        Args:
            api_key: Xodo-Sign API key (from env: XODO_SIGN_API_KEY)
            base_url: Base URL (default: https://api.xodosign.com/v1)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_key = api_key or os.getenv("XODO_SIGN_API_KEY")
        self.base_url = base_url or os.getenv(
            "XODO_SIGN_BASE_URL",
            "https://api.xodosign.com/v1"
        )
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_key:
            raise ValueError(
                "API key is required. Set XODO_SIGN_API_KEY environment variable."
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
        """Make HTTP request to Xodo-Sign API."""
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

    # Files and Documents

    def upload_file(
        self,
        file_path: str,
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload a file to Xodo-Sign."""
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

    # Signature Requests

    def create_signature_request(
        self,
        file_ids: List[str],
        signers: List[Dict[str, Any]],
        title: Optional[str] = None,
        message: Optional[str] = None,
        expiry_date: Optional[str] = None,
        reminder_enabled: bool = True
    ) -> Dict[str, Any]:
        """Create a signature request."""
        data = {
            'file_ids': file_ids,
            'signers': signers,
            'reminder_enabled': reminder_enabled
        }

        if title:
            data['title'] = title
        if message:
            data['message'] = message
        if expiry_date:
            data['expiry_date'] = expiry_date

        return self._request('POST', '/signature-requests', data=data)

    def get_signature_request(self, request_id: str) -> Dict[str, Any]:
        """Get signature request details."""
        return self._request('GET', f'/signature-requests/{request_id}')

    def list_signature_requests(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List signature requests."""
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status
        return self._request('GET', '/signature-requests', params=params)

    def cancel_signature_request(self, request_id: str) -> Dict[str, Any]:
        """Cancel a signature request."""
        return self._request('DELETE', f'/signature-requests/{request_id}')

    def send_reminder(self, request_id: str) -> Dict[str, Any]:
        """Send reminder for signature request."""
        return self._request('POST', f'/signature-requests/{request_id}/remind')

    def download_signed_document(self, request_id: str) -> bytes:
        """Download signed document."""
        url = urljoin(self.base_url + "/", f'/signature-requests/{request_id}/download')
        response = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
        response.raise_for_status()
        return response.content

    # Templates

    def list_templates(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List templates."""
        params = {'limit': limit, 'offset': offset}
        return self._request('GET', '/templates', params=params)

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Get template details."""
        return self._request('GET', f'/templates/{template_id}')

    def use_template(
        self,
        template_id: str,
        signers: List[Dict[str, Any]],
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create signature request from template."""
        data = {
            'template_id': template_id,
            'signers': signers
        }
        if title:
            data['title'] = title
        return self._request('POST', '/signature-requests/from-template', data=data)

    # Contacts

    def list_contacts(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List contacts."""
        params = {'limit': limit, 'offset': offset}
        return self._request('GET', '/contacts', params=params)

    def create_contact(
        self,
        email: str,
        name: Optional[str] = None,
        company: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a contact."""
        data = {'email': email}
        if name:
            data['name'] = name
        if company:
            data['company'] = company
        return self._request('POST', '/contacts', data=data)

    # Webhooks

    def create_webhook(
        self,
        url: str,
        events: List[str]
    ) -> Dict[str, Any]:
        """Create webhook."""
        data = {'url': url, 'events': events}
        return self._request('POST', '/webhooks', data=data)

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete webhook."""
        return self._request('DELETE', f'/webhooks/{webhook_id}')

    # Account

    def get_account(self) -> Dict[str, Any]:
        """Get account information."""
        return self._request('GET', '/account')

    def close(self):
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()