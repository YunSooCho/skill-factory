# SmartBill API Client

Romanian invoicing and accounting platform client for managing invoices, clients, products, and tax compliance.

## API Key Setup

1. Log in to [SmartBill](https://www.smartbill.ro)
2. Navigate to `Settings` → `API Settings`
3. Generate your API key
4. Find your company VAT code (CIF) for API access

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

```python
from smartbill import SmartBillClient

# Initialize client
client = SmartBillClient(
    api_key='your_api_key',
    company_vat_code='RO12345678'  # Your company's VAT code
)

# Get list of invoices
invoices = client.get_invoices(params={
    'dateStart': '2024-01-01',
    'dateEnd': '2024-12-31'
})

# Create a new invoice
invoice_data = {
    'client': {
        'cui': 'RO12345678',
        'nume': 'Client SRL',
        'adresa': 'Str. Exemplu 1, Bucuresti'
    },
    'serie': 'SMRT',
    'data': '2024-01-15',
    'scadenta': '2024-02-15',
    'observatii': 'Invoice for services',
    'produse': [{
        'denumire': 'Consulting Services',
        'cantitate': 1.0,
        'pretFaraTva': 100.0,
        'tva': 19.0,
        'moneda': 'RON'
    }]
}

invoice = client.create_invoice(invoice_data)
print(f"Created invoice: {invoice['numar']}")

# Send invoice via email
client.send_invoice_email(
    invoice_number='123',
    series='SMRT',
    email='client@example.com',
    message='Please find attached invoice'
)
```

## Methods

- `get_invoices()` - List invoices
- `get_invoice(invoice_number, series)` - Get specific invoice
- `create_invoice(invoice_data)` - Create new invoice
- `update_invoice(invoice_number, series, invoice_data)` - Update invoice
- `delete_invoice(invoice_number, series)` - Delete invoice
- `get_clients()` - List clients
- `create_client(client_data)` - Create client
- `update_client(client_id, client_data)` - Update client
- `get_products()` - List products
- `create_product(product_data)` - Create product
- `send_invoice_email(invoice_number, series, email, message)` - Send invoice via email
- `get_invoice_pdf(invoice_number, series)` - Get PDF of invoice
- `get_series()` - List invoice series

## Error Handling

```python
try:
    invoice = client.create_invoice(data)
except SmartBillAuthenticationError:
    print("Invalid API credentials")
except SmartBillRateLimitError:
    print("Too many requests, retry later")
except SmartBillError as e:
    print(f"API error: {e}")
```