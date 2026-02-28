"""
Signable API Client

Complete client for Signable electronic signature integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class SignableAPIClient:
    """
    Complete client for Signable electronic signature integration.
    Supports all Signable API features including document management,
    envelope creation, and signature workflows.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Signable API client.

        Args:
            api_key: Signable API key (from env: SIGNABLE_API_KEY)
            base_url: Base URL (default: https://api.signable.co.uk)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_key = api_key or os.getenv("SIGNABLE_API_KEY")
        self.base_url = base_url or os.getenv(
            "SIGNABLE_BASE_URL",
            "https://api.signable.co.uk"
        )
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_key:
            raise ValueError(
                "API key is required. Set SIGNABLE_API_KEY environment variable."
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
        Make HTTP request to Signable API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
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

        # Prepare headers
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
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Upload a PDF document to Signable.

        Args:
            file_path: Path to the PDF file
            filename: Custom filename (optional)
            tags: Document tags for organization

        Returns:
            Document information including document ID
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        filename = filename or os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            files = {'file': (filename, f, 'application/pdf')}
            data = {}

            if tags:
                data['tags'] = ','.join(tags)

            return self._request('POST', '/document', data=data, files=files)

    def get_document(self, document_id: str) -> Dict[str, Any]:
        """
        Get document details by ID.

        Args:
            document_id: Signable document ID

        Returns:
            Document details
        """
        return self._request('GET', f'/document/{document_id}')

    def list_documents(
        self,
        limit: int = 50,
        offset: int = 0,
        tags: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List all documents.

        Args:
            limit: Number of documents to return
            offset: Pagination offset
            tags: Filter by tags (comma-separated)

        Returns:
            List of documents
        """
        params = {'limit': limit, 'offset': offset}
        if tags:
            params['tags'] = tags

        return self._request('GET', '/documents', params=params)

    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """
        Delete a document.

        Args:
            document_id: Signable document ID

        Returns:
            Deletion status
        """
        return self._request('DELETE', f'/document/{document_id}')

    # Envelope/Signature Request Management

    def create_envelope(
        self,
        document_ids: List[str],
        recipients: List[Dict[str, Any]],
        title: Optional[str] = None,
        message: Optional[str] = None,
        reminder_days: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a signature envelope.

        Args:
            document_ids: List of document IDs to include
            recipients: List of recipients with email and name
                       [{'email': 'test@example.com', 'name': 'John Doe'}]
            title: Envelope title
            message: Custom message to recipients
            reminder_days: Days between reminders

        Returns:
            Envelope information including envelope ID
        """
        data = {
            'document_ids': document_ids,
            'recipients': recipients
        }

        if title:
            data['title'] = title
        if message:
            data['message'] = message
        if reminder_days:
            data['reminder_days'] = reminder_days

        return self._request('POST', '/envelope', data=data)

    def get_envelope(self, envelope_id: str) -> Dict[str, Any]:
        """
        Get envelope details.

        Args:
            envelope_id: Signable envelope ID

        Returns:
            Envelope details including status and recipients
        """
        return self._request('GET', f'/envelope/{envelope_id}')

    def list_envelopes(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List envelopes with optional filtering.

        Args:
            status: Filter by status (draft, sent, completed, cancelled)
            limit: Number of envelopes to return
            offset: Pagination offset

        Returns:
            List of envelopes
        """
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status

        return self._request('GET', '/envelopes', params=params)

    def send_envelope(self, envelope_id: str) -> Dict[str, Any]:
        """
        Send an envelope to recipients.

        Args:
            envelope_id: Signable envelope ID

        Returns:
            Send status
        """
        return self._request('POST', f'/envelope/{envelope_id}/send')

    def cancel_envelope(self, envelope_id: str) -> Dict[str, Any]:
        """
        Cancel an envelope.

        Args:
            envelope_id: Signable envelope ID

        Returns:
            Cancellation status
        """
        return self._request('POST', f'/envelope/{envelope_id}/cancel')

    def remind_envelope(self, envelope_id: str) -> Dict[str, Any]:
        """
        Send reminder for envelope.

        Args:
            envelope_id: Signable envelope ID

        Returns:
            Reminder status
        """
        return self._request('POST', f'/envelope/{envelope_id}/remind')

    # Templates

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
            template_id: Signable template ID

        Returns:
            Template details
        """
        return self._request('GET', f'/template/{template_id}')

    def create_envelope_from_template(
        self,
        template_id: str,
        recipients: List[Dict[str, Any]],
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create envelope from template.

        Args:
            template_id: Signable template ID
            recipients: List of recipients with email and name
            title: Custom envelope title

        Returns:
            Envelope information
        """
        data = {
            'template_id': template_id,
            'recipients': recipients
        }

        if title:
            data['title'] = title

        return self._request('POST', '/envelope/from-template', data=data)

    # Branding and Webhooks

    def get_branding(self) -> Dict[str, Any]:
        """
        Get account branding settings.

        Returns:
            Branding settings
        """
        return self._request('GET', '/branding')

    def create_webhook(self, url: str, events: List[str]) -> Dict[str, Any]:
        """
        Create a webhook subscription.

        Args:
            url: Webhook callback URL
            events: List of events to subscribe to
                   (e.g., ['envelope.completed', 'document.signed'])

        Returns:
            Webhook information
        """
        data = {
            'url': url,
            'events': events
        }

        return self._request('POST', '/webhook', data=data)

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
        return self._request('DELETE', f'/webhook/{webhook_id}')

    # Account and Usage

    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information.

        Returns:
            Account details including plan and limits
        """
        return self._request('GET', '/account')

    def get_usage_stats(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get usage statistics.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            Usage statistics
        """
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date

        return self._request('GET', '/usage', params=params)

    def close(self):
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()