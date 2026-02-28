# Helpwise

Helpwise is a shared inbox platform for managing team communications.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Helpwise API key:

1. Sign up at [Helpwise](https://helpwise.io)
2. Go to Settings > API Keys
3. Generate and copy your API key

## Usage

```python
from helpwise import HelpwiseClient

client = HelpwiseClient(api_key='your-api-key')

# Create a contact
contact = client.create_contact({
    'name': 'John Doe',
    'email': 'john@example.com'
})

# Search conversations
conversations = client.search_conversations(query='support')

# Get conversation details
conversation = client.get_conversation(conversation_id='conv-123')

# Apply tags to conversations
client.apply_tags_conversations(
    conversation_ids=['conv-1', 'conv-2'],
    tag='urgent'
)

# Remove tags from conversations
client.remove_tags_conversations(
    conversation_ids=['conv-1'],
    tag='urgent'
)

# Get overall report
report = client.get_overall_report()
```

## API Methods

- `create_contact(contact_data)` - Create a contact
- `get_contact(contact_id)` - Get contact details
- `update_contact(contact_id, data)` - Update a contact
- `search_contact(query)` - Search contacts
- `search_conversations(query)` - Search conversations
- `get_conversation(conversation_id)` - Get conversation details
- `apply_tags_conversations(conversation_ids, tag)` - Apply tags
- `remove_tags_conversations(conversation_ids, tag)` - Remove tags
- `get_overall_report()` - Get overall report