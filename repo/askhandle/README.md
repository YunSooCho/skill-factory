# AskHandle Customer Support Integration

AskHandle is a customer support platform that helps manage customer inquiries, ticket tracking, and multi-channel support automation.

## Features

- Multi-channel ticket management
- Team collaboration tools
- Knowledge base integration
- Customer relationship tracking
- Automated workflows
- SLA management
- Analytics and reporting

## Installation

```bash
pip install -e .
```

## API Key Setup

1. Log in to your AskHandle account
2. Go to Settings > API & Integrations
3. Generate an API key
4. Store credentials securely

## Usage

```python
from askhandle import AskHandleClient

# Initialize client
client = AskHandleClient(api_key="your-api-key")

# Get tickets
tickets = client.get_tickets(status="open")
for ticket in tickets:
    print(f"#{ticket['id']}: {ticket['subject']} - {ticket['status']}")

# Create a ticket
ticket = client.create_ticket({
    "customer_id": "CUST123",
    "subject": "Unable to login",
    "description": "I'm getting an error when trying to login",
    "priority": "high",
    "channel": "email"
})

# Get ticket details
details = client.get_ticket(ticket['id'])

# Add comment
client.add_comment(
    ticket_id="TICKET123",
    message="Could you please provide more details about the error?",
    internal=False
)

# Add internal note
client.add_comment(
    ticket_id="TICKET123",
    message="This appears to be a known issue with SSO",
    internal=True
)

# Assign ticket
client.assign_ticket(
    ticket_id="TICKET123",
    assignee_id="AGENT456",
    comment="Assigning to technical support"
)

# Change status
client.change_status(
    ticket_id="TICKET123",
    status="in_progress",
    comment="Investigating the issue"
)

# Merge tickets
client.merge_tickets(
    target_ticket_id="TICKET123",
    source_ticket_ids=["TICKET456", "TICKET789"]
)

# Get customers
customers = client.get_customers(limit=100)

# Get customer details
customer = client.get_customer("CUST123")

# Create customer
new_customer = client.create_customer({
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890"
})

# Get customer tickets
customer_tickets = client.get_customer_tickets("CUST123")

# Get agents
agents = client.get_agents()

# Get queues
queues = client.get_queues()

# Get knowledge base articles
articles = client.get_articles(category="Getting Started")

# Create article
article = client.create_article({
    "title": "How to Reset Your Password",
    "content": "Follow these steps to reset...",
    "category": "Account Management",
    "tags": ["password", "account"]
})

# Get tags
tags = client.get_tags()

# Search
results = client.search("login error")

# Get statistics
stats = client.get_statistics(
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

## API Methods

### Ticket Management
- `get_tickets(status, assignee, priority, limit, offset)` - List tickets
- `get_ticket(ticket_id)` - Get ticket details
- `create_ticket(data)` - Create ticket
- `update_ticket(ticket_id, data)` - Update ticket
- `delete_ticket(ticket_id)` - Delete ticket

### Comments & Notes
- `add_comment(ticket_id, message, internal, author_id)` - Add comment
- `get_comments(ticket_id, limit)` - Get comments

### Ticket Actions
- `assign_ticket(ticket_id, assignee_id, comment)` - Assign ticket
- `change_status(ticket_id, status, comment)` - Change status
- `merge_tickets(target_ticket_id, source_ticket_ids)` - Merge tickets

### Customer Management
- `get_customers(email, limit, offset)` - List customers
- `get_customer(customer_id)` - Get customer details
- `create_customer(data)` - Create customer
- `update_customer(customer_id, data)` - Update customer
- `get_customer_tickets(customer_id, limit)` - Get customer's tickets

### Agent Management
- `get_agents()` - List agents
- `get_agent(agent_id)` - Get agent details

### Queue Management
- `get_queues()` - List ticket queues

### Knowledge Base
- `get_articles(category, limit, offset)` - List articles
- `get_article(article_id)` - Get article details
- `create_article(data)` - Create article

### Tags & Search
- `get_tags()` - List tags
- `search(query, limit)` - Search across content

### Statistics
- `get_statistics(start_date, end_date)` - Get support statistics

### Webhooks
- `create_ticket_from_webhook(data)` - Create ticket via webhook

## Ticket Status

- `new` - Recently created
- `open` - Currently being worked on
- `in_progress` - Agent actively working
- `pending` - Waiting for customer response
- `resolved` - Issue resolved
- `closed` - Ticket closed
- `cancelled` - Ticket cancelled

## Priority Levels

- `low` - Low priority
- `medium` - Medium priority
- `high` - High priority
- `urgent` - Urgent priority

## Channels

- `email` - Email support
- `chat` - Live chat
- `phone` - Phone support
- `web` - Web form
- `social` - Social media

## Error Handling

```python
try:
    ticket = client.create_ticket({
        "customer_id": "CUST123",
        "subject": "Issue",
        "description": "..."
    })
except requests.RequestException as e:
    print(f"Error creating ticket: {e}")
```

## Webhooks

AskHandle supports webhooks for real-time updates:
- New ticket created
- Ticket status changed
- New comment added
- Assignment changed

Configure webhooks in your AskHandle settings.

## Support

For API documentation, visit https://docs.askhandle.com/