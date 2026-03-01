# WooCommerce Client

A Python client for the WooCommerce REST API, providing complete access to products, orders, customers, coupons, and store settings.

## Features

- **Products**: Full CRUD operations with variations management
- **Orders**: Create, retrieve, update, and manage orders
- **Customers**: Manage customer accounts and data
- **Coupons**: Create and manage discount coupons
- **Categories**: Manage product categories
- **Reports**: Generate sales and top-seller reports
- **Webhooks**: Subscribe to store events
- **Payment Gateways**: Configure payment methods
- **Shipping Methods**: Manage shipping options
- **Settings**: Access and update store settings

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

### Getting API Credentials

1. Log into your WordPress Admin Panel
2. Go to **WooCommerce → Settings → Advanced → REST API**
3. Click **Add Key**
4. Enter a description (e.g., "Yoom Integration")
5. Choose permissions:
   - **Read/Write** - Full access required for most operations
   - Or customize: Read products, Write products, Read orders, Write orders, etc.
6. Click **Generate API Key**
7. Copy the **Consumer Key** and **Consumer Secret**

### Environment Variables

Set the following environment variables:

```bash
export WOOCOMMERCE_STORE_URL="https://yourstore.com"
export WOOCOMMERCE_CONSUMER_KEY="ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export WOOCOMMERCE_CONSUMER_SECRET="cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## Usage Example

```python
from woocommerce import WooCommerceClient

# Initialize client
client = WooCommerceClient(
    store_url="https://mystore.com",
    consumer_key="ck_xxxxx",
    consumer_secret="cs_xxxxx"
)

# List products
products = client.list_products(page=1, per_page=20)
print(f"Found {len(products)} products")

# Get product details
product = client.get_product(123)
print(f"Product: {product['name']} - ${product['regular_price']}")

# Create a product
new_product = client.create_product({
    "name": "Awesome T-Shirt",
    "type": "simple",
    "regular_price": "29.99",
    "description": "<p>An amazing t-shirt</p>",
    "short_description": "Awesome t-shirt",
    "sku": "TSHIRT-001",
    "manage_stock": True,
    "stock_quantity": 100,
    "categories": [{"id": 15}]
})
print(f"Created product: {new_product['id']}")

# Update a product
updated = client.update_product(123, {
    "regular_price": "34.99"
})

# Delete a product (move to trash)
deleted = client.delete_product(123)
# Permanently delete
deleted = client.delete_product(123, force=True)

# Batch operations
batch = client.batch_products({
    "create": [{
        "name": "Product 1",
        "regular_price": "10.00"
    }],
    "update": [{
        "id": 123,
        "regular_price": "15.00"
    }]
})

# Product variations
variations = client.list_variations(product_id=456)
variation = client.create_variation(456, {
    "regular_price": "39.99",
    "attributes": [{"name": "Size", "option": "Large"}]
})

# Orders
orders = client.list_orders(status="processing", page=1)
order = client.get_order(789)

# Create an order
new_order = client.create_order({
    "payment_method": "bacs",
    "payment_method_title": "Direct Bank Transfer",
    "set_paid": True,
    "billing": {
        "first_name": "John",
        "last_name": "Doe",
        "address_1": "123 Main St",
        "city": "New York",
        "state": "NY",
        "postcode": "10001",
        "country": "US",
        "email": "john@example.com",
        "phone": "+1234567890"
    },
    "shipping": {
        "first_name": "John",
        "last_name": "Doe",
        "address_1": "123 Main St",
        "city": "New York",
        "state": "NY",
        "postcode": "10001",
        "country": "US"
    },
    "line_items": [{
        "product_id": 123,
        "quantity": 2
    }],
    "shipping_lines": [{
        "method_id": "flat_rate",
        "method_title": "Flat Rate",
        "total": "10.00"
    }]
})

# Update order status
client.update_order_status(789, "completed")

# Customers
customers = client.list_customers(search="john@example.com")
customer = client.create_customer({
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "billing": {
        "first_name": "Jane",
        "last_name": "Smith",
        "address_1": "456 Oak Ave",
        "city": "Los Angeles",
        "postcode": "90001",
        "country": "US"
    }
})

# Coupons
coupons = client.list_coupons()
coupon = client.create_coupon({
    "code": "SAVE20",
    "amount": "20.00",
    "discount_type": "percent",
    "description": "20% off all products",
    "individual_use": False
})

# Categories
categories = client.list_categories()
category = client.create_category({
    "name": "New Arrivals",
    "parent": 0
})

# Reports
sales_report = client.get_sales_report(period="last_30_days")
top_sellers = client.get_top_sellers_report(period="7days", limit=10)

# Webhooks
webhooks = client.list_webhooks()
new_webhook = client.create_webhook(
    name="Order Created",
    topic="order.created",
    delivery_url="https://your-server.com/webhooks/woocommerce"
)

# Payment gateways
gateways = client.list_payment_gateways()
gateway = client.get_payment_gateway("stripe")

# Shipping methods
methods = client.list_shipping_methods()

# System status
status = client.get_system_status()

# Settings (read/update)
general_settings = client.get_settings(group="general")
updated = client.update_settings("products", {
    "woocommerce_shop_currency": "USD"
})

# Use context manager
with WooCommerceClient(
    store_url="https://mystore.com",
    consumer_key="ck_xxxxx",
    consumer_secret="cs_xxxxx"
) as client:
    products = client.list_products()
```

## API Documentation

For complete API reference, see: https://woocommerce.github.io/woocommerce-rest-api-docs/

### Key Endpoints

| Resource | Methods |
|----------|---------|
| Products | list_products, get_product, create_product, update_product, delete_product, batch_products |
| Variations | list_variations, get_variation, create_variation, update_variation, delete_variation |
| Orders | list_orders, get_order, create_order, update_order, delete_order, update_order_status |
| Customers | list_customers, get_customer, create_customer, update_customer, delete_customer |
| Coupons | list_coupons, get_coupon, create_coupon, update_coupon, delete_coupon |
| Categories | list_categories, get_category, create_category, update_category, delete_category |
| Reports | get_sales_report, get_top_sellers_report |
| Webhooks | list_webhooks, get_webhook, create_webhook, update_webhook, delete_webhook |
| Gateways | list_payment_gateways, get_payment_gateway, update_payment_gateway |
| Shipping | list_shipping_methods, get_shipping_method |
| Settings | get_settings, update_settings |
| System | get_system_status |

### Order Status Types

- `pending` - Payment pending
- `processing` - Payment received, order processing
- `on-hold` - Awaiting payment or confirmation
- `completed` - Order fulfilled
- `cancelled` - Order cancelled
- `refunded` - Order refunded
- `failed` - Payment failed

### Product Types

- `simple` - Simple product
- `variable` - Variable product with variations
- `grouped` - Grouped product
- `external` - External/affiliate product

### Coupon Discount Types

- `percent` - Percentage discount
- `fixed_cart` - Fixed cart discount
- `fixed_product` - Fixed product discount

## Notes

- Maximum items per page is 100
- Use `force=True` parameter for permanent deletion
- Dates should be in ISO 8601 format or YYYY-MM-DD
- The API uses HTTP Basic Authentication (OAuth 1.0a)
- Rate limiting depends on your hosting provider

## Requirements

- Python 3.7+
- requests>=2.31.0

## License

MIT License