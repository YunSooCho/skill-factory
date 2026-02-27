# Elastic Email API Integration

## Overview
Implementation of Elastic Email email marketing and transactional email API for Yoom automation.

## Supported Features

### API Actions (9 operations)
- ✅ Contact: Add, Get, Get by email, Update, Delete, List
- ✅ List: Add, Get, Get all, Update
- ❌ Delete List (skipped)

### Triggers
- No triggers supported

## Setup

### 1. Get API Credentials
1. Visit https://elasticemail.com/ and sign up
2. Go to Settings > API Keys
3. Create a new API Key
4. Copy your API key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_key = "your_api_key"
```

## Usage

### Basic Example
```python
import asyncio
from elastic_email_client import ElasticEmailClient

async def main():
    api_key = "your_api_key"

    async with ElasticEmailClient(api_key=api_key) as client:
        # Create a list
        mailing_list = await client.add_list(
            name="Newsletter Subscribers"
        )

        # Add contact
        contact = await client.add_contact(
            email="john@example.com",
            list_ids=[mailing_list.id]
        )
        print(f"Contact: {contact.email}")
```

### Contact Management
```python
# Add contact with details
contact = await client.add_contact(
    email="jane@example.com",
    list_ids=["list_1", "list_2"],
    first_name="Jane",
    last_name="Doe",
    status="active",
    custom_fields={"source": "website", "country": "US"}
)

# Get contact by ID
contact = await client.get_contact(contact.id)

# Get contact by email
contact = await client.get_contact_by_email("john@example.com")

# Update contact
contact = await client.update_contact(
    contact_id=contact.id,
    first_name="Janet",
    status="inactive",
    list_ids=["list_3"]
)

# Delete contact
await client.delete_contact(contact.id)
```

### List Management
```python
# Create list
mailing_list = await client.add_list(
    name="Newsletter",
    description="Weekly newsletter subscribers"
)

# Get list by ID
mailing_list = await client.get_list(list_id="123")

# Get all lists
lists = await client.get_lists()
for lst in lists:
    print(f"{lst.name}: {lst.subscriber_count} subscribers")

# Update list
mailing_list = await client.update_list(
    list_id=mailing_list.id,
    name="Updated Newsletter Name",
    description="New description"
)
```

### Listing Contacts
```python
# List all contacts
contacts = await client.list_contacts(limit=50)

# List contacts in specific list
contacts = await client.list_contacts(
    list_id="list_123",
    limit=100
)

# List with pagination
contacts = await client.list_contacts(
    offset=100,
    limit=50
)
```

## Integration Type
- **Type:** API Key (Header-based)
- **Authentication:** `X-ElasticEmail-ApiKey` header
- **Protocol:** HTTPS REST API v4

## Testability
- ✅ All API actions testable with valid credentials
- ❌ No webhook triggers available

## Status Values

Contact status can be:
- `active` - Active contact (default)
- `inactive` - Inactive contact
- `bounced` - Bounced contact
- `unsubscribed` - Unsubscribed

```python
contact = await client.add_contact(
    email="user@example.com",
    status="inactive"  # Set initial status
)
```

## Custom Fields

Elastic Email supports custom fields:
```python
contact = await client.add_contact(
    email="user@example.com",
    list_ids=["list_1"],
    custom_fields={
        "company": "Acme Corp",
        "job_title": "Developer",
        "city": "San Francisco",
        "signup_date": "2024-02-27"
    }
)
```

## Best Practices

### List Organization
```python
# Create segments using custom fields for better targeting
await client.add_contact(
    email="customer@example.com",
    list_ids=["customers"],
    custom_fields={"type": "customer", "tier": "premium"}
)
```

### Bulk Operations
```python
# Use list operations instead of individual updates when possible
await client.update_contact(
    contact_id=contact.id,
    list_ids=["segment_1", "segment_2", "segment_3"]
)
```

### Status Management
```python
# Always check and update status based on engagement
if contact.status == "bounced":
    # Handle bounced contacts differently
    pass
```

### Pagination
```python
# Handle pagination for large lists
limit = 100
offset = 0

while True:
    contacts = await client.list_contacts(
        limit=limit,
        offset=offset
    )
    if not contacts:
        break

    # Process contacts
    for contact in contacts:
        print(contact.email)

    offset += limit
```

## Notes

- Delete List operation is **skipped** as per service specification
- All operations are async and require `async/await` syntax
- API rate limits apply, implement appropriate retry logic for production use
- Contact IDs and List IDs are returned as strings for compatibility