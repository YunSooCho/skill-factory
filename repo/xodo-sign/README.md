# Xodo-Sign API Integration

## Overview
Complete Xodo-Sign electronic signature API client for Yoom automation. Supports PDF signing, document management, templates, contacts, and webhooks.

## Supported Features
- ✅ File upload and management
- ✅ Create and send signature requests
- ✅ Multi-signer workflows
- ✅ Template-based requests
- ✅ Contact management
- ✅ Reminder system
- ✅ Webhook integration
- ✅ Document tracking

## Setup

### 1. Get API Key
Visit https://xodosign.com/developers to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export XODO_SIGN_API_KEY="your_api_key_here"
```

## Usage

```python
import os
from xodo_sign_client import XodoSignAPIClient

os.environ['XODO_SIGN_API_KEY'] = 'your_api_key'

client = XodoSignAPIClient()

# Upload file
file = client.upload_file('document.pdf')

# Create signature request
request = client.create_signature_request(
    file_ids=[file['id']],
    signers=[
        {'email': 'signer@example.com', 'name': 'John Doe'}
    ]
)

# Check status
status = client.get_signature_request(request['id'])

client.close()
```