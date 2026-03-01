# TwoChat API

TwoChat API integration for Yoom Apps.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from twochat import TwoChatClient

client = TwoChatClient(api_key="your_api_key")

# Send message
result = client.send_message(
    recipient_id="user_123",
    message="Hello from TwoChat API!"
)

# List conversations
conversations = client.list_conversations()

# Get conversation history
messages = client.get_conversation_history("conv_123")
```

## Features

- Send messages
- List conversations
- Get conversation history
- Create conversations
- Mark messages as read

## API Reference

- `send_message(recipient_id, message, message_type)` - Send message
- `list_conversations(limit, offset)` - List conversations
- `get_conversation_history(conversation_id, limit)` - Get history
- `create_conversation(participant_ids)` - Create conversation
- `mark_message_read(message_id)` - Mark as read
- `delete_message(message_id)` - Delete message

## Authentication

Requires TwoChat API Key.