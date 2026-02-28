# Chatbot

Chatbot is a conversational AI platform for automating customer conversations.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Chatbot API key:

1. Sign up at [Chatbot.com](https://www.chatbot.com)
2. Go to Settings > API > Generate Token
3. Copy your API token

## Usage

```python
from chatbot import ChatbotClient

# Initialize the client
client = ChatbotClient(api_key='your-api-key')

# Create a user
user = client.create_user({
    'externalId': 'user-123',
    'attributes': {
        'name': 'John Doe',
        'email': 'john@example.com'
    }
})
print(f"Created user: {user}")

# List users
users = client.list_users()
print(f"Found {len(users)} users")

# Create a segment
segment = client.create_segment(
    name='VIP Customers',
    conditions=[{'type': 'attribute', 'name': 'is_vip', 'operator': 'equals', 'value': True}]
)
print(f"Created segment: {segment}")

# Add users to segment
result = client.add_users_to_segment(segment_id='seg-123', user_ids=['user-1', 'user-2'])
print(f"Added users to segment: {result}")

# Search conversations
conversations = client.search_conversations(query='support request')
print(f"Found {len(conversations)} conversations")

# List segments
segments = client.list_segments()
print(f"Found {len(segments)} segments")
```

## API Methods

- `create_user(user_data)` - Create a new user
- `list_users(limit)` - List all users
- `get_user(user_id)` - Get a specific user
- `update_user(user_id, data)` - Update a user
- `delete_user(user_id)` - Delete a user
- `create_entity(data)` - Create an entity
- `list_entities(limit)` - List all entities
- `get_entity(entity_id)` - Get a specific entity
- `update_entity(entity_id, data)` - Update an entity
- `delete_entity(entity_id)` - Delete an entity
- `create_segment(name, conditions)` - Create a new segment
- `list_segments(limit)` - List all segments
- `update_segment(segment_id, data)` - Update a segment
- `delete_segment(segment_id)` - Delete a segment
- `add_users_to_segment(segment_id, user_ids)` - Add users to segment
- `search_conversations(query, limit)` - Search conversations