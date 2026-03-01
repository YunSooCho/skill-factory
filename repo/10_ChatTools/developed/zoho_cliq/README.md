# Zoho Cliq API

Zoho Cliq API integration for team communication.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from zoho_cliq import ZohoCliqClient

client = ZohoCliqClient(oauth_token="your_oauth_token")

# Send message to user
result = client.send_message(
    chat_id="user_123",
    message="Hello from Zoho Cliq!"
)

# Send message to channel
result = client.send_channel_message(
    channel_name="general",
    message="Hello channel!"
)

# List channels
channels = client.list_channels()

# Get user info
user = client.get_user_info()
```

## Features

- Send messages to users and channels
- List channels
- Get channel details
- Get user information
- Upload files
- Create channels
- Get unread message count

## API Reference

- `send_message(chat_id, message, message_format)` - Send to user
- `send_channel_message(channel_name, message, message_format)` - Send to channel
- `list_channels(limit)` - List channels
- `get_channel_detail(channel_id)` - Get channel info
- `get_user_info(user_id)` - Get user info
- `upload_file(chat_id, file_path, message)` - Upload file
- `create_channel(channel_name, description)` - Create channel
- `get_unread_count()` - Get unread count

## Authentication

Requires Zoho OAuth Token.