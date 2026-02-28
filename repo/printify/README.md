# Printify Client

A Python client for the Printify REST API, providing complete access to print-on-demand product creation, order management, and fulfillment.

## Features

- **Shops**: Manage connected sales channels (Shopify, Etsy, WooCommerce, etc.)
- **Products**: Create, update, delete, and publish POD products
- **Orders**: Full order lifecycle management (draft → production → fulfilled)
- **Catalog**: Browse product blueprints, print providers, and variants
- **File Uploads**: Upload custom designs and images
- **Webhooks**: Subscribe to order events
- **Shipping**: Calculate costs and track shipments

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

### Getting API Credentials

1. Log into your [Printify Dashboard](https://printify.com/dashboard/)
2. Go to **Settings → General**
3. Click **Generate API Token**
4. Enter a name (e.g., "Yoom Integration")
5. Copy the generated API token

### Environment Variables

Set the following environment variable:

```bash
export PRINTIFY_API_KEY="printify_api_token"
```

## Usage Example

```python
from printify import PrintifyClient

# Initialize client
client = PrintifyClient(api_key="xxxxx")

# List connected shops
shops = client.list_shops()
print(f"Available shops: {shops}")
shop_id = shops[0]['id']

# List products in shop
products = client.list_products(shop_id)
print(f"Products in shop: {len(products)}")

# Create a product
new_product = client.create_product(shop_id, {
    "title": "Custom T-Shirt",
    "description": "<p>A beautiful custom t-shirt</p>",
    "tags": ["tshirt", "custom", "apparel"],
    "variants": [{
        "id": "12345",  # Variant ID from catalog
        "price": 29.99,
        "is_enabled": True
    }],
    "images": [{
        "src": "https://example.com/image.jpg",
        "variant_ids": ["12345"],
        "position": 1
    }]
})
print(f"Created product: {new_product['id']}")

# Update a product
updated = client.update_product(shop_id, product_id, {
    "title": "Updated T-Shirt"
})

# Publish product to sales channel
published = client.publish_product(shop_id, product_id, external=True)
print(f"External ID: {published.get('external_id')}")

# Unpublish product
client.unpublish_product(shop_id, product_id)

# Delete product
client.delete_product(shop_id, product_id)

# Orders
orders = client.list_orders(shop_id, status="processing")
order = client.get_order(shop_id, order_id="abc123")

# Create a new order
new_order = client.create_order(shop_id, {
    "external_id": "order-12345",
    "line_items": [{
        "product_id": product_id,
        "variant_id": "12345",
        "quantity": 2
    }],
    "shipping_method": "standard",
    "address_to": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "country": "US",
        "region": "New York",
        "address1": "123 Main St",
        "city": "New York",
        "zip": "10001"
    },
    "total_price": "59.98",
    "currency": "USD"
})

# Submit draft order for production
submitted = client.submit_order_for_production(shop_id, order_id)

# Calculate shipping cost before creating order
shipping = client.calculate_shipping_cost(shop_id, order_data)

# Get shipment tracking info
shipment = client.get_order_shipment_info(shop_id, order_id)

# Cancel order (draft status only)
client.cancel_order(shop_id, order_id)

# Browse catalog blueprints
blueprints = client.list_blueprints()

# Get specific blueprint details
blueprint = client.get_blueprint(blueprint_id="123")

# Get print providers for a blueprint
providers = client.list_print_providers(blueprint_id="123")
for provider in providers:
    print(f"Provider: {provider['title']}")

# Get variants for a print provider
variants = client.get_print_provider_variants(
    blueprint_id="123",
    print_provider_id="5"
)

# Get mockup configurations
mockups = client.get_print_provider_mockups(
    blueprint_id="123",
    print_provider_id="5"
)

# Upload an image
upload = client.upload_image("/path/to/design.jpg")
image_url = upload['src']

# Upload image from URL
upload = client.upload_image_from_url(
    "https://example.com/image.jpg",
    "design.jpg"
)

# Webhooks
webhooks = client.list_webhooks(shop_id)

# Create webhook for order events
webhook = client.create_webhook(
    shop_id=shop_id,
    topic="order.created",
    url="https://your-server.com/webhooks/printify",
    signing_key="your_secret_key"
)

# Delete webhook
client.delete_webhook(shop_id, webhook_id)

# Get store settings
settings = client.get_store_settings(shop_id)

# Update store settings
client.update_store_settings(shop_id, {
    "sales_channels": [
        {"type": "shopify", "id": "shop123"}
    ]
})

# Filter blueprints with pagination
filtered = client.filter_blueprints(
    limit=50,
    offset=0,
    category_id=10
)

# Use context manager
with PrintifyClient(api_key="xxxxx") as client:
    shops = client.list_shops()
    products = client.list_products(shops[0]['id'])
```

## Creating Products with Custom Designs

```python
# 1. Upload your design
upload_response = client.upload_image("/path/to/design.png")
design_url = upload_response['src']

# 2. Get blueprint and print provider
blueprints = client.list_blueprints()
tshirt_blueprint = [b for b in blueprints if 't-shirt' in b['title'].lower()][0]

providers = client.list_print_providers(tshirt_blueprint['id'])
provider = providers[0]

# 3. Get variants
variants = client.get_print_provider_variants(
    blueprint_id=tshirt_blueprint['id'],
    print_provider_id=provider['id']
)

# 4. Create product with design
product_data = {
    "title": "My Custom T-Shirt",
    "description": "<p>Stunning custom design</p>",
    "tags": ["custom", "premium"],
    "variants": [
        {
            "id": variants['variants'][0]['id'],  # First variant
            "price": 34.99,
            "is_enabled": True,
            "options": { "Color": "White", "Size": "M" }
        }
    ],
    "images": [{
        "src": design_url,
        "variant_ids": [variants['variants'][0]['id']],
        "position": 1
    }]
}

product = client.create_product(shop_id, product_data)

# 5. Publish to sales channel
client.publish_product(shop_id, product['id'], external=True)
```

## API Documentation

For complete API reference, see: https://developers.printify.com/

### Key Endpoints

| Resource | Methods |
|----------|---------|
| Shops | list_shops, get_shop |
| Products | list_products, get_product, create_product, update_product, delete_product |
| Product Actions | publish_product, unpublish_product, set_product_visibility |
| Orders | list_orders, get_order, create_order, submit_order_for_production |
| Shipping | calculate_shipping_cost, get_order_shipment_info |
| Catalog | list_blueprints, get_blueprint, list_print_providers |
| Prints | get_print_provider_variants, get_print_provider_mockups |
| Uploads | upload_image, upload_image_from_url |
| Webhooks | list_webhooks, get_webhook, create_webhook, delete_webhook |
| Settings | get_store_settings, update_store_settings |

### Blueprint Categories

Common blueprint categories:
- Apparel (T-shirts, Hoodies, etc.)
- Phone Cases
- Wall Art (Posters, Canvas)
- Accessories (Mugs, Bags)
- Home Decor

### Order Status Flow

1. `draft` - Order created, not yet submitted
2. `processing()` - Submitted for production
3. `fulfilled` - Shipped to customer
4. `failed` - Production or shipping issue

### Webhook Topics

- `order.created` - New order created
- `order.updated` - Order updated
- `order.sent` - Sent to production
- `order.fulfilled` - Order shipped
- `order.cancelled` - Order cancelled

## Notes

- Maximum file upload size: 50MB
- Supported image formats: PNG, JPG, JPEG
- Products can have multiple variants (colors, sizes)
- Each variant can have different pricing
- Mockups are automatically generated for variants
- Webhook signatures should be verified using your signing_key
- All prices are in the store's configured currency

## Requirements

- Python 3.7+
- requests>=2.31.0

## License

MIT License