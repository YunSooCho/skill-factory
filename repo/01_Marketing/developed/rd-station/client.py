"""
RD Station API Client - Marketing Automation Platform
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime


class RDStationAPIError(Exception):
    """Base exception for RD Station API errors"""
    pass


class RDStationClient:
    """Client for RD Station Marketing API"""

    BASE_URL = "https://api.rd.services/platform"
    EVENTS_URL = "https://api.rd.services/platform/events"
    CONTACTS_URL = "https://api.rd.services/platform/contacts"

    def __init__(self, access_token: str, refresh_token: Optional[str] = None):
        """
        Initialize RD Station client

        Args:
            access_token: RD Station API access token
            refresh_token: Optional refresh token for token renewal
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request(self, method: str, url: str, json_data: Optional[Dict] = None,
                      params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to RD Station API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            url: API endpoint URL
            json_data: JSON payload for request body
            params: Query parameters

        Returns:
            Response JSON data

        Raises:
            RDStationAPIError: If API request fails
        """
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            if hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    if 'errors' in error_data:
                        error_msg = f"API Error: {error_data['errors']}"
                except:
                    pass
            raise RDStationAPIError(error_msg) from e

    # Contact Operations

    def create_contact(self, email: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new contact

        Args:
            email: Contact email (required)
            **kwargs: Additional contact fields (name, phone, job_title, etc.)

        Returns:
            Created contact data

        Raises:
            RDStationAPIError: If contact creation fails
        """
        contact_data = {"email": email}
        contact_data.update(kwargs)

        return self._make_request(
            method="POST",
            url=self.CONTACTS_URL,
            json_data=contact_data
        )

    def get_contact(self, email: str) -> Dict[str, Any]:
        """
        Get contact by email

        Args:
            email: Contact email

        Returns:
            Contact data

        Raises:
            RDStationAPIError: If contact retrieval fails
        """
        return self._make_request(
            method="GET",
            url=self.CONTACTS_URL,
            params={"email": email}
        )

    def get_contact_information(self, email: str) -> Dict[str, Any]:
        """
        Get detailed contact information

        Args:
            email: Contact email

        Returns:
            Detailed contact information

        Raises:
            RDStationAPIError: If contact information retrieval fails
        """
        return self.get_contact(email)  # Same as get_contact

    def update_contact(self, email: str, **kwargs) -> Dict[str, Any]:
        """
        Update contact information

        Args:
            email: Contact email
            **kwargs: Fields to update

        Returns:
            Updated contact data

        Raises:
            RDStationAPIError: If contact update fails
        """
        contact_data = {"email": email}
        contact_data.update(kwargs)

        return self._make_request(
            method="PATCH",
            url=f"{self.CONTACTS_URL}/{email}",
            json_data=contact_data
        )

    def update_contact_information(self, email: str, **kwargs) -> Dict[str, Any]:
        """
        Update contact information (alias for update_contact)

        Args:
            email: Contact email
            **kwargs: Fields to update

        Returns:
            Updated contact data

        Raises:
            RDStationAPIError: If contact update fails
        """
        return self.update_contact(email, **kwargs)

    def delete_contact(self, email: str) -> Dict[str, Any]:
        """
        Delete a contact

        Args:
            email: Contact email to delete

        Returns:
            Deletion response

        Raises:
            RDStationAPIError: If contact deletion fails
        """
        return self._make_request(
            method="DELETE",
            url=f"{self.CONTACTS_URL}/{email}"
        )

    # Event Operations

    def create_event(self, event_type: str, email: Optional[str] = None,
                     **kwargs) -> Dict[str, Any]:
        """
        Create a custom event

        Args:
            event_type: Type of event to create
            email: Contact email (optional)
            **kwargs: Additional event data

        Returns:
            Created event data

        Raises:
            RDStationAPIError: If event creation fails
        """
        event_data = {
            "event_type": event_type,
            "event_family": "CDP"
        }

        if email:
            event_data["email"] = email

        event_data.update(kwargs)

        return self._make_request(
            method="POST",
            url=self.EVENTS_URL,
            json_data=event_data
        )

    def create_default_conversion_event(self, email: str, event_value: Optional[float] = None,
                                        **kwargs) -> Dict[str, Any]:
        """
        Create a default conversion event

        Args:
            email: Contact email
            event_value: Optional conversion value
            **kwargs: Additional event data (name, funnel_name, etc.)

        Returns:
            Created event data

        Raises:
            RDStationAPIError: If event creation fails
        """
        event_data = {
            "event_type": "CONVERSION",
            "email": email,
            "event_family": "CDP"
        }

        if event_value is not None:
            event_data["value"] = event_value

        event_data.update(kwargs)

        return self._make_request(
            method="POST",
            url=self.EVENTS_URL,
            json_data=event_data
        )

    def create_call_event(self, email: str, call_status: str,
                          notes: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Create a call event

        Args:
            email: Contact email
            call_status: Call status (e.g., 'completed', 'no_answer', etc.)
            notes: Optional call notes
            **kwargs: Additional event data

        Returns:
            Created event data

        Raises:
            RDStationAPIError: If event creation fails
        """
        event_data = {
            "event_type": "CALL",
            "email": email,
            "event_family": "CDP",
            "call_status": call_status
        }

        if notes:
            event_data["notes"] = notes

        event_data.update(kwargs)

        return self._make_request(
            method="POST",
            url=self.EVENTS_URL,
            json_data=event_data
        )

    def create_closing_event(self, email: str, deal_value: float,
                             deal_status: str, **kwargs) -> Dict[str, Any]:
        """
        Create a closing event (deal won/lost)

        Args:
            email: Contact email
            deal_value: Deal value
            deal_status: Deal status (e.g., 'won', 'lost')
            **kwargs: Additional event data

        Returns:
            Created event data

        Raises:
            RDStationAPIError: If event creation fails
        """
        event_data = {
            "event_type": "CLOSING",
            "email": email,
            "event_family": "CDP",
            "value": deal_value,
            "deal_status": deal_status
        }

        event_data.update(kwargs)

        return self._make_request(
            method="POST",
            url=self.EVENTS_URL,
            json_data=event_data
        )

    def create_abandonment_event(self, email: str, abandoned_resource: str,
                                  **kwargs) -> Dict[str, Any]:
        """
        Create an abandonment event (e.g., cart abandonment)

        Args:
            email: Contact email
            abandoned_resource: Resource that was abandoned (e.g., 'cart', 'form')
            **kwargs: Additional event data

        Returns:
            Created event data

        Raises:
            RDStationAPIError: If event creation fails
        """
        event_data = {
            "event_type": "ABANDONMENT",
            "email": email,
            "event_family": "CDP",
            "abandoned_resource": abandoned_resource
        }

        event_data.update(kwargs)

        return self._make_request(
            method="POST",
            url=self.EVENTS_URL,
            json_data=event_data
        )

    def create_chat_starter_event(self, email: str, chat_channel: str,
                                    message: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Create a chat starter event

        Args:
            email: Contact email
            chat_channel: Chat channel (e.g., 'whatsapp', 'website_chat')
            message: Optional initial message
            **kwargs: Additional event data

        Returns:
            Created event data

        Raises:
            RDStationAPIError: If event creation fails
        """
        event_data = {
            "event_type": "CHAT_STARTER",
            "email": email,
            "event_family": "CDP",
            "chat_channel": chat_channel
        }

        if message:
            event_data["message"] = message

        event_data.update(kwargs)

        return self._make_request(
            method="POST",
            url=self.EVENTS_URL,
            json_data=event_data
        )

    # Tag Operations

    def add_tag_to_lead(self, email: str, tag: str) -> Dict[str, Any]:
        """
        Add a tag to a contact (lead)

        Args:
            email: Contact email
            tag: Tag to add

        Returns:
            Updated contact data with tags

        Raises:
            RDStationAPIError: If tag addition fails
        """
        # Get current contact to preserve existing data
        contact = self.get_contact(email)

        # Add tag to contact
        contact_data = contact.copy()
        if "tags" not in contact_data:
            contact_data["tags"] = []

        if tag not in contact_data["tags"]:
            contact_data["tags"].append(tag)

        return self._make_request(
            method="PATCH",
            url=f"{self.CONTACTS_URL}/{email}",
            json_data={"tags": contact_data["tags"]}
        )

    def close(self):
        """Close the session"""
        self.session.close()