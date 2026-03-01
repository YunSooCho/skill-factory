# ClickFunnels Integration

## Overview
Implementation of ClickFunnels API for Yoom automation.

## Supported Features

### Contact Management (6 endpoints)
- ✅ Create Contact
- ✅ Get Contact
- ✅ Update Contact
- ✅ Delete Contact
- ✅ Search Contacts
- ✅ Get List of Tags Applied to Contact

### Tag Management (5 endpoints)
- ✅ Get List All Tags in Workspace
- ✅ Create Contact Tag
- ✅ Update Contact Tag
- ✅ Apply Tag to Contact
- ✅ Remove Tag from Contact

### Enrollment Management (4 endpoints)
- ✅ Create New Enrollment
- ✅ Update Enrollment
- ✅ Search Enrollments
- ✅ Get List Courses

### Webhook Triggers (10 triggers)
- ✅ Order Created
- ✅ Subscription Invoice Paid
- ✅ Contact Suspended From Course
- ✅ Contact Identified
- ✅ Contact Submitted Form
- ✅ Course Enrollment Created
- ✅ Contact Created
- ✅ Contact Updated
- ✅ Course Enrollment Completed
- ✅ One-Time Order Paid

## Setup

### 1. Get API Key
1. Visit [ClickFunnels](https://www.clickfunnels.com/)
2. Sign up for an account
3. Go to Account Settings → Integrations → API
4. Generate your API key
5. Note your Workspace ID (visible in URL when logged in)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Contact Management
```python
import asyncio
from clickfunnels_client import ClickFunnelsClient

async def contact_example():
    api_key = "your_api_key"
    workspace_id = "your_workspace_id"

    async with ClickFunnelsClient(api_key=api_key) as client:
        # Create a new contact
        contact = await client.create_contact(
            workspace_id=workspace_id,
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            phone="+1234567890",
            tags=["customer", "vip"]
        )

        print(f"Created Contact ID: {contact.id}")
        print(f"Email: {contact.email}")

        # Get contact details
        contact = await client.get_contact(workspace_id, contact.id)
        print(f"First Name: {contact.first_name}")

        # Update contact
        updated = await client.update_contact(
            workspace_id=workspace_id,
            contact_id=contact.id,
            phone="+9876543210"
        )

        # Search contacts
        contacts = await client.search_contacts(
            workspace_id=workspace_id,
            email="john@example.com"
        )

        print(f"Found {len(contacts)} contacts")

        # Delete contact
        success = await client.delete_contact(workspace_id, contact.id)
        print(f"Deleted: {success}")

asyncio.run(contact_example())
```

### Tag Management
```python
async def tag_example():
    api_key = "your_api_key"
    workspace_id = "your_workspace_id"

    async with ClickFunnelsClient(api_key=api_key) as client:
        # List all tags
        tags = await client.list_tags(workspace_id)
        print(f"Total tags: {len(tags)}")

        # Create a tag
        tag = await client.create_tag(
            workspace_id=workspace_id,
            name="VIP Customer",
            color="#FF5733"
        )
        print(f"Created Tag ID: {tag.id}")

        # Update tag
        updated = await client.update_tag(
            workspace_id=workspace_id,
            tag_id=tag.id,
            color="#00FF00"
        )

        # Apply tag to contact
        contact_id = "contact_123"
        success = await client.apply_tag_to_contact(
            workspace_id=workspace_id,
            contact_id=contact_id,
            tag_id=tag.id
        )
        print(f"Tag applied: {success}")

        # Get contact tags
        contact_tags = await client.get_contact_tags(
            workspace_id=workspace_id,
            contact_id=contact_id
        )
        print(f"Contact has {len(contact_tags)} tags")

        # Remove tag from contact
        success = await client.remove_tag_from_contact(
            workspace_id=workspace_id,
            contact_id=contact_id,
            tag_id=tag.id
        )

        # Delete tag
        success = await client.delete_tag(workspace_id, tag.id)

asyncio.run(tag_example())
```

### Enrollment Management
```python
async def enrollment_example():
    api_key = "your_api_key"
    workspace_id = "your_workspace_id"

    async with ClickFunnelsClient(api_key=api_key) as client:
        # List all courses
        courses = await client.list_courses(workspace_id)
        print(f"Available courses: {len(courses)}")
        for course in courses:
            print(f"- {course.name} (ID: {course.id})")

        # Enroll a contact in a course
        enrollment = await client.create_enrollment(
            workspace_id=workspace_id,
            contact_id="contact_123",
            course_id=courses[0].id
        )
        print(f"Enrollment ID: {enrollment.id}")

        # Update enrollment status
        updated = await client.update_enrollment(
            workspace_id=workspace_id,
            enrollment_id=enrollment.id,
            status="completed"
        )

        # Search enrollments
        enrollments = await client.search_enrollments(
            workspace_id=workspace_id,
            contact_id="contact_123"
        )
        print(f"Contact enrollments: {len(enrollments)}")

asyncio.run(enrollment_example())
```

## Webhook Triggers

ClickFunnels can send webhooks for various events. Set up webhooks in ClickFunnels dashboard under Integrations → Webhooks.

```python
from clickfunnels_client import parse_webhook_event
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook/clickfunnels', methods=['POST'])
def handle_webhook():
    """Handle ClickFunnels webhook events"""
    payload = request.get_json()

    # Parse webhook event
    event = parse_webhook_event(payload)

    print(f"Event Type: {event.event_type}")
    print(f"Contact ID: {event.contact_id}")
    print(f"Order ID: {event.order_id}")
    print(f"Timestamp: {event.timestamp}")

    # Handle different event types
    if event.event_type == "order.created":
        # New order created
        print(f"New order: {event.order_id}")
        # Additional processing...

    elif event.event_type == "contact.created":
        # New contact created
        print(f"New contact: {event.contact_id}")
        # Additional processing...

    elif event.event_type == "course.enrollment.created":
        # New course enrollment
        print(f"New enrollment for contact: {event.contact_id}")
        # Additional processing...

    elif event.event_type == "subscription.invoice.paid":
        # Subscription paid
        print(f"Subscription paid: {event.order_id}")
        # Additional processing...

    # Respond to webhook
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(port=5000)
```

### Supported Webhook Events

1. **Order Created** - `order.created`
2. **Subscription Invoice Paid** - `subscription.invoice.paid`
3. **Contact Suspended From Course** - `course.enrollment.suspended`
4. **Contact Identified** - `contact.identified`
5. **Contact Submitted Form** - `form.submitted`
6. **Course Enrollment Created** - `course.enrollment.created`
7. **Contact Created** - `contact.created`
8. **Contact Updated** - `contact.updated`
9. **Course Enrollment Completed** - `course.enrollment.completed`
10. **One-Time Order Paid** - `order.paid`

## Integration Type
- **Type:** API Key (Bearer Token)
- **Authentication:** Bearer token in Authorization header
- **Protocol:** HTTPS REST API
- **Webhooks:** Supported via external webhook endpoint

## API Response Objects

### Contact
```python
@dataclass
class Contact:
    id: str                              # Contact ID
    email: str                           # Email address
    first_name: str                      # First name
    last_name: str                       # Last name
    phone: str                           # Phone number
    workspace_id: str                    # Workspace ID
    created_at: datetime                 # Creation timestamp
    updated_at: datetime                 # Update timestamp
    tags: List[str]                      # Applied tag IDs
    raw_response: Dict                   # Full API response
```

### Tag
```python
@dataclass
class Tag:
    id: str                              # Tag ID
    name: str                            # Tag name
    color: str                           # Tag color (hex)
    workspace_id: str                    # Workspace ID
    raw_response: Dict                   # Full API response
```

### Enrollment
```python
@dataclass
class Enrollment:
    id: str                              # Enrollment ID
    contact_id: str                      # Contact ID
    course_id: str                       # Course ID
    workspace_id: str                    # Workspace ID
    status: str                          # Status (active, completed, suspended)
    started_at: datetime                 # Start timestamp
    completed_at: datetime               # Completion timestamp
    raw_response: Dict                   # Full API response
```

### Course
```python
@dataclass
class Course:
    id: str                              # Course ID
    name: str                            # Course name
    description: str                     # Course description
    workspace_id: str                    # Workspace ID
    raw_response: Dict                   # Full API response
```

### WebhookEvent
```python
@dataclass
class WebhookEvent:
    event_type: str                      # Event type
    contact_id: str                      # Affected contact ID
    order_id: str                        # Affected order ID
    timestamp: datetime                  # Event timestamp
    payload: Dict[str, Any]              # Full webhook payload
```

## Error Handling

The client handles common errors:

- **ValueError**: Invalid parameters, resource not found, duplicate resources
- **aiohttp.ClientError**: Network errors
- **401 Unauthorized**: Invalid API key
- **404 Not Found**: Resource not found
- **409 Conflict**: Duplicate resource (email exists, tag already applied, etc.)
- **429 Rate Limit**: Too many requests

## Testability
- ⚠️ Requires paid ClickFunnels account
- ✅ All API actions are testable with valid API key
- ⚠️ Rate limits apply based on your plan
- ✅ Webhooks can be tested with sandbox/test mode

## Notes
- Workspace ID is required for all operations
- Workspace ID can be found in the URL when logged into ClickFunnels
- Contacts can have custom fields and tags for segmentation
- Tags are useful for organizing and segmenting contacts
- Webhooks need to be configured in the ClickFunnels dashboard
- Some features may require specific account levels
- API documentation: https://knowledgebase.clickfunnels.com/api-documentation
- Rate limits vary based on your plan level