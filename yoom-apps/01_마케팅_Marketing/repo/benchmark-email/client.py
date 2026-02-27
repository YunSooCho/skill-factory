"""
Benchmark Email API Client
"""

import requests
from typing import Optional, Dict, Any, List


class BenchmarkEmailAPIError(Exception):
    """Base exception for Benchmark Email API errors"""
    pass


class BenchmarkEmailAuthError(BenchmarkEmailAPIError):
    """Authentication error"""
    pass


class BenchmarkEmailRateLimitError(BenchmarkEmailAPIError):
    """Rate limit exceeded"""
    pass


class BenchmarkEmailClient:
    """Benchmark Email API Client for contact management"""

    BASE_URL = "https://clientapi.benchmarkemail.com"

    def __init__(self, api_key: str):
        """
        Initialize Benchmark Email client

        Args:
            api_key: Your Benchmark Email API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "AuthToken": api_key,
            "Content-Type": "application/json"
        })

    # ===== Contact Management =====

    def add_contact(
        self,
        email: str,
        list_id: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        country: Optional[str] = None,
        phone: Optional[str] = None,
        mobile: Optional[str] = None,
        fax: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        double_optin: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Add a contact to a list

        Args:
            email: Contact email (required)
            list_id: List ID to add contact to
            first_name: First name
            last_name: Last name
            company: Company name
            address: Street address
            city: City
            state: State/Province
            zip_code: Postal/ZIP code
            country: Country
            phone: Phone number
            mobile: Mobile phone number
            fax: Fax number
            custom_fields: Custom field key-value pairs
            double_optin: Whether to use double opt-in

        Returns:
            API response data
        """
        endpoint = f"{self.BASE_URL}/Contact"
        payload = {"Email": email}

        if list_id:
            payload["ListID"] = str(list_id)
        if first_name:
            payload["FirstName"] = first_name
        if last_name:
            payload["LastName"] = last_name
        if company:
            payload["Company"] = company
        if address:
            payload["Address"] = address
        if city:
            payload["City"] = city
        if state:
            payload["State"] = state
        if zip_code:
            payload["Zip"] = zip_code
        if country:
            payload["Country"] = country
        if phone:
            payload["Phone"] = phone
        if mobile:
            payload["Mobile"] = mobile
        if fax:
            payload["Fax"] = fax
        if custom_fields:
            for key, value in custom_fields.items():
                if not key.startswith("CustomField"):
                    key = f"CustomField{key}"
                payload[key] = str(value)
        if double_optin is not None:
            payload["DoubleOptin"] = "true" if double_optin else "false"

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def search_contact(
        self,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        list_id: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for contacts

        Args:
            email: Filter by email
            first_name: Filter by first name
            last_name: Filter by last name
            list_id: Filter by list
            custom_fields: Filter by custom fields
            limit: Maximum number of results

        Returns:
            List of contacts
        """
        endpoint = f"{self.BASE_URL}/Contact/Search"
        payload = {}

        if email:
            payload["Email"] = email
        if first_name:
            payload["FirstName"] = first_name
        if last_name:
            payload["LastName"] = last_name
        if list_id:
            payload["ListID"] = str(list_id)
        if custom_fields:
            for key, value in custom_fields.items():
                if not key.startswith("CustomField"):
                    key = f"CustomField{key}"
                payload[key] = str(value)
        if limit:
            payload["limit"] = str(limit)

        try:
            response = self.session.get(endpoint, params=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", {}).get("Contacts", [])
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def update_contact(
        self,
        contact_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        country: Optional[str] = None,
        phone: Optional[str] = None,
        mobile: Optional[str] = None,
        fax: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Update contact information

        Args:
            contact_id: Contact ID to update (email or internal ID)
            email: Updated email
            first_name: Updated first name
            last_name: Updated last name
            company: Updated company
            address: Updated address
            city: Updated city
            state: Updated state
            zip_code: Updated ZIP code
            country: Updated country
            phone: Updated phone
            mobile: Updated mobile
            fax: Updated fax
            custom_fields: Custom field updates

        Returns:
            API response data
        """
        endpoint = f"{self.BASE_URL}/Contact/Update"
        payload = {"ContactID": contact_id}

        if email:
            payload["Email"] = email
        if first_name:
            payload["FirstName"] = first_name
        if last_name:
            payload["LastName"] = last_name
        if company:
            payload["Company"] = company
        if address:
            payload["Address"] = address
        if city:
            payload["City"] = city
        if state:
            payload["State"] = state
        if zip_code:
            payload["Zip"] = zip_code
        if country:
            payload["Country"] = country
        if phone:
            payload["Phone"] = phone
        if mobile:
            payload["Mobile"] = mobile
        if fax:
            payload["Fax"] = fax
        if custom_fields:
            for key, value in custom_fields.items():
                if not key.startswith("CustomField"):
                    key = f"CustomField{key}"
                payload[key] = str(value)

        try:
            response = self.session.put(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def delete_contact(
        self,
        contact_id: str,
        list_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Delete a contact

        Args:
            contact_id: Contact ID to delete (email or internal ID)
            list_id: List ID (may be required)

        Returns:
            API response data
        """
        endpoint = f"{self.BASE_URL}/Contact/Delete"
        payload = {"ContactID": contact_id}

        if list_id:
            payload["ListID"] = str(list_id)

        try:
            response = self.session.delete(endpoint, params=payload)
            response.raise_for_status()
            return response.json() if response.content else {"success": True}
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def list_contacts(
        self,
        list_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        List contacts

        Args:
            list_id: Filter by list
            limit: Maximum number of results
            offset: Result offset for pagination
            sort_by: Sort field

        Returns:
            List of contacts
        """
        endpoint = f"{self.BASE_URL}/Contact/List"
        params = {}

        if list_id:
            params["ListID"] = str(list_id)
        if limit:
            params["limit"] = str(limit)
        if offset:
            params["offset"] = str(offset)
        if sort_by:
            params["sortBy"] = sort_by

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("response", {}).get("Contacts", [])
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def _handle_error(self, error: requests.exceptions.HTTPError):
        """Handle API errors"""
        if error.response.status_code == 401:
            raise BenchmarkEmailAuthError("Invalid API key")
        elif error.response.status_code == 429:
            raise BenchmarkEmailRateLimitError("Rate limit exceeded")
        elif error.response.status_code == 400:
            raise BenchmarkEmailAPIError(f"Invalid request: {error.response.text}")
        elif error.response.status_code == 403:
            raise BenchmarkEmailAPIError("Forbidden - insufficient permissions")
        elif error.response.status_code == 404:
            raise BenchmarkEmailAPIError("Resource not found")
        else:
            raise BenchmarkEmailAPIError(f"HTTP {error.response.status_code}: {error.response.text}")