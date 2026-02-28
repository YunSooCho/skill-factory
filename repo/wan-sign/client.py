"""
Wan-Sign API Client

Complete client for Wan-Sign electronic signature integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class WanSignAPIClient:
    """
    Complete client for Wan-Sign electronic signature integration.
    Supports document management, signature requests, and workflow automation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Wan-Sign API client.

        Args:
            api_key: Wan-Sign API key (from env: WAN_SIGN_API_KEY)
            base_url: Base URL (default: https://api.wansign.com/v1)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_key = api_key or os.getenv("WAN_SIGN_API_KEY")
        self.base_url = base_url or os.getenv(
            "WAN_SIGN_BASE_URL",
            "https://api.wansign.com/v1"
        )
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_key:
            raise ValueError(
                "API key is required. Set WAN_SIGN_API_KEY environment variable."
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
        """
        Make HTTP request to Wan-Sign API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            files: File uploads
            headers: Additional headers

        Returns:
            JSON response data

        Raises:
            requests.exceptions.RequestException: On request failure
        """
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

    # Document Operations

    def upload_document(
        self,
        file_path: str,
        filename: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload a document to Wan-Sign.

        Args:
            file_path: Path to the document file
            filename: Custom filename (optional)
            metadata: Additional document metadata

        Returns:
            Document information including document ID
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        filename = filename or os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            files = {'file': (filename, f, 'application/pdf')}
            data = {}

            if metadata:
                data['metadata'] = metadata

            return self._request('POST', '/documents', data=data, files=files)

    def get_document(self, document_id: str) -> Dict[str, Any]:
        """Get document details."""
        return self._request('GET', f'/documents/{document_id}')

    def list_documents(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List all documents."""
        params = {'limit': limit, 'offset': offset}
        return self._request('GET', '/documents', params=params)

    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete a document."""
        return self._request('DELETE', f'/documents/{document_id}')

    # Signature Requests

    def create_signature_request(
        self,
        document_id: str,
        recipients: List[Dict[str, Any]],
        subject: Optional[str] = None,
        message: Optional[str] = None,
        expiry_date: Optional[str] = None,
        reminder_interval: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a signature request.

        Args:
            document_id: Document ID to sign
            recipients: List of recipients with email and name
            subject: Email subject
            message: Email message
            expiry_date: Expiry date (YYYY-MM-DD)
            reminder_interval: Days between reminders

        Returns:
            Signature request information
        """
        data = {
            'document_id': document_id,
            'recipients': recipients
        }

        if subject:
            data['subject'] = subject
        if message:
            data['message'] = message
        if expiry_date:
            data['expiry_date'] = expiry_date
        if reminder_interval:
            data['reminder_interval'] = reminder_interval

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
        """List signature requests with filtering."""
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status
        return self._request('GET', '/signature-requests', params=params)

    def cancel_signature_request(self, request_id: str) -> Dict[str, Any]:
        """Cancel a signature request."""
        return self._request('POST', f'/signature-requests/{request_id}/cancel')

    def send_reminder(self, request_id: str) -> Dict[str, Any]:
        """Send reminder for signature request."""
        return self._request('POST', f'/signature-requests/{request_id}/remind')

    def download_signed_document(self, document_id: str) -> bytes:
        """Download signed document."""
        url = urljoin(self.base_url + "/", f'/documents/{document_id}/download')
        response = self.session.get(url, timeout=self.timeout, verify=self.verify_ssl)
        response.raise_for_status()
        return response.content

    # Templates

    def list_templates(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List all templates."""
        params = {'limit': limit, 'offset': offset}
        return self._request('GET', '/templates', params=params)

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Get template details."""
        return self._request('GET', f'/templates/{template_id}')

    def create_from_template(
        self,
        template_id: str,
        recipients: List[Dict[str, Any]],
        subject: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create signature request from template."""
        data = {
            'template_id': template_id,
            'recipients': recipients
        }
        if subject:
            data['subject'] = subject
        return self._request('POST', '/signature-requests/from-template', data=data)

    # Team and Account

    def get_account(self) -> Dict[str, Any]:
        """Get account information."""
        return self._request('GET', '/account')

    def get_team_members(self) -> Dict[str, Any]:
        """Get team members."""
        return self._request('GET', '/team/members')

    def get_usage_stats(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get usage statistics."""
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        return self._request('GET', '/usage', params=params)

    # Webhooks

    def create_webhook(
        self,
        url: str,
        events: List[str]
    ) -> Dict[str, Any]:
        """Create webhook subscription."""
        data = {'url': url, 'events': events}
        return self._request('POST', '/webhooks', data=data)

    def list_webhooks(self) -> Dict[str, Any]:
        """List all webhooks."""
        return self._request('GET', '/webhooks')

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete webhook."""
        return self._request('DELETE', f'/webhooks/{webhook_id}')

    def close(self):
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()