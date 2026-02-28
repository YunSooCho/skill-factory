"""
 Big Mailer API Client
"""

import time
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin

from .models import Contact, ContactField, ContactListResponse, FieldListResponse
from .exceptions import (
    BigMailerError,
    RateLimitError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
)


class BigMailerClient:
    """Big Mailer API Client"""

    BASE_URL = "https://api.bigmailer.io/api/v1/"
    API_VERSION = "v1"

    def __init__(
        self,
        api_key: str,
        account_id: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize Big Mailer client

        Args:
            api_key: Big Mailer API key
            account_id: Account ID (optional for some endpoints)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.account_id = account_id
        self.timeout = timeout
        self.session = requests.Session()

        # Rate limiting
        self._last_request_time = 0
        self._min_request_interval = 0.05  # 50ms between requests (allows ~20 requests per second)
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
    ) -> Dict:
        """
        Make API request with error handling and rate limiting

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: URL query parameters
            data: Form data
            json_data: JSON body data

        Returns:
            JSON response data

        Raises:
            BigMailerError: General API error
            RateLimitError: Rate limit exceeded
            AuthenticationError: Authentication failed
            ResourceNotFoundError: Resource not found
            ValidationError: Validation error
        """
        self._wait_for_rate_limit()

        url = urljoin(self.BASE_URL, endpoint)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Add account_id to params if not in endpoint
        if self.account_id and "account_id" not in endpoint:
            if params is None:
                params = {}
            params["account_id"] = self.account_id

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json_data,
                timeout=self.timeout,
            )

            # Update rate limit info from headers
            self._update_rate_limit(response.headers)

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise BigMailerError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise BigMailerError(f"Request failed: {str(e)}")

    def _update_rate_limit(self, headers: Dict):
        """Update rate limit information from response headers"""
        if "X-RateLimit-Remaining" in headers:
            self._rate_limit_remaining = int(headers["X-RateLimit-Remaining"])
        if "X-RateLimit-Reset" in headers:
            self._rate_limit_reset = int(headers["X-RateLimit-Reset"])

    def _handle_response(self, response: requests.Response) -> Dict:
        """
        Handle API response and raise appropriate exceptions

        Args:
            response: HTTP response object

        Returns:
            JSON response data

        Raises:
            BigMailerError: General API error
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
            # Return raw text if JSON parsing fails
            return {"raw": response_text}

        if response.status_code >= 200 and response.status_code < 300:
            return data
        elif response.status_code == 400:
            error_message = data.get("message", data.get("error", "Bad request"))
            raise ValidationError(error_message, response=data)
        elif response.status_code == 401:
            error_message = data.get("message", data.get("error", "Unauthorized"))
            raise AuthenticationError(error_message, response=data)
        elif response.status_code == 403:
            error_message = data.get("message", data.get("error", "Forbidden"))
            raise AuthenticationError(error_message, response=data)
        elif response.status_code == 404:
            error_message = data.get("message", data.get("error", "Not found"))
            raise ResourceNotFoundError(error_message, response=data)
        elif response.status_code == 422:
            error_message = data.get("message", data.get("error", "Validation failed"))
            if isinstance(data.get("errors"), list):
                errors = data["errors"]
                error_message = ", ".join([e.get("message", str(e)) for e in errors])
            raise ValidationError(error_message, response=data)
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            error_message = data.get("message", data.get("error", "Rate limit exceeded"))
            raise RateLimitError(error_message, retry_after=retry_after, response=data)
        else:
            error_message = data.get("message", data.get("error", f"HTTP {response.status_code}"))
            raise BigMailerError(error_message, status_code=response.status_code, response=data)

    # ==================== CONTACT ACTIONS ====================

    def list_contacts(
        self,
        page: int = 1,
        per_page: int = 25,
        email: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        lists: Optional[List[str]] = None,
        search: Optional[str] = None,
    ) -> ContactListResponse:
        """
        List contacts with filtering and pagination

        Args:
            page: Page number (default 1)
            per_page: Items per page (1-100, default 25)
            email: Filter by email
            status: Filter by status ('active', 'bounced', 'unsubscribed', etc.)
            tags: Filter by tags
            lists: Filter by lists
            search: Search query

        Returns:
            ContactListResponse with contacts and pagination info

        Raises:
            BigMailerError: If the request fails
            ValidationError: If parameters are invalid
        """
        if not 1 <= per_page <= 100:
            raise ValidationError("per_page must be between 1 and 100")

        params = {"page": page, "per_page": per_page}
        if email:
            params["email"] = email
        if status:
            params["status"] = status
        if tags:
            params["tags"] = ",".join(tags)
        if lists:
            params["lists"] = ",".join(lists)
        if search:
            params["search"] = search

        data = self._make_request("GET", "contacts", params=params)
        return ContactListResponse.from_api_response(data)

    def get_contact(self, contact_id: str) -> Contact:
        """
        Get a specific contact by ID

        Args:
            contact_id: The contact ID

        Returns:
            Contact object

        Raises:
            BigMailerError: If the request fails
            ResourceNotFoundError: If contact not found
        """
        data = self._make_request("GET", f"contacts/{contact_id}")
        return Contact.from_api_response(data)

    def get_contact_by_email(self, email: str) -> Optional[Contact]:
        """
        Get a contact by email address

        Args:
            email: Email address

        Returns:
            Contact object or None if not found

        Raises:
            BigMailerError: If the request fails
        """
        try:
            data = self._make_request("GET", "contacts", params={"email": email})
            response = ContactListResponse.from_api_response(data)
            if response.items:
                return response.items[0]
            return None
        except ResourceNotFoundError:
            return None

    def create_contact(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        tags: Optional[List[str]] = None,
        lists: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        send_welcome_email: bool = False,
    ) -> Contact:
        """
        Create a new contact

        Args:
            email: Email address (required)
            first_name: First name
            last_name: Last name
            name: Full name (overwrites first_name/last_name)
            phone: Phone number
            company: Company name
            tags: List of tags to add
            lists: List IDs to add contact to
            custom_fields: Custom field key-value pairs
            send_welcome_email: Whether to send welcome email

        Returns:
            Created Contact object

        Raises:
            BigMailerError: If the request fails
            ValidationError: If validation fails
        """
        if not email:
            raise ValidationError("email is required")

        payload = {"email": email}

        if name:
            payload["name"] = name
        else:
            if first_name:
                payload["first_name"] = first_name
            if last_name:
                payload["last_name"] = last_name
        if phone:
            payload["phone"] = phone
        if company:
            payload["company"] = company
        if tags:
            payload["tags"] = tags
        if lists:
            payload["lists"] = lists
        if custom_fields:
            payload["custom_fields"] = custom_fields
        if send_welcome_email:
            payload["send_welcome_email"] = True

        data = self._make_request("POST", "contacts", json_data=payload)
        return Contact.from_api_response(data)

    def update_contact(
        self,
        contact_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        tags: Optional[List[str]] = None,
        tags_add: Optional[List[str]] = None,
        tags_remove: Optional[List[str]] = None,
        lists: Optional[List[str]] = None,
        lists_add: Optional[List[str]] = None,
        lists_remove: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Contact:
        """
        Update an existing contact

        Args:
            contact_id: The contact ID
            email: New email (optional)
            first_name: First name
            last_name: Last name
            name: Full name (overwrites first_name/last_name)
            phone: Phone number
            company: Company name
            tags: Replace all tags (optional)
            tags_add: Tags to add (optional)
            tags_remove: Tags to remove (optional)
            lists: Replace all lists (optional)
            lists_add: Lists to add (optional)
            lists_remove: Lists to remove (optional)
            custom_fields: Custom field key-value pairs to update

        Returns:
            Updated Contact object

        Raises:
            BigMailerError: If the request fails
            ResourceNotFoundError: If contact not found
            ValidationError: If validation fails
        """
        payload = {}

        if email:
            payload["email"] = email
        if name is not None:
            payload["name"] = name
        if first_name is not None:
            payload["first_name"] = first_name
        if last_name is not None:
            payload["last_name"] = last_name
        if phone is not None:
            payload["phone"] = phone
        if company is not None:
            payload["company"] = company
        if tags is not None:
            payload["tags"] = tags
        if tags_add:
            payload["tags_add"] = tags_add
        if tags_remove:
            payload["tags_remove"] = tags_remove
        if lists is not None:
            payload["lists"] = lists
        if lists_add:
            payload["lists_add"] = lists_add
        if lists_remove:
            payload["lists_remove"] = lists_remove
        if custom_fields is not None:
            payload["custom_fields"] = custom_fields

        data = self._make_request("PATCH", f"contacts/{contact_id}", json_data=payload)
        return Contact.from_api_response(data)

    def delete_contact(self, contact_id: str) -> bool:
        """
        Delete a contact

        Args:
            contact_id: The contact ID

        Returns:
            True if deleted successfully

        Raises:
            BigMailerError: If the request fails
            ResourceNotFoundError: If contact not found
        """
        self._make_request("DELETE", f"contacts/{contact_id}")
        return True

    def batch_delete_contacts(self, contact_ids: List[str]) -> Dict[str, Any]:
        """
        Delete multiple contacts in batch

        Args:
            contact_ids: List of contact IDs to delete

        Returns:
            Response with success/failure info

        Raises:
            BigMailerError: If the request fails
            ValidationError: If validation fails
        """
        if not contact_ids:
            raise ValidationError("contact_ids list cannot be empty")

        payload = {"contact_ids": contact_ids}
        data = self._make_request("POST", "contacts/batch-delete", json_data=payload)
        return data

    # ==================== FIELD ACTIONS ====================

    def list_fields(self) -> FieldListResponse:
        """
        List all custom fields

        Returns:
            FieldListResponse with field definitions

        Raises:
            BigMailerError: If the request fails
        """
        data = self._make_request("GET", "fields")
        return FieldListResponse.from_api_response(data)

    def get_field(self, field_key: str) -> ContactField:
        """
        Get a specific custom field by key

        Args:
            field_key: The field key

        Returns:
            ContactField object

        Raises:
            BigMailerError: If the request fails
            ResourceNotFoundError: If field not found
        """
        data = self._make_request("GET", f"fields/{field_key}")
        return ContactField.from_api_response(data)

    # ==================== LIST/AUDIENCE ACTIONS ====================

    def get_list_contacts(
        self, list_id: str, page: int = 1, per_page: int = 25
    ) -> ContactListResponse:
        """
        Get all contacts in a specific list

        Args:
            list_id: The list ID
            page: Page number
            per_page: Items per page

        Returns:
            ContactListResponse with contacts

        Raises:
            BigMailerError: If the request fails
            ResourceNotFoundError: If list not found
        """
        if not 1 <= per_page <= 100:
            raise ValidationError("per_page must be between 1 and 100")

        params = {"page": page, "per_page": per_page}
        data = self._make_request("GET", f"lists/{list_id}/contacts", params=params)
        return ContactListResponse.from_api_response(data)

    # ==================== HELPER METHODS ====================

    def get_account_info(self) -> Dict:
        """
        Get account information

        Returns:
            Account data

        Raises:
            BigMailerError: If the request fails
        """
        data = self._make_request("GET", "account")
        return data

    def close(self):
        """Close the session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()