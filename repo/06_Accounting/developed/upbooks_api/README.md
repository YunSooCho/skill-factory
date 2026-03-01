# UpBooks API Client

Cloud accounting platform for invoicing, expenses, billing, and financial reporting.

## API Key Setup

1. Log in to [UpBooks](https://upbooks.com)
2. Go to Settings → Developer Settings → API Keys
3. Generate your API key
4. Note your Company ID

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

```python
from upbooks_api import UpBooksClient

# Initialize client
client = UpBooksClient(api_key='your_api_key', company_id='company_123')

# Get invoices
invoices = client.get_invoices()
print(f"Found {len(invoices.get('data', []))} invoices")

# Create an invoice
invoice_data = {
    'customer_id': 'cust_456',
    'invoice_date': '2024-02-15',
    'due_date': '2024-03-15',
    'line_items': [{
        'description': 'Service',
        'amount': 500.00
    }]
}
invoice = client.create_invoice(invoice_data)

# Get financial reports
report = client.get_reports('profit_loss', {'year': 2024})
```

## Methods

### Invoices
- `get_invoices(params)` - List invoices
- `get_invoice(invoice_id)` - Get specific invoice
- `create_invoice(invoice_data)` - Create invoice
- `update_invoice(invoice_id, invoice_data)` - Update invoice
- `delete_invoice(invoice_id)` - Delete invoice

### Vendors
- `get_vendors(params)` - List vendors
- `create_vendor(vendor_data)` - Create vendor

### Expenses
- `get_expenses(params)` - List expenses
- `create_expense(expense_data)` - Create expense

### Reports
- `get_reports(report_type, params)` - Get financial reports
- `get_ledger_entries(params)` - Get ledger entries

## Error Handling

```python
try:
    invoice = client.create_invoice(data)
except UpBooksAuthenticationError:
    print("Invalid API credentials")
except UpBooksRateLimitError:
    print("Rate limit exceeded")
except UpBooksError as e:
    print(f"API error: {e}")
```