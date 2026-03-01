"""
eSIM API - Embedded SIM Management Client

Supports:
- Create Order Profile
- Delete Profile
- Check Account Balance
- Cancel Profile
- Search Packages
- Suspend Profile
- Search Profiles
- Unsuspend Profile
- Handle Webhook (for triggers)
"""

import aiohttp
import json
import hmac
import hashlib
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Profile:
    """eSIM profile object"""
    id: str
    iccid: str
    status: str
    activation_code: Optional[str] = None
    plan_name: Optional[str] = None
    data_limit: Optional[int] = None
    data_used: Optional[int] = None
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    country: Optional[str] = None
    operator: Optional[str] = None


@dataclass
class Package:
    """eSIM package object"""
    id: str
    name: str
    country: str
    data_limit: int
    validity_days: int
    price: float
    currency: str
    operator: Optional[str] = None
    network_type: Optional[str] = None


@dataclass
class AccountBalance:
    """Account balance object"""
    balance: float
    currency: str
    available_credit: float


@dataclass
class WebhookEvent:
    """Webhook event object"""
    event_type: str
    timestamp: str
    data: Dict[str, Any]
    profile_id: Optional[str] = None


class EsimClient:
    """
    eSIM API client for managing embedded SIM profiles.

    Provides operations for eSIM profile lifecycle management, package searching,
    and account balance checking.

    API Documentation: https://lp.yoom.fun/apps/esim
    Requires an API key from your eSIM provider.
    """

    BASE_URL = "https://api.esim-provider.com/v1"

    def __init__(
        self,
        api_key: str,
        webhook_secret: Optional[str] = None
    ):
        """
        Initialize eSIM client.

        Args:
            api_key: eSIM provider API key
            webhook_secret: Optional secret for webhook signature verification
        """
        self.api_key = api_key
        self.webhook_secret = webhook_secret
        self.session = None
        self._rate_limit_delay = 0.1

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an API request with error handling.

        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Form data
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails or returns error
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            async with self.session.request(
                method,
                url,
                params=params,
                data=data,
                json=json_data
            ) as response:
                response_data = await response.json()

                if response.status >= 400:
                    error_message = response_data.get("error", response_data.get("message", "Unknown error"))
                    raise Exception(
                        f"eSIM API error (Status {response.status}): {error_message}"
                    )

                return response_data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")

    # ==================== Create Order Profile ====================

    async def create_order_profile(
        self,
        package_id: str,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        customer_reference: Optional[str] = None
    ) -> Profile:
        """
        Create a new eSIM profile order.

        Args:
            package_id: Package ID to purchase
            email: Optional email address for profile delivery
            phone_number: Optional phone number for notifications
            customer_reference: Optional customer reference ID

        Returns:
            Profile object with order details

        Raises:
            Exception: If order creation fails
            ValueError: If package_id is invalid
        """
        if not package_id:
            raise ValueError("package_id is required")

        payload = {"package_id": package_id}

        if email:
            payload["email"] = email
        if phone_number:
            payload["phone_number"] = phone_number
        if customer_reference:
            payload["customer_reference"] = customer_reference

        response_data = await self._make_request(
            "POST",
            "/profiles/order",
            json_data=payload
        )

        return Profile(
            id=response_data.get("id", ""),
            iccid=response_data.get("iccid", ""),
            status=response_data.get("status", "ordered"),
            activation_code=response_data.get("activation_code"),
            plan_name=response_data.get("plan_name"),
            data_limit=response_data.get("data_limit"),
            data_used=response_data.get("data_used", 0),
            valid_from=response_data.get("valid_from"),
            valid_until=response_data.get("valid_until"),
            country=response_data.get("country"),
            operator=response_data.get("operator")
        )

    # ==================== Delete Profile ====================

    async def delete_profile(self, profile_id: str) -> None:
        """
        Delete an eSIM profile.

        Args:
            profile_id: Profile ID to delete

        Raises:
            Exception: If deletion fails
            ValueError: If profile_id is empty
        """
        if not profile_id:
            raise ValueError("profile_id is required")

        await self._make_request(
            "DELETE",
            f"/profiles/{profile_id}"
        )

    # ==================== Check Account Balance ====================

    async def check_account_balance(self) -> AccountBalance:
        """
        Check the account balance.

        Returns:
            AccountBalance object with balance information

        Raises:
            Exception: If request fails
        """
        response_data = await self._make_request(
            "GET",
            "/account/balance"
        )

        return AccountBalance(
            balance=response_data.get("balance", 0.0),
            currency=response_data.get("currency", "USD"),
            available_credit=response_data.get("available_credit", 0.0)
        )

    # ==================== Cancel Profile ====================

    async def cancel_profile(
        self,
        profile_id: str,
        reason: Optional[str] = None
    ) -> Profile:
        """
        Cancel an eSIM profile.

        Args:
            profile_id: Profile ID to cancel
            reason: Optional cancellation reason

        Returns:
            Updated Profile object

        Raises:
            Exception: If cancellation fails
            ValueError: If profile_id is empty
        """
        if not profile_id:
            raise ValueError("profile_id is required")

        payload = {}
        if reason:
            payload["reason"] = reason

        response_data = await self._make_request(
            "POST",
            f"/profiles/{profile_id}/cancel",
            json_data=payload
        )

        return Profile(
            id=response_data.get("id", profile_id),
            iccid=response_data.get("iccid", ""),
            status=response_data.get("status", "cancelled"),
            activation_code=response_data.get("activation_code"),
            plan_name=response_data.get("plan_name"),
            data_limit=response_data.get("data_limit"),
            data_used=response_data.get("data_used"),
            valid_from=response_data.get("valid_from"),
            valid_until=response_data.get("valid_until"),
            country=response_data.get("country"),
            operator=response_data.get("operator")
        )

    # ==================== Search Packages ====================

    async def search_packages(
        self,
        country: Optional[str] = None,
        region: Optional[str] = None,
        data_min: Optional[int] = None,
        data_max: Optional[int] = None,
        validity_min: Optional[int] = None,
        validity_max: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[Package]:
        """
        Search for available eSIM packages.

        Args:
            country: Filter by country code (e.g., "US", "JP", "GB")
            region: Filter by region
            data_min: Minimum data limit in MB
            data_max: Maximum data limit in MB
            validity_min: Minimum validity in days
            validity_max: Maximum validity in days
            limit: Maximum number of results to return

        Returns:
            List of Package objects

        Raises:
            Exception: If search fails
        """
        params = {}

        if country:
            params["country"] = country
        if region:
            params["region"] = region
        if data_min:
            params["data_min"] = data_min
        if data_max:
            params["data_max"] = data_max
        if validity_min:
            params["validity_min"] = validity_min
        if validity_max:
            params["validity_max"] = validity_max
        if limit:
            params["limit"] = limit

        response_data = await self._make_request(
            "GET",
            "/packages/search",
            params=params
        )

        packages_list = response_data.get("packages", [])

        return [
            Package(
                id=pkg.get("id", ""),
                name=pkg.get("name", ""),
                country=pkg.get("country", ""),
                data_limit=pkg.get("data_limit", 0),
                validity_days=pkg.get("validity_days", 0),
                price=pkg.get("price", 0.0),
                currency=pkg.get("currency", "USD"),
                operator=pkg.get("operator"),
                network_type=pkg.get("network_type")
            )
            for pkg in packages_list
        ]

    async def get_package(self, package_id: str) -> Optional[Package]:
        """
        Get details of a specific package.

        Args:
            package_id: Package ID

        Returns:
            Package object or None if not found

        Raises:
            Exception: If request fails
        """
        try:
            response_data = await self._make_request(
                "GET",
                f"/packages/{package_id}"
            )

            return Package(
                id=response_data.get("id", ""),
                name=response_data.get("name", ""),
                country=response_data.get("country", ""),
                data_limit=response_data.get("data_limit", 0),
                validity_days=response_data.get("validity_days", 0),
                price=response_data.get("price", 0.0),
                currency=response_data.get("currency", "USD"),
                operator=response_data.get("operator"),
                network_type=response_data.get("network_type")
            )

        except Exception:
            return None

    # ==================== Suspend Profile ====================

    async def suspend_profile(
        self,
        profile_id: str,
        reason: Optional[str] = None
    ) -> Profile:
        """
        Suspend an eSIM profile.

        Args:
            profile_id: Profile ID to suspend
            reason: Optional suspension reason

        Returns:
            Updated Profile object

        Raises:
            Exception: If suspension fails
            ValueError: If profile_id is empty
        """
        if not profile_id:
            raise ValueError("profile_id is required")

        payload = {}
        if reason:
            payload["reason"] = reason

        response_data = await self._make_request(
            "POST",
            f"/profiles/{profile_id}/suspend",
            json_data=payload
        )

        return Profile(
            id=response_data.get("id", profile_id),
            iccid=response_data.get("iccid", ""),
            status=response_data.get("status", "suspended"),
            activation_code=response_data.get("activation_code"),
            plan_name=response_data.get("plan_name"),
            data_limit=response_data.get("data_limit"),
            data_used=response_data.get("data_used"),
            valid_from=response_data.get("valid_from"),
            valid_until=response_data.get("valid_until"),
            country=response_data.get("country"),
            operator=response_data.get("operator")
        )

    # ==================== Search Profiles ====================

    async def search_profiles(
        self,
        status: Optional[str] = None,
        iccid: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Profile]:
        """
        Search for eSIM profiles.

        Args:
            status: Filter by status (active, suspended, cancelled, expired)
            iccid: Filter by ICCID
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            List of Profile objects

        Raises:
            Exception: If search fails
        """
        params = {}

        if status:
            params["status"] = status
        if iccid:
            params["iccid"] = iccid
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        response_data = await self._make_request(
            "GET",
            "/profiles",
            params=params
        )

        profiles_list = response_data.get("profiles", [])

        return [
            Profile(
                id=profile.get("id", ""),
                iccid=profile.get("iccid", ""),
                status=profile.get("status", ""),
                activation_code=profile.get("activation_code"),
                plan_name=profile.get("plan_name"),
                data_limit=profile.get("data_limit"),
                data_used=profile.get("data_used"),
                valid_from=profile.get("valid_from"),
                valid_until=profile.get("valid_until"),
                country=profile.get("country"),
                operator=profile.get("operator")
            )
            for profile in profiles_list
        ]

    async def get_profile(self, profile_id: str) -> Optional[Profile]:
        """
        Get details of a specific profile.

        Args:
            profile_id: Profile ID

        Returns:
            Profile object or None if not found

        Raises:
            Exception: If request fails
        """
        try:
            response_data = await self._make_request(
                "GET",
                f"/profiles/{profile_id}"
            )

            return Profile(
                id=response_data.get("id", ""),
                iccid=response_data.get("iccid", ""),
                status=response_data.get("status", ""),
                activation_code=response_data.get("activation_code"),
                plan_name=response_data.get("plan_name"),
                data_limit=response_data.get("data_limit"),
                data_used=response_data.get("data_used"),
                valid_from=response_data.get("valid_from"),
                valid_until=response_data.get("valid_until"),
                country=response_data.get("country"),
                operator=response_data.get("operator")
            )

        except Exception:
            return None

    # ==================== Unsuspend Profile ====================

    async def unsuspend_profile(
        self,
        profile_id: str
    ) -> Profile:
        """
        Unsuspend an eSIM profile.

        Args:
            profile_id: Profile ID to unsuspend

        Returns:
            Updated Profile object

        Raises:
            Exception: If unsuspension fails
            ValueError: If profile_id is empty
        """
        if not profile_id:
            raise ValueError("profile_id is required")

        response_data = await self._make_request(
            "POST",
            f"/profiles/{profile_id}/unsuspend"
        )

        return Profile(
            id=response_data.get("id", profile_id),
            iccid=response_data.get("iccid", ""),
            status=response_data.get("status", "active"),
            activation_code=response_data.get("activation_code"),
            plan_name=response_data.get("plan_name"),
            data_limit=response_data.get("data_limit"),
            data_used=response_data.get("data_used"),
            valid_from=response_data.get("valid_from"),
            valid_until=response_data.get("valid_until"),
            country=response_data.get("country"),
            operator=response_data.get("operator")
        )

    # ==================== Webhook Handling ====================

    async def handle_webhook(
        self,
        payload: bytes,
        signature: Optional[str] = None
    ) -> WebhookEvent:
        """
        Handle incoming webhook events.

        Supported events:
        - low_data_capacity: Data usage reaches low threshold
        - expired_plan: Plan has expired
        - changed_esim_status: eSIM status changed
        - changed_profile_status: Profile status changed
        - new_order_profile: New profile order created

        Args:
            payload: Raw webhook payload
            signature: Optional signature for verification

        Returns:
            WebhookEvent object

        Raises:
            Exception: If webhook is invalid or verification fails
        """
        # Verify signature if secret is configured
        if self.webhook_secret and signature:
            expected_signature = hmac.new(
                self.webhook_secret.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(expected_signature, signature):
                raise Exception("Invalid webhook signature")

        try:
            event_data = json.loads(payload.decode("utf-8"))
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid webhook payload: {str(e)}")

        return WebhookEvent(
            event_type=event_data.get("event_type", ""),
            timestamp=event_data.get("timestamp", datetime.utcnow().isoformat()),
            data=event_data.get("data", {}),
            profile_id=event_data.get("profile_id")
        )

    def verify_webhook_signature(
        self,
        payload: bytes,
        signature: str
    ) -> bool:
        """
        Verify webhook signature.

        Args:
            payload: Raw webhook payload
            signature: Signature to verify

        Returns:
            True if signature is valid, False otherwise
        """
        if not self.webhook_secret:
            return False

        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)


# ==================== Example Usage ====================

async def main():
    """Example usage of eSIM client"""

    # Replace with your actual API key
    API_KEY = "your_esim_api_key"
    WEBHOOK_SECRET = "your_webhook_secret"

    async with EsimClient(api_key=API_KEY, webhook_secret=WEBHOOK_SECRET) as client:
        try:
            # Check account balance
            balance = await client.check_account_balance()
            print(f"Account balance: {balance.balance} {balance.currency}")

            # Search for packages
            packages = await client.search_packages(
                country="US",
                data_min=1000,
                validity_min=7
            )
            print(f"Found {len(packages)} packages")
            for pkg in packages[:3]:
                print(f"  - {pkg.name}: {pkg.data_limit}MB, {pkg.validity_days} days")

            # Create profile order
            if packages:
                order_profile = await client.create_order_profile(
                    package_id=packages[0].id,
                    email="user@example.com",
                    customer_reference="REF-12345"
                )
                print(f"Order created: {order_profile.id}, Status: {order_profile.status}")

                # Search profiles
                profiles = await client.search_profiles(status="ordered")
                print(f"Found {len(profiles)} profiles")

                # Get profile details
                if profiles:
                    profile_info = await client.get_profile(profiles[0].id)
                    print(f"Profile: {profile_info.plan_name} ({profile_info.status})")

                    # Suspend profile
                    suspended = await client.suspend_profile(profiles[0].id)
                    print(f"Profile suspended: {suspended.status}")

                    # Unsuspend profile
                    unsuspended = await client.unsuspend_profile(profiles[0].id)
                    print(f"Profile unsuspended: {unsuspended.status}")

                    # Cancel profile
                    cancelled = await client.cancel_profile(profiles[0].id, reason="Test")
                    print(f"Profile cancelled: {cancelled.status}")

                    # Delete profile
                    await client.delete_profile(profiles[0].id)
                    print("Profile deleted")

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())