"""
Webhook triggers implementation.
"""
import hmac
import hashlib
from typing import Callable, Optional, Dict, Any


class KlaviyoTriggers:
    """Webhook triggers for integration."""

    def __init__(self, webhook_secret: Optional[str] = None):
        """Initialize triggers handler."""
        self.webhook_secret = webhook_secret
        self.handlers = {}

    def register_handler(self, event_type: str, handler: Callable):
        """Register webhook handler."""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Verify webhook signature."""
        if not self.webhook_secret:
            return False
        
        expected = hmac.new(self.webhook_secret.encode(), payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def handle_webhook(self, event_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process webhook event."""
        event_type = event_data.get("event_type") or event_data.get("type")
        if not event_type:
            return None
        
        for handler in self.handlers.get(event_type, []):
            try:
                handler(event_data)
            except Exception as e:
                print(f"Handler error: {str(e)}")
        
        return event_data
