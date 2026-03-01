# Discord Bot API Client

Python async client for Discord Bot API for server management.

## Features

- Send messages to channels and threads
- Send and download files
- Comprehensive channel and thread management (Create, Rename, Delete, Invite)
- Guild (server) management
- Role management & Assignment
- Member management & Search
- Webhook and gateway event handling
- Custom API connections

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

        # Search for a member
        members = await client.search_guild_members(
            guild_id=123456789012345678,
            query="JohnDoe"
        )
        if members:
            print(f"Found member: {members[0].user['username']}")

        # Get active threads
        threads = await client.get_active_threads(guild_id=123456789012345678)
        print(f"Found {len(threads)} active threads.")

asyncio.run(main())
```

## API Actions

The client supports the following 23 API actions:

**Messages & Files**
1. **Send Message** (`send_message`) - Send a message to a channel
2. **Send Message to Thread** (`send_message_to_thread`) - Send a message to a thread
3. **Send File** (`send_file`) - Upload and send a file to a channel
4. **Download Message File** (`download_message_file`) - Download an attachment from a URL

**Users & Roles**
5. **Overwrite User Roles** (`overwrite_member_roles`) - Overwrite a member's roles completely
6. **Remove User Role** (`remove_member_role`) - Remove a specific role from a member
7. **Get Role Info** (`get_role_info`) - Get detailed information about a role
8. **Add Specific Role** (`add_member_role`) - Grant a specific role to a member
9. **Search Users in Server** (`search_guild_members`) - Search for members by query
10. **Remove User from Server** (`kick_member`) - Kick a user from the guild
11. **Get Member Info** (`get_member_info`) - Get details of a specific member
12. **Modify Member** (`modify_member`) - Change nickname, mute status, etc.
13. **Create Role** (`create_role`) - Create a new role

**Channels & Threads**
14. **Create DM Channel** (`create_dm_channel`) - Open a direct message channel
15. **Create Channel** (`create_channel`) - Create a new channel based on type
16. **Close Channel** (`delete_channel`) - Delete or close a channel
17. **Rename Channel** (`rename_channel`) - Rename an existing channel
18. **Create Channel Invite** (`create_channel_invite`) - Generate an invite URL
19. **Create Thread in Forum** (`create_forum_thread`) - Start a new forum thread
20. **Create Thread from Message** (`create_thread_from_message`) - Start a thread from a specific message

**Data Retrieval & Utilities**
21. **Get Channel Messages** (`get_channel_messages`) - Fetch message history from a channel
22. **Get Thread Messages** (`get_thread_messages`) - Fetch message history from a thread
23. **Get Specific Message** (`get_message`) - Retrieve a single message by ID
24. **Get Server Channels List** (`get_guild_channels`) - Get all channels in a server
25. **Get Server Threads List** (`get_active_threads`) - Get all active threads in a server
26. **Get Guild Info** (`get_guild_info`) - Get guild (server) information
27. **Custom Connect** (`custom_connect`) - Make a raw HTTP request to Discord API

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