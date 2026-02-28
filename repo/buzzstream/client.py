"""
Buzzstream API Client

Supports:
- Get Contacts
- Create Contact
- Update Contact
- Delete Contact
- Get Projects
- Create Project
- Track Outreach
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Contact:
    """Contact information"""
    id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    website: Optional[str] = None
    social_profiles: Dict[str, str] = None
    tags: List[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        if self.social_profiles is None:
            self.social_profiles = {}
        if self.tags is None:
            self.tags = []


@dataclass
class Project:
    """Project information"""
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    contact_count: int = 0
    created_at: Optional[str] = None


@dataclass
class Outreach:
    """Outreach activity"""
    id: Optional[str] = None
    contact_id: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    channel: Optional[str] = None
    sent_at: Optional[str] = None
    replied_at: Optional[str] = None
    response: Optional[str] = None


@dataclass
class OutreachNote:
    """Outreach note"""
    contact_id: Optional[str] = None
    note: Optional[str] = None
    created_at: Optional[str] = None


class BuzzstreamClient:
    """
    Buzzstream API client for PR outreach and contact management.

    Authentication: API Key (Header: X-API-Key)
    Base URL: https://api.buzzstream.com/v1
    """

    BASE_URL = "https://api.buzzstream.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Buzzstream client.

        Args:
            api_key: Buzzstream API key
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

    # ==================== Contacts ====================

    def get_contacts(
        self,
        project_id: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get contacts with filtering.

        Args:
            project_id: Filter by project ID
            status: Filter by status
            tags: Filter by tags
            search: Search query
            limit: Number of results
            offset: Pagination offset

        Returns:
            Contact list and pagination info
        """
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset
        }

        if project_id:
            params["project_id"] = project_id
        if status:
            params["status"] = status
        if tags:
            params["tags"] = ",".join(tags)
        if search:
            params["search"] = search

        result = self._request("GET", "/contacts", params=params)

        contacts = [self._parse_contact(c) for c in result.get("contacts", [])]
        total = result.get("total", 0)

        return {
            "contacts": contacts,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    def get_contact(self, contact_id: str) -> Contact:
        """
        Get a specific contact.

        Args:
            contact_id: Contact ID

        Returns:
            Contact object
        """
        if not contact_id:
            raise ValueError("Contact ID is required")

        result = self._request("GET", f"/contacts/{contact_id}")
        return self._parse_contact(result)

    def create_contact(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        website: Optional[str] = None,
        social_profiles: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        notes: Optional[str] = None,
        project_id: Optional[str] = None
    ) -> Contact:
        """
        Create a new contact.

        Args:
            first_name: First name
            last_name: Last name
            email: Email address
            phone: Phone number
            company: Company name
            website: Website URL
            social_profiles: Dictionary of social profiles (twitter, linkedin, etc.)
            tags: List of tags
            notes: Contact notes
            project_id: Project ID to associate contact with

        Returns:
            Created Contact object
        """
        payload: Dict[str, Any] = {}

        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if email:
            payload["email"] = email
        if phone:
            payload["phone"] = phone
        if company:
            payload["company"] = company
        if website:
            payload["website"] = website
        if social_profiles:
            payload["social_profiles"] = social_profiles
        if tags:
            payload["tags"] = tags
        if notes:
            payload["notes"] = notes
        if project_id:
            payload["project_id"] = project_id

        result = self._request("POST", "/contacts", json=payload)
        return self._parse_contact(result)

    def update_contact(
        self,
        contact_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        website: Optional[str] = None,
        social_profiles: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        notes: Optional[str] = None,
        status: Optional[str] = None
    ) -> Contact:
        """
        Update an existing contact.

        Args:
            contact_id: Contact ID
            first_name: Updated first name
            last_name: Updated last name
            email: Updated email
            phone: Updated phone
            company: Updated company
            website: Updated website
            social_profiles: Updated social profiles
            tags: Updated tags
            notes: Updated notes
            status: Updated status

        Returns:
            Updated Contact object
        """
        if not contact_id:
            raise ValueError("Contact ID is required")

        payload: Dict[str, Any] = {}

        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if email:
            payload["email"] = email
        if phone:
            payload["phone"] = phone
        if company:
            payload["company"] = company
        if website:
            payload["website"] = website
        if social_profiles:
            payload["social_profiles"] = social_profiles
        if tags:
            payload["tags"] = tags
        if notes:
            payload["notes"] = notes
        if status:
            payload["status"] = status

        result = self._request("PATCH", f"/contacts/{contact_id}", json=payload)
        return self._parse_contact(result)

    def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Delete a contact.

        Args:
            contact_id: Contact ID

        Returns:
            Deletion response
        """
        if not contact_id:
            raise ValueError("Contact ID is required")

        return self._request("DELETE", f"/contacts/{contact_id}")

    def add_contact_note(self, contact_id: str, note: str) -> OutreachNote:
        """
        Add a note to a contact.

        Args:
            contact_id: Contact ID
            note: Note content

        Returns:
            Note object
        """
        if not contact_id:
            raise ValueError("Contact ID is required")
        if not note:
            raise ValueError("Note content is required")

        payload = {"note": note}
        result = self._request("POST", f"/contacts/{contact_id}/notes", json=payload)
        return self._parse_note(result)

    # ==================== Projects ====================

    def get_projects(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get projects.

        Args:
            status: Filter by status
            limit: Number of results
            offset: Pagination offset

        Returns:
            Project list and pagination info
        """
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset
        }

        if status:
            params["status"] = status

        result = self._request("GET", "/projects", params=params)

        projects = [self._parse_project(p) for p in result.get("projects", [])]
        total = result.get("total", 0)

        return {
            "projects": projects,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        type: Optional[str] = None,
        start_date: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> Project:
        """
        Create a new project.

        Args:
            name: Project name
            description: Project description
            type: Project type (outreach, pr, link_building, etc.)
            start_date: Start date (ISO format)
            due_date: Due date (ISO format)

        Returns:
            Created Project object
        """
        if not name:
            raise ValueError("Project name is required")

        payload: Dict[str, Any] = {"name": name}

        if description:
            payload["description"] = description
        if type:
            payload["type"] = type
        if start_date:
            payload["start_date"] = start_date
        if due_date:
            payload["due_date"] = due_date

        result = self._request("POST", "/projects", json=payload)
        return self._parse_project(result)

    # ==================== Outreach ====================

    def create_outreach(
        self,
        contact_id: str,
        type: str,
        subject: Optional[str] = None,
        content: Optional[str] = None,
        channel: str = "email",
        project_id: Optional[str] = None
    ) -> Outreach:
        """
        Create a new outreach activity.

        Args:
            contact_id: Contact ID
            type: Outreach type (email, call, social, etc.)
            subject: Outreach subject
            content: Outreach content/message
            channel: Channel (email, twitter, linkedin, etc.)
            project_id: Project ID

        Returns:
            Created Outreach object
        """
        if not contact_id:
            raise ValueError("Contact ID is required")
        if not type:
            raise ValueError("Outreach type is required")

        payload: Dict[str, Any] = {
            "contact_id": contact_id,
            "type": type,
            "channel": channel
        }

        if subject:
            payload["subject"] = subject
        if content:
            payload["content"] = content
        if project_id:
            payload["project_id"] = project_id

        result = self._request("POST", "/outreach", json=payload)
        return self._parse_outreach(result)

    def track_outreach(
        self,
        contact_id: str,
        outreach_id: Optional[str] = None,
        status: Optional[str] = None,
        response: Optional[str] = None
    ) -> Outreach:
        """
        Track and update outreach activity.

        Args:
            contact_id: Contact ID
            outreach_id: Outreach ID
            status: Outreach status (sent, delivered, opened, replied, etc.)
            response: Response received

        Returns:
            Updated Outreach object
        """
        if not contact_id:
            raise ValueError("Contact ID is required")

        payload: Dict[str, Any] = {"contact_id": contact_id}

        if outreach_id:
            payload["outreach_id"] = outreach_id
        if status:
            payload["status"] = status
        if response:
            payload["response"] = response

        endpoint = f"/outreach/{outreach_id}" if outreach_id else "/outreach"
        result = self._request("PATCH", endpoint, json=payload)
        return self._parse_outreach(result)

    def get_outreach_history(self, contact_id: str, limit: int = 20) -> List[Outreach]:
        """
        Get outreach history for a contact.

        Args:
            contact_id: Contact ID
            limit: Number of results

        Returns:
            List of Outreach objects
        """
        if not contact_id:
            raise ValueError("Contact ID is required")

        result = self._request("GET", f"/contacts/{contact_id}/outreach", params={"limit": limit})
        return [self._parse_outreach(o) for o in result.get("outreach", [])]

    # ==================== Helper Methods ====================

    def _parse_contact(self, data: Dict[str, Any]) -> Contact:
        """Parse contact data from API response"""
        return Contact(
            id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            company=data.get("company"),
            website=data.get("website"),
            social_profiles=data.get("social_profiles", {}),
            tags=data.get("tags", []),
            status=data.get("status"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def _parse_project(self, data: Dict[str, Any]) -> Project:
        """Parse project data from API response"""
        return Project(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            type=data.get("type"),
            status=data.get("status"),
            start_date=data.get("start_date"),
            due_date=data.get("due_date"),
            contact_count=data.get("contact_count", 0),
            created_at=data.get("created_at")
        )

    def _parse_outreach(self, data: Dict[str, Any]) -> Outreach:
        """Parse outreach data from API response"""
        return Outreach(
            id=data.get("id"),
            contact_id=data.get("contact_id"),
            type=data.get("type"),
            status=data.get("status"),
            subject=data.get("subject"),
            content=data.get("content"),
            channel=data.get("channel"),
            sent_at=data.get("sent_at"),
            replied_at=data.get("replied_at"),
            response=data.get("response")
        )

    def _parse_note(self, data: Dict[str, Any]) -> OutreachNote:
        """Parse note data from API response"""
        return OutreachNote(
            contact_id=data.get("contact_id"),
            note=data.get("note"),
            created_at=data.get("created_at")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_buzzstream_api_key"

    client = BuzzstreamClient(api_key=api_key)

    try:
        # Create a project
        project = client.create_project(
            name="Q1 PR Campaign 2024",
            description="Outreach for Q1 product launch",
            type="outreach",
            start_date="2024-01-01T00:00:00Z",
            due_date="2024-03-31T23:59:59Z"
        )
        print(f"Project created: {project.id}")
        print(f"Name: {project.name}")

        # Create a contact
        contact = client.create_contact(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            company="Tech Blog",
            website="https://techblog.com",
            social_profiles={
                "twitter": "@jane_tech",
                "linkedin": "linkedin.com/in/jane"
            },
            tags=["tech", "reviewer"],
            notes="Interested in reviewing new tech products",
            project_id=project.id
        )
        print(f"\nContact created: {contact.id}")
        print(f"Name: {contact.first_name} {contact.last_name}")
        print(f"Company: {contact.company}")

        # Get contacts
        contacts_response = client.get_contacts(
            project_id=project.id,
            limit=10
        )
        print(f"\nContacts in project: {contacts_response['total']}")

        # Create outreach
        outreach = client.create_outreach(
            contact_id=contact.id,
            type="email",
            subject="Product Review Opportunity",
            content="Hi Jane,\n\nWe'd love for you to review our new product...",
            channel="email",
            project_id=project.id
        )
        print(f"\nOutreach created: {outreach.id}")
        print(f"Status: {outreach.status}")

        # Track outreach response
        updated_outreach = client.track_outreach(
            contact_id=contact.id,
            outreach_id=outreach.id,
            status="replied",
            response="Thanks for reaching out! I'm interested."
        )
        print(f"Outreach updated: {updated_outreach.status}")
        print(f"Response: {updated_outreach.response}")

        # Get outreach history
        history = client.get_outreach_history(contact_id=contact.id)
        print(f"\nOutreach history: {len(history)} activities")

        # Add contact note
        note = client.add_contact_note(
            contact_id=contact.id,
            note="Follow up next week about the review article."
        )
        print(f"Note added: {note.created_at}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()