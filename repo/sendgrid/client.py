"""
SendGrid API Client Implementation

Provides methods for:
- Send Email: Send emails
- Send Email with Attachment: Send emails with file attachments
- Create Contact List: Create a contact list
- Add Contact to List: Add a contact to a list
- Search Contact: Find contact information
- Delete Contact: Remove a contact
- Get Bounce List: Get list of bounced emails
"""

import requests
import time
import mimetypes
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class RateLimiter:
    max_requests: int = 600
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


class SendGridError(Exception):
    pass


class AuthenticationError(SendGridError):
    pass


class RateLimitError(SendGridError):
    pass


class InvalidRequestError(SendGridError):
    pass


class APIError(SendGridError):
    pass


class SendGridClient:
    """SendGrid API Client - Email service"""

    BASE_URL = "https://api.sendgrid.com/v3"

    def __init__(self, api_key: str, timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limiter = RateLimiter(max_requests=600, time_window=60)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, params: dict = None, data: dict = None, headers: dict = None) -> Dict[str, Any]:
        self.rate_limiter.wait_if_needed()
        url = f"{self.BASE_URL}{endpoint}"
        last_error = None

        req_headers = self.session.headers.copy()
        if headers:
            req_headers.update(headers)

        for attempt in range(self.max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=req_headers,
                    timeout=self.timeout
                )

                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key")
                elif response.status_code == 429:
                    raise RateLimitError("Rate limit exceeded")
                elif response.status_code == 400:
                    error_data = response.json() if response.content else {}
                    raise InvalidRequestError(f"Invalid request: {error_data.get('errors', 'Unknown error')}")
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

    def send_email(
        self,
        from_email: str,
        to_emails: List[str],
        subject: str,
        content: str,
        content_type: str = "text/plain",
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None,
        reply_to: Optional[str] = None,
        categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send an email"""
        if not from_email or not to_emails or not subject:
            raise InvalidRequestError("from_email, to_emails, and subject are required")

        personalizations = [{"to": [{"email": email} for email in to_emails]}]

        if cc_emails:
            personalizations[0]["cc"] = [{"email": email} for email in cc_emails]
        if bcc_emails:
            personalizations[0]["bcc"] = [{"email": email} for email in bcc_emails]

        data = {
            "personalizations": personalizations,
            "from": {"email": from_email},
            "subject": subject,
            "content": [{"type": content_type, "value": content}]
        }

        if reply_to:
            data["reply_to"] = {"email": reply_to}
        if categories:
            data["categories"] = categories

        return self._make_request("POST", "/mail/send", data=data)

    def send_email_with_attachment(
        self,
        from_email: str,
        to_emails: List[str],
        subject: str,
        content: str,
        attachments: List[Dict[str, str]],
        content_type: str = "text/plain",
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send an email with file attachments"""
        if not attachments:
            raise InvalidRequestError("attachments list is required")

        attachment_data = []
        for attachment in attachments:
            content_bytes = attachment.get("content", "")
            if len(content_bytes) > 1024 * 25:
                raise InvalidRequestError("Attachment size exceeds 25MB limit")

            attachment_data.append({
                "content": content_bytes,
                "type": attachment.get("content_type", "application/octet-stream"),
                "filename": attachment.get("filename", "attachment"),
                "disposition": "attachment"
            })

        return self.send_email(
            from_email=from_email,
            to_emails=to_emails,
            subject=subject,
            content=content,
            content_type=content_type,
            cc_emails=cc_emails,
            bcc_emails=bcc_emails
        )

    def create_contact_list(self, name: str) -> Dict[str, Any]:
        """Create a contact list"""
        if not name:
            raise InvalidRequestError("name is required")

        data = {"name": name}
        return self._make_request("POST", "/marketing/lists", data=data)

    def add_contact_to_list(
        self,
        list_id: str,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add a contact to a list"""
        if not list_id or not email:
            raise InvalidRequestError("list_id and email are required")

        data = {
            "list_ids": [list_id],
            "contacts": [{
                "email": email,
                "first_name": first_name or "",
                "last_name": last_name or ""
            }]
        }

        if custom_fields:
            data["contacts"][0]["custom_fields"] = custom_fields

        return self._make_request("PUT", "/marketing/contacts", data=data)

    def search_contact(self, email: str) -> Dict[str, Any]:
        """Search for a contact by email"""
        if not email:
            raise InvalidRequestError("email is required")

        data = {"query": f"email = '{email}'"}
        return self._make_request("POST", "/marketing/contacts/search", data=data)

    def delete_contact(self, email: str) -> Dict[str, Any]:
        """Delete a contact by email"""
        if not email:
            raise InvalidRequestError("email is required")

        first_response = self.search_contact(email)
        contact_ids = first_response.get("result", [])

        if not contact_ids:
            raise InvalidRequestError("Contact not found")

        ids = [c.get("id") for c in contact_ids]
        return self._make_request("DELETE", "/marketing/contacts", data={"ids": ids})

    def get_bounce_list(self, start_time: Optional[str] = None, end_time: Optional[str] = None) -> Dict[str, Any]:
        """Get list of bounced emails"""
        data = {}
        if start_time:
            data["start_time"] = start_time
        if end_time:
            data["end_time"] = end_time

        return self._make_request("GET", "/suppression/bounces", params=data)

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()