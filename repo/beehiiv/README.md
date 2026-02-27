# Beehiiv API Client

Python async client for [Beehiiv API](https://developers.beehiiv.com) - newsletter platform for creators.

## Features

- ✅ Create Subscription
- ✅ Retrieve Subscription by ID
- ✅ Retrieve Subscription by Email
- ✅ Update Subscription
- ✅ Delete Subscription
- ✅ Add Tags to Subscription
- ✅ List Subscriber IDs
- ✅ Retrieve Single Post
- ✅ Search Posts
- ✅ Retrieve Segments

## Installation

```bash
pip install -r requirements.txt
```

## API Documentation

- Official API Docs: https://developers.beehiiv.com
- Rate Limiting: https://developers.beehiiv.com/welcome/rate-limiting

## Authentication

Get your API key from [Beehiiv Settings](https://app.beehiiv.com/settings/api).

You need:
- API Key (Bearer token)
- Publication ID (format: `pub_xxxxxxxxxxxxxxxxx`)

## Usage

### Basic Setup

```python
import asyncio
from beehiiv_client import BeehiivAPIClient, SubscriptionCreateRequest

async def main():
    api_key = "your_api_key"
    publication_id = "pub_your_publication_id"

    async with BeehiivAPIClient(api_key=api_key, publication_id=publication_id) as client:
        # Create subscription
        request = SubscriptionCreateRequest(
            email="user@example.com",
            send_welcome_email=True
        )
        subscription = await client.create_subscription(request)
        print(f"Created: {subscription.id}")

asyncio.run(main())
```

### Create Subscription

```python
request = SubscriptionCreateRequest(
    email="subscriber@example.com",
    send_welcome_email=True,
    utm_source="website",
    utm_medium="organic",
    custom_fields=[
        {"name": "First Name", "value": "John"}
    ]
)

subscription = await client.create_subscription(request)
```

### Get Subscription

```python
# By ID
sub = await client.get_subscription_by_id("sub_xxx")

# By email
sub = await client.get_subscription_by_email("user@example.com")
```

### List Subscriptions

```python
result = await client.list_subscriptions(limit=10)

# Lightweight: IDs only
result = await client.list_subscriber_ids(limit=100)
```

### Update Subscription

```python
from beehiiv_client import SubscriptionUpdateRequest

request = SubscriptionUpdateRequest(tier="premium")
updated = await client.update_subscription("sub_xxx", request)
```

### Add Tags

```python
await client.add_tags_to_subscription("sub_xxx", ["VIP", "Active"])
```

### Posts

```python
# List posts
posts = await client.list_posts(limit=10, status="confirmed")

# Get single post
post = await client.get_post_by_id("post_xxx")

# Search posts
results = await client.search_posts(query="newsletter", status="confirmed")
```

### Segments

```python
segments = await client.list_segments()
for seg in segments["data"]:
    print(f"{seg.name}: {seg.count} subscribers")
```

### Delete Subscription

```python
success = await client.delete_subscription("sub_xxx")
```

## Response Objects

### Subscription

```python
@dataclass
class Subscription:
    id: str
    email: str
    status: str  # validating, active, etc.
    created: int  # Unix timestamp
    subscription_tier: str  # free, premium
    subscription_premium_tier_names: List[str]
    # ... UTM fields, custom_fields, etc.
```

## Rate Limits

See [Rate Limiting docs](https://developers.beehiiv.com/welcome/rate-limiting) for details.

## Testing

Run the example:

```bash
python test_beehiiv.py
```

## License

Part of the Skill Factory project.