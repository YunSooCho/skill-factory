"""
Keygen - License Management API

Supports:
- Create License
- Get License
- Update License
- Renew License
- Suspend License
- Reinstate License
- Search Licenses
- Create User
- Get User
- Update User
- Search Users
- Request Reset Password
- Reset User Password
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class License:
    """License representation"""
    id: str
    key: str
    product_id: str
    policy_id: str
    user_id: Optional[str]
    status: str
    expiry: str
    created_at: str


@dataclass
class User:
    """User representation"""
    id: str
    name: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: str


class KeygenClient:
    """
    Keygen API client for license management.

    API Documentation: https://keygen.sh/docs/api
    Requires an API key from Keygen.
    """

    BASE_URL = "https://api.keygen.sh/v1"

    def __init__(self, account_id: str, api_key: str):
        """
        Initialize Keygen client.

        Args:
            account_id: Keygen account ID
            api_key: API key
        """
        self.account_id = account_id
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/vnd.api+json"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    # ==================== License Operations ====================

    async def create_license(
        self,
        policy_id: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> License:
        """
        Create a new license.

        Args:
            policy_id: Policy ID for the license
            user_id: User ID (optional)
            metadata: Custom metadata

        Returns:
            License with created license data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "data": {
                    "type": "licenses",
                    "attributes": {
                        "policy": f"policies/{policy_id}"
                    },
                    "relationships": {}
                }
            }

            if user_id:
                payload["data"]["relationships"]["user"] = {
                    "data": {"type": "users", "id": user_id}
                }

            if metadata:
                payload["data"]["attributes"]["metadata"] = metadata

            async with self.session.post(
                f"{self.BASE_URL}/accounts/{self.account_id}/licenses",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"Keygen error: {data.get('errors', 'Unknown error')}")

                attrs = data["data"]["attributes"]

                return License(
                    id=data["data"]["id"],
                    key=attrs.get("key", ""),
                    product_id=data["data"]["relationships"]["product"]["data"]["id"],
                    policy_id=data["data"]["relationships"]["policy"]["data"]["id"],
                    user_id=data["data"]["relationships"].get("user", {}).get("data", {}).get("id"),
                    status=attrs.get("status", ""),
                    expiry=attrs.get("expiry", ""),
                    created_at=attrs.get("created", "")
                )

        except Exception as e:
            raise Exception(f"Failed to create license: {str(e)}")

    async def get_license(self, license_id: str) -> License:
        """
        Get license details.

        Args:
            license_id: License ID

        Returns:
            License with license data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/accounts/{self.account_id}/licenses/{license_id}"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Keygen error: {data.get('errors', 'Unknown error')}")

                attrs = data["data"]["attributes"]

                return License(
                    id=data["data"]["id"],
                    key=attrs.get("key", ""),
                    product_id=data["data"]["relationships"]["product"]["data"]["id"],
                    policy_id=data["data"]["relationships"]["policy"]["data"]["id"],
                    user_id=data["data"]["relationships"].get("user", {}).get("data", {}).get("id"),
                    status=attrs.get("status", ""),
                    expiry=attrs.get("expiry", ""),
                    created_at=attrs.get("created", "")
                )

        except Exception as e:
            raise Exception(f"Failed to get license: {str(e)}")

    async def update_license(
        self,
        license_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> License:
        """
        Update a license.

        Args:
            license_id: License ID
            metadata: New metadata

        Returns:
            License with updated data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "data": {
                    "type": "licenses",
                    "id": license_id,
                    "attributes": {}
                }
            }

            if metadata:
                payload["data"]["attributes"]["metadata"] = metadata

            async with self.session.patch(
                f"{self.BASE_URL}/accounts/{self.account_id}/licenses/{license_id}",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Keygen error: {data.get('errors', 'Unknown error')}")

                attrs = data["data"]["attributes"]

                return License(
                    id=data["data"]["id"],
                    key=attrs.get("key", ""),
                    product_id=data["data"]["relationships"]["product"]["data"]["id"],
                    policy_id=data["data"]["relationships"]["policy"]["data"]["id"],
                    user_id=data["data"]["relationships"].get("user", {}).get("data", {}).get("id"),
                    status=attrs.get("status", ""),
                    expiry=attrs.get("expiry", ""),
                    created_at=attrs.get("created", "")
                )

        except Exception as e:
            raise Exception(f"Failed to update license: {str(e)}")

    async def renew_license(self, license_id: str) -> License:
        """
        Renew a license.

        Args:
            license_id: License ID

        Returns:
            License with renewed data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "data": {
                    "type": "license-actions",
                    "attributes": {
                        "action": "renew"
                    }
                }
            }

            async with self.session.post(
                f"{self.BASE_URL}/accounts/{self.account_id}/licenses/{license_id}/actions",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 202:
                    raise Exception(f"Keygen error: {data.get('errors', 'Unknown error')}")

                attrs = data["data"]["attributes"]

                return License(
                    id=data["data"]["id"],
                    key=attrs.get("key", ""),
                    product_id=data["data"]["relationships"]["product"]["data"]["id"],
                    policy_id=data["data"]["relationships"]["policy"]["data"]["id"],
                    user_id=data["data"]["relationships"].get("user", {}).get("data", {}).get("id"),
                    status=attrs.get("status", ""),
                    expiry=attrs.get("expiry", ""),
                    created_at=attrs.get("created", "")
                )

        except Exception as e:
            raise Exception(f"Failed to renew license: {str(e)}")

    async def suspend_license(self, license_id: str, reason: str = "") -> bool:
        """
        Suspend a license.

        Args:
            license_id: License ID
            reason: Suspension reason

        Returns:
            True if successful

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "data": {
                    "type": "license-actions",
                    "attributes": {
                        "action": "suspend",
                        "reason": reason
                    }
                }
            }

            async with self.session.post(
                f"{self.BASE_URL}/accounts/{self.account_id}/licenses/{license_id}/actions",
                json=payload
            ) as response:
                if response.status != 202:
                    data = await response.json()
                    raise Exception(f"Keygen error: {data.get('errors', 'Unknown error')}")

                return True

        except Exception as e:
            raise Exception(f"Failed to suspend license: {str(e)}")

    async def reinstate_license(self, license_id: str) -> bool:
        """
        Reinstate a suspended license.

        Args:
            license_id: License ID

        Returns:
            True if successful

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "data": {
                    "type": "license-actions",
                    "attributes": {
                        "action": "reinstate"
                    }
                }
            }

            async with self.session.post(
                f"{self.BASE_URL}/accounts/{self.account_id}/licenses/{license_id}/actions",
                json=payload
            ) as response:
                if response.status != 202:
                    data = await response.json()
                    raise Exception(f"Keygen error: {data.get('errors', 'Unknown error')}")

                return True

        except Exception as e:
            raise Exception(f"Failed to reinstate license: {str(e)}")

    async def search_licenses(
        self,
        user_id: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 20
    ) -> List[License]:
        """
        Search for licenses.

        Args:
            user_id: Filter by user ID (optional)
            query: Search query (optional)
            limit: Maximum results

        Returns:
            List of License

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            filters = {"limit": limit}

            if user_id:
                filters["userId"] = user_id
            if query:
                filters["q"] = query

            async with self.session.get(
                f"{self.BASE_URL}/accounts/{self.account_id}/licenses",
                params=filters
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Keygen error: {data.get('errors', 'Unknown error')}")

                licenses = []
                for item in data.get("data", []):
                    attrs = item["attributes"]
                    licenses.append(License(
                        id=item["id"],
                        key=attrs.get("key", ""),
                        product_id=item["relationships"]["product"]["data"]["id"],
                        policy_id=item["relationships"]["policy"]["data"]["id"],
                        user_id=item["relationships"].get("user", {}).get("data", {}).get("id"),
                        status=attrs.get("status", ""),
                        expiry=attrs.get("expiry", ""),
                        created_at=attrs.get("created", "")
                    ))

                return licenses

        except Exception as e:
            raise Exception(f"Failed to search licenses: {str(e)}")

    # ==================== User Operations ====================

    async def create_user(
        self,
        email: str,
        name: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> User:
        """
        Create a new user.

        Args:
            email: User email
            name: Full name (optional)
            first_name: First name (optional)
            last_name: Last name (optional)

        Returns:
            User with created user data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "data": {
                    "type": "users",
                    "attributes": {
                        "email": email
                    }
                }
            }

            if name:
                payload["data"]["attributes"]["name"] = name
            if first_name:
                payload["data"]["attributes"]["firstName"] = first_name
            if last_name:
                payload["data"]["attributes"]["lastName"] = last_name

            async with self.session.post(
                f"{self.BASE_URL}/accounts/{self.account_id}/users",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 201:
                    raise Exception(f"Keygen error: {data.get('errors', 'Unknown error')}")

                attrs = data["data"]["attributes"]

                return User(
                    id=data["data"]["id"],
                    name=attrs.get("name", ""),
                    email=attrs.get("email", ""),
                    first_name=attrs.get("firstName"),
                    last_name=attrs.get("lastName"),
                    created_at=attrs.get("created", "")
                )

        except Exception as e:
            raise Exception(f"Failed to create user: {str(e)}")

    async def get_user(self, user_id: str) -> User:
        """
        Get user details.

        Args:
            user_id: User ID

        Returns:
            User with user data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            async with self.session.get(
                f"{self.BASE_URL}/accounts/{self.account_id}/users/{user_id}"
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Keygen error: {data.get('errors', 'Unknown error')}")

                attrs = data["data"]["attributes"]

                return User(
                    id=data["data"]["id"],
                    name=attrs.get("name", ""),
                    email=attrs.get("email", ""),
                    first_name=attrs.get("firstName"),
                    last_name=attrs.get("lastName"),
                    created_at=attrs.get("created", "")
                )

        except Exception as e:
            raise Exception(f"Failed to get user: {str(e)}")

    async def update_user(
        self,
        user_id: str,
        name: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> User:
        """
        Update a user.

        Args:
            user_id: User ID
            name: Full name (optional)
            first_name: First name (optional)
            last_name: Last name (optional)

        Returns:
            User with updated data

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "data": {
                    "type": "users",
                    "id": user_id,
                    "attributes": {}
                }
            }

            if name:
                payload["data"]["attributes"]["name"] = name
            if first_name:
                payload["data"]["attributes"]["firstName"] = first_name
            if last_name:
                payload["data"]["attributes"]["lastName"] = last_name

            async with self.session.patch(
                f"{self.BASE_URL}/accounts/{self.account_id}/users/{user_id}",
                json=payload
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Keygen error: {data.get('errors', 'Unknown error')}")

                attrs = data["data"]["attributes"]

                return User(
                    id=data["data"]["id"],
                    name=attrs.get("name", ""),
                    email=attrs.get("email", ""),
                    first_name=attrs.get("firstName"),
                    last_name=attrs.get("lastName"),
                    created_at=attrs.get("created", "")
                )

        except Exception as e:
            raise Exception(f"Failed to update user: {str(e)}")

    async def search_users(
        self,
        query: Optional[str] = None,
        limit: int = 20
    ) -> List[User]:
        """
        Search for users.

        Args:
            query: Search query (optional)
            limit: Maximum results

        Returns:
            List of User

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            params = {"limit": limit}

            if query:
                params["q"] = query

            async with self.session.get(
                f"{self.BASE_URL}/accounts/{self.account_id}/users",
                params=params
            ) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(f"Keygen error: {data.get('errors', 'Unknown error')}")

                users = []
                for item in data.get("data", []):
                    attrs = item["attributes"]
                    users.append(User(
                        id=item["id"],
                        name=attrs.get("name", ""),
                        email=attrs.get("email", ""),
                        first_name=attrs.get("firstName"),
                        last_name=attrs.get("lastName"),
                        created_at=attrs.get("created", "")
                    ))

                return users

        except Exception as e:
            raise Exception(f"Failed to search users: {str(e)}")

    async def request_reset_password(self, email: str) -> bool:
        """
        Request a password reset for a user.

        Args:
            email: User email

        Returns:
            True if successful

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "data": {
                    "type": "users",
                    "attributes": {
                        "email": email
                    }
                }
            }

            async with self.session.post(
                f"{self.BASE_URL}/accounts/{self.account_id}/actions/reset-password",
                json=payload
            ) as response:
                if response.status != 202:
                    data = await response.json()
                    raise Exception(f"Keygen error: {data.get('errors', 'Unknown error')}")

                return True

        except Exception as e:
            raise Exception(f"Failed to request password reset: {str(e)}")

    async def reset_user_password(
        self,
        user_id: str,
        new_password: str
    ) -> bool:
        """
        Reset a user's password.

        Args:
            user_id: User ID
            new_password: New password

        Returns:
            True if successful

        Raises:
            ValueError: If API request fails
            aiohttp.ClientError: If request fails
        """
        try:
            payload = {
                "data": {
                    "type": "users",
                    "id": user_id,
                    "attributes": {
                        "password": new_password
                    }
                }
            }

            async with self.session.patch(
                f"{self.BASE_URL}/accounts/{self.account_id}/users/{user_id}",
                json=payload
            ) as response:
                if response.status != 200:
                    data = await response.json()
                    raise Exception(f"Keygen error: {data.get('errors', 'Unknown error')}")

                return True

        except Exception as e:
            raise Exception(f"Failed to reset user password: {str(e)}")