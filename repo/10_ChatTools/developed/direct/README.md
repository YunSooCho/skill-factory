# Direct API Client

Python async client for Direct direct messaging platform API.

## Features

- Send and receive direct messages
- Conversation management
- Message read status tracking
- Webhook event handling
- Rate limiting (20 requests/second)

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

1. Visit [Direct](https://lp.yoom.fun/apps/direct)
2. Sign up or log in to your account
3. Navigate to Settings → API Keys
4. Click "Generate New API Key"
5. Copy your API key and store it securely

## Usage

```python
import asyncio
from direct.client import DirectClient

async def main():
    api_key = "your_direct_api_key"

    async with DirectClient(api_key) as client:
        # Create a new conversation
        conversation = await client.create_conversation(
            peer_id="user_123456",
            initial_message="Hello! How can I help you?"
        )
        print(f"Created conversation: {conversation.id}")

        # Send a message
        message = await client.send_message(
            conversation_id=conversation.id,
            content="Here is the information you requested."
        )
        print(f"Sent message: {message.id}")

        # List conversations
        conversations = await client.list_conversations(limit=20)
        print(f"Found {len(conversations)} conversations")

        # Get conversation details
        conv_details = await client.get_conversation(
            conversation_id=conversation.id,
            include_messages=True,
            message_limit=10
        )
        print(f"Conversation: {conv_details.id}")
        print(f"Unread count: {conv_details.unread_count}")

        # Mark as read
        success = await client.mark_as_read(
            conversation_id=conversation.id,
            message_id=message.id
        )
        print(f"Marked as read: {success}")

asyncio.run(main())
```

## API Actions

1. **Send Message** - Send a message to a conversation
2. **List Conversations** - Retrieve all conversations
3. **Create Conversation** - Create a new direct conversation
4. **Get Conversation** - Get details of a specific conversation
5. **Mark as Read** - Mark conversation or message as read
6. **Delete Message** - Delete a specific message

## Triggers

- **New Message** - Fired when a new message is sent
- **Message Read** - Fired when a message is read

## Webhook Handling

```python
def handle_webhook(webhook_data):
    result = client.handle_webhook(webhook_data)

    if result["event_type"] == "message.created":
        message = result["message"]
        print(f"New message: {message.content}")
    elif result["event_type"] == "message.read":
        print(f"Message read: {result['message_id']}")
```

## Documentation

- Direct Platform: https://lp.yoom.fun/apps/direct
- API Base URL: `https://api.direct.com/v1`
- Rate Limit: 20 requests per second

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