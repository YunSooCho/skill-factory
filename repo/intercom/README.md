# Intercom

Intercom is a complete customer communication platform for conversations, messaging, and support.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Intercom access token:

1. Sign up at [Intercom](https://www.intercom.com)
2. Go to Developer Hub > Authentication
3. Create a new access token

## Usage

```python
from intercom import IntercomClient

client = IntercomClient(access_token='your-access-token')

# Create a contact
contact = client.create_contact({
    'email': 'john@example.com',
    'name': 'John Doe'
})

# Create a conversation
conversation = client.create_conversation({
    'from': {'type': 'user', 'id': contact['id']},
    'body': 'Hello! I need help with my account'
})

# Reply to conversation
reply = client.reply_to_conversation(
    conversation_id='conv-123',
    message_type='comment',
    body='How can we help you today?'
)

# Send an event
client.send_event(
    event_name='viewed_pricing',
    user_id='user-123'
)

# List tickets
tickets = client.list_tickets(page=1)

# Create a ticket
ticket = client.create_ticket({
    'type': 'ticket',
    'title': 'Support Request',
    'contact_id': contact['id']
})

# Create an article
article = client.create_article({
    'title': 'How to use our product',
    'body': '...',
    'author_id': 'author-123'
})
```

## API Methods

### Contacts
- `create_contact(contact_data)` - Create a contact
- `get_contact(contact_id)` - Get contact details
- `update_contact(contact_id, data)` - Update a contact
- `delete_contact(contact_id)` - Delete a contact
- `list_contacts(**params)` - List contacts
- `search_contacts(query)` - Search contacts
- `tag_contact(contact_id, tag_ids)` - Tag a contact
- `untag_contact(contact_id, tag_id)` - Remove tag from contact
- `note_to_contact(contact_id, body)` - Add note to contact

### Conversations
- `create_conversation(conversation_data)` - Create a conversation
- `get_conversation(conversation_id)` - Get conversation
- `list_conversations(**params)` - List conversations
- `reply_to_conversation(conversation_id, message_type, body)` - Reply to conversation
- `assign_conversation(conversation_id, assignee_id)` - Assign conversation
- `get_conversation_last_message(conversation_id)` - Get last message

### Tickets
- `create_ticket(ticket_data)` - Create a ticket
- `get_ticket(ticket_id)` - Get ticket
- `update_ticket(ticket_id, data)` - Update ticket
- `list_tickets(**params)` - List tickets
- `create_ticket_type(data)` - Create ticket type

### Companies
- `create_or_update_company(data)` - Create or update company
- `get_company(company_id)` - Get company
- `search_companies(query)` - Search companies
- `tag_company(company_id, tag_ids)` - Tag a company

### Articles
- `create_article(article_data)` - Create an article
- `get_article(article_id)` - Get article
- `update_article(article_id, data)` - Update article
- `list_articles(**params)` - List articles
- `search_articles(query)` - Search articles

### Other
- `send_event(event_name, user_id, **kwargs)` - Send an event
- `create_message(message_data)` - Create a message
- `create_or_update_tag(name, **kwargs)` - Create or update tag
- `delete_tag(tag_id)` - Delete tag
- `list_admins()` - List admins
- `list_teams()` - List teams
- `import_data_source(url)` - Import data source
- `add_translated_article(article_id, translations)` - Add translation