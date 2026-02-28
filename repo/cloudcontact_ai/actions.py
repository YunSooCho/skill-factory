"""
CloudContact AI API Actions implementation.
"""
import requests
import time
from typing import Optional, List, Dict, Any
from .models import Contact, SMSMessage, Campaign, ContactSearchResult
from .exceptions import (
    CloudContactAIError,
    CloudContactAIAuthenticationError,
    CloudContactAIRateLimitError,
    CloudContactAINotFoundError,
    CloudContactAIValidationError,
)


class CloudContactAIActions:
    """CloudContact AI API actions for Yoom integration."""

    BASE_URL = "https://api.cloudcontactai.com/v1"

    def __init__(self, client_id: str, api_key: str, timeout: int = 30):
        """
        Initialize CloudContact AI API client.

        Args:
            client_id: Client ID for authentication
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.client_id = client_id
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "X-Client-Id": client_id,
                "X-API-Key": api_key,
            }
        )

        # Rate limiting state
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
        self.rate_limit_remaining = 1000

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        retry_on_rate_limit: bool = True,
    ) -> Dict[str, Any]:
        """
        Make authenticated request to CloudContact AI API with rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data
            retry_on_rate_limit: Whether to retry on 429 errors

        Returns:
            Response JSON as dict

        Raises:
            CloudContactAIError: For API errors
            CloudContactAIAuthenticationError: For auth errors
            CloudContactAIRateLimitError: For rate limit errors
            CloudContactAINotFoundError: For 404 errors
        """
        # Rate limiting
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)

        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=self.timeout,
            )
            self.last_request_time = time.time()

            # Update rate limit info from headers
            self.rate_limit_remaining = int(
                response.headers.get("X-RateLimit-Remaining", self.rate_limit_remaining)
            )

            # Handle error responses
            if response.status_code == 401:
                error_data = response.json() if response.text else {}
                raise CloudContactAIAuthenticationError(
                    message=error_data.get("message", "Authentication failed"),
                    status_code=401,
                    response=error_data,
                )
            elif response.status_code == 404:
                raise CloudContactAINotFoundError(
                    message="Resource not found",
                    status_code=404,
                )
            elif response.status_code == 429:
                if retry_on_rate_limit:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    return self._make_request(
                        method, endpoint, params, data, retry_on_rate_limit=False
                    )
                raise CloudContactAIRateLimitError(
                    message="Rate limit exceeded",
                    status_code=429,
                )
            elif response.status_code >= 400:
                try:
                    error_data = response.json() if response.text else {}
                    error_msg = error_data.get(
                        "message", error_data.get("error", f"API Error: {response.status_code}")
                    )
                except:
                    error_msg = f"API Error: {response.status_code}"
                raise CloudContactAIError(
                    message=error_msg,
                    status_code=response.status_code,
                    response=error_data if response.text else {},
                )

            return response.json()

        except requests.Timeout:
            raise CloudContactAIError(f"Request timeout after {self.timeout} seconds")
        except requests.RequestException as e:
            raise CloudContactAIError(f"Request failed: {str(e)}")

    # ==================== API Actions ====================

    def create_contact(
        self,
        first_name: str,
        last_name: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        external_id: Optional[str] = None,
        add_to_lists: Optional[List[str]] = None,
    ) -> Contact:
        """
        Create a new contact in CloudContact AI.

        Args:
            first_name: Contact's first name
            last_name: Contact's last name
            phone: Contact's phone number (E.164 format recommended)
            email: Contact's email address
            external_id: External identifier for the contact
            add_to_lists: List of list IDs to add contact to

        Returns:
            Created Contact object

        Raises:
            CloudContactAIValidationError: If required fields missing
            CloudContactAIError: For API errors
        """
        if not first_name or not last_name:
            raise CloudContactAIValidationError("first_name and last_name are required")

        data = {
            "first_name": first_name,
            "last_name": last_name,
        }

        if phone:
            data["phone"] = phone
        if email:
            data["email"] = email
        if external_id:
            data["external_id"] = external_id
        if add_to_lists:
            data["lists"] = add_to_lists

        response = self._make_request("POST", "/contacts", data=data)
        return Contact.from_dict(response)

    def send_sms_by_campaign(
        self,
        accounts: List[Dict[str, str]],
        message: str,
        title: str,
        scheduled_timestamp: Optional[str] = None,
        scheduled_timezone: Optional[str] = None,
        add_to_list: str = "noList",
        contact_input: str = "accounts",
        from_type: str = "single",
        senders: Optional[List[Dict[str, str]]] = None,
    ) -> Campaign:
        """
        Send SMS messages to a list of contacts via campaign.

        Args:
            accounts: List of contact dicts with first_name, last_name, phone
            message: SMS message content (supports ${FirstName}, ${LastName} variables)
            title: Campaign title
            scheduled_timestamp: ISO 8601 format timestamp for scheduled sending
            scheduled_timezone: Timezone for scheduled sending (e.g., 'America/New_York')
            add_to_list: List ID to add contacts to ('noList' to skip)
            contact_input: Contact input type ('accounts', 'list', 'upload')
            from_type: From type ('single', 'pool', 'number')
            senders: List of sender configurations

        Returns:
            Created Campaign object with campaign ID

        Raises:
            CloudContactAIValidationError: If required fields missing
            CloudContactAIError: For API errors
        """
        if not accounts or not message or not title:
            raise CloudContactAIValidationError(
                "accounts, message, and title are required"
            )

        data = {
            "accounts": accounts,
            "message": message,
            "title": title,
            "campaign_type": "SMS",
            "add_to_list": add_to_list,
            "contact_input": contact_input,
            "from_type": from_type,
        }

        if scheduled_timestamp:
            data["scheduled_timestamp"] = scheduled_timestamp
        if scheduled_timezone:
            data["scheduled_timezone"] = scheduled_timezone
        if senders:
            data["senders"] = senders

        response = self._make_request("POST", "/campaigns/sms", data=data)
        return Campaign.from_dict(response)

    def get_sent_sms_messages(
        self,
        campaign_id: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> List[SMSMessage]:
        """
        Get sent SMS messages with optional filtering.

        Args:
            campaign_id: Filter by campaign ID
            status: Filter by status (e.g., 'SENT', 'FAILED', 'PENDING')
            start_date: Start date filter (ISO 8601 format)
            end_date: End date filter (ISO 8601 format)
            page: Page number for pagination
            page_size: Number of messages per page

        Returns:
            List of SMSMessage objects

        Raises:
            CloudContactAIError: For API errors
        """
        params = {"page": page, "page_size": page_size}

        if campaign_id:
            params["campaign_id"] = campaign_id
        if status:
            params["status"] = status
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        response = self._make_request("GET", "/messages/sms", params=params)

        messages = []
        if "messages" in response:
            messages = [SMSMessage.from_dict(m) for m in response["messages"]]
        elif "items" in response:
            messages = [SMSMessage.from_dict(m) for m in response["items"]]

        return messages

    def search_contacts(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        external_id: Optional[str] = None,
        list_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> ContactSearchResult:
        """
        Search for contacts with various filters.

        Args:
            first_name: Filter by first name (partial match)
            last_name: Filter by last name (partial match)
            phone: Filter by phone number
            email: Filter by email address
            external_id: Filter by external ID
            list_id: Filter by list ID
            start_date: Filter contacts created after this date
            end_date: Filter contacts created before this date
            page: Page number for pagination
            page_size: Number of contacts per page

        Returns:
            ContactSearchResult with list of contacts and metadata

        Raises:
            CloudContactAIError: For API errors
        """
        params = {"page": page, "page_size": page_size}

        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name
        if phone:
            params["phone"] = phone
        if email:
            params["email"] = email
        if external_id:
            params["external_id"] = external_id
        if list_id:
            params["list_id"] = list_id
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        response = self._make_request("GET", "/contacts/search", params=params)
        return ContactSearchResult.from_dict(response)

    def close(self):
        """Close the session."""
        self.session.close()