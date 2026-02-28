"""
Microsoft Entra ID API - Identity Management Client

Supports:
- Add User
- Delete User
- Search User
- Add User to Group
- Remove User from Group
"""

import aiohttp
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class User:
    """User object"""
    id: str
    user_principal_name: str
    display_name: str
    mail: Optional[str] = None
    given_name: Optional[str] = None
    surname: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    account_enabled: bool = True


@dataclass
class Group:
    """Group object"""
    id: str
    display_name: str
    description: Optional[str] = None
    mail_enabled: bool = False
    security_enabled: bool = True


@dataclass
class GroupMember:
    """Group member object"""
    id: str
    user_principal_name: Optional[str] = None
    display_name: Optional[str] = None
    mail: Optional[str] = None


class EntraIDClient:
    """
    Microsoft Entra ID API client for identity and access management.

    Provides operations for user and group management in Microsoft Entra ID
    (formerly Azure Active Directory).

    API Documentation: https://learn.microsoft.com/en-us/graph/api/overview
    Requires:
    - Azure AD App Registration with appropriate permissions
    - Client ID, Client Secret, and Tenant ID
    """

    BASE_URL = "https://graph.microsoft.com/v1.0"

    def __init__(
        self,
        tenant_id: str,
        client_id: str,
        client_secret: str,
        scope: Optional[List[str]] = None
    ):
        """
        Initialize Entra ID client.

        Args:
            tenant_id: Azure AD tenant ID
            client_id: Application (client) ID from Azure AD app registration
            client_secret: Client secret from Azure AD app registration
            scope: Optional list of OAuth scopes (default: User.ReadWrite.All, Group.ReadWrite.All)
        """
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope or [
            "https://graph.microsoft.com/User.ReadWrite.All",
            "https://graph.microsoft.com/Group.ReadWrite.All"
        ]
        self.session = None
        self.access_token = None
        self._rate_limit_delay = 0.1  # 100ms between requests

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        await self._authenticate()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _authenticate(self) -> None:
        """
        Authenticate with Azure AD and get access token.

        Raises:
            Exception: If authentication fails
        """
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"

        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": " ".join(self.scope)
        }

        try:
            async with self.session.post(url, data=data) as response:
                response_data = await response.json()

                if response.status != 200:
                    error = response_data.get("error_description", response_data.get("error", "Authentication failed"))
                    raise Exception(f"Authentication error: {error}")

                self.access_token = response_data.get("access_token")

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during authentication: {str(e)}")

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated API request.

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
        if not self.access_token:
            await self._authenticate()

        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        try:
            async with self.session.request(
                method,
                url,
                headers=headers,
                params=params,
                data=data,
                json=json_data
            ) as response:
                response_text = await response.text()

                if response.status == 204:
                    return {}

                response_data = await response.json()

                if response.status >= 400:
                    error = response_data.get("error", {})
                    error_message = error.get("message", f"HTTP {response.status} error")
                    raise Exception(f"Entra ID API error: {error_message}")

                return response_data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            # Some DELETE operations return empty responses
            if response.status in [200, 204]:
                return {}
            raise Exception(f"Invalid JSON response: {response_text}")

    # ==================== Add User ====================

    async def add_user(
        self,
        user_principal_name: str,
        display_name: str,
        mail_nickname: str,
        password: str,
        given_name: Optional[str] = None,
        surname: Optional[str] = None,
        job_title: Optional[str] = None,
        department: Optional[str] = None,
        mail: Optional[str] = None,
        account_enabled: bool = True,
        force_change_password_next_sign_in: bool = False
    ) -> User:
        """
        Add a new user to Entra ID.

        Args:
            user_principal_name: User principal name (e.g., user@example.com)
            display_name: Display name for the user
            mail_nickname: Mail nickname (used for email)
            password: Initial password for the user
            given_name: Optional first name
            surname: Optional last name
            job_title: Optional job title
            department: Optional department
            mail: Optional email address
            account_enabled: Whether account is enabled (default: True)
            force_change_password_next_sign_in: Whether user must change password on first login

        Returns:
            User object with created user details

        Raises:
            Exception: If user creation fails or user already exists
            ValueError: If required parameters are invalid
        """
        if not user_principal_name or not display_name:
            raise ValueError("user_principal_name and display_name are required")

        if not mail_nickname:
            mail_nickname = user_principal_name.split("@")[0]

        payload = {
            "accountEnabled": account_enabled,
            "displayName": display_name,
            "mailNickname": mail_nickname,
            "userPrincipalName": user_principal_name,
            "passwordProfile": {
                "forceChangePasswordNextSignIn": force_change_password_next_sign_in,
                "password": password
            }
        }

        if given_name:
            payload["givenName"] = given_name
        if surname:
            payload["surname"] = surname
        if job_title:
            payload["jobTitle"] = job_title
        if department:
            payload["department"] = department
        if mail:
            payload["mail"] = mail

        response_data = await self._make_request(
            "POST",
            "/users",
            json_data=payload
        )

        return User(
            id=response_data.get("id", ""),
            user_principal_name=response_data.get("userPrincipalName", user_principal_name),
            display_name=response_data.get("displayName", display_name),
            mail=response_data.get("mail", mail),
            given_name=response_data.get("givenName"),
            surname=response_data.get("surname"),
            job_title=response_data.get("jobTitle"),
            department=response_data.get("department"),
            account_enabled=response_data.get("accountEnabled", account_enabled)
        )

    # ==================== Delete User ====================

    async def delete_user(self, user_id: str) -> None:
        """
        Delete a user from Entra ID.

        Args:
            user_id: User ID (object ID) to delete

        Raises:
            Exception: If deletion fails or user is not found
            ValueError: If user_id is empty
        """
        if not user_id:
            raise ValueError("user_id is required")

        await self._make_request(
            "DELETE",
            f"/users/{user_id}"
        )

    # ==================== Search User ====================

    async def search_user(
        self,
        search_term: Optional[str] = None,
        filter: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[User]:
        """
        Search for users in Entra ID.

        Args:
            search_term: OData search string (e.g., '"search term"')
            filter: OData filter string (e.g., "startswith(displayName,'John')")
            top: Maximum number of results to return

        Returns:
            List of User objects

        Raises:
            Exception: If search fails
        """
        params = {}
        if search_term:
            params["$search"] = f'"{search_term}"'
            params["$count"] = "true"  # Required for $search
        if filter:
            params["$filter"] = filter
        if top:
            params["$top"] = top

        # Add ConsistencyLevel header for $search
        headers = {"ConsistencyLevel": "eventual"}

        response_data = await self._make_request(
            "GET",
            "/users",
            params=params
        )

        users_list = response_data.get("value", [])

        return [
            User(
                id=user.get("id", ""),
                user_principal_name=user.get("userPrincipalName", ""),
                display_name=user.get("displayName", ""),
                mail=user.get("mail"),
                given_name=user.get("givenName"),
                surname=user.get("surname"),
                job_title=user.get("jobTitle"),
                department=user.get("department"),
                account_enabled=user.get("accountEnabled", True)
            )
            for user in users_list
        ]

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get a specific user by ID.

        Args:
            user_id: User ID (object ID)

        Returns:
            User object or None if not found

        Raises:
            Exception: If request fails
        """
        try:
            response_data = await self._make_request(
                "GET",
                f"/users/{user_id}"
            )

            return User(
                id=response_data.get("id", ""),
                user_principal_name=response_data.get("userPrincipalName", ""),
                display_name=response_data.get("displayName", ""),
                mail=response_data.get("mail"),
                given_name=response_data.get("givenName"),
                surname=response_data.get("surname"),
                job_title=response_data.get("jobTitle"),
                department=response_data.get("department"),
                account_enabled=response_data.get("accountEnabled", True)
            )

        except Exception:
            return None

    async def get_user_by_principal_name(
        self,
        user_principal_name: str
    ) -> Optional[User]:
        """
        Get a user by their principal name.

        Args:
            user_principal_name: User principal name (e.g., user@example.com)

        Returns:
            User object or None if not found

        Raises:
            Exception: If request fails
        """
        users = await self.search_user(
            filter=f"userPrincipalName eq '{user_principal_name}'"
        )

        return users[0] if users else None

    # ==================== Add User to Group ====================

    async def add_user_to_group(
        self,
        group_id: str,
        user_id: str
    ) -> None:
        """
        Add a user to a group.

        Args:
            group_id: Group ID (object ID)
            user_id: User ID (object ID)

        Raises:
            Exception: If operation fails or IDs are invalid
            ValueError: If group_id or user_id is empty
        """
        if not group_id or not user_id:
            raise ValueError("group_id and user_id are required")

        payload = {
            "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"
        }

        await self._make_request(
            "POST",
            f"/groups/{group_id}/members/$ref",
            json_data=payload
        )

    async def add_user_to_group_by_name(
        self,
        group_name: str,
        user_principal_name: str
    ) -> None:
        """
        Add a user to a group by their names.

        Args:
            group_name: Group display name
            user_principal_name: User principal name

        Raises:
            Exception: If operation fails or entities are not found
        """
        # Get group by name
        groups_response = await self._make_request(
            "GET",
            "/groups",
            params={"$filter": f"displayName eq '{group_name}'"}
        )

        groups = groups_response.get("value", [])
        if not groups:
            raise Exception(f"Group not found: {group_name}")

        group_id = groups[0].get("id")

        # Get user by principal name
        user = await self.get_user_by_principal_name(user_principal_name)
        if not user:
            raise Exception(f"User not found: {user_principal_name}")

        # Add to group
        await self.add_user_to_group(group_id, user.id)

    # ==================== Remove User from Group ====================

    async def remove_user_from_group(
        self,
        group_id: str,
        user_id: str
    ) -> None:
        """
        Remove a user from a group.

        Args:
            group_id: Group ID (object ID)
            user_id: User ID (object ID)

        Raises:
            Exception: If operation fails or IDs are invalid
            ValueError: If group_id or user_id is empty
        """
        if not group_id or not user_id:
            raise ValueError("group_id and user_id are required")

        await self._make_request(
            "DELETE",
            f"/groups/{group_id}/members/{user_id}/$ref"
        )

    async def remove_user_from_group_by_name(
        self,
        group_name: str,
        user_principal_name: str
    ) -> None:
        """
        Remove a user from a group by their names.

        Args:
            group_name: Group display name
            user_principal_name: User principal name

        Raises:
            Exception: If operation fails or entities are not found
        """
        # Get group by name
        groups_response = await self._make_request(
            "GET",
            "/groups",
            params={"$filter": f"displayName eq '{group_name}'"}
        )

        groups = groups_response.get("value", [])
        if not groups:
            raise Exception(f"Group not found: {group_name}")

        group_id = groups[0].get("id")

        # Get user by principal name
        user = await self.get_user_by_principal_name(user_principal_name)
        if not user:
            raise Exception(f"User not found: {user_principal_name}")

        # Remove from group
        await self.remove_user_from_group(group_id, user.id)

    # ==================== Group Operations ====================

    async def list_group_members(
        self,
        group_id: str
    ) -> List[GroupMember]:
        """
        List all members of a group.

        Args:
            group_id: Group ID (object ID)

        Returns:
            List of GroupMember objects

        Raises:
            Exception: If request fails
        """
        response_data = await self._make_request(
            "GET",
            f"/groups/{group_id}/members"
        )

        members_list = response_data.get("value", [])

        return [
            GroupMember(
                id=member.get("id", ""),
                user_principal_name=member.get("userPrincipalName"),
                display_name=member.get("displayName"),
                mail=member.get("mail")
            )
            for member in members_list
        ]

    async def get_user_groups(
        self,
        user_id: str
    ) -> List[Group]:
        """
        Get all groups that a user is a member of.

        Args:
            user_id: User ID (object ID)

        Returns:
            List of Group objects

        Raises:
            Exception: If request fails
        """
        response_data = await self._make_request(
            "GET",
            f"/users/{user_id}/memberOf"
        )

        groups_list = response_data.get("value", [])

        return [
            Group(
                id=group.get("id", ""),
                display_name=group.get("displayName", ""),
                description=group.get("description"),
                mail_enabled=group.get("mailEnabled", False),
                security_enabled=group.get("securityEnabled", True)
            )
            for group in groups_list
        ]


# ==================== Example Usage ====================

async def main():
    """Example usage of Entra ID client"""

    # Replace with your actual Azure AD credentials
    TENANT_ID = "your_tenant_id"
    CLIENT_ID = "your_client_id"
    CLIENT_SECRET = "your_client_secret"

    async with EntraIDClient(
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    ) as client:
        try:
            # Add a new user
            new_user = await client.add_user(
                user_principal_name="john.doe@example.com",
                display_name="John Doe",
                mail_nickname="john.doe",
                password="SecurePassword123!",
                given_name="John",
                surname="Doe",
                job_title="Software Engineer",
                department="Engineering",
                account_enabled=True,
                force_change_password_next_sign_in=True
            )
            print(f"Created user: {new_user.display_name} (ID: {new_user.id})")

            # Search for users
            users = await client.search_user(
                filter="startswith(displayName,'John')",
                top=10
            )
            print(f"Found {len(users)} users")
            for user in users:
                print(f"  - {user.display_name} ({user.user_principal_name})")

            # Get user by principal name
            user = await client.get_user_by_principal_name("john.doe@example.com")
            if user:
                print(f"User found: {user.display_name}")

            # Add user to group
            group_id = "group_object_id_here"
            await client.add_user_to_group(group_id, new_user.id)
            print(f"Added user to group {group_id}")

            # List group members
            members = await client.list_group_members(group_id)
            print(f"Group members: {len(members)}")
            for member in members:
                print(f"  - {member.display_name}")

            # Remove user from group
            await client.remove_user_from_group(group_id, new_user.id)
            print(f"Removed user from group")

            # Delete user
            await client.delete_user(new_user.id)
            print("User deleted successfully")

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())