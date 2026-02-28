# Satori API Client

Python client for Satori API - provides customer management and action tracking.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

Get your API key from Satori and initialize the client:

```python
from client import SatoriClient

client = SatoriClient(api_key="your-api-key")
```

## API Actions

### Register Customer

Create a new customer:

```python
result = client.register_customer(
    customer_id="cust123",
    name="John Doe",
    email="john@example.com",
    phone="+1234567890",
    properties={
        "plan": "pro",
        "signup_date": "2024-01-01",
        "company": "Acme Corp"
    }
)

print(f"Customer created at {result['created']}")
```

### Register or Update Customer

Create a new customer or update an existing one:

```python
result = client.register_or_update_customer(
    customer_id="cust123",
    email="john@example.com",
    properties={
        "plan": "premium",
        "last_login": "2024-02-01"
    }
)

if 'created' in result:
    print("New customer created")
else:
    print("Customer updated")
```

### Register Customer Action

Track customer actions and events:

```python
# Track a purchase
result = client.register_customer_action(
    customer_id="cust123",
    action_name="purchase",
    action_value=99.99,
    action_properties={
        "product_id": "prod456",
        "product_name": "Pro Subscription"
    }
)

# Track custom events
result = client.register_customer_action(
    customer_id="cust123",
    action_name="page_view",
    action_properties={
        "page": "/pricing",
        "duration": 45
    }
)

print(f"Action ID: {result['action_id']}")
```

### Delete Customer

Remove a customer:

```python
result = client.delete_customer("cust123")
print(f"Customer deleted at {result['deleted']}")
```

## Error Handling

```python
from client import (
    SatoriClient,
    AuthenticationError,
    RateLimitError,
    InvalidRequestError,
    APIError
)

client = SatoriClient(api_key="your-api-key")

try:
    result = client.register_customer(
        customer_id="cust123",
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
with SatoriClient(api_key="your-api-key") as client:
    result = client.register_customer(
        customer_id="cust123",
        name="John Doe"
    )
    # Session automatically closed
```

## Rate Limiting

The client includes built-in rate limiting (300 requests per minute by default) and automatic retries with exponential backoff.

## Common Use Cases

### Customer Onboarding

```python
with SatoriClient(api_key="your-api-key") as client:
    # Create customer
    client.register_or_update_customer(
        customer_id="new_user_123",
        name="Jane Smith",
        email="jane@example.com",
        properties={
            "signup_date": "2024-02-15",
            "source": "marketing_campaign",
            "plan": "free"
        }
    )

    # Track onboarding action
    client.register_customer_action(
        customer_id="new_user_123",
        action_name="onboarding_completed",
        action_properties={
            "steps_completed": 5,
            "time_spent_minutes": 15
        }
    )
```

### E-commerce Integration

```python
with SatoriClient(api_key="your-api-key") as client:
    # Update customer with purchase info
    customer_id = "cust_123"

    client.register_or_update_customer(
        customer_id=customer_id,
        properties={
            "total_purchases": 10,
            "lifetime_value": 999.99,
            "last_purchase": "2024-02-15"
        }
    )

    # Log purchase action
    client.register_customer_action(
        customer_id=customer_id,
        action_name="purchase",
        action_value=99.99,
        action_properties={
            "product_id": "prod_789",
            "product_name": "Premium Widget",
            "quantity": 1
        }
    )
```

## License

MIT License