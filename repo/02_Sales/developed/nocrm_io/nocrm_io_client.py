"""
NoCRM.io API Client
API Documentation: https://www.nocrm.io/api/
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime
import json
import hmac
import hashlib


class NoCRMAPIError(Exception):
    """Custom exception for NoCRM API errors."""
    pass


class NoCRMClient:
    """Client for NoCRM.io API - Lead management and CRM."""

    def __init__(self, api_key: str, base_url: str = "https://api.nocrm.io/v1"):
        """
        Initialize NoCRM.io API client.

        Args:
            api_key: Your NoCRM API key
            base_url: API base URL (default: https://api.nocrm.io/v1)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {api_key}",
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
            raise NoCRMAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise NoCRMAPIError(f"Request failed: {str(e)}")
        except json.JSONDecodeError:
            raise NoCRMAPIError("Invalid JSON response")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"message": response.text}

    def create_lead(
        self,
        title: str,
        description: Optional[str] = None,
        status: Optional[str] = "todo",
        contact_name: Optional[str] = None,
        contact_email: Optional[str] = None,
        contact_phone: Optional[str] = None,
        company: Optional[str] = None,
        amount: Optional[float] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new lead.

        Args:
            title: Lead title
            description: Lead description
            status: Initial status (todo, won, lost, standby)
            contact_name: Contact person name
            contact_email: Contact email
            contact_phone: Contact phone
            company: Company name
            amount: Lead amount/value
            tags: List of tags
            custom_fields: Custom field values

        Returns:
            Created lead data
        """
        data = {
            "title": title,
            "status": status or "todo"
        }

        if description:
            data["description"] = description
        if contact_name:
            data["contact_name"] = contact_name
        if contact_email:
            data["contact_email"] = contact_email
        if contact_phone:
            data["contact_phone"] = contact_phone
        if company:
            data["company"] = company
        if amount is not None:
            data["amount"] = amount
        if tags:
            data["tags"] = tags
        if custom_fields:
            data["custom_fields"] = custom_fields

        return self._make_request("POST", "/leads", json=data)

    def retrieve_lead(self, lead_id: str) -> Dict[str, Any]:
        """
        Get lead details by ID.

        Args:
            lead_id: Lead ID

        Returns:
            Lead data
        """
        return self._make_request("GET", f"/leads/{lead_id}")

    def update_lead(
        self,
        lead_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        contact_name: Optional[str] = None,
        contact_email: Optional[str] = None,
        contact_phone: Optional[str] = None,
        company: Optional[str] = None,
        amount: Optional[float] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update lead information.

        Args:
            lead_id: Lead ID
            title: Lead title
            description: Lead description
            status: Lead status
            contact_name: Contact person name
            contact_email: Contact email
            contact_phone: Contact phone
            company: Company name
            amount: Lead amount/value
            tags: List of tags
            custom_fields: Custom field values

        Returns:
            Updated lead data
        """
        data = {}
        if title:
            data["title"] = title
        if description:
            data["description"] = description
        if status:
            data["status"] = status
        if contact_name:
            data["contact_name"] = contact_name
        if contact_email:
            data["contact_email"] = contact_email
        if contact_phone:
            data["contact_phone"] = contact_phone
        if company:
            data["company"] = company
        if amount is not None:
            data["amount"] = amount
        if tags is not None:
            data["tags"] = tags
        if custom_fields is not None:
            data["custom_fields"] = custom_fields

        return self._make_request("PUT", f"/leads/{lead_id}", json=data)

    def delete_lead(self, lead_id: str) -> Dict[str, Any]:
        """
        Delete a lead.

        Args:
            lead_id: Lead ID

        Returns:
            Deletion result
        """
        return self._make_request("DELETE", f"/leads/{lead_id}")

    def search_leads(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        contact_email: Optional[str] = None,
        company: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for leads.

        Args:
            query: General search query
            status: Filter by status (todo, won, lost, standby)
            contact_email: Filter by contact email
            company: Filter by company
            tags: Filter by tags
            limit: Max results
            offset: Pagination offset

        Returns:
            List of matching leads
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        if query:
            params["query"] = query
        if status:
            params["status"] = status
        if contact_email:
            params["contact_email"] = contact_email
        if company:
            params["company"] = company
        if tags:
            params["tags"] = ",".join(tags)

        return self._make_request("GET", "/leads", params=params)

    def add_comment_to_lead(self, lead_id: str, comment: str) -> Dict[str, Any]:
        """
        Add a comment to a lead.

        Args:
            lead_id: Lead ID
            comment: Comment content

        Returns:
            Created comment data
        """
        data = {
            "comment": comment,
            "created_at": datetime.now().isoformat()
        }
        return self._make_request("POST", f"/leads/{lead_id}/comments", json=data)

    def add_attachment_to_lead(
        self,
        lead_id: str,
        file_name: str,
        file_url: str,
        file_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add an attachment to a lead.

        Args:
            lead_id: Lead ID
            file_name: File name
            file_url: URL to the file
            file_type: File type/extension

        Returns:
            Created attachment data
        """
        data = {
            "file_name": file_name,
            "file_url": file_url,
            "attached_at": datetime.now().isoformat()
        }
        if file_type:
            data["file_type"] = file_type

        return self._make_request("POST", f"/leads/{lead_id}/attachments", json=data)

    def create_category(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a lead category.

        Args:
            name: Category name
            description: Category description

        Returns:
            Created category data
        """
        data = {
            "name": name,
            "description": description or ""
        }
        return self._make_request("POST", "/categories", json=data)

    def create_predefined_tag(self, name: str, color: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a predefined tag.

        Args:
            name: Tag name
            color: Tag color (hex code)

        Returns:
            Created tag data
        """
        data = {
            "name": name,
            "color": color or "#000000"
        }
        return self._make_request("POST", "/tags", json=data)

    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        role: Optional[str] = "user"
    ) -> Dict[str, Any]:
        """
        Create a new user.

        Args:
            email: User email
            first_name: First name
            last_name: Last name
            role: User role (admin, user)

        Returns:
            Created user data
        """
        data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "role": role or "user"
        }
        return self._make_request("POST", "/users", json=data)

    def retrieve_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get user details by ID.

        Args:
            user_id: User ID

        Returns:
            User data
        """
        return self._make_request("GET", f"/users/{user_id}")

    def search_users(
        self,
        query: Optional[str] = None,
        role: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for users.

        Args:
            query: Search query
            role: Filter by role
            limit: Max results
            offset: Pagination offset

        Returns:
            List of users
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        if query:
            params["query"] = query
        if role:
            params["role"] = role

        return self._make_request("GET", "/users", params=params)

    def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming webhook events.

        Supported events:
        - lead_status_changed
        - lead_status_todo
        - lead_status_won
        - lead_status_lost
        - lead_status_cancelled
        - lead_status_standby
        - new_comment
        - new_lead

        Args:
            payload: Webhook payload

        Returns:
            Processed webhook data
        """
        event_type = payload.get("event_type")
        event_data = payload.get("data", {})

        if not event_type:
            raise NoCRMAPIError("Missing event_type in webhook payload")

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
    client = NoCRMClient(api_key="your_api_key_here")

    try:
        result = client.create_lead(
            title="New Sales Opportunity",
            description="Enterprise software deal",
            contact_name="John Doe",
            contact_email="john@example.com",
            contact_phone="+1234567890"
        )
        print("Lead created:", result)
    except NoCRMAPIError as e:
        print(f"Error: {e}")