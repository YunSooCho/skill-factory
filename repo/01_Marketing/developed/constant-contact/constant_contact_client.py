"""
Constant Contact API Client
Email Marketing API for contacts, lists, tags
"""

import requests
from typing import Dict, Optional, Any, List
import time
import hmac
import hashlib
import json
from flask import Flask, request, jsonify


class ConstantContactClient:
    """Constant Contact V3 API Client"""

    def __init__(self, api_key: str, base_url: str = "https://api.cc.email/v3"):
        """
        Initialize Constant Contact client

        Args:
            api_key: Constant Contact API key (OAuth access token)
            base_url: Base URL for API requests
        """
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = 30

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response"""
        if response.status_code == 401:
            raise ValueError("Invalid API key or token expired")
        elif response.status_code == 403:
            raise ValueError("Access forbidden")
        elif response.status_code == 404:
            raise ValueError("Resource not found")
        elif response.status_code == 409:
            raise ValueError("Resource already exists")
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            time.sleep(retry_after)
            raise ValueError(f"Rate limit exceeded. Wait {retry_after} seconds before retrying.")
        elif response.status_code >= 500:
            raise ValueError(f"Server error: {response.status_code}")

        return response.json()

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with API key"""
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    # ==================== Contacts ====================

    def create_contact(
        self,
        email: str,
        first_name: str = None,
        last_name: str = None,
        phone_number: str = None,
        list_ids: List[str] = None,
        custom_fields: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a new contact

        Args:
            email: Contact email address
            first_name: First name (optional)
            last_name: Last name (optional)
            phone_number: Phone number (optional)
            list_ids: List IDs to add contact to (optional)
            custom_fields: Custom field values (optional)

        Returns:
            Created contact data
        """
        url = f"{self.base_url}/contacts"

        contact_data = {
            'email_address': {
                'address': email,
                'permission_to_send': 'implicit'
            }
        }

        if first_name:
            contact_data['first_name'] = first_name
        if last_name:
            contact_data['last_name'] = last_name
        if phone_number:
            contact_data['phone_numbers'] = [{'phone_number': phone_number}]
        if list_ids:
            contact_data['list_memberships'] = list_ids
        if custom_fields:
            contact_data['custom_fields'] = [
                {'custom_field_id': key, 'value': value}
                for key, value in custom_fields.items()
            ]

        try:
            response = requests.post(url, json=contact_data, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to create contact: {str(e)}")

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Get contact by ID

        Args:
            contact_id: Contact ID

        Returns:
            Contact data
        """
        url = f"{self.base_url}/contacts/{contact_id}"

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get contact: {str(e)}")

    def search_contact(
        self,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Search contacts by email or name

        Args:
            email: Email address to search (optional)
            first_name: First name to search (optional)
            last_name: Last name to search (optional)
            limit: Maximum results to return

        Returns:
            Dict with contacts
        """
        url = f"{self.base_url}/contacts"

        params = {'limit': limit}

        if email:
            params['email'] = email
        if first_name:
            params['first_name'] = first_name
        if last_name:
            params['last_name'] = last_name

        try:
            response = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to search contacts: {str(e)}")

    def update_contact(
        self,
        contact_id: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        phone_number: str = None,
        list_ids: List[str] = None
    ) -> Dict[str, Any]:
        """
        Update contact

        Args:
            contact_id: Contact ID
            email: New email address (optional)
            first_name: New first name (optional)
            last_name: New last name (optional)
            phone_number: New phone number (optional)
            list_ids: New list memberships (optional)

        Returns:
            Updated contact data
        """
        url = f"{self.base_url}/contacts/{contact_id}"

        update_data = {}

        if email:
            update_data['email_address'] = {
                'address': email,
                'permission_to_send': 'implicit'
            }
        if first_name is not None:
            update_data['first_name'] = first_name
        if last_name is not None:
            update_data['last_name'] = last_name
        if phone_number:
            update_data['phone_numbers'] = [{'phone_number': phone_number}]
        if list_ids is not None:
            update_data['list_memberships'] = list_ids

        try:
            response = requests.patch(url, json=update_data, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to update contact: {str(e)}")

    def delete_contact(self, contact_id: str) -> bool:
        """
        Delete contact

        Args:
            contact_id: Contact ID

        Returns:
            True if deleted successfully
        """
        url = f"{self.base_url}/contacts/{contact_id}"

        try:
            response = requests.delete(url, headers=self._get_headers(), timeout=self.timeout)
            if response.status_code == 204:
                return True
            raise ValueError(f"Delete failed with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to delete contact: {str(e)}")

    def get_contact_activity_detail(
        self,
        contact_id: str,
        activity_type: str = None
    ) -> Dict[str, Any]:
        """
        Get contact activity details

        Args:
            contact_id: Contact ID
            activity_type: Activity type filter (optional)

        Returns:
            Activity data
        """
        url = f"{self.base_url}/contacts/{contact_id}/activities"

        params = {}
        if activity_type:
            params['activity_type'] = activity_type

        try:
            response = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get contact activity: {str(e)}")

    def get_contact_action_summary(
        self,
        contact_id: str
    ) -> Dict[str, Any]:
        """
        Get contact action summary

        Args:
            contact_id: Contact ID

        Returns:
            Action summary data
        """
        url = f"{self.base_url}/contacts/{contact_id}/report_summary"

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get contact action summary: {str(e)}")

    def add_contact_to_list(
        self,
        contact_id: str,
        list_id: str
    ) -> Dict[str, Any]:
        """
        Add contact to list

        Args:
            contact_id: Contact ID
            list_id: List ID

        Returns:
            Updated contact data
        """
        url = f"{self.base_url}/contacts/{contact_id}"

        update_data = {
            'list_memberships': [list_id]
        }

        try:
            response = requests.patch(url, json=update_data, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to add contact to list: {str(e)}")

    # ==================== Contact Lists ====================

    def create_contact_list(
        self,
        name: str,
        description: str = None
    ) -> Dict[str, Any]:
        """
        Create a contact list

        Args:
            name: List name
            description: List description (optional)

        Returns:
            Created list data
        """
        url = f"{self.base_url}/contact_lists"

        list_data = {
            'name': name
        }

        if description:
            list_data['description'] = description

        try:
            response = requests.post(url, json=list_data, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to create contact list: {str(e)}")

    def get_contact_list(self, list_id: str) -> Dict[str, Any]:
        """
        Get contact list by ID

        Args:
            list_id: List ID

        Returns:
            List data
        """
        url = f"{self.base_url}/contact_lists/{list_id}"

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get contact list: {str(e)}")

    def search_contact_list(
        self,
        name: str = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Search contact lists

        Args:
            name: List name to search (optional)
            limit: Maximum results to return

        Returns:
            Dict with contact lists
        """
        url = f"{self.base_url}/contact_lists"

        params = {'limit': limit}

        if name:
            params['name'] = name

        try:
            response = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to search contact lists: {str(e)}")

    def update_contact_list(
        self,
        list_id: str,
        name: str = None,
        description: str = None
    ) -> Dict[str, Any]:
        """
        Update contact list

        Args:
            list_id: List ID
            name: New name (optional)
            description: New description (optional)

        Returns:
            Updated list data
        """
        url = f"{self.base_url}/contact_lists/{list_id}"

        update_data = {}
        if name is not None:
            update_data['name'] = name
        if description is not None:
            update_data['description'] = description

        try:
            response = requests.patch(url, json=update_data, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to update contact list: {str(e)}")

    def delete_contact_list(self, list_id: str) -> bool:
        """
        Delete contact list

        Args:
            list_id: List ID

        Returns:
            True if deleted successfully
        """
        url = f"{self.base_url}/contact_lists/{list_id}"

        try:
            response = requests.delete(url, headers=self._get_headers(), timeout=self.timeout)
            if response.status_code == 204:
                return True
            raise ValueError(f"Delete failed with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to delete contact list: {str(e)}")

    def get_average_open_and_click_rate(self, list_id: str) -> Dict[str, Any]:
        """
        Get average open and click rate for list

        Args:
            list_id: List ID

        Returns:
            Average rates data
        """
        url = f"{self.base_url}/contact_lists/{list_id}/report_summary"

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get average rates: {str(e)}")

    # ==================== Tags ====================

    def create_tag(self, name: str) -> Dict[str, Any]:
        """
        Create a tag

        Args:
            name: Tag name

        Returns:
            Created tag data
        """
        url = f"{self.base_url}/contact_tags"

        tag_data = {
            'name': name
        }

        try:
            response = requests.post(url, json=tag_data, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to create tag: {str(e)}")

    def get_tag_detail(self, tag_id: str) -> Dict[str, Any]:
        """
        Get tag detail

        Args:
            tag_id: Tag ID

        Returns:
            Tag data
        """
        url = f"{self.base_url}/contact_tags/{tag_id}"

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get tag detail: {str(e)}")

    def update_tag(self, tag_id: str, name: str) -> Dict[str, Any]:
        """
        Update tag

        Args:
            tag_id: Tag ID
            name: New name

        Returns:
            Updated tag data
        """
        url = f"{self.base_url}/contact_tags/{tag_id}"

        update_data = {
            'name': name
        }

        try:
            response = requests.patch(url, json=update_data, headers=self._get_headers(), timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to update tag: {str(e)}")

    def delete_tag(self, tag_id: str) -> bool:
        """
        Delete tag

        Args:
            tag_id: Tag ID

        Returns:
            True if deleted successfully
        """
        url = f"{self.base_url}/contact_tags/{tag_id}"

        try:
            response = requests.delete(url, headers=self._get_headers(), timeout=self.timeout)
            if response.status_code == 204:
                return True
            raise ValueError(f"Delete failed with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to delete tag: {str(e)}")


class ConstantContactWebhookHandler:
    """Webhook handler for Constant Contact events"""

    @staticmethod
    def parse_webhook_event(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Constant Contact webhook event

        Args:
            data: Webhook payload

        Returns:
            Parsed event data
        """
        return {
            'event_type': data.get('type'),
            'contact_id': data.get('contact_id'),
            'email': data.get('email_address'),
            'timestamp': data.get('timestamp'),
            'campaign_id': data.get('campaign_id'),
            'details': data.get('details', {})
        }

    @staticmethod
    def handle_new_contact(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle new contact webhook

        Args:
            data: Webhook payload

        Returns:
            Parsed contact data
        """
        return {
            'contact_id': data.get('contact_id'),
            'email_address': data.get('email_address'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'created_at': data.get('created_at')
        }

    @staticmethod
    def handle_updated_contact(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle updated contact webhook

        Args:
            data: Webhook payload

        Returns:
            Parsed contact data
        """
        return {
            'contact_id': data.get('contact_id'),
            'email_address': data.get('email_address'),
            'updated_fields': data.get('updated_fields', []),
            'updated_at': data.get('updated_at')
        }


# Flask Webhook Server Example
def create_webhook_server(webhook_secret: str = None, host: str = '0.0.0.0', port: int = 8080):
    """
    Create Flask server for Constant Contact webhooks

    Args:
        webhook_secret: Webhook secret for verification (optional)
        host: Server host
        port: Server port
    """
    app = Flask(__name__)

    @app.route('/webhook/constant-contact', methods=['POST'])
    def handle_webhook():
        """Handle Constant Contact webhook"""
        try:
            data = request.json
            event_type = data.get('type')

            if event_type == 'new_contact':
                parsed = ConstantContactWebhookHandler.handle_new_contact(data)
                print(f"New contact: {parsed}")
            elif event_type == 'updated_contact':
                parsed = ConstantContactWebhookHandler.handle_updated_contact(data)
                print(f"Updated contact: {parsed}")
            elif event_type == 'email_open':
                print(f"Email opened by {data.get('email_address')}")
            elif event_type == 'email_click':
                print(f"Email clicked by {data.get('email_address')}")
            elif event_type == 'email_bounce':
                print(f"Email bounced for {data.get('email_address')}")
            elif event_type == 'email_optout':
                print(f"Email optout by {data.get('email_address')}")

            return jsonify({'status': 'success'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({'status': 'healthy'}), 200

    app.run(host=host, port=port)


# CLI Example
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage:")
        print("  Create contact: python constant_contact_client.py create <api_key> <email> [first_name] [last_name]")
        print("  Get contact: python constant_contact_client.py get <api_key> <contact_id>")
        print("  Search contact: python constant_contact_client.py search <api_key> <email>")
        print("  Update contact: python constant_contact_client.py update <api_key> <contact_id> [email] [first_name]")
        print("  Delete contact: python constant_contact_client.py delete <api_key> <contact_id>")
        print("  Create list: python constant_contact_client.py create-list <api_key> <name>")
        print("  Get list: python constant_contact_client.py get-list <api_key> <list_id>")
        print("  Create tag: python constant_contact_client.py create-tag <api_key> <name>")
        print("  Start webhook server: python constant_contact_client.py webhook [port]")
        sys.exit(1)

    api_key = sys.argv[2]

    client = ConstantContactClient(api_key)

    if sys.argv[1] == "create":
        email = sys.argv[3]
        first_name = sys.argv[4] if len(sys.argv) > 4 else None
        last_name = sys.argv[5] if len(sys.argv) > 5 else None

        contact = client.create_contact(email, first_name, last_name)
        print(f"Contact created: {contact}")

    elif sys.argv[1] == "get":
        contact_id = sys.argv[3]
        contact = client.get_contact(contact_id)
        print(f"Contact: {contact}")

    elif sys.argv[1] == "search":
        email = sys.argv[3]
        result = client.search_contact(email=email)
        print(f"Search result: {result}")

    elif sys.argv[1] == "update":
        contact_id = sys.argv[3]
        email = sys.argv[4] if len(sys.argv) > 4 else None
        first_name = sys.argv[5] if len(sys.argv) > 5 else None

        contact = client.update_contact(contact_id, email, first_name)
        print(f"Contact updated: {contact}")

    elif sys.argv[1] == "delete":
        contact_id = sys.argv[3]
        success = client.delete_contact(contact_id)
        if success:
            print(f"Contact {contact_id} deleted successfully")

    elif sys.argv[1] == "create-list":
        name = sys.argv[3]
        list_data = client.create_contact_list(name)
        print(f"List created: {list_data}")

    elif sys.argv[1] == "get-list":
        list_id = sys.argv[3]
        list_data = client.get_contact_list(list_id)
        print(f"List: {list_data}")

    elif sys.argv[1] == "create-tag":
        name = sys.argv[3]
        tag_data = client.create_tag(name)
        print(f"Tag created: {tag_data}")

    elif sys.argv[1] == "webhook":
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        print(f"Starting webhook server on port {port}...")
        create_webhook_server(port=port)