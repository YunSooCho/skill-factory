"""
 RD Station API Client
"""

import time
import requests
from typing import Optional, Dict, List, Any, Union
from urllib.parse import urljoin

from .models import Contact, ConversionEvent, ContactListResponse
from .exceptions import (
    RDStationError,
    RateLimitError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
)


class RDStationClient:
    """RD Station API Client (v2/plataforma)"""

    BASE_URL = "https://plugapi.rd.services/platform/api/"
    MARKETING_API_URL = "https://api.rd.services/platform/v1/"
    EVENTS_API_URL = "https://api.rd.services/platform/events/"

    def __init__(
        self,
        access_token: str,
        public_token: Optional[str] = None,
        api_version: str = "v2",
        timeout: int = 30,
    ):
        """
        Initialize RD Station client

        Args:
            access_token: RD Station access token (personal/private)
            public_token: Public token for events (optional)
            api_version: API version to use ('v1' or 'v2')
            timeout: Request timeout in seconds
        """
        self.access_token = access_token
        self.public_token = public_token
        self.api_version = api_version
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
        use_events_endpoint: bool = False,
        use_public_token: bool = False,
    ) -> Union[Dict, List]:
        """
        Make API request with error handling and rate limiting

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: URL query parameters
            data: Form data
            json_data: JSON body data
            use_events_endpoint: Use events API URL
            use_public_token: Use public token instead of access token

        Returns:
            JSON response data

        Raises:
            RDStationError: General API error
            RateLimitError: Rate limit exceeded
            AuthenticationError: Authentication failed
            ResourceNotFoundError: Resource not found
            ValidationError: Validation error
        """
        self._wait_for_rate_limit()

        # Determine base URL
        if use_events_endpoint:
            base_url = self.EVENTS_API_URL
        elif self.api_version == "v1":
            base_url = self.MARKETING_API_URL
        else:
            base_url = self.BASE_URL

        url = urljoin(base_url, endpoint)

        # Set authentication
        token = self.public_token if use_public_token else self.access_token
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

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
            raise RDStationError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise RDStationError(f"Request failed: {str(e)}")

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
            RDStationError: General API error
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

        # RD Station sometimes returns errors in specific format
        if isinstance(data, dict):
            error = data.get("error", data.get("errors"))
            if error:
                error_msg = error if isinstance(error, str) else str(error)
                raise RDStationError(error_msg, response=data)

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
            if isinstance(data.get("errors"), list):
                errors = data["errors"]
                error_message = ", ".join([e.get("message", str(e)) for e in errors])
            raise ValidationError(error_message, response=data)
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            error_message = self._extract_error_message(data)
            raise RateLimitError(error_message, retry_after=retry_after, response=data)
        else:
            error_message = self._extract_error_message(data)
            raise RDStationError(
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
                or data.get("error_message")
                or str(data)
            )
        return str(data)

    # ==================== CONTACT ACTIONS ====================

    def create_contact(
        self,
        email: str,
        name: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        mobile: Optional[str] = None,
        company: Optional[str] = None,
        job_title: Optional[str] = None,
        website: Optional[str] = None,
        bio: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        tags: Optional[List[str]] = None,
        lifecycle_stage: Optional[str] = None,
        lead_source: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Contact:
        """
        Create a new contact

        Args:
            email: Email address (required)
            name: Full name
            first_name: First name
            last_name: Last name
            phone: Phone number
            mobile: Mobile phone
            company: Company name
            job_title: Job title
            website: Website URL
            bio: Bio/description
            city: City
            state: State/Region
            country: Country
            tags: List of tags
            lifecycle_stage: Lifecycle stage
            lead_source: Lead source
            custom_fields: Custom field key-value pairs

        Returns:
            Created Contact object

        Raises:
            RDStationError: If the request fails
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
        if mobile:
            payload["mobile"] = mobile
        if company:
            payload["company"] = company
        if job_title:
            payload["job_title"] = job_title
        if website:
            payload["website"] = website
        if bio:
            payload["bio"] = bio
        if city:
            payload["city"] = city
        if state:
            payload["state"] = state
        if country:
            payload["country"] = country
        if tags:
            payload["tags"] = tags
        if lifecycle_stage:
            payload["lifecycle_stage"] = lifecycle_stage
        if lead_source:
            payload["lead_source"] = lead_source
        if custom_fields:
            payload["custom_fields"] = custom_fields

        data = self._make_request("POST", "contacts", json_data=payload)
        return Contact.from_api_response(data)

    def get_contact(self, email: str) -> Contact:
        """
        Get a contact by email

        Args:
            email: Email address

        Returns:
            Contact object

        Raises:
            RDStationError: If the request fails
            ResourceNotFoundError: If contact not found
        """
        if not email:
            raise ValidationError("email is required")

        data = self._make_request("GET", f"contacts/email:{email}")
        return Contact.from_api_response(data)

    def get_contact_by_uuid(self, uuid: str) -> Contact:
        """
        Get a contact by UUID

        Args:
            uuid: Contact UUID

        Returns:
            Contact object

        Raises:
            RDStationError: If the request fails
            ResourceNotFoundError: If contact not found
        """
        if not uuid:
            raise ValidationError("uuid is required")

        data = self._make_request("GET", f"contacts/{uuid}")
        return Contact.from_api_response(data)

    def update_contact(
        self,
        email: str,
        name: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        mobile: Optional[str] = None,
        company: Optional[str] = None,
        job_title: Optional[str] = None,
        website: Optional[str] = None,
        bio: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        tags: Optional[List[str]] = None,
        lifecycle_stage: Optional[str] = None,
        lead_source: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Contact:
        """
        Update an existing contact

        Args:
            email: Email address
            name: Full name
            first_name: First name
            last_name: Last name
            phone: Phone number
            mobile: Mobile phone
            company: Company name
            job_title: Job title
            website: Website URL
            bio: Bio/description
            city: City
            state: State/Region
            country: Country
            tags: List of tags
            lifecycle_stage: Lifecycle stage
            lead_source: Lead source
            custom_fields: Custom field key-value pairs

        Returns:
            Updated Contact object

        Raises:
            RDStationError: If the request fails
            ResourceNotFoundError: If contact not found
            ValidationError: If validation fails
        """
        if not email:
            raise ValidationError("email is required")

        payload = {}

        if name is not None:
            payload["name"] = name
        if first_name is not None:
            payload["first_name"] = first_name
        if last_name is not None:
            payload["last_name"] = last_name
        if phone is not None:
            payload["phone"] = phone
        if mobile is not None:
            payload["mobile"] = mobile
        if company is not None:
            payload["company"] = company
        if job_title is not None:
            payload["job_title"] = job_title
        if website is not None:
            payload["website"] = website
        if bio is not None:
            payload["bio"] = bio
        if city is not None:
            payload["city"] = city
        if state is not None:
            payload["state"] = state
        if country is not None:
            payload["country"] = country
        if tags is not None:
            payload["tags"] = tags
        if lifecycle_stage is not None:
            payload["lifecycle_stage"] = lifecycle_stage
        if lead_source is not None:
            payload["lead_source"] = lead_source
        if custom_fields is not None:
            payload["custom_fields"] = custom_fields

        data = self._make_request("PATCH", f"contacts/email:{email}", json_data=payload)
        return Contact.from_api_response(data)

    def delete_contact(self, email: str) -> bool:
        """
        Delete a contact

        Args:
            email: Email address

        Returns:
            True if deleted successfully

        Raises:
            RDStationError: If the request fails
            ResourceNotFoundError: If contact not found
        """
        if not email:
            raise ValidationError("email is required")

        self._make_request("DELETE", f"contacts/email:{email}")
        return True

    def list_contacts(
        self,
        page: int = 1,
        per_page: int = 25,
        email: Optional[str] = None,
        lifecycle_stage: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> ContactListResponse:
        """
        List contacts with filtering and pagination

        Args:
            page: Page number
            per_page: Items per page (1-100)
            email: Filter by email
            lifecycle_stage: Filter by lifecycle stage
            tags: Filter by tags

        Returns:
            ContactListResponse with contacts and pagination

        Raises:
            RDStationError: If the request fails
            ValidationError: If parameters are invalid
        """
        if not 1 <= per_page <= 100:
            raise ValidationError("per_page must be between 1 and 100")

        params = {"page": page, "per_page": per_page}
        if email:
            params["email"] = email
        if lifecycle_stage:
            params["lifecycle_stage"] = lifecycle_stage
        if tags:
            params["tags"] = ",".join(tags)

        data = self._make_request("GET", "contacts", params=params)
        return ContactListResponse.from_api_response(data)

    def get_contact_information(self, email: str) -> Contact:
        """
        Get contact information (alias for get_contact)

        Args:
            email: Email address

        Returns:
            Contact object

        Raises:
            RDStationError: If the request fails
            ResourceNotFoundError: If contact not found
        """
        return self.get_contact(email)

    # ==================== TAG ACTIONS ====================

    def add_tag_to_lead(
        self,
        email: str,
        tag: str,
    ) -> Contact:
        """
        Add a tag to a lead

        Args:
            email: Lead email
            tag: Tag to add

        Returns:
            Updated Contact object

        Raises:
            RDStationError: If the request fails
            ResourceNotFoundError: If contact not found
        """
        if not email:
            raise ValidationError("email is required")
        if not tag:
            raise ValidationError("tag is required")

        contact = self.get_contact(email)
        if contact.tags is None:
            contact.tags = []

        if tag not in contact.tags:
            contact.tags.append(tag)

        return self.update_contact(email, tags=contact.tags)

    def remove_tag_from_lead(
        self,
        email: str,
        tag: str,
    ) -> Contact:
        """
        Remove a tag from a lead

        Args:
            email: Lead email
            tag: Tag to remove

        Returns:
            Updated Contact object

        Raises:
            RDStationError: If the request fails
            ResourceNotFoundError: If contact not found
        """
        if not email:
            raise ValidationError("email is required")
        if not tag:
            raise ValidationError("tag is required")

        contact = self.get_contact(email)
        if contact.tags is None:
            contact.tags = []

        if tag in contact.tags:
            contact.tags.remove(tag)

        return self.update_contact(email, tags=contact.tags)

    # ==================== CONVERSION EVENT ACTIONS ====================

    def create_default_conversion_event(
        self,
        event_name: str,
        email: str,
        revenue: Optional[float] = None,
        currency: str = "USD",
        funnel_name: Optional[str] = None,
        url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConversionEvent:
        """
        Create a default conversion event

        Args:
            event_name: Name of the conversion event
            email: Associated email
            revenue: Revenue value (optional)
            currency: Currency code (default USD)
            funnel_name: Funnel name
            url: URL of the conversion
            metadata: Additional metadata

        Returns:
            Created ConversionEvent

        Raises:
            RDStationError: If the request fails
            ValidationError: If validation fails
        """
        if not event_name:
            raise ValidationError("event_name is required")
        if not email:
            raise ValidationError("email is required")

        payload = {
            "event_name": event_name,
            "event_identifier": event_name,
            "channel": "api",
            "email": email,
        }

        if revenue:
            payload["revenue"] = revenue
            payload["currency"] = currency
        if funnel_name:
            payload["funnel_name"] = funnel_name
        if url:
            payload["url"] = url
        if metadata:
            payload["metadata"] = metadata

        data = self._make_request(
            "POST", "events", json_data=payload, use_events_endpoint=True
        )
        return ConversionEvent.from_api_response(data)

    def create_closing_event(
        self,
        email: str,
        value: float,
        deal_name: Optional[str] = None,
        currency: str = "USD",
        closed_at: Optional[str] = None,
        deal_stage: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConversionEvent:
        """
        Create a closing/won deal event

        Args:
            email: Associated email
            value: Deal value
            deal_name: Deal name
            currency: Currency code (default USD)
            closed_at: Deal close date (ISO 8601)
            deal_stage: Deal stage
            metadata: Additional metadata

        Returns:
            Created ConversionEvent

        Raises:
            RDStationError: If the request fails
            ValidationError: If validation fails
        """
        if not email:
            raise ValidationError("email is required")
        if not value:
            raise ValidationError("value is required")

        payload = {
            "event_name": "SALES_WON",
            "event_identifier": "sales_won",
            "channel": "api",
            "email": email,
            "revenue": value,
            "currency": currency,
        }

        if deal_name:
            payload["metadata"] = payload.get("metadata", {})
            payload["metadata"]["deal_name"] = deal_name
        if closed_at:
            payload["conversion_at"] = closed_at
        if deal_stage:
            payload["metadata"] = payload.get("metadata", {})
            payload["metadata"]["deal_stage"] = deal_stage
        if metadata:
            payload["metadata"] = {**(payload.get("metadata", {})), **metadata}

        data = self._make_request(
            "POST", "events", json_data=payload, use_events_endpoint=True
        )
        return ConversionEvent.from_api_response(data)

    def create_call_event(
        self,
        email: str,
        call_type: str,
        outcome: str,
        duration: Optional[int] = None,
        notes: Optional[str] = None,
        call_date: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConversionEvent:
        """
        Create a call event

        Args:
            email: Associated email
            call_type: Type of call ('inbound' or 'outbound')
            outcome: Call outcome
            duration: Call duration in seconds
            notes: Call notes
            call_date: Call date (ISO 8601)
            metadata: Additional metadata

        Returns:
            Created ConversionEvent

        Raises:
            RDStationError: If the request fails
            ValidationError: If validation fails
        """
        if not email:
            raise ValidationError("email is required")
        if not call_type:
            raise ValidationError("call_type is required")
        if not outcome:
            raise ValidationError("outcome is required")

        payload = {
            "event_name": "CALL",
            "event_identifier": "call",
            "channel": "api",
            "email": email,
            "metadata": {
                "call_type": call_type,
                "outcome": outcome,
            },
        }

        if duration:
            payload["metadata"]["duration"] = duration
        if notes:
            payload["metadata"]["notes"] = notes
        if call_date:
            payload["conversion_at"] = call_date
        if metadata:
            payload["metadata"] = {**(payload.get("metadata", {})), **metadata}

        data = self._make_request(
            "POST", "events", json_data=payload, use_events_endpoint=True
        )
        return ConversionEvent.from_api_response(data)

    def create_abandonment_event(
        self,
        email: str,
        abandoned_resource: str,
        abandonment_reason: Optional[str] = None,
        abandoned_at: Optional[str] = None,
        url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConversionEvent:
        """
        Create an abandonment event

        Args:
            email: Associated email
            abandoned_resource: Resource that was abandoned
            abandonment_reason: Reason for abandonment
            abandoned_at: Abandonment date (ISO 8601)
            url: URL of the abandoned resource
            metadata: Additional metadata

        Returns:
            Created ConversionEvent

        Raises:
            RDStationError: If the request fails
            ValidationError: If validation fails
        """
        if not email:
            raise ValidationError("email is required")
        if not abandoned_resource:
            raise ValidationError("abandoned_resource is required")

        payload = {
            "event_name": "ABANDONMENT",
            "event_identifier": "abandonment",
            "channel": "api",
            "email": email,
            "metadata": {
                "abandoned_resource": abandoned_resource,
            },
        }

        if abandonment_reason:
            payload["metadata"]["reason"] = abandonment_reason
        if abandoned_at:
            payload["conversion_at"] = abandoned_at
        if url:
            payload["url"] = url
        if metadata:
            payload["metadata"] = {**(payload.get("metadata", {})), **metadata}

        data = self._make_request(
            "POST", "events", json_data=payload, use_events_endpoint=True
        )
        return ConversionEvent.from_api_response(data)

    def create_chat_starter_event(
        self,
        email: str,
        chat_channel: str,
        conversation_id: Optional[str] = None,
        message: Optional[str] = None,
        started_at: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConversionEvent:
        """
        Create a chat starter event

        Args:
            email: Associated email
            chat_channel: Chat channel (e.g., 'whatsapp', 'telegram', 'website')
            conversation_id: Conversation ID
            message: Initial message
            started_at: Start time (ISO 8601)
            metadata: Additional metadata

        Returns:
            Created ConversionEvent

        Raises:
            RDStationError: If the request fails
            ValidationError: If validation fails
        """
        if not email:
            raise ValidationError("email is required")
        if not chat_channel:
            raise ValidationError("chat_channel is required")

        payload = {
            "event_name": "CHAT_STARTED",
            "event_identifier": "chat_started",
            "channel": "api",
            "email": email,
            "metadata": {
                "chat_channel": chat_channel,
            },
        }

        if conversation_id:
            payload["metadata"]["conversation_id"] = conversation_id
        if message:
            payload["metadata"]["message"] = message
        if started_at:
            payload["conversion_at"] = started_at
        if metadata:
            payload["metadata"] = {**(payload.get("metadata", {})), **metadata}

        data = self._make_request(
            "POST", "events", json_data=payload, use_events_endpoint=True
        )
        return ConversionEvent.from_api_response(data)

    # ==================== HELPER METHODS ====================

    def get_account_info(self) -> Dict:
        """
        Get account information

        Returns:
            Account data

        Raises:
            RDStationError: If the request fails
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