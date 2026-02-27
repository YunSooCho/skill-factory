# ClickSend SMS & Email Messaging Integration

## Overview
Implementation of ClickSend API for Yoom automation.

## Supported Features

### SMS Messaging (4 endpoints)
- ✅ Send SMS
- ✅ Send SMS Campaign
- ✅ Send Email-SMS (Email)
- ✅ Cancel SMS

### Contact List Management (4 endpoints)
- ✅ Create Contact List
- ✅ Update Contact List
- ✅ Delete Contact List
- ✅ Search Contact List

### Contact Management (5 endpoints)
- ✅ Create Contact
- ✅ Get Contact
- ✅ Update Contact
- ✅ Delete Contact
- ✅ Get Contacts

## Setup

### 1. Get API Credentials
1. Visit [ClickSend](https://www.clicksend.com/)
2. Sign up for an account
3. Go to Settings → API Credentials
4. Get your **Username** and **API Key**

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### SMS Messaging
```python
import asyncio
from datetime import datetime, timedelta
from clicksend_client import ClickSendClient

async def sms_example():
    username = "your_username"
    api_key = "your_api_key"

    async with ClickSendClient(username=username, api_key=api_key) as client:
        # Send single SMS
        message = await client.send_sms(
            body="Hello from ClickSend!",
            to="+15551234567",  # Include country code
            from_number="ClickSend"  # Optional sender name
        )

        print(f"Message ID: {message.message_id}")
        print(f"Status: {message.status}")

        # Send SMS campaign to multiple recipients
        recipients = [
            "+15551234567",
            "+442071234567",
            "+61212345678"
        ]

        campaign = await client.send_sms_campaign(
            body="Special offer! Use code SAVE20 for 20% off.",
            recipients=recipients,
            from_number="YourBrand"
        )

        print(f"Campaign ID: {campaign.message_id}")
        print(f"Recipients: {campaign.recipient_count}")

        # Schedule an SMS for later
        scheduled_time = datetime.now() + timedelta(hours=24)
        scheduled_msg = await client.send_sms(
            body="Don't forget our webinar tomorrow!",
            to="+15551234567",
            schedule=scheduled_time
        )

        print(f"Scheduled message ID: {scheduled_msg.message_id}")

        # Cancel a scheduled message
        success = await client.cancel_sms(message_id="msg123456")
        print(f"Cancelled: {success}")

asyncio.run(sms_example())
```

### Email Messaging
```python
async def email_example():
    username = "your_username"
    api_key = "your_api_key"

    async with ClickSendClient(username=username, api_key=api_key) as client:
        # Send email
        message = await client.send_email_sms(
            to="recipient@example.com",
            subject="Welcome to Our Service",
            body="<h1>Welcome!</h1><p>Thank you for signing up.</p>",
            from_name="Your Company"
        )

        print(f"Email ID: {message.message_id}")
        print(f"Status: {message.status}")

        # Schedule an email for later
        scheduled_time = datetime.now() + timedelta(days=1)
        scheduled_msg = await client.send_email_sms(
            to="recipient@example.com",
            subject="Reminder: Don't forget!",
            body="Your appointment is tomorrow.",
            schedule=scheduled_time
        )

asyncio.run(email_example())
```

### Contact List Management
```python
async def list_example():
    username = "your_username"
    api_key = "your_api_key"

    async with ClickSendClient(username=username, api_key=api_key) as client:
        # Create a contact list
        contact_list = await client.create_contact_list(
            name="VIP Customers",
            description="Our most valuable customers"
        )

        print(f"List ID: {contact_list.list_id}")
        print(f"Name: {contact_list.name}")

        # Search contact lists
        lists = await client.search_contact_lists()
        print(f"Total lists: {len(lists)}")

        for lst in lists:
            print(f"- {lst.name} ({lst.contact_count} contacts)")

        # Update a list
        updated = await client.update_contact_list(
            list_id=contact_list.list_id,
            description="Updated description"
        )

        # Delete a list
        success = await client.delete_contact_list(contact_list.list_id)
        print(f"Deleted: {success}")

asyncio.run(list_example())
```

### Contact Management
```python
async def contact_example():
    username = "your_username"
    api_key = "your_api_key"

    async with ClickSendClient(username=username, api_key=api_key) as client:
        # Create a contact
        contact = await client.create_contact(
            phone_number="+15551234567",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            custom_fields={
                "company": "ACME Corp",
                "notes": "VIP customer"
            },
            list_id=12345
        )

        print(f"Contact ID: {contact.contact_id}")
        print(f"Phone: {contact.phone_number}")
        print(f"Email: {contact.email}")

        # Get contact details
        contact = await client.get_contact(contact.contact_id)
        print(f"First Name: {contact.first_name}")

        # Update contact
        updated = await client.update_contact(
            contact_id=contact.contact_id,
            first_name="Jane",
            phone_number="+19998887777"
        )

        # Get all contacts (paginated)
        contacts = await client.get_contacts(
            list_id=12345,
            page=1,
            limit=25
        )

        print(f"Total contacts: {len(contacts)}")

        # Get contacts by phone or email
        contacts = await client.get_contacts(
            phone="+15551234567",
            limit=10
        )

        # Delete contact
        success = await client.delete_contact(contact.contact_id)
        print(f"Deleted: {success}")

asyncio.run(contact_example())
```

## Integration Type
- **Type:** API Key (Basic Auth)
- **Authentication:** Basic Auth with API username and API key
- **Protocol:** HTTPS REST API
- **Response Format:** JSON

## API Response Objects

### Message
```python
@dataclass
class Message:
    message_id: str                      # Message ID
    status: str                          # Status (pending, sent, delivered, failed)
    schedule: datetime                   # Scheduled time
    recipient_count: int                 # Number of recipients
    body: str                            # Message content
    raw_response: Dict                   # Full API response
```

### ContactList
```python
@dataclass
class ContactList:
    list_id: int                         # List ID
    name: str                            # List name
    status: str                          # Status (active, disabled)
    created_at: datetime                 # Creation timestamp
    contact_count: int                   # Number of contacts in list
    raw_response: Dict                   # Full API response
```

### Contact
```python
@dataclass
class Contact:
    contact_id: int                      # Contact ID
    phone_number: str                    # Phone number (with country code)
    email: str                           # Email address
    first_name: str                      # First name
    last_name: str                       # Last name
    custom_fields: Dict[str, str]        # Custom field values
    lists: List[int]                     # List IDs contact belongs to
    raw_response: Dict                   # Full API response
```

## Phone Number Format

Phone numbers must include the country code:
- US: `+15551234567`
- UK: `+442071234567`
- Australia: `+61212345678`

## Message Status

| Status | Description |
|--------|-------------|
| pending | Message queued for processing |
| sent | Message sent to carrier |
| delivered | Message successfully delivered |
| failed | Message delivery failed |
| cancelled | Message was cancelled |

## Error Handling

The client handles common errors:

- **ValueError**: Invalid parameters, resource not found, duplicate resources
- **aiohttp.ClientError**: Network errors
- **401 Unauthorized**: Invalid credentials
- **403 Forbidden**: Insufficient credits or permissions
- **404 Not Found**: Resource not found
- **409 Conflict**: Duplicate resource
- **429 Rate Limit**: Too many requests

## Testability
- ✅ Free trial available (with limited credits)
- ✅ All API actions are testable with valid credentials
- ⚠️ SMS/Email sending consumes credits
- ⚠️ Rate limits apply based on your plan

## Notes
- Requires both username and API key for authentication
- SMS and email consumption are counted against your credit balance
- Scheduled messages can be cancelled before they're sent
- Contacts can belong to multiple lists
- Custom fields allow storing additional information
- Phone numbers must include country codes (format: +[country_code][number])
- Campaign sending is more efficient than individual messages for bulk operations
- API documentation: https://rest.clicksend.com/v3/