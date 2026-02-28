# Yousign API Integration

## Overview
Complete Yousign electronic signature API client for Yoom automation. Supports AES/eIDAS compliant signatures, advanced workflows, and compliance features.

## Supported Features
- ✅ File upload and management
- ✅ Advanced signature request workflows
- ✅ Multi-signer supports with ordering
- ❁ SMS and email delivery modes
- ✅ Audit trail and compliance documents
- ✅ Procedure-based workflows
- ✅ User and team management
- ✅ Webhook integrations
- ✅ Brand customization
- ✅ Usage statistics and quotas

## Setup

### 1. Get API Credentials
Visit https://developer.yousign.com to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export YOUSIGN_API_KEY="your_api_key_here"
export YOUSIGN_BASE_URL="https://api.yousign.com/v3"  # optional
```

## Usage

### Basic Signature Request
```python
import os
from yousign_client import YousignAPIClient

os.environ['YOUSIGN_API_KEY'] = 'your_api_key'

client = YousignAPIClient()

# Upload file
file_response = client.upload_file('contract.pdf')
file_id = file_response['id']

# Create signature request
request = client.create_signature_request(
    name='Service Agreement',
    signers=[
        {
            'info': {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com'
            },
            'signature_level': 'electronic_signature'
        }
    ]
)

# Add document to request
client.add_document_to_request(request['id'], file_id)

# Activate request
client.activate_signature_request(request['id'])

client.close()
```

### Advanced Workflow
```python
# Create with SMS delivery
request = client.create_signature_request(
    name='High-Security Agreement',
    signers=[
        {
            'info': {'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com'},
            'signature_level': 'qualified_electronic_signature'
        }
    ],
    delivery_mode='sms'
)

# Get audit trail
audit = client.download_audit_trail(request['id'])

# Download completed documents in ZIP
completed = client.download_completed_documents(request['id'])
```

### Webhooks and Monitoring
```python
# Create webhook
client.create_webhook(
    url='https://your-app.com/webhooks/yousign',
    events=['procedure.finished', 'procedure.started']
)

# Check usage
quota = client.get_connection_quota()
stats = client.get_usage_stats()
```

## Integration Type
- **Type:** API Key (Bearer Token)
- **Authentication:** Bearer token in Authorization header
- **Protocol:** HTTPS REST API

## Testability
- ✅ Sandbox environment available
- ✅ All API actions testable
- ✅ Free trial for development

## Notes
- Supports AES, eIDAS compliant signatures
- Advanced authentication levels available
- SMS verification for high-security signatures
- Full audit trail for compliance
- Multi-language support available