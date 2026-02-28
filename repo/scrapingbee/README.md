# ScrapingBee API Client

Python client for [ScrapingBee](https://www.scrapingbee.com/) - Web scraping API with headless browser support.

## Features

- ✅ Scrape static and dynamic websites
- ✅ JavaScript rendering
- ✅ CSS selector data extraction
- ✅ Screenshot capture
- ✅ Proxy support
- ✅ Country-specific geolocation

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from scrapingbee.client import ScrapingBeeClient

client = ScrapingBeeClient(api_key="your_api_key")

# Basic scraping
result = client.scrape("https://example.com")
print(result)

# Scrape with JavaScript rendering
html = client.scrape_html("https://dynamic-site.com", render_js=True)

# Extract specific data
extract_rules = {
    "title": "h1",
    "content": ".content p"
}
data = client.scrape_text("https://site.com", extract_rules=extract_rules)
print(data)
```