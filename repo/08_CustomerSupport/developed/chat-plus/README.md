# ChatPlus Chat Platform Integration

ChatPlus is a customer messaging platform enabling real-time communication with customers through live chat.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to your ChatPlus account
2. Go to Settings > API Access
3. Generate an API key

## Usage
```python
from chat_plus import ChatPlusClient

client = ChatPlusClient(api_key="your-api-key")

# Get messages
messages = client.get_messages(chat_id="CHAT123")

# Send message
client.send_message(chat_id="CHAT123", message="Hello!")

# Get chats
chats = client.get_chats()

# Statistics
stats = client.get_statistics("2024-01-01", "2024-01-31")
```

## API Methods
- `get_messages(chat_id, limit)` - Get chat messages
- `send_message(chat_id, message)` - Send message
- `get_chats(limit)` - List chats
- `get_user(user_id)` - Get user details
- `create_user(data)` - Create user
- `get_agents()` - Get support agents
- `get_statistics(start_date, end_date)` - Get statistics