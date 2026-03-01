# Brevo API Integration

## Overview
Brevo API for email, SMS, and WhatsApp marketing. Full suite of contact management and campaign tools.

## Supported Features
- ✅ Get Contact - Retrieve contact details
- ✅ Create Contact - Add new contacts
- ✅ Update Contact - Modify contact information
- ✅ Add Contact to List - Add existing contact to list
- ✅ Send Transactional Email - Send individual emails
- ✅ Create SMS Campaign - Create SMS campaigns
- ✅ Send SMS Immediately - Send SMS now
- ✅ Create WhatsApp Campaign - Create WhatsApp campaigns
- ✅ Get Email Report - Get campaign statistics
- ✅ Send Campaign Report - Email campaign reports

## Webhooks
- ✅ Marketing Email Opened
- ✅ Marketing Email Delivered
- ✅ Marketing Email Link Clicked
- ✅ Marketing Email Unsubscribe
- ✅ Transactional Email Opened
- ✅ Transactional Email Clicked
- ✅ Transactional Email Delivered
- ✅ Contact Created

## Setup

### 1. Get API Key
1. Sign up at [Brevo](https://www.brevo.com/)
2. Go to SMTP & API → API Keys
3. Generate API key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_key = "your_brevo_api_key"
```

## Usage

```python
from brevo_client import BrevoClient

client = BrevoClient(api_key="your_key")

# Contact management
contact = client.create_contact(
    email="user@example.com",
    first_name="John",
    last_name="Doe",
    list_ids=[1],
    attributes={"COUNTRY": "Japan", "PLAN": "Premium"}
)

fetched = client.get_contact("user@example.com")
client.update_contact(
    "user@example.com",
    list_ids=[1, 2],  # Add to another list
    attributes={"STATUS": "Active"}
)

# Transactional email
client.send_transactional_email(
    to=[{"email": "recipient@example.com", "name": "John Doe"}],
    subject="Your order has been shipped!",
    html_content="<h1>Order Shipped</h1><p>Your package is on the way.</p>",
    sender={"email": "shipping@store.com", "name": "Store"},
    tags=["order", "shipping"]
)

# SMS campaign
sms = client.create_sms_campaign(
    name="Flash Sale",
    sender="STORE",
    content="50% off today only! Visit store.com",
    recipients={"listIds": [2]}
)
client.send_sms_now(sms.id)

# WhatsApp campaign
whatsapp = client.create_whatsapp_campaign(
    name="Order Update",
    template_id=12345,
    recipients={"listIds": [1]}
)

# Get campaign statistics
stats = client.get_email_campaign_report(campaign_id=123)
print(f"Open rate: {stats.opened / stats.sent * 100:.1f}%")

# Email report
client.send_campaign_report(
    campaign_id=123,
    email="manager@company.com",
    language="en"
)

# Verify webhook
signature = request.headers.get("X-Signature")
if client.verify_webhook(signature, request.body, "your_webhook_key"):
    # Process webhook
    pass

client.close()
```

## Integration Type
- **Type:** API Key
- **Authentication:** api-key header
- **Protocol:** HTTPS REST API

## Testability
- ✅ All operations testable with valid API key

## Notes
- Free tier includes 300 emails/day
- SMS credits required for SMS operations
- WhatsApp templates must be pre-approved
- Webhook verification available
- Comprehensive campaign analytics