"""
Myphoner API Client
API Documentation: https://www.myphoner.com/developers
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime
import json


class MyphonerAPIError(Exception):
    """Custom exception for Myphoner API errors."""
    pass


class MyphonerClient:
    """Client for Myphoner API - Lead management and tracking."""

    def __init__(self, api_key: str, base_url: str = "https://api.myphoner.com/v1"):
        """
        Initialize Myphoner API client.

        Args:
            api_key: Your Myphoner API key
            base_url: API base URL (default: https://api.myphoner.com/v1)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        self.rate_limit_wait = 1.0  # seconds between requests

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make API request with error handling.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional arguments for request

        Returns:
            Response data as dictionary

        Raises:
            MyphonerAPIError: If request fails
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
            raise MyphonerAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise MyphonerAPIError(f"Request failed: {str(e)}")
        except json.JSONDecodeError:
            raise MyphonerAPIError("Invalid JSON response")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"message": response.text}

    def create_lead(
        self,
        list_id: str,
        name: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        title: Optional[str] = None,
        notes: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new lead.

        Args:
            list_id: ID of the list to add lead to
            name: Lead name
            phone: Phone number
            email: Email address
            company: Company name
            title: Job title
            notes: Additional notes
            custom_fields: Custom field values

        Returns:
            Created lead data
        """
        data = {
            "list_id": list_id,
            "name": name,
            "phone": phone,
            "email": email,
            "company": company,
            "title": title,
            "notes": notes
        }
        if custom_fields:
            data["custom_fields"] = custom_fields

        return self._make_request("POST", "/leads", json=data)

    def get_lead(self, lead_id: str) -> Dict[str, Any]:
        """
        Get lead details by ID.

        Args:
            lead_id: ID of the lead

        Returns:
            Lead data
        """
        return self._make_request("GET", f"/leads/{lead_id}")

    def update_lead(
        self,
        lead_id: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        title: Optional[str] = None,
        notes: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update lead information.

        Args:
            lead_id: ID of the lead to update
            name: Lead name
            phone: Phone number
            email: Email address
            company: Company name
            title: Job title
            notes: Additional notes
            custom_fields: Custom field values

        Returns:
            Updated lead data
        """
        data = {}
        if name is not None:
            data["name"] = name
        if phone is not None:
            data["phone"] = phone
        if email is not None:
            data["email"] = email
        if company is not None:
            data["company"] = company
        if title is not None:
            data["title"] = title
        if notes is not None:
            data["notes"] = notes
        if custom_fields is not None:
            data["custom_fields"] = custom_fields

        return self._make_request("PUT", f"/leads/{lead_id}", json=data)

    def search_leads(
        self,
        list_id: str,
        query: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for leads.

        Args:
            list_id: ID of the list to search
            query: Search query string
            status: Filter by status (todo, won, lost, callback)
            limit: Maximum number of results (default: 50)
            offset: Offset for pagination (default: 0)

        Returns:
            List of leads matching criteria
        """
        params = {
            "list_id": list_id,
            "limit": limit,
            "offset": offset
        }
        if query:
            params["query"] = query
        if status:
            params["status"] = status

        return self._make_request("GET", "/leads", params=params)

    def list_columns(self, list_id: str) -> Dict[str, Any]:
        """
        List all columns in a list.

        Args:
            list_id: ID of the list

        Returns:
            List of columns with their properties
        """
        params = {"list_id": list_id}
        return self._make_request("GET", "/columns", params=params)

    def mark_winner(self, lead_id: str, notes: Optional[str] = None) -> Dict[str, Any]:
        """
        Mark a lead as winner (successful sale).

        Args:
            lead_id: ID of the lead
            notes: Optional notes about the sale

        Returns:
            Updated lead data
        """
        data = {"status": "won"}
        if notes:
            data["notes"] = notes

        return self._make_request("PUT", f"/leads/{lead_id}/status", json=data)

    def mark_loser(self, lead_id: str, notes: Optional[str] = None) -> Dict[str, Any]:
        """
        Mark a lead as loser (lost sale).

        Args:
            lead_id: ID of the lead
            notes: Optional notes about why the sale was lost

        Returns:
            Updated lead data
        """
        data = {"status": "lost"}
        if notes:
            data["notes"] = notes

        return self._make_request("PUT", f"/leads/{lead_id}/status", json=data)

    def mark_callback(
        self,
        lead_id: str,
        callback_date: Optional[datetime] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Mark a lead for callback.

        Args:
            lead_id: ID of the lead
            callback_date: When to callback (datetime object)
            notes: Optional notes about the callback

        Returns:
            Updated lead data
        """
        data = {"status": "callback"}
        if callback_date:
            data["callback_date"] = callback_date.isoformat()
        if notes:
            data["notes"] = notes

        return self._make_request("PUT", f"/leads/{lead_id}/status", json=data)

    def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming webhook events.

        Supported events:
        - lead_marked_winner
        - lead_marked_loser
        - lead_archived
        - lead_marked_callback

        Args:
            payload: Webhook payload

        Returns:
            Processed webhook data
        """
        event_type = payload.get("event_type")
        event_data = payload.get("data", {})

        if not event_type:
            raise MyphonerAPIError("Missing event_type in webhook payload")

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
        import hmac
        import hashlib

        expected_signature = hmac.new(
            webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)


# Example usage
if __name__ == "__main__":
    # Example: Initialize client
    client = MyphonerClient(api_key="your_api_key_here")

    # Example: Create a lead
    try:
        result = client.create_lead(
            list_id="list_123",
            name="John Doe",
            phone="+1234567890",
            email="john@example.com",
            company="Acme Inc."
        )
        print("Lead created:", result)
    except MyphonerAPIError as e:
        print(f"Error: {e}")