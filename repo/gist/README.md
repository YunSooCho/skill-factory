# Gist

Gist is a customer engagement platform for managing contacts and campaigns.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Gist API key:

1. Sign up at [Gist](https://www.gist.com)
2. Go to Settings > API Keys
3. Generate and copy your API key

## Usage

```python
from gist import GistClient

# Initialize the client
client = GistClient(api_key='your-api-key')

# Create or update a contact
contact = client.create_or_update_contact({
    'email': 'john@example.com',
    'first_name': 'John',
    'last_name': 'Doe'
})
print(f"Contact: {contact}")

# Search contacts
contacts = client.search_contact(query='john')
print(f"Found {len(contacts)} contacts")

# Get a specific contact
contact = client.get_contact(contact_id='contact-123')
print(f"Contact: {contact}")

# Tag contacts
result = client.tag_contacts(tag='VIP', contact_ids=['contact-1', 'contact-2'])
print(f"Tagged contacts: {result}")

# Remove tag from contacts
result = client.remove_tag_from_contacts(tag='VIP', contact_ids=['contact-1'])
print(f"Removed tag: {result}")

# Subscribe contact to campaign
result = client.subscribe_contact_to_campaign(
    contact_id='contact-123',
    campaign_id='campaign-456'
)
print(f"Subscribed: {result}")

# Unsubscribe contact from campaign
result = client.unsubscribe_contact_from_campaign(
    contact_id='contact-123',
    campaign_id='campaign-456'
)
print(f"Unsubscribed: {result}")

# Delete contact
result = client.delete_contact(contact_id='contact-123')
print(f"Deleted: {result}")
```

## API Methods

- `create_or_update_contact(contact_data)` - Create or update a contact
- `get_contact(contact_id)` - Get a specific contact
- `search_contact(query)` - Search contacts
- `delete_contact(contact_id)` - Delete a contact
- `tag_contacts(tag, contact_ids)` - Tag multiple contacts
- `remove_tag_from_contacts(tag, contact_ids)` - Remove a tag from contacts
- `subscribe_contact_to_campaign(contact_id, campaign_id)` - Subscribe to campaign
- `unsubscribe_contact_from_campaign(contact_id, campaign_id)` - Unsubscribe from campaign