# Wan-Sign API Integration

## Overview
Complete Wan-Sign electronic signature API client for Yoom automation. Supports documents, signature requests, templates, webhooks, and team management.

## Supported Features
- ✅ Document upload and management
- ✅ Create and track signature requests
- ✅ Multi-recipient signing workflows
- ✅ Template-based signature requests
- ✅ Reminder system
- ✅ Signed document download
- ✅ Team member management
- ✅ Webhook notifications
- ✅ Usage statistics

## Setup

### 1. Get API Credentials
Visit https://developer.wansign.com to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export WAN_SIGN_API_KEY="your_api_key_here"
```

## Usage

```python
import os
from wan_sign_client import WanSignAPIClient

os.environ['WAN_SIGN_API_KEY'] = 'your_api_key'

client = WanSignAPIClient()

# Upload document
doc = client.upload_document('contract.pdf')

# Create signature request
request = client.create_signature_request(
    document_id=doc['id'],
    recipients=[
        {'email': 'client@example.com', 'name': 'John Doe'}
    ],
    subject='Please sign agreement'
)

# Track status
status = client.get_signature_request(request['id'])

# Use template
template_request = client.create_from_template(
    template_id='tpl_123',
    recipients=[{'email': 'signer@example.com', 'name': 'Signer'}]
)

client.close()
```