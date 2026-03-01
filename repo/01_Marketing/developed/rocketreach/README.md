# RocketReach API Client

Python client for RocketReach API - provides people lookup, company lookup, and bulk contact enrichment.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

Get your API key from [rocketreach.co](https://rocketreach.co) and initialize the client:

```python
from client import RocketReachClient

client = RocketReachClient(api_key="your-api-key")
```

## API Actions

### Lookup Person

Find person information by email, name, or LinkedIn URL:

```python
# By email
result = client.lookup_person(email="john@example.com")
print(result['name'])
print(result['title'])

# By name
result = client.lookup_person(name="John Smith")

# By LinkedIn URL
result = client.lookup_person(linkedin_url="https://linkedin.com/in/johnsmith")
```

### Lookup Company

Find company information:

```python
# By domain
result = client.lookup_company(domain="example.com")
print(result['name'])
print(result['industry'])

# By name
result = client.lookup_company(name="Example Corporation")

# By LinkedIn URL
result = client.lookup_company(linkedin_url="https://linkedin.com/company/examplecorp")
```

### Bulk People Lookup

Lookup multiple people at once (up to 100 per request):

```python
queries = [
    {"email": "john@example.com"},
    {"email": "jane@example.com"},
    {"name": "Bob Johnson"}
]

result = client.bulk_people_lookup(queries)
print(f"Request ID: {result['request_id']}")

for person in result['results']:
    print(f"{person['name']} - {person.get('title', 'N/A')}")

for failed in result['failed']:
    print(f"Failed: {failed}")
```

## Error Handling

```python
from client import (
    RocketReachClient,
    AuthenticationError,
    RateLimitError,
    InsufficientCreditsError,
    InvalidRequestError,
    APIError
)

client = RocketReachClient(api_key="your-api-key")

try:
    result = client.lookup_person(email="john@example.com")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded, please wait")
except InsufficientCreditsError:
    print("Insufficient API credits, top up required")
except InvalidRequestError as e:
    print(f"Invalid request: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Context Manager

Use with context manager for automatic session cleanup:

```python
with RocketReachClient(api_key="your-api-key") as client:
    result = client.lookup_person(email="john@example.com")
    # Session automatically closed
```

## Rate Limiting

The client includes built-in rate limiting (200 requests per minute by default) and automatic retries with exponential backoff.

## Credits

RocketReach uses a credit-based system. Each lookup consumes credits. Monitor your credit balance via the RocketReach dashboard.

## License

MIT License