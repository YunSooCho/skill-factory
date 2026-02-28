# Front Shared Inbox Integration

Front is a shared inbox platform for managing customer communications across multiple channels.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to your Front account
2. Go to Settings > API Tokens
3. Generate an API token

## Usage
```python
from front import FrontClient

client = FrontClient(api_token="your-token")

# Get conversations
conversations = client.get_conversations(status="archived")

# Get conversation
conv = client.get_conversation("conv_123")

# Send message
client.send_message("conv_123", "Thank you for your message!")

# Add comment
client.add_comment("conv_123", "Internal note: check with support")

# Get inboxes
inboxes = client.get_inboxes()

# Get team members
teammates = client.get_teammates()
```

## API Methods
- `get_conversations(status, limit)` - List conversations
- `get_conversation(conversation_id)` - Get conversation
- `send_message(conversation_id, message)` - Send reply
- `add_comment(conversation_id, comment)` - Add internal comment
- `get_inboxes()` - List inboxes
- `get_teams()` - List teams
- `get_teammates()` - List team members
- `get_channels()` - List channels