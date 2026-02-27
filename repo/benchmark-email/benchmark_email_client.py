"""
Benchmark Email API Client

Supports:
- Add Contact
- Update Contact
- Search Contact
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Contact:
    """Benchmark Email contact representation"""
    id: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    company: Optional[str] = None
    birth_date: Optional[str] = None
    custom_fields: Optional[List[Dict[str, Any]]] = None
    status: Optional[str] = None
    created_at: Optional[str] = None


class BenchmarkEmailClient:
    """
    Benchmark Email API client for email marketing and contact management.

    API Documentation: https://api.benchmarkemail.com/Doc/
    Authentication: API Token (Header: AuthToken)
    Base URL: https://api.benchmarkemail.com/1.0
    """

    BASE_URL = "https://api.benchmarkemail.com/1.0"

    def __init__(self, api_token: str):
        """
        Initialize Benchmark Email client.

        Args:
            api_token: Benchmark Email API token
        """
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "AuthToken": self.api_token,
            "Content-Type": "application/json"
        })
        self.remaining_requests = 1000

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a request to Benchmark Email API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional arguments

        Returns:
            Response data
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201):
                data = response.json()
                return data
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid API token")
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

    def add_contact(
        self,
        data: Optional[Dict[str, Any]] = None,
        email: Optional[str] = None,
        list_id: Optional[str] = None,
        **kwargs
    ) -> Contact:
        """
        Add a new contact.

        Args:
            data: Full contact data dictionary
            email: Email address (alternative to data)
            list_id: List ID to add contact to
            **kwargs: Additional contact fields

        Returns:
            Contact object
        """
        if not data and not email:
            raise ValueError("Either data or email must be provided")

        payload = data or {"email": email}
        payload.update(kwargs)

        if list_id:
            payload["listID"] = list_id

        result = self._request("POST", "/Contact", json=payload)
        return self._parse_contact(result)

    def update_contact(
        self,
        contact_id: str,
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Contact:
        """
        Update an existing contact.

        Args:
            contact_id: Contact ID
            data: Full contact data dictionary
            **kwargs: Fields to update

        Returns:
            Updated Contact object
        """
        payload = data or {}
        payload.update(kwargs)
        payload["id"] = contact_id

        result = self._request("POST", "/Contact", json=payload)
        return self._parse_contact(result)

    def search_contact(
        self,
        email: Optional[str] = None,
        list_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Contact]:
        """
        Search for contacts.

        Args:
            email: Filter by email
            list_id: Filter by list ID
            limit: Number of results
            offset: Pagination offset

        Returns:
            List of Contact objects
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        if list_id:
            params["listID"] = list_id
        if email:
            # For specific email search, use different endpoint
            result = self._request("GET", f"/Contact/GetByEmail", params={"email": email})
            if result.get("id"):
                return [self._parse_contact(result)]
            return []

        result = self._request("GET", "/Contact", params=params)

        contacts = []
        if isinstance(result, dict) and "data" in result:
            for contact_data in result.get("data", []):
                contacts.append(self._parse_contact(contact_data))
        elif isinstance(result, list):
            for contact_data in result:
                contacts.append(self._parse_contact(contact_data))

        return contacts

    def _parse_contact(self, data: Dict[str, Any]) -> Contact:
        """Parse contact data from API response"""
        custom_fields = []
        if "customfield" in data:
            if isinstance(data["customfield"], list):
                custom_fields = data["customfield"]
            elif isinstance(data["customfield"], dict):
                custom_fields = [{"name": k, "value": v} for k, v in data["customfield"].items()]

        return Contact(
            id=data.get("id"),
            email=data.get("email"),
            first_name=data.get("firstname"),
            last_name=data.get("lastname"),
            phone=data.get("phone"),
            address=data.get("address"),
            address2=data.get("address2"),
            city=data.get("city"),
            state=data.get("state"),
            zip_code=data.get("zip"),
            country=data.get("country"),
            company=data.get("company"),
            birth_date=data.get("birthdate"),
            custom_fields=custom_fields,
            status=data.get("status"),
            created_at=data.get("createddate")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_token = "your_benchmark_email_token"

    client = BenchmarkEmailClient(api_token=api_token)

    try:
        # Add a contact
        contact = client.add_contact(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            city="Tokyo",
            country="Japan",
            list_id="list_id_here"
        )
        print(f"Contact added: {contact.id} - {contact.email}")

        # Search for contact
        contacts = client.search_contact(email="test@example.com")
        if contacts:
            print(f"Found contact: {contacts[0].email}")

        # Update contact
        if contacts:
            updated = client.update_contact(
                contacts[0].id,
                first_name="Jane",
                city="Osaka"
            )
            print(f"Updated: {updated.first_name} in {updated.city}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()