# Channel Talk Customer Messaging Integration

Channel Talk is a customer messaging platform enabling real-time chat, automation, and team collaboration.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to Channel Talk account
2. Get API Key and Secret Key from settings

## Usage
```python
from channel_talk import ChannelTalkClient

client = ChannelTalkClient(
    api_key="your-api-key",
    secret_key="your-secret-key"
)

# Get messages
messages = client.get_messages(chat_id="CHAT123")

# Send message
client.send_message(chat_id="CHAT123", message="Hello!", sender_id="USER456")

# Get chats
chats = client.get_chats(state="open")

# Get user
user = client.get_user("USER789")

# Create user
client.create_user({
    "name": "John Doe",
    "avatarUrl": "https://example.com/avatar.jpg"
})

# Manage tags
client.add_user_tags("USER789", ["VIP", "Enterprise"])
client.remove_user_tags("USER789", ["Old Tag"])

# Get teams
teams = client.get_teams()

# Get managers
managers = client.get_managers()

# Get campaigns
campaigns = client.get_campaigns()

# Send campaign
client.send_campaign("CAMP456")

# Get statistics
stats = client.get_statistics("2024-01-01", "2024-01-31")

# Search messages
results = client.search_messages("urgent")
```

## API Methods

### Messaging
- `get_messages(chat_id, limit)` - Get chat messages
- `send_message(chat_id, message, sender_id)` - Send message to chat

### Chats
- `get_chats(state, limit, offset)` - List chats
- `get_chat(chat_id)` - Get chat details

### Users
- `get_user(user_id)` - Get user details
- `create_user(data)` - Create user
- `update_user(user_id, data)` - Update user
- `get_user_tags(user_id)` - Get user tags
- `add_user_tags(user_id, tags)` - Add tags
- `remove_user_tags(user_id, tags)` - Remove tags

### Teams & Agents
- `get_teams()` - List teams
- `get_managers(team_id)` - List managers
- `get_manager(manager_id)` - Get manager

### Campaigns
- `get_campaigns(limit)` - List campaigns
- `get_campaign(campaign_id)` - Get campaign stats
- `send_campaign(campaign_id)` - Send campaign

### Plugins & Statistics
- `get_plugin_configs()` - Get plugin configurations
- `get_statistics(start_date, end_date, by)` - Get channel statistics

### Search
- `search_messages(query, limit)` - Search messages

## Webhooks
Channel Talk supports webhooks for real-time notifications:
- New chat
- New message
- User created/updated
- Tag added/removed

Configure webhooks in your Channel Talk settings.