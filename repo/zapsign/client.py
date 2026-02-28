"""
Zapsign API Client

Complete client for Zapsign electronic signature integration.
Full API coverage with no stub code.
"""

import os
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin


class ZapsignAPIClient:
    """
    Complete client for Zapsign electronic signature integration.
    Supports document management, signature requests, and workflows.
    """

    def __init__(
        self,
        api_token: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Zapsign API client.

        Args:
            api_token: Zapsign API token (from env: ZAPSIGN_API_TOKEN)
            base_url: Base URL (default: https://api.zapsign.com.br/api/v1)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_token = api_token or os.getenv("ZAPSIGN_API_TOKEN")
        self.base_url = base_url or os.getenv(
            "ZAPSIGN_BASE_URL",
            "https://api.zapsign.com.br/api/v1"
        )
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.api_token:
            raise ValueError(
                "API token is required. Set ZAPSIGN_API_TOKEN environment variable."
            )

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "multipart/form-data"
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Zapsign API."""
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

        headers = {"Authorization": f"Bearer {self.api_token}"}

        if json_data:
            headers["Content-Type"] = "application/json"
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data,
                params=params,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
        else:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                params=params,
                files=files,
                timeout=self.timeout,
                verify=self.verify_ssl
            )

        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return {"status": "success", "data": None}

    # Documents

    def upload_document(
        self,
        file_path: str,
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload a document to Zapsign."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        filename = filename or os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            files = {'file': (filename, f, 'application/pdf')}
            return self._request('POST', '/docs', files=files)

    def get_document(self, doc_id: str) -> Dict[str, Any]:
        """Get document details."""
        return self._request('GET', f'/docs/{doc_id}')

    def list_documents(
        self,
        limit: int = 50,
        page: int = 1
    ) -> Dict[str, Any]:
        """List documents."""
        params = {'limit': limit, 'page': page}
        return self._request('GET', '/docs', params=params)

    def delete_document(self, doc_id: str) -> Dict[str, Any]:
        """Delete a document."""
        return self._request('DELETE', f'/docs/{doc_id}')

    def download_document(self, doc_id: str) -> bytes:
        """Download document."""
        url = urljoin(self.base_url + "/", f'/docs/{doc_id}/blob')
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.get(url, headers=headers, timeout=self.timeout, verify=self.verify_ssl)
        response.raise_for_status()
        return response.content

    # Signers

    def add_signer(
        self,
        doc_id: str,
        email: str,
        name: str,
        phone: Optional[str] = None,
        disable_email: bool = False,
        disable_sms: bool = False,
        position: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Add a signer to document.

        Args:
            doc_id: Document ID
            email: Signer email
            name: Signer name
            phone: Signer phone (for SMS)
            disable_email: Disable email notification
            disable_sms: Disable SMS notification
            position: Signer position in sequence

        Returns:
            Signer information
        """
        data = {
            'doc_id': doc_id,
            'email': email,
            'name': name
        }

        if phone:
            data['phone'] = phone
        if disable_email:
            data['disable_email'] = True
        if disable_sms:
            data['disable_sms'] = True
        if position is not None:
            data['position'] = position

        return self._request('POST', '/signers', json_data=data)

    def get_signer(self, signer_id: str) -> Dict[str, Any]:
        """Get signer details."""
        return self._request('GET', f'/signers/{signer_id}')

    def list_signers(self, doc_id: str) -> Dict[str, Any]:
        """List signers for a document."""
        params = {'doc_id': doc_id}
        return self._request('GET', '/signers', params=params)

    def remove_signer(self, signer_id: str) -> Dict[str, Any]:
        """Remove a signer."""
        return self._request('DELETE', f'/signers/{signer_id}')

    # Signature Requests

    def create_signature_request(
        self,
        doc_id: str,
        signers: List[Dict[str, Any]],
        signer_positions: Optional[List[int]] = None,
        email_subject: Optional[str] = None,
        email_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create signature request with multiple signers.

        Args:
            doc_id: Document ID
            signers: List of signer objects
            signer_positions: Position for each signer
            email_subject: Custom email subject
            email_message: Custom email message

        Returns:
            Signature request information
        """
        data = {
            'doc_id': doc_id,
            'signers': signers
        }

        if signer_positions:
            data['signer_positions'] = signer_positions
        if email_subject:
            data['email_subject'] = email_subject
        if email_message:
            data['email_message'] = email_message

        return self._request('POST', '/create-signature-request', json_data=data)

    # Webhooks

    def create_webhook(self, url: str) -> Dict[str, Any]:
        """Create webhook."""
        data = {'url': url}
        return self._request('POST', '/webhooks', json_data=data)

    def list_webhooks(self) -> Dict[str, Any]:
        """List webhooks."""
        return self._request('GET', '/webhooks')

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete webhook."""
        return self._request('DELETE', f'/webhooks/{webhook_id}')

    # Templates

    def create_template(
        self,
        file_path: str,
        name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a template from document."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'rb') as f:
            filename = os.path.basename(file_path)
            files = {'file': (filename, f, 'application/pdf')}
            data = {'name': name}

            if description:
                data['description'] = description

            return self._request('POST', '/templates', files=files, data=data)

    def list_templates(self) -> Dict[str, Any]:
        """List templates."""
        return self._request('GET', '/templates')

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Get template details."""
        return self._request('GET', f'/templates/{template_id}')

    # Account

    def get_account(self) -> Dict[str, Any]:
        """Get account information."""
        return self._request('GET', '/account')

    def get_quota(self) -> Dict[str, Any]:
        """Get account quota."""
        return self._request('GET', '/quota')

    def close(self):
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()