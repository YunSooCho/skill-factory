# Bitly API Integration

## Overview
Bitly API for URL shortening, management, and analytics. Create, search, and track click statistics for shortened links.

## Supported Features
- ✅ Create Bitlink - Shorten URLs
- ✅ Get Bitlink - Retrieve link details
- ✅ Search Bitlinks - Find by tags, query, or date
- ✅ Delete Bitlink - Remove links
- ✅ Expand Bitlink - Get original long URL
- ✅ Get Click Summary - Total click statistics
- ✅ Get Click Counts - Clicks over time

## Setup

### 1. Get Access Token
1. Sign up at [Bitly](https://bitly.com/)
2. Go to Settings → Developer Settings
3. Generate access token

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
access_token = "your_bitly_access_token"
```

## Usage

```python
from bitly_client import BitlyClient

client = BitlyClient(access_token="your_token")

# Create shortened link
bitlink = client.create_bitlink(
    long_url="https://example.com/very/long/path",
    title="Campaign Link",
    tags=["marketing", "q42024"]
)
print(f"Shortened: {bitlink.link}")

# Get details
details = client.get_bitlink(bitlink.id)
print(f"Created: {details.created_at}")

# Search by tags
links = client.search_bitlinks(tags=["marketing"], limit=20)

# Get click statistics
summary = client.get_click_summary(bitlink.id, unit="day", units=30)
print(f"Total clicks (30d): {summary.total_clicks}")

# Click breakdown
clicks = client.get_click_counts(bitlink.id, unit="day", units=30)
for day in clicks.clicks:
    print(f"{day['date']}: {day['clicks']} clicks")

# Expand link
long_url = client.expand_bitlink(bitlink.id)

client.close()
```

## Integration Type
- **Type:** API Key (OAuth Token)
- **Authentication:** Bearer token (Authorization header)
- **Protocol:** HTTPS REST API

## Testability
- ✅ URL operations: Testable with valid access token
- ✅ Analytics: Available for existing bitlinks

## Notes
- Free tier has rate limits (~1000 requests/hour)
- Custom domains require account upgrade
- Click aggregate with slight delay after link creation
- Tags are case-sensitive strings