# Signtime API Integration

## Overview
Complete Signtime electronic signature API client for Yoom automation. Supports document management, signature workflows, templates, webhooks, and account analytics.

## Supported Features
- ✅ Upload and manage documents
- ✅ Create and send signature requests
- ✅ Multi-signer workflows
- ✅ Template creation and reuse
- ✅ Signature request tracking
- ✅ Reminder and cancellation
- ✅ Webhook event notifications
- ✅ Account analytics and audit logs

## Setup

### 1. Get API Credentials
Visit https://signtime.com/developers to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
export SIGNTIME_API_KEY="your_api_key_here"
export SIGNTIME_BASE_URL="https://api.signtime.com/v1"  # optional
```

## Usage

### Basic Workflow
```python
import os
from signtime_client import SigntimeAPIClient

os.environ['SIGNTIME_API_KEY'] = 'your_api_key'

client = SigntimeAPIClient()

# Upload document
doc = client.upload_document('contract.pdf')
document_id = doc['id']

# Create signature request
request = client.create_signature_request(
    document_id=document_id,
    signers=[
        {'email': 'client@example.com', 'name': 'John Doe'},
        {'email': 'witness@example.com', 'name': 'Jane Smith'}
    ],
    message='Please sign this agreement',
    expiry_days=30
)

# Track status
status = client.get_signature_request(request['id'])
print(f"Status: {status['status']}")

client.close()
```

### Template Usage
```python
# Create template
template = client.create_template(
    document_path='nda-template.pdf',
    name='NDA Template',
    description='Non-disclosure agreement',
    signer_roles=[
        {'role': 'disclosing_party', 'label': 'Disclosing Party'},
        {'role': 'receiving_party', 'label': 'Receiving Party'}
    ]
)

# Use template
request = client.use_template(
    template_id=template['id'],
    signers=[
        {'role': 'disclosing_party', 'email': 'a@company.com', 'name': 'Alice'},
        {'role': 'receiving_party', 'email': 'b@company.com', 'name': 'Bob'}
    ]
)
```

### Webhooks and Analytics
```python
# Setup webhook
client.create_webhook(
    url='https://your-app.com/webhooks/signtime',
    events=['signature_request.completed', 'signature_request.cancelled']
)

# Get analytics
analytics = client.get_analytics(period='month')
print(f"Signatures this month: {analytics['total_signatures']}")

# Get audit log
audit = client.get_audit_log(limit=50)
```

## Integration Type
- **Type:** API Key (Bearer Token)
- **Authentication:** Bearer token in Authorization header
- **Protocol:** HTTPS REST API

## Testability
- ✅ All API actions are testable with valid documents
- ✅ Sandbox/test environment available
- ✅ Free trial for development testing

## Notes
- Supports PDF documents
- Multi-signer workflows with ordering
- Templates speed up repeat document types
- Webhooks provide real-time updates
- Audit logs available for compliance