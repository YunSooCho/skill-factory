# Bownow API Integration

## Overview
Bownow API for lead management and CRM. Track, update, and organize customer leads.

## Supported Features
- ✅ Create Lead - Add new leads
- ✅ Get Lead - Retrieve lead details
- ✅ Update Lead - Modify lead information
- ✅ Delete Lead - Remove leads
- ✅ Search Leads - Find by various criteria

## Webhooks
- ✅ Lead Updated Notification
- ✅ Form Conversion Notification

## Setup

### 1. Get API Token
1. Sign up at [Bownow](https://bownow.jp/)
2. Go to Settings → API
3. Generate API token

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_token = "your_api_token"
```

## Usage

```python
from bownow_client import BownowClient

client = BownowClient(api_token="your_token")

# Create lead
lead = client.create_lead(
    name="山田 太郎",
    email="taro@example.com",
    phone="03-1234-5678",
    company="株式会社ABC",
    title="マネージャー",
    status="新規",
    source="Web"
)

# Search leads
results = client.search_leads(
    company="株式会社ABC",
    status="新規"
)

# Update lead
client.update_lead(
    lead.id,
    status="商談中",
    score=75
)

# Verify webhook
signature = request.headers["X-Signature"]
payload = request.get_body()
if client.verify_webhook(signature, payload, "your_webhook_secret"):
    # Process webhook
    pass

client.close()
```

## Integration Type
- **Type:** API Token
- **Authentication:** Bearer token (Authorization header)
- **Protocol:** HTTPS REST API

## Testability
- ✅ All operations testable with valid API token

## Notes
- Japanese lead management platform
- Supports custom fields
- Lead scoring available
- Webhook verification included