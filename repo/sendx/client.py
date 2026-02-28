"""
SendX API Client Implementation - Email marketing service
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
    max_requests: int = 450
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


class SendXError(Exception):
    pass


class AuthenticationError(SendXError):
    pass


class RateLimitError(SendXError):
    pass


class InvalidRequestError(SendXError):
    pass


class APIError(SendXError):
    pass


class SendXClient:
    """SendX API Client"""

    BASE_URL = "https://app.sendx.io/api/v1"

    def __init__(self, api_key: str, webhook_secret: Optional[str] = None, timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.webhook_secret = webhook_secret
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limiter = RateLimiter(max_requests=450, time_window=60)
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

    def create_contact(self, email: str, first_name: Optional[str] = None, last_name: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a contact"""
        if not email:
            raise InvalidRequestError("email is required")

        data = {"email": email}
        if first_name:
            data["firstName"] = first_name
        if last_name:
            data["lastName"] = last_name
        if attributes:
            data["attributes"] = attributes

        return self._make_request("POST", "/contacts", data=data)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get contact by ID"""
        if not contact_id:
            raise InvalidRequestError("contact_id is required")
        return self._make_request("GET", f"/contacts/{contact_id}")

    def search_contact(self, email: str) -> Dict[str, Any]:
        """Search contact by email"""
        if not email:
            raise InvalidRequestError("email is required")
        return self._make_request("GET", "/contacts", params={"email": email})

    def update_contact(self, contact_id: str, email: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update contact"""
        if not contact_id:
            raise InvalidRequestError("contact_id is required")

        data = {}
        if email:
            data["email"] = email
        if first_name:
            data["firstName"] = first_name
        if last_name:
            data["lastName"] = last_name
        if attributes:
            data["attributes"] = attributes

        return self._make_request("PUT", f"/contacts/{contact_id}", data=data)

    def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """Delete contact"""
        if not contact_id:
            raise InvalidRequestError("contact_id is required")
        return self._make_request("DELETE", f"/contacts/{contact_id}")

    def create_list(self, name: str) -> Dict[str, Any]:
        """Create a list"""
        if not name:
            raise InvalidRequestError("name is required")
        return self._make_request("POST", "/lists", data={"name": name})

    def get_list(self, list_id: str) -> Dict[str, Any]:
        """Get list by ID"""
        if not list_id:
            raise InvalidRequestError("list_id is required")
        return self._make_request("GET", f"/lists/{list_id}")

    def search_list(self, name: str) -> Dict[str, Any]:
        """Search list by name"""
        if not name:
            raise InvalidRequestError("name is required")
        return self._make_request("GET", "/lists", params={"name": name})

    def update_list(self, list_id: str, name: str) -> Dict[str, Any]:
        """Update list"""
        if not list_id or not name:
            raise InvalidRequestError("list_id and name are required")
        return self._make_request("PUT", f"/lists/{list_id}", data={"name": name})

    def delete_list(self, list_id: str) -> Dict[str, Any]:
        """Delete list"""
        if not list_id:
            raise InvalidRequestError("list_id is required")
        return self._make_request("DELETE", f"/lists/{list_id}")

    def create_tag(self, name: str) -> Dict[str, Any]:
        """Create a tag"""
        if not name:
            raise InvalidRequestError("name is required")
        return self._make_request("POST", "/tags", data={"name": name})

    def get_tag(self, tag_id: str) -> Dict[str, Any]:
        """Get tag by ID"""
        if not tag_id:
            raise InvalidRequestError("tag_id is required")
        return self._make_request("GET", f"/tags/{tag_id}")

    def search_tag(self, name: str) -> Dict[str, Any]:
        """Search tag by name"""
        if not name:
            raise InvalidRequestError("name is required")
        return self._make_request("GET", "/tags", params={"name": name})

    def update_tag(self, tag_id: str, name: str) -> Dict[str, Any]:
        """Update tag"""
        if not tag_id or not name:
            raise InvalidRequestError("tag_id and name are required")
        return self._make_request("PUT", f"/tags/{tag_id}", data={"name": name})

    def delete_tag(self, tag_id: str) -> Dict[str, Any]:
        """Delete tag"""
        if not tag_id:
            raise InvalidRequestError("tag_id is required")
        return self._make_request("DELETE", f"/tags/{tag_id}")

    def verify_webhook_signature(self, payload_bytes: bytes, signature: str) -> bool:
        """Verify webhook signature"""
        if not self.webhook_secret:
            return False

        if not signature or '=' not in signature:
            return False

        version, hash_value = signature.split('=', 1)

        if version != 'sha256':
            return False

        expected_hash = hmac.new(
            self.webhook_secret.encode(),
            payload_bytes,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_hash, hash_value)

    def handle_webhook_event(self, payload: Dict[str, Any], signature: Optional[str] = None) -> Dict[str, Any]:
        """Handle webhook events"""
        if signature and self.webhook_secret:
            payload_bytes = json.dumps(payload).encode()
            if not self.verify_webhook_signature(payload_bytes, signature):
                raise InvalidRequestError("Invalid webhook signature")

        event_type = payload.get("type", payload.get("event_type"))

        return {
            "event_type": event_type,
            "contact": payload.get("contact", {}),
            "email": payload.get("email"),
            "campaign": payload.get("campaign", {}),
            "timestamp": payload.get("timestamp", payload.get("createdAt"))
        }

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()