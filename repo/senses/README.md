# Senses API Client

Python API client for Senses - Marketing automation platform.

[Official Site](https://senses.co.jp/) | [API Documentation](https://docs.senses.co.jp/)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

```python
from senses_client import SensesClient

# Initialize client with your API key
client = SensesClient(
    api_key="your_api_key"
)
```

Get API key from Senses dashboard settings.

## Usage

### Create Form

```python
# Create a new form
fields = [
    {"type": "text", "name": "name", "label": "Name", "required": True},
    {"type": "email", "name": "email", "label": "Email", "required": True},
    {"type": "tel", "name": "phone", "label": "Phone", "required": False}
]

response = client.create_form(
    name="Registration Form",
    fields=fields,
    success_message="Thank you for registering!",
    thank_you_url="https://example.com/thank-you"
)
print(response)
```

### Get Form

```python
# Get form details
response = client.get_form(form_id=123)
print(response)
```

### Update Form

```python
# Update form fields
response = client.update_form(
    form_id=123,
    fields=fields
)
print(response)
```

### Delete Form

```python
# Delete a form
response = client.delete_form(form_id=123)
print(response)
```

### Create Landing Page

```python
# Create a new landing page
html_content = """
<!DOCTYPE html>
<html>
<body>
    <h1>Welcome</h1>
    <p>Fill out our form</p>
</body>
</html>
"""

response = client.create_landing_page(
    name="Campaign Landing Page",
    content=html_content
)
print(response)
```

### Get Landing Page

```python
# Get landing page details
response = client.get_landing_page(page_id=456)
print(response)
```

### Create Campaign

```python
# Create a new campaign
response = client.create_campaign(
    name="Spring Campaign 2026",
    type="email",
    status="draft"
)
print(response)
```

### Get Campaign

```python
# Get campaign details
response = client.get_campaign(campaign_id=789)
print(response)
```

### Update Campaign

```python
# Update campaign status
response = client.update_campaign(
    campaign_id=789,
    status="active"
)
print(response)
```

### Create User

```python
# Create a new user
response = client.create_user(
    email="user@example.com",
    first_name="John",
    last_name="Doe",
    phone="+1234567890",
    custom_attributes={"company": "Example Inc."}
)
print(response)
```

### Get User

```python
# Get user details
response = client.get_user(user_id=101)
print(response)
```

### Update User

```python
# Update user information
response = client.update_user(
    user_id=101,
    phone="+0987654321"
)
print(response)
```

### Delete User

```python
# Delete a user
response = client.delete_user(user_id=101)
print(response)
```

### Create Email Template

```python
# Create an email template
response = client.create_email_template(
    name="Welcome Email",
    subject="Welcome to Our Service",
    html_content="<h1>Hello!</h1><p>Thank you for joining us!</p>",
    text_content="Hello! Thank you for joining us!"
)
print(response)
```

### Send Email

```python
# Send an email
response = client.send_email(
    to="recipient@example.com",
    subject="Your Subject",
    html_content="<h1>Hello</h1><p>This is a test email.</p>"
)
print(response)
```

### Create Segment

```python
# Create a segment based on criteria
criteria = {
    "field": "email",
    "operator": "contains",
    "value": "@example.com"
}

response = client.create_segment(
    name="Example Domain Users",
    criteria=criteria
)
print(response)
```

### Get Segment

```python
# Get segment details
response = client.get_segment(segment_id=202)
print(response)
```

### Create Workflow

```python
# Create a workflow
trigger = {
    "type": "form_submit",
    "form_id": 123
}

actions = [
    {"type": "send_email", "template_id": 1},
    {"type": "add_to_segment", "segment_id": 202}
]

response = client.create_workflow(
    name="Welcome Workflow",
    trigger=trigger,
    actions=actions
)
print(response)
```

### Get Workflow

```python
# Get workflow details
response = client.get_workflow(workflow_id=303)
print(response)
```

### Update Workflow

```python
# Update workflow
response = client.update_workflow(
    workflow_id=303,
    name="Updated Welcome Workflow",
    active=True
)
print(response)
```

### Trigger Workflow

```python
# Manually trigger a workflow
response = client.trigger_workflow(
    workflow_id=303,
    data={"email": "user@example.com", "name": "John Doe"}
)
print(response)
```

### Get Analytics

```python
# Get analytics data
response = client.get_analytics(
    type="email",
    start_date="2026-02-01",
    end_date="2026-02-28",
    filters={"campaign_id": 789}
)
print(response)
```

## API Actions Implemented

| Action | Method | Description |
|--------|--------|-------------|
| Create Form | `create_form()` | Create form |
| Get Form | `get_form()` | Get form details |
| Update Form | `update_form()` | Update form |
| Delete Form | `delete_form()` | Delete form |
| Create Landing Page | `create_landing_page()` | Create landing page |
| Get Landing Page | `get_landing_page()` | Get landing page details |
| Update Landing Page | `update_landing_page()` | Update landing page |
| Delete Landing Page | `delete_landing_page()` | Delete landing page |
| Create Campaign | `create_campaign()` | Create campaign |
| Get Campaign | `get_campaign()` | Get campaign details |
| Update Campaign | `update_campaign()` | Update campaign |
| Delete Campaign | `delete_campaign()` | Delete campaign |
| Create User | `create_user()` | Create user |
| Get User | `get_user()` | Get user details |
| Update User | `update_user()` | Update user |
| Delete User | `delete_user()` | Delete user |
| Create Email Template | `create_email_template()` | Create email template |
| Send Email | `send_email()` | Send email |
| Create Segment | `create_segment()` | Create segment |
| Get Segment | `get_segment()` | Get segment details |
| Update Segment | `update_segment()` | Update segment |
| Delete Segment | `delete_segment()` | Delete segment |
| Create Workflow | `create_workflow()` | Create workflow |
| Get Workflow | `get_workflow()` | Get workflow details |
| Update Workflow | `update_workflow()` | Update workflow |
| Delete Workflow | `delete_workflow()` | Delete workflow |
| Trigger Workflow | `trigger_workflow()` | Trigger workflow |
| Get Analytics | `get_analytics()` | Get analytics data |

## Response Format

```python
{
    "status": "success",
    "data": {
        "id": 123,
        "name": "Form Name",
        "fields": [...],
        // ... other fields
    },
    "status_code": 200
}
```

## Error Handling

```python
from senses_client import SensesAPIError

try:
    response = client.create_user(
        email="user@example.com",
        first_name="John",
        last_name="Doe"
    )
except SensesAPIError as e:
    print(f"Senses API Error: {e}")
```

## Rate Limiting

The client does not implement rate limiting. Your application should handle rate limit errors (HTTP 429) with appropriate backoff.

## Testing

```bash
python test_senses.py
```

**Note:** Tests require valid Senses credentials.

## Yoom Integration

This client implements comprehensive workflow automation for:
- Forms and landing page creation
- Campaign management
- User/segment management
- Email marketing
- Workflow automation
- Analytics

For detailed Yoom mapping, refer to the service specification.

## Notes

- Form types: text, email, tel, number, textarea, select, checkbox, radio, date
- Campaign types: email, sms, push
- Workflow triggers: form_submit, user_created, segment_added, time_based
- Analytics types: email, form, landing_page, campaign