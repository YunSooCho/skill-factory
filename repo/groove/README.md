# Groove

Groove is a customer support platform for managing tickets and customer communications.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Groove API token:

1. Sign up at [Groove](https://www.groovehq.com)
2. Go to Settings > Integrations > API
3. Generate and copy your API token

## Usage

```python
from groove import GrooveClient

client = GrooveClient(api_token='your-api-token')

# Create a ticket
ticket = client.create_ticket({
    'summary': 'Support request',
    'body': 'I need help with my account'
})

# Get ticket details
ticket = client.get_ticket(ticket_id='ticket-123')

# Update ticket state
client.update_ticket_state(ticket_id='ticket-123', state='closed')

# Create a message on a ticket
message = client.create_message(
    ticket_id='ticket-123',
    message_data={'body': 'Thank you for contacting us!'}
)

# Search tickets
tickets = client.search_ticket(query='support')
```

## API Methods

- `create_ticket(ticket_data)` - Create a ticket
- `get_ticket(ticket_id)` - Get ticket details
- `update_ticket_state(ticket_id, state)` - Update ticket state
- `search_ticket(q)` - Search tickets
- `create_message(ticket_id, message_data)` - Add message to ticket
- `get_customer(customer_id)` - Get customer details