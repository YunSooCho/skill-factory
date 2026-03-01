# NoCRM.io API Client

Python client library for NoCRM.io API - Lead management and CRM system focused on sales teams.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

You need an API key from NoCRM.io. Initialize the client with your API key:

```python
from nocrm_io_client import NoCRMClient

client = NoCRMClient(api_key="your_api_key_here")
```

## Usage Examples

### Create a Lead

```python
result = client.create_lead(
    title="New Enterprise Opportunity",
    description="Large software deal with Acme Corp",
    status="todo",
    contact_name="John Doe",
    contact_email="john@example.com",
    contact_phone="+1234567890",
    company="Acme Corp.",
    amount=250000.0,
    tags=["enterprise", "high-value"]
)
```

### Get Lead Details

```python
lead = client.retrieve_lead(lead_id="lead_123")
```

### Update a Lead

```python
result = client.update_lead(
    lead_id="lead_123",
    status="won",
    amount=300000.0,
    tags={"enterprise", "high-value", "closed"}
)
```

### Search Leads

```python
leads = client.search_leads(
    query="enterprise",
    status="todo",
    company="Acme",
    tags=["priority"],
    limit=50
)
```

### Delete a Lead

```python
result = client.delete_lead(lead_id="lead_123")
```

### Add Comment to Lead

```python
result = client.add_comment_to_lead(
    lead_id="lead_123",
    comment="Client agreed to the terms, ready to close."
)
```

### Add Attachment to Lead

```python
result = client.add_attachment_to_lead(
    lead_id="lead_123",
    file_name="proposal.pdf",
    file_url="https://example.com/files/proposal.pdf",
    file_type="pdf"
)
```

### Create Category

```python
result = client.create_category(
    name="Enterprise Deals",
    description="Large enterprise customer deals"
)
```

### Create Predefined Tag

```python
result = client.create_predefined_tag(
    name="High-Priority",
    color="#FF0000"
)
```

### Create User

```python
result = client.create_user(
    email="newuser@example.com",
    first_name="Jane",
    last_name="Smith",
    role="user"
)
```

### Get User Details

```python
user = client.retrieve_user(user_id="user_123")
```

### Search Users

```python
users = client.search_users(
    query="Jane",
    role="sales",
    limit=50
)
```

## Webhook Handling

```python
# Verify webhook signature
is_valid = client.verify_webhook_signature(
    payload=request_body,
    signature=request.headers.get("X-Webhook-Signature"),
    webhook_secret="your_webhook_secret"
)

# Handle webhook event
data = client.handle_webhook(payload)
```

## API Actions

### Lead Management
- Create Lead
- Retrieve Lead
- Update Lead
- Delete Lead
- Search Leads
- Add Comment to Lead
- Add Attachment to Lead

### Organization
- Create Category
- Create Predefined Tag

### User Management
- Create User
- Retrieve User
- Search Users

## Triggers

- Lead Status Changed (General)
- Lead Status Changed to ToDo
- Lead Status Changed to Won
- Lead Status Changed to Lost
- Lead Status Changed to Cancelled
- Lead Status Changed to Standby
- New Comment
- New Lead

## Error Handling

```python
from nocrm_io_client import NoCRMClient, NoCRMAPIError

try:
    lead = client.retrieve_lead(lead_id="invalid_id")
except NoCRMAPIError as e:
    print(f"Error: {e}")
```

## Notes

- API uses Token authentication
- Lead statuses: todo, won, lost, standby, cancelled
- All monetary values should be in float format
- Webhook signature verification uses HMAC-SHA256
- Tags support for categorization and filtering