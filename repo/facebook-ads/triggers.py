"""
Facebook Ads Webhook Triggers implementation.
"""
import hmac
import hashlib
from typing import Callable, Optional, Dict, Any
from .models import Lead
from .exceptions import FacebookAdsError, FacebookAdsAuthenticationError


class FacebookAdsTriggers:
    """Facebook Ads webhook triggers for Yoom integration."""

    WEBHOOK_EVENT_LEAD = "leadgen"

    def __init__(self, app_secret: Optional[str] = None):
        """
        Initialize Facebook Ads triggers handler.

        Args:
            app_secret: Facebook App Secret for webhook signature verification
        """
        self.app_secret = app_secret
        self.handlers = {
            self.WEBHOOK_EVENT_LEAD: [],
        }

    def register_handler(self, event_type: str, handler: Callable[[Lead], None]):
        """
        Register a callback function for a specific webhook event.

        Args:
            event_type: Event type ('leadgen')
            handler: Callback function that receives Lead object
        """
        if event_type not in self.handlers:
            raise ValueError(f"Unknown event type: {event_type}")
        self.handlers[event_type].append(handler)

    def unregister_handler(self, event_type: str, handler: Callable[[Lead], None]):
        """
        Unregister a callback function for a specific webhook event.

        Args:
            event_type: Event type
            handler: Callback function to remove
        """
        if event_type in self.handlers and handler in self.handlers[event_type]:
            self.handlers[event_type].remove(handler)

    def verify_webhook_signature(
        self, payload: bytes, signature: str
    ) -> bool:
        """
        Verify Facebook webhook signature (X-Hub-Signature-256).

        Args:
            payload: Raw webhook payload bytes
            signature: Signature from X-Hub-Signature-256 header (format: sha256=...)

        Returns:
            True if signature is valid

        Raises:
            FacebookAdsAuthenticationError: If signature verification fails
        """
        if not self.app_secret:
            raise FacebookAdsAuthenticationError(
                "app_secret not configured for signature verification"
            )

        # Extract hash from signature (format: sha256=...)
        parts = signature.split("=", 1)
        if len(parts) != 2 or parts[0] != "sha256":
            raise FacebookAdsAuthenticationError("Invalid signature format")

        expected_hash = parts[1]

        # Calculate HMAC-SHA256
        actual_hash = hmac.new(
            self.app_secret.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()

        # Compare securely
        return hmac.compare_digest(expected_hash, actual_hash)

    def handle_webhook_challenge(self, mode: str, token: str, challenge: str) -> Optional[str]:
        """
        Handle Facebook webhook verification challenge.

        Args:
            mode: Subscription mode
            token: Verification token
            challenge: Challenge string to echo back

        Returns:
            Challenge string if verification succeeds, None otherwise
        """
        # You can validate the token against your verification token
        # For now, we'll accept any mode='subscribe' request
        if mode == "subscribe":
            return challenge
        return None

    def handle_webhook(self, event_data: Dict[str, Any]) -> Optional[Lead]:
        """
        Process incoming webhook event and call registered handlers.

        Args:
            event_data: Webhook event payload from Facebook

        Returns:
            Lead object if valid event, None otherwise

        Raises:
            FacebookAdsError: For invalid event data
        """
        # Facebook webhook structure:
        # {
        #   "object": "page",
        #   "entry": [{
        #     "changes": [{
        #       "value": {
        #         "leadgen_id": "...",
        #         "ad_id": "...",
        #         ...
        #       }
        #     }]
        #   }]
        # }

        try:
            entries = event_data.get("entry", [])
            if not entries:
                return None

            for entry in entries:
                changes = entry.get("changes", [])
                for change in changes:
                    field = change.get("field")
                    value = change.get("value", {})

                    # Check if it's a lead event
                    if field == "leadgen":
                        lead = Lead.from_dict(value)

                        # Call registered handlers
                        for handler in self.handlers[self.WEBHOOK_EVENT_LEAD]:
                            try:
                                handler(lead)
                            except Exception as e:
                                # Continue processing even if one handler fails
                                print(f"Handler error for lead event: {str(e)}")

                        return lead

        except Exception as e:
            raise FacebookAdsError(f"Failed to process webhook event: {str(e)}")

        return None

    def subscribe_to_webhook(
        self,
        object_type: str,
        callback_url: str,
        fields: Optional[str] = None,
        verify_token: Optional[str] = None,
        access_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Subscribe to Facebook webhook events.

        Args:
            object_type: Object type (e.g., 'page', 'user')
            callback_url: URL to receive webhook events
            fields: Comma-separated list of fields to subscribe to
            verify_token: Verification token for challenge
            access_token: App access token

        Returns:
            Subscription response

        Raises:
            FacebookAdsError: If subscription fails
        """
        import requests

        url = f"https://graph.facebook.com/{self.API_VERSION}/{object_id}/subscriptions"
        data = {
            "object": object_type,
            "callback_url": callback_url,
            "fields": fields or "leadgen",
            "verify_token": verify_token,
        }

        if access_token:
            data["access_token"] = access_token

        try:
            response = requests.post(url, data=data, timeout=30)
            if response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise FacebookAdsError(
                    f"Webhook subscription failed: {error_data.get('error', {}).get('message', response.text)}"
                )

            return response.json()

        except requests.RequestException as e:
            raise FacebookAdsError(f"Failed to subscribe to webhook: {str(e)}")

    def list_webhooks(
        self, object_id: str, access_token: str
    ) -> List[Dict[str, Any]]:
        """
        List all webhook subscriptions for an object.

        Args:
            object_id: Facebook object ID
            access_token: App access token

        Returns:
            List of webhook subscriptions

        Raises:
            FacebookAdsError: If listing fails
        """
        import requests

        url = f"https://graph.facebook.com/{self.API_VERSION}/{object_id}/subscriptions"
        params = {"access_token": access_token}

        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code >= 400:
                error_data = response.json() if response.text else {}
                raise FacebookAdsError(
                    f"Webhook listing failed: {error_data.get('error', {}).get('message', response.text)}"
                )

            data = response.json()
            return data.get("data", [])

        except requests.RequestException as e:
            raise FacebookAdsError(f"Failed to list webhooks: {str(e)}")