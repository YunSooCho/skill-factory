"""
Frictio API Client
Sales enablement platform focused on triggers/webhooks

Note: Frictio provides webhook triggers but no direct API actions in the Yoom integration.
This module provides webhook verification and trigger handling capabilities.

Yoom Integration:
- 0 API Actions
- 3 Triggers:
  1. Meeting ended
  2. Playbook execution result updated
  3. Playbook generated
"""

import hmac
import hashlib
import json
from typing import Dict, Any, Optional, Callable
from enum import Enum


class FrictioEventType(Enum):
    """Frictio webhook event types"""
    MEETING_ENDED = "meeting_ended"
    PLAYBOOK_RESULT_UPDATED = "playbook_result_updated"
    PLAYBOOK_GENERATED = "playbook_generated"


class FrictioWebhookError(Exception):
    """Custom exception for Frictio webhook errors"""
    pass


class FrictioClient:
    """
    Frictio Webhook Handler
    Handles webhook verification, parsing, and trigger routing
    """

    def __init__(self, webhook_secret: Optional[str] = None):
        """
        Initialize Frictio webhook client

        Args:
            webhook_secret: Secret key for webhook signature verification (optional)
        """
        self.webhook_secret = webhook_secret
        self.event_handlers = {}

    def verify_webhook_signature(self, payload: bytes, signature: str,
                                 algorithm: str = 'sha256') -> bool:
        """
        Verify webhook signature for security

        Args:
            payload: Raw request body
            signature: Signature from request header
            algorithm: Hash algorithm to use

        Returns:
            True if signature is valid

        Raises:
            FrictioWebhookError: If verification fails
        """
        if not self.webhook_secret:
            raise FrictioWebhookError("Webhook secret not configured")

        # Calculate expected signature
        expected_sig = hmac.new(
            self.webhook_secret.encode(),
            payload,
            getattr(hashlib, algorithm)
        ).hexdigest()

        # Compare signatures securely
        if not hmac.compare_digest(expected_sig, signature):
            raise FrictioWebhookError("Invalid webhook signature")

        return True

    def register_event_handler(self, event_type: FrictioEventType,
                               handler: Callable[[Dict[str, Any]], None]):
        """
        Register a handler for a specific event type

        Args:
            event_type: Event type to handle
            handler: Callback function that receives event data
        """
        self.event_handlers[event_type.value] = handler

    def unregister_event_handler(self, event_type: FrictioEventType):
        """Unregister an event handler"""
        if event_type.value in self.event_handlers:
            del self.event_handlers[event_type.value]

    def parse_webhook_event(self, payload: bytes, signature: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse and validate incoming webhook event

        Args:
            payload: Request body bytes
            signature: Webhook signature (optional if not configured)

        Returns:
            Parsed event data

        Raises:
            FrictioWebhookError: If parsing or validation fails
        """
        # Verify signature if secret is configured
        if self.webhook_secret:
            if not signature:
                raise FrictioWebhookError("Missing webhook signature")

            # Handle different signature formats
            # Some APIs prepend with algorithm name (e.g., "sha256=...")
            if '=' in signature:
                signature = signature.split('=', 1)[1]

            if not self.verify_webhook_signature(payload, signature):
                raise FrictioWebhookError("Invalid webhook signature")

        # Parse JSON payload
        try:
            event_data = json.loads(payload.decode('utf-8'))
        except json.JSONDecodeError as e:
            raise FrictioWebhookError(f"Invalid JSON payload: {str(e)}")

        # Validate event structure
        if 'event_type' not in event_data:
            raise FrictioWebhookError("Missing event_type in webhook payload")

        return event_data

    def handle_webhook(self, payload: bytes, signature: Optional[str] = None) -> Dict[str, Any]:
        """
        Process incoming webhook and route to appropriate handler

        Args:
            payload: Request body bytes
            signature: Webhook signature

        Returns:
            Response data with processing result

        Raises:
            FrictioWebhookError: If processing fails
        """
        # Parse and validate event
        event_data = self.parse_webhook_event(payload, signature)
        event_type = event_data.get('event_type')

        # Route to handler
        if event_type in self.event_handlers:
            try:
                handler = self.event_handlers[event_type]
                handler(event_data)
                return {
                    'success': True,
                    'message': f'Event {event_type} handled successfully',
                    'event_type': event_type
                }
            except Exception as e:
                raise FrictioWebhookError(f"Handler error: {str(e)}")
        else:
            # Log unhandled event
            return {
                'success': True,
                'message': f'No handler registered for event {event_type}',
                'event_type': event_type,
                'handled': False
            }

    # ========== SPECIFIC EVENT HANDLERS ==========

    def on_meeting_ended(self, handler: Callable[[Dict[str, Any]], None]):
        """
        Register handler for meeting ended events

        Event data structure example:
        {
            "event_type": "meeting_ended",
            "meeting_id": "string",
            "participant_count": 0,
            "duration_minutes": 0,
            "timestamp": "2025-02-28T00:00:00Z"
        }
        """
        self.register_event_handler(FrictioEventType.MEETING_ENDED, handler)

    def on_playbook_result_updated(self, handler: Callable[[Dict[str, Any]], None]):
        """
        Register handler for playbook result updated events

        Event data structure example:
        {
            "event_type": "playbook_result_updated",
            "playbook_id": "string",
            "playbook_name": "string",
            "result": {},
            "timestamp": "2025-02-28T00:00:00Z"
        }
        """
        self.register_event_handler(FrictioEventType.PLAYBOOK_RESULT_UPDATED, handler)

    def on_playbook_generated(self, handler: Callable[[Dict[str, Any]], None]):
        """
        Register handler for playbook generated events

        Event data structure example:
        {
            "event_type": "playbook_generated",
            "playbook_id": "string",
            "playbook_name": "string",
            "template_id": "string",
            "timestamp": "2025-02-28T00:00:00Z"
        }
        """
        self.register_event_handler(FrictioEventType.PLAYBOOK_GENERATED, handler)


# ========== FLASK WEBHOOK SERVER EXAMPLE ==========

def create_flask_app(client: FrictioClient, webhook_path: str = '/webhook/frictio'):
    """
    Create a Flask app to handle Frictio webhooks

    Usage:
        from flask import Flask, request, jsonify

        client = FrictioClient(webhook_secret='your_secret')

        def handle_meeting_ended(data):
            print(f"Meeting ended: {data}")

        client.on_meeting_ended(handle_meeting_ended)

        app = create_flask_app(client)
        app.run(port=5000)

    Args:
        client: FrictioClient instance
        webhook_path: Webhook endpoint path

    Returns:
        Flask application
    """
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        raise ImportError("Flask is required for webhook server. Install with: pip install flask")

    app = Flask(__name__)

    @app.route(webhook_path, methods=['POST'])
    def handle_webhook():
        try:
            # Get signature from header
            signature = request.headers.get('X-Frictio-Signature') or request.headers.get('X-Webhook-Signature')

            # Handle webhook
            result = client.handle_webhook(request.data, signature)

            return jsonify(result), 200

        except FrictioWebhookError as e:
            return jsonify({'success': False, 'error': str(e)}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': 'Internal server error'}), 500

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'frictio-webhook'}), 200

    return app


# ========== EXAMPLE USAGE ==========

if __name__ == '__main__':
    import os

    # Initialize client with webhook secret
    WEBHOOK_SECRET = os.getenv('FRICTIO_WEBHOOK_SECRET', 'your_webhook_secret')
    client = FrictioClient(webhook_secret=WEBHOOK_SECRET)

    # Example handler for meeting ended
    def handle_meeting_ended(event_data: Dict[str, Any]):
        print(f"Meeting ended event received:")
        print(f"  Meeting ID: {event_data.get('meeting_id')}")
        print(f"  Duration: {event_data.get('duration_minutes')} minutes")
        print(f"  Participants: {event_data.get('participant_count')}")

        # Add your business logic here
        # For example: send notification, update CRM, etc.

    # Example handler for playbook result updated
    def handle_playbook_result_updated(event_data: Dict[str, Any]):
        print(f"Playbook result updated:")
        print(f"  Playbook: {event_data.get('playbook_name')}")
        print(f"  Result: {event_data.get('result')}")

    # Example handler for playbook generated
    def handle_playbook_generated(event_data: Dict[str, Any]):
        print(f"Playbook generated:")
        print(f"  Playbook: {event_data.get('playbook_name')}")
        print(f"  Template: {event_data.get('template_id')}")

    # Register handlers
    client.on_meeting_ended(handle_meeting_ended)
    client.on_playbook_result_updated(handle_playbook_result_updated)
    client.on_playbook_generated(handle_playbook_generated)

    # Start webhook server (requires Flask)
    try:
        app = create_flask_app(client)
        print("Starting Frictio webhook server on port 5000...")
        print(f"Webhook endpoint: http://localhost:5000/webhook/frictio")
        print("Press Ctrl+C to stop")

        # app.run(host='0.0.0.0', port=5000)
        # Uncomment the above line to actually start the server

    except ImportError:
        print("Flask not installed. Webhooks cannot be tested without Flask.")
        print("To test locally, create a mock webhook payload:")
        print("""
import json

payload = json.dumps({
    'event_type': 'meeting_ended',
    'meeting_id': '12345',
    'duration_minutes': 30,
    'participant_count': 5,
    'timestamp': '2025-02-28T10:00:00Z'
})

client.handle_webhook(payload.encode(), signature=None)
        """)