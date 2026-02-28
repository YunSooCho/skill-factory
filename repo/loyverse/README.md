# Loyverse Client

A Python client for the Loyverse POS REST API, providing complete access to items, customers, orders, inventory, and more.

## Features

- **Items**: Create, update, delete products
- **Categories**: Manage item categories
- **Customers**: Customer management and loyalty points
- **Orders**: Retrieve order history
- **Inventory**: Stock tracking and adjustments
- **Stores**: Location management
- **Tax Rates**: Tax configuration
- **Discounts**: Discount management
- **Shifts**: Employee shift tracking

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

### Getting API Credentials

1. Log into your [Loyverse Back Office](https://backoffice.loyverse.com/)
2. Go to **Settings → Integrations → Loyverse POS API**
3. Click **Generate API Key**
4. Copy the generated API key

### Environment Variables

Set the following environment variable:

```bash
export LOYVERSE_API_KEY="your_api_key_from_backoffice"
```

## Usage Example

```python
from loyverse import LoyverseClient

# Initialize client
client = LoyverseClient(api_key="xxxxx")

# List items
items = client.list_items(start_index=0, count=50)
print(f"Total items: {items['total']}")

# Get specific item
item = client.get_item("item123")
print(f"Item: {item['name']} - ${item['price']}")

# Create item
new_item = client.create_item({
    "name": "Coffee",
    "category_id": "cat123",
    "price": 3.50,
    "cost": 1.00,
    "sku": "COFFEE-001",
    "is_active": True
})

# Update item
updated = client.update_item(item_id="item123", {"price": 4.00})

# List categories
categories = client.list_categories()

# Create category
new_category = client.create_category({
    "name": "Drinks",
    "color_hex": "#FF5722"
})

# Customers
customers = client.list_customers()
customer = client.get_customer("cust456")

# Create customer
new_customer = client.create_customer({
    "name": "John Doe",
    "phone": "+1234567890",
    "email": "john@example.com",
    "note": "VIP customer",
    "comment": "Prefers dark roast"
})

# Add loyalty points
updated_customer = client.add_customer_points(
    customer_id="cust456",
    points=100,
    reason="Purchase bonus"
)

# Orders
orders = client.list_orders(
    start_index=0,
    count=50,
    from_date="1704067200",  # Unix timestamp
    to_date="1706745600"
)

order = client.get_order("order789")

# Inventory tracks
inventory_tracks = client.list_inventory_tracks()

# Get inventory levels
inventory = client.get_inventory_levels(store_id="store123")

# Adjust inventory
adjustment = client.adjust_inventory(
    item_id="item123",
    quantity=-5,  # Remove 5 items
    store_id="store123",
    reason="Sale"
)

# Stores
stores = client.list_stores()
store = client.get_store("store123")

# Tax rates
tax_rates = client.list_tax_rates()

# Units
units = client.list_units()

# Modifier groups
modifier_groups = client.list_modifier_groups()
mod_group = client.get_modifier_group("mod123")

# Discounts
discounts = client.list_discounts()

# Payment types
payment_types = client.list_payment_types()

# Shifts
shifts = client.list_shifts()
shift = client.get_shift("shift456")

# Close shift
closed_shift = client.close_shift(shift_id="shift456")

# Receipt templates
templates = client.list_receipt_templates()

# Accounting categories
accounting_categories = client.list_accounting_categories()

# Account info
account = client.get_account_info()

# Use context manager
with LoyverseClient(api_key="xxxxx") as client:
    items = client.list_items()
    customers = client.list_customers()
    orders = client.list_orders()
```

## API Documentation

For complete API reference, see: https://help.loyverse.com/help/loyverse-pos-api

### Key Endpoints

| Resource | Methods |
|----------|---------|
| Items | list_items, get_item, create_item, update_item, delete_item |
| Categories | list_categories, get_category, create_category, update_category |
| Customers | list_customers, get_customer, create_customer, update_customer, delete_customer, add_customer_points |
| Orders | list_orders, get_order |
| Inventory | list_inventory_tracks, get_inventory_track, get_inventory_levels, adjust_inventory |
| Stores | list_stores, get_store |
| Tax Rates | list_tax_rates |
| Units | list_units |
| Discounts | list_discounts, get_discount |
| Shifts | list_shifts, get_shift, close_shift |
| Receipt Templates | list_receipt_templates, get_receipt_template |

## Inventory Adjustment Reasons

- **Sale**: Sale transaction
- **Purchase**: Purchase/stock receipt
- **Inventory**: Inventory count adjustment
- **Return**: Customer return
- **Write-off**: Write-off/damage
- **Spoilage**: Spoiled goods
- **Theft**: Theft/loss

## Notes

- Maximum items per request is 100
- All monetary values are in your configured currency
- Dates in filter parameters use Unix timestamp format
- Loyvers e uses an item-based inventory system
- Categories can be organized hierarchically
- Loyalty points can be added or removed

## Requirements

- Python 3.7+
- requests>=2.31.0

## License

MIT License