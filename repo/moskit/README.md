# Moskit CRM API Integration

## Overview
Implementation of Moskit CRM API for sales pipeline management for Yoom automation.

## Supported Features
- ✅ Deal: Create, Get, Update, Delete, Search
- ✅ Company: Create, Get, Update, Delete, Search
- ✅ Contact: Create, Get, Update, Delete, Search
- ✅ Activity: Create, Get, Update, Delete, Search

## Setup

### Get API Key
Visit https://app.moskit.com/settings/api and obtain your API key.

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure
```python
from moskit_client import MoskitClient, Deal, Company, Contact

api_key = "your_moskit_api_key"

async with MoskitClient(api_key=api_key) as client:
    pass
```

## Usage

```python
# Create deal
deal = Deal(
    title="Enterprise Deal",
    value=50000.0,
    contact_id="contact_123"
)
await client.create_deal(deal)

# Search companies
companies = await client.search_company(industry="Technology")
```

## Notes
- Async operations with rate limiting
- Complete pipeline management
- Full CRUD for all entities