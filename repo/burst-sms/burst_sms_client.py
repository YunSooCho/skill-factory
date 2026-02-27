"""
Burst SMS API Client
SMS sending and webhook handling
"""

import requests
from typing import Dict, Optional, Any, List
import time
import hmac
import hashlib
import json
from flask import Flask, request, jsonify


class BurstSMSClient:
    """Burst SMS API Client for SMS operations"""

    def __init__(self, api_key: str, base_url: str = "https://api.transmitsms.com"):
        """
        Initialize Burst SMS client

        Args:
            api_key: Burst SMS API key
            base_url: Base URL for API requests
        """
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = 30

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response"""
        if response.status_code == 401:
            raise ValueError("Invalid API key")
        elif response.status_code == 403:
            raise ValueError("Access forbidden - insufficient credits or permissions")
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            time.sleep(retry_after)
            raise ValueError(f"Rate limit exceeded. Wait {retry_after} seconds before retrying.")
        elif response.status_code >= 500:
            raise ValueError(f"Server error: {response.status_code}")

        return response.json()

    def send_sms(
        self,
        to: str,
        message: str,
        from_: str = None,
        message_id: str = None
    ) -> Dict[str, Any]:
        """
        Send SMS message

        Args:
            to: Recipient phone number (with country code, e.g., +821012345678)
            message: SMS message content (max 160 chars per segment)
            from_: Sender ID (optional)
            message_id: Custom message ID (optional)

        Returns:
            Dict with response including:
                - success: Boolean
                - message_id: Message ID
                - recipients: List of recipient results
                - cost: SMS cost
        """
        url = f"{self.base_url}/send-sms.json"

        data = {
            'api_key': self.api_key,
            'to': to,
            'message': message
        }

        if from_ is not None:
            data['from'] = from_
        if message_id is not None:
            data['message_id'] = message_id

        try:
            response = requests.post(url, data=data, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to send SMS: {str(e)}")

    def retrieve_messages(
        self,
        message_id: str = None,
        from_: str = None,
        to: str = None,
        date_from: str = None,
        date_to: str = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Retrieve sent messages

        Args:
            message_id: Filter by message ID (optional)
            from_: Filter by sender (optional)
            to: Filter by recipient (optional)
            date_from: Filter by start date (YYYY-MM-DD)
            date_to: Filter by end date (YYYY-MM-DD)
            limit: Number of messages to return
            offset: Offset for pagination

        Returns:
            Dict with messages list
        """
        url = f"{self.base_url}/get-sms.json"

        params = {
            'api_key': self.api_key,
            'limit': limit,
            'offset': offset
        }

        if message_id is not None:
            params['message_id'] = message_id
        if from_ is not None:
            params['from'] = from_
        if to is not None:
            params['to'] = to
        if date_from is not None:
            params['date_from'] = date_from
        if date_to is not None:
            params['date_to'] = date_to

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to retrieve messages: {str(e)}")

    def list_related_messages(
        self,
        message_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List messages related to a specific message

        Args:
            message_id: Original message ID
            limit: Number of messages to return
            offset: Offset for pagination

        Returns:
            Dict with related messages list
        """
        url = f"{self.base_url}/get-sms.json"

        params = {
            'api_key': self.api_key,
            'message_id': message_id,
            'limit': limit,
            'offset': offset
        }

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to list related messages: {str(e)}")

    def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """
        Get status of a specific message

        Args:
            message_id: Message ID

        Returns:
            Dict with message status
        """
        url = f"{self.base_url}/get-sms.json"

        params = {
            'api_key': self.api_key,
            'message_id': message_id
        }

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get message status: {str(e)}")


class BurstSMSWebhookHandler:
    """Webhook handler for Burst SMS events"""

    @staticmethod
    def verify_webhook_signature(payload: bytes, signature: str, webhook_secret: str) -> bool:
        """
        Verify webhook signature

        Args:
            payload: Raw request payload
            signature: X-BurstSMS-Signature header
            webhook_secret: Webhook secret key

        Returns:
            True if signature is valid
        """
        if not signature or not webhook_secret:
            return False

        # Calculate expected signature
        expected_signature = hmac.new(
            webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    @staticmethod
    def parse_incoming_message(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse incoming message webhook data

        Args:
            data: Webhook payload

        Returns:
            Parsed message data
        """
        return {
            'message_id': data.get('message_id'),
            'from': data.get('from'),
            'to': data.get('to'),
            'message': data.get('message'),
            'timestamp': data.get('timestamp'),
            'keyword': data.get('keyword'),
            'custom': data.get('custom')
        }

    @staticmethod
    def parse_new_message(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse new message trigger webhook data

        Args:
            data: Webhook payload

        Returns:
            Parsed message data
        """
        return {
            'message_id': data.get('message_id'),
            'status': data.get('status'),
            'recipient': data.get('recipient'),
            'sent_at': data.get('sent_at'),
            'delivered_at': data.get('delivered_at'),
            'cost': data.get('cost')
        }


# Flask Webhook Server Example
def create_webhook_server(webhook_secret: str = None, host: str = '0.0.0.0', port: int = 8080):
    """
    Create Flask server for Burst SMS webhooks

    Args:
        webhook_secret: Webhook secret for signature verification
        host: Server host
        port: Server port
    """
    app = Flask(__name__)

    @app.route('/webhook/received-message', methods=['POST'])
    def handle_received_message():
        """Handle received message webhook"""
        if webhook_secret:
            signature = request.headers.get('X-BurstSMS-Signature')
            payload = request.data

            if not BurstSMSWebhookHandler.verify_webhook_signature(payload, signature, webhook_secret):
                return jsonify({'error': 'Invalid signature'}), 401

        try:
            data = request.json
            parsed = BurstSMSWebhookHandler.parse_incoming_message(data)
            print(f"Received message: {parsed}")
            return jsonify({'status': 'success'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/webhook/new-message', methods=['POST'])
    def handle_new_message():
        """Handle new message webhook"""
        if webhook_secret:
            signature = request.headers.get('X-BurstSMS-Signature')
            payload = request.data

            if not BurstSMSWebhookHandler.verify_webhook_signature(payload, signature, webhook_secret):
                return jsonify({'error': 'Invalid signature'}), 401

        try:
            data = request.json
            parsed = BurstSMSWebhookHandler.parse_new_message(data)
            print(f"New message: {parsed}")
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
        print("  Send SMS: python burst_sms_client.py send <api_key> <to_number> <message> [sender_id]")
        print("  Get messages: python burst_sms_client.py get <api_key>")
        print("  Get message status: python burst_sms_client.py status <api_key> <message_id>")
        print("  Start webhook server: python burst_sms_client.py webhook [webhook_secret] [port]")
        sys.exit(1)

    api_key = sys.argv[2]

    if sys.argv[1] == "send":
        to = sys.argv[3]
        message = sys.argv[4]
        from_ = sys.argv[5] if len(sys.argv) > 5 else None

        client = BurstSMSClient(api_key)
        result = client.send_sms(to, message, from_=from_)

        if result.get('success'):
            print(f"SMS sent successfully")
            print(f"Message ID: {result.get('message_id')}")
            print(f"Cost: {result.get('cost')}")
        else:
            print(f"Failed to send SMS: {result}")

    elif sys.argv[1] == "get":
        message_id = sys.argv[3] if len(sys.argv) > 3 else None

        client = BurstSMSClient(api_key)
        result = client.retrieve_messages(message_id=message_id)

        messages = result.get('messages', result.get('sms_list', []))
        print(f"Total messages: {len(messages)}")
        for msg in messages[:10]:
            print(f"  - {msg.get('message_id')}: {msg.get('status')}")

    elif sys.argv[1] == "status":
        message_id = sys.argv[3]

        client = BurstSMSClient(api_key)
        result = client.get_message_status(message_id)

        print(f"Message ID: {result.get('message_id')}")
        print(f"Status: {result.get('status')}")
        print(f"Recipient: {result.get('recipient')}")

    elif sys.argv[1] == "webhook":
        webhook_secret = sys.argv[3] if len(sys.argv) > 3 else None
        port = int(sys.argv[4]) if len(sys.argv) > 4 else 8080

        print(f"Starting webhook server on port {port}...")
        if webhook_secret:
            print(f"Webhook signature verification enabled")
        create_webhook_server(webhook_secret, port=port)