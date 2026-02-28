# Discord Bot API Client

Python async client for Discord Bot API for server management.

## Features

- Send messages with embeds
- Channel management
- Guild (server) management
- Role management
- Member management
- Webhook and gateway event handling

## Installation

```bash
pip install -r requirements.txt
```

## Bot Token Setup

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" tab and create a bot
4. Copy your bot token
5. Enable necessary bot permissions
6. Invite bot to your server using OAuth2 URL

## Usage

```python
import asyncio
from discord_bot.client import DiscordBotClient

async def main():
    bot_token = "your_discord_bot_token"

    async with DiscordBotClient(bot_token) as client:
        # Send a message
        message = await client.send_message(
            channel_id=123456789012345678,
            content="Hello from Discord Bot API!",
            embeds=[{
                "title": "Important Notification",
                "description": "This is an embedded message",
                "color": 0x00ff00
            }]
        )
        print(f"Sent message: {message.id}")

        # Create a channel
        channel = await client.create_channel(
            guild_id=123456789012345678,
            name="general-chat",
            channel_type=0,  # Text channel
            topic="General discussion channel"
        )
        print(f"Created channel: {channel.name}")

        # Get guild info
        guild = await client.get_guild_info(guild_id=123456789012345678)
        print(f"Guild: {guild.name}")
        print(f"Members: {guild.member_count}")

        # Create a role
        role = await client.create_role(
            guild_id=123456789012345678,
            name="VIP Member",
            color=0xff0000,
            hoist=True,
            mentionable=True
        )
        print(f"Created role: {role.name}")

        # Get member info
        member = await client.get_member_info(
            guild_id=123456789012345678,
            user_id=987654321098765432
        )
        print(f"Member: {member.user['username']}")

        # Modify member
        await client.modify_member(
            guild_id=123456789012345678,
            user_id=987654321098765432,
            nick="New Nickname"
        )

asyncio.run(main())
```

## API Actions

1. **Send Message** - Send a message to a channel
2. **Create Channel** - Create a new channel in a guild
3. **Get Guild Info** - Get guild (server) information
4. **Create Role** - Create a new role
5. **Get Member Info** - Get member information
6. **Modify Member** - Modify member properties

## Channel Types

- `0` - Text channel
- `2` - Voice channel
- `4` - Category
- `5` - News channel
- `13` - Stage channel

## Embeds

Create rich embeds with your messages:

```python
embeds = [{
    "title": "Important Update",
    "description": "This is an important announcement",
    "color": 0x00ff00,
    "fields": [
        {"name": "Field 1", "value": "Value 1", "inline": True},
        {"name": "Field 2", "value": "Value 2", "inline": True}
    ],
    "footer": {"text": "Footer text"},
    "timestamp": "2024-01-01T00:00:00.000Z"
}]
```

## Triggers

- **Message Created** - Fired when a new message is sent
- **Member Joined** - Fired when a member joins the guild

## Webhook/Gateway Handling

```python
def handle_webhook(webhook_data):
    result = client.handle_webhook(webhook_data)

    if result["event_type"] == "MESSAGE_CREATE":
        message = result["message"]
        print(f"New message: {message.content}")
    elif result["event_type"] == "GUILD_MEMBER_ADD":
        member = result["member"]
        print(f"New member: {member.user['username']}")
```

## Documentation

- Discord Developer Portal: https://discord.com/developers
- API Documentation: https://discord.com/developers/docs/intro
- API Base URL: `https://discord.com/api/v10`

## Error Handling

```python
try:
    message = await client.send_message(
        channel_id=123456789012345678,
        content="Hello"
    )
except Exception as e:
    print(f"Error: {e}")
```