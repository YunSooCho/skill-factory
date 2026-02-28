# Zoho Books

Zoho Books is a cloud-based accounting and bookkeeping platform that helps businesses manage their finances, invoices, expenses, and reports.

## API Documentation

- **Official API Doc:** https://www.zoho.com/books/api/v3/
- **Base URL:** `https://www.zohoapis.com/books/v3` (varies by data center)
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
    'https://www.zohoapis.com/books/v3/organizations',
    headers={'Authorization': auth_token}
)
orgs = resp.json()
org_id = orgs['organizations'][0]['organization_id']
```

**Method 2 - Web:**
1. Login to Zoho Books admin console
2. Click organization dropdown
3. Click "Manage Organizations"
4. Find your organization ID in the data

### Data Center Domains

Check your Zoho Books URL to determine the domain:
- Books URL: `books.zoho.com` → domain: `us` (https://www.zohoapis.com/books/v3)
- Books URL: `books.zoho.eu` → domain: `eu` (https://www.zohoapis.eu/books/v3)
- Books URL: `books.zoho.in` → domain: `in` (https://www.zohoapis.in/books/v3)
- Books URL: `books.zoho.jp` → domain: `jp` (https://www.zohoapis.jp/books/v3)

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import ZohoBooksClient

# Initialize client
client = ZohoBooksClient(
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

# Create an expense
expense_data = {
    "account_id": "2000000034567",
    "date": "2024-02-28",
    "amount": 500.00,
    "description": "Office supplies"
}
expense = client.create_expense(expense_data)
print(f"Created expense: {expense}")

# Get profit and loss report
pnl = client.get_profit_and_loss()
print(f"Profit & Loss: {pnl}")

# Get balance sheet
balance_sheet = client.get_balance_sheet()
print(f"Balance Sheet: {balance_sheet}")
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
| `GET /contacts` | List contacts/customers |
| `POST /contacts` | Create contact |
| `GET /items` | List items |
| `POST /items` | Create item |
| `GET /estimates` | List estimates |
| `POST /estimates` | Create estimate |
| `GET /customerpayments` | List payments received |
| `POST /customerpayments` | Record payment |
| `GET /expenses` | List expenses |
| `POST /expenses` | Create expense |
| `GET /reports/profitandloss` | Profit & Loss statement |
| `GET /reports/balancesheet` | Balance sheet |
| `GET /bankaccounts` | List bank accounts |

## Error Handling

```python
from client import ZohoBooksClient, ZohoBooksError, ZohoBooksRateLimitError, ZohoBooksAuthenticationError

try:
    client = ZohoBooksClient(auth_token="...", organization_id="...")
    invoices = client.get_invoices()
except ZohoBooksRateLimitError:
    print("Rate limit exceeded - try again later")
except ZohoBooksAuthenticationError:
    print("Invalid auth token")
except ZohoBooksError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.