# Freshchat

Freshchat is a customer messaging platform for engaging with customers in real-time.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Freshchat API key:

1. Sign up at [Freshchat](https://www.freshchat.com)
2. Go to Settings > API Key Settings
3. Copy your API Token and App ID

## Usage

```python
from freshchat import FreshchatClient

# Initialize the client
client = FreshchatClient(api_key='your-api-token', app_id='your-app-id')

# Create a user
user = client.create_user({
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'john@example.com'
})
print(f"Created user: {user}")

# Create a conversation
conversation = client.create_conversation({
    'messages': [{'body': 'Hello, I need help with my account'}]
})
print(f"Created conversation: {conversation}")

# Send message to conversation
message = client.send_message_to_conversation(
    conversation_id='conv-123',
    message={'body': 'How can we help you today?'}
)
print(f"Sent message: {message}")

# List conversation messages
messages = client.list_conversation_messages(conversation_id='conv-123')
print(f"Found {len(messages)} messages")

# List agents
agents = client.list_agents()
print(f"Found {len(agents)} agents")

# Search users
users = client.search_user(query='john')
print(f"Found {len(users)} users")

# Update a user
updated = client.update_user(user_id='user-123', data={'first_name': 'Jane'})
print(f"Updated user: {updated}")

# Get a report
report = client.get_report(report_id='report-123')
print(f"Report: {report}")
```

## API Methods

- `create_user(user_data)` - Create a new user
- `update_user(user_id, data)` - Update a user
- `create_conversation(conversation_data)` - Create a conversation
- `send_message_to_conversation(conversation_id, message)` - Send a message
- `list_conversation_messages(conversation_id, limit)` - List messages
- `list_agents()` - List all agents
- `search_user(query)` - Search users
- `get_report(report_id)` - Get a report
- `generate_raw_data_report(report_config)` - Generate a report
- `download_report_file(report_id)` - Download a report file