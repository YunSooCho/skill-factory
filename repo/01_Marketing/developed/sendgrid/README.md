# SendGrid API Client

Python client for SendGrid API - email sending and contact management.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

```python
from client import SendGridClient

client = SendGridClient(api_key="your-api-key")
```

## API Actions

### Send Email

```python
result = client.send_email(
    from_email="sender@example.com",
    to_emails=["recipient@example.com"],
    subject="Test Email",
    content="Hello from SendGrid!",
    content_type="text/plain"
)
```

### Send Email with Attachment

```python
attachments = [
    {
        "filename": "document.pdf",
        "content_type": "application/pdf",
        "content": "base64_encoded_content"
    }
]

result = client.send_email_with_attachment(
    from_email="sender@example.com",
    to_emails=["recipient@example.com"],
    subject="Email with Attachment",
    content="Please find attached document",
    attachments=attachments
)
```

### Create Contact List

```python
result = client.create_contact_list("Newsletter Subscribers")
list_id = result['id']
```

### Add Contact to List

```python
result = client.add_contact_to_list(
    list_id="list123",
    email="john@example.com",
    first_name="John",
    last_name="Doe",
    custom_fields={"interest": "technology"}
)
```

### Search Contact

```python
result = client.search_contact("john@example.com")
```

### Delete Contact

```python
result = client.delete_contact("john@example.com")
```

### Get Bounce List

```python
result = client.get_bounce_list(
    start_time="2024-01-01T00:00:00Z",
    end_time="2024-12-31T23:59:59Z"
)
```

## License

MIT License
