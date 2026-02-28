"""
Signtime API Client

Complete client for Signtime electronic signature integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class SigntimeAPIClient:
    """
    Complete client for Signtime electronic signature integration.
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
        Initialize Signtime API client.

        Args:
            api_key: Signtime API key (from env: SIGNTIME_API_KEY)
            base_url: Base URL (default: https://api.signtime.com/v1)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_key = api_key or os.getenv("SIGNTIME_API_KEY")
        self.base_url = base_url or os.getenv(
            "SIGNTIME_BASE_URL",
            "https://api.signtime.com/v1"
        )
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_key:
            raise ValueError(
                "API key is required. Set SIGNTIME_API_KEY environment variable."
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
        Make HTTP request to Signtime API.

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

    # Document Management

    def upload_document(
        self,
        file_path: str,
        filename: Optional[str] = None,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a document to Signtime.

        Args:
            file_path: Path to the document file
            filename: Custom filename (optional)
            category: Document category

        Returns:
            Document information including document ID
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        filename = filename or os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            files = {'file': (filename, f, 'application/pdf')}
            data = {}

            if category:
                data['category'] = category

            return self._request('POST', '/documents', data=data, files=files)

    def get_document(self, document_id: str) -> Dict[str, Any]:
        """
        Get document details.

        Args:
            document_id: Signtime document ID

        Returns:
            Document details
        """
        return self._request('GET', f'/documents/{document_id}')

    def list_documents(
        self,
        limit: int = 50,
        offset: int = 0,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List documents with optional filtering.

        Args:
            limit: Number of documents to return
            offset: Pagination offset
            category: Filter by category

        Returns:
            List of documents
        """
        params = {'limit': limit, 'offset': offset}
        if category:
            params['category'] = category

        return self._request('GET', '/documents', params=params)

    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """
        Delete a document.

        Args:
            document_id: Signtime document ID

        Returns:
            Deletion status
        """
        return self._request('DELETE', f'/documents/{document_id}')

    def download_document(self, document_id: str) -> bytes:
        """
        Download a document.

        Args:
            document_id: Signtime document ID

        Returns:
            Document file content as bytes
        """
        url = urljoin(self.base_url + "/", f'documents/{document_id}/download')

        response = self.session.get(
            url,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        response.raise_for_status()

        return response.content

    # Signature Workflows

    def create_signature_request(
        self,
        document_id: str,
        signers: List[Dict[str, Any]],
        message: Optional[str] = None,
        expiry_days: Optional[int] = None,
        reminder_enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Create a signature request.

        Args:
            document_id: Document ID to sign
            signers: List of signers with email and name
                    [{'email': 'test@example.com', 'name': 'John Doe'}]
            message: Custom message to signers
            expiry_days: Days until signature request expires
            reminder_enabled: Enable automatic reminders

        Returns:
            Signature request information
        """
        data = {
            'document_id': document_id,
            'signers': signers,
            'reminder_enabled': reminder_enabled
        }

        if message:
            data['message'] = message
        if expiry_days:
            data['expiry_days'] = expiry_days

        return self._request('POST', '/signature-requests', data=data)

    def get_signature_request(self, request_id: str) -> Dict[str, Any]:
        """
        Get signature request details.

        Args:
            request_id: Signature request ID

        Returns:
            Signature request details including status
        """
        return self._request('GET', f'/signature-requests/{request_id}')

    def list_signature_requests(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List signature requests.

        Args:
            status: Filter by status (pending, completed, cancelled)
            limit: Number of requests to return
            offset: Pagination offset

        Returns:
            List of signature requests
        """
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status

        return self._request('GET', '/signature-requests', params=params)

    def cancel_signature_request(self, request_id: str) -> Dict[str, Any]:
        """
        Cancel a signature request.

        Args:
            request_id: Signature request ID

        Returns:
            Cancellation status
        """
        return self._request('POST', f'/signature-requests/{request_id}/cancel')

    def remind_signature_request(self, request_id: str) -> Dict[str, Any]:
        """
        Send reminder for signature request.

        Args:
            request_id: Signature request ID

        Returns:
            Reminder status
        """
        return self._request('POST', f'/signature-requests/{request_id}/remind')

    # Templates

    def create_template(
        self,
        document_path: str,
        name: str,
        description: Optional[str] = None,
        signer_roles: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Create a signature template.

        Args:
            document_path: Path to document file
            name: Template name
            description: Template description
            signer_roles: Predefined signer roles
                          [{'role': 'client', 'label': 'Client'}]

        Returns:
            Template information
        """
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"File not found: {document_path}")

        data = {
            'name': name,
            'description': description or ''
        }

        if signer_roles:
            data['signer_roles'] = signer_roles

        filename = os.path.basename(document_path)

        with open(document_path, 'rb') as f:
            files = {'document': (filename, f, 'application/pdf')}
            return self._request('POST', '/templates', data=data, files=files)

    def list_templates(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List all templates.

        Args:
            limit: Number of templates to return
            offset: Pagination offset

        Returns:
            List of templates
        """
        params = {'limit': limit, 'offset': offset}
        return self._request('GET', '/templates', params=params)

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """
        Get template details.

        Args:
            template_id: Template ID

        Returns:
            Template details
        """
        return self._request('GET', f'/templates/{template_id}')

    def use_template(
        self,
        template_id: str,
        signers: List[Dict[str, Any]],
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create signature request from template.

        Args:
            template_id: Template ID to use
            signers: List of signers matching template roles
            message: Custom message to signers

        Returns:
            Signature request information
        """
        data = {
            'template_id': template_id,
            'signers': signers
        }

        if message:
            data['message'] = message

        return self._request('POST', '/signature-requests/from-template', data=data)

    # Webhooks

    def create_webhook(
        self,
        url: str,
        events: List[str],
        secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a webhook subscription.

        Args:
            url: Webhook callback URL
            events: List of events to subscribe to
            secret: Optional secret for webhook signature verification

        Returns:
            Webhook information
        """
        data = {
            'url': url,
            'events': events
        }

        if secret:
            data['secret'] = secret

        return self._request('POST', '/webhooks', data=data)

    def list_webhooks(self) -> Dict[str, Any]:
        """
        List all webhooks.

        Returns:
            List of webhooks
        """
        return self._request('GET', '/webhooks')

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """
        Delete a webhook.

        Args:
            webhook_id: Webhook ID

        Returns:
            Deletion status
        """
        return self._request('DELETE', f'/webhooks/{webhook_id}')

    # Account and Analytics

    def get_account(self) -> Dict[str, Any]:
        """
        Get account information.

        Returns:
            Account details
        """
        return self._request('GET', '/account')

    def get_analytics(
        self,
        period: str = 'month',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get account analytics.

        Args:
            period: Period type (day, week, month, year)
            start_date: Custom start date (YYYY-MM-DD)
            end_date: Custom end date (YYYY-MM-DD)

        Returns:
            Analytics data
        """
        params = {'period': period}

        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date

        return self._request('GET', '/analytics', params=params)

    def get_audit_log(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get account audit log.

        Args:
            limit: Number of entries to return
            offset: Pagination offset

        Returns:
            Audit log entries
        """
        params = {'limit': limit, 'offset': offset}
        return self._request('GET', '/audit-log', params=params)

    def close(self):
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()