# Beamer API Client

Python async client for [Beamer API](https://www.getbeamer.com/api) - a user engagement and notification platform for announcing product updates, news, and features.

## Features

- ✅ Create Posts
- ✅ Multi-language support
- ✅ Segmentation filters
- ✅ Push notifications
- ✅ Analytics tracking

## Installation

```bash
pip install -r requirements.txt
```

## API Documentation

- Official API Docs: https://www.getbeamer.com/api
- Settings & API Key: https://app.getbeamer.com/settings

## Authentication

Get your API key from Beamer Settings → API.

**Rate Limits:**
- 30 requests/second (paid accounts)
- Monthly limits:
  - Free: 1,000 requests
  - Starter: 2,000 requests
  - Pro: 20,000 requests
  - Scale: 100,000 requests

## Usage

### Basic Setup

```python
import asyncio
from beamer_client import BeamerAPIClient, PostCreation

async def main():
    api_key = "your_api_key_here"

    async with BeamerAPIClient(api_key=api_key) as client:
        # Test connection
        status = await client.ping()
        print(f"Connected to: {status.get('name')}")

        # Create a post
        post_data = PostCreation(
            title=["New Feature Released"],
            content=["We've just released an exciting new feature!"],
            category="new",
            publish=True
        )

        post = await client.create_post(post_data)
        print(f"Created post: {post.id}")

asyncio.run(main())
```

### Create Post (Single Language)

```python
post_data = PostCreation(
    title="Product Update v2.0",
    content="Check out our latest features...",
    category="new",
    publish=True
)

post = await client.create_post(post_data)
```

### Create Post (Multiple Translations)

```python
post_data = PostCreation(
    title=["Mise à jour", "Actualización", "Update"],
    content=[
        "Nouvelle fonctionnalité disponible",
        "Nueva característica disponible",
        "New feature available"
    ],
    category="new",
    language=["FR", "ES", "EN"],
    link_url=["https://example.com/fr", "https://example.com/es", "https://example.com/en"],
    link_text=["En savoir plus", "Más información", "Learn more"],
    publish=True
)

post = await client.create_post(post_data)
```

### Segmented Post

```python
# Post only visible to admins segment
post_data = PostCreation(
    title=["Internal Announcement"],
    content=["Team update for admins"],
    filter="admins",
    publish=True
)

post = await client.create_post(post_data)
```

### Get Posts

```python
# Get published posts
posts = await client.get_posts(published=True, max_results=10)

# Filter by category
posts = await client.get_posts(category="new", max_results=5)

# Filter by date range
posts = await client.get_posts(
    date_from="2024-01-01T00:00:00Z",
    date_to="2024-12-31T23:59:59Z"
)
```

### Get Single Post

```python
post = await client.get_post_by_id("12345")
print(f"Post: {post.translations[0].title}")
print(f"Views: {post.views}, Clicks: {post.clicks}")
```

### Delete Post

```python
success = await client.delete_post("12345")
```

## PostCreation Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | `List[str]` | ✅ Yes | Post titles (one per translation) |
| content | `List[str]` | ✅ Yes | Post content (one per translation) |
| language | `List[str]` | No | ISO 639 codes (e.g., `["EN", "FR"]`) |
| category | `str` | No | Category for organization |
| publish | `bool` | No | Whether to publish (default: `True`) |
| archive | `bool` | No | Whether to archive (default: `False`) |
| pinned | `bool` | No | Whether to pin (default: `False`) |
| show_in_widget | `bool` | No | Show in widget (default: `True`) |
| show_in_standalone | `bool` | No | Show in standalone (default: `True`) |
| link_url | `List[str]` | No | CTA URLs (one per translation) |
| link_text | `List[str]` | No | CTA text (one per translation) |
| filter | `str` | No | Segmentation filter |
| filter_url | `str` | No | URL segmentation |
| filter_user_id | `str` | No | User ID for single-user posts |
| date | `str` | No | Publication date (ISO 8601) |
| due_date | `str` | No | Expiration date (ISO 8601) |
| enable_feedback | `bool` | No | Enable feedback (default: `True`) |
| enable_reactions | `bool` | No | Enable reactions (default: `True`) |
| enable_social_share | `bool` | No | Enable social share (default: `True`) |
| auto_open | `bool` | No | Auto open widget (default: `False`) |
| send_push_notification | `bool` | No | Send push (default: `True`) |
| boosted_announcement | `str` | No | "snippet" or "large" |
| links_in_new_window | `bool` | No | Open links in new tab (default: `True`) |

## Response Objects

### Post

```python
@dataclass
class Post:
    id: str
    date: str
    due_date: Optional[str]
    published: bool
    pinned: bool
    show_in_widget: bool
    show_in_standalone: bool
    category: str
    boosted_announcement: Optional[str]
    translations: List[PostTranslation]
    filter: Optional[str]
    filter_url: Optional[str]
    filter_user_id: Optional[str]
    auto_open: bool
    edition_date: str
    feedback_enabled: bool
    reactions_enabled: bool
    views: int
    unique_views: int
    clicks: int
    feedbacks: int
    positive_reactions: int
    neutral_reactions: int
    negative_reactions: int
```

### PostTranslation

```python
@dataclass
class PostTranslation:
    title: str
    content: str
    language: str
    category: Optional[str]
    link_url: Optional[str]
    link_text: Optional[str]
    images: Optional[List[str]]
```

## Error Handling

```python
try:
    post = await client.create_post(post_data)
except Exception as e:
    if "Authentication failed" in str(e):
        print("Invalid API key")
    elif "Rate limit exceeded" in str(e):
        print("Monthly limit reached")
    else:
        print(f"Error: {e}")
```

## Testing

Run the example script to test your API key:

```bash
python test_beamer.py
```

## License

This implementation is part of the Skill Factory project.