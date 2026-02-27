"""
ConvertKit API Client
Email marketing API for subscribers, forms, tags
"""

import requests
from typing import Dict, Optional, Any, List
import time
import json
from flask import Flask, request, jsonify


class ConvertKitClient:
    """ConvertKit V3 API Client"""

    def __init__(self, api_secret: str, base_url: str = "https://api.convertkit.com/v3"):
        """
        Initialize ConvertKit client

        Args:
            api_secret: ConvertKit API secret key
            base_url: Base URL for API requests
        """
        self.api_secret = api_secret
        self.base_url = base_url
        self.timeout = 30

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response"""
        if response.status_code == 401:
            raise ValueError("Invalid API secret")
        elif response.status_code == 403:
            raise ValueError("Access forbidden")
        elif response.status_code == 404:
            raise ValueError("Resource not found")
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            time.sleep(retry_after)
            raise ValueError(f"Rate limit exceeded. Wait {retry_after} seconds before retrying.")
        elif response.status_code >= 500:
            raise ValueError(f"Server error: {response.status_code}")

        return response.json()

    def _get_params(self) -> Dict[str, str]:
        """Get parameters with API secret"""
        return {'api_secret': self.api_secret}

    # ==================== Subscribers ====================

    def search_subscriber(self, email_address: str) -> Dict[str, Any]:
        """
        Search subscriber by email

        Args:
            email_address: Email address to search

        Returns:
            Subscriber data
        """
        url = f"{self.base_url}/subscribers"

        params = self._get_params()
        params['email_address'] = email_address

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to search subscriber: {str(e)}")

    def get_subscriber(self, subscriber_id: str) -> Dict[str, Any]:
        """
        Get subscriber by ID

        Args:
            subscriber_id: Subscriber ID

        Returns:
            Subscriber data
        """
        url = f"{self.base_url}/subscribers/{subscriber_id}"

        params = self._get_params()

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get subscriber: {str(e)}")

    def add_subscriber_to_form(
        self,
        form_id: str,
        email: str,
        first_name: str = None,
        fields: Dict[str, Any] = None,
        tags: List[int] = None
    ) -> Dict[str, Any]:
        """
        Add subscriber to form

        Args:
            form_id: Form ID
            email: Member email address
            first_name: Member first name (optional)
            fields: Custom fields (optional)
            tags: Tag IDs (optional)

        Returns:
            Subscriber data
        """
        url = f"{self.base_url}/forms/{form_id}/subscribe"

        data = {
            'api_secret': self.api_secret,
            'email': email
        }

        if first_name:
            data['first_name'] = first_name
        if fields:
            data['fields'] = fields
        if tags:
            data['tags'] = tags

        try:
            response = requests.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to add subscriber to form: {str(e)}")

    def update_subscriber(
        self,
        subscriber_id: str,
        email: str = None,
        first_name: str = None,
        fields: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Update subscriber

        Args:
            subscriber_id: Subscriber ID
            email: New email address (optional)
            first_name: New first name (optional)
            fields: Custom fields (optional)

        Returns:
            Updated subscriber data
        """
        url = f"{self.base_url}/subscribers/{subscriber_id}"

        data = {'api_secret': self.api_secret}

        if email:
            data['email_address'] = email
        if first_name:
            data['first_name'] = first_name
        if fields:
            data['fields'] = fields

        try:
            response = requests.put(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to update subscriber: {str(e)}")

    def unsubscribe_subscriber(self, subscriber_id: str) -> bool:
        """
        Cancel subscription for subscriber

        Args:
            subscriber_id: Subscriber ID

        Returns:
            True if unsubscribed successfully
        """
        url = f"{self.base_url}/subscribers/{subscriber_id}/unsubscribe"

        try:
            response = requests.post(url, json={'api_secret': self.api_secret}, timeout=self.timeout)
            if response.status_code == 200:
                return True
            raise ValueError(f"Unsubscribe failed with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to unsubscribe subscriber: {str(e)}")

    # ==================== Tags ====================

    def add_tag_to_subscriber(self, subscriber_id: str, tag_id: str) -> Dict[str, Any]:
        """
        Add tag to subscriber

        Args:
            subscriber_id: Subscriber ID
            tag_id: Tag ID

        Returns:
            Tag assignment data
        """
        url = f"{self.base_url}/subscribers/{subscriber_id}/tags"

        data = {
            'api_secret': self.api_secret,
            'tag_id': tag_id
        }

        try:
            response = requests.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to add tag to subscriber: {str(e)}")

    def remove_tag_from_subscriber(self, subscriber_id: str, tag_id: str) -> bool:
        """
        Remove tag from subscriber

        Args:
            subscriber_id: Subscriber ID
            tag_id: Tag ID

        Returns:
            True if tag removed successfully
        """
        url = f"{self.base_url}/subscribers/{subscriber_id}/tags/{tag_id}"

        try:
            response = requests.delete(url, params=self._get_params(), timeout=self.timeout)
            if response.status_code == 200:
                return True
            raise ValueError(f"Remove tag failed with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to remove tag from subscriber: {str(e)}")


class ConvertKitWebhookHandler:
    """Webhook handler for ConvertKit events"""

    @staticmethod
    def parse_webhook_event(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse ConvertKit webhook event

        Args:
            data: Webhook payload

        Returns:
            Parsed event data
        """
        return {
            'event_type': data.get('type'),
            'subscriber': data.get('subscriber', {}),
            'timestamp': data.get('timestamp')
        }

    @staticmethod
    def handle_subscriber_activated(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle subscriber activated webhook

        Args:
            data: Webhook payload

        Returns:
            Parsed subscriber data
        """
        subscriber = data.get('subscriber', {})
        return {
            'subscriber_id': subscriber.get('id'),
            'email': subscriber.get('email_address'),
            'first_name': subscriber.get('first_name'),
            'activated_at': data.get('timestamp')
        }

    @staticmethod
    def handle_subscriber_tagged(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle subscriber tagged webhook

        Args:
            data: Webhook payload

        Returns:
            Parsed event data
        """
        subscriber = data.get('subscriber', {})
        return {
            'subscriber_id': subscriber.get('id'),
            'tag': data.get('tag'),
            'email': subscriber.get('email_address')
        }

    @staticmethod
    def handle_subscriber_untagged(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle subscriber untagged webhook

        Args:
            data: Webhook payload

        Returns:
            Parsed event data
        """
        subscriber = data.get('subscriber', {})
        return {
            'subscriber_id': subscriber.get('id'),
            'tag': data.get('tag'),
            'email': subscriber.get('email_address')
        }

    @staticmethod
    def handle_form_subscription(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle form subscription webhook

        Args:
            data: Webhook payload

        Returns:
            Parsed event data
        """
        subscriber = data.get('subscriber', {})
        return {
            'subscriber_id': subscriber.get('id'),
            'form_id': data.get('form_id'),
            'email': subscriber.get('email_address'),
            'subscribed_at': data.get('timestamp')
        }

    @staticmethod
    def handle_unsubscribe(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle unsubscribe webhook

        Args:
            data: Webhook payload

        Returns:
            Parsed event data
        """
        subscriber = data.get('subscriber', {})
        return {
            'subscriber_id': subscriber.get('id'),
            'email': subscriber.get('email_address'),
            'unsubscribed_at': data.get('timestamp')
        }

    @staticmethod
    def handle_purchase(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle purchase webhook

        Args:
            data: Webhook payload

        Returns:
            Parsed purchase data
        """
        subscriber = data.get('subscriber', {})
        purchase = data.get('purchase', {})
        return {
            'subscriber_id': subscriber.get('id'),
            'purchase_id': purchase.get('id'),
            'transaction_id': purchase.get('transaction_id'),
            'email': subscriber.get('email_address'),
            'amount': purchase.get('total')
        }

    @staticmethod
    def handle_email_bounce(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle email bounce webhook

        Args:
            data: Webhook payload

        Returns:
            Parsed bounce data
        """
        subscriber = data.get('subscriber', {})
        return {
            'subscriber_id': subscriber.get('id'),
            'email': subscriber.get('email_address'),
            'bounce_reason': data.get('bounce_reason'),
            'bounced_at': data.get('timestamp')
        }


# Flask Webhook Server Example
def create_webhook_server(webhook_secret: str = None, host: str = '0.0.0.0', port: int = 8080):
    """
    Create Flask server for ConvertKit webhooks

    Args:
        webhook_secret: Webhook secret for verification (optional)
        host: Server host
        port: Server port
    """
    app = Flask(__name__)

    @app.route('/webhook/convertkit', methods=['POST'])
    def handle_webhook():
        """Handle ConvertKit webhook"""
        try:
            data = request.json
            event_type = data.get('type')

            if event_type == 'subscriber.subscribed':
                parsed = ConvertKitWebhookHandler.handle_subscriber_activated(data)
                print(f"Subscriber activated: {parsed}")
            elif event_type == 'subscriber.subscribed_to_form':
                parsed = ConvertKitWebhookHandler.handle_form_subscription(data)
                print(f"Form subscription: {parsed}")
            elif event_type == 'subscriber.tag_added':
                parsed = ConvertKitWebhookHandler.handle_subscriber_tagged(data)
                print(f"Subscriber tagged: {parsed}")
            elif event_type == 'subscriber.tag_removed':
                parsed = ConvertKitWebhookHandler.handle_subscriber_untagged(data)
                print(f"Subscriber untagged: {parsed}")
            elif event_type == 'subscribe.unsubscribed':
                parsed = ConvertKitWebhookHandler.handle_unsubscribe(data)
                print(f"Unsubscribe: {parsed}")
            elif event_type == 'purchase.created':
                parsed = ConvertKitWebhookHandler.handle_purchase(data)
                print(f"Purchase made: {parsed}")
            elif event_type == 'subscriber.email_bounced':
                parsed = ConvertKitWebhookHandler.handle_email_bounce(data)
                print(f"Email bounced: {parsed}")

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
        print("  Search subscriber: python convertkit_client.py search <api_secret> <email>")
        print("  Get subscriber: python convertkit_client.py get <api_secret> <subscriber_id>")
        print("  Add to form: python convertkit_client.py add-form <api_secret> <form_id> <email>")
        print("  Update subscriber: python convertkit_client.py update <api_secret> <subscriber_id> [email] [name]")
        print("  Unsubscribe: python convertkit_client.py unsubscribe <api_secret> <subscriber_id>")
        print("  Add tag: python convertkit_client.py add-tag <api_secret> <subscriber_id> <tag_id>")
        print("  Remove tag: python convertkit_client.py remove-tag <api_secret> <subscriber_id> <tag_id>")
        print("  Start webhook server: python convertkit_client.py webhook [port]")
        sys.exit(1)

    api_secret = sys.argv[2]

    client = ConvertKitClient(api_secret)

    if sys.argv[1] == "search":
        email = sys.argv[3]
        result = client.search_subscriber(email)
        print(f"Subscriber: {result}")

    elif sys.argv[1] == "get":
        subscriber_id = sys.argv[3]
        result = client.get_subscriber(subscriber_id)
        print(f"Subscriber: {result}")

    elif sys.argv[1] == "add-form":
        form_id = sys.argv[3]
        email = sys.argv[4]
        result = client.add_subscriber_to_form(form_id, email)
        print(f"Subscribed: {result}")

    elif sys.argv[1] == "update":
        subscriber_id = sys.argv[3]
        email = sys.argv[4] if len(sys.argv) > 4 else None
        first_name = sys.argv[5] if len(sys.argv) > 5 else None
        result = client.update_subscriber(subscriber_id, email, first_name)
        print(f"Updated: {result}")

    elif sys.argv[1] == "unsubscribe":
        subscriber_id = sys.argv[3]
        success = client.unsubscribe_subscriber(subscriber_id)
        if success:
            print(f"Subscriber {subscriber_id} unsubscribed successfully")

    elif sys.argv[1] == "add-tag":
        subscriber_id = sys.argv[3]
        tag_id = sys.argv[4]
        result = client.add_tag_to_subscriber(subscriber_id, tag_id)
        print(f"Tag added: {result}")

    elif sys.argv[1] == "remove-tag":
        subscriber_id = sys.argv[3]
        tag_id = sys.argv[4]
        success = client.remove_tag_from_subscriber(subscriber_id, tag_id)
        if success:
            print(f"Tag removed from {subscriber_id}")

    elif sys.argv[1] == "webhook":
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        print(f"Starting webhook server on port {port}...")
        create_webhook_server(port=port)