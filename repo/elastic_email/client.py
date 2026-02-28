"""
 Elastic Email API Client
"""

import time
import requests
from typing import Optional, Dict, List, Any, Union
from urllib.parse import urljoin

from .models import Contact, EmailList, ContactListResponse, EmailListListResponse
from .exceptions import (
    ElasticEmailError,
    RateLimitError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
)


class ElasticEmailClient:
    """Elastic Email API Client (v2/newer API)"""

    BASE_URL = "https://api.elasticemail.com/v2/"
    ALTERNATIVE_BASE = "https://api.elasticemail.com/"

    def __init__(
        self,
        api_key: str,
        base_url: str = None,
        timeout: int = 30,
    ):
        """
        Initialize Elastic Email client

        Args:
            api_key: Elastic Email API key
            base_url: Optional alternative base URL
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
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
        use_alternative_api: bool = False,
    ) -> Union[Dict, List]:
        """
        Make API request with error handling and rate limiting

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: URL query parameters
            data: Form data
            json_data: JSON body data
            use_alternative_api: Use alternative base URL

        Returns:
            JSON response data

        Raises:
            ElasticEmailError: General API error
            RateLimitError: Rate limit exceeded
            AuthenticationError: Authentication failed
            ResourceNotFoundError: Resource not found
            ValidationError: Validation error
        """
        self._wait_for_rate_limit()

        base = self.ALTERNATIVE_BASE if use_alternative_api else self.base_url
        url = urljoin(base, endpoint)

        # For Elastic Email, typically API key is sent via query param or header
        if params is None:
            params = {}
        params["apikey"] = self.api_key

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                data=data,
                json=json_data,
                timeout=self.timeout,
            )

            # Update rate limit info from headers
            self._update_rate_limit(response.headers)

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ElasticEmailError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise ElasticEmailError(f"Request failed: {str(e)}")

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
            ElasticEmailError: General API error
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
            # Try to parse as text if JSON fails
            if response.status_code < 400:
                return {"success": True, "status_code": response.status_code}
            return {"raw": response_text}

        # Elastic Email often returns {"success": True/False, "error": "..."}
        if isinstance(data, dict):
            success = data.get("success")
            if success is False:
                error_msg = data.get("error", "Unknown error")
                if "authentication" in error_msg.lower() or "unauthorized" in error_msg.lower():
                    raise AuthenticationError(error_msg, response=data)
                elif "not found" in error_msg.lower():
                    raise ResourceNotFoundError(error_msg, response=data)
                raise ElasticEmailError(error_msg, response=data)

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
            raise ElasticEmailError(
                error_message or f"HTTP {response.status_code}",
                status_code=response.status_code,
                response=data,
            )

    def _extract_error_message(self, data: Union[Dict, List]) -> str:
        """Extract error message from response data"""
        if isinstance(data, dict):
            return (
                data.get("message")
                or data.get("error")
                or data.get("errorMessage")
                or str(data)
            )
        return str(data)

    # ==================== CONTACT ACTIONS ====================

    def add_contact(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        name: Optional[str] = None,
        lists: Optional[List[str]] = None,
        fields: Optional[Dict[str, Any]] = None,
        status: str = "active",
        send_welcome_email: bool = False,
    ) -> Contact:
        """
        Add a new contact

        Args:
            email: Email address (required)
            first_name: First name
            last_name: Last name
            name: Full name (overwrites first_name/last_name)
            lists: List IDs to add contact to
            fields: Custom field key-value pairs
            status: Contact status ('active', 'bounced', 'unsubscribed', etc.)
            send_welcome_email: Whether to send welcome email

        Returns:
            Created Contact object

        Raises:
            ElasticEmailError: If the request fails
            ValidationError: If validation fails
        """
        if not email:
            raise ValidationError("email is required")

        # Use alternative API which supports contact management
        data = {
            "email": email,
            "status": status,
            "sendWelcomeEmail": send_welcome_email,
        }

        if name:
            data["name"] = name
        else:
            if first_name:
                data["firstName"] = first_name
            if last_name:
                data["lastName"] = last_name
        if lists:
            data["listNames"] = lists
        if fields:
            data["fields"] = fields

        response = self._make_request("POST", "contact/add", use_alternative_api=True, json_data=data)
        return Contact.from_api_response(response)

    def get_contact(self, email: str) -> Contact:
        """
        Get a contact by email

        Args:
            email: Email address

        Returns:
            Contact object

        Raises:
            ElasticEmailError: If the request fails
            ResourceNotFoundError: If contact not found
        """
        if not email:
            raise ValidationError("email is required")

        data = self._make_request(
            "GET", "contact/load", use_alternative_api=True, params={"email": email}
        )
        return Contact.from_api_response(data)

    def update_contact(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        name: Optional[str] = None,
        lists: Optional[List[str]] = None,
        fields: Optional[Dict[str, Any]] = None,
        status: Optional[str] = None,
    ) -> Contact:
        """
        Update an existing contact

        Args:
            email: Email address
            first_name: First name
            last_name: Last name
            name: Full name
            lists: List IDs to set
            fields: Custom field key-value pairs to update
            status: Contact status

        Returns:
            Updated Contact object

        Raises:
            ElasticEmailError: If the request fails
            ResourceNotFoundError: If contact not found
            ValidationError: If validation fails
        """
        if not email:
            raise ValidationError("email is required")

        data = {"email": email}

        if name is not None:
            data["name"] = name
        else:
            if first_name is not None:
                data["firstName"] = first_name
            if last_name is not None:
                data["lastName"] = last_name
        if lists is not None:
            data["listNames"] = lists
        if fields is not None:
            data["fields"] = fields
        if status is not None:
            data["status"] = status

        response = self._make_request(
            "PUT", "contact/update", use_alternative_api=True, json_data=data
        )
        return Contact.from_api_response(response)

    def delete_contact(self, email: str) -> bool:
        """
        Delete a contact

        Args:
            email: Email address

        Returns:
            True if deleted successfully

        Raises:
            ElasticEmailError: If the request fails
            ResourceNotFoundError: If contact not found
        """
        if not email:
            raise ValidationError("email is required")

        self._make_request(
            "DELETE", "contact/delete", use_alternative_api=True, params={"email": email}
        )
        return True

    def list_contacts(
        self,
        list_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> ContactListResponse:
        """
        List contacts with filtering and pagination

        Args:
            list_id: Filter by list ID
            limit: Maximum number of contacts to return (1-500)
            offset: Pagination offset
            status: Filter by status
            search: Search query

        Returns:
            ContactListResponse with contacts and pagination info

        Raises:
            ElasticEmailError: If the request fails
            ValidationError: If parameters are invalid
        """
        if not 1 <= limit <= 500:
            raise ValidationError("limit must be between 1 and 500")

        params = {"limit": limit, "offset": offset}
        if list_id:
            params["list"] = list_id
        if status:
            params["status"] = status
        if search:
            params["search"] = search

        data = self._make_request("GET", "contact/list", use_alternative_api=True, params=params)
        return ContactListResponse.from_api_response(data)

    # ==================== LIST ACTIONS ====================

    def add_list(
        self,
        name: str,
        description: Optional[str] = None,
        status: str = "active",
    ) -> EmailList:
        """
        Create a new email list

        Args:
            name: List name (required)
            description: List description
            status: List status ('active' or 'inactive')

        Returns:
            Created EmailList object

        Raises:
            ElasticEmailError: If the request fails
            ValidationError: If validation fails
        """
        if not name:
            raise ValidationError("name is required")

        data = {"name": name, "status": status}
        if description:
            data["description"] = description

        response = self._make_request("POST", "list/create", use_alternative_api=True, json_data=data)
        return EmailList.from_api_response(response)

    def get_list(self, list_id: str) -> EmailList:
        """
        Get a list by ID

        Args:
            list_id: The list ID

        Returns:
            EmailList object

        Raises:
            ElasticEmailError: If the request fails
            ResourceNotFoundError: If list not found
        """
        if not list_id:
            raise ValidationError("list_id is required")

        data = self._make_request(
            "GET", "list/load", use_alternative_api=True, params={"list": list_id}
        )
        return EmailList.from_api_response(data)

    def update_list(
        self,
        list_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> EmailList:
        """
        Update an email list

        Args:
            list_id: The list ID
            name: New name
            description: New description
            status: New status ('active' or 'inactive')

        Returns:
            Updated EmailList object

        Raises:
            ElasticEmailError: If the request fails
            ResourceNotFoundError: If list not found
            ValidationError: If validation fails
        """
        if not list_id:
            raise ValidationError("list_id is required")

        data = {"list": list_id}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if status is not None:
            data["status"] = status

        response = self._make_request(
            "PUT", "list/update", use_alternative_api=True, json_data=data
        )
        return EmailList.from_api_response(response)

    def get_lists(
        self,
        limit: int = 100,
        offset: int = 0,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> EmailListListResponse:
        """
        Get all email lists

        Args:
            limit: Maximum number of lists to return (1-500)
            offset: Pagination offset
            status: Filter by status
            search: Search query

        Returns:
            EmailListListResponse with lists

        Raises:
            ElasticEmailError: If the request fails
            ValidationError: If parameters are invalid
        """
        if not 1 <= limit <= 500:
            raise ValidationError("limit must be between 1 and 500")

        params = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        if search:
            params["search"] = search

        data = self._make_request("GET", "list/list", use_alternative_api=True, params=params)
        return EmailListListResponse.from_api_response(data)

    # ==================== EMAIL SENDING ACTIONS (Optional) ====================

    def send_email(
        self,
        to: Union[str, List[str]],
        subject: str,
        body_html: str,
        from_email: str,
        from_name: str,
        body_text: Optional[str] = None,
        reply_to: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        Send an email

        Args:
            to: Recipient email(s)
            subject: Email subject
            body_html: HTML email body
            from_email: From email
            from_name: From name
            body_text: Plain text email body
            reply_to: Reply-to address
            cc: CC recipients
            bcc: BCC recipients
            attachments: List of attachment dictionaries

        Returns:
            Response with message info

        Raises:
            ElasticEmailError: If the request fails
            ValidationError: If validation fails
        """
        if not to:
            raise ValidationError("to is required")
        if not subject:
            raise ValidationError("subject is required")
        if not body_html:
            raise ValidationError("body_html is required")
        if not from_email:
            raise ValidationError("from_email is required")

        data = {
            "to": to if isinstance(to, str) else ",".join(to),
            "subject": subject,
            "bodyHtml": body_html,
            "from": from_email,
            "fromName": from_name,
        }

        if body_text:
            data["bodyText"] = body_text
        if reply_to:
            data["replyTo"] = reply_to
        if cc:
            data["cc"] = ",".join(cc)
        if bcc:
            data["bcc"] = ",".join(bcc)
        if attachments:
            data["attachments"] = attachments

        response = self._make_request("POST", "email/send", use_alternative_api=True, json_data=data)
        return response

    # ==================== HELPER METHODS ====================

    def get_account_info(self) -> Dict:
        """
        Get account information

        Returns:
            Account data

        Raises:
            ElasticEmailError: If the request fails
        """
        data = self._make_request(
            "GET", "account/load", use_alternative_api=True, params={}
        )
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