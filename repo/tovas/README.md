# Tovas API Client

Business management platform for invoicing, inventory, and financial operations.

## API Key Setup

1. Log in to [Tovas](https://tovas.com)
2. Go to Settings → API Integration
3. Generate your API key
4. Note your Account ID

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

```python
from tovas import TovasClient

# Initialize client
client = TovasClient(api_key='your_api_key', account_id='your_account_id')

# Get invoices
invoices = client.get_invoices()
print(f"Found {len(invoices.get('data', []))} invoices")

# Create an invoice
invoice_data = {
    'client_id': 'client_123',
    'invoice_date': '2024-02-15',
    'line_items': [{
        'product_id': 'prod_456',
        'quantity': 2,
        'unit_price': 50.00
    }]
}
invoice = client.create_invoice(invoice_data)
```

## Methods

- `get_invoices(params)` - List invoices
- `get_invoice(invoice_id)` - Get specific invoice
- `create_invoice(invoice_data)` - Create invoice
- `update_invoice(invoice_id, invoice_data)` - Update invoice
- `get_clients(params)` - List clients
- `create_client(client_data)` - Create client
- `get_products(params)` - List products
- `create_product(product_data)` - Create product
- `get_orders(params)` - List orders
- `create_order(order_data)` - Create order

## Error Handling

```python
try:
    invoice = client.create_invoice(data)
except TovasAuthenticationError:
    print("Invalid API credentials")
except TovasRateLimitError:
    print("Rate limit exceeded")
except TovasError as e:
    print(f"API error: {e}")
```