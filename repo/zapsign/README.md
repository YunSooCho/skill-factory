# Zapsign API Integration

## Overview
Complete Zapsign electronic signature API client for Yoom automation. Supports document management, multi-signer workflows, templates, and webhooks.

## Supported Features
- ✅ Upload and manage documents
- ✅ Add and manage multiple signers
- ✅ Email and SMS notifications
- ✅ Sequential signing workflows
- ✅ Template creation and reuse
- ✅ Webhook integrations
- ✅ Account quota management
- ✅ Document download

## Setup

### 1. Get API Token
Visit https://app.zapsign.com.br/api-tokens to generate your API token.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export ZAPSIGN_API_TOKEN="your_api_token_here"
```

## Usage

### Basic Workflow
```python
import os
from zapsign_client import ZapsignAPIClient

os.environ['ZAPSIGN_API_TOKEN'] = 'your_api_token'

client = ZapsignAPIClient()

# Upload document
doc = client.upload_document('contract.pdf')
doc_id = doc['token']

# Create signature request with multiple signers
request = client.create_signature_request(
    doc_id=doc_id,
    signers=[
        {'name': 'John Doe', 'email': 'john@example.com'},
        {'name': 'Jane Smith', 'email': 'jane@example.com'}
    ],
    signer_positions=[1, 2],  # Sequential signing
    email_subject='Please sign this contract'
)

# Download signed document
document_content = client.download_document(doc_id)

client.close()
```

### Add Signers Individually
```python
# Add signer with SMS
client.add_signer(
    doc_id=doc_id,
    email='client@example.com',
    name='Client Name',
    phone='+5511999999999',
    position=1
)

# Add signer without email notification
client.add_signer(
    doc_id=doc_id,
    email='witness@example.com',
    name='Witness Name',
    disable_email=True,
    position=2
)
```

### Templates
```python
# Create template
template = client.create_template(
    file_path='nda-template.pdf',
    name='NDA Template',
    description='Non-disclosure agreement'
)

# List templates
templates = client.list_templates()
```

### Webhooks and Account
```python
# Create webhook
client.create_webhook('https://your-app.com/webhooks/zapsign')

# Check account quota
quota = client.get_quota()
```

## Integration Type
- **Type:** API Token (Bearer Token)
- **Authentication:** Bearer token in Authorization header
- **Protocol:** HTTPS REST API
- **Region:** Brazil-based service

## Testability
- ✅ Sandbox environment available
- ✅ All API actions testable
- ✅ Free trial for development

## Notes
- Supports PDF documents
- Brazilian service with local support
- SMS notifications available
- Sequential and parallel signing supported
- Templates simplify repeat documents