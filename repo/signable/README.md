# Signable API Integration

## Overview
Complete Signable electronic signature API client for Yoom automation. Supports document management, signature envelopes, templates, branding, and webhooks.

## Supported Features
- ✅ Upload and manage PDF documents
- ✅ Create and send signature envelopes
- ✅ Manage recipients and signature workflows
- ✅ Envelope status tracking
- ✅ Template management and reuse
- ✅ Reminder and cancellation workflows
- ✅ Webhook integration for event notifications
- ✅ Account branding configuration
- ✅ Usage analytics and statistics

## Setup

### 1. Get API Credentials
Visit https://app.signable.co.uk/api/ to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
export SIGNABLE_API_KEY="your_api_key_here"
export SIGNABLE_BASE_URL="https://api.signable.co.uk"  # optional
```

## Usage

### Basic Example
```python
import os
from signable_client import SignableAPIClient

# Configure
os.environ['SIGNABLE_API_KEY'] = 'your_api_key'

client = SignableAPIClient()

# Upload document
result = client.upload_document('contract.pdf')
document_id = result['id']

# Create envelope
envelope = client.create_envelope(
    document_ids=[document_id],
    recipients=[
        {'email': 'client@example.com', 'name': 'John Doe'}
    ],
    title='Service Agreement'
)

# Send for signature
client.send_envelope(envelope['id'])

# Check status
status = client.get_envelope(envelope['id'])
print(f"Status: {status['status']}")

client.close()
```

### Template and Webhooks
```python
# Create envelope from template
envelope = client.create_envelope_from_template(
    template_id='tpl_abc123',
    recipients=[
        {'email': 'signer@example.com', 'name': 'Jane Smith'}
    ]
)

# Setup webhooks
client.create_webhook(
    url='https://your-app.com/webhooks/signable',
    events=['envelope.completed', 'document.signed']
)
```

### List and Filter
```python
# List all completed envelopes
envelopes = client.list_envelopes(status='completed')

# Get usage statistics
usage = client.get_usage_stats(
    start_date='2024-01-01',
    end_date='2024-12-31'
)
```

## Integration Type
- **Type:** API Key (Bearer Token)
- **Authentication:** Bearer token in Authorization header
- **Protocol:** HTTPS REST API

## Testability
- ✅ All API actions are testable with valid documents
- ✅ Sandbox environment available
- ✅ Free tier for development testing

## Notes
- Only PDF files are supported for upload
- Envelopes can contain multiple documents
- Webhooks receive real-time status updates
- Rate limits apply based on account plan