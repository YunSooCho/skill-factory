"""
Nimble API Client
API Documentation: https://developer.nimble.com/api/
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime
import json
import hmac
import hashlib


class NimbleAPIError(Exception):
    """Custom exception for Nimble API errors."""
    pass


class NimbleClient:
    """Client for Nimble API - CRM and contact management."""

    def __init__(self, api_key: str, base_url: str = "https://api.nimble.com/api/v1"):
        """
        Initialize Nimble API client.

        Args:
            api_key: Your Nimble API key
            base_url: API base URL (default: https://api.nimble.com/api/v1)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make API request with error handling.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request arguments

        Returns:
            Response data
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()

            data = response.json()
            return {
                "status": "success",
                "data": data,
                "status_code": response.status_code
            }

        except requests.exceptions.HTTPError as e:
            error_data = self._parse_error(response)
            raise NimbleAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise NimbleAPIError(f"Request failed: {str(e)}")
        except json.JSONDecodeError:
            raise NimbleAPIError("Invalid JSON response")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"message": response.text}

    def create_contact(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new contact.

        Args:
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number
            company: Company name
            title: Job title
            tags: List of tags
            custom_fields: Custom field values

        Returns:
            Created contact data
        """
        data = {
            "fields": {
                "first name": [{"value": first_name}],
                "last name": [{"value": last_name}],
                "email": [{"value": email, "modifier": "personal"}],
                "phone": [{"value": phone, "modifier": "mobile"}],
                "company name": [{"value": company}],
                "job title": [{"value": title}]
            },
            "tags": tags or []
        }

        if custom_fields:
            data["custom_fields"] = custom_fields

        return self._make_request("POST", "/contact", json=data)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Get contact details by ID.

        Args:
            contact_id: Contact ID

        Returns:
            Contact data
        """
        return self._make_request("GET", f"/contact/{contact_id}")

    def update_contact(
        self,
        contact_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update contact information.

        Args:
            contact_id: Contact ID
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number
            company: Company name
            title: Job title
            tags: List of tags
            custom_fields: Custom field values

        Returns:
            Updated contact data
        """
        data = {
            "fields": {
                "first name": [{"value": first_name}],
                "last name": [{"value": last_name}],
                "email": [{"value": email, "modifier": "personal"}],
                "phone": [{"value": phone, "modifier": "mobile"}],
                "company name": [{"value": company}],
                "job title": [{"value": title}]
            }
        }

        if tags is not None:
            data["tags"] = tags
        if custom_fields:
            data["custom_fields"] = custom_fields

        return self._make_request("PUT", f"/contact/{contact_id}", json=data)

    def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Delete a contact.

        Args:
            contact_id: Contact ID

        Returns:
            Deletion result
        """
        return self._make_request("DELETE", f"/contact/{contact_id}")

    def search_contact(
        self,
        query: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for contacts.

        Args:
            query: General search query
            email: Email address filter
            phone: Phone number filter
            company: Company name filter
            tags: Filter by tags
            limit: Max results
            offset: Pagination offset

        Returns:
            List of matching contacts
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        if query:
            params["query"] = query
        if email:
            params["email"] = email
        if phone:
            params["phone"] = phone
        if company:
            params["company"] = company
        if tags:
            params["tags"] = ",".join(tags)

        return self._make_request("GET", "/contacts", params=params)

    def assign_tag_to_contact(self, contact_id: str, tags: List[str]) -> Dict[str, Any]:
        """
        Assign tags to a contact.

        Args:
            contact_id: Contact ID
            tags: List of tags to assign

        Returns:
            Updated contact data
        """
        data = {"tags": tags}
        return self._make_request("POST", f"/contact/{contact_id}/tags", json=data)

    def create_contact_note(
        self,
        contact_id: str,
        note: str,
        note_type: Optional[str] = "general"
    ) -> Dict[str, Any]:
        """
        Create a note for a contact.

        Args:
            contact_id: Contact ID
            note: Note content
            note_type: Type of note (general, call, meeting, etc.)

        Returns:
            Created note data
        """
        data = {
            "note": note,
            "note_type": note_type,
            "created": datetime.now().isoformat()
        }
        return self._make_request("POST", f"/contact/{contact_id}/notes", json=data)

    def update_contact_note(
        self,
        contact_id: str,
        note_id: str,
        note: str,
        note_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a contact note.

        Args:
            contact_id: Contact ID
            note_id: Note ID
            note: Updated note content
            note_type: Type of note

        Returns:
            Updated note data
        """
        data = {"note": note}
        if note_type:
            data["note_type"] = note_type

        return self._make_request("PUT", f"/contact/{contact_id}/notes/{note_id}", json=data)

    def search_contact_notes(
        self,
        contact_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get notes for a contact.

        Args:
            contact_id: Contact ID
            limit: Max results
            offset: Pagination offset

        Returns:
            List of notes
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        return self._make_request("GET", f"/contact/{contact_id}/notes", params=params)

    def create_deal(
        self,
        title: str,
        value: float,
        currency: str = "USD",
        probability: Optional[int] = None,
        expected_close_date: Optional[str] = None,
        contact_id: Optional[str] = None,
        notes: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new deal.

        Args:
            title: Deal title
            value: Deal value
            currency: Currency code (default: USD)
            probability: Close probability (0-100)
            expected_close_date: Expected close date (ISO format)
            contact_id: Associated contact ID
            notes: Deal notes
            custom_fields: Custom field values

        Returns:
            Created deal data
        """
        data = {
            "title": title,
            "value": value,
            "currency": currency
        }

        if probability is not None:
            data["probability"] = probability
        if expected_close_date:
            data["expected_close_date"] = expected_close_date
        if contact_id:
            data["contact_id"] = contact_id
        if notes:
            data["notes"] = notes
        if custom_fields:
            data["custom_fields"] = custom_fields

        return self._make_request("POST", "/deal", json=data)

    def get_deal(self, deal_id: str) -> Dict[str, Any]:
        """
        Get deal details.

        Args:
            deal_id: Deal ID

        Returns:
            Deal data
        """
        return self._make_request("GET", f"/deal/{deal_id}")

    def update_deal(
        self,
        deal_id: str,
        title: Optional[str] = None,
        value: Optional[float] = None,
        currency: Optional[str] = None,
        probability: Optional[int] = None,
        expected_close_date: Optional[str] = None,
        status: Optional[str] = None,
        notes: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update deal information.

        Args:
            deal_id: Deal ID
            title: Deal title
            value: Deal value
            currency: Currency code
            probability: Close probability (0-100)
            expected_close_date: Expected close date
            status: Deal status
            notes: Deal notes
            custom_fields: Custom field values

        Returns:
            Updated deal data
        """
        data = {}
        if title:
            data["title"] = title
        if value is not None:
            data["value"] = value
        if currency:
            data["currency"] = currency
        if probability is not None:
            data["probability"] = probability
        if expected_close_date:
            data["expected_close_date"] = expected_close_date
        if status:
            data["status"] = status
        if notes:
            data["notes"] = notes
        if custom_fields:
            data["custom_fields"] = custom_fields

        return self._make_request("PUT", f"/deal/{deal_id}", json=data)

    def delete_deal(self, deal_id: str) -> Dict[str, Any]:
        """
        Delete a deal.

        Args:
            deal_id: Deal ID

        Returns:
            Deletion result
        """
        return self._make_request("DELETE", f"/deal/{deal_id}")

    def list_deals(
        self,
        status: Optional[str] = None,
        contact_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List deals.

        Args:
            status: Filter by status
            contact_id: Filter by contact ID
            limit: Max results
            offset: Pagination offset

        Returns:
            List of deals
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        if status:
            params["status"] = status
        if contact_id:
            params["contact_id"] = contact_id

        return self._make_request("GET", "/deals", params=params)

    def create_draft_message(
        self,
        contact_id: str,
        subject: str,
        body: str,
        message_type: str = "email"
    ) -> Dict[str, Any]:
        """
        Create a draft message.

        Args:
            contact_id: Contact ID
            subject: Message subject
            body: Message body
            message_type: Message type (email, etc.)

        Returns:
            Created draft data
        """
        data = {
            "contact_id": contact_id,
            "subject": subject,
            "body": body,
            "message_type": message_type,
            "created": datetime.now().isoformat()
        }
        return self._make_request("POST", "/message/draft", json=data)

    def search_draft_messages(
        self,
        contact_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search draft messages.

        Args:
            contact_id: Filter by contact ID
            limit: Max results
            offset: Pagination offset

        Returns:
            List of draft messages
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        if contact_id:
            params["contact_id"] = contact_id

        return self._make_request("GET", "/message/drafts", params=params)

    def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming webhook events.

        Supported events:
        - new_contact

        Args:
            payload: Webhook payload

        Returns:
            Processed webhook data
        """
        event_type = payload.get("event_type")
        event_data = payload.get("data", {})

        if not event_type:
            raise NimbleAPIError("Missing event_type in webhook payload")

        return {
            "event": event_type,
            "data": event_data,
            "processed_at": datetime.now().isoformat()
        }

    def verify_webhook_signature(
        self,
        payload: str,
        signature: str,
        webhook_secret: str
    ) -> bool:
        """
        Verify webhook signature for security.

        Args:
            payload: Raw webhook payload string
            signature: Signature from webhook header
            webhook_secret: Your webhook secret

        Returns:
            True if signature is valid
        """
        expected_signature = hmac.new(
            webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)


# Example usage
if __name__ == "__main__":
    client = NimbleClient(api_key="your_api_key_here")

    try:
        result = client.create_contact(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="+1234567890"
        )
        print("Contact created:", result)
    except NimbleAPIError as e:
        print(f"Error: {e}")