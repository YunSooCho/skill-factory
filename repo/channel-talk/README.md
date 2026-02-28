# Channel Talk

Channel Talk is a live chat platform for customer support and communication.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Channel Talk API key:

1. Sign up at [Channel Talk](https://channel.io)
2. Go to Settings > Developer > API Key
3. Generate and copy your API key

## Usage

```python
from channel_talk import ChannelTalkClient

# Initialize the client
client = ChannelTalkClient(api_key='your-api-key')

# List user chat history
chats = client.list_user_chats(user_id='user-123')
print(f"Found {len(chats)} chats")

# Send message to user chat
message = client.send_message_to_user_chat(
    chat_id='chat-123',
    message={'plainText': 'Hello! How can I help you?'}
)
print(f"Sent message: {message}")

# Complete a user chat
result = client.complete_user_chat(chat_id='chat-123')
print(f"Chat completed: {result}")

# Send message to internal chat
message = client.send_message_to_internal_chat(
    channel_id='channel-123',
    message={'plainText': 'Internal note about the chat'}
)
print(f"Sent internal message: {message}")
```

## API Methods

- `list_user_chats(user_id, limit, offset)` - List user chat history
- `send_message_to_user_chat(chat_id, message)` - Send message to user chat
- `complete_user_chat(chat_id)` - Mark chat as complete
- `send_message_to_internal_chat(channel_id, message)` - Send message to internal chat