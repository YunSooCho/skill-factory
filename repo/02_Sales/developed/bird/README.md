# Bird API Client

Python client for Bird messaging API.

## Features

- Contacts: Manage contacts
- Conversations: Create and manage conversations
- Messages: Send and receive messages
- Participants: Manage conversation participants
- Channels: Search channels

## Installation

```bash
pip install aiohttp
```

## API Actions (16)

Full CRUD for conversations, contacts, messages, participants

## Triggers (8)

- Received/Sent Email Message
- Created Conversation
- Created Channel
- Opened Email
- Deleted/Updated Conversation
- Updated Channel

## Usage

```python
import asyncio
from bird import BirdClient

async def main():
    client = BirdClient(workspace_id="your_workspace", api_key="your_key")

    # Create contact
    contact = await client.create_contact({
        "name": "John Doe",
        "email": "john@example.com"
    })
    print(f"Contact: {contact.id}")

    # Create conversation
    conv = await client.create_conversation({
        "title": "Support Chat"
    })
    print(f"Conversation: {conv.id}")

    # Send message
    msg = await client.create_conversation_message(conv.id, {
        "content": "Hello!"
    })
    print(f"Message: {msg.id}")

asyncio.run(main())
```

## Authentication

Get credentials from Bird dashboard.

## License

MIT