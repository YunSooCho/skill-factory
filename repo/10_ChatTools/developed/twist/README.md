# Twist API

Twist API integration for Yoom Apps.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from twist import TwistClient

client = TwistClient(api_token="your_api_token")

# Send message
result = client.send_message(
    content="Hello from Twist API!",
    conversation_id=12345
)

# List channels
workspace_id = 67890
channels = client.list_channels(workspace_id)

# Search messages
messages = client.search_messages("query", workspace_id)
```

## Features

- Send messages to conversations
- List workspaces and channels
- Search messages
- Get thread details

## API Reference

- `send_message(content, conversation_id, attachments)` - Send message
- `list_channels(workspace_id)` - List channels
- `list_conversations(channel_id, limit)` - List conversations
- `search_messages(query, workspace_id)` - Search messages
- `get_thread(thread_id)` - Get thread details
- `list_workspaces()` - List workspaces

## Authentication

Requires Twist API Token from your account settings.