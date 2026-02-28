# Ontraport API Integration

## Overview
Implementation of Ontraport CRM and marketing automation API for Yoom automation.

## Supported Features
- ✅ Contact: Create, Get, Update, Delete, Search
- ✅ Product: Create, Get, Update, Delete, Search
- ✅ Transaction: Get, Search
- ✅ Task: Create Task Message, Add to Contact

## Setup

### Get API Credentials
Visit https://admin.ontraport.com/#!/administration to get API ID and key.

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure
```python
from ontraport_client import OntraportClient, Contact, Product

api_id = "your_api_id"
api_key = "your_api_key"

async with OntraportClient(api_id=api_id, api_key=api_key) as client:
    pass
```

## Usage

```python
# Create contact
contact = Contact(
    first_name="John",
    last_name="Doe",
    email="john@example.com"
)
await client.create_contact(contact)

# Create product
product = Product(
    product_name="Premium Plan",
    price=99.99
)
await client.create_product(product)
```

## Notes
- Async operations with rate limiting
- Comprehensive marketing automation
- Contact, product, transaction management