# Whatsable Message API

Whatsable Message API integration for WhatsApp messaging.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from whatsable_message import WhatsableMessageClient

client = WhatsableMessageClient(api_key="your_api_key")

# Send text message
result = client.send_message(
    phone_number="+1234567890",
    message="Hello from Whatsable!",
    message_type="text"
)

# Send image
result = client.send_message(
    phone_number="+1234567890",
    message_type="image",
    media_url="https://example.com/image.jpg"
)

# Send bulk messages
bulk_messages = [
    {"phone_number": "+1234567890", "type": "text", "content": "Message 1"},
    {"phone_number": "+0987654321", "type": "text", "content": "Message 2"}
]
result = client.send_bulk_messages(bulk_messages)
```

## Features

- Send text, image, video, document messages
- Send bulk messages
- Check message status
- Get account balance
- List messages
- Cancel scheduled messages

## API Reference

- `send_message(phone_number, message, message_type, media_url)` - Send message
- `send_bulk_messages(messages)` - Send bulk
- `get_message_status(message_id)` - Get status
- `get_account_balance()` - Get balance
- `get_account_info()` - Get account info
- `list_messages(date_from, date_to, limit)` - List messages
- `cancel_message(message_id)` - Cancel message

## Authentication

Requires Whatsable Message API Key.