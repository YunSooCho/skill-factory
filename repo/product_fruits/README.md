# ProductFruits

ProductFruits is a user onboarding platform for engaging and educating new users.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your ProductFruits API key:

1. Sign up at [ProductFruits](https://productfruits.com)
2. Go to Settings > API Keys
3. Generate and copy your API key

## Usage

```python
from product_fruits import ProductFruitsClient

client = ProductFruitsClient(api_key='your-api-key')

# Create or update a user
user = client.create_or_update_user({
    'username': 'john.doe',
    'email': 'john@example.com',
    'role': 'admin',
    'firstName': 'John',
    'lastName': 'Doe',
    'signUpAt': '2024-01-01T00:00:00Z'
})

print(f"User: {user}")
```

## API Methods

- `create_or_update_user(user_data)` - Create or update a user

## Triggers

ProductFruits provides trigger-based webhooks for:
- Survey Finished
- Feedback Received

Configure webhooks in your ProductFruits dashboard.