"""
ClickMeeting Webinar & Conference API Client

Supports:
- List Conference Rooms
- Create Conference
- Get Room
- Update Conference
- Delete Conference
- List Sessions
- Get Session
- Register Participant
- Get Registration
- Get Attendees of Room Session
- Get All Registrants of Session
- Generate PDF Report
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class ConferenceRoom:
    """Conference/Room data"""
    id: int
    name: str
    room_type: str
    status: str
    permanent_url: Optional[str]
    starts_at: Optional[datetime]
    duration: Optional[int]
    description: Optional[str]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class Session:
    """Session data"""
    id: int
    room_id: int
    name: str
    status: str
    starts_at: datetime
    ends_at: Optional[datetime]
    duration: int
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class Participant:
    """Participant data"""
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: str
    registered_at: Optional[datetime]
    room_id: Optional[int]
    session_id: Optional[int]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class Attendee:
    """Attendee data"""
    id: int
    session_id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    join_time: Optional[datetime]
    leave_time: Optional[datetime]
    duration: Optional[int]  # in seconds
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class GeneratedReport:
    """Generated report data"""
    session_id: int
    report_url: str
    report_type: str
    generated_at: datetime
    raw_response: Optional[Dict[str, Any]] = None


class ClickMeetingClient:
    """
    ClickMeeting Webinar & Conference API client.

    API Documentation: https://dev.clickmeeting.com/api/
    This service provides webinar room management, scheduling, and participant management.
    """

    BASE_URL = "https://api.clickmeeting.com/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize ClickMeeting client.

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
            "User-Agent": "ClickMeetingClient/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key
        }

    # ==================== Conference Room Management ====================

    async def list_conference_rooms(
        self,
        status: Optional[str] = None,
        page: int = 1,
        per_page: int = 25
    ) -> List[ConferenceRoom]:
        """
        List all conference rooms.

        Args:
            status: Filter by status (active, upcoming, archived) (optional)
            page: Page number (default: 1)
            per_page: Results per page (default: 25)

        Returns:
            List[ConferenceRoom]: List of conference rooms

        Raises:
            aiohttp.ClientError: If API request fails
        """
        url = f"{self.BASE_URL}/conferences"
        params = {"page": page, "per_page": per_page}

        if status:
            params["status"] = status

        try:
            async with self.session.get(
                url,
                headers=self._get_headers(),
                params=params
            ) as response:
                response.raise_for_status()
                data = await response.json()

                rooms = []
                for item in data:
                    rooms.append(self._parse_room(item))

                return rooms

        except aiohttp.ClientResponseError as e:
            if e.status == 401:
                raise ValueError("Invalid or missing API key")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def create_conference(
        self,
        name: str,
        starts_at: datetime,
        duration: int,
        room_type: str = "webinar",
        description: Optional[str] = None,
        access_type: int = 2,
        password: Optional[str] = None
    ) -> ConferenceRoom:
        """
        Create a new conference.

        Args:
            name: Conference name
            starts_at: Start time for the conference
            duration: Duration in minutes
            room_type: Room type (webinar, meeting) (default: webinar)
            description: Conference description (optional)
            access_type: Access type (2=public, 3=password) (default: 2)
            password: Password for password-protected rooms (optional)

        Returns:
            ConferenceRoom: Created conference data

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If API request fails
        """
        if not name or not name.strip():
            raise ValueError("name is required")
        if not starts_at:
            raise ValueError("starts_at is required")
        if not duration or duration <= 0:
            raise ValueError("duration must be greater than 0")

        url = f"{self.BASE_URL}/conferences"

        payload = {
            "name": name.strip(),
            "room_type": room_type,
            "starts_at": starts_at.isoformat(),
            "duration": duration,
            "access_type": access_type
        }

        if description:
            payload["description"] = description.strip()
        if password and access_type == 3:
            payload["password"] = password

        try:
            async with self.session.post(
                url,
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_room(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 400:
                raise ValueError(f"Invalid request parameters: {e.message}")
            elif e.status == 401:
                raise ValueError("Invalid or missing API key")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from API")

    async def get_room(self, room_id: int) -> ConferenceRoom:
        """
        Get room details.

        Args:
            room_id: Conference room ID

        Returns:
            ConferenceRoom: Room data

        Raises:
            ValueError: If room not found
            aiohttp.ClientError: If API request fails
        """
        if not room_id:
            raise ValueError("room_id is required")

        url = f"{self.BASE_URL}/conferences/{room_id}"

        try:
            async with self.session.get(
                url,
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_room(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Room {room_id} not found")
            elif e.status == 401:
                raise ValueError("Invalid or missing API key")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def update_conference(
        self,
        room_id: int,
        name: Optional[str] = None,
        starts_at: Optional[datetime] = None,
        duration: Optional[int] = None,
        description: Optional[str] = None,
        password: Optional[str] = None
    ) -> ConferenceRoom:
        """
        Update a conference.

        Args:
            room_id: Conference room ID
            name: New name (optional)
            starts_at: New start time (optional)
            duration: New duration (optional)
            description: New description (optional)
            password: New password (optional)

        Returns:
            ConferenceRoom: Updated conference data

        Raises:
            ValueError: If room not found
            aiohttp.ClientError: If API request fails
        """
        if not room_id:
            raise ValueError("room_id is required")

        url = f"{self.BASE_URL}/conferences/{room_id}"

        payload = {}
        if name:
            payload["name"] = name.strip()
        if starts_at:
            payload["starts_at"] = starts_at.isoformat()
        if duration:
            payload["duration"] = duration
        if description is not None:
            payload["description"] = description.strip()
        if password:
            payload["password"] = password

        if not payload:
            raise ValueError("At least one field to update must be provided")

        try:
            async with self.session.patch(
                url,
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_room(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Room {room_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def delete_conference(self, room_id: int) -> bool:
        """
        Delete a conference.

        Args:
            room_id: Conference room ID

        Returns:
            bool: True if deletion was successful

        Raises:
            ValueError: If room not found
            aiohttp.ClientError: If API request fails
        """
        if not room_id:
            raise ValueError("room_id is required")

        url = f"{self.BASE_URL}/conferences/{room_id}"

        try:
            async with self.session.delete(
                url,
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                return True

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Room {room_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")

    # ==================== Session Management ====================

    async def list_sessions(
        self,
        room_id: int,
        status: Optional[str] = None,
        page: int = 1,
        per_page: int = 25
    ) -> List[Session]:
        """
        List sessions for a room.

        Args:
            room_id: Conference room ID
            status: Filter by status (active, finished, upcoming) (optional)
            page: Page number (default: 1)
            per_page: Results per page (default: 25)

        Returns:
            List[Session]: List of sessions

        Raises:
            ValueError: If room not found
            aiohttp.ClientError: If API request fails
        """
        if not room_id:
            raise ValueError("room_id is required")

        url = f"{self.BASE_URL}/conferences/{room_id}/sessions"
        params = {"page": page, "per_page": per_page}

        if status:
            params["status"] = status

        try:
            async with self.session.get(
                url,
                headers=self._get_headers(),
                params=params
            ) as response:
                response.raise_for_status()
                data = await response.json()

                sessions = []
                for item in data:
                    sessions.append(self._parse_session(item))

                return sessions

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Room {room_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def get_session(self, room_id: int, session_id: int) -> Session:
        """
        Get session details.

        Args:
            room_id: Conference room ID
            session_id: Session ID

        Returns:
            Session: Session data

        Raises:
            ValueError: If session not found
            aiohttp.ClientError: If API request fails
        """
        if not room_id or not session_id:
            raise ValueError("room_id and session_id are required")

        url = f"{self.BASE_URL}/conferences/{room_id}/sessions/{session_id}"

        try:
            async with self.session.get(
                url,
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_session(data)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Session {session_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    # ==================== Participant Management ====================

    async def register_participant(
        self,
        room_id: int,
        email: str,
        first_name: str,
        last_name: str,
        **kwargs
    ) -> Participant:
        """
        Register a participant for a room.

        Args:
            room_id: Conference room ID
            email: Participant email
            first_name: Participant first name
            last_name: Participant last name
            **kwargs: Additional fields like company, phone, etc.

        Returns:
            Participant: Registered participant data

        Raises:
            ValueError: If required parameters are missing
            aiohttp.ClientError: If API request fails
        """
        if not room_id:
            raise ValueError("room_id is required")
        if not email or not email.strip():
            raise ValueError("email is required")
        if not first_name or not first_name.strip():
            raise ValueError("first_name is required")
        if not last_name or not last_name.strip():
            raise ValueError("last_name is required")

        url = f"{self.BASE_URL}/conferences/{room_id}/registration"

        payload = {
            "email": email.strip(),
            "first_name": first_name.strip(),
            "last_name": last_name.strip()
        }

        # Add optional fields
        if kwargs:
            payload.update(kwargs)

        try:
            async with self.session.post(
                url,
                headers=self._get_headers(),
                data=json.dumps(payload)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_participant(data, room_id=room_id)

        except aiohttp.ClientResponseError as e:
            if e.status == 400:
                raise ValueError(f"Invalid request parameters: {e.message}")
            elif e.status == 401:
                raise ValueError("Invalid or missing API key")
            elif e.status == 404:
                raise ValueError(f"Room {room_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from API")

    async def get_registration(self, room_id: int, participant_id: int) -> Participant:
        """
        Get participant registration details.

        Args:
            room_id: Conference room ID
            participant_id: Participant ID

        Returns:
            Participant: Participant data

        Raises:
            ValueError: If participant not found
            aiohttp.ClientError: If API request fails
        """
        if not room_id or not participant_id:
            raise ValueError("room_id and participant_id are required")

        url = f"{self.BASE_URL}/conferences/{room_id}/registrations/{participant_id}"

        try:
            async with self.session.get(
                url,
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return self._parse_participant(data, room_id=room_id)

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Participant {participant_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def get_all_registrants(self, room_id: int, session_id: Optional[int] = None) -> List[Participant]:
        """
        Get all registrants for a room or session.

        Args:
            room_id: Conference room ID
            session_id: Optional session ID to filter

        Returns:
            List[Participant]: List of registrants

        Raises:
            ValueError: If room not found
            aiohttp.ClientError: If API request fails
        """
        if not room_id:
            raise ValueError("room_id is required")

        url = f"{self.BASE_URL}/conferences/{room_id}/registrations"

        try:
            async with self.session.get(
                url,
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                data = await response.json()

                registrants = []
                for item in data:
                    registrants.append(self._parse_participant(item, room_id=room_id))

                return registrants

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Room {room_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    async def get_attendees(self, room_id: int, session_id: int) -> List[Attendee]:
        """
        Get attendees who joined a session.

        Args:
            room_id: Conference room ID
            session_id: Session ID

        Returns:
            List[Attendee]: List of attendees

        Raises:
            ValueError: If session not found
            aiohttp.ClientError: If API request fails
        """
        if not room_id or not session_id:
            raise ValueError("room_id and session_id are required")

        url = f"{self.BASE_URL}/conferences/{room_id}/sessions/{session_id}/attendees"

        try:
            async with self.session.get(
                url,
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                data = await response.json()

                attendees = []
                for item in data:
                    attendees.append(self._parse_attendee(item, session_id))

                return attendees

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Session {session_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    # ==================== Report Generation ====================

    async def generate_pdf_report(self, session_id: int) -> GeneratedReport:
        """
        Generate a PDF report for a session.

        Args:
            session_id: Session ID

        Returns:
            GeneratedReport: Report data with download URL

        Raises:
            ValueError: If session not found
            aiohttp.ClientError: If API request fails
        """
        if not session_id:
            raise ValueError("session_id is required")

        url = f"{self.BASE_URL}/sessions/{session_id}/report.pdf"

        try:
            async with self.session.get(
                url,
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                data = await response.json()

                return GeneratedReport(
                    session_id=session_id,
                    report_url=data.get("url", ""),
                    report_type="pdf",
                    generated_at=datetime.now(),
                    raw_response=data
                )

        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise ValueError(f"Session {session_id} not found")
            else:
                raise aiohttp.ClientError(f"API request failed: {e.message}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            raise aiohttp.ClientError(f"Error: {str(e)}")

    # ==================== Helper Methods ====================

    def _parse_room(self, data: Dict[str, Any]) -> ConferenceRoom:
        """Parse room data"""
        starts_at = None
        if data.get("starts_at"):
            try:
                starts_at = datetime.fromisoformat(data["starts_at"].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass

        return ConferenceRoom(
            id=data.get("id", 0),
            name=data.get("name", ""),
            room_type=data.get("room_type", ""),
            status=data.get("status", ""),
            permanent_url=data.get("permanent_url"),
            starts_at=starts_at,
            duration=data.get("duration"),
            description=data.get("description"),
            raw_response=data
        )

    def _parse_session(self, data: Dict[str, Any]) -> Session:
        """Parse session data"""
        starts_at = None
        ends_at = None

        if data.get("starts_at"):
            try:
                starts_at = datetime.fromisoformat(data["starts_at"].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass

        if data.get("ends_at"):
            try:
                ends_at = datetime.fromisoformat(data["ends_at"].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass

        return Session(
            id=data.get("id", 0),
            room_id=data.get("room_id", 0),
            name=data.get("name", ""),
            status=data.get("status", ""),
            starts_at=starts_at,
            ends_at=ends_at,
            duration=data.get("duration", 0),
            raw_response=data
        )

    def _parse_participant(self, data: Dict[str, Any], room_id: Optional[int] = None) -> Participant:
        """Parse participant data"""
        registered_at = None
        if data.get("created_at"):
            try:
                registered_at = datetime.fromisoformat(data["created_at"].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass

        return Participant(
            id=data.get("id", 0),
            email=data.get("email", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            role=data.get("role", ""),
            registered_at=registered_at,
            room_id=room_id or data.get("room_id"),
            session_id=data.get("session_id"),
            raw_response=data
        )

    def _parse_attendee(self, data: Dict[str, Any], session_id: int) -> Attendee:
        """Parse attendee data"""
        join_time = None
        leave_time = None

        if data.get("join_time"):
            try:
                join_time = datetime.fromisoformat(data["join_time"].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass

        if data.get("leave_time"):
            try:
                leave_time = datetime.fromisoformat(data["leave_time"].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass

        return Attendee(
            id=data.get("id", 0),
            session_id=session_id,
            email=data.get("email", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            join_time=join_time,
            leave_time=leave_time,
            duration=data.get("duration"),
            raw_response=data
        )