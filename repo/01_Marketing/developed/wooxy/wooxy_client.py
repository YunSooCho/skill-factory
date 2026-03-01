"""
Wooxy API Client
Email marketing and web push notifications

API Documentation: https://wooxy.com/docs/
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import time


@dataclass
class Contact:
    """Contact data model"""
    email: Optional[str] = None
    phone: Optional[str] = None
    web_push_token: Optional[str] = None
    web_push_subscription: Optional[Dict[str, Any]] = None
    custom_fields: Optional[Dict[str, Any]] = None


class RateLimiter:
    """Simple rate limiter for API requests"""

    def __init__(self, max_requests: int = 200, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.requests = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.time()
            self.requests = [req_time for req_time in self.requests
                            if now - req_time < self.per_seconds]

            if len(self.requests) >= self.max_requests:
                sleep_time = self.per_seconds - (now - self.requests[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    self.requests = []

            self.requests.append(now)


class WooxyClient:
    """
    Wooxy API client for email marketing and web push.

    API Documentation: https://wooxy.com/docs/
    Rate Limit: 200 requests per 60 seconds
    """

    BASE_URL = "https://api.wooxy.com/api/v1"

    def __init__(self, api_key: str):
        """
        Initialize Wooxy API client.

        Args:
            api_key: Your Wooxy API key
        """
        self.api_key = api_key
        self.session = None
        self.rate_limiter = RateLimiter(max_requests=200, per_seconds=60)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        return {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API request with error handling and rate limiting.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails or returns error
        """
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}{endpoint}"

        try:
            async with self.session.request(
                method,
                url,
                headers=self._get_headers(),
                params=params,
                json=json_data
            ) as response:
                try:
                    data = await response.json()
                except:
                    text = await response.text()
                    data = {"raw_response": text}

                if response.status >= 400:
                    error_msg = data.get("error", data.get("message", "Unknown error"))
                    raise Exception(f"Wooxy API error ({response.status}): {error_msg}")

                return data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during request to {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during Wooxy API request: {str(e)}")

    # ==================== Contact Management ====================

    async def new_contact(self, contact: Contact, list_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new contact.

        Args:
            contact: Contact object with email, phone, or web push token
            list_id: Optional list ID to add contact to

        Returns:
            Response with created contact data

        Raises:
            Exception: If request fails
        """
        data = {}
        if contact.email:
            data["email"] = contact.email
        if contact.phone:
            data["phone"] = contact.phone
        if contact.web_push_token:
            data["web_push_token"] = contact.web_push_token
        if contact.web_push_subscription:
            data["web_push_subscription"] = contact.web_push_subscription
        if contact.custom_fields:
            data["custom_fields"] = contact.custom_fields

        if list_id:
            data["list_id"] = list_id

        return await self._request("POST", "/contacts", json_data=data)

    async def update_contact(
        self,
        contact_id: str,
        contact: Contact
    ) -> Dict[str, Any]:
        """
        Update an existing contact.

        Args:
            contact_id: ID of the contact to update
            contact: Contact object with fields to update

        Returns:
            Response with updated contact data

        Raises:
            Exception: If request fails
        """
        data = {}
        if contact.email:
            data["email"] = contact.email
        if contact.phone:
            data["phone"] = contact.phone
        if contact.web_push_token:
            data["web_push_token"] = contact.web_push_token
        if contact.web_push_subscription:
            data["web_push_subscription"] = contact.web_push_subscription
        if contact.custom_fields:
            data["custom_fields"] = contact.custom_fields

        return await self._request(
            "PUT",
            f"/contacts/{contact_id}",
            json_data=data
        )

    async def remove_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Remove a contact.

        Args:
            contact_id: ID of the contact to remove

        Returns:
            Response confirming removal

        Raises:
            Exception: If request fails
        """
        return await self._request("DELETE", f"/contacts/{contact_id}")

    # ==================== Email Marketing ====================

    async def send_email(
        self,
        template_id: str,
        recipient: str,
        variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send an email to a recipient.

        Args:
            template_id: Email template ID
            recipient: Recipient email address or contact ID
            variables: Optional template variables

        Returns:
            Response with send result

        Raises:
            Exception: If request fails
        """
        data = {
            "template_id": template_id,
            "recipient": recipient
        }

        if variables:
            data["variables"] = variables

        return await self._request("POST", "/emails/send", json_data=data)

    async def send_trigger_email(
        self,
        trigger_id: str,
        recipient: str,
        variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a triggered email.

        Args:
            trigger_id: Trigger workflow ID
            recipient: Recipient email address
            variables: Optional template variables

        Returns:
            Response with send result

        Raises:
            Exception: If request fails
        """
        data = {
            "trigger_id": trigger_id,
            "recipient": recipient
        }

        if variables:
            data["variables"] = variables

        return await self._request(
            "POST",
            "/emails/trigger/send",
            json_data=data
        )

    # ==================== Web Push ====================

    async def send_web_push(
        self,
        subscription: Dict[str, Any],
        title: str,
        body: str,
        icon: Optional[str] = None,
        click_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a web push notification.

        Args:
            subscription: Web push subscription object
            title: Notification title
            body: Notification body
            icon: Optional icon URL
            click_url: Optional click-through URL

        Returns:
            Response with send result

        Raises:
            Exception: If request fails
        """
        data = {
            "subscription": subscription,
            "notification": {
                "title": title,
                "body": body
            }
        }

        if icon:
            data["notification"]["icon"] = icon
        if click_url:
            data["notification"]["click_url"] = click_url

        return await self._request("POST", "/web-push/send", json_data=data)

    async def send_triggered_web_push(
        self,
        trigger_id: str,
        subscription: Dict[str, Any],
        variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a triggered web push.

        Args:
            trigger_id: Trigger workflow ID
            subscription: Web push subscription object
            variables: Optional notification variables

        Returns:
            Response with send result

        Raises:
            Exception: If request fails
        """
        data = {
            "trigger_id": trigger_id,
            "subscription": subscription
        }

        if variables:
            data["variables"] = variables

        return await self._request(
            "POST",
            "/web-push/trigger/send",
            json_data=data
        )

    # ==================== Events ====================

    async def create_event(
        self,
        event_name: str,
        contact_id: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a custom event.

        Args:
            event_name: Name of the event
            contact_id: Optional contact ID associated with event
            properties: Optional event properties

        Returns:
            Response with created event data

        Raises:
            Exception: If request fails
        """
        data = {
            "event_name": event_name
        }

        if contact_id:
            data["contact_id"] = contact_id
        if properties:
            data["properties"] = properties

        return await self._request("POST", "/events", json_data=data)

    async def fire_event(
        self,
        event_name: str,
        contact_id: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Fire a trigger event.

        Args:
            event_name: Name of the event to fire
            contact_id: Contact ID to associate event with
            properties: Optional event properties

        Returns:
            Response with event firing result

        Raises:
            Exception: If request fails
        """
        data = {
            "event_name": event_name,
            "contact_id": contact_id
        }

        if properties:
            data["properties"] = properties

        return await self._request("POST", "/events/fire", json_data=data)

    # ==================== Webhook Handling ====================

    def handle_webhook(self, event_data: Dict[str, Any], signature: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle webhook events from Wooxy.

        Supported events:
        - subscribed_email
        - subscribed_web_push_contact_mobile
        - read_email
        - delivered_email
        - clicked_email
        - unsubscribed_web_push_contact_desktop
        - clicked_web_push
        - unsubscribed_email
        - complained_email
        - undelivered_web_push
        - subscribed_web_push_contact_desktop
        - hard_bounce_email
        - delivered_web_push
        - unsubscribed_web_push_contact_mobile

        Args:
            event_data: Webhook event data
            signature: Optional webhook signature for verification

        Returns:
            Processed event data

        Raises:
            Exception: If event data is invalid
        """
        if not event_data or "event_type" not in event_data:
            raise ValueError("Invalid webhook event data: missing 'event_type' field")

        event_type = event_data["event_type"]
        event_data["processed_at"] = datetime.utcnow().isoformat()

        # Process based on event type
        if "subscribed" in event_type:
            event_data["category"] = "subscription"
        elif "read" in event_type:
            event_data["category"] = "engagement"
        elif "delivered" in event_type:
            event_data["category"] = "delivery"
        elif "clicked" in event_type:
            event_data["category"] = "engagement"
        elif "unsubscribed" in event_type:
            event_data["category"] = "unsubscription"
        elif "bounced" in event_type:
            event_data["category"] = "bounce"
        elif "complained" in event_type:
            event_data["category"] = "complaint"

        return event_data