# Inout WhatsApp API Client

Python async client for Inout WhatsApp Business API integration.

## Features

- Send WhatsApp messages
- Template message support
- Message delivery status tracking
- Contact management
- Webhook event handling

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

1. Visit [Inout WhatsApp](https://lp.yoom.fun/apps/inout-whatsapp)
2. Sign up or log in to your account
3. Navigate to Settings → API Keys
4. Click "Generate New API Key"
5. Copy your API key and store it securely
6. Verify your WhatsApp Business account

## Usage

```python
import asyncio
from inout_whatsapp.client import InoutWhatsAppClient

async def main():
    api_key = "your_whatsapp_api_key"

    async with InoutWhatsAppClient(api_key) as client:
        # Send a text message
        message = await client.send_message(
            to="+1234567890",
            content="Hello from WhatsApp API!"
        )
        print(f"Sent message: {message.id}")

        # Send a media message
        media_message = await client.send_message(
            to="+1234567890",
            content="Check out this image!",
            media_url="https://example.com/image.jpg"
        )

        # Send a template message
        template_message = await client.send_template(
            to="+1234567890",
            template_name="welcome_message",
            parameters={"name": "John"}
        )

        # Get message status
        status = await client.get_message_status(message_id=message.id)
        print(f"Message status: {status.status}")

        # List messages for a contact
        messages = await client.list_messages(phone="+1234567890", limit=20)
        print(f"Found {len(messages)} messages")

        # Get contact info
        contact = await client.get_contact(phone="+1234567890")
        print(f"Contact: {contact.name or contact.phone}")

        # List all contacts
        contacts = await client.list_contacts(limit=50)
        print(f"Found {len(contacts)} contacts")

asyncio.run(main())
```

## API Actions

1. **Send Message** - Send a text or media message
2. **Send Template** - Send a pre-approved template message
3. **Get Message Status** - Get delivery/read status
4. **List Messages** - List messages with optional phone filter
5. **Get Contact** - Get contact information
6. **List Contacts** - List all contacts

## Message Statuses

- `sent` - Message sent to WhatsApp server
- `delivered` - Message delivered to recipient
- `read` - Message read by recipient
- `failed` - Message failed to deliver

## Phone Number Format

Use the E.164 format (e.g., `+1234567890`):

```python
# US number
to="+14155552671"

# UK number
to="+447700900123"

# Korean number
to="+821012345678"
```

## Template Messages

Use pre-approved WhatsApp templates:

```python
await client.send_template(
    to="+1234567890",
    template_name="shipping_update",
    parameters={
        "tracking_number": "1234567890",
        "estimated_delivery": "2024-01-15"
    }
)
```

## Triggers

- **Message Received** - Fired when a new message is received
- **Status Updated** - Fired when message status changes

## Webhook Handling

```python
def handle_webhook(webhook_data):
    result = client.handle_webhook(webhook_data)

    if result["event_type"] == "message.received":
        message = result["message"]
        print(f"New message from {message.from_}: {message.content}")
    elif result["event_type"] == "message.status.updated":
        status = result["status"]
        print(f"Message {status.message_id} status: {status.status}")
```

## Documentation

- Inout WhatsApp: https://lp.yoom.fun/apps/inout-whatsapp
- API Base URL: `https://api.inout-whatsapp.com/v1`

## Error Handling

```python
try:
    message = await client.send_message(
        to="+1234567890",
        content="Hello"
    )
except Exception as e:
    print(f"Error: {e}")
```