# Jitbit

Jitbit is a help desk platform for managing customer support tickets.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Jitbit API key:

1. Sign up at [Jitbit](https://www.jitbit.com)
2. Go to Settings > API
3. Generate and copy your API key and base URL

## Usage

```python
from jitbit import JitbitClient

client = JitbitClient(api_key='your-api-key', base_url='https://yourcompany.jitbit.com')

# Create a ticket
ticket = client.create_ticket({
    'Subject': 'Support Request',
    'Body': 'I need help with my account',
    'UserID': 123
})

# List tickets
tickets = client.list_tickets()

# Get ticket details
ticket = client.get_ticket(ticket_id='123')

# Search tickets
tickets = client.search_tickets(query='account')

# Create a user
user = client.create_user({
    'Username': 'john.doe',
    'FirstName': 'John',
    'LastName': 'Doe',
    'Email': 'john@example.com'
})

# Create a knowledge base article
article = client.create_kb_article({
    'Title': 'How to reset password',
    'Body': '...',
    'CategoryID': 1
})
```

## API Methods

- `create_ticket(ticket_data)` - Create a ticket
- `get_ticket(ticket_id)` - Get ticket details
- `list_tickets(**params)` - List tickets
- `search_tickets(query)` - Search tickets
- `attach_file_to_ticket(ticket_id, file_data)` - Attach file to ticket
- `create_user(user_data)` - Create a user
- `list_users()` - List users
- `create_kb_article(article_data)` - Create KB article