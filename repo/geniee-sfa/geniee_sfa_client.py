"""
Geniee SFA API Client
Sales Force Automation platform focused on triggers/webhooks

Note: Geniee SFA provides webhook triggers but no direct API actions in the Yoom integration.
This module provides webhook verification and trigger handling capabilities.

Yoom Integration:
- 0 API Actions
- 6 Triggers:
  1. Prospect created
  2. Deal information created
  3. Prospect created and updated
  4. Deal information created and updated
  5. Company information created
  6. Company information created and updated
"""

import hmac
import hashlib
import json
from typing import Dict, Any, Optional, Callable
from enum import Enum


class GenieeSFATriggerType(Enum):
    """Geniee SFA webhook trigger types"""
    PROSPECT_CREATED = "prospect_created"
    DEAL_CREATED = "deal_created"
    PROSPECT_CREATED_UPDATED = "prospect_created_updated"
    DEAL_CREATED_UPDATED = "deal_created_updated"
    COMPANY_CREATED = "company_created"
    COMPANY_CREATED_UPDATED = "company_created_updated"


class GenieeSFAWebhookError(Exception):
    """Custom exception for Geniee SFA webhook errors"""
    pass


class GenieeSFAClient:
    """
    Geniee SFA Webhook Handler
    Handles webhook verification, parsing, and trigger routing for SFA events
    """

    def __init__(self, webhook_secret: Optional[str] = None):
        """
        Initialize Geniee SFA webhook client

        Args:
            webhook_secret: Secret key for webhook signature verification (optional)
        """
        self.webhook_secret = webhook_secret
        self.event_handlers = {}
        self.middleware_handlers = []

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
            GenieeSFAWebhookError: If verification fails
        """
        if not self.webhook_secret:
            raise GenieeSFAWebhookError("Webhook secret not configured")

        # Calculate expected signature
        expected_sig = hmac.new(
            self.webhook_secret.encode(),
            payload,
            getattr(hashlib, algorithm)
        ).hexdigest()

        # Handle different signature formats
        if '=' in signature:
            signature = signature.split('=', 1)[1]

        # Compare signatures securely
        if not hmac.compare_digest(expected_sig, signature):
            raise GenieeSFAWebhookError("Invalid webhook signature")

        return True

    def register_event_handler(self, trigger_type: GenieeSFATriggerType,
                               handler: Callable[[Dict[str, Any]], None]):
        """
        Register a handler for a specific trigger type

        Args:
            trigger_type: Trigger type to handle
            handler: Callback function that receives event data
        """
        self.event_handlers[trigger_type.value] = handler

    def unregister_event_handler(self, trigger_type: GenieeSFATriggerType):
        """Unregister an event handler"""
        if trigger_type.value in self.event_handlers:
            del self.event_handlers[trigger_type.value]

    def add_middleware(self, middleware: Callable[[Dict[str, Any]], Dict[str, Any]]):
        """
        Add middleware function to process event data before handlers

        Args:
            middleware: Function that takes event data and returns modified data
        """
        self.middleware_handlers.append(middleware)

    def parse_webhook_event(self, payload: bytes, signature: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse and validate incoming webhook event

        Args:
            payload: Request body bytes
            signature: Webhook signature (optional if not configured)

        Returns:
            Parsed event data

        Raises:
            GenieeSFAWebhookError: If parsing or validation fails
        """
        # Verify signature if secret is configured
        if self.webhook_secret:
            if not signature:
                raise GenieeSFAWebhookError("Missing webhook signature")

            signature = signature.split('=', 1)[1] if '=' in signature else signature

            if not self.verify_webhook_signature(payload, signature):
                raise GenieeSFAWebhookError("Invalid webhook signature")

        # Parse JSON payload
        try:
            event_data = json.loads(payload.decode('utf-8'))
        except json.JSONDecodeError as e:
            raise GenieeSFAWebhookError(f"Invalid JSON payload: {str(e)}")

        # Validate event structure
        if 'trigger_type' not in event_data and 'event_type' not in event_data:
            raise GenieeSFAWebhookError("Missing trigger_type or event_type in webhook payload")

        # Normalize event key name
        if 'event_type' in event_data and 'trigger_type' not in event_data:
            event_data['trigger_type'] = event_data['event_type']

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
            GenieeSFAWebhookError: If processing fails
        """
        # Parse and validate event
        event_data = self.parse_webhook_event(payload, signature)
        trigger_type = event_data.get('trigger_type')

        # Apply middleware
        processed_data = event_data
        for middleware in self.middleware_handlers:
            try:
                processed_data = middleware(processed_data)
            except Exception as e:
                raise GenieeSFAWebhookError(f"Middleware error: {str(e)}")

        # Route to handler
        if trigger_type in self.event_handlers:
            try:
                handler = self.event_handlers[trigger_type]
                handler(processed_data)
                return {
                    'success': True,
                    'message': f'Trigger {trigger_type} handled successfully',
                    'trigger_type': trigger_type
                }
            except Exception as e:
                raise GenieeSFAWebhookError(f"Handler error: {str(e)}")
        else:
            return {
                'success': True,
                'message': f'No handler registered for trigger {trigger_type}',
                'trigger_type': trigger_type,
                'handled': False
            }

    # ========== SPECIFIC TRIGGER HANDLERS ==========

    def on_prospect_created(self, handler: Callable[[Dict[str, Any]], None]):
        """
        Register handler for prospect created events

        Event data example:
        {
            "trigger_type": "prospect_created",
            "prospect_id": "12345",
            "prospect_name": "John Doe",
            "email": "john@example.com",
            "status": "New",
            "timestamp": "2025-02-28T10:00:00Z"
        }
        """
        self.register_event_handler(GenieeSFATriggerType.PROSPECT_CREATED, handler)

    def on_deal_created(self, handler: Callable[[Dict[str, Any]], None]):
        """
        Register handler for deal created events

        Event data example:
        {
            "trigger_type": "deal_created",
            "deal_id": "54321",
            "deal_name": "Big Deal",
            "amount": 1000000,
            "status": "Negotiation",
            "timestamp": "2025-02-28T10:00:00Z"
        }
        """
        self.register_event_handler(GenieeSFATriggerType.DEAL_CREATED, handler)

    def on_prospect_created_updated(self, handler: Callable[[Dict[str, Any]], None]):
        """
        Register handler for prospect created and updated events

        Event data includes both create and update notifications
        """
        self.register_event_handler(GenieeSFATriggerType.PROSPECT_CREATED_UPDATED, handler)

    def on_deal_created_updated(self, handler: Callable[[Dict[str, Any]], None]):
        """
        Register handler for deal created and updated events

        Event data includes both create and update notifications
        """
        self.register_event_handler(GenieeSFATriggerType.DEAL_CREATED_UPDATED, handler)

    def on_company_created(self, handler: Callable[[Dict[str, Any]], None]):
        """
        Register handler for company created events

        Event data example:
        {
            "trigger_type": "company_created",
            "company_id": "98765",
            "company_name": "Example Corp",
            "industry": "Technology",
            "website": "https://example.com",
            "timestamp": "2025-02-28T10:00:00Z"
        }
        """
        self.register_event_handler(GenieeSFATriggerType.COMPANY_CREATED, handler)

    def on_company_created_updated(self, handler: Callable[[Dict[str, Any]], None]):
        """
        Register handler for company created and updated events

        Event data includes both create and update notifications
        """
        self.register_event_handler(GenieeSFATriggerType.COMPANY_CREATED_UPDATED, handler)


# ========== FLASK WEBHOOK SERVER EXAMPLE ==========

def create_flask_app(client: GenieeSFAClient, webhook_path: str = '/webhook/geniee-sfa'):
    """
    Create a Flask app to handle Geniee SFA webhooks

    Usage:
        from flask import Flask

        client = GenieeSFAClient(webhook_secret='your_secret')

        def handle_prospect_created(data):
            print(f"New prospect: {data}")

        client.on_prospect_created(handle_prospect_created)

        app = create_flask_app(client)
        app.run(port=5000)

    Args:
        client: GenieeSFAClient instance
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
            signature = (request.headers.get('X-Geniee-Signature') or
                        request.headers.get('X-Webhook-Signature'))

            # Handle webhook
            result = client.handle_webhook(request.data, signature)

            return jsonify(result), 200

        except GenieeSFAWebhookError as e:
            return jsonify({'success': False, 'error': str(e)}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': 'Internal server error'}), 500

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'geniee-sfa-webhook'}), 200

    return app


