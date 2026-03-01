# Reverse Contact API Client

Python client for Reverse Contact API - provides reverse email lookup, domain search, and LinkedIn profile enrichment.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

Get your API key from [reversecontact.com](https://www.reversecontact.com) and initialize the client:

```python
from client import ReverseContactClient

client = ReverseContactClient(api_key="your-api-key")
```

## API Actions

### Email Lookup

Find person and company information by email:

```python
result = client.email_lookup("john@example.com")
print(result['person']['name'])
print(result['company']['name'])
```

### Domain Lookup

Get company information by domain:

```python
result = client.domain_lookup("example.com")
print(result['company']['name'])
print(result['company']['industry'])
```

### Get LinkedIn Profile

Retrieve LinkedIn profile details for an email:

```python
result = client.get_linkedin_profile("john@example.com")
print(result['profile_url'])
print(result['headline'])
```

### Get LinkedIn Company

Retrieve LinkedIn company details:

```python
result = client.get_linkedin_company("example.com")
print(result['company_url'])
print(result['followers'])
```

## Error Handling

```python
from client import (
    ReverseContactClient,
    AuthenticationError,
    RateLimitError,
    InvalidRequestError,
    APIError
)

client = ReverseContactClient(api_key="your-api-key")

try:
    result = client.email_lookup("john@example.com")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded, please wait")
except InvalidRequestError as e:
    print(f"Invalid request: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Context Manager

Use with context manager for automatic session cleanup:

```python
with ReverseContactClient(api_key="your-api-key") as client:
    result = client.email_lookup("john@example.com")
    # Session automatically closed
```

## Rate Limiting

The client includes built-in rate limiting (100 requests per minute by default) and automatic retries with exponential backoff.

## License

MIT License