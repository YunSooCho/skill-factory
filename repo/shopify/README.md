# Shopify Client

A Python client for the Shopify Admin REST API, providing complete access to products, orders, customers, inventory, and more.

## Features

- **Products**: Create, read, update, delete products with variants and images
- **Orders**: List, create, update, cancel, and manage orders
- **Customers**: Manage customer data and search
- **Inventory**: Track and adjust inventory levels across locations
- **Collections**: Manage product collections
- **Locations**: Fetch store locations
- **Metafields**: Add custom data to products
- **Webhooks**: Subscribe to store events

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

### Option 1: Admin API Access Token (Recommended)

1. Go to Shopify Admin: `https://{your-store}.myshopify.com/admin/settings/apps/sales_channels/shopify-api/credentials`
2. Click "Create API credential"
3. Select "Admin API access" and authenticate
4. Configure access scopes:
   - `read_products`, `write_products` - Product management
   - `read_orders`, `write_orders` - Order management
   - `read_customers`, `write_customers` - Customer management
   - `read_inventory`, `write_inventory` - Inventory management
   - `read_locations` - Location access
   - `read_webhooks`, `write_webhooks` - Webhook management
5. Click "Install app" to generate access token
6. Copy the access token

### Option 2: API Key + Password (Legacy)

1. Go to Shopify Admin → Settings → Apps and sales channels → Develop apps
2. Create custom app
3. Configure Admin API scopes
4. Install app and get API key and password

### Environment Variables

Set the following environment variables:

```bash
export SHOPIFY_STORE_NAME="your-store-name"  # From your-store.myshopify.com
export SHOPIFY_ACCESS_TOKEN="your-admin-api-token"
# OR for legacy auth:
# export SHOPIFY_API_KEY="your-api-key"
# export SHOPIFY_PASSWORD="your-password"
```

## Usage Example

```python
from shopify import ShopifyClient

# Initialize with access token
client = ShopifyClient(
    store_name="mystore",
    access_token="shpat_xxxxx"
)

# List products
products = client.list_products(limit=50)
print(f"Found {len(products['products'])} products")

# Create a product
new_product = client.create_product({
    "title": "New T-Shirt",
    "body_html": "<p>Awesome t-shirt</p>",
    "vendor": "MyBrand",
    "product_type": "Apparel",
    "variants": [{
        "option1": "Medium",
        "price": "29.99",
        "sku": "TSHIRT-M",
        "inventory_quantity": 100
    }]
})
print(f"Created product: {new_product['product']['id']}")

# Update a product
updated = client.update_product(123456789, {
    "title": "Updated T-Shirt"
})

# List orders
orders = client.list_orders(status="open", limit=50)

# Create an order
new_order = client.create_order({
    "line_items": [{
        "product_id": 123456789,
        "quantity": 1
    }],
    "customer": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com"
    },
    "billing_address": {
        "first_name": "John",
        "last_name": "Doe",
        "address1": "123 Main St",
        "city": "New York",
        "country_code": "US",
        "zip": "10001"
    },
    "financial_status": "paid"
})

# Create a customer
customer = client.create_customer({
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "accepts_marketing": True
})

# Search customers
results = client.search_customers("john@example.com")

# Get inventory levels
inventory = client.list_inventory_levels(location_ids=[123456])

# Adjust inventory
client.update_inventory_levels(
    inventory_item_id="987654321",
    location_id="123456",
    available=50  # Adjust quantity
)

# Create webhook
webhook = client.create_webhook(
    topic="orders/create",
    address="https://your-server.com/webhooks/shopify"
)

# Use context manager
with ShopifyClient(store_name="mystore", access_token="shpat_xxxxx") as client:
    products = client.list_products()
```

## API Documentation

For complete API reference, see: https://shopify.dev/api/admin-rest

### Key Endpoints

| Resource | Methods |
|----------|---------|
| Products | list_products, get_product, create_product, update_product, delete_product |
| Orders | list_orders, get_order, create_order, update_order, cancel_order |
| Customers | list_customers, get_customer, search_customers, create_customer, update_customer |
| Inventory | list_inventory_levels, update_inventory_levels |
| Collections | list_collections, get_collection |
| Locations | list_locations, get_location |
| Webhooks | list_webhooks, create_webhook, delete_webhook |

## Notes

- The API version defaults to "2024-01" but can be changed via the `version` parameter
- Maximum request limit is 250 items per request
- All date parameters should be in ISO 8601 format
- The client handles automatic retry on rate limit errors (429 status)

## Requirements

- Python 3.7+
- requests>=2.31.0

## License

MIT License