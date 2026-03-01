"""
Sendy API Client Implementation - Self-hosted email newsletter service
"""

import requests
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class RateLimiter:
    max_requests: int = 100
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


class SendyError(Exception):
    pass


class APIError(SendyError):
    pass


class InvalidRequestError(SendyError):
    pass


class SendyClient:
    """Sendy API Client"""

    def __init__(self, api_url: str, api_key: str, timeout: int = 30, max_retries: int = 3):
        """
        Initialize Sendy client

        Args:
            api_url: Your Sendy installation URL (e.g., https://sendy.yourdomain.com)
            api_key: Your Sendy API key
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limiter = RateLimiter(max_requests=100, time_window=60)
        self.session = requests.Session()

    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        self.rate_limiter.wait_if_needed()
        url = f"{self.api_url}/{endpoint}"
        last_error = None

        data['api_key'] = self.api_key

        for attempt in range(self.max_retries):
            try:
                response = self.session.post(url, data=data, timeout=self.timeout)

                if response.status_code >= 500:
                    raise APIError(f"Server error: {response.status_code}")

                response.raise_for_status()

                text = response.text.strip()

                if text == "Invalid API key":
                    raise APIError("Invalid API key")
                elif text == "Error":
                    raise APIError("Unknown error occurred")
                elif text.startswith("Error:"):
                    raise APIError(text)

                return {"status": "success", "message": text}

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
        list_id: str,
        name: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        referrer: Optional[str] = None,
        silent: bool = False
    ) -> Dict[str, Any]:
        """Add a subscriber to a list"""
        if not email or not list_id:
            raise InvalidRequestError("email and list_id are required")

        data = {
            "email": email,
            "list": list_id
        }

        if name:
            data['name'] = name
        if custom_fields:
            data.update({f"field[{k}]": v for k, v in custom_fields.items()})
        if referrer:
            data['referrer'] = referrer
        if silent:
            data['silent'] = '1'

        return self._make_request("subscribe", data)

    def delete_subscriber(self, email: str, list_id: str) -> Dict[str, Any]:
        """Delete a subscriber from a list"""
        if not email or not list_id:
            raise InvalidRequestError("email and list_id are required")

        data = {
            "email": email,
            "list": list_id
        }

        return self._make_request("unsubscribe", data)

    def unsubscribe_user(self, email: str, list_id: str) -> Dict[str, Any]:
        """Unsubscribe a user from a list (alias for delete_subscriber)"""
        return self.delete_subscriber(email, list_id)

    def get_lists(self) -> Dict[str, Any]:
        """Get all lists"""
        return self._make_request("getLists", {})

    def get_brands(self) -> Dict[str, Any]:
        """Get all brands"""
        return self._make_request("getBrands", {})

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()