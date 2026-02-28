# Freshservice

Freshservice is an IT service management platform for managing IT tickets and assets.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Freshservice API key:

1. Sign up at [Freshservice](https://www.freshservice.com)
2. Go to your profile > API Key Settings
3. Copy your API key

## Usage

```python
from freshservice import FreshserviceClient

# Initialize the client
client = FreshserviceClient(domain='yourcompany.freshservice.com', api_key='your-api-key')

# Create a ticket
ticket = client.create_ticket({
    'subject': 'Laptop not working',
    'description': 'My laptop is not booting up',
    'requester_id': 123,
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

# Create a requester
requester = client.create_requester({
    'name': 'John Doe',
    'email': 'john@example.com'
})
print(f"Created requester: {requester}")

# Create a task
task = client.create_task({
    'title': 'Diagnose laptop issue',
    'ticket_id': 12345
})
print(f"Created task: {task}")

# List tasks
tasks = client.list_tasks(ticket_id=12345)
print(f"Found {len(tasks)} tasks")

# Create a time entry
time_entry = client.create_time_entry({
    'ticket_id': 12345,
    'agent_id': 456,
    'time_spent': '60',
    'note': 'Troubleshooting'
})
print(f"Created time entry: {time_entry}")

# Create a reply
reply = client.create_reply(
    ticket_id=12345,
    body='We are working on your issue.'
)
print(f"Created reply: {reply}")

# Search tickets
tickets = client.search_tickets(query='laptop')
print(f"Found {len(tickets)} tickets")
```

## API Methods

### Tickets
- `create_ticket(ticket_data)` - Create a new ticket
- `get_ticket(ticket_id)` - Get a ticket by ID
- `update_ticket(ticket_id, data)` - Update a ticket
- `delete_ticket(ticket_id)` - Delete a ticket
- `search_tickets(query)` - Search tickets
- `create_reply(ticket_id, body, **kwargs)` - Create a reply
- `list_conversations(ticket_id)` - List conversations
- `delete_conversation(conversation_id)` - Delete a conversation

### Requesters
- `create_requester(data)` - Create a requester
- `get_requester(requester_id)` - Get a requester
- `update_requester(requester_id, data)` - Update a requester
- `delete_requester(requester_id)` - Delete a requester
- `search_requesters(query)` - Search requesters

### Agents
- `create_agent(data)` - Create an agent
- `update_agent(agent_id, data)` - Update an agent
- `search_agents(query)` - Search agents

### Tasks
- `create_task(task_data)` - Create a task
- `get_task(task_id)` - Get a task
- `update_task(task_id, data)` - Update a task
- `delete_task(task_id)` - Delete a task
- `list_tasks(ticket_id)` - List tasks

### Time Entries
- `create_time_entry(entry_data)` - Create a time entry
- `get_time_entry(entry_id)` - Get a time entry
- `update_time_entry(entry_id, data)` - Update a time entry
- `delete_time_entry(entry_id)` - Delete a time entry
- `list_time_entries(ticket_id)` - List time entries