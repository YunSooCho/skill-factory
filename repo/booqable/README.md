# Booqable API Integration

## Overview
Complete Booqable rental inventory management API client for Yoom automation. Supports orders, products, customers, stock management, and workflows.

## Supported Features
- ✅ Create and manage rental orders
- ✅ Product and product group management
- ✅ Customer management
- ✅ Stock/inventory tracking
- ✅ Location management
- ✅ Tax rate configuration
- ✅ Invoice and document generation
- ✅ Webhook integrations
- ✅ Order confirmation and cancellation

## Setup

### 1. Get API Key
Visit https://app.booqable.com/settings/api to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export BOOQABLE_API_KEY="your_api_key_here"
```

## Usage

### Creating a Rental Order
```python
import os
from booqable_client import BooqableAPIClient

os.environ['BOOQABLE_API_KEY'] = 'your_api_key'

client = BooqableAPIClient()

# Create order
order = client.create_order(
    customer_id='cust_123',
    start_date='2024-01-15',
    end_date='2024-01-20',
    order_items=[
        {'product_id': 'prod_456', 'quantity': 2},
        {'product_id': 'prod_789', 'quantity': 1}
    ],
    notes='Event rental request',
    status='concept'
)

# Confirm order
client.confirm_order(order['id'])

client.close()
```

### Managing Products and Customers
```python
# List products
products = client.list_products()

# Create customer
customer = client.create_customer(
    first_name='John',
    last_name='Doe',
    email='john@example.com',
    company='Acme Corp'
)

# Check stock
stock = client.list_stock_items(product_id='prod_456')
```

### Webhooks
```python
# Create webhook
client.create_webhook(
    url='https://your-app.com/webhooks/booqable',
    events=['order.confirmed', 'order.cancelled']
)
```

## Integration Type
- **Type:** API Key (Token)
- **Authentication:** Token header
- **Protocol:** HTTPS REST API
- **Focus:** Rental inventory management

## Testability
- ✅ Sandbox environment available
- ✅ All API actions testable
- ✅ Free trial for development

## Notes
- Specialized for rental businesses
- Comprehensive inventory tracking
- Multi-location support
- Automatic pricing calculations
- Integrated with payment providers