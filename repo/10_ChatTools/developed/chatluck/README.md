# Chatluck API Client

Python async client for Chatluck messaging platform API.

## Features

- Send and receive messages
- Channel management
- User management
- Webhook event handling
- Rate limiting (10 requests/second)

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

1. Visit [Chatluck](https://lp.yoom.fun/apps/chatluck)
2. Sign up or log in to your account
3. Navigate to Settings → API Keys
4. Click "Generate New API Key"
5. Copy your API key and store it securely

## Usage

```python
import asyncio
from chatluck.client import ChatluckClient

async def main():
    api_key = "your_chatluck_api_key"

    async with ChatluckClient(api_key) as client:
        # Send a message
        message = await client.send_message(
            channel_id="ch_123456",
            content="Hello from Chatluck API!"
        )
        print(f"Sent message: {message.id}")

        # List messages
        messages = await client.list_messages(
            channel_id="ch_123456",
            limit=10
        )
        print(f"Retrieved {len(messages)} messages")

        # Create a channel
        channel = await client.create_channel(
            name="Team Project",
            description="Discussion for our project"
        )
        print(f"Created channel: {channel.id}")

        # List channels
        channels = await client.list_channels(limit=20)
        print(f"Found {len(channels)} channels")

        # Get user info
        user = await client.get_user_info("user_123456")
        print(f"User: {user.name}")

        # List users
        users = await client.list_users(limit=50)
        print(f"Total users: {len(users)}")

asyncio.run(main())
```

## API Actions

1. **Send Message** - Send a message to a channel
2. **List Messages** - Retrieve messages from a channel
3. **Create Channel** - Create a new chat channel
4. **List Channels** - Retrieve available channels
5. **Get User Info** - Get information about a specific user
6. **List Users** - Retrieve list of users

## Triggers

- **New Message** - Fired when a new message is sent
- **User Joined** - Fired when a user joins a channel

## Webhook Handling

```python
def handle_webhook(webhook_data):
    result = client.handle_webhook(webhook_data)

    if result["event_type"] == "message.created":
        message = result["message"]
        print(f"New message: {message.content}")
    elif result["event_type"] == "user.joined":
        user = result["user"]
        print(f"User joined: {user.name}")
```

## Documentation

- [Chatluck Platform](https://lp.yoom.fun/apps/chatluck)
- API Base URL: `https://api.chatluck.com/v1`
- Rate Limit: 10 requests per second

## Error Handling

The client will raise exceptions on failed requests. Always wrap API calls in try-except blocks:

```python
try:
    message = await client.send_message(channel_id="ch_123", content="Hello")
except Exception as e:
    print(f"Error sending message: {e}")
```