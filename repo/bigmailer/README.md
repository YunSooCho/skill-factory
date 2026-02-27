# Big Mailer API Integration

## Overview
Big Mailer API for contact management and email marketing. Full CRUD support for contacts and custom fields.

## Supported Features
- ✅ List Contacts - Get all contacts with pagination
- ✅ Create Contact - Add new contacts
- ✅ Get Contact - Retrieve specific contact
- ✅ Update Contact - Modify contact details
- ✅ Delete Contact - Remove contacts
- ✅ List Fields - Get all custom fields

## Setup

### 1. Get API Key
1. Sign up at [Big Mailer](https://www.bigmailer.io/)
2. Go to Settings → API
3. Generate your API key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_key = "your_api_key"
```

## Usage

```python
from bigmailer_client import BigMailerClient

client = BigMailerClient(api_key="your_key")

# Create contact
contact = client.create_contact(
    email="user@example.com",
    first_name="John",
    last_name="Doe",
    company="Acme Inc"
)

# List contacts
contacts = client.list_contacts(limit=20)

# Update with custom fields
client.update_contact(
    contact.id,
    custom_fields={"location": "Tokyo", "plan": "Premium"}
)

# List custom fields
fields = client.list_fields()
for field in fields:
    print(f"{field.name} ({field.type})")

client.close()
```

## Integration Type
- **Type:** API Key
- **Authentication:** X-API-Key header
- **Protocol:** HTTPS REST API

## Testability
- ✅ All operations testable with valid API key