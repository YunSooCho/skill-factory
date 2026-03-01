# Hilos API Client

Python async client for Hilos customer messaging platform API.

## Features

- Send messages to customers
- Conversation management
- Template messages
- Contact management
- Webhook event handling

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

1. Visit [Hilos](https://lp.yoom.fun/apps/hilos)
2. Sign up or log in to your account
3. Navigate to Settings → API Keys
4. Click "Generate New API Key"
5. Copy your API key and store it securely

## Usage

```python
import asyncio
from hilos.client import HilosClient

async def main():
    api_key = "your_hilos_api_key"

    async with HilosClient(api_key) as client:
        # List contacts
        contacts = await client.list_contacts(limit=20)
        print(f"Found {len(contacts)} contacts")

        if contacts:
            contact_id = contacts[0].id

            # Get contact details
            contact = await client.get_contact(contact_id=contact_id)
            print(f"Contact: {contact.name}")

        # List conversations
        conversations = await client.list_conversations(status="open", limit=10)
        print(f"Found {len(conversations)} conversations")

        if conversations:
            conversation_id = conversations[0].id

            # Get conversation details
            conversation = await client.get_conversation(conversation_id=conversation_id)
            print(f"Conversation: {conversation.id}")

            # Send a message
            message = await client.send_message(
                conversation_id=conversation_id,
                content="Hello! How can I help you today?"
            )

            # Send a template message
            template_message = await client.send_template(
                contact_id=contact_id,
                template_name="welcome_message",
                parameters={"name": contact.name}
            )

asyncio.run(main())
```

## API Actions

1. **Send Message** - Send a message to a conversation
2. **List Conversations** - List conversations with optional filters
3. **Get Conversation** - Get conversation details
4. **Send Template** - Send a pre-configured template message
5. **Get Contact** - Get contact details
6. **List Contacts** - List contacts with optional filters

## Conversation Statuses

- `open` - Active conversation
- `closed` - Closed conversation
- `pending` - Waiting for response

## Template Messages

Use pre-configured templates:

```python
await client.send_template(
    contact_id="contact_123",
    template_name="order_confirmation",
    parameters={"order_id": "12345", "total": "$99.99"}
)
```

## Triggers

- **Message Received** - Fired when a new message is received
- **Conversation Created** - Fired when a new conversation is created

## Webhook Handling

```python
def handle_webhook(webhook_data):
    result = client.handle_webhook(webhook_data)

    if result["event_type"] == "message.received":
        message = result["message"]
        print(f"New message: {message.content}")
    elif result["event_type"] == "conversation.created":
        conversation = result["conversation"]
        print(f"New conversation: {conversation.id}")
```

## Documentation

- Hilos Platform: https://lp.yoom.fun/apps/hilos
- API Base URL: `https://api.hilos.co/v1`

## Error Handling

```python
try:
    message = await client.send_message(
        conversation_id="conv_123",
        content="Hello"
    )
except Exception as e:
    print(f"Error: {e}")
```