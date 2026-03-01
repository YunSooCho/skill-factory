"""
Nethunt API Client
API Documentation: https://nethunt.com/api
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime
import json
import hmac
import hashlib


class NethuntAPIError(Exception):
    """Custom exception for Nethunt API errors."""
    pass


class NethuntClient:
    """Client for Nethunt API - CRM and contact management."""

    def __init__(self, api_key: str, base_url: str = "https://nethunt.com/api/v1"):
        """
        Initialize Nethunt API client.

        Args:
            api_key: Your Nethunt API key
            base_url: API base URL (default: https://nethunt.com/api/v1)
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
            raise NethuntAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise NethuntAPIError(f"Request failed: {str(e)}")
        except json.JSONDecodeError:
            raise NethuntAPIError("Invalid JSON response")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"message": response.text}

    def create_record(
        self,
        folder_id: str,
        fields: Dict[str, Any],
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new record.

        Args:
            folder_id: Folder ID
            fields: Field values (dict of field_id: value)
            tags: List of tags to assign

        Returns:
            Created record data
        """
        data = {
            "folder": folder_id,
            "fields": fields,
            "created_at": datetime.now().isoformat()
        }

        if tags:
            data["tags"] = tags

        return self._make_request("POST", "/records", json=data)

    def get_record(self, record_id: str) -> Dict[str, Any]:
        """
        Get record details by ID.

        Args:
            record_id: Record ID

        Returns:
            Record data
        """
        return self._make_request("GET", f"/records/{record_id}")

    def update_record(
        self,
        record_id: str,
        fields: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        add_tags: Optional[List[str]] = None,
        remove_tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update record information.

        Args:
            record_id: Record ID
            fields: Updated field values (dict of field_id: value)
            tags: Replace all tags with this list
            add_tags: Add these tags (existing tags kept)
            remove_tags: Remove these tags

        Returns:
            Updated record data
        """
        data = {}

        if fields is not None:
            data["fields"] = fields
        if tags is not None:
            data["tags"] = tags
        if add_tags:
            data["add_tags"] = add_tags
        if remove_tags:
            data["remove_tags"] = remove_tags

        data["updated_at"] = datetime.now().isoformat()

        return self._make_request("PUT", f"/records/{record_id}", json=data)

    def delete_record(self, record_id: str) -> Dict[str, Any]:
        """
        Delete a record.

        Args:
            record_id: Record ID

        Returns:
            Deletion result
        """
        return self._make_request("DELETE", f"/records/{record_id}")

    def search_records(
        self,
        folder_id: Optional[str] = None,
        query: Optional[str] = None,
        fields: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> Dict[str, Any]:
        """
        Search for records.

        Args:
            folder_id: Filter by folder ID
            query: Search query string
            fields: Filter by field values (dict of field_id: value)
            tags: Filter by tags (all tags must match)
            limit: Max results
            offset: Pagination offset
            sort_by: Field ID to sort by
            sort_order: Sort direction (asc or desc)

        Returns:
            List of matching records
        """
        params = {
            "limit": limit,
            "offset": offset,
            "sort_order": sort_order
        }

        if folder_id:
            params["folder"] = folder_id
        if query:
            params["query"] = query
        if fields:
            params["fields"] = json.dumps(fields)
        if tags:
            params["tags"] = ",".join(tags)
        if sort_by:
            params["sort_by"] = sort_by

        return self._make_request("GET", "/records", params=params)

    def create_comment(
        self,
        record_id: str,
        text: str,
        comment_type: Optional[str] = "general"
    ) -> Dict[str, Any]:
        """
        Add a comment to a record.

        Args:
            record_id: Record ID
            text: Comment text
            comment_type: Comment type (general, note, etc.)

        Returns:
            Created comment data
        """
        data = {
            "record_id": record_id,
            "text": text,
            "comment_type": comment_type,
            "created_at": datetime.now().isoformat()
        }
        return self._make_request("POST", "/comments", json=data)

    def get_comments(
        self,
        record_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get comments for a record.

        Args:
            record_id: Record ID
            limit: Max results
            offset: Pagination offset

        Returns:
            List of comments
        """
        params = {
            "record_id": record_id,
            "limit": limit,
            "offset": offset
        }
        return self._make_request("GET", "/comments", params=params)

    def update_comment(
        self,
        comment_id: str,
        text: str
    ) -> Dict[str, Any]:
        """
        Update a comment.

        Args:
            comment_id: Comment ID
            text: Updated text

        Returns:
            Updated comment data
        """
        data = {
            "text": text,
            "updated_at": datetime.now().isoformat()
        }
        return self._make_request("PUT", f"/comments/{comment_id}", json=data)

    def delete_comment(self, comment_id: str) -> Dict[str, Any]:
        """
        Delete a comment.

        Args:
            comment_id: Comment ID

        Returns:
            Deletion result
        """
        return self._make_request("DELETE", f"/comments/{comment_id}")

    def get_folders(self) -> Dict[str, Any]:
        """
        Get all folders.

        Returns:
            List of folders
        """
        return self._make_request("GET", "/folders")

    def get_folder(self, folder_id: str) -> Dict[str, Any]:
        """
        Get folder details.

        Args:
            folder_id: Folder ID

        Returns:
            Folder data
        """
        return self._make_request("GET", f"/folders/{folder_id}")

    def get_fields(self, folder_id: str) -> Dict[str, Any]:
        """
        Get fields for a folder.

        Args:
            folder_id: Folder ID

        Returns:
            List of fields
        """
        return self._make_request("GET", f"/folders/{folder_id}/fields")

    def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming webhook events.

        Supported events:
        - new_record
        - update_record
        - new_comment

        Args:
            payload: Webhook payload

        Returns:
            Processed webhook data
        """
        event_type = payload.get("event_type")
        event_data = payload.get("data", {})

        if not event_type:
            raise NethuntAPIError("Missing event_type in webhook payload")

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
    client = NethuntClient(api_key="your_api_key_here")

    try:
        result = client.create_record(
            folder_id="folder_123",
            fields={"name": "John Doe", "email": "john@example.com"}
        )
        print("Record created:", result)
    except NethuntAPIError as e:
        print(f"Error: {e}")