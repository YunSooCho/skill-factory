# Relation

Relation is a Japanese customer support platform for managing tickets and customer information.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Relation API key:

1. Sign up at [Relation](https://www.relation.jp)
2. Go to Settings > API
3. Generate and copy your API key

## Usage

```python
from relation import RelationClient

client = RelationClient(api_key='your-api-key')

# Register a customer in address book
customer = client.register_address_customer({
    'name': '山田太郎',
    'email': 'yamada@example.com',
    'phone': '03-1234-5678'
})

# Search customers
customers = client.search_address_customers(query='山田')

# Update customer
client.update_address_customer(
    customer_id='customer-123',
    data={'email': 'new@example.com'}
)

# Delete customer
client.delete_address_customer(customer_id='customer-123')

# Create a ticket from memo
ticket = client.create_ticket_from_memo(
    memo='Customer needs help with their account',
    customer_id='customer-123'
)

# Get ticket details
ticket = client.get_ticket_details(ticket_id='ticket-456')

# Update ticket status
client.update_ticket_status(
    ticket_id='ticket-456',
    status='in_progress'
)

# Add memo to ticket
client.add_memo_to_ticket(
    ticket_id='ticket-456',
    memo='Follow up scheduled for tomorrow'
)

# List tickets by status
tickets = client.list_tickets_by_status(status='open')
```

## API Methods

### Address Book (Customers)
- `register_address_customer(customer_data)` - Register a customer
- `update_address_customer(customer_id, data)` - Update customer
- `delete_address_customer(customer_id)` - Delete customer
- `search_address_customers(query)` - Search customers

### Tickets
- `create_ticket_from_memo(memo, **kwargs)` - Create ticket from memo
- `get_ticket_details(ticket_id)` - Get ticket details
- `update_ticket_status(ticket_id, status)` - Update ticket status
- `add_memo_to_ticket(ticket_id, memo)` - Add memo to ticket
- `list_tickets_by_status(status)` - List tickets by status