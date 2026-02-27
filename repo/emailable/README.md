# Emailable API Integration

## Overview
Implementation of Emailable email verification service API for Yoom automation.

## Supported Features

### API Actions (1 operation)
- ✅ Verify Email

### Triggers
- No triggers supported

## Setup

### 1. Get API Credentials
1. Visit https://emailable.com/ and sign up
2. Go to Settings > API Keys
3. Generate a new API Key
4. Copy your API key

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
from emailable_client import EmailableClient

async def main():
    api_key = "your_api_key"

    async with EmailableClient(api_key=api_key) as client:
        # Verify email
        verification = await client.verify_email("test@example.com")
        print(f"Deliverable: {verification.deliverable}")
        print(f"Score: {verification.score}/10")
```

### Email Verification
```python
# Basic verification
verification = await client.verify_email("user@example.com")

print(f"Email: {verification.email}")
print(f"Deliverable: {verification.deliverable}")
print(f"Score: {verification.score}/10")
print(f"State: {verification.state}")

# Email type flags
print(f"Free Email: {verification.free_email}")
print(f"Role Email: {verification.role_email}")
print(f"Disposable: {verification.disposable}")
print(f"Accept All: {verification.accept_all}")

# Technical details
print(f"Domain: {verification.domain}")
print(f"Mailbox Active: {verification.mailbox_active}")
print(f"MX Record: {verification.mx_record}")
print(f"SMTP Check: {verification.smtp_check}")

if verification.reason:
    print(f"Reason: {verification.reason}")
```

### Advanced Verification
```python
# Verification with custom SMTP timeout
verification = await client.verify_email(
    email="user@example.com",
    smtp_timeout=15,  # 15 seconds timeout
    hygiene=True
)

print(f"Score: {verification.score}/10")
```

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

# Count results by state
states = {}
for result in results:
    states[result.state] = states.get(result.state, 0) + 1

print("Verification Summary:")
for state, count in states.items():
    print(f"  {state}: {count}")
```

### Quality Filtering
```python
# Filter emails by quality threshold
async def get_valid_emails(emails: List[str], min_score: float = 8.0) -> List[str]:
    """Get emails that meet quality threshold"""
    tasks = [client.verify_email(email) for email in emails]
    results = await asyncio.gather(*tasks)

    valid_emails = [
        r.email for r in results
        if r.deliverable and r.score >= min_score
    ]

    return valid_emails

valid_emails = await get_valid_emails(emails, min_score=8.0)
print(f"Valid emails: {len(valid_emails)}")
```

## Integration Type
- **Type:** API Key (Query parameter)
- **Authentication:** `apikey` in query parameters
- **Protocol:** HTTPS REST API

## Testability
- ✅ All API actions testable with valid credentials
- ❌ No webhook triggers available

## Verification States

### Deliverable (Recommended)
```python
if verification.state == "deliverable":
    print("✅ Email is safe to send to")
```
- Score: 8-10
- Active mailbox
- Valid MX records
- SMTP check passed

### Undeliverable (Do Not Send)
```python
if verification.state == "undeliverable":
    print("❌ Email cannot receive emails")
```
- Score: 0-1
- Invalid format or domain
- No MX records
- Mailbox does not exist

### Risky (Proceed with Caution)
```python
if verification.state == "risky":
    print("⚠️ Email may have deliverability issues")
```
- Score: 2-7
- Uncertain deliverability
- May bounce frequently
- Consider manual review

### Unknown (Unable to Verify)
```python
if verification.state == "unknown":
    print("❓ Unable to verify email")
```
- Score: N/A
- Verification timeout
- Server unavailable
- Temporary error

## Understanding Score

The score ranges from 0 to 10:
- **8-10** - Excellent quality, safe to send
- **6-7** - Good quality, proceed with caution
- **4-5** - Fair quality, may bounce
- **2-3** - Poor quality, high bounce risk
- **0-1** - Invalid, do not send

```python
verification = await client.verify_email("user@example.com")

if verification.score >= 8:
    action = "Send immediately"
elif verification.score >= 6:
    action = "Send with monitoring"
elif verification.score >= 4:
    action = "Consider alternative email"
else:
    action = "Do not send"

print(f"Action: {action} (Score: {verification.score})")
```

## Email Type Flags

### Free Email Providers
```python
if verification.free_email:
    print("This is a free email provider (Gmail, Yahoo, etc.)")
```

Common free providers:
- gmail.com, yahoo.com, hotmail.com
- outlook.com, aol.com, icloud.com
- mail.com, protonmail.com, zoho.com

