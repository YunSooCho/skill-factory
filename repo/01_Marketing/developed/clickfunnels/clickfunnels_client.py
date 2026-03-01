"""
ClickFunnels API Client

Supports:
- Create Contact
- Get Contact
- Update Contact
- Delete Contact
- Search Contacts
- Get List All Tags in Workspace
- Create Contact Tag
- Update Contact Tag
- Remove Contact Tag
- Create Applied Tag
- Get List of Tags Applied to Contact
- Remove Applied Tag
- Create New Enrollment
- Update Enrollment
- Search Enrollments
- Get List Courses
- Webhook Triggers for events
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class Contact:
    """Contact data"""
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    workspace_id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    tags: List[str]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class Tag:
    """Tag data"""
    id: str
    name: str
    color: Optional[str]
    workspace_id: str
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class Enrollment:
    """Course enrollment data"""
    id: str
    contact_id: str
    course_id: str
    workspace_id: str
    status: str
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class Course:
    """Course data"""
    id: str
    name: str
    description: Optional[str]
    workspace_id: str
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class WebhookEvent:
    """Webhook event data"""
    event_type: str
    contact_id: Optional[str]
    order_id: Optional[str]
    timestamp: datetime
    payload: Dict[str, Any]


class ClickFunnelsClient:
    """
    ClickFunnels API client for contacts, tags, and course enrollments.

    API Documentation: https://knowledgebase.clickfunnels.com/api-documentation
    """

    BASE_URL = "https://api.myclickfunnels.com"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize ClickFunnels client.

        Args:
            api_key: API key for authentication
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        return {
            "User-Agent": "ClickFunnelsClient/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _get_auth(self) -> Dict[str, str]:
        """Get authentication"""
        return {
            "Authorization": f"Bearer {self.api_key}"
        }

    # ==================== Contact Management ====================

    async def create_contact(
        self,
        workspace_id: str,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Contact:
        """
        Create a new contact.

        Args:
            workspace_id: Workspace ID
            email: Contact email
            first_name: First name (optional)
            last_name: Last name (optional)
            phone: Phone number (optional)
            tags: List of tag IDs to apply (optional)

        Returns:
            Contact: Created contact data

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")
        if not email or not email.strip():
            raise ValueError("email is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/contacts"

        payload = {
            "email": email.strip()
        }

        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if phone:
            payload["phone"] = phone
        if tags:
            payload["tags"] = tags

        try:
            async with self.session.post(
                url,
                headers={**self._get_headers(), **self._get_auth()},
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_contact(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 400:
                raise ValueError(f"Invalid request parameters: {e.message}")
            elif e.status == 401:
                raise ValueError("Invalid or missing API key")
            elif e.status == 404:
                raise ValueError(f"Workspace {workspace_id} not found")
            elif e.status == 409:
                raise ValueError("Contact with this email already exists")
            elif e.status == 429:
                raise ValueError(f"Rate limit exceeded. Please try again later.")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from API")

    async def get_contact(self, workspace_id: str, contact_id: str) -> Contact:
        """
        Get contact information.

        Args:
            workspace_id: Workspace ID
            contact_id: Contact ID

        Returns:
            Contact: Contact data

        Raises:
            ValueError: If contact not found
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")
        if not contact_id:
            raise ValueError("contact_id is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/contacts/{contact_id}"

        try:
            async with self.session.get(
                url,
                headers={**self._get_headers(), **self._get_auth()}
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_contact(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Contact {contact_id} not found")
            elif e.status == 401:
                raise ValueError("Invalid or missing API key")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def update_contact(
        self,
        workspace_id: str,
        contact_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Contact:
        """
        Update contact information.

        Args:
            workspace_id: Workspace ID
            contact_id: Contact ID
            email: New email (optional)
            first_name: New first name (optional)
            last_name: New last name (optional)
            phone: New phone (optional)

        Returns:
            Contact: Updated contact data

        Raises:
            ValueError: If contact not found
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")
        if not contact_id:
            raise ValueError("contact_id is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/contacts/{contact_id}"

        payload = {}
        if email:
            payload["email"] = email.strip()
        if first_name is not None:
            payload["first_name"] = first_name
        if last_name is not None:
            payload["last_name"] = last_name
        if phone is not None:
            payload["phone"] = phone

        if not payload:
            raise ValueError("At least one field to update must be provided")

        try:
            async with self.session.patch(
                url,
                headers={**self._get_headers(), **self._get_auth()},
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_contact(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Contact {contact_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def delete_contact(self, workspace_id: str, contact_id: str) -> bool:
        """
        Delete a contact.

        Args:
            workspace_id: Workspace ID
            contact_id: Contact ID

        Returns:
            bool: True if deletion was successful

        Raises:
            ValueError: If contact not found
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")
        if not contact_id:
            raise ValueError("contact_id is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/contacts/{contact_id}"

        try:
            async with self.session.delete(
                url,
                headers={**self._get_headers(), **self._get_auth()}
            ) as response:
                response.raise_for_status()
                return True

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Contact {contact_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")

    async def search_contacts(
        self,
        workspace_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        tag_ids: Optional[List[str]] = None,
        page: int = 1,
        per_page: int = 50
    ) -> List[Contact]:
        """
        Search contacts in a workspace.

        Args:
            workspace_id: Workspace ID
            email: Email to search (optional)
            first_name: First name to search (optional)
            last_name: Last name to search (optional)
            tag_ids: Filter by tag IDs (optional)
            page: Page number (default: 1)
            per_page: Results per page (default: 50)

        Returns:
            List[Contact]: List of contacts

        Raises:
            ValueError: If workspace not found
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/contacts"
        params = {"page": page, "per_page": per_page}

        if email:
            params["email"] = email.strip()
        if first_name:
            params["first_name"] = first_name.strip()
        if last_name:
            params["last_name"] = last_name.strip()
        if tag_ids:
            params["tag_ids"] = ",".join(tag_ids)

        try:
            async with self.session.get(
                url,
                headers={**self._get_headers(), **self._get_auth()},
                params=params
            ) as response:
                response.raise_for_status()
                data = await response.json()

                contacts = []
                # Handle both array and wrapped response formats
                items = data if isinstance(data, list) else data.get("data", data.get("contacts", []))
                for item in items:
                    contacts.append(self._parse_contact(item))

                return contacts

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Workspace {workspace_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    # ==================== Tag Management ====================

    async def list_tags(self, workspace_id: str) -> List[Tag]:
        """
        Get all tags in a workspace.

        Args:
            workspace_id: Workspace ID

        Returns:
            List[Tag]: List of tags

        Raises:
            ValueError: If workspace not found
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/tags"

        try:
            async with self.session.get(
                url,
                headers={**self._get_headers(), **self._get_auth()}
            ) as response:
                response.raise_for_status()
                data = await response.json()

                tags = []
                items = data if isinstance(data, list) else data.get("data", data.get("tags", []))
                for item in items:
                    tags.append(self._parse_tag(item))

                return tags

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Workspace {workspace_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def create_tag(
        self,
        workspace_id: str,
        name: str,
        color: Optional[str] = None
    ) -> Tag:
        """
        Create a new tag.

        Args:
            workspace_id: Workspace ID
            name: Tag name
            color: Tag color (hex code) (optional)

        Returns:
            Tag: Created tag data

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")
        if not name:
            raise ValueError("name is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/tags"

        payload = {"name": name}
        if color:
            payload["color"] = color

        try:
            async with self.session.post(
                url,
                headers={**self._get_headers(), **self._get_auth()},
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_tag(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 409:
                raise ValueError("Tag with this name already exists")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def update_tag(
        self,
        workspace_id: str,
        tag_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None
    ) -> Tag:
        """
        Update a tag.

        Args:
            workspace_id: Workspace ID
            tag_id: Tag ID
            name: New name (optional)
            color: New color (optional)

        Returns:
            Tag: Updated tag data

        Raises:
            ValueError: If tag not found
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")
        if not tag_id:
            raise ValueError("tag_id is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/tags/{tag_id}"

        payload = {}
        if name:
            payload["name"] = name
        if color:
            payload["color"] = color

        if not payload:
            raise ValueError("At least one field to update must be provided")

        try:
            async with self.session.patch(
                url,
                headers={**self._get_headers(), **self._get_auth()},
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_tag(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Tag {tag_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def delete_tag(self, workspace_id: str, tag_id: str) -> bool:
        """
        Delete a tag.

        Args:
            workspace_id: Workspace ID
            tag_id: Tag ID

        Returns:
            bool: True if deletion was successful

        Raises:
            ValueError: If tag not found
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")
        if not tag_id:
            raise ValueError("tag_id is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/tags/{tag_id}"

        try:
            async with self.session.delete(
                url,
                headers={**self._get_headers(), **self._get_auth()}
            ) as response:
                response.raise_for_status()
                return True

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Tag {tag_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")

    async def apply_tag_to_contact(
        self,
        workspace_id: str,
        contact_id: str,
        tag_id: str
    ) -> bool:
        """
        Apply a tag to a contact.

        Args:
            workspace_id: Workspace ID
            contact_id: Contact ID
            tag_id: Tag ID

        Returns:
            bool: True if tag was applied

        Raises:
            ValueError: If contact or tag not found
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")
        if not contact_id:
            raise ValueError("contact_id is required")
        if not tag_id:
            raise ValueError("tag_id is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/contacts/{contact_id}/tags"

        payload = {"tag_id": tag_id}

        try:
            async with self.session.post(
                url,
                headers={**self._get_headers(), **self._get_auth()},
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                return True

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError("Contact or tag not found")
            elif e.status == 409:
                raise ValueError("Tag already applied to contact")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")

    async def get_contact_tags(self, workspace_id: str, contact_id: str) -> List[Tag]:
        """
        Get all tags applied to a contact.

        Args:
            workspace_id: Workspace ID
            contact_id: Contact ID

        Returns:
            List[Tag]: List of tags applied to contact

        Raises:
            ValueError: If contact not found
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")
        if not contact_id:
            raise ValueError("contact_id is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/contacts/{contact_id}/tags"

        try:
            async with self.session.get(
                url,
                headers={**self._get_headers(), **self._get_auth()}
            ) as response:
                response.raise_for_status()
                data = await response.json()

                tags = []
                items = data if isinstance(data, list) else data.get("data", [])
                for item in items:
                    tags.append(self._parse_tag(item))

                return tags

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Contact {contact_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def remove_tag_from_contact(
        self,
        workspace_id: str,
        contact_id: str,
        tag_id: str
    ) -> bool:
        """
        Remove a tag from a contact.

        Args:
            workspace_id: Workspace ID
            contact_id: Contact ID
            tag_id: Tag ID

        Returns:
            bool: True if tag was removed

        Raises:
            ValueError: If contact or tag not found
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")
        if not contact_id:
            raise ValueError("contact_id is required")
        if not tag_id:
            raise ValueError("tag_id is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/contacts/{contact_id}/tags/{tag_id}"

        try:
            async with self.session.delete(
                url,
                headers={**self._get_headers(), **self._get_auth()}
            ) as response:
                response.raise_for_status()
                return True

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError("Tag not applied to contact")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")

    # ==================== Enrollment Management ====================

    async def create_enrollment(
        self,
        workspace_id: str,
        contact_id: str,
        course_id: str
    ) -> Enrollment:
        """
        Enroll a contact in a course.

        Args:
            workspace_id: Workspace ID
            contact_id: Contact ID
            course_id: Course ID

        Returns:
            Enrollment: Enrollment data

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If API request fails
        """
        if not all([workspace_id, contact_id, course_id]):
            raise ValueError("workspace_id, contact_id, and course_id are required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/enrollments"

        payload = {
            "contact_id": contact_id,
            "course_id": course_id
        }

        try:
            async with self.session.post(
                url,
                headers={**self._get_headers(), **self._get_auth()},
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_enrollment(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 409:
                raise ValueError("Contact is already enrolled in this course")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def update_enrollment(
        self,
        workspace_id: str,
        enrollment_id: str,
        status: Optional[str] = None
    ) -> Enrollment:
        """
        Update enrollment status.

        Args:
            workspace_id: Workspace ID
            enrollment_id: Enrollment ID
            status: New status (active, completed, suspended) (optional)

        Returns:
            Enrollment: Updated enrollment data

        Raises:
            ValueError: If enrollment not found
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")
        if not enrollment_id:
            raise ValueError("enrollment_id is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/enrollments/{enrollment_id}"

        payload = {}
        if status:
            payload["status"] = status

        if not payload:
            raise ValueError("At least one field to update must be provided")

        try:
            async with self.session.patch(
                url,
                headers={**self._get_headers(), **self._get_auth()},
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_enrollment(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Enrollment {enrollment_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def search_enrollments(
        self,
        workspace_id: str,
        contact_id: Optional[str] = None,
        course_id: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        per_page: int = 50
    ) -> List[Enrollment]:
        """
        Search enrollments.

        Args:
            workspace_id: Workspace ID
            contact_id: Filter by contact ID (optional)
            course_id: Filter by course ID (optional)
            status: Filter by status (optional)
            page: Page number (default: 1)
            per_page: Results per page (default: 50)

        Returns:
            List[Enrollment]: List of enrollments

        Raises:
            ValueError: If workspace not found
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/enrollments"
        params = {"page": page, "per_page": per_page}

        if contact_id:
            params["contact_id"] = contact_id
        if course_id:
            params["course_id"] = course_id
        if status:
            params["status"] = status

        try:
            async with self.session.get(
                url,
                headers={**self._get_headers(), **self._get_auth()},
                params=params
            ) as response:
                response.raise_for_status()
                data = await response.json()

                enrollments = []
                items = data if isinstance(data, list) else data.get("data", data.get("enrollments", []))
                for item in items:
                    enrollments.append(self._parse_enrollment(item))

                return enrollments

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Workspace {workspace_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def list_courses(self, workspace_id: str) -> List[Course]:
        """
        Get all courses in a workspace.

        Args:
            workspace_id: Workspace ID

        Returns:
            List[Course]: List of courses

        Raises:
            ValueError: If workspace not found
            aiohttp.ClientError: If API request fails
        """
        if not workspace_id:
            raise ValueError("workspace_id is required")

        url = f"{self.BASE_URL}/workspaces/{workspace_id}/courses"

        try:
            async with self.session.get(
                url,
                headers={**self._get_headers(), **self._get_auth()}
            ) as response:
                response.raise_for_status()
                data = await response.json()

                courses = []
                items = data if isinstance(data, list) else data.get("data", data.get("courses", []))
                for item in items:
                    courses.append(self._parse_course(item))

                return courses

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Workspace {workspace_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    # ==================== Helper Methods ====================

    def _parse_contact(self, data: Dict[str, Any]) -> Contact:
        """Parse contact data"""
        created_at = self._parse_datetime(data.get("created_at"))
        updated_at = self._parse_datetime(data.get("updated_at"))

        tags = data.get("tags", [])
        tag_ids = []
        if isinstance(tags, list):
            tag_ids = [t.get("id") if isinstance(t, dict) else t for t in tags]

        return Contact(
            id=str(data.get("id", "")),
            email=data.get("email", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            phone=data.get("phone"),
            workspace_id=str(data.get("workspace_id", "")),
            created_at=created_at,
            updated_at=updated_at,
            tags=tag_ids,
            raw_response=data
        )

    def _parse_tag(self, data: Dict[str, Any]) -> Tag:
        """Parse tag data"""
        return Tag(
            id=str(data.get("id", "")),
            name=data.get("name", ""),
            color=data.get("color"),
            workspace_id=str(data.get("workspace_id", "")),
            raw_response=data
        )

    def _parse_enrollment(self, data: Dict[str, Any]) -> Enrollment:
        """Parse enrollment data"""
        started_at = self._parse_datetime(data.get("started_at"))
        completed_at = self._parse_datetime(data.get("completed_at"))

        return Enrollment(
            id=str(data.get("id", "")),
            contact_id=str(data.get("contact_id", "")),
            course_id=str(data.get("course_id", "")),
            workspace_id=str(data.get("workspace_id", "")),
            status=data.get("status", ""),
            started_at=started_at,
            completed_at=completed_at,
            raw_response=data
        )

    def _parse_course(self, data: Dict[str, Any]) -> Course:
        """Parse course data"""
        return Course(
            id=str(data.get("id", "")),
            name=data.get("name", ""),
            description=data.get("description"),
            workspace_id=str(data.get("workspace_id", "")),
            raw_response=data
        )

    def _parse_datetime(self, dt_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string"""
        if not dt_str:
            return None
        try:
            return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return None


# Webhook handler
def parse_webhook_event(payload: Dict[str, Any]) -> WebhookEvent:
    """
    Parse webhook event from ClickFunnels.

    Args:
        payload: Webhook payload JSON

    Returns:
        WebhookEvent: Parsed event data
    """
    event_type = payload.get("type") or payload.get("event_type", "")
    contact_id = payload.get("contact_id") or payload.get("contact", {}).get("id")
    order_id = payload.get("order_id") or payload.get("order", {}).get("id")

    timestamp = datetime.now()
    if "timestamp" in payload:
        try:
            timestamp = datetime.fromisoformat(payload["timestamp"].replace('Z', '+00:00'))
        except (ValueError, TypeError):
            pass

    return WebhookEvent(
        event_type=event_type,
        contact_id=str(contact_id) if contact_id else None,
        order_id=str(order_id) if order_id else None,
        timestamp=timestamp,
        payload=payload
    )