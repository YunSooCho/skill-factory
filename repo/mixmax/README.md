# Mixmax API Integration

## Overview
Implementation of Mixmax email sequences and messaging API for Yoom automation.

## Supported Features
- ✅ Cancel Active Sequence Recipients
- ✅ Add Recipients to Sequence
- ✅ Send Message
- ✅ Get Message
- ✅ Create Email Draft
- ✅ Get Recipient Sequence
- ✅ List Messages
- ✅ Search Sequence

## Setup

### Get API Key
Visit https://mixmax.com/ and obtain your API key from account settings.

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure
```python
from mixmax_client import MixmaxClient, Message, EmailDraft

api_key = "your_mixmax_api_key"

async with MixmaxClient(api_key=api_key) as client:
    # Use the client
    pass
```

## Usage

```python
# Send message
message = Message(
    to=["recipient@example.com"],
    subject="Test Subject",
    body="Message body"
)
sent = await client.send_message(message)

# Create draft
draft = EmailDraft(
    to=["recipient@example.com"],
    subject="Draft Subject",
    body="Draft body"
)
created = await client.create_email_draft(draft)

# Sequence operations
await client.add_recipients_to_sequence(sequence_id, recipients)
```

## Notes
- Async operations with rate limiting
- Built-in retry logic
- Complete message and sequence management