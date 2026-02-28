# Whapi API

Whapi API integration for WhatsApp messaging.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from whapi import WhapiClient

client = WhapiClient(api_token="your_api_token")

# Send message
result = client.send_message(
    phone_number="+1234567890",
    message="Hello from Whapi!"
)

# Send template
result = client.send_template(
    phone_number="+1234567890",
    template_name="welcome",
    template_params={"name": "John"}
)

# Send file
result = client.send_file(
    phone_number="+1234567890",
    file_url="https://example.com/file.pdf",
    file_type="document"
)
```

## Features

- Send text messages
- Send template messages
- Send files (image, video, document, audio)
- Check message status
- List messages
- Webhook management

## API Reference

- `send_message(phone_number, message, preview_url)` - Send text
- `send_template(phone_number, template_name, template_params)` - Send template
- `send_file(phone_number, file_url, file_type, caption)` - Send file
- `get_message_status(message_id)` - Get status
- `list_messages(limit, skip)` - List messages
- `set_webhook(webhook_url, webhook_events)` - Set webhook
- `delete_webhook()` - Delete webhook

## Authentication

Requires Whapi API Token.