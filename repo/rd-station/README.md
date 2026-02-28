# RD Station API Client

Python client for [RD Station](https://www.rdstation.com/) Marketing Automation API.

## Features

- ✅ Contact management (create, read, update, delete)
- ✅ Event tracking (conversion, call, closing, abandonment, chat)
- ✅ Tag management for leads
- ✅ Comprehensive error handling
- ✅ Rate limiting support (via session management)

## Installation

```bash
pip install -r requirements.txt
```

## Getting Started

### 1. Get API Credentials

1. Visit [RD Station Developers](https://developers.rdstation.com/)
2. Create an account or log in
3. Generate API tokens in your account settings
4. You'll need:
   - **Access Token**: For API authentication
   - **Refresh Token** (optional): For token renewal

### 2. Initialize the Client

```python
from rd_station.client import RDStationClient

# Initialize with your access token
client = RDStationClient(
    access_token="your_access_token_here",
    refresh_token="your_refresh_token_here"  # optional
)
```

## Usage Examples

### Contact Operations

```python
# Create a new contact
contact = client.create_contact(
    email="john.doe@example.com",
    name="John Doe",
    job_title="Marketing Manager",
    phone="+1234567890",
    website="https://example.com"
)
print(contact)

# Get contact information
contact_info = client.get_contact(email="john.doe@example.com")
print(contact_info)

# Update contact
updated = client.update_contact(
    email="john.doe@example.com",
    name="John Updated",
    company="New Company"
)
print(updated)

# Delete contact
result = client.delete_contact(email="john.doe@example.com")
print(result)
```

### Event Tracking

```python
# Create conversion event
conversion = client.create_default_conversion_event(
    email="user@example.com",
    event_value=99.99,
    name="Purchase",
    funnel_name="Main Sales Funnel"
)
print(conversion)

# Create call event
call_event = client.create_call_event(
    email="lead@example.com",
    call_status="completed",
    notes="Very interested in our product",
    duration_minutes=15
)
print(call_event)

# Create closing/won deal event
closing_event = client.create_closing_event(
    email="customer@example.com",
    deal_value=5000.00,
    deal_status="won",
    deal_name="Enterprise Plan"
)
print(closing_event)

# Create abandonment event
abandonment = client.create_abandonment_event(
    email="cart_user@example.com",
    abandoned_resource="cart",
    items_count=3,
    total_value=149.97
)
print(abandonment)

# Create chat starter event
chat = client.create_chat_starter_event(
    email="visitor@example.com",
    chat_channel="website_chat",
    message="I have a question about pricing"
)
print(chat)
```

### Tag Management

```python
# Add tag to lead
result = client.add_tag_to_lead(
    email="lead@example.com",
    tag="High Priority"
)
print(result)
```

## API Reference

### Contact Methods

- `create_contact(email, **kwargs)` - Create a new contact
- `get_contact(email)` - Get contact by email
- `get_contact_information(email)` - Get detailed contact info
- `update_contact(email, **kwargs)` - Update contact data
- `update_contact_information(email, **kwargs)` - Update contact info (alias)
- `delete_contact(email)` - Delete a contact

### Event Methods

- `create_event(event_type, email=None, **kwargs)` - Create a custom event
- `create_default_conversion_event(email, event_value=None, **kwargs)` - Create conversion event
- `create_call_event(email, call_status, notes=None, **kwargs)` - Create call event
- `create_closing_event(email, deal_value, deal_status, **kwargs)` - Create closing event
- `create_abandonment_event(email, abandoned_resource, **kwargs)` - Create abandonment event
- `create_chat_starter_event(email, chat_channel, message=None, **kwargs)` - Create chat starter event

### Tag Methods

- `add_tag_to_lead(email, tag)` - Add a tag to a lead

## Error Handling

The client includes comprehensive error handling:

```python
from rd_station.client import RDStationClient, RDStationAPIError

client = RDStationClient(
    access_token="your_token"
)

try:
    contact = client.create_contact(
        email="test@example.com",
        name="Test User"
    )
    print(contact)
except RDStationAPIError as e:
    print(f"API Error: {e}")
finally:
    client.close()
```

## Rate Limiting

The client uses `requests.Session` which automatically handles connection pooling and can be extended with rate limiting middleware if needed.

## Common Fields

### Contact Fields
- `email` (required): Contact's email address
- `name`: Full name
- `job_title`: Job title
- `company`: Company name
- `phone`: Phone number
- `website`: Website URL
- `personal_phone`: Personal phone
- `mobile`: Mobile phone
- `linkedin`: LinkedIn profile URL
- `twitter`: Twitter handle
- `facebook`: Facebook profile URL
- `bio`: Bio/description

### Event Fields
- `event_type`: Type of event
- `email`: Contact's email
- `event_family`: Event family (default: "CDP")
- `value`: Event value (for conversion/closing events)
- `name`: Event name
- `funnel_name`: Funnel name (for conversion events)

## Best Practices

1. **Always close the client**: Use `client.close()` or a context manager
2. **Handle exceptions**: Wrap API calls in try-except blocks
3. **Use meaningful event names**: Make events easy to filter and analyze
4. **Validate emails**: Ensure emails are valid before creating contacts
5. **Tag strategically**: Use tags for segmentation and targeting

## License

MIT License

## Support

For issues or questions:
- RD Station Developers: https://developers.rdstation.com/
- RD Station Help Center: https://ajuda.rdstation.com/