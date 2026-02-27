# Email List Verify API Integration

## Overview
Implementation of Email List Verify email validation service API for Yoom automation.

## Supported Features

### API Actions (4 operations)
- ✅ Email Address Verification
- ✅ Email Deliverability Evaluation
- ✅ Find Business Email Address
- ✅ Check Disposable Email Domain

### Triggers
- No triggers supported

## Setup

### 1. Get API Credentials
1. Visit https://emaillistverify.com/ and sign up
2. Go to Account > API Key
3. Copy your API key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_key = "your_api_key"
```

## Usage

### Basic Example
```python
import asyncio
from email_list_verify_client import EmailListVerifyClient

async def main():
    api_key = "your_api_key"

    async with EmailListVerifyClient(api_key=api_key) as client:
        # Verify email
        verification = await client.verify_email("test@example.com")
        print(f"Valid: {verification.is_valid}")
```

### Email Verification
```python
# Basic verification
verification = await client.verify_email("user@example.com")

print(f"Email: {verification.email}")
print(f"Valid: {verification.is_valid}")
print(f"Score: {verification.score}")
print(f"Disposable: {verification.is_disposable}")
print(f"Free Provider: {verification.is_free_provider}")
print(f"Role Email: {verification.is_role_email}")
print(f"MX Record: {verification.mx_record}")
print(f"SMTP Check: {verification.smtp_check}")

if verification.reason:
    print(f"Reason: {verification.reason}")
```

### Email Deliverability Evaluation
```python
# Comprehensive deliverability check
deliverability = await client.evaluate_deliverability("user@example.com")

print(f"Deliverable: {deliverability.deliverable}")
print(f"Confidence Score: {deliverability.confidence_score}")

if deliverability.issues:
    print("\nIssues:")
    for issue in deliverability.issues:
        print(f"  ⚠️ {issue}")

if deliverability.suggestions:
    print("\nSuggestions:")
    for suggestion in deliverability.suggestions:
        print(f"  💡 {suggestion}")
```

### Business Email Finder
```python
# Find business email for a person
emails = await client.find_business_email(
    first_name="John",
    last_name="Doe",
    domain="acme.com"
)

print(f"Found {len(emails)} candidate emails:")
for email in emails:
    print(f"\n  Email: {email.email}")
    print(f"  Confidence: {email.confidence}")
    if email.full_name:
        print(f"  Name: {email.full_name}")
    if email.company:
        print(f"  Company: {email.company}")

# Get best match
if emails:
    best_match = max(emails, key=lambda e: e.confidence)
    print(f"\nBest match: {best_match.email}")
```

### Disposable Domain Check
```python
# Check if domain is disposable
check = await client.check_disposable_domain("tempmail.com")

print(f"Domain: {check.domain}")
print(f"Disposable: {check.is_disposable}")
if check.provider:
    print(f"Provider: {check.provider}")

# Also works with @ prefix
check = await client.check_disposable_domain("@guerrillamail.com")
print(f"Disposable: {check.is_disposable}")
```

## Integration Type
- **Type:** API Key (Query parameter)
- **Authentication:** `secret` in query parameters
- **Protocol:** HTTPS REST API

## Testability
- ✅ All API actions testable with valid credentials
- ❌ No webhook triggers available

## Verification Score

The verification score ranges from 0.0 to 1.0:
- **1.0** - High confidence, email is valid
- **0.7-0.9** - Good confidence, likely valid
- **0.5-0.7** - Medium confidence, proceed with caution
- **0.0-0.5** - Low confidence, likely invalid

```python
verification = await client.verify_email("user@example.com")

if verification.score >= 0.9:
    print("High confidence - proceed")
elif verification.score >= 0.7:
    print("Good confidence - may proceed")
else:
    print("Low confidence - investigate further")
```

## Common Email Types

### Role-Based Emails
```python
# These are addressed to roles, not individuals
verification = await client.verify_email("info@company.com")
if verification.is_role_email:
    print("This is a role-based email")
```

Common role-based emails: info@, support@, sales@, contact@, admin@, team@

### Free Email Providers
```python
verification = await client.verify_email("user@gmail.com")
if verification.is_free_provider:
    print("This is a free email provider")
```

Common providers: gmail.com, yahoo.com, hotmail.com, outlook.com, aol.com

### Disposable Email Providers
```python
verification = await client.verify_email("user@tempmail.com")
if verification.is_disposable:
    print("This is a disposable email service")
```

## Best Practices

### Bulk Verification
```python
# Verify multiple emails efficiently
emails = [
    "user1@example.com",
    "user2@example.com",
    "user3@example.com"
]

tasks = [client.verify_email(email) for email in emails]
results = await asyncio.gather(*tasks)

valid_emails = [r.email for r in results if r.is_valid]
print(f"Valid emails: {len(valid_emails)}")
```

### Business Email Enrichment
```python
# Enrich contact information with business emails
async def enrich_lead(name: str, domain: str):
    parts = name.split()
    if len(parts) >= 2:
        results = await client.find_business_email(
            first_name=parts[0],
            last_name=" ".join(parts[1:]),
            domain=domain
        )
        return results
    return []

emails = await enrich_lead("John Smith", "acme.com")
```

### Form Validation
```python
# Validate email on form submission
async def validate_registration_email(email: str) -> bool:
    try:
        verification = await client.verify_email(email)

        # Enforce quality rules
        if verification.is_disposable:
            raise ValueError("Disposable emails not allowed")

        if verification.is_role_email:
            raise ValueError("Please use a personal email")

        if verification.score < 0.7:
            raise ValueError("Email validation failed")

        return verification.is_valid
    except Exception as e:
        print(f"Validation error: {e}")
        return False
```

### Deliverability Assessment
```python
# Assess email quality before sending campaigns
deliverability = await client.evaluate_deliverability(email)

if not deliverability.deliverable:
    print("Issues found:")
    for issue in deliverability.issues:
        print(f"  - {issue}")

    # Exclude low-quality emails from campaigns
    return False

return deliverability.confidence_score >= 0.8
```

### Domain Validation
```python
# Check multiple domains for disposable providers
domains = ["gmail.com", "tempmail.com", "guerrillamail.com"]

tasks = [client.check_disposable_domain(d) for d in domains]
results = await asyncio.gather(*tasks)

disposable_domains = [r.domain for r in results if r.is_disposable]
print(f"Disposable domains: {disposable_domains}")
```

## Rate Limits

- Free tier typically allows 100-300 verifications per day
- Implement appropriate rate limiting for production
- Consider caching results to reduce API calls

```python
from functools import lru_cache
import asyncio

@lru_cache(maxsize=1000)
async def cached_verify(email: str):
    """Cached email verification"""
    return await client.verify_email(email)

result = await cached_verify("user@example.com")
# Subsequent calls for same email will use cache
```

## Interpreting Results

### Status Codes
- **ok** - Email is valid and deliverable
- **error** - Email verification failed with SMTP error
- **invalid** - Email format is invalid
- **not_allowed** - Domain blacklisted or blocked

### Issues and Suggestions
The deliverability evaluation provides:
- **Issues** - Problems that would prevent email delivery
- **Suggestions** - Recommendations to improve deliverability

Common issues:
- No MX records
- SMTP check failed
- Disposable provider
- Role-based address

Common suggestions:
- Request business email
- Verify domain spelling
- Ask for alternative email

## Notes

- Always handle API errors gracefully
- Implement retry logic for transient failures
- Cache verification results to stay within rate limits
- Consider batching for bulk verification
- Free providers and role emails aren't invalid, but may need different handling based on your use case