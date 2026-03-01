# Benchmark Email API Integration

## Overview
Benchmark Email API for contact management and email marketing. Simplified contact CRUD operations.

## Supported Features
- ✅ Add Contact - Create new email contacts
- ✅ Update Contact - Modify existing contact information
- ✅ Search Contact - Find contacts by email or list

## Setup

### 1. Get API Token
1. Sign up at [Benchmark Email](https://www.benchmarkemail.com/)
2. Go to Settings → API Management
3. Generate your API token

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
from benchmark_email_client import BenchmarkEmailClient

client = BenchmarkEmailClient(api_token="your_token")

# Add contact
contact = client.add_contact(
    email="user@example.com",
    first_name="John",
    last_name="Doe",
    city="Tokyo",
    country="Japan"
)

# Search
contacts = client.search_contact(email="user@example.com")

# Update
client.update_contact(
    contact.id,
    phone="+81-90-1234-5678"
)

client.close()
```

## Integration Type
- **Type:** API Token
- **Authentication:** AuthToken header
- **Protocol:** HTTPS REST API

## Testability
- ✅ Testable with valid API token