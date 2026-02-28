# Gist Communication Platform Integration

Gist provides unified customer communication and engagement platform.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to Gist account
2. Generate API key in settings

## Usage
```python
from gist import GistClient

client = GistClient(api_key="your-key")

# Get conversations
conversations = client.get_conversations()

# Send message
client.send_message("CONV123", "Hello!")

# Manage users
user = client.get_user("USER456")
client.create_user({"name": "John", "email": "john@example.com"})

# Get teams
teams = client.get_teams()
```

## API Methods
- `get_messages(conversation_id, limit)` - Get messages
- `send_message(conversation_id, message)` - Send message
- `get_conversations(limit)` - List conversations
- `get_user(user_id)` - Get user
- `create_user(data)` - Create user
- `get_teams()` - List teams