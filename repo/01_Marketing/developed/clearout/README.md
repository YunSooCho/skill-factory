# Clearout Email Validator & Finder Integration

## Overview
Implementation of Clearout Email Validator & Finder API for Yoom automation.

## Supported Features
### Email Validation (7 endpoints)
- ✅ Validate Email Address
- ✅ Check Email for Business Account
- ✅ Check Email for Free Account
- ✅ Check Email for Role Account
- ✅ Check Email for Disposable Email
- ✅ Check Email for Catch-all
- ✅ Check Progress Status of Bulk Customer List

### Email Finder (2 endpoints)
- ✅ Instant Email Finder
- ✅ Check Progress Status of Bulk Email Finder

### Bulk Processing (1 endpoint)
- ✅ Bulk Customer List Validation

## Setup

### 1. Get API Key
1. Visit [Clearout](https://clearout.io/)
2. Sign up for a free account
3. Get your API key from the dashboard

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Email Validation
```python
import asyncio
from clearout_client import ClearoutClient

async def example():
    api_key = "your_api_key"

    async with ClearoutClient(api_key=api_key) as client:
        # Validate a single email
        result = await client.validate_email("test@example.com")

        print(f"Valid: {result.is_valid}")
        print(f"Status: {result.status}")
        print(f"Disposable: {result.is_disposable}")
        print(f"Free Email: {result.is_free}")
        print(f"Role Account: {result.is_role_account}")
        print(f"Score: {result.score}")

        # Check specific email types
        is_business = await client.check_email_for_business_account("john@company.com")
        is_free = await client.check_email_for_free_account("test@gmail.com")
        is_role = await client.check_email_for_role_account("admin@company.com")
        is_disposable = await client.check_email_for_disposable_email("temp@10minutemail.com")
        is_catch_all = await client.check_email_for_catch_all("user@company.com")

asyncio.run(example())
```

### Email Finder
```python
async def finder_example():
    api_key = "your_api_key"

    async with ClearoutClient(api_key=api_key) as client:
        # Find email based on name and domain
        result = await client.find_email(
            first_name="John",
            last_name="Doe",
            domain="company.com"
        )

        print(f"Email: {result.email}")
        print(f"Confidence Score: {result.confidence_score}")
        print(f"Domain Status: {result.domain_status}")

asyncio.run(finder_example())
```

### Bulk Email Validation
```python
async def bulk_validation_example():
    api_key = "your_api_key"

    async with ClearoutClient(api_key=api_key) as client:
        # Upload bulk job
        emails = [
            "john@example.com",
            "jane@example.com",
            "invalid-email"
        ]

        job = await client.bulk_customer_list(emails, name="My Batch")

        print(f"Job ID: {job.job_id}")
        print(f"Status: {job.status}")

        # Check progress
        while job.status != "completed":
            await asyncio.sleep(5)
            job = await client.check_bulk_status(job.job_id)
            print(f"Progress: {job.processed}/{job.total_emails}")

        # Final results
        print(f"Valid: {job.valid}")
        print(f"Invalid: {job.invalid}")

asyncio.run(bulk_validation_example())
```

### Bulk Email Finder
```python
async def bulk_finder_example():
    api_key = "your_api_key"

    async with ClearoutClient(api_key=api_key) as client:
        contacts = [
            {"first_name": "John", "last_name": "Doe", "domain": "company.com"},
            {"first_name": "Jane", "last_name": "Smith", "domain": "startup.com"}
        ]

        job = await client.bulk_email_finder(contacts, name="Contact Finder")

        print(f"Job ID: {job.job_id}")
        print(f"Status: {job.status}")

asyncio.run(bulk_finder_example())
```

### Convenience Function
```python
from clearout_client import validate_email_simple

# Quick validation without context manager
is_valid = asyncio.run(validate_email_simple(
    api_key="your_api_key",
    email="test@example.com"
))

print(is_valid)
```

## Integration Type
- **Type:** API Key
- **Authentication:** API key in query parameters
- **Protocol:** HTTPS REST API

## API Response Objects

### EmailValidationResult
```python
@dataclass
class EmailValidationResult:
    email: str                          # Validated email
    is_valid: bool                      # Overall validity
    status: str                         # Status (valid, invalid, unknown)
    result: str                         # Detailed result description
    reason: str                         # Validation reason
    score: float                        # Quality score (0-100)
    is_disposable: bool                 # Is disposable email service
    is_free: bool                       # Is free email provider
    is_role_account: bool               # Is role-based (admin, support, etc.)
    is_catch_all: bool                  # Domain has catch-all enabled
    domain: str                         # Email domain
    mx_records: List[str]               # MX records
    raw_response: Dict                  # Full API response
```

### EmailFindResult
```python
@dataclass
class EmailFindResult:
    email: str                          # Found email address
    confidence_score: float             # Confidence score (0-100)
    first_name: str                     # Contact's first name
    last_name: str                      # Contact's last name
    domain: str                         # Company domain
    domain_status: str                  # Domain verification status
    verification_status: str            # Email verification status
    raw_response: Dict                  # Full API response
```

### BulkJobStatus
```python
@dataclass
class BulkJobStatus:
    job_id: str                         # Job identifier
    status: str                         # Job status (in_progress, completed, etc.)
    total_emails: int                   # Total emails to process
    processed: int                      # Processed count
    valid: int                          # Valid emails count
    invalid: int                        # Invalid emails count
    risk_stats: Dict                    # Risk category breakdown
    created_at: str                     # Job creation timestamp
    completed_at: str                   # Job completion timestamp
    raw_response: Dict                  # Full API response
```

## Error Handling

The client handles common errors:

- **ValueError**: Invalid parameters or email format
- **aiohttp.ClientError**: Network errors
- **401 Unauthorized**: Invalid API key
- **429 Rate Limit**: Too many requests
- **404 Not Found**: Job ID not found

## Testability
- ✅ Free tier available (100 credits/month)
- ✅ All API actions are testable with valid API key
- ⚠️ Rate limits apply based on your plan

## Notes
- Validate emails before sending campaigns to reduce bounce rates
- Email finder has confidence scores - higher is better
- Bulk jobs are processed asynchronously - use job_id to check status
- Free tier has limited credits; consider a paid plan for bulk operations
- API documentation: https://apidocs.clearout.io/