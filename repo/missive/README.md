# Missive Team Inbox Integration

Missive provides team inbox and collaboration platform for shared email management.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to Missive account
2. Generate API token from settings

## Usage
```python
from missive import MissiveClient

client = MissiveClient(api_token="your-token")

# Get conversations
convs = client.get_conversations()

# Get conversation
conv = client.get_conversation("conv_123")

# Send message
client.send_message("conv_123", {
    "body": "Hello!",
    "html": "<p>Hello!</p>"
})

# Get tasks
tasks = client.get_tasks("conv_123")

# Create task
client.create_task({
    "title": "Follow up",
    "due_on": "2024-03-15",
    "assignee_id": "user_456"
})

# Get teams
teams = client.get_teams()

# Get users
users = client.get_users()
```

## API Methods
- `get_conversations(limit)` - List conversations
- `get_conversation(conversation_id)` - Get conversation
- `send_message(conversation_id, data)` - Send message
- `get_tasks(conversation_id)` - Get tasks
- `create_task(data)` - Create task
- `get_teams()` - List teams
- `get_users()` - List users