### Role-Based Emails
```python
if verification.role_email:
    print("This is a role-based email address")
```

Common role emails:
- info@, support@, sales@
- contact@, admin@, team@
- help@, office@, staff@

### Disposable Emails
```python
if verification.disposable:
    print("This is a temporary disposable email")
```

Common disposable providers:
- tempmail.com, guerrillamail.com
- mailinator.com, 10minutemail.com

### Accept All Domains
```python
if verification.accept_all:
    print("Domain accepts all emails (catch-all)")
```

Catch-all domains accept emails to any address but may not deliver to actual mailboxes.

## Best Practices

### Form Validation
```python
# Validate email during registration
async def validate_signup_email(email: str) -> tuple[bool, str]:
    """Validate email for user signup"""
    try:
        verification = await client.verify_email(email)

        # Block certain email types
        if verification.disposable:
            return False, "Disposable emails not allowed"

        if verification.role_email and verification.score < 6:
            return False, "Please use your personal business email"

        if verification.score < 8:
            return False, "Email address may be invalid"

        return verification.deliverable, "Email is valid"

    except Exception as e:
        return False, f"Verification failed: {e}"

is_valid, message = await validate_signup_email("user@example.com")
print(f"{message}")
```

### Campaign Preparation
```python
# Prepare email list for campaigns
async def prepare_campaign(emails: List[str]) -> Dict[str, List[str]]:
    """Segregate emails by quality"""
    tasks = [client.verify_email(email) for email in emails]
    results = await asyncio.gather(*tasks)

    deliverable = []
    risky = []
    undeliverable = []

    for result in results:
        if result.state == "deliverable":
            deliverable.append(result.email)
        elif result.state == "risky":
            risky.append(result.email)
        else:
            undeliverable.append(result.email)

    return {
        "deliverable": deliverable,
        "risky": risky,
        "undeliverable": undeliverable
    }

segments = await prepare_campaign(email_list)
print(f"Ready to send: {len(segments['deliverable'])}")
print(f"Review needed: {len(segments['risky'])}")
```

### Data Enrichment
```python
# Add verification data to your records
async def enrich_contact(contact: Dict[str, Any]) -> Dict[str, Any]:
    """Add email verification data to contact"""
    verification = await client.verify_email(contact['email'])

    contact.update({
        'email_valid': verification.deliverable,
        'email_score': verification.score,
        'email_state': verification.state,
        'is_free_email': verification.free_email,
        'is_role_email': verification.role_email,
        'is_disposable': verification.disposable,
        'mailbox_active': verification.mailbox_active,
        'verified_at': verification.processed_at
    })

    return contact

enriched = await enrich_contact({"email": "user@example.com", "name": "John"})
```

### Batch Processing with Rate Limits
```python
# Process emails with rate limiting
async def process_batch(emails: List[str], batch_size: int = 100):
    """Process emails in batches with delays"""
    results = []

    for i in range(0, len(emails), batch_size):
        batch = emails[i:i + batch_size]

        tasks = [client.verify_email(email) for email in batch]
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)

        # Rate limit: wait between batches
        if i + batch_size < len(emails):
            await asyncio.sleep(1)

    return results

results = await process_batch(email_list, batch_size=100)
```

### Email Health Monitoring
```python
# Monitor email list health over time
async def get_email_health(emails: List[str]) -> Dict[str, float]:
    """Calculate email list health metrics"""
    tasks = [client.verify_email(email) for email in emails]
    results = await asyncio.gather(*tasks)

    total = len(results)
    deliverable = sum(1 for r in results if r.deliverable)
    risky = sum(1 for r in results if r.state == "risky")
    undeliverable = sum(1 for r in results if r.state == "undeliverable")

    avg_score = sum(r.score for r in results) / total if total > 0 else 0

    return {
        "total": total,
        "deliverable_pct": (deliverable / total) * 100 if total > 0 else 0,
        "risky_pct": (risky / total) * 100 if total > 0 else 0,
        "undeliverable_pct": (undeliverable / total) * 100 if total > 0 else 0,
        "average_score": avg_score
    }

health = await get_email_health(email_list)
print(f"Deliverable: {health['deliverable_pct']:.1f}%")
print(f"Average Score: {health['average_score']:.1f}/10")
```

## Notes

- Free tier has daily verification limits
- Implement appropriate rate limiting for bulk processing
- Cache results to avoid re-verifying the same email
- Consider using webhooks for bulk verification (not implemented in this client)
- SMTP timeout can be adjusted for performance vs accuracy tradeoff
- Hygiene check helps identify problematic email patterns
- Always handle API errors and timeouts gracefully