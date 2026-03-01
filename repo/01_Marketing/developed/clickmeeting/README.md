# ClickMeeting Webinar & Conference Integration

## Overview
Implementation of ClickMeeting API for Yoom automation.

## Supported Features

### Conference Room Management (6 endpoints)
- ✅ List Conference Rooms
- ✅ Create Conference
- ✅ Get Room
- ✅ Update Conference
- ✅ Delete Conference
- ✅ Generate PDF Report

### Session Management (2 endpoints)
- ✅ List Sessions
- ✅ Get Session

### Participant Management (4 endpoints)
- ✅ Register Participant
- ✅ Get Registration
- ✅ Get All Registrants of Session
- ✅ Get Attendees of Room Session

## Setup

### 1. Get API Key
1. Visit [ClickMeeting](https://www.clickmeeting.com/)
2. Sign up for an account
3. Go to Settings → Account → API
4. Generate your API key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Conference Room Management
```python
import asyncio
from datetime import datetime, timedelta
from clickmeeting_client import ClickMeetingClient

async def room_example():
    api_key = "your_api_key"

    async with ClickMeetingClient(api_key=api_key) as client:
        # List all conference rooms
        rooms = await client.list_conference_rooms()
        print(f"Total rooms: {len(rooms)}")
        for room in rooms:
            print(f"- {room.name} (Status: {room.status})")

        # Create a new conference
        starts_at = datetime.now() + timedelta(days=7)
        room = await client.create_conference(
            name="Webinar: Product Launch",
            starts_at=starts_at,
            duration=60,
            room_type="webinar",
            description="Join us for our product launch webinar!",
            access_type=2  # Public
        )

        print(f"Created Room ID: {room.id}")
        print(f"Permanent URL: {room.permanent_url}")

        # Get room details
        room = await client.get_room(room.id)
        print(f"Room Status: {room.status}")

        # Update conference
        updated = await client.update_conference(
            room_id=room.id,
            description="Updated description"
        )

        # Delete conference
        success = await client.delete_conference(room.id)
        print(f"Deleted: {success}")

asyncio.run(room_example())
```

### Session Management
```python
async def session_example():
    api_key = "your_api_key"
    room_id = 12345

    async with ClickMeetingClient(api_key=api_key) as client:
        # List sessions in a room
        sessions = await client.list_sessions(room_id)
        print(f"Sessions: {len(sessions)}")

        for session in sessions:
            print(f"- {session.name} (Status: {session.status})")
            print(f"  Started: {session.starts_at}")

        # Get specific session details
        if sessions:
            session = await client.get_session(room_id, sessions[0].id)
            print(f"Session duration: {session.duration} minutes")

asyncio.run(session_example())
```

### Participant Management
```python
async def participant_example():
    api_key = "your_api_key"
    room_id = 12345

    async with ClickMeetingClient(api_key=api_key) as client:
        # Register a participant
        participant = await client.register_participant(
            room_id=room_id,
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            company="ACME Corp",
            phone="+1234567890"
        )

        print(f"Registered Participant ID: {participant.id}")

        # Get participant registration details
        registration = await client.get_registration(room_id, participant.id)
        print(f"Email: {registration.email}")

        # Get all registrants for a room
        registrants = await client.get_all_registrants(room_id)
        print(f"Total registrants: {len(registrants)}")

        # Get attendees for a specific session
        session_id = 67890
        attendees = await client.get_attendees(room_id, session_id)
        print(f"Session attendees: {len(attendees)}")

        for attendee in attendees:
            print(f"- {attendee.email}")
            if attendee.join_time and attendee.leave_time:
                duration = attendee.duration or "unknown"
                print(f"  Duration: {duration} seconds")

asyncio.run(participant_example())
```

### Generate Reports
```python
async def report_example():
    api_key = "your_api_key"
    session_id = 67890

    async with ClickMeetingClient(api_key=api_key) as client:
        # Generate PDF report
        report = await client.generate_pdf_report(session_id)

        print(f"Report URL: {report.report_url}")
        print(f"Generated at: {report.generated_at}")

asyncio.run(report_example())
```

## Integration Type
- **Type:** API Key (X-API-KEY header)
- **Authentication:** API key in custom header
- **Protocol:** HTTPS REST API
- **Response Format:** JSON

## API Response Objects

### ConferenceRoom
```python
@dataclass
class ConferenceRoom:
    id: int                              # Room ID
    name: str                            # Room name
    room_type: str                       # Room type (webinar, meeting)
    status: str                          # Status (active, upcoming, archived)
    permanent_url: str                   # Permanent URL for the room
    starts_at: datetime                  # Start time
    duration: int                        # Duration in minutes
    description: str                     # Room description
    raw_response: Dict                   # Full API response
```

### Session
```python
@dataclass
class Session:
    id: int                              # Session ID
    room_id: int                         # Room ID
    name: str                            # Session name
    status: str                          # Status (active, finished, upcoming)
    starts_at: datetime                  # Start time
    ends_at: datetime                    # End time
    duration: int                        # Duration in minutes
    raw_response: Dict                   # Full API response
```

### Participant
```python
@dataclass
class Participant:
    id: int                              # Participant ID
    email: str                           # Email address
    first_name: str                      # First name
    last_name: str                       # Last name
    role: str                            # Role (presenter, attendee, etc.)
    registered_at: datetime              # Registration timestamp
    room_id: int                         # Room ID
    session_id: int                      # Session ID (if applicable)
    raw_response: Dict                   # Full API response
```

### Attendee
```python
@dataclass
class Attendee:
    id: int                              # Attendee ID
    session_id: int                      # Session ID
    email: str                           # Email address
    first_name: str                      # First name
    last_name: str                       # Last name
    join_time: datetime                  # Join time
    leave_time: datetime                 # Leave time
    duration: int                        # Attendance duration in seconds
    raw_response: Dict                   # Full API response
```

### GeneratedReport
```python
@dataclass
class GeneratedReport:
    session_id: int                      # Session ID
    report_url: str                      # URL to download PDF report
    report_type: str                     # Report type (pdf)
    generated_at: datetime               # Generation timestamp
    raw_response: Dict                   # Full API response
```

## Room Access Types

| Type | Value | Description |
|------|-------|-------------|
| Public | 2 | Anyone with URL can join |
| Password Protected | 3 | Requires password to join |
| Private | 4 | Invitation only |

## Room Types

| Type | Description |
|------|-------------|
| webinar | One-to-many presentation |
| meeting | Many-to-many collaboration |

## Error Handling

The client handles common errors:

- **ValueError**: Invalid parameters, resource not found
- **aiohttp.ClientError**: Network errors
- **401 Unauthorized**: Invalid API key
- **404 Not Found**: Room, session, or participant not found
- **400 Bad Request**: Invalid request parameters
- **429 Rate Limit**: Too many requests

## Testability
- ✅ Free trial available
- ✅ All API actions are testable with valid API key
- ⚠️ Rate limits apply based on your plan
- ⚠️ Some features may require specific plan levels

## Notes
- Room creation requires proper scheduling with start time and duration
- Permanent URL is generated for each room
- Participants can be registered even before the room starts
- Registrants are those who signed up, attendees are those who actually joined
- Reports are generated asynchronously and contain a download URL
- Access level determines how people can join the room
- Session data includes actual meeting information (start/end times)
- API documentation: https://dev.clickmeeting.com/api/