# ========== EXAMPLE USAGE ==========

if __name__ == '__main__':
    import os

    # Initialize client with webhook secret
    WEBHOOK_SECRET = os.getenv('GENIEE_SFA_WEBHOOK_SECRET', 'your_webhook_secret')
    client = GenieeSFAClient(webhook_secret=WEBHOOK_SECRET)

    # Example handlers
    def handle_prospect_created(event_data: Dict[str, Any]):
        print(f"New prospect created:")
        print(f"  Name: {event_data.get('prospect_name')}")
        print(f"  Email: {event_data.get('email')}")
        print(f"  ID: {event_data.get('prospect_id')}")

    def handle_deal_created(event_data: Dict[str, Any]):
        print(f"New deal created:")
        print(f"  Deal: {event_data.get('deal_name')}")
        print(f"  Amount: {event_data.get('amount')}")
        print(f"  Status: {event_data.get('status')}")

    def handle_company_created(event_data: Dict[str, Any]):
        print(f"New company created:")
        print(f"  Name: {event_data.get('company_name')}")
        print(f"  Website: {event_data.get('website')}")

    # Register handlers
    client.on_prospect_created(handle_prospect_created)
    client.on_deal_created(handle_deal_created)
    client.on_company_created(handle_company_created)
    client.on_prospect_created_updated(handle_prospect_created)
    client.on_deal_created_updated(handle_deal_created)
    client.on_company_created_updated(handle_company_created)

    # Add middleware for logging
    def logging_middleware(event_data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[Webhook] Received: {event_data.get('trigger_type')}")
        return event_data

    client.add_middleware(logging_middleware)

    # Start webhook server (requires Flask)
    try:
        app = create_flask_app(client)
        print("Starting Geniee SFA webhook server on port 5000...")
        print(f"Webhook endpoint: http://localhost:5000/webhook/geniee-sfa")
        print("Press Ctrl+C to stop")

        # app.run(host='0.0.0.0', port=5000)
        # Uncomment the above line to actually start the server

    except ImportError:
        print("Flask not installed. Cannot start webhook server.")
        print("Install Flask: pip install flask")