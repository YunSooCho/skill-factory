"""
BigMailer API Client
"""

import requests
from typing import Optional, Dict, Any, List


class BigMailerAPIError(Exception):
    """Base exception for BigMailer API errors"""
    pass


class BigMailerAuthError(BigMailerAPIError):
    """Authentication error"""
    pass


class BigMailerRateLimitError(BigMailerAPIError):
    """Rate limit exceeded"""
    pass


class BigMailerClient:
    """BigMailer API Client for contact management"""

    BASE_URL = "https://api.bigmailer.io/v1"

    def __init__(self, api_key: str):
        """
        Initialize BigMailer client

        Args:
            api_key: Your BigMailer API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        })

    # ===== Contact Management =====

    def create_contact(
        self,
        email: str,
        brand_id: str,
        list_ids: Optional[List[str]] = None,
        field_values: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        opt_in: Optional[bool] = None,
        transaction_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new contact

        Args:
            email: Contact email (required)
            brand_id: Brand ID (required)
            list_ids: List of list IDs to add contact to
            field_values: Custom field key-value pairs
            tags: List of tags
            opt_in: Opt-in status
            transaction_id: Transaction ID for idempotency

        Returns:
            API response data
        """
        endpoint = f"{self.BASE_URL}/contacts"
        payload = {
            "email": email,
            "brand_id": brand_id,
        }

        if list_ids:
            payload["list_ids"] = list_ids
        if field_values:
            payload["field_values"] = field_values
        if tags:
            payload["tags"] = tags
        if opt_in is not None:
            payload["opt_in"] = opt_in
        if transaction_id:
            payload["transaction_id"] = transaction_id

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def get_contact(
        self,
        contact_id: str,
        brand_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a single contact

        Args:
            contact_id: Contact ID or email
            brand_id: Brand ID (optional if contact_id is hash)

        Returns:
            Contact data
        """
        endpoint = f"{self.BASE_URL}/contacts/{contact_id}"
        params = {}
        if brand_id:
            params["brand_id"] = brand_id

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def update_contact(
        self,
        contact_id: str,
        brand_id: Optional[str] = None,
        email: Optional[str] = None,
        list_ids: Optional[List[str]] = None,
        field_values: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        opt_in: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Update a contact

        Args:
            contact_id: Contact ID or email
            brand_id: Brand ID
            email: Updated email
            list_ids: Updated list IDs
            field_values: Updated field values
            tags: Updated tags
            opt_in: Updated opt-in status

        Returns:
            Updated contact data
        """
        endpoint = f"{self.BASE_URL}/contacts/{contact_id}"
        params = {}
        if brand_id:
            params["brand_id"] = brand_id

        payload = {}
        if email:
            payload["email"] = email
        if list_ids is not None:
            payload["list_ids"] = list_ids
        if field_values is not None:
            payload["field_values"] = field_values
        if tags is not None:
            payload["tags"] = tags
        if opt_in is not None:
            payload["opt_in"] = opt_in

        try:
            response = self.session.put(endpoint, params=params, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def delete_contact(
        self,
        contact_id: str,
        brand_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Delete a contact

        Args:
            contact_id: Contact ID or email
            brand_id: Brand ID

        Returns:
            API response data
        """
        endpoint = f"{self.BASE_URL}/contacts/{contact_id}"
        params = {}
        if brand_id:
            params["brand_id"] = brand_id

        try:
            response = self.session.delete(endpoint, params=params)
            response.raise_for_status()
            return response.json() if response.content else {"success": True}
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def list_contacts(
        self,
        brand_id: Optional[str] = None,
        list_id: Optional[str] = None,
        tag: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        List contacts

        Args:
            brand_id: Filter by brand
            list_id: Filter by list
            tag: Filter by tag
            limit: Maximum number of results
            offset: Result offset
            search: Search query

        Returns:
            List of contacts
        """
        endpoint = f"{self.BASE_URL}/contacts"
        params = {}

        if brand_id:
            params["brand_id"] = brand_id
        if list_id:
            params["list_id"] = list_id
        if tag:
            params["tag"] = tag
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if search:
            params["search"] = search

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("data", data.get("contacts", []))
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def list_fields(
        self,
        brand_id: str,
    ) -> List[Dict[str, Any]]:
        """
        List custom fields

        Args:
            brand_id: Brand ID

        Returns:
            List of field definitions
        """
        endpoint = f"{self.BASE_URL}/fields"
        params = {"brand_id": brand_id}

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("data", data.get("fields", []))
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)

    def _handle_error(self, error: requests.exceptions.HTTPError):
        """Handle API errors"""
        if error.response.status_code == 401:
            raise BigMailerAuthError("Invalid API key")
        elif error.response.status_code == 429:
            raise BigMailerRateLimitError("Rate limit exceeded")
        elif error.response.status_code == 400:
            raise BigMailerAPIError(f"Invalid request: {error.response.text}")
        elif error.response.status_code == 403:
            raise BigMailerAPIError("Forbidden - insufficient permissions")
        elif error.response.status_code == 404:
            raise BigMailerAPIError("Resource not found")
        else:
            raise BigMailerAPIError(f"HTTP {error.response.status_code}: {error.response.text}")