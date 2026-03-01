# Dub API Integration

## Overview
Implementation of Dub link management and short link API for Yoom automation.

## Supported Features

### API Actions (8 operations)
- ✅ Link: Create, Get, Update, Upsert, Delete, Search
- ✅ Tag: Create, Update, Delete, List
- ✅ Analytics: Get click statistics

### Triggers (2 events)
- ✅ Created Link
- ✅ Clicked Link

## Setup

### 1. Get API Credentials
1. Visit https://dub.co/ and sign up
2. Go to Settings > API Keys
3. Generate a new API token
4. Note your workspace ID (from URL or settings)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_token = "your_api_token"
workspace_id = "your_workspace_id"  # Optional, defaults to your primary workspace
```

## Usage

### Basic Example
```python
import asyncio
from dub_client import DubClient

async def main():
    api_token = "your_api_token"
    workspace_id = "ws_xxx"  # Optional

    async with DubClient(
        api_token=api_token,
        workspace_id=workspace_id
    ) as client:
        # Create short link
        link = await client.create_link(
            long_url="https://example.com/long-url",
            short_code="mylink"
        )
        print(f"Short URL: {link.short_url}")
```

### Link Management
```python
# Create link with tags and metadata
link = await client.create_link(
    long_url="https://example.com/product",
    short_code="product",
    title="Product Page",
    description="Official product landing page",
    tags=["product", "marketing"],
    domain="dub.co",
    public_stats=True
)

# Get link
link = await client.get_link(link.id)

# Update link
link = await client.update_link(
    link_id=link.id,
    title="Updated Title"
)

# Delete link
await client.delete_link(link.id)

# Get link by domain and key
link = await client.get_link_by_domain_key("dub.co", "product")
```

### Upsert Link
```python
# Create or update if exists
link = await client.upsert_link(
    domain="dub.co",
    key="promo-2024",
    url="https://example.com/promo",
    title="2024 Promotion",
    tags=["promo", "2024"]
)
```

### Search Links
```python
# Search by query
links = await client.search_links(query="marketing")

# Filter by tag
links = await client.search_links(tag_ids=["tag-1", "tag-2"])

# Filter by domain
links = await client.search_links(domain="dub.co")

# Archived links only
links = await client.search_links(archived=True)
```

### Tag Management
```python
# Create tag
tag = await client.create_tag(
    name="campaign-2024",
    color="#FF5733"
)

# Update tag
tag = await client.update_tag(
    tag_id=tag.id,
    color="#00BFFF"
)

# List all tags
tags = await client.list_tags()

# Delete tag
await client.delete_tag(tag.id)
```

### Analytics
```python
# Get click analytics
clicks = await client.get_clicks(
    link_id=link.id,
    start="2024-01-01",
    end="2024-12-31",
    limit=100
)

for click in clicks:
    print(f"Click from {click.city}, {click.country} via {click.device}")
```

## Integration Type
- **Type:** API Token (Bearer)
- **Authentication:** Bearer token in Authorization header
- **Protocol:** HTTPS REST API

## Testability
- ✅ All API actions testable with valid credentials
- ⚠️ Webhook triggers require public endpoint

## Webhook Setup

To receive triggers:
1. Go to Settings > Webhooks in Dub
2. Add your webhook endpoint URL
3. Select events to track:
   - `link.created` - When a new link is created
   - `link.clicked` - When a link is clicked
4. Dub will POST event data to your endpoint

Example webhook payload:
```json
{
  "event": "link.clicked",
  "data": {
    "link": {
      "id": "123",
      "shortLink": "https://dub.co/mylink",
      "url": "https://example.com"
    },
    "click": {
      "ip": "1.2.3.4",
      "city": "San Francisco",
      "country": "US",
      "device": "iPhone",
      "browser": "Safari"
    }
  },
  "createdAt": "2024-02-27T10:00:00Z"
}
```

## Advanced Features

### Custom Domain
```python
link = await client.create_link(
    long_url="https://example.com",
    domain="promo.yourbrand.com",  # Your custom domain
    short_code="launch"
)
```

### Link Expiration
```python
link = await client.create_link(
    long_url="https://example.com/limited",
    short_code="limited",
    expires_at="2024-12-31T23:59:59Z"
)
```

### Password Protection
```python
link = await client.create_link(
    long_url="https://example.com/private",
    short_code="private",
    password="secure123"
)
```