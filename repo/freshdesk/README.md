# Freshdesk

Freshdesk is a complete customer support platform for managing tickets and customer interactions.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Freshdesk API key:

1. Sign up at [Freshdesk](https://www.freshdesk.com)
2. Go to your profile > API Key Settings
3. Copy your API key

## Usage

```python
from freshdesk import FreshdeskClient

# Initialize the client
client = FreshdeskClient(domain='yourcompany.freshdesk.com', api_key='your-api-key')

# Create a ticket
ticket = client.create_ticket({
    'subject': 'Issue with my order',
    'description': 'My order has not been delivered yet',
    'email': 'customer@example.com',
    'priority': 2,
    'status': 2
})
print(f"Created ticket: {ticket}")

# Get a ticket
ticket = client.get_ticket(ticket_id=12345)
print(f"Ticket: {ticket}")

# Update a ticket
updated = client.update_ticket(ticket_id=12345, data={'status': 4, 'priority': 3})
print(f"Updated ticket: {updated}")

# Create a contact
contact = client.create_contact({
    'name': 'John Doe',
    'email': 'john@example.com'
})
print(f"Created contact: {contact}")

# Search contacts
contacts = client.search_contacts(query='John')
print(f"Found {len(contacts)} contacts")

# Reply to a ticket
reply = client.reply_to_ticket(
    ticket_id=12345,
    body='Thank you for contacting us. We are looking into this.'
)
print(f"Replied: {reply}")

# Add a note to a ticket
note = client.add_note_to_ticket(
    ticket_id=12345,
    note='Internal note: Customer is waiting for update'
)
print(f"Added note: {note}")

# List ticket conversations
conversations = client.list_ticket_conversations(ticket_id=12345)
print(f"Found {len(conversations)} conversations")

# Create a company
company = client.create_company({'name': 'Acme Corp'})
print(f"Created company: {company}")
```

## API Methods

### Tickets
- `create_ticket(ticket_data)` - Create a new ticket
- `get_ticket(ticket_id)` - Get a ticket by ID
- `update_ticket(ticket_id, data)` - Update a ticket
- `delete_ticket(ticket_id)` - Delete a ticket
- `reply_to_ticket(ticket_id, body, **kwargs)` - Reply to a ticket
- `add_note_to_ticket(ticket_id, note, **kwargs)` - Add a note to a ticket
- `list_ticket_conversations(ticket_id)` - List ticket conversations
- `get_latest_ticket_conversation(ticket_id)` - Get latest conversation

### Contacts
- `create_contact(contact_data)` - Create a contact
- `get_contact(contact_id)` - Get a contact by ID
- `update_contact(contact_id, data)` - Update a contact
- `delete_contact(contact_id)` - Delete a contact
- `search_contacts(query)` - Search contacts

### Companies
- `create_company(data)` - Create a company
- `get_company(company_id)` - Get a company by ID
- `update_company(company_id, data)` - Update a company
- `delete_company(company_id)` - Delete a company
- `search_companies(query)` - Search companies