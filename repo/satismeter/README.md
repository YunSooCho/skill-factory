# Satismeter API Client

Python client for Satismeter API - provides user management and survey response handling for customer feedback.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

Get your API key and write key from [Satismeter](https://www.satismeter.com) and initialize the client:

```python
from client import SatismeterClient

client = SatismeterClient(
    api_key="your-api-key",
    write_key="your-write-key"  # Optional, defaults to api_key
)
```

## API Actions

### Add or Update User

Add a new user or update existing user information:

```python
result = client.add_or_update_user(
    user_id="user123",
    email="john@example.com",
    name="John Doe",
    properties={
        "plan": "pro",
        "signup_date": "2024-01-01",
        "company": "Acme Corp"
    },
    project_id="your-project-id"  # Optional
)

if result['created']:
    print("User created successfully")
else:
    print("User updated successfully")
```

### List Users

Get a list of survey users:

```python
# List all users
result = client.list_users(limit=50)
print(f"Total users: {result['total']}")

# Filter by project
result = client.list_users(
    project_id="your-project-id",
    limit=100,
    offset=0
)

# Filter by email
result = client.list_users(email="john@example.com")

for user in result['users']:
    print(f"{user['name']} ({user['email']})")
    # Access custom properties
    print(f"Plan: {user.get('properties', {}).get('plan', 'N/A')}")
```

## Webhook Handling (Trigger: New Survey Response)

Satismeter can send webhook events when users respond to surveys:

```python
from flask import Flask, request

app = Flask(__name__)
client = SatismeterClient(
    api_key="your-api-key",
    write_key="your-write-key"
)

WEBHOOK_SECRET = "your-webhook-secret"

@app.route('/webhook/satismeter', methods=['POST'])
def handle_webhook():
    payload = request.get_json()
    signature = request.headers.get('X-Satismeter-Signature')

    try:
        event = client.handle_webhook_event(
            payload=payload,
            signature=signature,
            webhook_secret=WEBHOOK_SECRET
        )

        # Handle survey response event
        if event['event_type'] == 'survey_response':
            user = event['user']
            response = event['response']
            survey = event['survey']
            answers = event['answers']

            print(f"New survey response from {user.get('name', 'Unknown')}")
            print(f"Survey: {survey.get('name', 'Unknown')}")
            print(f"Score: {response.get('score', 'N/A')}")

            # Process answers
            for answer in answers:
                print(f"Question: {answer.get('question')}")
                print(f"Answer: {answer.get('answer')}")

        return {'status': 'success'}, 200

    except Exception as e:
        print(f"Webhook error: {e}")
        return {'status': 'error'}, 400

if __name__ == '__main__':
    app.run(port=5000)
```

### Manual Signature Verification

Verify webhook signatures manually:

```python
payload = request.get_data(as_text=True)
signature = request.headers.get('X-Satismeter-Signature')

is_valid = client.verify_webhook_signature(
    payload=payload,
    signature=signature,
    webhook_secret="your-webhook-secret"
)

if is_valid:
    print("Webhook signature verified")
else:
    print("Invalid webhook signature")
```

## Error Handling

```python
from client import (
    SatismeterClient,
    AuthenticationError,
    RateLimitError,
    InvalidRequestError,
    APIError
)

client = SatismeterClient(api_key="your-api-key")

try:
    result = client.add_or_update_user(
        user_id="user123",
        email="john@example.com"
    )
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
with SatismeterClient(api_key="your-api-key") as client:
    result = client.add_or_update_user(
        user_id="user123",
        email="john@example.com"
    )
    # Session automatically closed
```

## Rate Limiting

The client includes built-in rate limiting (500 requests per minute by default) and automatic retries with exponential backoff.

## Common User Properties

When adding/updating users, you can include custom properties:

```python
result = client.add_or_update_user(
    user_id="user123",
    email="john@example.com",
    name="John Doe",
    properties={
        # Common properties
        "company": "Acme Corp",
        "role": "Manager",
        "plan": "Pro",
        "mrr": 99.99,

        # Custom properties for targeting surveys
        "signup_date": "2024-01-01",
        "last_login": "2024-01-15",
        "feature_usage": 42,
        "support_tickets": 3
    }
)
```

## License

MIT License