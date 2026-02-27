# Beamer API Integration

## Overview
Beamer customer communication platform for product releases. Create posts, announcements, and changelog entries.

## Supported Features
- ✅ Create Post (Create announcement/changelog post)

## Setup

### 1. Get API Key
1. Sign up at https://www.getbeamer.com/
2. Go to Settings → API Keys
3. Generate your API key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_key = "your_beamer_api_key"
```

## Usage

### Basic Example
```python
import asyncio
from beamer_client import BeamerClient

async def main():
    api_key = "your_key"

    async with BeamerClient(api_key=api_key) as client:
        response = await client.create_post(
            title="New Feature Released",
            content="We've added...",
            category="new",
            publish=True
        )
        print(f"Post created: {response.post_id}")

asyncio.run(main())
```

### Post Categories
- `announcement` - General announcement
- `new` - New features
- `improvement` - Improvements
- `fix` - Bug fixes
- `comingsoon` - Coming soon

### Advanced Usage
```python
async def advanced_example():
    async with BeamerClient(api_key="your_key") as client:
        response = await client.create_post(
            title="Major Update",
            content="Check out our new features",
            html="<p>Rich HTML content</p>",
            category="announcement",
            publish=True,
            author_name="John Doe",
            author_email="john@example.com",
            image_url="https://example.com/image.png",
            external_url="https://yourapp.com/features"
        )
        print(f"URL: {response.url}")

asyncio.run(advanced_example())
```

## Integration Type
- **Type:** API Key
- **Authentication:** Bearer token (Authorization header)
- **Protocol:** HTTPS REST API

## Testability
- ✅ Create Post: Testable with valid API key

## Notes
- Posts can be saved as draft (publish=False)
- Categories help organize content
- HTML content supported for rich formatting
- Free tier available for testing