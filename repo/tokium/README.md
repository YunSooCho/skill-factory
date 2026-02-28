# Tokium API Client

Financial management platform for invoicing, expenses, and accounting operations.

## API Key Setup

1. Log in to [Tokium](https://tokium.com)
2. Navigate to Settings → API → Generate API Key
3. Note your Account ID if required

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

```python
from tokium import TokiumClient

# Initialize client
client = TokiumClient(api_key='your_api_key', account_id='your_account_id')

# Get all invoices
invoices = client.get_invoices()
print(f"Found {len(invoices.get('data', []))} invoices")

# Create a new invoice
invoice_data = {
    'customer_id': 'cust_123',
    'invoice_date': '2024-02-15',
    'due_date': '2024-03-15',
    'items': [{
        'description': 'Service A',
        'quantity': 1,
        'unit_price': 100.00,
        'tax_rate': 20
    }],
    'currency': 'USD'
}
invoice = client.create_invoice(invoice_data)
print(f"Created invoice: {invoice['id']}")

# Send invoice via email
client.send_invoice_email(invoice['id'])
```

## Methods

### Invoices
- `get_invoices(params)` - List invoices
- `get_invoice(invoice_id)` - Get specific invoice
- `create_invoice(invoice_data)` - Create invoice
- `update_invoice(invoice_id, invoice_data)` - Update invoice
- `delete_invoice(invoice_id)` - Delete invoice
- `send_invoice_email(invoice_id)` - Send invoice via email

### Customers
- `get_customers(params)` - List customers
- `create_customer(customer_data)` - Create customer

### Expenses
- `get_expenses(params)` - List expenses
- `create_expense(expense_data)` - Create expense

### Accounts
- `get_accounts(params)` - List accounts

## Error Handling

```python
try:
    invoice = client.create_invoice(data)
except TokiumAuthenticationError:
    print("Invalid API credentials")
except TokiumRateLimitError:
    print("Rate limit exceeded, retry later")
except TokiumError as e:
    print(f"API error: {e}")
```