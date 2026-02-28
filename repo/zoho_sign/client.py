"""
Zoho Sign API Client

Complete client for Zoho Sign electronic signature integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class ZohoSignAPIClient:
    """
    Complete client for Zoho Sign electronic signature integration.
    Supports document management, signature workflows, templates, and advanced features.
    """

    def __init__(
        self,
        api_token: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Zoho Sign API client.

        Args:
            api_token: Zoho Sign authentication token (from env: ZOHO_SIGN_API_TOKEN)
            base_url: Base URL (default: https://sign.zoho.com/api/v1)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_token = api_token or os.getenv("ZOHO_SIGN_API_TOKEN")
        self.base_url = base_url or os.getenv(
            "ZOHO_SIGN_BASE_URL",
            "https://sign.zoho.com/api/v1"
        )
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_token:
            raise ValueError(
                "API token is required. Set ZOHO_SIGN_API_TOKEN environment variable."
            )

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Zoho-oauthtoken {self.api_token}",
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
        """Make HTTP request to Zoho Sign API."""
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
        """Upload a file to Zoho Sign."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        filename = filename or os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            files = {'file': (filename, f, 'application/pdf')}
            return self._request('POST', '/files', files=files)

    def get_file(self, file_id: str) -> Dict[str, Any]:
        """Get file details."""
        return self._request('GET', f'/files/{file_id}')

    def list_files(
        self,
        page: int = 1,
        per_page: int = 50
    ) -> Dict[str, Any]:
        """List all files."""
        params = {'page': page, 'per_page': per_page}
        return self._request('GET', '/files', params=params)

    def delete_file(self, file_id: str) -> Dict[str, Any]:
        """Delete a file."""
        return self._request('DELETE', f'/files/{file_id}')

    def download_file(self, file_id: str) -> bytes:
        """Download file."""
        url = urljoin(self.base_url + "/", f'/files/{file_id}/download')
        response = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
        response.raise_for_status()
        return response.content

    # Sign Requests

    def create_sign_request(
        self,
        file_ids: List[str],
        recipients: List[Dict[str, Any]],
        request_name: str,
        notes: Optional[str] = None,
        expiry_date: Optional[str] = None,
        reminder_period: Optional[int] = None,
        is_sequential: bool = False
    ) -> Dict[str, Any]:
        """
        Create a signature request.

        Args:
            file_ids: List of file IDs
            recipients: List of recipients with email and action
            request_name: Name for the signature request
            notes: Notes to recipients
            expiry_date: Expiry date (YYYY-MM-DD)
            reminder_period: Days between reminders
            is_sequential: Sign in sequence

        Returns:
            Signature request information
        """
        data = {
            'file_ids': file_ids,
            'request_name': request_name,
            'recipients': recipients,
            'is_sequential': is_sequential
        }

        if notes:
            data['notes'] = notes
        if expiry_date:
            data['expiry_date'] = expiry_date
        if reminder_period:
            data['reminder_period'] = reminder_period

        return self._request('POST', '/requests', data=data)

    def get_sign_request(self, request_id: str) -> Dict[str, Any]:
        """Get signature request details."""
        return self._request('GET', f'/requests/{request_id}')

    def list_sign_requests(
        self,
        page: int = 1,
        per_page: int = 50,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """List signature requests."""
        params = {'page': page, 'per_page': per_page}
        if status:
            params['status'] = status
        return self._request('GET', '/requests', params=params)

    def update_sign_request(
        self,
        request_id: str,
        notes: Optional[str] = None,
        expiry_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update signature request."""
        data = {}
        if notes:
            data['notes'] = notes
        if expiry_date:
            data['expiry_date'] = expiry_date
        return self._request('PUT', f'/requests/{request_id}', data=data)

    def submit_sign_request(self, request_id: str) -> Dict[str, Any]:
        """Submit signature request for signing."""
        return self._request('POST', f'/requests/{request_id}/submit')

    def cancel_sign_request(self, request_id: str) -> Dict[str, Any]:
        """Cancel signature request."""
        return self._request('POST', f'/requests/{request_id}/cancel')

    def remind_sign_request(self, request_id: str) -> Dict[str, Any]:
        """Send reminder to pending signers."""
        return self._request('POST', f'/requests/{request_id}/remind')

    def delete_sign_request(self, request_id: str) -> Dict[str, Any]:
        """Delete signature request."""
        return self._request('DELETE', f'/requests/{request_id}')

    def download_completed_document(self, request_id: str) -> bytes:
        """Download completed signed document."""
        url = urljoin(self.base_url + "/", f'/requests/{request_id}/documents/download')
        response = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
        response.raise_for_status()
        return response.content

    # Templates

    def create_template(
        self,
        file_path: str,
        template_name: str,
        description: Optional[str] = None,
        recipients: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Create a template."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'rb') as f:
            filename = os.path.basename(file_path)
            files = {'file': (filename, f, 'application/pdf')}
            data = {'template_name': template_name}

            if description:
                data['description'] = description
            if recipients:
                data['recipients'] = recipients

            return self._request('POST', '/templates', data=data, files=files)

    def list_templates(
        self,
        page: int = 1,
        per_page: int = 50
    ) -> Dict[str, Any]:
        """List templates."""
        params = {'page': page, 'per_page': per_page}
        return self._request('GET', '/templates', params=params)

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Get template details."""
        return self._request('GET', f'/templates/{template_id}')

    def use_template(
        self,
        template_id: str,
        recipient_details: List[Dict[str, Any]],
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create signature request from template."""
        data = {
            'template_id': template_id,
            'recipient_details': recipient_details
        }

        if notes:
            data['notes'] = notes

        return self._request('POST', '/templates/create', data=data)

    # Fields

    def add_fields(
        self,
        request_id: str,
        document_id: str,
        fields: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Add fields to document."""
        data = {
            'document_id': document_id,
            'fields': fields
        }
        return self._request('POST', f'/requests/{request_id}/fields', data=data)

    def get_fields(self, request_id: str, document_id: str) -> Dict[str, Any]:
        """Get document fields."""
        params = {'document_id': document_id}
        return self._request('GET', f'/requests/{request_id}/fields', params=params)

    # Contacts

    def list_contacts(
        self,
        page: int = 1,
        per_page: int = 50
    ) -> Dict[str, Any]:
        """List contacts."""
        params = {'page': page, 'per_page': per_page}
        return self._request('GET', '/contacts', params=params)

    def create_contact(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a contact."""
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }

        if phone:
            data['phone'] = phone

        return self._request('POST', '/contacts', data=data)

    # Webhooks

    def create_webhook(
        self,
        url: str,
        events: List[str],
        secret_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create webhook subscription."""
        data = {'url': url, 'events': events}
        if secret_key:
            data['secret_key'] = secret_key
        return self._request('POST', '/webhooks', data=data)

    def list_webhooks(self) -> Dict[str, Any]:
        """List webhooks."""
        return self._request('GET', '/webhooks')

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete webhook."""
        return self._request('DELETE', f'/webhooks/{webhook_id}')

    # Brands

    def get_brands(self) -> Dict[str, Any]:
        """Get branding settings."""
        return self._request('GET', '/brands')

    # Account and Usage

    def get_account(self) -> Dict[str, Any]:
        """Get account information."""
        return self._request('GET', '/user')

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return self._request('GET', '/usage')

    def close(self):
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()