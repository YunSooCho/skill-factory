"""
Garoon API - Cybozu Garoon Integration Client

Supports:
- Workflow: Get pending approval requests
- Workflow: Get request lists
- Workflow: Get attached files
- User: Search user information
- Schedule: Search facility availability
- Schedule: Search user availability
- Schedule: Create event
- Schedule: Update event
- Schedule: Delete event
- Schedule: Get multiple user events
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
class User:
    """User information object"""
    id: str
    name: str
    code: str
    email: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None


@dataclass
class Event:
    """Schedule event object"""
    id: str
    subject: str
    start: str
    end: str
    attendees: List[str]
    description: Optional[str] = None
    location: Optional[str] = None
    facility_id: Optional[str] = None
    event_type: str = "normal"


@dataclass
class AvailabilitySlot:
    """Availability slot object"""
    start: str
    end: str
    available: bool


@dataclass
class WorkflowRequest:
    """Workflow request object"""
    id: str
    title: str
    applicant_id: str
    status: str
    apply_time: str
    form_id: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Attachment:
    """File attachment object"""
    id: str
    name: str
    size: int
    content_type: str
    url: Optional[str] = None


@dataclass
class WebhookEvent:
    """Webhook event object"""
    event_type: str
    timestamp: str
    data: Dict[str, Any]
    trigger_user_id: Optional[str] = None


class GaroonClient:
    """
    Garoon API client for Cybozu Garoon integration.

    Garoon is a Japanese groupware solution providing calendar, workflow,
    and other collaboration features. This client handles API interactions
    with these features.

    API Documentation: https://lp.yoom.fun/apps/garoon
    Requires:
    - Garoon domain
    - API token or OAuth credentials
    """

    def __init__(
        self,
        domain: str,
        api_token: str,
        webhook_secret: Optional[str] = None
    ):
        """
        Initialize Garoon client.

        Args:
            domain: Garoon domain (e.g., "example.cybozu.com")
            api_token: Garoon API token
            webhook_secret: Optional secret for webhook signature verification
        """
        self.domain = domain
        self.api_token = api_token
        self.webhook_secret = webhook_secret
        self.session = None
        self._rate_limit_delay = 0.1
        self.BASE_URL = f"https://{domain}/g/api/v1"

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"X-Cybozu-API-Token": self.api_token}
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
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
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
                if response.status == 204:
                    return {}

                response_data = await response.json()

                if response.status >= 400:
                    error_message = response_data.get("error", response_data.get("message", "Unknown error"))
                    raise Exception(
                        f"Garoon API error (Status {response.status}): {error_message}"
                    )

                return response_data

        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")

    # ==================== Workflow Operations ====================

    async def get_pending_approval_requests(
        self,
        limit: Optional[int] = None
    ) -> List[WorkflowRequest]:
        """
        Get list of pending approval requests.

        Args:
            limit: Maximum number of results to return

        Returns:
            List of WorkflowRequest objects

        Raises:
            Exception: If request fails
        """
        params = {}
        if limit:
            params["limit"] = limit

        response_data = await self._make_request(
            "GET",
            "/workflow/approval/requests/pending",
            params=params
        )

        requests_list = response_data.get("requests", [])

        return [
            WorkflowRequest(
                id=req.get("request_id", ""),
                title=req.get("title", ""),
                applicant_id=req.get("applicant_id", ""),
                status=req.get("status", "pending"),
                apply_time=req.get("apply_time", ""),
                form_id=req.get("form_id"),
                description=req.get("description")
            )
            for req in requests_list
        ]

    async def get_workflow_requests(
        self,
        status: Optional[str] = None,
        applicant_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[WorkflowRequest]:
        """
        Get list of workflow requests with filters.

        Args:
            status: Filter by status (draft, pending, approved, rejected)
            applicant_id: Filter by applicant user ID
            from_date: Filter by start date (ISO 8601 format)
            to_date: Filter by end date (ISO 8601 format)
            limit: Maximum number of results to return

        Returns:
            List of WorkflowRequest objects

        Raises:
            Exception: If request fails
        """
        params = {}

        if status:
            params["status"] = status
        if applicant_id:
            params["applicant_id"] = applicant_id
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if limit:
            params["limit"] = limit

        response_data = await self._make_request(
            "GET",
            "/workflow/approval/requests",
            params=params
        )

        requests_list = response_data.get("requests", [])

        return [
            WorkflowRequest(
                id=req.get("request_id", ""),
                title=req.get("title", ""),
                applicant_id=req.get("applicant_id", ""),
                status=req.get("status", ""),
                apply_time=req.get("apply_time", ""),
                form_id=req.get("form_id"),
                description=req.get("description")
            )
            for req in requests_list
        ]

    async def get_request_attachments(
        self,
        request_id: str
    ) -> List[Attachment]:
        """
        Get files attached to a workflow request.

        Args:
            request_id: Request ID

        Returns:
            List of Attachment objects

        Raises:
            Exception: If request fails
            ValueError: If request_id is empty
        """
        if not request_id:
            raise ValueError("request_id is required")

        response_data = await self._make_request(
            "GET",
            f"/workflow/approval/requests/{request_id}/attachments"
        )

        attachments_list = response_data.get("attachments", [])

        return [
            Attachment(
                id=att.get("id", ""),
                name=att.get("name", ""),
                size=att.get("size", 0),
                content_type=att.get("content_type", ""),
                url=att.get("url")
            )
            for att in attachments_list
        ]

    async def download_attachment(
        self,
        attachment_id: str,
        output_path: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Download an attachment file.

        Args:
            attachment_id: Attachment ID
            output_path: Optional file path to save the file

        Returns:
            File bytes if output_path is None
            None if output_path is provided (file is saved to disk)

        Raises:
            Exception: If download fails
        """
        url = f"{self.BASE_URL}/workflow/approval/attachments/{attachment_id}"

        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Download failed (Status {response.status})")

                file_content = await response.read()

                if output_path:
                    with open(output_path, "wb") as f:
                        f.write(file_content)
                    return None
                else:
                    return file_content

        except aiohttp.ClientError as e:
            raise Exception(f"Network error during download: {str(e)}")

    # ==================== User Operations ====================

    async def search_users(
        self,
        keyword: Optional[str] = None,
        employee_code: Optional[str] = None,
        department: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[User]:
        """
        Search for users.

        Args:
            keyword: Search keyword (searches in name and email)
            employee_code: Filter by employee code
            department: Filter by department name
            limit: Maximum number of results to return

        Returns:
            List of User objects

        Raises:
            Exception: If request fails
        """
        params = {}

        if keyword:
            params["keyword"] = keyword
        if employee_code:
            params["code"] = employee_code
        if department:
            params["department"] = department
        if limit:
            params["limit"] = limit

        response_data = await self._make_request(
            "GET",
            "/base/users",
            params=params
        )

        users_list = response_data.get("users", [])

        return [
            User(
                id=user.get("id", ""),
                name=user.get("name", ""),
                code=user.get("code", ""),
                email=user.get("email"),
                department=user.get("department"),
                title=user.get("title")
            )
            for user in users_list
        ]

    async def get_user(self, user_id: str) -> Optional[User]:
        """
        Get details of a specific user.

        Args:
            user_id: User ID

        Returns:
            User object or None if not found

        Raises:
            Exception: If request fails
        """
        try:
            response_data = await self._make_request(
                "GET",
                f"/base/users/{user_id}"
            )

            return User(
                id=response_data.get("id", ""),
                name=response_data.get("name", ""),
                code=response_data.get("code", ""),
                email=response_data.get("email"),
                department=response_data.get("department"),
                title=response_data.get("title")
            )

        except Exception:
            return None

    # ==================== Schedule Operations ====================

    async def create_event(
        self,
        subject: str,
        start: str,
        end: str,
        attendees: List[str],
        description: Optional[str] = None,
        location: Optional[str] = None,
        facility_id: Optional[str] = None,
        is_all_day: bool = False,
        visibility: str = "public"
    ) -> Event:
        """
        Create a new schedule event.

        Args:
            subject: Event title
            start: Start time (ISO 8601 format)
            end: End time (ISO 8601 format)
            attendees: List of attendee user IDs
            description: Optional event description
            location: Optional location
            facility_id: Optional facility ID to reserve
            is_all_day: Whether this is an all-day event
            visibility: Event visibility (public, private, limited)

        Returns:
            Created Event object

        Raises:
            Exception: If creation fails
            ValueError: If required parameters are missing
        """
        if not subject or not start or not end:
            raise ValueError("subject, start, and end are required")

        payload = {
            "subject": subject,
            "start": start,
            "end": end,
            "attendees": attendees,
            "is_all_day": is_all_day,
            "visibility": visibility
        }

        if description:
            payload["description"] = description
        if location:
            payload["location"] = location
        if facility_id:
            payload["facility_id"] = facility_id

        response_data = await self._make_request(
            "POST",
            "/schedule/events",
            json_data=payload
        )

        return Event(
            id=response_data.get("id", ""),
            subject=response_data.get("subject", subject),
            start=response_data.get("start", start),
            end=response_data.get("end", end),
            attendees=response_data.get("attendees", attendees),
            description=response_data.get("description"),
            location=response_data.get("location"),
            facility_id=response_data.get("facility_id"),
            event_type=response_data.get("type", "normal")
        )

    async def update_event(
        self,
        event_id: str,
        subject: Optional[str] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        facility_id: Optional[str] = None,
        visibility: Optional[str] = None
    ) -> Event:
        """
        Update an existing schedule event.

        Args:
            event_id: Event ID to update
            subject: Optional new event title
            start: Optional new start time
            end: Optional new end time
            attendees: Optional new list of attendees
            description: Optional new description
            location: Optional new location
            facility_id: Optional new facility ID
            visibility: Optional new visibility setting

        Returns:
            Updated Event object

        Raises:
            Exception: If update fails
            ValueError: If event_id is empty
        """
        if not event_id:
            raise ValueError("event_id is required")

        payload = {}

        if subject:
            payload["subject"] = subject
        if start:
            payload["start"] = start
        if end:
            payload["end"] = end
        if attendees:
            payload["attendees"] = attendees
        if description:
            payload["description"] = description
        if location:
            payload["location"] = location
        if facility_id:
            payload["facility_id"] = facility_id
        if visibility:
            payload["visibility"] = visibility

        response_data = await self._make_request(
            "PUT",
            f"/schedule/events/{event_id}",
            json_data=payload
        )

        return Event(
            id=response_data.get("id", event_id),
            subject=response_data.get("subject", ""),
            start=response_data.get("start", ""),
            end=response_data.get("end", ""),
            attendees=response_data.get("attendees", []),
            description=response_data.get("description"),
            location=response_data.get("location"),
            facility_id=response_data.get("facility_id"),
            event_type=response_data.get("type", "normal")
        )

    async def delete_event(self, event_id: str) -> None:
        """
        Delete a schedule event.

        Args:
            event_id: Event ID to delete

        Raises:
            Exception: If deletion fails
            ValueError: If event_id is empty
        """
        if not event_id:
            raise ValueError("event_id is required")

        await self._make_request(
            "DELETE",
            f"/schedule/events/{event_id}"
        )

    async def get_user_events(
        self,
        user_ids: List[str],
        start: str,
        end: str,
        target: Optional[str] = None
    ) -> List[Event]:
        """
        Get events for multiple users.

        Args:
            user_ids: List of user IDs
            start: Start date/time (ISO 8601 format)
            end: End date/time (ISO 8601 format)
            target: Optional target type (user, facility)

        Returns:
            List of Event objects

        Raises:
            Exception: If request fails
            ValueError: If required parameters are missing
        """
        if not user_ids or not start or not end:
            raise ValueError("user_ids, start, and end are required")

        params = {
            "user_ids": ",".join(user_ids),
            "start": start,
            "end": end
        }

        if target:
            params["target"] = target

        response_data = await self._make_request(
            "GET",
            "/schedule/events",
            params=params
        )

        events_list = response_data.get("events", [])

        return [
            Event(
                id=event.get("id", ""),
                subject=event.get("subject", ""),
                start=event.get("start", ""),
                end=event.get("end", ""),
                attendees=event.get("attendees", []),
                description=event.get("description"),
                location=event.get("location"),
                facility_id=event.get("facility_id"),
                event_type=event.get("type", "normal")
            )
            for event in events_list
        ]

    async def check_user_availability(
        self,
        user_id: str,
        start: str,
        end: str
    ) -> List[AvailabilitySlot]:
        """
        Check user availability within a time range.

        Args:
            user_id: User ID to check
            start: Start time (ISO 8601 format)
            end: End time (ISO 8601 format)

        Returns:
            List of AvailabilitySlot objects

        Raises:
            Exception: If request fails
        """
        params = {
            "user_id": user_id,
            "start": start,
            "end": end
        }

        response_data = await self._make_request(
            "GET",
            "/schedule/availability/user",
            params=params
        )

        slots_list = response_data.get("slots", [])

        return [
            AvailabilitySlot(
                start=slot.get("start", ""),
                end=slot.get("end", ""),
                available=slot.get("available", True)
            )
            for slot in slots_list
        ]

    async def check_facility_availability(
        self,
        facility_id: str,
        start: str,
        end: str
    ) -> List[AvailabilitySlot]:
        """
        Check facility availability within a time range.

        Args:
            facility_id: Facility ID to check
            start: Start time (ISO 8601 format)
            end: End time (ISO 8601 format)

        Returns:
            List of AvailabilitySlot objects

        Raises:
            Exception: If request fails
        """
        params = {
            "facility_id": facility_id,
            "start": start,
            "end": end
        }

        response_data = await self._make_request(
            "GET",
            "/schedule/availability/facility",
            params=params
        )

        slots_list = response_data.get("slots", [])

        return [
            AvailabilitySlot(
                start=slot.get("start", ""),
                end=slot.get("end", ""),
                available=slot.get("available", True)
            )
            for slot in slots_list
        ]

    # ==================== Webhook Handling ====================

    async def handle_webhook(
        self,
        payload: bytes,
        signature: Optional[str] = None
    ) -> WebhookEvent:
        """
        Handle incoming webhook events.

        Supported events:
        - schedule_created: When a schedule is registered
        - schedule_updated: When a schedule is registered or updated
        - workflow_approved: When a workflow is approved

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
            event_type=event_data.get("eventType", ""),
            timestamp=event_data.get("createdAt", datetime.utcnow().isoformat()),
            data=event_data.get("data", {}),
            trigger_user_id=event_data.get("triggerUserId")
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
    """Example usage of Garoon client"""

    # Replace with your actual credentials
    DOMAIN = "example.cybozu.com"
    API_TOKEN = "your_garoon_api_token"

    async with GaroonClient(domain=DOMAIN, api_token=API_TOKEN) as client:
        try:
            # Search users
            users = await client.search_users(keyword="山田", limit=10)
            print(f"Found {len(users)} users")
            for user in users[:3]:
                print(f"  - {user.name} ({user.code})")

            # Get pending approval requests
            pending = await client.get_pending_approval_requests(limit=10)
            print(f"Pending requests: {len(pending)}")
            for req in pending[:3]:
                print(f"  - {req.title} (Status: {req.status})")

            # Check user availability
            if users:
                availability = await client.check_user_availability(
                    users[0].id,
                    "2024-03-01T09:00:00Z",
                    "2024-03-01T18:00:00Z"
                )
                print(f"Available slots for {users[0].name}: {len(availability)}")

            # Create event
            if len(users) >= 2:
                event = await client.create_event(
                    subject="Project Meeting",
                    start="2024-03-05T10:00:00Z",
                    end="2024-03-05T11:00:00Z",
                    attendees=[users[0].id, users[1].id],
                    location="Meeting Room A",
                    description="Weekly project sync"
                )
                print(f"Created event: {event.id} - {event.subject}")

                # Get user events
                events = await client.get_user_events(
                    user_ids=[users[0].id],
                    start="2024-03-01T00:00:00Z",
                    end="2024-03-31T23:59:59Z"
                )
                print(f"Events in March: {len(events)}")

                # Update event
                updated = await client.update_event(
                    event.id,
                    location="Meeting Room B"
                )
                print(f"Updated event location to: {updated.location}")

                # Delete event
                await client.delete_event(event.id)
                print("Event deleted")

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())