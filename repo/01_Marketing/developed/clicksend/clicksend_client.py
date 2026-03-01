"""
ClickSend SMS & Email Messaging API Client

Supports:
- Send SMS
- Send SMS Campaign
- Send Email-SMS
- Cancel SMS
- Create Contact List
- Update Contact List
- Delete Contact List
- Search Contact List
- Create Contact
- Get Contact
- Update Contact
- Delete Contact
- Get Contacts
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class ContactList:
    """Contact list data"""
    list_id: int
    name: str
    status: str
    created_at: Optional[datetime]
    contact_count: int
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class Contact:
    """Contact data"""
    contact_id: int
    phone_number: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    custom_fields: Optional[Dict[str, str]]
    lists: List[int]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class Message:
    """SMS/Email message data"""
    message_id: str
    status: str
    schedule: Optional[datetime]
    recipient_count: int
    body: str
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class DeliveryReceipt:
    """Delivery receipt data"""
    message_id: str
    status: str
    status_code: str
    timestamp: datetime
    recipient: str
    raw_response: Optional[Dict[str, Any]] = None


class ClickSendClient:
    """
    ClickSend SMS & Email Messaging API client.

    API Documentation: https://rest.clicksend.com/v3/
    This service provides SMS, email messaging, and contact management.
    """

    BASE_URL = "https://rest.clicksend.com/v3"

    def __init__(self, username: str, api_key: str, timeout: int = 30):
        """
        Initialize ClickSend client.

        Args:
            username: ClickSend username
            api_key: ClickSend API key
            timeout: Request timeout in seconds (default: 30)
        """
        self.username = username
        self.api_key = api_key
        self.timeout = timeout
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        auth = aiohttp.BasicAuth(self.username, self.api_key)
        return {
            "User-Agent": "ClickSendClient/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _get_auth(self) -> aiohttp.BasicAuth:
        """Get basic authentication"""
        return aiohttp.BasicAuth(self.username, self.api_key)

    # ==================== SMS Messaging ====================

    async def send_sms(
        self,
        body: str,
        to: str,
        from_number: Optional[str] = None,
        schedule: Optional[datetime] = None,
        custom_string: Optional[str] = None
    ) -> Message:
        """
        Send a single SMS message.

        Args:
            body: Message content
            to: Recipient phone number (with country code, e.g., +1234567890)
            from_number: Sender number or name (optional)
            schedule: Schedule for later sending (optional)
            custom_string: Custom reference string (optional)

        Returns:
            Message: Sent message data

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If API request fails
        """
        if not body or not body.strip():
            raise ValueError("body is required")
        if not to or not to.strip():
            raise ValueError("to is required")

        url = f"{self.BASE_URL}/sms/send"

        messages = [{
            "body": body.strip(),
            "to": to.strip()
        }]

        if from_number:
            messages[0]["from"] = from_number
        if custom_string:
            messages[0]["custom_string"] = custom_string

        payload = {"messages": messages}
        if schedule:
            payload["schedule"] = schedule.isoformat()

        try:
            async with self.session.post(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_message(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 400:
                raise ValueError(f"Invalid request parameters: {e.message}")
            elif e.status == 401:
                raise ValueError("Invalid or missing API credentials")
            elif e.status == 403:
                raise ValueError("Insufficient credits or permissions")
            elif e.status == 429:
                raise ValueError(f"Rate limit exceeded. Please try again later.")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from API")

    async def send_sms_campaign(
        self,
        body: str,
        recipients: List[str],
        list_id: Optional[int] = None,
        from_number: Optional[str] = None,
        schedule: Optional[datetime] = None
    ) -> Message:
        """
        Send SMS campaign to multiple recipients.

        Args:
            body: Message content
            recipients: List of recipient phone numbers
            list_id: Contact list ID to send to (alternative to recipients)
            from_number: Sender number or name (optional)
            schedule: Schedule for later sending (optional)

        Returns:
            Message: Campaign message data

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If API request fails
        """
        if not body or not body.strip():
            raise ValueError("body is required")
        if not recipients and not list_id:
            raise ValueError("Either recipients or list_id is required")

        url = f"{self.BASE_URL}/sms/send"

        messages = [{"body": body.strip()}]

        if recipients:
            messages[0]["to"] = ",".join(recipients)
        if list_id:
            messages[0]["list_id"] = list_id
        if from_number:
            messages[0]["from"] = from_number

        payload = {"messages": messages}
        if schedule:
            payload["schedule"] = schedule.isoformat()

        try:
            async with self.session.post(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_message(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 403:
                raise ValueError("Insufficient credits or permissions")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def send_email_sms(
        self,
        to: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
        schedule: Optional[datetime] = None
    ) -> Message:
        """
        Send an email message.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (HTML or plain text)
            from_email: Sender email (optional, uses default if not provided)
            from_name: Sender name (optional)
            schedule: Schedule for later sending (optional)

        Returns:
            Message: Sent email data

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If API request fails
        """
        if not to or not to.strip():
            raise ValueError("to is required")
        if not subject or not subject.strip():
            raise ValueError("subject is required")
        if not body:
            raise ValueError("body is required")

        url = f"{self.BASE_URL}/email/send"

        emails = [{
            "to": to.strip(),
            "subject": subject.strip(),
            "body": body
        }]

        if from_email:
            emails[0]["from_email"] = from_email
        if from_name:
            emails[0]["from_name"] = from_name

        payload = {"emails": emails}
        if schedule:
            payload["schedule"] = schedule.isoformat()

        try:
            async with self.session.post(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_message(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 403:
                raise ValueError("Insufficient credits or permissions")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def cancel_sms(self, message_id: str) -> bool:
        """
        Cancel a scheduled SMS.

        Args:
            message_id: Message ID to cancel

        Returns:
            bool: True if cancellation was successful

        Raises:
            ValueError: If message not found or already sent
            aiohttp.ClientError: If API request fails
        """
        if not message_id:
            raise ValueError("message_id is required")

        url = f"{self.BASE_URL}/sms/cancel"

        payload = {"messages": [message_id]}

        try:
            async with self.session.post(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                return True

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Message {message_id} not found or already sent")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")

    # ==================== Contact List Management ====================

    async def create_contact_list(
        self,
        name: str,
        description: Optional[str] = None
    ) -> ContactList:
        """
        Create a new contact list.

        Args:
            name: List name
            description: List description (optional)

        Returns:
            ContactList: Created contact list

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If API request fails
        """
        if not name or not name.strip():
            raise ValueError("name is required")

        url = f"{self.BASE_URL}/lists"

        payload = {"list_name": name.strip()}
        if description:
            payload["list_description"] = description.strip()

        try:
            async with self.session.post(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_contact_list(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 409:
                raise ValueError("List with this name already exists")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def update_contact_list(
        self,
        list_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> ContactList:
        """
        Update a contact list.

        Args:
            list_id: Contact list ID
            name: New name (optional)
            description: New description (optional)

        Returns:
            ContactList: Updated contact list

        Raises:
            ValueError: If list not found
            aiohttp.ClientError: If API request fails
        """
        if not list_id:
            raise ValueError("list_id is required")

        url = f"{self.BASE_URL}/lists/{list_id}"

        payload = {}
        if name:
            payload["list_name"] = name.strip()
        if description is not None:
            payload["list_description"] = description.strip()

        if not payload:
            raise ValueError("At least one field to update must be provided")

        try:
            async with self.session.put(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_contact_list(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"List {list_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def delete_contact_list(self, list_id: int) -> bool:
        """
        Delete a contact list.

        Args:
            list_id: Contact list ID

        Returns:
            bool: True if deletion was successful

        Raises:
            ValueError: If list not found
            aiohttp.ClientError: If API request fails
        """
        if not list_id:
            raise ValueError("list_id is required")

        url = f"{self.BASE_URL}/lists/{list_id}"

        try:
            async with self.session.delete(
                url,
                auth=self._get_auth(),
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                return True

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"List {list_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")

    async def search_contact_lists(
        self,
        name: Optional[str] = None,
        page: int = 1,
        limit: int = 50
    ) -> List[ContactList]:
        """
        Search contact lists.

        Args:
            name: Filter by list name (optional)
            page: Page number (default: 1)
            limit: Results per page (default: 50)

        Returns:
            List[ContactList]: List of contact lists

        Raises:
            aiohttp.ClientError: If API request fails
        """
        url = f"{self.BASE_URL}/lists"
        params = {"page": page, "limit": limit}

        if name:
            params["list_name"] = name.strip()

        try:
            async with self.session.get(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                params=params
            ) as response:
                response.raise_for_status()
                data = await response.json()

                lists = []
                items = data.get("data", data)
                for item in items:
                    lists.append(self._parse_contact_list(item))

                return lists

        except aiohttp.ClientResponseError as e:
            if e.status == 401:
                raise ValueError("Invalid credentials")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    # ==================== Contact Management ====================

    async def create_contact(
        self,
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        custom_fields: Optional[Dict[str, str]] = None,
        list_id: Optional[int] = None
    ) -> Contact:
        """
        Create a new contact.

        Args:
            phone_number: Phone number (with country code)
            email: Email address
            first_name: First name
            last_name: Last name
            custom_fields: Custom field values
            list_id: List ID to add contact to

        Returns:
            Contact: Created contact

        Raises:
            ValueError: If neither phone nor email provided
            aiohttp.ClientError: If API request fails
        """
        if not phone_number and not email:
            raise ValueError("Either phone_number or email is required")

        url = f"{self.BASE_URL}/contacts"

        payload = {}
        if phone_number:
            payload["phone_number"] = phone_number
        if email:
            payload["email"] = email
        if first_name:
            payload["first_name"] = first_name.strip()
        if last_name:
            payload["last_name"] = last_name.strip()
        if custom_fields:
            payload["custom_field"] = custom_fields
        if list_id:
            payload["list_id"] = list_id

        try:
            async with self.session.post(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_contact(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 409:
                raise ValueError("Contact already exists")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def get_contact(self, contact_id: int) -> Contact:
        """
        Get contact details.

        Args:
            contact_id: Contact ID

        Returns:
            Contact: Contact data

        Raises:
            ValueError: If contact not found
            aiohttp.ClientError: If API request fails
        """
        if not contact_id:
            raise ValueError("contact_id is required")

        url = f"{self.BASE_URL}/contacts/{contact_id}"

        try:
            async with self.session.get(
                url,
                auth=self._get_auth(),
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_contact(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Contact {contact_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def update_contact(
        self,
        contact_id: int,
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        custom_fields: Optional[Dict[str, str]] = None
    ) -> Contact:
        """
        Update a contact.

        Args:
            contact_id: Contact ID
            phone_number: New phone number (optional)
            email: New email (optional)
            first_name: New first name (optional)
            last_name: New last name (optional)
            custom_fields: Updated custom fields (optional)

        Returns:
            Contact: Updated contact

        Raises:
            ValueError: If contact not found
            aiohttp.ClientError: If API request fails
        """
        if not contact_id:
            raise ValueError("contact_id is required")

        url = f"{self.BASE_URL}/contacts/{contact_id}"

        payload = {}
        if phone_number:
            payload["phone_number"] = phone_number
        if email:
            payload["email"] = email
        if first_name:
            payload["first_name"] = first_name.strip()
        if last_name:
            payload["last_name"] = last_name.strip()
        if custom_fields:
            payload["custom_field"] = custom_fields

        if not payload:
            raise ValueError("At least one field to update must be provided")

        try:
            async with self.session.put(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_contact(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Contact {contact_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def delete_contact(self, contact_id: int) -> bool:
        """
        Delete a contact.

        Args:
            contact_id: Contact ID

        Returns:
            bool: True if deletion was successful

        Raises:
            ValueError: If contact not found
            aiohttp.ClientError: If API request fails
        """
        if not contact_id:
            raise ValueError("contact_id is required")

        url = f"{self.BASE_URL}/contacts/{contact_id}"

        try:
            async with self.session.delete(
                url,
                auth=self._get_auth(),
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                return True

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Contact {contact_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")

    async def get_contacts(
        self,
        list_id: Optional[int] = None,
        page: int = 1,
        limit: int = 50,
        phone: Optional[str] = None,
        email: Optional[str] = None
    ) -> List[Contact]:
        """
        Get contacts with optional filtering.

        Args:
            list_id: Filter by list ID (optional)
            page: Page number (default: 1)
            limit: Results per page (default: 50)
            phone: Filter by phone number (optional)
            email: Filter by email (optional)

        Returns:
            List[Contact]: List of contacts

        Raises:
            aiohttp.ClientError: If API request fails
        """
        url = f"{self.BASE_URL}/contacts"
        params = {"page": page, "limit": limit}

        if list_id:
            params["list_id"] = list_id
        if phone:
            params["phone_number"] = phone.strip()
        if email:
            params["email"] = email.strip()

        try:
            async with self.session.get(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                params=params
            ) as response:
                response.raise_for_status()
                data = await response.json()

                contacts = []
                items = data.get("data", data)
                for item in items:
                    contacts.append(self._parse_contact(item))

                return contacts

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError("Contacts not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    # ==================== Helper Methods ====================

    def _parse_message(self, data: Dict[str, Any]) -> Message:
        """Parse message data"""
        schedule = None
        if data.get("schedule"):
            try:
                schedule = datetime.fromisoformat(data["schedule"].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass

        return Message(
            message_id=str(data.get("message_id", data.get("request_id", ""))),
            status=data.get("status", data.get("messages", [{}])[0].get("status", "unknown")),
            schedule=schedule,
            recipient_count=data.get("recipient_count", len(data.get("messages", []))),
            body=data.get("messages", [{}])[0].get("body", ""),
            raw_response=data
        )

    def _parse_contact_list(self, data: Dict[str, Any]) -> ContactList:
        """Parse contact list data"""
        created_at = None
        if data.get("created_at"):
            try:
                created_at = datetime.fromisoformat(data["created_at"].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass

        return ContactList(
            list_id=int(data.get("list_id", data.get("id", 0))),
            name=data.get("list_name", data.get("name", "")),
            status=data.get("status", "active"),
            created_at=created_at,
            contact_count=int(data.get("contact_count", data.get("count", 0))),
            raw_response=data
        )

    def _parse_contact(self, data: Dict[str, Any]) -> Contact:
        """Parse contact data"""
        custom_fields = data.get("custom_field", {})
        lists = data.get("lists", [])
        list_ids = [lst.get("list_id") if isinstance(lst, dict) else lst for lst in lists]

        return Contact(
            contact_id=int(data.get("contact_id", data.get("id", 0))),
            phone_number=data.get("phone_number"),
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            custom_fields=custom_fields,
            lists=list_ids,
            raw_response=data
        )