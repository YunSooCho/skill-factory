"""
CloudContact AI Contact Management API Client

Supports:
- Create Contact
- Search Contacts
- Get Sent SMS Messages
- Sent SMS Messages by Campaign
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
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    company: Optional[str]
    tags: Optional[List[str]]
    custom_fields: Optional[Dict[str, Any]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class SMSMessage:
    """SMS message data"""
    id: int
    phone: str
    message: str
    status: str
    sent_at: Optional[datetime]
    campaign_id: Optional[int]
    campaign_name: Optional[str]
    delivery_status: Optional[str]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class Campaign:
    """Campaign data"""
    id: int
    name: str
    status: str
    created_at: Optional[datetime]
    message_count: int
    raw_response: Optional[Dict[str, Any]] = None


class CloudContactAIClient:
    """
    CloudContact AI Contact Management API client.

    API Documentation: Check CloudContact AI documentation
    This service provides contact management and SMS messaging.
    """

    BASE_URL = "https://api.cloudcontact.ai/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize CloudContact AI client.

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
            "User-Agent": "CloudContactAIClient/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }

    # ==================== Contact Management ====================

    async def create_contact(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Contact:
        """
        Create a new contact.

        Args:
            first_name: Contact's first name (optional)
            last_name: Contact's last name (optional)
            email: Contact's email address (optional)
            phone: Contact's phone number (optional)
            company: Contact's company (optional)
            tags: List of tags for the contact (optional)
            custom_fields: Additional custom fields (optional)

        Returns:
            Contact: Created contact data

        Raises:
            ValueError: If no contact data provided
            aiohttp.ClientError: If API request fails

        Note:
            At least one of first_name, last_name, email, or phone should be provided.
        """
        # Check if any significant data is provided
        if not any([first_name, last_name, email, phone]):
            raise ValueError("At least one of first_name, last_name, email, or phone is required")

        url = f"{self.BASE_URL}/contacts"

        payload = {}
        if first_name:
            payload["first_name"] = first_name.strip()
        if last_name:
            payload["last_name"] = last_name.strip()
        if email:
            payload["email"] = email.strip().lower()
        if phone:
            payload["phone"] = phone.strip()
        if company:
            payload["company"] = company.strip()
        if tags:
            payload["tags"] = tags
        if custom_fields:
            payload["custom_fields"] = custom_fields

        try:
            async with self.session.post(
                url,
                headers=self._get_headers(),
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
            elif e.status == 409:
                raise ValueError("Contact with this email or phone already exists")
            elif e.status == 429:
                raise ValueError(f"Rate limit exceeded. Please try again later.")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from API")

    async def search_contacts(
        self,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company: Optional[str] = None,
        tags: Optional[List[str]] = None,
        page: int = 1,
        per_page: int = 50
    ) -> List[Contact]:
        """
        Search contacts with optional filters.

        Args:
            email: Filter by email (exact match) (optional)
            phone: Filter by phone (exact match) (optional)
            first_name: Filter by first name (partial match) (optional)
            last_name: Filter by last name (partial match) (optional)
            company: Filter by company (partial match) (optional)
            tags: Filter by tags (contact must have all tags) (optional)
            page: Page number (default: 1)
            per_page: Results per page (default: 50)

        Returns:
            List[Contact]: List of matching contacts

        Raises:
            aiohttp.ClientError: If API request fails
        """
        url = f"{self.BASE_URL}/contacts"
        params = {"page": page, "per_page": per_page}

        if email:
            params["email"] = email.strip().lower()
        if phone:
            params["phone"] = phone.strip()
        if first_name:
            params["first_name"] = first_name.strip()
        if last_name:
            params["last_name"] = last_name.strip()
        if company:
            params["company"] = company.strip()
        if tags:
            params["tags"] = ",".join(tags)

        try:
            async with self.session.get(
                url,
                headers=self._get_headers(),
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
            if e.status == 401:
                raise ValueError("Invalid or missing API key")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    # ==================== SMS Messaging ====================

    async def get_sent_sms_messages(
        self,
        phone: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        per_page: int = 50
    ) -> List[SMSMessage]:
        """
        Get sent SMS messages with optional filters.

        Args:
            phone: Filter by recipient phone number (optional)
            status: Filter by status (sent, delivered, failed) (optional)
            start_date: Filter messages sent after this date (optional)
            end_date: Filter messages sent before this date (optional)
            page: Page number (default: 1)
            per_page: Results per page (default: 50)

        Returns:
            List[SMSMessage]: List of SMS messages

        Raises:
            aiohttp.ClientError: If API request fails
        """
        url = f"{self.BASE_URL}/sms/sent"
        params = {"page": page, "per_page": per_page}

        if phone:
            params["phone"] = phone.strip()
        if status:
            params["status"] = status.lower()
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()

        try:
            async with self.session.get(
                url,
                headers=self._get_headers(),
                params=params
            ) as response:
                response.raise_for_status()
                data = await response.json()

                messages = []
                items = data if isinstance(data, list) else data.get("data", data.get("messages", []))
                for item in items:
                    messages.append(self._parse_sms_message(item))

                return messages

        except aiohttp.ClientResponseError as e:
            if e.status == 401:
                raise ValueError("Invalid or missing API key")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def get_sent_sms_by_campaign(
        self,
        campaign_id: int,
        page: int = 1,
        per_page: int = 50
    ) -> List[SMSMessage]:
        """
        Get sent SMS messages for a specific campaign.

        Args:
            campaign_id: Campaign ID
            page: Page number (default: 1)
            per_page: Results per page (default: 50)

        Returns:
            List[SMSMessage]: List of SMS messages from the campaign

        Raises:
            ValueError: If campaign not found
            aiohttp.ClientError: If API request fails
        """
        if not campaign_id:
            raise ValueError("campaign_id is required")

        url = f"{self.BASE_URL}/sms/campaigns/{campaign_id}/messages"
        params = {"page": page, "per_page": per_page}

        try:
            async with self.session.get(
                url,
                headers=self._get_headers(),
                params=params
            ) as response:
                response.raise_for_status()
                data = await response.json()

                messages = []
                items = data if isinstance(data, list) else data.get("data", data.get("messages", []))
                for item in items:
                    messages.append(self._parse_sms_message(item))

                return messages

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Campaign {campaign_id} not found")
            elif e.status == 401:
                raise ValueError("Invalid or missing API key")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    # ==================== Additional Helper Methods ====================

    async def get_campaigns(
        self,
        status: Optional[str] = None,
        page: int = 1,
        per_page: int = 50
    ) -> List[Campaign]:
        """
        Get SMS campaigns with optional filtering.

        Args:
            status: Filter by status (active, completed, cancelled) (optional)
            page: Page number (default: 1)
            per_page: Results per page (default: 50)

        Returns:
            List[Campaign]: List of campaigns

        Raises:
            aiohttp.ClientError: If API request fails
        """
        url = f"{self.BASE_URL}/sms/campaigns"
        params = {"page": page, "per_page": per_page}

        if status:
            params["status"] = status.lower()

        try:
            async with self.session.get(
                url,
                headers=self._get_headers(),
                params=params
            ) as response:
                response.raise_for_status()
                data = await response.json()

                campaigns = []
                items = data if isinstance(data, list) else data.get("data", data.get("campaigns", []))
                for item in items:
                    campaigns.append(self._parse_campaign(item))

                return campaigns

        except aiohttp.ClientResponseError as e:
            if e.status == 401:
                raise ValueError("Invalid or missing API key")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    # ==================== Helper Methods ====================

    def _parse_contact(self, data: Dict[str, Any]) -> Contact:
        """Parse contact data"""
        created_at = None
        updated_at = None

        if data.get("created_at"):
            try:
                created_at = datetime.fromisoformat(data["created_at"].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass

        if data.get("updated_at"):
            try:
                updated_at = datetime.fromisoformat(data["updated_at"].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass

        return Contact(
            id=int(data.get("id", data.get("contact_id", 0))),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            company=data.get("company"),
            tags=data.get("tags", []),
            custom_fields=data.get("custom_fields"),
            created_at=created_at,
            updated_at=updated_at,
            raw_response=data
        )

    def _parse_sms_message(self, data: Dict[str, Any]) -> SMSMessage:
        """Parse SMS message data"""
        sent_at = None
        if data.get("sent_at") or data.get("created_at"):
            dt_str = data.get("sent_at") or data.get("created_at")
            try:
                sent_at = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass

        return SMSMessage(
            id=int(data.get("id", data.get("message_id", 0))),
            phone=data.get("phone", data.get("recipient", "")),
            message=data.get("message", data.get("body", "")),
            status=data.get("status", "unknown"),
            sent_at=sent_at,
            campaign_id=data.get("campaign_id", data.get("campaign", {}).get("id")),
            campaign_name=data.get("campaign_name", data.get("campaign", {}).get("name")),
            delivery_status=data.get("delivery_status", data.get("delivery_state")),
            raw_response=data
        )

    def _parse_campaign(self, data: Dict[str, Any]) -> Campaign:
        """Parse campaign data"""
        created_at = None
        if data.get("created_at"):
            try:
                created_at = datetime.fromisoformat(data["created_at"].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass

        return Campaign(
            id=int(data.get("id", data.get("campaign_id", 0))),
            name=data.get("name", ""),
            status=data.get("status", "unknown"),
            created_at=created_at,
            message_count=int(data.get("message_count", data.get("count", 0))),
            raw_response=data
        )


# Convenience functions
async def create_contact_simple(
    api_key: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    **kwargs
) -> Contact:
    """
    Convenience function to create a contact.

    Args:
        api_key: API key
        email: Contact email
        phone: Contact phone
        **kwargs: Additional contact fields

    Returns:
        Contact: Created contact
    """
    async with CloudContactAIClient(api_key=api_key) as client:
        return await client.create_contact(email=email, phone=phone, **kwargs)

async def search_contacts_simple(
    api_key: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    **kwargs
) -> List[Contact]:
    """
    Convenience function to search contacts.

    Args:
        api_key: API key
        email: Filter by email
        phone: Filter by phone
        **kwargs: Additional search filters

    Returns:
        List[Contact]: List of matching contacts
    """
    async with CloudContactAIClient(api_key=api_key) as client:
        return await client.search_contacts(email=email, phone=phone, **kwargs)