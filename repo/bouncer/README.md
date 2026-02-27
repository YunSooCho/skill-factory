# Bouncer API Integration

## Overview
Bouncer API for email and domain verification. Validate email addresses and check domain health.

## Supported Features
- ✅ Verify Email Address - Check email validity
- ✅ Verify Domain - Check domain configuration

## Setup

### 1. Get API Key
1. Sign up at [Bouncer](https://usebouncer.com/)
2. Go to Settings → API
3. Generate API key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_key = "your_api_key"
```

## Usage

```python
from bouncer_client import BouncerClient, EmailStatus

client = BouncerClient(api_key="your_key")

# Verify email
result = client.verify_email("user@example.com")
print(f"Status: {result.status.value}")
print(f"Deliverable: {result.status == EmailStatus.DELIVERABLE}")
print(f"Reason: {result.reason}")
print(f"Disposable: {result.is_disposable}")
print(f"Score: {result.score}")

# Verify domain
domain_result = client.verify_domain("example.com")
print(f"Valid MX: {domain_result.mx_records}")
print(f"SPF: {domain_result.spf_record}")
print(f"DMARC: {domain_result.dmarc_record}")

client.close()
```

## Integration Type
- **Type:** API Key
- **Authentication:** x-api-key header
- **Protocol:** HTTPS REST API

## Testability
- ✅ All operations testable with valid API key

## Notes
- Rate limits apply (typically 100 requests/minute on free tier)
- Verification results include confidence scores
- Supports real-time verification