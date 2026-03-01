"""
Phone Appli People API - Phone System Client

Supports:
- Manage internal contacts
- Manage external contacts
- Manage phonebook folders
- Manage departments
- User profile operations
"""

import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import os


@dataclass
class Contact:
    """Contact information"""
    contact_id: str
    name: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    mobile: Optional[str]
    company: Optional[str]
    department_id: Optional[str]
    folder_id: Optional[str]
    is_internal: bool
    created_at: str
    updated_at: str


@dataclass
class Department:
    """Department information"""
    department_id: str
    name: str
    description: Optional[str]
    parent_id: Optional[str]
    manager_id: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class PhonebookFolder:
    """Phonebook folder information"""
    folder_id: str
    name: str
    folder_type: str  # 'personal', 'shared', or 'external'
    owner_id: Optional[str]
    is_shared: bool
    created_at: str
    updated_at: str


@dataclass
class UserProfile:
    """User profile information"""
    user_id: str
    username: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    extension: Optional[str]
    department_id: Optional[str]
    created_at: str
    updated_at: str


class PhoneAppliPeopleClient:
    """
    Phone Appli People API client for phone system management.

    API Documentation: https://lp.yoom.fun/apps/phone-appli-people
    Requires API key from Yoom integration.
    """

    BASE_URL = "https://api.phoneapplipeople.com/v1"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize Phone Appli People client.

        Args:
            api_key: API key (defaults to YOOM_PHONE_APPLI_PEOPLE_API_KEY env var)
            base_url: Custom base URL for testing
        """
        self.api_key = api_key or os.environ.get("YOOM_PHONE_APPLI_PEOPLE_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set YOOM_PHONE_APPLI_PEOPLE_API_KEY environment variable")

        self.base_url = base_url or self.BASE_URL
        self.session = None
        self._rate_limit_delay = 0.3  # 300ms between requests

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request with rate limiting"""
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async with statement")

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        headers["Content-Type"] = "application/json"

        # Rate limiting
        await asyncio.sleep(self._rate_limit_delay)

        url = f"{self.base_url}{endpoint}"

        async with self.session.request(method, url, headers=headers, **kwargs) as response:
            if response.status == 429:
                retry_after = int(response.headers.get("Retry-After", 2))
                await asyncio.sleep(retry_after)
                return await self._request(method, endpoint, **kwargs)

            if response.status >= 400:
                error_text = await response.text()
                raise Exception(f"API error {response.status}: {error_text}")

            if response.status == 204:
                return {}

            return await response.json()

    # ==================== Internal Contact Operations ====================

    async def create_internal_contact(self, contact_data: Dict[str, Any]) -> Contact:
        """Create a new internal contact"""
        data = await self._request("POST", "/contacts/internal", json=contact_data)

        return Contact(
            contact_id=data.get("contact_id", ""),
            name=data.get("name", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            mobile=data.get("mobile"),
            company=data.get("company"),
            department_id=data.get("department_id"),
            folder_id=data.get("folder_id"),
            is_internal=True,
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def get_internal_contact(self, contact_id: str) -> Contact:
        """Get internal contact by ID"""
        data = await self._request("GET", f"/contacts/internal/{contact_id}")

        return Contact(
            contact_id=data.get("contact_id", contact_id),
            name=data.get("name", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            mobile=data.get("mobile"),
            company=data.get("company"),
            department_id=data.get("department_id"),
            folder_id=data.get("folder_id"),
            is_internal=True,
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def update_internal_contact(self, contact_id: str, update_data: Dict[str, Any]) -> Contact:
        """Update internal contact"""
        data = await self._request("PATCH", f"/contacts/internal/{contact_id}", json=update_data)

        return Contact(
            contact_id=data.get("contact_id", contact_id),
            name=data.get("name", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            mobile=data.get("mobile"),
            company=data.get("company"),
            department_id=data.get("department_id"),
            folder_id=data.get("folder_id"),
            is_internal=True,
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def delete_internal_contact(self, contact_id: str) -> Dict[str, Any]:
        """Delete internal contact"""
        return await self._request("DELETE", f"/contacts/internal/{contact_id}")

    async def search_internal_contacts(self, query: Optional[str] = None, **filters) -> List[Contact]:
        """Search internal contacts"""
        params = {"query": query} if query else {}
        params.update(filters)

        data = await self._request("GET", "/contacts/internal", params=params)

        contacts = []
        for item in data.get("contacts", []):
            contacts.append(Contact(
                contact_id=item.get("contact_id", ""),
                name=item.get("name", ""),
                first_name=item.get("first_name"),
                last_name=item.get("last_name"),
                email=item.get("email"),
                phone=item.get("phone"),
                mobile=item.get("mobile"),
                company=item.get("company"),
                department_id=item.get("department_id"),
                folder_id=item.get("folder_id"),
                is_internal=True,
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return contacts

    # ==================== External Contact Operations ====================

    async def create_external_contact(self, contact_data: Dict[str, Any]) -> Contact:
        """Create a new external contact"""
        data = await self._request("POST", "/contacts/external", json=contact_data)

        return Contact(
            contact_id=data.get("contact_id", ""),
            name=data.get("name", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            mobile=data.get("mobile"),
            company=data.get("company"),
            department_id=data.get("department_id"),
            folder_id=data.get("folder_id"),
            is_internal=False,
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def get_external_contact(self, contact_id: str) -> Contact:
        """Get external contact by ID"""
        data = await self._request("GET", f"/contacts/external/{contact_id}")

        return Contact(
            contact_id=data.get("contact_id", contact_id),
            name=data.get("name", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            mobile=data.get("mobile"),
            company=data.get("company"),
            department_id=data.get("department_id"),
            folder_id=data.get("folder_id"),
            is_internal=False,
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def update_external_contact(self, contact_id: str, update_data: Dict[str, Any]) -> Contact:
        """Update external contact"""
        data = await self._request("PATCH", f"/contacts/external/{contact_id}", json=update_data)

        return Contact(
            contact_id=data.get("contact_id", contact_id),
            name=data.get("name", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            mobile=data.get("mobile"),
            company=data.get("company"),
            department_id=data.get("department_id"),
            folder_id=data.get("folder_id"),
            is_internal=False,
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def delete_external_contact(self, contact_id: str) -> Dict[str, Any]:
        """Delete external contact"""
        return await self._request("DELETE", f"/contacts/external/{contact_id}")

    async def search_external_contacts(self, query: Optional[str] = None, **filters) -> List[Contact]:
        """Search external contacts"""
        params = {"query": query} if query else {}
        params.update(filters)

        data = await self._request("GET", "/contacts/external", params=params)

        contacts = []
        for item in data.get("contacts", []):
            contacts.append(Contact(
                contact_id=item.get("contact_id", ""),
                name=item.get("name", ""),
                first_name=item.get("first_name"),
                last_name=item.get("last_name"),
                email=item.get("email"),
                phone=item.get("phone"),
                mobile=item.get("mobile"),
                company=item.get("company"),
                department_id=item.get("department_id"),
                folder_id=item.get("folder_id"),
                is_internal=False,
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return contacts

    # ==================== Phonebook Folder Operations ====================

    async def search_external_phonebook_folders(self, **filters) -> List[PhonebookFolder]:
        """Search external phonebook folders"""
        data = await self._request("GET", "/folders/external", params=filters)

        folders = []
        for item in data.get("folders", []):
            folders.append(PhonebookFolder(
                folder_id=item.get("folder_id", ""),
                name=item.get("name", ""),
                folder_type=item.get("folder_type", "external"),
                owner_id=item.get("owner_id"),
                is_shared=item.get("is_shared", False),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return folders

    async def create_personal_folder(self, folder_data: Dict[str, Any]) -> PhonebookFolder:
        """Create personal phonebook folder"""
        data = await self._request("POST", "/folders/personal", json=folder_data)

        return PhonebookFolder(
            folder_id=data.get("folder_id", ""),
            name=data.get("name", ""),
            folder_type="personal",
            owner_id=data.get("owner_id"),
            is_shared=False,
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def update_personal_folder(self, folder_id: str, update_data: Dict[str, Any]) -> PhonebookFolder:
        """Update personal phonebook folder"""
        data = await self._request("PATCH", f"/folders/personal/{folder_id}", json=update_data)

        return PhonebookFolder(
            folder_id=data.get("folder_id", folder_id),
            name=data.get("name", ""),
            folder_type="personal",
            owner_id=data.get("owner_id"),
            is_shared=False,
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def create_shared_folder(self, folder_data: Dict[str, Any]) -> PhonebookFolder:
        """Create shared phonebook folder"""
        data = await self._request("POST", "/folders/shared", json=folder_data)

        return PhonebookFolder(
            folder_id=data.get("folder_id", ""),
            name=data.get("name", ""),
            folder_type="shared",
            owner_id=data.get("owner_id"),
            is_shared=True,
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def update_shared_folder(self, folder_id: str, update_data: Dict[str, Any]) -> PhonebookFolder:
        """Update shared phonebook folder"""
        data = await self._request("PATCH", f"/folders/shared/{folder_id}", json=update_data)

        return PhonebookFolder(
            folder_id=data.get("folder_id", folder_id),
            name=data.get("name", ""),
            folder_type="shared",
            owner_id=data.get("owner_id"),
            is_shared=True,
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Department Operations ====================

    async def create_department(self, department_data: Dict[str, Any]) -> Department:
        """Create a new department"""
        data = await self._request("POST", "/departments", json=department_data)

        return Department(
            department_id=data.get("department_id", ""),
            name=data.get("name", ""),
            description=data.get("description"),
            parent_id=data.get("parent_id"),
            manager_id=data.get("manager_id"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat())
        )

    async def get_department(self, department_id: str) -> Department:
        """Get department by ID"""
        data = await self._request("GET", f"/departments/{department_id}")

        return Department(
            department_id=data.get("department_id", department_id),
            name=data.get("name", ""),
            description=data.get("description"),
            parent_id=data.get("parent_id"),
            manager_id=data.get("manager_id"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def update_department(self, department_id: str, update_data: Dict[str, Any]) -> Department:
        """Update department"""
        data = await self._request("PATCH", f"/departments/{department_id}", json=update_data)

        return Department(
            department_id=data.get("department_id", department_id),
            name=data.get("name", ""),
            description=data.get("description"),
            parent_id=data.get("parent_id"),
            manager_id=data.get("manager_id"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def delete_department(self, department_id: str) -> Dict[str, Any]:
        """Delete department"""
        return await self._request("DELETE", f"/departments/{department_id}")

    async def search_departments(self, query: Optional[str] = None, **filters) -> List[Department]:
        """Search departments"""
        params = {"query": query} if query else {}
        params.update(filters)

        data = await self._request("GET", "/departments", params=params)

        departments = []
        for item in data.get("departments", []):
            departments.append(Department(
                department_id=item.get("department_id", ""),
                name=item.get("name", ""),
                description=item.get("description"),
                parent_id=item.get("parent_id"),
                manager_id=item.get("manager_id"),
                created_at=item.get("created_at", ""),
                updated_at=item.get("updated_at", "")
            ))

        return departments

    # ==================== User Profile Operations ====================

    async def get_user_profile(self, user_id: str) -> UserProfile:
        """Get user profile"""
        data = await self._request("GET", f"/users/{user_id}/profile")

        return UserProfile(
            user_id=data.get("user_id", user_id),
            username=data.get("username", ""),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            extension=data.get("extension"),
            department_id=data.get("department_id"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    async def update_user_profile(self, user_id: str, update_data: Dict[str, Any]) -> UserProfile:
        """Update user profile"""
        data = await self._request("PATCH", f"/users/{user_id}/profile", json=update_data)

        return UserProfile(
            user_id=data.get("user_id", user_id),
            username=data.get("username", ""),
            name=data.get("name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
            extension=data.get("extension"),
            department_id=data.get("department_id"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", "")
        )

    # ==================== Webhook Handlers ====================

    async def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming webhook events"""
        event_type = payload.get("event_type")
        event_data = payload.get("data", {})

        if event_type == "incoming_call":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "outgoing_call":
            return {"status": "acknowledged", "event_type": event_type}
        elif event_type == "external_contact_created_or_updated":
            return {"status": "acknowledged", "event_type": event_type}
        else:
            return {"status": "acknowledged", "event_type": event_type}