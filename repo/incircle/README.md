# Incircle API Client

Python async client for Incircle team communication platform API.

## Features

- Send and receive messages
- Channel management
- Member management
- Team collaboration
- Webhook event handling

## Installation

```bash
pip install -r requirements.txt
```

## API Token Setup

1. Visit [Incircle](https://lp.yoom.fun/apps/incircle)
2. Sign up or log in to your account
3. Navigate to Settings → API Tokens
4. Click "Generate New Token"
5. Copy your API token and store it securely

## Usage

```python
import asyncio
from incircle.client import IncircleClient

async def main():
    api_token = "your_incircle_api_token"

    async with IncircleClient(api_token) as client:
        # List channels
        channels = await client.list_channels(limit=20)
        print(f"Found {len(channels)} channels")

        if channels:
            channel_id = channels[0].id

            # Send a message
            message = await client.send_message(
                channel_id=channel_id,
                content="Hello from Incircle API!"
            )

            # Get channel details
            channel = await client.get_channel(channel_id=channel_id)
            print(f"Channel: {channel.name}")

        # Create a new channel
        new_channel = await client.create_channel(
            name="team-projects",
            description="Discussion for team projects",
            channel_type="public"
        )
        print(f"Created channel: {new_channel.name}")

        # List members
        members = await client.list_members(limit=50)
        print(f"Found {len(members)} members")

        # Invite a member to a channel
        invited_member = await client.invite_member(
            channel_id=channel_id,
            email="newmember@example.com",
            role="member"
        )

asyncio.run(main())
```

## API Actions

1. **Send Message** - Send a message to a channel
2. **List Channels** - List channels with optional type filter
3. **Create Channel** - Create a new channel
4. **Get Channel** - Get channel details
5. **List Members** - List members (channel or workspace)
6. **Invite Member** - Invite a member to a channel

## Channel Types

- `public` - Public channels visible to all members
- `private` - Private channels visible only to members
- `dm` - Direct message channels

## Member Roles

- `owner` - Full permissions
- `admin` - Administrative permissions
- `member` - Standard member permissions
- `guest` - Limited access

## Triggers

- **New Message** - Fired when a new message is sent
- **Member Invited** - Fired when a member is invited

## Webhook Handling

```python
def handle_webhook(webhook_data):
    result = client.handle_webhook(webhook_data)

    if result["event_type"] == "message.created":
        message = result["message"]
        print(f"New message: {message.content}")
    elif result["event_type"] == "member.invited":
        member = result["member"]
        print(f"Member invited: {member.email}")
```

## Documentation

- Incircle Platform: https://lp.yoom.fun/apps/incircle
- API Base URL: `https://api.incircle.io/v1`

## Error Handling

```python
try:
    message = await client.send_message(
        channel_id="ch_123",
        content="Hello"
    )
except Exception as e:
    print(f"Error: {e}")
```