"""
 CloudContact AI API Client
"""

import time
import requests
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin

from .models import Contact, SMSMessage, Campaign, ContactListResponse, SMSListResponse
from .exceptions import (
    CloudContactAIError,
    RateLimitError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
)


class CloudContactAIClient:
    """CloudContact AI API Client"""

    BASE_URL = "https://api.cloudcontact.ai/api/v1/"
    API_VERSION = "v1"

    def __init__(
        self,
        api_key: str,
        account_id: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize CloudContact AI client

        Args:
            api_key: CloudContact AI API key
            account_id: Account ID (optional for some endpoints)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.account_id = account_id
        self.timeout = timeout
        self.session = requests.Session()

        # Rate limiting
        self._last_request_time = 0
        self._min_request_interval = 0.05  # 50ms between requests
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
            CloudContactAIError: General API error
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

        # Add account_id to params if not in endpoint and not in JSON
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
            raise CloudContactAIError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise CloudContactAIError(f"Request failed: {str(e)}")

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
            CloudContactAIError: General API error
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
            raise CloudContactAIError(error_message, status_code=response.status_code, response=data)

    # ==================== CONTACT ACTIONS ====================

    def create_contact(
        self,
        phone: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        name: Optional[str] = None,
        company: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        opted_in: bool = False,
    ) -> Contact:
        """
        Create a new contact

        Args:
            phone: Phone number (required)
            email: Email address
            first_name: First name
            last_name: Last name
            name: Full name (overwrites first_name/last_name)
            company: Company name
            tags: List of tags
            custom_fields: Custom field key-value pairs
            opted_in: Whether the contact has opted in to SMS

        Returns:
            Created Contact object

        Raises:
            CloudContactAIError: If the request fails
            ValidationError: If validation fails
        """
        if not phone:
            raise ValidationError("phone is required")

        payload = {"phone": phone}

        if name:
            payload["name"] = name
        else:
            if first_name:
                payload["first_name"] = first_name
            if last_name:
                payload["last_name"] = last_name
        if email:
            payload["email"] = email
        if company:
            payload["company"] = company
        if tags:
            payload["tags"] = tags
        if custom_fields:
            payload["custom_fields"] = custom_fields
        payload["opted_in"] = opted_in

        data = self._make_request("POST", "contacts", json_data=payload)
        return Contact.from_api_response(data)

    def get_contact(self, contact_id: str) -> Contact:
        """
        Get a specific contact by ID

        Args:
            contact_id: The contact ID

        Returns:
            Contact object

        Raises:
            CloudContactAIError: If the request fails
            ResourceNotFoundError: If contact not found
        """
        data = self._make_request("GET", f"contacts/{contact_id}")
        return Contact.from_api_response(data)

    def update_contact(
        self,
        contact_id: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        name: Optional[str] = None,
        company: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        opted_in: Optional[bool] = None,
    ) -> Contact:
        """
        Update an existing contact

        Args:
            contact_id: The contact ID
            phone: Phone number
            email: Email address
            first_name: First name
            last_name: Last name
            name: Full name
            company: Company name
            tags: List of tags
            custom_fields: Custom field key-value pairs
            opted_in: Whether the contact has opted in to SMS

        Returns:
            Updated Contact object

        Raises:
            CloudContactAIError: If the request fails
            ResourceNotFoundError: If contact not found
            ValidationError: If validation fails
        """
        payload = {}

        if phone:
            payload["phone"] = phone
        if email is not None:
            payload["email"] = email
        if name is not None:
            payload["name"] = name
        if first_name is not None:
            payload["first_name"] = first_name
        if last_name is not None:
            payload["last_name"] = last_name
        if company is not None:
            payload["company"] = company
        if tags is not None:
            payload["tags"] = tags
        if custom_fields is not None:
            payload["custom_fields"] = custom_fields
        if opted_in is not None:
            payload["opted_in"] = opted_in

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
            CloudContactAIError: If the request fails
            ResourceNotFoundError: If contact not found
        """
        self._make_request("DELETE", f"contacts/{contact_id}")
        return True

    def search_contacts(
        self,
        query: str,
        page: int = 1,
        per_page: int = 25,
        search_type: str = "all",
    ) -> ContactListResponse:
        """
        Search contacts by query

        Args:
            query: Search query (phone, email, name)
            page: Page number
            per_page: Items per page (1-100)
            search_type: Type of search ('all', 'phone', 'email', 'name')

        Returns:
            ContactListResponse with contacts and pagination

        Raises:
            CloudContactAIError: If the request fails
            ValidationError: If parameters are invalid
        """
        if not query:
            raise ValidationError("query is required")

        if not 1 <= per_page <= 100:
            raise ValidationError("per_page must be between 1 and 100")

        if search_type not in ["all", "phone", "email", "name"]:
            raise ValidationError("search_type must be one of: all, phone, email, name")

        params = {
            "query": query,
            "page": page,
            "per_page": per_page,
            "search_type": search_type,
        }

        data = self._make_request("GET", "contacts/search", params=params)
        return ContactListResponse.from_api_response(data)

    def list_contacts(
        self,
        page: int = 1,
        per_page: int = 25,
        tags: Optional[List[str]] = None,
        opted_in: Optional[bool] = None,
    ) -> ContactListResponse:
        """
        List contacts with filtering and pagination

        Args:
            page: Page number
            per_page: Items per page (1-100)
            tags: Filter by tags
            opted_in: Filter by opted-in status

        Returns:
            ContactListResponse with contacts and pagination

        Raises:
            CloudContactAIError: If the request fails
            ValidationError: If parameters are invalid
        """
        if not 1 <= per_page <= 100:
            raise ValidationError("per_page must be between 1 and 100")

        params = {"page": page, "per_page": per_page}
        if tags:
            params["tags"] = ",".join(tags)
        if opted_in is not None:
            params["opted_in"] = str(opted_in).lower()

        data = self._make_request("GET", "contacts", params=params)
        return ContactListResponse.from_api_response(data)

    # ==================== SMS CAMPAIGN ACTIONS ====================

    def send_sms_campaign(
        self,
        phone: str,
        message: str,
        campaign_name: Optional[str] = None,
        scheduled_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send SMS message (create campaign)

        Args:
            phone: Recipient phone number
            message: SMS message content
            campaign_name: Optional campaign name
            scheduled_at: Optional scheduled time (ISO 8601 format)

        Returns:
            Response with campaign/message info

        Raises:
            CloudContactAIError: If the request fails
            ValidationError: If validation fails
        """
        if not phone:
            raise ValidationError("phone is required")
        if not message:
            raise ValidationError("message is required")

        payload = {"phone": phone, "message": message}

        if campaign_name:
            payload["campaign_name"] = campaign_name
        if scheduled_at:
            payload["scheduled_at"] = scheduled_at

        data = self._make_request("POST", "sms/send", json_data=payload)
        return data

    def send_bulk_sms_campaign(
        self,
        phones: List[str],
        message: str,
        campaign_name: str,
        scheduled_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send bulk SMS campaign to multiple recipients

        Args:
            phones: List of recipient phone numbers
            message: SMS message content
            campaign_name: Campaign name
            scheduled_at: Optional scheduled time (ISO 8601 format)

        Returns:
            Response with campaign info

        Raises:
            CloudContactAIError: If the request fails
            ValidationError: If validation fails
        """
        if not phones:
            raise ValidationError("phones list cannot be empty")
        if not message:
            raise ValidationError("message is required")
        if not campaign_name:
            raise ValidationError("campaign_name is required")

        payload = {"phones": phones, "message": message, "campaign_name": campaign_name}

        if scheduled_at:
            payload["scheduled_at"] = scheduled_at

        data = self._make_request("POST", "sms/bulk", json_data=payload)
        return data

    def get_sent_sms_messages(
        self,
        campaign_id: Optional[str] = None,
        phone: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        per_page: int = 25,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> SMSListResponse:
        """
        Get sent SMS messages with filtering

        Args:
            campaign_id: Filter by campaign ID
            phone: Filter by phone number
            status: Filter by status ('sent', 'delivered', 'failed', 'pending')
            page: Page number
            per_page: Items per page (1-100)
            from_date: Filter from date (ISO 8601 format)
            to_date: Filter to date (ISO 8601 format)

        Returns:
            SMSListResponse with messages and pagination

        Raises:
            CloudContactAIError: If the request fails
            ValidationError: If parameters are invalid
        """
        if not 1 <= per_page <= 100:
            raise ValidationError("per_page must be between 1 and 100")

        params = {"page": page, "per_page": per_page}
        if campaign_id:
            params["campaign_id"] = campaign_id
        if phone:
            params["phone"] = phone
        if status:
            if status not in ["sent", "delivered", "failed", "pending"]:
                raise ValidationError(
                    "status must be one of: sent, delivered, failed, pending"
                )
            params["status"] = status
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        data = self._make_request("GET", "sms", params=params)
        return SMSListResponse.from_api_response(data)

    def get_sms_message(self, message_id: str) -> SMSMessage:
        """
        Get a specific SMS message by ID

        Args:
            message_id: The message ID

        Returns:
            SMSMessage object

        Raises:
            CloudContactAIError: If the request fails
            ResourceNotFoundError: If message not found
        """
        data = self._make_request("GET", f"sms/{message_id}")
        return SMSMessage.from_api_response(data)

    # ==================== CAMPAIGN ACTIONS ====================

    def get_campaign(self, campaign_id: str) -> Campaign:
        """
        Get a campaign by ID

        Args:
            campaign_id: The campaign ID

        Returns:
            Campaign object

        Raises:
            CloudContactAIError: If the request fails
            ResourceNotFoundError: If campaign not found
        """
        data = self._make_request("GET", f"campaigns/{campaign_id}")
        return Campaign.from_api_response(data)

    def list_campaigns(
        self,
        page: int = 1,
        per_page: int = 25,
        status: Optional[str] = None,
    ) -> List[Campaign]:
        """
        List campaigns

        Args:
            page: Page number
            per_page: Items per page (1-100)
            status: Filter by status

        Returns:
            List of Campaign objects

        Raises:
            CloudContactAIError: If the request fails
            ValidationError: If parameters are invalid
        """
        if not 1 <= per_page <= 100:
            raise ValidationError("per_page must be between 1 and 100")

        params = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status

        data = self._make_request("GET", "campaigns", params=params)

        campaigns = []
        if isinstance(data, list):
            campaigns = [Campaign.from_api_response(c) for c in data]
        elif "items" in data:
            campaigns = [Campaign.from_api_response(c) for c in data["items"]]
        elif "campaigns" in data:
            campaigns = [Campaign.from_api_response(c) for c in data["campaigns"]]
        elif isinstance(data, dict) and "id" in data:
            campaigns = [Campaign.from_api_response(data)]

        return campaigns

    # ==================== HELPER METHODS ====================

    def get_account_info(self) -> Dict:
        """
        Get account information

        Returns:
            Account data

        Raises:
            CloudContactAIError: If the request fails
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