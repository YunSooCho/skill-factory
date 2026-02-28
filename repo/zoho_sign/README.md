# Zoho Sign API Integration

## Overview
Complete Zoho Sign electronic signature API client for Yoom automation. Supports documents, templates, workflows, fields, and advanced features.

## Supported Features
- ✅ Upload and manage files
- ✅ Create and manage signature requests
- ✅ Sequential and parallel signing
- ✅ Template creation and reuse
- ✅ Field placement and configuration
- ✅ Contact management
- ✅ Reminder and expiry settings
- ✅ Webhook integrations
- ✅ Brand customization
- ✅ Account and usage statistics

## Setup

### 1. Get API Token
Visit https://accounts.zoho.com/apiauthtoken/create to generate your authtoken.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export ZOHO_SIGN_API_TOKEN="your_authtoken_here"
export ZOHO_SIGN_BASE_URL="https://sign.zoho.com/api/v1"  # optional
```

## Usage

### Basic Signature Request
```python
import os
from zoho_sign_client import ZohoSignAPIClient

os.environ['ZOHO_SIGN_API_TOKEN'] = 'your_api_token'

client = ZohoSignAPIClient()

# Upload file
file_response = client.upload_file('contract.pdf')
file_ids = [file_response['requests']['request_id']]

# Create signature request
request = client.create_sign_request(
    file_ids=file_ids,
    recipients=[
        {
            'participantEmail': 'signer@example.com',
            'participantName': 'John Doe',
            'actionType': 'sign'
        }
    ],
    request_name='Service Agreement',
    notes='Please review and sign',
    expiry_date='2025-01-01',
    reminder_period=3
)

# Submit for signing
client.submit_sign_request(request['requests']['request_id'])

client.close()
```

### Template Usage
```python
# Create template
template = client.create_template(
    file_path='nda-template.pdf',
    template_name='NDA Template',
    description='Non-disclosure agreement',
    recipients=[
        {
            'roleName': 'Disclosing Party',
            'actionType': 'sign'
        },
        {
            'roleName': 'Receiving Party',
            'actionType': 'sign'
        }
    ]
)

# Use template
request = client.use_template(
    template_id=template['templates']['template_id'],
    recipient_details=[
        {'participantEmail': 'party1@company.com', 'participantName': 'Alice'},
        {'participantEmail': 'party2@company.com', 'participantName': 'Bob'}
    ]
)
```

### Sequential Signing and Fields
```python
# Sequential signing
request = client.create_sign_request(
    file_ids=file_ids,
    recipients=[
        {'participantEmail': 'first@example.com', 'actionType': 'sign'},
        {'participantEmail': 'second@example.com', 'actionType': 'sign'}
    ],
    request_name='Multi-sign Document',
    is_sequential=True
)

# Add fields
client.add_fields(
    request_id=request['requests']['request_id'],
    document_id=request['requests']['documents'][0]['document_id'],
    fields=[
        {
            'FieldType': 'signature',
            'PageIndex': 0,
            'X': 100,
            'Y': 200,
            'Width': 150,
            'Height': 50,
            'ParticipantIndex': 0
        }
    ]
)
```

### Webhooks and Monitoring
```python
# Create webhook
client.create_webhook(
    url='https://your-app.com/webhooks/zohosign',
    events=['request.completed', 'request.cancelled'],
    secret_key='webhook_secret'
)

# Check usage
stats = client.get_usage_stats()
print(f"Used: {stats['usage_report']['signed']}")
```

## Integration Type
- **Type:** Authtoken
- **Authentication:** Zoho-oauthtoken header
- **Protocol:** HTTPS REST API
- **Ecosystem:** Zoho Suite

## Testability
- ✅ Free plan for testing
- ✅ Sandbox environment available
- ✅ All API actions testable

## Notes
- Part of Zoho ecosystem
- Integration with Zoho CRM, Docs, etc.
- Strong security and compliance
- Multi-region support available
- Advanced workflow features
- Support for various field types