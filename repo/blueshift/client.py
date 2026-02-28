"""
Blueshift API Client

Supports:
- Sync Customer Data
- Send Email Campaign
- Send SMS Campaign
- Track Customer Event
- Get Customer Profile
- Create Campaign
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Customer:
    """Customer data"""
    customer_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    attributes: Dict[str, Any] = None
    segments: List[str] = None

    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}
        if self.segments is None:
            self.segments = []


@dataclass
class Campaign:
    """Campaign data"""
    campaign_id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    recipient_count: int = 0


@dataclass
class Event:
    """Customer event"""
    event_name: Optional[str] = None
    customer_id: Optional[str] = None
    properties: Dict[str, Any] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}


class BlueshiftClient:
    """
    Blueshift API client for customer data platform and marketing automation.

    Authentication: API Key (Header: X-API-Key)
    Base URL: https://api.getblueshift.com/v1
    """

    BASE_URL = "https://api.getblueshift.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Blueshift client.

        Args:
            api_key: Blueshift API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling and rate limiting"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201, 202, 204):
                if response.status_code == 204:
                    return {}
                data = response.json()
                return data
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid API key")
            elif response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Please retry later.")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Customer Data ====================

    def sync_customer(
        self,
        customer_id: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None
    ) -> Customer:
        """
        Sync customer data.

        Args:
            customer_id: Unique customer ID
            email: Email address
            phone: Phone number
            first_name: First name
            last_name: Last name
            attributes: Custom attributes

        Returns:
            Customer object
        """
        if not customer_id:
            raise ValueError("Customer ID is required")

        payload: Dict[str, Any] = {"customer_id": customer_id}

        if email:
            payload["email"] = email
        if phone:
            payload["phone"] = phone
        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if attributes:
            payload["customer_attributes"] = attributes

        result = self._request("POST", "/customer/sync", json=payload)
        return self._parse_customer(result)

    # ==================== Customer Events ====================

    def track_event(
        self,
        event_name: str,
        customer_id: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Track a customer event.

        Args:
            event_name: Event name
            customer_id: Customer ID
            properties: Event properties

        Returns:
            Event tracking response
        """
        if not event_name:
            raise ValueError("Event name is required")
        if not customer_id:
            raise ValueError("Customer ID is required")

        payload: Dict[str, Any] = {
            "event_name": event_name,
            "customer_id": customer_id
        }

        if properties:
            payload["properties"] = properties

        return self._request("POST", "/event/track", json=payload)

    # ==================== Customer Profile ====================

    def get_customer_profile(self, customer_id: str) -> Customer:
        """
        Get customer profile.

        Args:
            customer_id: Customer ID

        Returns:
            Customer object
        """
        if not customer_id:
            raise ValueError("Customer ID is required")

        result = self._request("GET", f"/customers/{customer_id}")
        return self._parse_customer(result)

    # ==================== Campaign Operations ====================

    def create_campaign(
        self,
        name: str,
        campaign_type: str,
        triggers: Optional[Dict[str, Any]] = None
    ) -> Campaign:
        """
        Create a new campaign.

        Args:
            name: Campaign name
            campaign_type: Campaign type (email, sms, push, etc.)
            triggers: Campaign triggers

        Returns:
            Campaign object
        """
        if not name:
            raise ValueError("Campaign name is required")
        if not campaign_type:
            raise ValueError("Campaign type is required")

        payload: Dict[str, Any] = {
            "name": name,
            "type": campaign_type
        }

        if triggers:
            payload["triggers"] = triggers

        result = self._request("POST", "/campaigns", json=payload)
        return self._parse_campaign(result)

    def send_email_campaign(
        self,
        customer_ids: List[str],
        campaign_uuid: str,
        variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send an email campaign to customers.

        Args:
            customer_ids: List of customer IDs
            campaign_uuid: Campaign UUID
            variables: Template variables

        Returns:
            Send response
        """
        if not customer_ids:
            raise ValueError("At least one customer ID is required")
        if not campaign_uuid:
            raise ValueError("Campaign UUID is required")

        payload: Dict[str, Any] = {
            "customer_ids": customer_ids,
            "campaign_uuid": campaign_uuid
        }

        if variables:
            payload["variables"] = variables

        return self._request("POST", "/campaigns/send/email", json=payload)

    def send_sms_campaign(
        self,
        customer_ids: List[str],
        campaign_uuid: str,
        variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send an SMS campaign to customers.

        Args:
            customer_ids: List of customer IDs
            campaign_uuid: Campaign UUID
            variables: Template variables

        Returns:
            Send response
        """
        if not customer_ids:
            raise ValueError("At least one customer ID is required")
        if not campaign_uuid:
            raise ValueError("Campaign UUID is required")

        payload: Dict[str, Any] = {
            "customer_ids": customer_ids,
            "campaign_uuid": campaign_uuid
        }

        if variables:
            payload["variables"] = variables

        return self._request("POST", "/campaigns/send/sms", json=payload)

    # ==================== Helper Methods ====================

    def _parse_customer(self, data: Dict[str, Any]) -> Customer:
        """Parse customer data from API response"""
        return Customer(
            customer_id=data.get("customer_id"),
            email=data.get("email"),
            phone=data.get("phone"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            attributes=data.get("attributes", {}),
            segments=data.get("segments", [])
        )

    def _parse_campaign(self, data: Dict[str, Any]) -> Campaign:
        """Parse campaign data from API response"""
        return Campaign(
            campaign_id=data.get("uuid"),
            name=data.get("name"),
            type=data.get("type"),
            status=data.get("status"),
            created_at=data.get("created_at"),
            recipient_count=data.get("recipient_count", 0)
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_blueshift_api_key"

    client = BlueshiftClient(api_key=api_key)

    try:
        # Sync customer data
        customer = client.sync_customer(
            customer_id="cust123",
            email="user@example.com",
            first_name="John",
            last_name="Doe",
            attributes={"plan": "premium", "signup_date": "2024-01-15"}
        )
        print(f"Customer synced: {customer.email}")

        # Track event
        client.track_event(
            event_name="purchase",
            customer_id="cust123",
            properties={"product_id": "prod123", "amount": 99.99}
        )
        print("Event tracked successfully")

        # Get customer profile
        profile = client.get_customer_profile("cust123")
        print(f"Profile: {profile.first_name} {profile.last_name}")

        # Create campaign
        campaign = client.create_campaign(
            name="Welcome Campaign",
            campaign_type="email"
        )
        print(f"Campaign created: {campaign.campaign_id}")

        # Send email campaign
        response = client.send_email_campaign(
            customer_ids=["cust123"],
            campaign_uuid=campaign.campaign_id,
            variables={"first_name": "John"}
        )
        print("Email campaign sent")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()