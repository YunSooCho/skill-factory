# Zoho Invoice

Zoho Invoice is a cloud-based invoicing and billing platform that helps businesses create and send professional invoices, track payments, and manage billing online.

## API Documentation

- **Official API Doc:** https://www.zoho.com/invoice/api/v3/
- **Base URL:** `https://www.zohoapis.com/invoice/v3` (varies by data center)
- **Rate Limit:** 100 requests per minute per organization

## API Keys & Authentication

### Getting OAuth Token

1. Go to [Zoho Developer Console](https://developer.zoho.com/)
2. Create a new app or use existing app
3. Generate OAuth 2.0 token
4. Copy the token - format: `Zoho-oauthtoken <your_token>`

### Getting Organization ID

**Method 1 - API:**
```python
import requests
auth_token = "Zoho-oauthtoken YOUR_TOKEN"
resp = requests.get(
    'https://www.zohoapis.com/invoice/v3/organizations',
    headers={'Authorization': auth_token}
)
orgs = resp.json()
org_id = orgs['organizations'][0]['organization_id']
```

**Method 2 - Web:**
1. Login to Zoho Invoice admin console
2. Click organization dropdown
3. Click "Manage Organizations"
4. Find your organization ID in the data

### Data Center Domains

Check your Zoho Invoice URL to determine the domain:
- Invoice URL: `invoice.zoho.com` → domain: `us` (https://www.zohoapis.com/invoice/v3)
- Invoice URL: `invoice.zoho.eu` → domain: `eu` (https://www.zohoapis.eu/invoice/v3)
- Invoice URL: `invoice.zoho.in` → domain: `in` (https://www.zohoapis.in/invoice/v3)
- Invoice URL: `invoice.zoho.jp` → domain: `jp` (https://www.zohoapis.jp/invoice/v3)

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import ZohoInvoiceClient

# Initialize client
client = ZohoInvoiceClient(
    auth_token="Zoho-oauthtoken YOUR_TOKEN",
    organization_id="10234695",
    domain="us",  # Change based on your data center
    timeout=30
)

# Get organizations
orgs = client.get_organizations()
print(f"Organizations: {orgs}")

# Get invoices
invoices = client.get_invoices()
print(f"Invoices: {invoices}")

# Get specific invoice
invoice = client.get_invoice("2000000056789")
print(f"Invoice: {invoice}")

# Create a new invoice
invoice_data = {
    "customer_id": "2000000012345",
    "invoice_number": "INV-001",
    "date": "2024-02-28",
    "line_items": [
        {
            "item_id": "2000000023456",
            "quantity": 1,
            "rate": 100.00
        }
    ]
}
new_invoice = client.create_invoice(invoice_data)
print(f"Created invoice: {new_invoice}")

# Send invoice via email
client.send_invoice(new_invoice['invoice']['invoice_id'], {
    "to_mail_ids": ["customer@example.com"],
    "subject": "Invoice INV-001",
    "body": "Please find attached the invoice."
})

# Get contacts/customers
contacts = client.get_contacts()
print(f"Contacts: {contacts}")

# Create a new contact
contact_data = {
    "contact_name": "Acme Corporation",
    "contact_type": "customer",
    "email": "billing@acme.com"
}
new_contact = client.create_contact(contact_data)
print(f"Created contact: {new_contact}")

# Get items
items = client.get_items()
print(f"Items: {items}")

# Create an estimate
estimate_data = {
    "customer_id": "2000000012345",
    "estimate_number": "EST-001",
    "date": "2024-02-28",
    "line_items": [
        {
            "item_id": "2000000023456",
            "quantity": 1,
            "rate": 100.00
        }
    ]
}
estimate = client.create_estimate(estimate_data)
print(f"Created estimate: {estimate}")

# Convert estimate to invoice
invoice = client.convert_estimate_to_invoice(estimate['estimate']['estimate_id'])
print(f"Converted to invoice: {invoice}")

# Record a payment
payment_data = {
    "customer_id": "2000000012345",
    "payment_mode": "creditcard",
    "amount": 100.00,
    "date": "2024-02-28",
    "description": "Payment for INV-001"
}
payment = client.record_payment(payment_data)
print(f"Recorded payment: {payment}")

# Create an expense
expense_data = {
    "account_id": "2000000034567",
    "date": "2024-02-28",
    "amount": 500.00,
    "description": "Office supplies"
}
expense = client.create_expense(expense_data)
print(f"Created expense: {expense}")

# Get invoice report
report = client.get_invoice_report()
print(f"Invoice report: {report}")
```

## Common Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /organizations` | Get list of organizations |
| `GET /invoices` | List invoices |
| `GET /invoices/{id}` | Get invoice details |
| `POST /invoices` | Create invoice |
| `PUT /invoices/{id}` | Update invoice |
| `DELETE /invoices/{id}` | Delete invoice |
| `POST /invoices/{id}/email` | Send invoice via email |
| `POST /invoices/{id}/status/sent` | Mark invoice as sent |
| `GET /contacts` | List contacts/customers |
| `POST /contacts` | Create contact |
| `GET /items` | List items |
| `POST /items` | Create item |
| `GET /estimates` | List estimates |
| `POST /estimates` | Create estimate |
| `POST /estimates/{id}/converttoinvoice` | Convert estimate to invoice |
| `GET /recurringinvoices` | List recurring invoices |
| `POST /recurringinvoices` | Create recurring invoice |
| `GET /customerpayments` | List payments received |
| `POST /customerpayments` | Record payment |
| `GET /expenses` | List expenses |
| `POST /expenses` | Create expense |
| `GET /recurringexpenses` | List recurring expenses |
| `POST /recurringexpenses` | Create recurring expense |
| `GET /reports/invoicesales` | Invoice sales report |
| `GET /reports/salesbyperson` | Sales by person report |

## Error Handling

```python
from client import ZohoInvoiceClient, ZohoInvoiceError, ZohoInvoiceRateLimitError, ZohoInvoiceAuthenticationError

try:
    client = ZohoInvoiceClient(auth_token="...", organization_id="...")
    invoices = client.get_invoices()
except ZohoInvoiceRateLimitError:
    print("Rate limit exceeded - try again later")
except ZohoInvoiceAuthenticationError:
    print("Invalid auth token")
except ZohoInvoiceError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.