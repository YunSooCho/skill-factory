"""
SendPulse API Client Implementation

Provides methods for:
- Add Email: Add email address
- Delete Email: Remove email
- Search Contact: Find contact
- Add Phone Number: Add SMS contact
- Delete Phone Number: Remove SMS contact
- Change Phone Number: Update phone number
- Get Phone Number: Get phone number details
- Update Variables for Phone Number: Update phone variables
- Change Variables for Phone: Change phone variables
- Add Email to Blacklist: Add email to blacklist
- Add Phone Number to Blacklist: Add phone to blacklist
- Unsubscribe Mailing List: Unsubscribe from list
- Get Email Campaign Statistics: Get campaign stats
"""

import requests
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class RateLimiter:
    max_requests: int = 500
    time_window: int = 60
    requests: list = None

    def __post_init__(self):
        if self.requests is None:
            self.requests = []

    def wait_if_needed(self):
        now = time.time()
        self.requests = [r for r in self.requests if now - r < self.time_window]

        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
                self.requests = []

        self.requests.append(now)


class SendPulseError(Exception):
    pass


class AuthenticationError(SendPulseError):
    pass


class RateLimitError(SendPulseError):
    pass


class InvalidRequestError(SendPulseError):
    pass


class APIError(SendPulseError):
    pass


class SendPulseClient:
    """SendPulse API Client - Email and SMS marketing"""

    BASE_URL = "https://api.sendpulse.com"

    def __init__(self, client_id: str, client_secret: str, timeout: int = 30, max_retries: int = 3):
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limiter = RateLimiter(max_requests=500, time_window=60)
        self.session = requests.Session()
        self.access_token = None
        self._auth()

    def _auth(self):
        """Authenticate and get access token"""
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(f"{self.BASE_URL}/oauth/access_token", data=data, timeout=self.timeout)
        response.raise_for_status()
        self.access_token = response.json()["access_token"]
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, params: dict = None, data: dict = None) -> Dict[str, Any]:
        self.rate_limiter.wait_if_needed()
        url = f"{self.BASE_URL}{endpoint}"
        last_error = None

        for attempt in range(self.max_retries):
            try:
                response = self.session.request(method=method, url=url, params=params, json=data, timeout=self.timeout)

                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key")
                elif response.status_code == 429:
                    raise RateLimitError("Rate limit exceeded")
                elif response.status_code == 400:
                    error_data = response.json() if response.content else {}
                    raise InvalidRequestError(f"Invalid request: {error_data.get('message', 'Unknown error')}")
                elif response.status_code >= 500:
                    raise APIError(f"Server error: {response.status_code}")

                response.raise_for_status()
                return response.json()

            except requests.Timeout:
                last_error = f"Request timeout after {self.timeout} seconds"
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise APIError(last_error)
            except requests.RequestException as e:
                last_error = str(e)
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise APIError(f"Request failed: {last_error}")

        raise APIError(f"Max retries exceeded: {last_error}")

    def add_email(self, books: list, emails: list) -> Dict[str, Any]:
        """Add emails to address books"""
        if not books or not emails:
            raise InvalidRequestError("books and emails are required")

        data = [
            {
                "book_id": book,
                "emails": emails
            }
            for book in books
        ]
        return self._make_request("POST", "/emails", data=data)

    def delete_email(self, email: str, book_id: int) -> Dict[str, Any]:
        """Delete email from address book"""
        if not email:
            raise InvalidRequestError("email is required")

        data = {"email": email, "book_id": book_id}
        return self._make_request("DELETE", "/emails", data=data)

    def search_contact(self, email: str) -> Dict[str, Any]:
        """Search for a contact by email"""
        if not email:
            raise InvalidRequestError("email is required")

        return self._make_request("GET", f"/emails/{email}")

    def add_phone_number(self, phone: str, book_id: int, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add phone number to address book"""
        if not phone:
            raise InvalidRequestError("phone is required")

        data = {
            "phone": phone,
            "book_id": book_id
        }

        if variables:
            data["variables"] = variables

        return self._make_request("POST", "/sms/numbers", data=data)

    def delete_phone_number(self, phone: str, book_id: int) -> Dict[str, Any]:
        """Delete phone number from address book"""
        if not phone:
            raise InvalidRequestError("phone is required")

        data = {"phone": phone, "book_id": book_id}
        return self._make_request("DELETE", "/sms/numbers", data=data)

    def change_phone_number(self, phone: str, new_phone: str, book_id: int) -> Dict[str, Any]:
        """Change phone number in address book"""
        if not phone or not new_phone:
            raise InvalidRequestError("phone and new_phone are required")

        data = {
            "phone": phone,
            "new_phone": new_phone,
            "book_id": book_id
        }
        return self._make_request("PUT", "/sms/numbers", data=data)

    def get_phone_number(self, phone: str, book_id: int) -> Dict[str, Any]:
        """Get phone number details"""
        if not phone:
            raise InvalidRequestError("phone is required")

        return self._make_request("GET", f"/sms/numbers/{phone}", params={"book_id": book_id})

    def update_variables_for_phone_number(self, phone: str, book_id: int, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Update variables for phone number"""
        if not phone or not variables:
            raise InvalidRequestError("phone and variables are required")

        data = {
            "phone": phone,
            "book_id": book_id,
            "variables": variables
        }
        return self._make_request("PUT", "/sms/numbers/variables", data=data)

    def change_variables_for_phone(self, phone: str, book_id: int, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Change variables for phone"""
        return self.update_variables_for_phone_number(phone, book_id, variables)

    def add_email_to_blacklist(self, email: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Add email to blacklist"""
        if not email:
            raise InvalidRequestError("email is required")

        data = {"email": email}
        if reason:
            data["reason"] = reason

        return self._make_request("POST", "/emails/blacklist", data=data)

    def add_phone_number_to_blacklist(self, phone: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Add phone number to blacklist"""
        if not phone:
            raise InvalidRequestError("phone is required")

        data = {"phone": phone}
        if reason:
            data["reason"] = reason

        return self._make_request("POST", "/sms/blacklist", data=data)

    def unsubscribe_mailing_list(self, emails: list, book_id: int) -> Dict[str, Any]:
        """Unsubscribe emails from mailing list"""
        if not emails:
            raise InvalidRequestError("emails list is required")

        data = {
            "emails": emails,
            "book_id": book_id
        }
        return self._make_request("POST", "/emails/unsubscribe", data=data)

    def get_email_campaign_statistics(self, campaign_id: int) -> Dict[str, Any]:
        """Get email campaign statistics"""
        if not campaign_id:
            raise InvalidRequestError("campaign_id is required")

        return self._make_request("GET", f"/campaigns/{campaign_id}/statistics")

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()