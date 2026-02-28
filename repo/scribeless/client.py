"""
Scribeless API Client Implementation

Provides methods for:
- Create Recipient: Add a recipient for handwritten letter service
"""

import requests
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class RateLimiter:
    """Rate limiter for API requests"""
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


class ScribelessError(Exception):
    """Base exception for Scribeless API errors"""
    pass


class AuthenticationError(ScribelessError):
    pass


class RateLimitError(ScribelessError):
    pass


class InvalidRequestError(ScribelessError):
    pass


class APIError(ScribelessError):
    pass


class ScribelessClient:
    """Scribeless API Client - Handwritten letter service"""

    BASE_URL = "https://api.scribeless.io/v1"

    def __init__(self, api_key: str, timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limiter = RateLimiter(max_requests=100, time_window=60)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.rate_limiter.wait_if_needed()
        url = f"{self.BASE_URL}{endpoint}"
        last_error = None

        for attempt in range(self.max_retries):
            try:
                response = self.session.request(method=method, url=url, json=data, timeout=self.timeout)

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

    def create_recipient(
        self,
        name: str,
        address_line1: str,
        city: str,
        postal_code: str,
        country_code: str,
        address_line2: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a recipient for handwritten letter service

        Args:
            name: Recipient's full name (required)
            address_line1: Primary address line (required)
            city: City name (required)
            postal_code: Postal/ZIP code (required)
            country_code: ISO 3166-1 alpha-2 country code (required)
            address_line2: Secondary address line (optional)
            phone: Phone number (optional)
            email: Email address (optional)
            company: Company name (optional)
            metadata: Custom metadata as key-value pairs (optional)

        Returns:
            Dictionary containing:
                - recipient_id: Recipient ID
                - name: Recipient name
                - address: Address details
                - created_at: Timestamp of creation

        Example:
            >>> client = ScribelessClient(api_key="your-api-key")
            >>> result = client.create_recipient(
            ...     name="John Doe",
            ...     address_line1="123 Main St",
            ...     city="New York",
            ...     postal_code="10001",
            ...     country_code="US"
            ... )
        """
        if not all([name, address_line1, city, postal_code, country_code]):
            raise InvalidRequestError("name, address_line1, city, postal_code, and country_code are required")

        data = {
            "name": name,
            "address": {
                "line1": address_line1,
                "city": city,
                "postal_code": postal_code,
                "country_code": country_code.upper()
            }
        }

        if address_line2:
            data["address"]["line2"] = address_line2
        if phone:
            data["phone"] = phone
        if email:
            data["email"] = email
        if company:
            data["company"] = company
        if metadata:
            data["metadata"] = metadata

        return self._make_request("POST", "/recipients", data=data)

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()