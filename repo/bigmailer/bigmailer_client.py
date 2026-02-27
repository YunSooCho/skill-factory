"""
Big Mailer API Client

Supports:
- List Contacts
- Create Contact
- Delete Contact
- Update Contact
- Get Contact
- List Fields
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Contact:
    """Big Mailer contact representation"""
    id: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Field:
    """Big Mailer field representation"""
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    default_value: Optional[str] = None
    required: bool = False


class BigMailerClient:
    """
    Big Mailer API client for email marketing and contact management.

    Authentication: API Key (Header: X-API-Key)
    Base URL: https://api.bigmailer.io
    """

    BASE_URL = "https://api.bigmailer.io/v1"

    def __init__(self, api_key: str):
        """
        Initialize Big Mailer client.

        Args:
            api_key: Big Mailer API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201):
                data = response.json()
                return data
            elif response.status_code == 204:
                return {}
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid API key")
            elif response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Contact Operations ====================

    def list_contacts(
        self,
        limit: int = 100,
        offset: int = 0,
        search: Optional[str] = None
    ) -> List[Contact]:
        """
        List all contacts.

        Args:
            limit: Number of results
            offset: Pagination offset
            search: Search term for email or name

        Returns:
            List of Contact objects
        """
        params = {"limit": limit, "offset": offset}
        if search:
            params["search"] = search

        result = self._request("GET", "/contacts", params=params)

        contacts = []
        if isinstance(result, dict) and "data" in result:
            for contact_data in result.get("data", []):
                contacts.append(self._parse_contact(contact_data))
        elif isinstance(result, list):
            for contact_data in result:
                contacts.append(self._parse_contact(contact_data))

        return contacts

    def create_contact(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """
        Create a new contact.

        Args:
            email: Email address (required)
            first_name: First name
            last_name: Last name
            phone: Phone number
            company: Company name
            custom_fields: Dictionary of custom field values

        Returns:
            Contact object
        """
        if not email:
            raise ValueError("Email is required")

        payload = {"email": email}

        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if phone:
            payload["phone"] = phone
        if company:
            payload["company"] = company
        if custom_fields:
            payload["custom_fields"] = custom_fields

        result = self._request("POST", "/contacts", json=payload)
        return self._parse_contact(result)

    def get_contact(self, contact_id: str) -> Contact:
        """
        Get a specific contact by ID.

        Args:
            contact_id: Contact ID

        Returns:
            Contact object
        """
        result = self._request("GET", f"/contacts/{contact_id}")
        return self._parse_contact(result)

    def update_contact(
        self,
        contact_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """
        Update an existing contact.

        Args:
            contact_id: Contact ID
            email: Email address
            first_name: First name
            last_name: Last name
            phone: Phone number
            company: Company name
            custom_fields: Dictionary of custom field values

        Returns:
            Updated Contact object
        """
        payload = {}

        if email:
            payload["email"] = email
        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if phone:
            payload["phone"] = phone
        if company:
            payload["company"] = company
        if custom_fields:
            payload["custom_fields"] = custom_fields

        result = self._request("PUT", f"/contacts/{contact_id}", json=payload)
        return self._parse_contact(result)

    def delete_contact(self, contact_id: str) -> None:
        """
        Delete a contact.

        Args:
            contact_id: Contact ID
        """
        self._request("DELETE", f"/contacts/{contact_id}")

    # ==================== Field Operations ====================

    def list_fields(self) -> List[Field]:
        """
        List all custom fields.

        Returns:
            List of Field objects
        """
        result = self._request("GET", "/fields")

        fields = []
        if isinstance(result, dict) and "data" in result:
            for field_data in result.get("data", []):
                fields.append(self._parse_field(field_data))
        elif isinstance(result, list):
            for field_data in result:
                fields.append(self._parse_field(field_data))

        return fields

    # ==================== Helper Methods ====================

    def _parse_contact(self, data: Dict[str, Any]) -> Contact:
        """Parse contact data from API response"""
        return Contact(
            id=data.get("id"),
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            phone=data.get("phone"),
            company=data.get("company"),
            status=data.get("status"),
            custom_fields=data.get("custom_fields"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def _parse_field(self, data: Dict[str, Any]) -> Field:
        """Parse field data from API response"""
        return Field(
            id=data.get("id"),
            name=data.get("name"),
            type=data.get("type"),
            default_value=data.get("default_value"),
            required=data.get("required", False)
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_bigmailer_api_key"

    client = BigMailerClient(api_key=api_key)

    try:
        # Create contact
        contact = client.create_contact(
            email="test@example.com",
            first_name="John",
            last_name="Doe"
        )
        print(f"Created: {contact.id} - {contact.email}")

        # Get contact
        fetched = client.get_contact(contact.id)
        print(f"Fetched: {fetched.first_name} {fetched.last_name}")

        # Update contact
        updated = client.update_contact(
            contact.id,
            phone="+81-90-1234-5678"
        )
        print(f"Updated: Phone {updated.phone}")

        # List contacts
        contacts = client.list_contacts(limit=10)
        print(f"Total contacts: {len(contacts)}")

        # List fields
        fields = client.list_fields()
        print(f"Custom fields: {len(fields)}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()