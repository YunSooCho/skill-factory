"""
CleverReach Email Marketing API Client

Supports:
- Add Receiver
- Get Receiver Information
- Update Receiver
- Delete Receivers
- Search Receivers
- Add Event to Receiver
- Register Email to Group Blacklist
- Trigger: New Receiver
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class Receiver:
    """Receiver/subscriber data"""
    id: int
    email: str
    source: Optional[str] = None
    activated: Optional[bool] = None
    registered: Optional[datetime] = None
    deactivated: Optional[bool] = None
    attributes: Optional[Dict[str, Any]] = None
    global_attributes: Optional[Dict[str, Any]] = None
    events: Optional[List[str]] = None
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class Group:
    """Group/list data"""
    id: int
    name: str
    last_mailing: Optional[str] = None
    receiver_count: int = 0
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class WebhookEvent:
    """Webhook event data"""
    event_type: str
    receiver_id: int
    group_id: int
    timestamp: datetime
    payload: Dict[str, Any]


class CleverReachClient:
    """
    CleverReach Email Marketing API client.

    API Documentation: https://rest.cleverreach.com/doc/
    This service provides email list management, subscriber management, and event tracking.
    """

    BASE_URL = "https://rest.cleverreach.com/v3"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize CleverReach client.

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
            "User-Agent": "CleverReachClient/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _get_auth(self) -> aiohttp.BasicAuth:
        """Get basic authentication"""
        # CleverReach uses the API key as username, no password needed
        return aiohttp.BasicAuth(self.api_key, "")

    # ==================== Receiver Management ====================

    async def add_receiver(
        self,
        group_id: int,
        email: str,
        source: Optional[str] = None,
        activated: bool = True,
        attributes: Optional[Dict[str, Any]] = None,
        global_attributes: Optional[Dict[str, Any]] = None
    ) -> Receiver:
        """
        Add a new receiver/subscriber to a group.

        Args:
            group_id: The ID of the group/list
            email: Receiver email address
            source: Source of the subscriber (optional)
            activated: Whether to activate immediately (default: True)
            attributes: Receiver-specific attributes
            global_attributes: Global attributes for the receiver

        Returns:
            Receiver: Created receiver data

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If API request fails
        """
        if not group_id:
            raise ValueError("group_id is required")
        if not email or not email.strip():
            raise ValueError("email is required")

        url = f"{self.BASE_URL}/groups/{group_id}/receivers"

        payload = {
            "email": email.strip(),
            "activated": activated
        }

        if source:
            payload["source"] = source
        if attributes:
            payload["attributes"] = attributes
        if global_attributes:
            payload["global_attributes"] = global_attributes

        try:
            async with self.session.post(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_receiver(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 400:
                raise ValueError(f"Invalid request parameters: {e.message}")
            elif e.status == 401:
                raise ValueError("Invalid or missing API key")
            elif e.status == 404:
                raise ValueError(f"Group {group_id} not found")
            elif e.status == 409:
                raise ValueError("Email already exists in group")
            elif e.status == 429:
                raise ValueError(f"Rate limit exceeded. Please try again later.")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from API")

    async def get_receiver(self, receiver_id: int, group_id: int) -> Receiver:
        """
        Get receiver information.

        Args:
            receiver_id: The ID of the receiver
            group_id: The ID of the group

        Returns:
            Receiver: Receiver data

        Raises:
            ValueError: If receiver or group not found
            aiohttp.ClientError: If API request fails
        """
        if not receiver_id:
            raise ValueError("receiver_id is required")
        if not group_id:
            raise ValueError("group_id is required")

        url = f"{self.BASE_URL}/groups/{group_id}/receivers/{receiver_id}"

        try:
            async with self.session.get(
                url,
                auth=self._get_auth(),
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_receiver(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Receiver {receiver_id} not found in group {group_id}")
            elif e.status == 401:
                raise ValueError("Invalid or missing API key")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def update_receiver(
        self,
        receiver_id: int,
        group_id: int,
        email: Optional[str] = None,
        activated: Optional[bool] = None,
        attributes: Optional[Dict[str, Any]] = None,
        global_attributes: Optional[Dict[str, Any]] = None
    ) -> Receiver:
        """
        Update receiver information.

        Args:
            receiver_id: The ID of the receiver
            group_id: The ID of the group
            email: New email address (optional)
            activated: Activation status (optional)
            attributes: Updated attributes (optional)
            global_attributes: Updated global attributes (optional)

        Returns:
            Receiver: Updated receiver data
        """
        if not receiver_id:
            raise ValueError("receiver_id is required")
        if not group_id:
            raise ValueError("group_id is required")

        url = f"{self.BASE_URL}/groups/{group_id}/receivers/{receiver_id}"

        payload = {}
        if email:
            payload["email"] = email.strip()
        if activated is not None:
            payload["activated"] = activated
        if attributes is not None:
            payload["attributes"] = attributes
        if global_attributes is not None:
            payload["global_attributes"] = global_attributes

        if not payload:
            raise ValueError("At least one field to update must be provided")

        try:
            async with self.session.put(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_receiver(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Receiver {receiver_id} not found")
            elif e.status == 409:
                raise ValueError("Email already exists in group")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def delete_receiver(self, receiver_id: int, group_id: int) -> bool:
        """
        Delete a receiver from a group.

        Args:
            receiver_id: The ID of the receiver
            group_id: The ID of the group

        Returns:
            bool: True if deletion was successful

        Raises:
            ValueError: If receiver or group not found
            aiohttp.ClientError: If API request fails
        """
        if not receiver_id:
            raise ValueError("receiver_id is required")
        if not group_id:
            raise ValueError("group_id is required")

        url = f"{self.BASE_URL}/groups/{group_id}/receivers/{receiver_id}"

        try:
            async with self.session.delete(
                url,
                auth=self._get_auth(),
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                return True

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Receiver {receiver_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")

    async def delete_receivers(
        self,
        group_id: int,
        receiver_ids: Optional[List[int]] = None,
        emails: Optional[List[str]] = None
    ) -> int:
        """
        Delete multiple receivers from a group.

        Args:
            group_id: The ID of the group
            receiver_ids: List of receiver IDs to delete
            emails: List of emails to delete

        Returns:
            int: Number of receivers deleted

        Raises:
            ValueError: If neither receiver_ids nor emails provided
            aiohttp.ClientError: If API request fails
        """
        if not receiver_ids and not emails:
            raise ValueError("Either receiver_ids or emails must be provided")

        url = f"{self.BASE_URL}/groups/{group_id}/receivers/deletebatch"

        payload = {}
        if receiver_ids:
            payload["ids"] = receiver_ids
        if emails:
            payload["emails"] = emails

        try:
            async with self.session.post(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return len(data.get("deleted", []))

        except aiohttp.ClientResponseError as e:
            raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def search_receivers(
        self,
        group_id: int,
        email: Optional[str] = None,
        page: int = 0,
       pagesize: int = 50,
        order: str = "asc",
        orderby: str = "id"
    ) -> List[Receiver]:
        """
        Search receivers in a group.

        Args:
            group_id: The ID of the group
            email: Email to search for (partial match) (optional)
            page: Page number (default: 0)
            pagesize: Number of results per page (default: 50)
            order: Sort order (asc/desc) (default: asc)
            orderby: Sort field (id, email, etc.) (default: id)

        Returns:
            List[Receiver]: List of receivers

        Raises:
            ValueError: If group not found
            aiohttp.ClientError: If API request fails
        """
        if not group_id:
            raise ValueError("group_id is required")

        url = f"{self.BASE_URL}/groups/{group_id}/receivers"
        params = {
            "page": page,
            "pagesize": pagesize,
            "order": order,
            "orderby": orderby
        }

        if email:
            params["email"] = email.strip()

        try:
            async with self.session.get(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                params=params
            ) as response:
                response.raise_for_status()
                data = await response.json()

                receivers = []
                for item in data:
                    receivers.append(self._parse_receiver(item))

                return receivers

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Group {group_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    # ==================== Event Management ====================

    async def add_event_to_receiver(
        self,
        receiver_id: int,
        group_id: int,
        event_type: str,
        event_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Add an event to a receiver.

        Args:
            receiver_id: The ID of the receiver
            group_id: The ID of the group
            event_type: Type of event (e.g., "purchase", "click", "open")
            event_data: Additional event data (optional)

        Returns:
            bool: True if event was added successfully

        Raises:
            ValueError: If receiver or group not found
            aiohttp.ClientError: If API request fails
        """
        if not receiver_id:
            raise ValueError("receiver_id is required")
        if not group_id:
            raise ValueError("group_id is required")
        if not event_type:
            raise ValueError("event_type is required")

        url = f"{self.BASE_URL}/groups/{group_id}/receivers/{receiver_id}/events"

        payload = {
            "type": event_type
        }

        if event_data:
            payload["data"] = event_data

        try:
            async with self.session.post(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                return True

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Receiver {receiver_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")

    # ==================== Blacklist Management ====================

    async def register_email_to_blacklist(
        self,
        email: str,
        group_id: Optional[int] = None,
        reason: Optional[str] = None
    ) -> bool:
        """
        Register an email to the blacklist.

        Args:
            email: Email address to blacklist
            group_id: Optional group ID for blacklist. If None, global blacklist.
            reason: Reason for blacklisting (optional)

        Returns:
            bool: True if email was added to blacklist

        Raises:
            ValueError: If email is required
            aiohttp.ClientError: If API request fails
        """
        if not email or not email.strip():
            raise ValueError("email is required")

        if group_id:
            url = f"{self.BASE_URL}/groups/{group_id}/receivers/blacklist"
        else:
            url = f"{self.BASE_URL}/receivers/blacklist"

        payload = {
            "email": email.strip()
        }

        if reason:
            payload["reason"] = reason
        if group_id:
            payload["group_id"] = group_id

        try:
            async with self.session.post(
                url,
                auth=self._get_auth(),
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                return True

        except aiohttp.ClientResponseError as e:
            if e.status == 409:
                raise ValueError("Email is already blacklisted")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")

    # ==================== Helper Methods ====================

    def _parse_receiver(self, data: Dict[str, Any]) -> Receiver:
        """Parse receiver data"""
        registered = None
        if data.get("registered"):
            try:
                registered = datetime.fromisoformat(data.get("registration_time", ""))
            except (ValueError, TypeError):
                pass

        return Receiver(
            id=data.get("id"),
            email=data.get("email", ""),
            source=data.get("source"),
            activated=data.get("activated"),
            registered=registered,
            deactivated=data.get("deactivated"),
            attributes=data.get("attributes"),
            global_attributes=data.get("global_attributes"),
            events=data.get("events", []),
            raw_response=data
        )

    def get_receiver_information(self, receiver_id: int, group_id: int) -> Receiver:
        """Alias for get_receiver"""
        return self.get_receiver(receiver_id, group_id)


# Webhook handler for trigger
def parse_webhook_event(payload: Dict[str, Any]) -> WebhookEvent:
    """
    Parse webhook event from CleverReach.

    Args:
        payload: Webhook payload JSON

    Returns:
        WebhookEvent: Parsed event data
    """
    event_type = payload.get("type", "")
    receiver_id = payload.get("receiver_id", 0)
    group_id = payload.get("group_id", 0)

    timestamp = datetime.now()
    if "timestamp" in payload:
        try:
            timestamp = datetime.fromisoformat(payload["timestamp"])
        except (ValueError, TypeError):
            pass

    return WebhookEvent(
        event_type=event_type,
        receiver_id=receiver_id,
        group_id=group_id,
        timestamp=timestamp,
        payload=payload
    )