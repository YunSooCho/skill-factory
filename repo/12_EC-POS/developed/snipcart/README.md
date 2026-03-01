# Snipcart Client

A Python client for the Snipcart REST API, providing complete access to checkout, orders, products, subscriptions, and more.

## Features

- **Orders**: Full order management and status updates
- **Customers**: Manage customer information
- **Products**: Catalog management with variants
- **Discounts**: Create and manage coupons
- **Subscriptions**: Recurring billing support
- **Refunds**: Process refunds on orders
- **Shipping**: Custom shipping rates
- **Taxes**: Tax configuration
- **Webhooks**: Subscribe to checkout events
- **Analytics**: Sales and order insights

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

### Getting API Credentials

1. Log into your [Snipcart Dashboard](https://app.snipcart.com/dashboard/account/apikeys)
2. Go to **Account → API Keys**
3. Copy your:
   - **Public key**: For storefront integration
   - **Secret key**: For server-side operations (required for this client)

### Environment Variables

Set the following environment variable:

```bash
export SNIPCART_API_SECRET="your_secret_key_from_dashboard"
# Optional, for storefront operations
export SNIPCART_API_KEY="your_public_key"
```

## Usage Example

```python
from snipcart import SnipcartClient

# Initialize client
client = SnipcartClient(api_secret="xxxxx")

# List orders
orders = client.list_orders(limit=50)
print(f"Total orders: {orders['totalItems']}")

# Get a specific order
order = client.get_order("abc123")
print(f"Order total: ${order['total']}")

# Update order status
updated = client.update_order_status(
    order_id="abc123",
    status="Processed",
    email_customer=True,
    comment="Order has been fulfilled"
)

# Process an order
processed = client.process_order("abc123", email_customer=True)

# Customers
customers = client.list_customers(limit=50)
customer = client.get_customer_by_email("john@example.com")

# Update customer
updated_customer = client.update_customer(customer_id, {
    "name": "John Smith"
})

# Products
products = client.list_products(limit=50)
product = client.get_product_by_user_id("TSHIRT-001")

# List product variants
variants = client.list_product_variants(product_id="prod123")

# Update product variant
client.update_product_variant(
    product_id="prod123",
    variant_id="var456",
    {"price": 29.99}
)

# Discounts (Coupons)
discounts = client.list_discounts()

# Create a discount
new_discount = client.create_discount({
    "name": "Summer Sale",
    "code": "SUMMER20",
    "type": "Percentage",
    "amount": 20,
    "maxNumberOfUsages": 100,
    "triggers": {
        "minimumAmount": {
            "amount": 50
        }
    }
})

# Update discount
client.update_discount(discount_id, {"amount": 25})

# Archive discount
client.archive_discount(discount_id)

# List subscriptions
subscriptions = client.list_subscriptions(limit=50)
subscription = client.get_subscription("sub123")

# Cancel subscription (at end of billing cycle)
cancelled = client.cancel_subscription(sub_id, end_now=False)

# Cancel immediately
cancelled = client.cancel_subscription(sub_id, end_now=True)

# Pause subscription
paused = client.pause_subscription(sub_id)

# Resume subscription
resumed = client.resume_subscription(sub_id)

# Subscription plans
plans = client.list_plans()

# Create a subscription plan
new_plan = client.create_plan({
    "name": "Monthly Box",
    "productId": "prod123",
    "variantId": "var456",
    "interval": "Month",
    "intervalCount": 1,
    "trialPeriodInDays": 7,
    "initialCharge": 0
})

# Refunds
refunds = client.list_refunds()

# Create a refund
new_refund = client.create_refund(
    order_id="abc123",
    items=[{
        "itemId": "item456",
        "quantity": 1,
        "amount": 29.99
    }],
    notify_customer=True
)

# Carts
carts = client.list_carts()
cart = client.get_cart("cart789")

# Taxes
taxes = client.list_taxes()
tax = client.get_tax("tax123")

# Update tax configuration
updated = client.update_tax(tax_id, {
    "name": "California Sales Tax",
    "rate": 8.75,
    "taxes": [{
        "rate": 8.75,
        "type": "State"
    }]
})

# Shipping rates
shipping_rates = client.list_shipping_rates()

# Create custom shipping rate
new_rate = client.create_shipping_rate({
    "description": "Free Shipping",
    "cost": 0,
    "type": "Fixed",
    "triggers": {
        "minimumAmount": {
            "amount": 100
        }
    },
    "destinations": [
        {"countryCode": "US"}
    ]
})

# Webhooks
webhooks = client.list_webhooks()

# Create webhook
new_webhook = client.create_webhook(
    url="https://your-server.com/webhooks/snipcart",
    events=[
        "order.created",
        "order.completed",
        "subscription.paused",
        "subscription.resumed"
    ],
    secret="your_webhook_secret"
)

# Update webhook
client.update_webhook(webhook_id, {
    "url": "https://new-url.com/webhooks"
})

# Test webhook
test_result = client.test_webhook(webhook_id)

# Delete webhook
client.delete_webhook(webhook_id)

# Analytics
sales_stats = client.get_sales_stats(
    from_date="2024-01-01",
    to_date="2024-12-31"
)

orders_stats = client.get_orders_stats(
    from_date="2024-01-01",
    to_date="2024-12-31"
)

top_products = client.get_top_products(limit=10)

# Categories
categories = client.list_categories()
category = client.get_category("cat123")

# Use context manager
with SnipcartClient(api_secret="xxxxx") as client:
    orders = client.list_orders()
    customers = client.list_customers()
```

## Discount Types

Snipcart supports several discount types:

- **FixedAmount**: Fixed monetary discount
- **Percentage**: Percentage-based discount
- **Shipping**: Free or reduced shipping
- **RatePerItem**: Rate per item quantity
- **PerQuantityTier**: Tiered quantity discounts

## Subscription Intervals

Supported billing intervals:

- **Month**: Monthly billing
- **Week**: Weekly billing
- **Day**: Daily billing

## Webhook Events

Available webhook event types:

### Orders
- `order.created`
- `order.completed`
- `order.updated`
- `order.trackingadded`
- `order.statuschanged`

### Subscriptions
- `subscription.created`
- `subscription.paused`
- `subscription.resumed`
- `subscription.cancelled`
- `subscription.updated`
- `subscription.paymentfailed`
- `subscription.invoicecreated`

### Customers
- `customer.updated`

## Order Status Flow

The order lifecycle:

1. **InProgress**: Order placed, payment pending
2. **Processed**: Payment authorized, ready for fulfillment
3. **Incomplete**: Payment failed or abandoned

You can also add custom statuses like "Shipped", "Refunded", etc.

## API Documentation

For complete API reference, see: https://docs.snipcart.com/v3/api-reference/introduction

### Key Endpoints

| Resource | Methods |
|----------|---------|
| Orders | list_orders, get_order, get_order_by_invoice, update_order_status, process_order |
| Customers | list_customers, get_customer, get_customer_by_email, update_customer |
| Products | list_products, get_product, get_product_by_user_id, update_product |
| Variants | list_product_variants, get_product_variant, update_product_variant |
| Discounts | list_discounts, get_discount, create_discount, update_discount, delete_discount |
| Subscriptions | list_subscriptions, get_subscription, cancel_subscription, pause_subscription, resume_subscription |
| Plans | list_plans, get_plan, create_plan, update_plan, delete_plan |
| Refunds | list_refunds, get_refund, create_refund |
| Shipping | list_shipping_rates, get_shipping_rate, create_shipping_rate, update_shipping_rate |
| Taxes | list_taxes, get_tax, update_tax |
| Webhooks | list_webhooks, get_webhook, create_webhook, update_webhook, delete_webhook, test_webhook |
| Analytics | get_sales_stats, get_orders_stats, get_top_products |
| Categories | list_categories, get_category, update_category |

## Notes

- Maximum items per page is 100
- API uses HTTP Basic Authentication with Secret API key
- All monetary values are in your configured currency
- Dates should be in ISO 8601 format
- Webhook signatures can be verified using the secret key set during webhook creation
- Subscriptions require an active billing method

## Requirements

- Python 3.7+
- requests>=2.31.0

## License

MIT License