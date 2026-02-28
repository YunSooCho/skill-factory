# Front

Front is a shared inbox platform for managing team communication and customer support.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Front API token:

1. Sign up at [Front](https://frontapp.com)
2. Go to Settings > API Settings
3. Generate and copy your API token

## Usage

```python
from front import FrontClient

# Initialize the client
client = FrontClient(api_token='your-api-token')

# Search conversations
conversations = client.search_conversations(q='support', limit=20)
print(f"Found conversations: {conversations}")

# Send a new message
message = client.send_new_message({
    'to': ['customer@example.com'],
    'subject': 'Hello from support',
    'body': 'Thank you for contacting us!'
})
print(f"Sent message: {message}")

# Send a reply
reply = client.send_reply(
    conversation_id='cnv_123',
    data={
        'body': 'Thanks for your message!',
        'author_id': 'user_456'
    }
)
print(f"Sent reply: {reply}")

# Create a contact
contact = client.create_contact({
    'name': 'John Doe',
    'email': 'john@example.com'
})
print(f"Created contact: {contact}")

# List inboxes
inboxes = client.list_inboxes()
print(f"Found {len(inboxes.get('_results', []))} inboxes")

# Add tags to conversation
result = client.add_tags_to_conversation(
    conversation_id='cnv_123',
    tag_ids=['tag_urgent']
)
print(f"Added tags: {result}")

# Add comment to conversation
comment = client.add_comment_to_conversation(
    conversation_id='cnv_123',
    body='Internal note: Follow up tomorrow'
)
print(f"Added comment: {comment}")

# Retrieve a message
message = client.retrieve_message(message_id='msg_123')
print(f"Message: {message}")
```

## API Methods

### Conversations
- `search_conversations(q, limit)` - Search conversations
- `send_new_message(data)` - Send a new message
- `send_reply(conversation_id, data)` - Send a reply
- `get_conversation_last_message(conversation_id)` - Get last message
- `add_tags_to_conversation(conversation_id, tag_ids)` - Add tags
- `add_comment_to_conversation(conversation_id, body)` - Add comment
- `list_conversation_messages(conversation_id, limit)` - List messages
- `create_discussion_conversation(data)` - Create discussion

### Contacts
- `create_contact(data)` - Create a contact
- `retrieve_contact(contact_id)` - Get contact
- `retrieve_contact_by_email(email)` - Get contact by email
- `update_contact(contact_id, data)` - Update contact
- `delete_contact(contact_id)` - Delete contact

### Messages
- `retrieve_message(message_id)` - Get message

### Other
- `add_links_to_conversation(conversation_id, data)` - Add links
- `create_draft_reply(conversation_id, data)` - Create draft
- `list_inboxes()` - List inboxes