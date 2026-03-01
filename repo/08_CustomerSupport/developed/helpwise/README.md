# Helpwise Shared Inbox Integration

Helpwise is a shared inbox platform for managing team email accounts.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to Helpwise account
2. Generate API key from settings

## Usage
```python
from helpwise import HelpwiseClient

client = HelpwiseClient(api_key="your-key")

# Get inboxes
inboxes = client.get_inboxes()

# Get conversations
convs = client.get_conversations(inbox_id="INBOX123")

# Send reply
client.send_reply("CONV456", "Here's the answer")

# Add note
client.create_note("CONV456", "Following up on this")

# Assign
client.assign_conversation("CONV456", "USER789")

# Get labels
labels = client.get_labels()

# Get team
team = client.get_team_members()
```

## API Methods
- `get_inboxes()` - List inboxes
- `get_conversations(inbox_id, limit)` - Get conversations
- `get_conversation(conversation_id)` - Get conversation
- `send_reply(conversation_id, message)` - Reply to conversation
- `create_note(conversation_id, note)` - Add internal note
- `assign_conversation(conversation_id, assignee_id)` - Assign conversation
- `get_labels()` - List labels
- `add_label(conversation_id, label_id)` - Add label
- `get_team_members()` - List team members