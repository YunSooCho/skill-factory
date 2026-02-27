# Beehiiv API Integration

## Overview
Beehiiv newsletter platform for managing subscriptions, posts, and segments. Full API support for subscriber management, content publishing, and audience segmentation.

## Supported Features
- ✅ Create Subscription - Create new newsletter subscribers
- ✅ Retrieve Subscription by ID - Get subscription details
- ✅ Retrieve Subscription by Email - Find subscriber by email
- ✅ Update Subscription - Modify subscriber information
- ✅ Delete Subscription - Remove subscribers
- ✅ Add Tags to Subscription - Add tags for segmentation
- ✅ List Subscriber Ids - Get all subscriber IDs
- ✅ Retrieve a Single Post - Get post details
- ✅ Search Posts by Publication - List and filter posts
- ✅ Retrieve Segments - Get all audience segments

## Setup

### 1. Get API Key and Publication ID
1. Sign up at [Beehiiv](https://www.beehiiv.com/)
2. Go to Settings → API Keys
3. Generate your API key
4. Find your Publication ID (format: `pub_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_key = "your_beamer_api_key"
publication_id = "pub_00000000-0000-0000-0000-000000000000"
```

## Usage

### Basic Subscription Management
```python
from beehiiv_client import BeehiivClient

api_key = "your_api_key"
publication_id = "pub_00000000-0000-0000-0000-000000000000"

client = BeehiivClient(api_key=api_key, publication_id=publication_id)

# Create a new subscriber
subscription = client.create_subscription(
    email="subscriber@example.com",
    custom_fields=[
        {"name": "First Name", "value": "John"},
        {"name": "Last Name", "value": "Doe"}
    ],
    utm_source="website",
    utm_medium="form",
    send_welcome_email=True
)
print(f"Created: {subscription.id} - {subscription.email}")

# Retrieve by email
subscriber = client.get_subscription_by_email("subscriber@example.com")
print(f"Status: {subscriber.status}")

# Add tags for segmentation
tagged = client.add_tags_to_subscription(subscription.id, ["VIP", "Early Adopter"])
print(f"Tags: {tagged.tags}")

# Update subscriber
updated = client.update_subscription(
    subscription.id,
    {
        "custom_fields": [
            {"name": "Location", "value": "Tokyo"}
        ]
    }
)

# Close connection when done
client.close()
```

### Post Operations
```python
client = BeehiivClient(api_key=api_key, publication_id=publication_id)

# Get a specific post
post = client.get_post("post_id_here")
print(f"Post: {post.title}")

# Search posts with filters
posts = client.search_posts(
    limit=20,
    status="sent"  # Only sent posts
)

for post in posts:
    print(f"- {post.title} ({post.status})")

client.close()
```

### Segment Management
```python
client = BeehiivClient(api_key=api_key, publication_id=publication_id)

# Get all segments
segments = client.get_segments()

for segment in segments:
    print(f"{segment.name}: {segment.subscriber_count} subscribers")

client.close()
```

### Webhook Verification
```python
client = BeehiivClient(api_key=api_key, publication_id=publication_id)

# Verify incoming webhook
signature = request.headers.get("X-Signature")
payload = request.get_body()
webhook_secret = "your_webhook_secret"

if client.verify_webhook(signature, payload, webhook_secret):
    # Process webhook
    print("Webhook verified!")
else:
    print("Invalid webhook signature")

client.close()
```

### Subscription Tiers
```python
# Create a premium subscriber
subscription = client.create_subscription(
    email="premium@example.com",
    tier="premium",
    premium_tiers=["Gold", "VIP"]
)

# Upgrade existing subscriber
client.update_subscription(
    subscription.id,
    {"tier": "premium", "premium_tier_ids": ["tier_id_123"]}
)
```

### Advanced Options
```python
# Create with all available options
subscription = client.create_subscription(
    email="advanced@example.com",
    reactivate_existing=True,
    send_welcome_email=True,
    custom_fields=[
        {"name": "First Name", "value": "Jane"},
        {"name": "Last Name", "value": "Smith"},
        {"name": "Country", "value": "Japan"}
    ],
    utm_source="newsletter",
    utm_medium="referral",
    utm_campaign="growth_2024",
    utm_term="organic",
    utm_content="header_cta",
    referring_site="https://example.com",
    referral_code="FRIEND20",
    tier="free",
    premium_tiers=["Basic"],
    stripe_customer_id="cus_12345abc",
    double_opt_override="off",  # Skip double opt-in
    automation_ids=["auto_abc123"]  # Add to automations
)
```

## Integration Type
- **Type:** API Key
- **Authentication:** Bearer token (Authorization header)
- **Protocol:** HTTPS REST API
- **Version:** v2

## Rate Limiting
The client automatically handles rate limits:
- Monitors `X-RateLimit-Remaining` header
- Waits automatically when approaching limits
- Retries with exponential backoff on 429 errors

## Webhooks
Supported webhook events:
- **Subscription Created** - New subscriber added
- **Subscription Confirmed** - Double opt-in confirmed
- **Subscription Deleted** - Subscriber removed
- **Subscription Upgraded** - Tier upgrade
- **Subscription Downgraded** - Tier downgrade
- **Post Sent** - Newsletter published
- **Survey Response Submitted** - Survey responses

Use `verify_webhook()` method to authenticate incoming webhooks.

## Testability
- ✅ All 10 API actions: Testable with valid API key and publication ID
- ✅ Subscription operations: Test with test email addresses
- ✅ Post operations: Test reading existing posts
- ✅ Segments: Test retrieving segments

## Notes
- Publication ID is required for all operations
- Email addresses must be valid formats
- Custom fields must exist in publication before use
- Tags are case-sensitive
- Subscriptions support double opt-in (can be overridden)
- Premium tiers allow multiple concurrent assignments
- Rate limit is approximately 1000 requests per hour

## Error Handling
The client includes comprehensive error handling:
- Automatic retry for server errors (5xx)
- Rate limit detection and automatic waiting
- Clear error messages for 4xx errors
- Invalid parameter validation