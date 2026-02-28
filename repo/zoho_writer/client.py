"""
 Zoho Writer API Client
"""

import time
import requests
from typing import Optional, Dict, List, Any, Union
from urllib.parse import urljoin

from .models import (
    Document,
    Template,
    DocumentMetrics,
    DocumentListResponse,
    TemplateListResponse,
    WebhookEvent,
)
from .exceptions import (
    ZohoWriterError,
    RateLimitError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
)


class ZohoWriterClient:
    """Zoho Writer API Client (v1)"""

    BASE_URL = "https://writer.zoho.com/api/v1/"
    UPLOAD_URL = "https://writer.zoho.com/api/v1/"

    def __init__(
        self,
        auth_token: str,
        organization_id: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize Zoho Writer client

        Args:
            auth_token: Zoho authentication token
            organization_id: Organization ID (optional, for enterprise)
            timeout: Request timeout in seconds
        """
        self.auth_token = auth_token
        self.organization_id = organization_id
        self.timeout = timeout
        self.session = requests.Session()

        # Rate limiting
        self._last_request_time = 0
        self._min_request_interval = 0.1  # 100ms between requests
        self._rate_limit_remaining = 1000
        self._rate_limit_reset = time.time() + 3600

    def _wait_for_rate_limit(self):
        """Apply rate limiting to requests"""
        now = time.time()
        time_since_last = now - self._last_request_time

        if time_since_last < self._min_request_interval:
            sleep_time = self._min_request_interval - time_since_last
            time.sleep(sleep_time)

        self._last_request_time = time.time()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        use_upload_endpoint: bool = False,
    ) -> Union[Dict, List]:
        """
        Make API request with error handling and rate limiting

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: URL query parameters
            data: Form data
            json_data: JSON body data
            files: Files to upload
            use_upload_endpoint: Use upload endpoint instead

        Returns:
            JSON response data

        Raises:
            ZohoWriterError: General API error
            RateLimitError: Rate limit exceeded
            AuthenticationError: Authentication failed
            ResourceNotFoundError: Resource not found
            ValidationError: Validation error
        """
        self._wait_for_rate_limit()

        base_url = self.UPLOAD_URL if use_upload_endpoint else self.BASE_URL
        url = urljoin(base_url, endpoint)

        # Zoho auth token in query params
        if params is None:
            params = {}
        params["authtoken"] = self.auth_token

        if self.organization_id:
            params["organization_id"] = self.organization_id

        headers = {
            "Accept": "application/json",
        }

        if json_data:
            headers["Content-Type"] = "application/json"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                data=data,
                json=json_data,
                files=files,
                timeout=self.timeout,
            )

            # Update rate limit info from headers
            self._update_rate_limit(response.headers)

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ZohoWriterError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise ZohoWriterError(f"Request failed: {str(e)}")

    def _update_rate_limit(self, headers: Dict):
        """Update rate limit information from response headers"""
        if "X-RateLimit-Remaining" in headers:
            self._rate_limit_remaining = int(headers["X-RateLimit-Remaining"])
        if "X-RateLimit-Reset" in headers:
            self._rate_limit_reset = int(headers["X-RateLimit-Reset"])

    def _handle_response(self, response: requests.Response) -> Union[Dict, List]:
        """
        Handle API response and raise appropriate exceptions

        Args:
            response: HTTP response object

        Returns:
            JSON response data

        Raises:
            ZohoWriterError: General API error
            RateLimitError: Rate limit exceeded
            AuthenticationError: Authentication failed
            ResourceNotFoundError: Resource not found
            ValidationError: Validation error
        """
        try:
            response_text = response.text
            if response_text:
                data = response.json()
            else:
                data = {}
        except ValueError:
            return {"raw": response_text}

        # Zoho API error handling
        if isinstance(data, dict):
            if "error" in data:
                error_code = data.get("error", {}).get("code", "")
                error_message = data.get("error", {}).get("message", "Unknown error")

                if error_code in ["AUTHENTICATION_FAILURE", "INVALID_TOKEN"]:
                    raise AuthenticationError(error_message, response=data)
                elif error_code == "NOT_FOUND":
                    raise ResourceNotFoundError(error_message, response=data)
                else:
                    raise ZohoWriterError(error_message, response=data)

        if response.status_code >= 200 and response.status_code < 300:
            return data
        elif response.status_code == 400:
            error_message = self._extract_error_message(data)
            raise ValidationError(error_message, response=data)
        elif response.status_code == 401:
            error_message = self._extract_error_message(data)
            raise AuthenticationError(error_message, response=data)
        elif response.status_code == 403:
            error_message = self._extract_error_message(data)
            raise AuthenticationError(error_message, response=data)
        elif response.status_code == 404:
            error_message = self._extract_error_message(data)
            raise ResourceNotFoundError(error_message, response=data)
        elif response.status_code == 422:
            error_message = self._extract_error_message(data)
            raise ValidationError(error_message, response=data)
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            error_message = self._extract_error_message(data)
            raise RateLimitError(error_message, retry_after=retry_after, response=data)
        else:
            error_message = self._extract_error_message(data)
            raise ZohoWriterError(
                error_message or f"HTTP {response.status_code}",
                status_code=response.status_code,
                response=data,
            )

    def _extract_error_message(self, data: Union[Dict, List]) -> str:
        """Extract error message from response data"""
        if isinstance(data, dict):
            return (
                data.get("message")
                or data.get("error_message")
                or data.get("error", {}).get("message", "")
                or str(data)
            )
        return str(data)

    # ==================== DOCUMENT CREATION ====================

    def create_document(
        self,
        name: str,
        content: Optional[str] = None,
        format: str = "docx",
        language: str = "en",
        folder_id: Optional[str] = None,
    ) -> Document:
        """
        Create a new document (3)

        Args:
            name: Document name
            content: Initial content (optional)
            format: Document format ('docx', 'odt', 'pdf')
            language: Language code
            folder_id: Folder ID (optional)

        Returns:
            Created Document

        Raises:
            ZohoWriterError: If the request fails
            ValidationError: If validation fails
        """
        if not name:
            raise ValidationError("name is required")

        params = {
            "document_name": name,
            "content": content or "",
            "format": format,
            "lang": language,
        }

        if folder_id:
            params["folder_id"] = folder_id

        data = self._make_request("POST", "documents", params=params)
        return Document.from_api_response(data)

    def upload_document(
        self,
        file_path: str,
        name: Optional[str] = None,
        folder_id: Optional[str] = None,
    ) -> Document:
        """
        Create document by uploading content file (14)

        Args:
            file_path: Local file path
            name: Document name (optional, defaults to file name)
            folder_id: Folder ID (optional)

        Returns:
            Uploaded Document

        Raises:
            ZohoWriterError: If the request fails
            ValidationError: If validation fails
        """
        if not file_path:
            raise ValidationError("file_path is required")

        import os

        if not os.path.exists(file_path):
            raise ValidationError(f"File not found: {file_path}")

        files = {"content": open(file_path, "rb")}
        params = {}

        if name:
            params["document_name"] = name
        else:
            params["document_name"] = os.path.basename(file_path)

        if folder_id:
            params["folder_id"] = folder_id

        try:
            data = self._make_request("POST", "documents/upload", params=params, files=files, use_upload_endpoint=True)
            files["content"].close()
            return Document.from_api_response(data)
        except Exception as e:
            files["content"].close()
            raise e

    def create_from_template(
        self,
        template_id: str,
        name: str,
        merge_data: Optional[Dict[str, Any]] = None,
    ) -> Document:
        """
        Create document from template (1)

        Args:
            template_id: Template ID
            name: New document name
            merge_data: Data to merge into template

        Returns:
            Created Document

        Raises:
            ZohoWriterError: If the request fails
            ValidationError: If validation fails
        """
        if not template_id:
            raise ValidationError("template_id is required")
        if not name:
            raise ValidationError("name is required")

        params = {
            "template_id": template_id,
            "document_name": name,
        }

        if merge_data:
            params["merge_data"] = merge_data

        data = self._make_request("POST", f"templates/{template_id}/create", params=params)
        return Document.from_api_response(data)

    def create_from_url(
        self,
        url: str,
        name: str,
        format: Optional[str] = None,
    ) -> Document:
        """
        Create document from web URL (17)

        Args:
            url: Web URL to import from
            name: Document name
            format: Expected format (optional, auto-detected)

        Returns:
            Imported Document

        Raises:
            ZohoWriterError: If the request fails
            ValidationError: If validation fails
        """
        if not url:
            raise ValidationError("url is required")
        if not name:
            raise ValidationError("name is required")

        params = {
            "document_url": url,
            "document_name": name,
        }

        if format:
            params["format"] = format

        data = self._make_request("POST", "documents/import", params=params)
        return Document.from_api_response(data)

    def copy_document(
        self,
        document_id: str,
        new_name: str,
    ) -> Document:
        """
        Create a copy of a document (11)

        Args:
            document_id: Document ID to copy
            new_name: Name for the new copy

        Returns:
            Copied Document

        Raises:
            ZohoWriterError: If the request fails
            ResourceNotFoundError: If document not found
        """
        if not document_id:
            raise ValidationError("document_id is required")
        if not new_name:
            raise ValidationError("new_name is required")

        params = {"document_name": new_name}
        data = self._make_request("POST", f"documents/{document_id}/copy", params=params)
        return Document.from_api_response(data)

    # ==================== DOCUMENT LISTING ====================

    def list_documents(
        self,
        status: Optional[str] = None,
        sort_by: str = "modified_time",
        sort_order: str = "desc",
    ) -> DocumentListResponse:
        """
        Get documents list (13)

        Args:
            status: Filter by status ('active', 'trashed')
            sort_by: Sort field ('name', 'created_time', 'modified_time')
            sort_order: Sort order ('asc', 'desc')

        Returns:
            DocumentListResponse

        Raises:
            ZohoWriterError: If the request fails
        """
        params = {"sort_by": sort_by, "sort_order": sort_order}
        if status:
            params["status"] = status

        data = self._make_request("GET", "documents", params=params)
        return DocumentListResponse.from_api_response(data)

    def list_recent_documents(
        self,
        limit: int = 10,
    ) -> DocumentListResponse:
        """
        Get recent documents list (12)

        Args:
            limit: Maximum number of documents to return

        Returns:
            DocumentListResponse

        Raises:
            ZohoWriterError: If the request fails
        """
        if limit < 1:
            raise ValidationError("limit must be >= 1")

        params = {"limit": limit}
        data = self._make_request("GET", "documents/recent", params=params)
        return DocumentListResponse.from_api_response(data)

    def list_favorite_documents(self) -> DocumentListResponse:
        """
        Get favorite documents list (2)

        Returns:
            DocumentListResponse

        Raises:
            ZohoWriterError: If the request fails
        """
        data = self._make_request("GET", "documents/favorites")
        return DocumentListResponse.from_api_response(data)

    def list_trashed_documents(self) -> DocumentListResponse:
        """
        Get trashed documents list (6)

        Returns:
            DocumentListResponse

        Raises:
            ZohoWriterError: If the request fails
        """
        params = {"status": "trashed"}
        data = self._make_request("GET", "documents", params=params)
        return DocumentListResponse.from_api_response(data)

    def get_document(self, document_id: str) -> Document:
        """
        Get a document by ID

        Args:
            document_id: Document ID

        Returns:
            Document

        Raises:
            ZohoWriterError: If the request fails
            ResourceNotFoundError: If document not found
        """
        if not document_id:
            raise ValidationError("document_id is required")

        data = self._make_request("GET", f"documents/{document_id}")
        return Document.from_api_response(data)

    # ==================== DOCUMENT UPDATE ====================

    def update_document(
        self,
        document_id: str,
        content: str,
        replace_all: bool = True,
    ) -> Dict[str, Any]:
        """
        Update existing document content (9)

        Args:
            document_id: Document ID
            content: New content
            replace_all: Replace all content or append

        Returns:
            Update result

        Raises:
            ZohoWriterError: If the request fails
            ValidationError: If validation fails
        """
        if not document_id:
            raise ValidationError("document_id is required")
        if not content:
            raise ValidationError("content is required")

        params = {
            "content": content,
            "mode": "replace_all" if replace_all else "append",
        }

        data = self._make_request("PUT", f"documents/{document_id}/content", params=params)
        return data

    # ==================== DOCUMENT ACTIONS ====================

    def move_to_trash(self, document_id: str) -> bool:
        """
        Move document to trash (5)

        Args:
            document_id: Document ID

        Returns:
            True if moved

        Raises:
            ZohoWriterError: If the request fails
            ResourceNotFoundError: If document not found
        """
        if not document_id:
            raise ValidationError("document_id is required")

        self._make_request("PUT", f"documents/{document_id}/trash")
        return True

    def restore_document(self, document_id: str) -> Document:
        """
        Restore a trashed document (10)

        Args:
            document_id: Document ID

        Returns:
            Restored Document

        Raises:
            ZohoWriterError: If the request fails
            ResourceNotFoundError: If document not found
        """
        if not document_id:
            raise ValidationError("document_id is required")

        data = self._make_request("PUT", f"documents/{document_id}/restore")
        return Document.from_api_response(data)

    def delete_trashed_document(self, document_id: str) -> bool:
        """
        Permanently delete a trashed document (15)

        Args:
            document_id: Document ID

        Returns:
            True if deleted

        Raises:
            ZohoWriterError: If the request fails
            ResourceNotFoundError: If document not found
        """
        if not document_id:
            raise ValidationError("document_id is required")

        self._make_request("DELETE", f"documents/{document_id}/trash")
        return True

    # ==================== DOCUMENT DOWNLOAD ====================

    def download_document(
        self,
        document_id: str,
        format: str = "docx",
        output_path: Optional[str] = None,
    ) -> Union[bytes, str]:
        """
        Download document (7)

        Args:
            document_id: Document ID
            format: Download format ('docx', 'pdf', 'odt', 'html')
            output_path: Optional file path to save to

        Returns:
            Document content as bytes, or file path if output_path provided

        Raises:
            ZohoWriterError: If the request fails
            ValidationError: If validation fails
        """
        if not document_id:
            raise ValidationError("document_id is required")

        params = {"format": format}
        headers = {"Accept": "application/octet-stream"}

        try:
            response = self.session.get(
                urljoin(self.BASE_URL, f"documents/{document_id}/download"),
                params=params,
                headers=headers,
                timeout=self.timeout,
            )

            if response.status_code == 200:
                content = response.content

                if output_path:
                    with open(output_path, "wb") as f:
                        f.write(content)
                    return output_path
                return content
            else:
                raise ZohoWriterError(f"Download failed: HTTP {response.status_code}")

        except requests.exceptions.RequestException as e:
            raise ZohoWriterError(f"Download failed: {str(e)}")

    # ==================== DOCUMENT METRICS ====================

    def get_document_metrics(self, document_id: str) -> DocumentMetrics:
        """
        Get document metrics (16)

        Args:
            document_id: Document ID

        Returns:
            DocumentMetrics

        Raises:
            ZohoWriterError: If the request fails
            ResourceNotFoundError: If document not found
        """
        if not document_id:
            raise ValidationError("document_id is required")

        data = self._make_request("GET", f"documents/{document_id}/metrics")
        return DocumentMetrics.from_api_response(data)

    # ==================== DOCUMENT TRANSLATION ====================

    def translate_document(
        self,
        document_id: str,
        target_language: str,
        source_language: Optional[str] = None,
        create_new: bool = True,
    ) -> Document:
        """
        Translate document (8)

        Args:
            document_id: Document ID
            target_language: Target language code (e.g., 'fr', 'es', 'de')
            source_language: Source language code (optional, auto-detected)
            create_new: Create new document or update existing

        Returns:
            Translated Document

        Raises:
            ZohoWriterError: If the request fails
            ValidationError: If validation fails
        """
        if not document_id:
            raise ValidationError("document_id is required")
        if not target_language:
            raise ValidationError("target_language is required")

        params = {
            "target_language": target_language,
            "create_new": create_new,
        }

        if source_language:
            params["source_language"] = source_language

        data = self._make_request("POST", f"documents/{document_id}/translate", params=params)
        return Document.from_api_response(data)

    # ==================== TEMPLATE ACTIONS ====================

    def list_templates(
        self,
        category: Optional[str] = None,
    ) -> TemplateListResponse:
        """
        Get templates list (4)

        Args:
            category: Filter by category

        Returns:
            TemplateListResponse

        Raises:
            ZohoWriterError: If the request fails
        """
        params = {}
        if category:
            params["category"] = category

        data = self._make_request("GET", "templates", params=params)
        return TemplateListResponse.from_api_response(data)

    def get_template(self, template_id: str) -> Template:
        """
        Get a template by ID

        Args:
            template_id: Template ID

        Returns:
            Template

        Raises:
            ZohoWriterError: If the request fails
            ResourceNotFoundError: If template not found
        """
        if not template_id:
            raise ValidationError("template_id is required")

        data = self._make_request("GET", f"templates/{template_id}")
        return Template.from_api_response(data)

    # ==================== WEBHOOK / TRIGGERS ====================

    def create_webhook(
        self,
        webhook_url: str,
        event_types: List[str],
        document_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a webhook for triggers

        Args:
            webhook_url: URL to receive webhook events
            event_types: List of event types ('document.created', 'document.updated')
            document_id: Optional document ID to filter events

        Returns:
            Webhook configuration data

        Raises:
            ZohoWriterError: If the request fails
            ValidationError: If validation fails
        """
        if not webhook_url:
            raise ValidationError("webhook_url is required")
        if not event_types:
            raise ValidationError("event_types is required")

        json_data = {
            "webhook_url": webhook_url,
            "events": event_types,
        }

        if document_id:
            json_data["document_id"] = document_id

        data = self._make_request("POST", "webhooks", json_data=json_data)
        return data

    def list_webhooks(self) -> List[Dict]:
        """
        List all webhooks

        Returns:
            List of webhook configurations

        Raises:
            ZohoWriterError: If the request fails
        """
        data = self._make_request("GET", "webhooks")
        return data.get("webhooks", [])

    def delete_webhook(self, webhook_id: str) -> bool:
        """
        Delete a webhook

        Args:
            webhook_id: Webhook ID

        Returns:
            True if deleted

        Raises:
            ZohoWriterError: If the request fails
        """
        self._make_request("DELETE", f"webhooks/{webhook_id}")
        return True

    def verify_webhook_event(self, payload: Dict, signature: Optional[str] = None) -> bool:
        """
        Verify webhook event signature

        Args:
            payload: Webhook event payload
            signature: X-Zoho-Signature header value (optional)

        Returns:
            True if signature is valid

        Note:
            Zoho webhooks use HMAC-SHA256 signature verification
        """
        if not signature:
            return False

        # Zoho signature format
        import hmac
        import hashlib

        # In a real implementation, you would use a webhook secret
        # This is a simplified version
        computed = hmac.new(
            self.auth_token.encode(), str(payload).encode(), hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(computed[6:], signature)

    # ==================== HELPER METHODS ====================

    def close(self):
        """Close the session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()