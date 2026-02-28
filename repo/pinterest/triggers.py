"""
Pinterest Webhook Triggers implementation.
"""
import hashlib
import hmac
from typing import Callable, Optional, Dict, Any
from .models import PinterestPin
from .exceptions import PinterestAPIError, PinterestAuthenticationError


class PinterestTriggers:
    """Pinterest webhook triggers for Yoom integration."""

    WEBHOOK_EVENT_NEW_PIN = "EVENT_PIN_CREATE"
    WEBHOOK_EVENT_UPDATE_PIN = "EVENT_PIN_UPDATE"
    WEBHOOK_EVENT_DELETE_PIN = "EVENT_PIN_DELETE"

    def __init__(self, webhook_secret: Optional[str] = None):
        """
        Initialize Pinterest triggers handler.

        Args:
            webhook_secret: Optional secret for webhook signature verification
        """
        self.webhook_secret = webhook_secret
        self.handlers = {
            self.WEBHOOK_EVENT_NEW_PIN: [],
            self.WEBHOOK_EVENT_UPDATE_PIN: [],
            self.WEBHOOK_EVENT_DELETE_PIN: [],
        }

    def register_handler(self, event_type: str, handler: Callable[[PinterestPin], None]):
        """
        Register a callback function for a specific webhook event.

        Args:
            event_type: Event type (e.g., EVENT_PIN_CREATE)
            handler: Callback function that receives PinterestPin object
        """
        if event_type not in self.handlers:
            raise ValueError(f"Unknown event type: {event_type}")
        self.handlers[event_type].append(handler)

    def unregister_handler(
        self, event_type: str, handler: Callable[[PinterestPin], None]
    ):
        """
        Unregister a callback function for a specific webhook event.

        Args:
            event_type: Event type
            handler: Callback function to remove
        """
        if event_type in self.handlers and handler in self.handlers[event_type]:
            self.handlers[event_type].remove(handler)

    def verify_webhook_signature(
        self, payload: bytes, signature: str, timestamp: str
    ) -> bool:
        """
        Verify Pinterest webhook signature.

        Args:
            payload: Raw webhook payload bytes
            signature: Base64 signature from header
            timestamp: Timestamp from header

        Returns:
            True if signature is valid

        Raises:
            PinterestAuthenticationError: If signature verification fails
        """
        if not self.webhook_secret:
            raise PinterestAuthenticationError(
                "webhook_secret not configured for signature verification"
            )

        # Pinterest uses HMAC-SHA256
        # Format: timestamp + "." + payload
        signed_payload = timestamp.encode("utf-8") + b"." + payload
        expected_signature = hmac.new(
            self.webhook_secret.encode("utf-8"),
            signed_payload,
            hashlib.sha256,
        ).digest()

        # Compare signatures safely
        received = hmac.compare_digest(expected_signature, signature.encode("utf-8"))
        return received

    def handle_webhook(self, event_data: Dict[str, Any]) -> Optional[PinterestPin]:
        """
        Process incoming webhook event and call registered handlers.

        Args:
            event_data: Webhook event payload

        Returns:
            PinterestPin object if valid event, None otherwise

        Raises:
            PinterestAPIError: For invalid event data
        """
        # Extract event type and data
        event_type = event_data.get("event_type") or event_data.get("code")
        event_data_resource = event_data.get("data", {}).get("resource_data", {})

        if not event_type:
            raise PinterestAPIError("Missing event_type in webhook payload")

        # Map Pinterest event codes to our internal types
        event_mapping = {
            "EVENT_PIN_CREATE": self.WEBHOOK_EVENT_NEW_PIN,
            "EVENT_PIN_UPDATE": self.WEBHOOK_EVENT_UPDATE_PIN,
            "EVENT_PIN_DELETE": self.WEBHOOK_EVENT_DELETE_PIN,
        }

        mapped_event = event_mapping.get(event_type)
        if not mapped_event:
            # Unknown event type, skip processing
            return None

        # Parse pin data
        try:
            pin = PinterestPin.from_dict(event_data_resource)
        except Exception as e:
            raise PinterestAPIError(f"Failed to parse pin data: {str(e)}")

        # Call registered handlers
        for handler in self.handlers[mapped_event]:
            try:
                handler(pin)
            except Exception as e:
                # Continue processing even if one handler fails
                print(f"Handler error for event {mapped_event}: {str(e)}")

        return pin

    def create_webhook(self, access_token: str, webhook_url: str) -> str:
        """
        Create a webhook subscription on Pinterest.

        Args:
            access_token: OAuth access token
            webhook_url: URL to receive webhook events

        Returns:
            Webhook ID

        Raises:
            PinterestAPIError: If webhook creation fails
        """
        import requests

        url = "https://api.pinterest.com/v5/webhooks"
        headers = {"Authorization": f"Bearer {access_token}"}
        data = {
            "callback_url": webhook_url,
            "interests": {
                "interest_type": "USER",
                "interest_id": "self",
            },
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise PinterestAPIError(
                    f"Webhook creation failed: {error_data.get('message', response.text)}"
                )

            webhook_data = response.json()
            return webhook_data.get("data", {}).get("id")

        except requests.RequestException as e:
            raise PinterestAPIError(f"Failed to create webhook: {str(e)}")

    def delete_webhook(self, access_token: str, webhook_id: str) -> bool:
        """
        Delete a webhook subscription from Pinterest.

        Args:
            access_token: OAuth access token
            webhook_id: Webhook ID to delete

        Returns:
            True if successful

        Raises:
            PinterestAPIError: If webhook deletion fails
        """
        import requests

        url = f"https://api.pinterest.com/v5/webhooks/{webhook_id}"
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = requests.delete(url, headers=headers, timeout=30)
            if response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise PinterestAPIError(
                    f"Webhook deletion failed: {error_data.get('message', response.text)}"
                )
            return True

        except requests.RequestException as e:
            raise PinterestAPIError(f"Failed to delete webhook: {str(e)}")

    def list_webhooks(self, access_token: str) -> list:
        """
        List all webhook subscriptions for the authenticated user.

        Args:
            access_token: OAuth access token

        Returns:
            List of webhook objects

        Raises:
            PinterestAPIError: If listing fails
        """
        import requests

        url = "https://api.pinterest.com/v5/webhooks"
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise PinterestAPIError(
                    f"Webhook listing failed: {error_data.get('message', response.text)}"
                )

            data = response.json()
            return data.get("items", [])

        except requests.RequestException as e:
            raise PinterestAPIError(f"Failed to list webhooks: {str(e)}")