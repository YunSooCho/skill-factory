"""
Sender API Client Implementation

Provides methods for:
- Add Subscriber: Add new subscriber
- List Subscribers: List all subscribers
- Get Subscriber: Get subscriber details
- Update Subscriber: Update subscriber information
- Delete Subscriber: Remove subscriber
- Add Subscribers to Group: Add subscribers to a group
- Remove Subscribers from Group: Remove subscribers from group
- Triggers: Handle webhook events
"""

import requests
import time
import hmac
import hashlib
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class RateLimiter:
    max_requests: int = 400
    time_window: int = 60
    requests: list = None

    def __post_init__(self):
        if self.requests is None:
            self.requests = []

    def wait_if_needed(self):
        now = time.time()
        self.requests = [r for r in self.requests if now - r < self.time_window]

        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
                self.requests = []

        self.requests.append(now)


class SenderError(Exception):
    pass


class AuthenticationError(SenderError):
    pass


class RateLimitError(SenderError):
    pass


class InvalidRequestError(SenderError):
    pass


class APIError(SenderError):
    pass


class SenderClient:
    """Sender API Client - Email marketing service"""

    BASE_URL = "https://api.sender.net/v1"

    def __init__(self, api_key: str, timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limiter = RateLimiter(max_requests=400, time_window=60)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, params: dict = None, data: dict = None) -> Dict[str, Any]:
        self.rate_limiter.wait_if_needed()
        url = f"{self.BASE_URL}{endpoint}"
        last_error = None

        for attempt in range(self.max_retries):
            try:
                response = self.session.request(method=method, url=url, params=params, json=data, timeout=self.timeout)

                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key")
                elif response.status_code == 429:
                    raise RateLimitError("Rate limit exceeded")
                elif response.status_code == 400:
                    error_data = response.json() if response.content else {}
                    raise InvalidRequestError(f"Invalid request: {error_data.get('message', 'Unknown error')}")
                elif response.status_code >= 500:
                    raise APIError(f"Server error: {response.status_code}")

                response.raise_for_status()
                return response.json()

            except requests.Timeout:
                last_error = f"Request timeout after {self.timeout} seconds"
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise APIError(last_error)
            except requests.RequestException as e:
                last_error = str(e)
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise APIError(f"Request failed: {last_error}")

        raise APIError(f"Max retries exceeded: {last_error}")

    def add_subscriber(
        self,
        email: str,
        name: Optional[str] = None,
        fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add a new subscriber"""
        if not email:
            raise InvalidRequestError("email is required")

        data = {"email": email}
        if name:
            data["name"] = name
        if fields:
            data["fields"] = fields

        return self._make_request("POST", "/subscribers", data=data)

    def list_subscribers(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """List all subscribers"""
        if limit > 1000:
            raise InvalidRequestError("limit cannot exceed 1000")
        return self._make_request("GET", "/subscribers", params={"limit": limit, "offset": offset})

    def get_subscriber(self, email: str) -> Dict[str, Any]:
        """Get subscriber details by email"""
        if not email:
            raise InvalidRequestError("email is required")
        return self._make_request("GET", f"/subscribers/{email}")

    def update_subscriber(
        self,
        email: str,
        name: Optional[str] = None,
        fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update subscriber information"""
        if not email:
            raise InvalidRequestError("email is required")

        data = {}
        if name:
            data["name"] = name
        if fields:
            data["fields"] = fields

        return self._make_request("PUT", f"/subscribers/{email}", data=data)

    def delete_subscriber(self, email: str) -> Dict[str, Any]:
        """Delete a subscriber"""
        if not email:
            raise InvalidRequestError("email is required")
        return self._make_request("DELETE", f"/subscribers/{email}")

    def add_subscribers_to_group(
        self,
        group_id: str,
        emails: List[str]
    ) -> Dict[str, Any]:
        """Add subscribers to a group"""
        if not group_id or not emails:
            raise InvalidRequestError("group_id and emails are required")

        data = {
            "group_id": group_id,
            "emails": emails
        }
        return self._make_request("POST", "/groups/subscribers", data=data)

    def remove_subscribers_from_group(
        self,
        group_id: str,
        emails: List[str]
    ) -> Dict[str, Any]:
        """Remove subscribers from a group"""
        if not group_id or not emails:
            raise InvalidRequestError("group_id and emails are required")

        data = {
            "group_id": group_id,
            "emails": emails
        }
        return self._make_request("DELETE", "/groups/subscribers", data=data)

    def verify_webhook_signature(self, payload_bytes: bytes, signature: str, webhook_secret: str) -> bool:
        """Verify webhook signature"""
        if not webhook_secret:
            return False

        if not signature or '=' not in signature:
            return False

        version, hash_value = signature.split('=', 1)

        if version != 'sha256':
            return False

        expected_hash = hmac.new(
            webhook_secret.encode(),
            payload_bytes,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_hash, hash_value)

    def handle_webhook_event(self, payload: Dict[str, Any], signature: Optional[str] = None, webhook_secret: Optional[str] = None) -> Dict[str, Any]:
        """Handle webhook events"""
        if signature and webhook_secret:
            payload_bytes = json.dumps(payload).encode()
            if not self.verify_webhook_signature(payload_bytes, signature, webhook_secret):
                raise InvalidRequestError("Invalid webhook signature")

        event_type = payload.get("type")

        if event_type == "new_subscriber":
            return {
                "event_type": event_type,
                "subscriber": payload.get("subscriber", {}),
                "timestamp": payload.get("timestamp")
            }
        elif event_type == "updated_subscriber":
            return {
                "event_type": event_type,
                "subscriber": payload.get("subscriber", {}),
                "changes": payload.get("changes", {}),
                "timestamp": payload.get("timestamp")
            }
        elif event_type in ["new_unsubscriber", "new_unsubscriber_from_group"]:
            return {
                "event_type": event_type,
                "email": payload.get("email"),
                "group": payload.get("group"),
                "timestamp": payload.get("timestamp")
            }
        elif event_type == "new_subscriber_in_group":
            return {
                "event_type": event_type,
                "email": payload.get("email"),
                "subscriber": payload.get("subscriber", {}),
                "group": payload.get("group"),
                "timestamp": payload.get("timestamp")
            }
        else:
            return {"event_type": event_type, "data": payload}

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()