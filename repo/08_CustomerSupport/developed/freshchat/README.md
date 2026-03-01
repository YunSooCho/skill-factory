# Freshchat Live Chat Integration

Freshchat provides modern live chat and messaging for customer support.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to your Freshworks account
2. Generate API token for Freshchat

## Usage
```python
from freshchat import FreshchatClient

client = FreshchatClient(api_key="your-token")

# Get conversations
conversations = client.get_conversations(status="open")

# Send message
client.send_message(conversation_id="CONV123", message="Hello!")

# Manage users
user = client.get_user("USER123")
client.create_user({"first_name": "John", "email": "john@example.com"})

# Get teams
teams = client.get_groups()
```

## API Methods
- `get_conversations(status, limit)` - List conversations
- `get_conversation(conversation_id)` - Get conversation
- `send_message(conversation_id, message)` - Send message
- `get_user(user_id)` - Get user
- `create_user(data)` - Create user
- `get_groups()` - List support groups
- `get_agents()` - List agents