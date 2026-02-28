# Raynet CRM API Client

Python API client for Raynet CRM API.

[Official Site](https://raynet.info/) | [API Documentation](https://raynet.info/api/)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

```python
from raynet_crm_client import RaynetCrmClient

# Initialize client with your API key
client = RaynetCrmClient(
    api_key="your_instance_name_or_api_key"
)
```

Get API key from Raynet CRM settings.

## Usage

### Create Account

```python
# Create a new account/company
response = client.create_account(
    name="Example Company",
    identification_number="12345678",
    vat_number="CZ12345678",
    phone="+1234567890",
    email="contact@example.com",
    website="https://example.com"
)
print(response)
```

### Get Account

```python
# Get account details
response = client.get_account(account_id=123)
print(response)
```

### Search Accounts

```python
# Search accounts
response = client.search_accounts(query="Example", limit=50)
print(response)

# List all accounts
response = client.search_accounts(limit=100)
print(response)
```

### Update Account

```python
# Update an existing account
response = client.update_account(
    account_id=123,
    phone="+0987654321",
    email="new@example.com"
)
print(response)
```

### Delete Account

```python
# Delete an account
response = client.delete_account(account_id=123)
print(response)
```

### Create Contact

```python
# Create a new contact
response = client.create_contact(
    first_name="John",
    last_name="Doe",
    company_id=123,
    position="CEO",
    phone="+1234567890",
    mobile="+0987654321",
    email="john.doe@example.com"
)
print(response)
```

### Get Contact

```python
# Get contact details
response = client.get_contact(contact_id=456)
print(response)
```

### Search Contacts

```python
# Search contacts by name/email
response = client.search_contacts(query="John", limit=50)
print(response)

# Search contacts by company
response = client.search_contacts(company_id=123, limit=50)
print(response)
```

### Update Contact

```python
# Update an existing contact
response = client.update_contact(
    contact_id=456,
    position="CTO",
    phone="+1111111111"
)
print(response)
```

### Delete Contact

```python
# Delete a contact
response = client.delete_contact(contact_id=456)
print(response)
```

### Create Product

```python
# Create a new product
response = client.create_product(
    name="Product Name",
    code="PROD001",
    price=99.99,
    description="Product description"
)
print(response)
```

### Get Product

```python
# Get product details
response = client.get_product(product_id=789)
print(response)
```

### Search Products

```python
# Search products
response = client.search_products(query="Product", limit=50)
print(response)
```

### Update Product

```python
# Update an existing product
response = client.update_product(
    product_id=789,
    price=89.99,
    description="Updated description"
)
print(response)
```

### Delete Product

```python
# Delete a product
response = client.delete_product(product_id=789)
print(response)
```

### Create Lead

```python
# Create a new lead
response = client.create_lead(
    first_name="Jane",
    last_name="Smith",
    company_name="Acme Inc.",
    email="jane.smith@example.com",
    phone="+1234567890",
    status="new"
)
print(response)
```

### Get Lead

```python
# Get lead details
response = client.get_lead(lead_id=101)
print(response)
```

### Search Leads

```python
# Search leads
response = client.search_leads(query="Jane", limit=50)
print(response)

# Filter by status
response = client.search_leads(status="new", limit=50)
print(response)
```

### Update Lead

```python
# Update an existing lead
response = client.update_lead(
    lead_id=101,
    status="contacted"
)
print(response)
```

### Delete Lead

```python
# Delete a lead
response = client.delete_lead(lead_id=101)
print(response)
```

## API Actions Implemented

| Action | Method | Description |
|--------|--------|-------------|
| Create Account | `create_account()` | Create account |
| Get Account | `get_account()` | Get account details |
| Search Account | `search_accounts()` | Search accounts |
| Update Account | `update_account()` | Update account |
| Delete Account | `delete_account()` | Delete account |
| Create Contact | `create_contact()` | Create contact |
| Get Contact | `get_contact()` | Get contact details |
| Search Contact | `search_contacts()` | Search contacts |
| Update Contact | `update_contact()` | Update contact |
| Delete Contact | `delete_contact()` | Delete contact |
| Create Product | `create_product()` | Create product |
| Get Product | `get_product()` | Get product details |
| Search Product | `search_products()` | Search products |
| Update Product | `update_product()` | Update product |
| Delete Product | `delete_product()` | Delete product |
| Create Lead | `create_lead()` | Create lead |
| Get Lead | `get_lead()` | Get lead details |
| Search Lead | `search_leads()` | Search leads |
| Update Lead | `update_lead()` | Update lead |
| Delete Lead | `delete_lead()` | Delete lead |

## Response Format

```python
{
    "status": "success",
    "data": {
        "id": 123,
        "primaryName": "Example Company",
        // ... other fields
    },
    "status_code": 200
}
```

## Error Handling

```python
from raynet_crm_client import RaynetCrmAPIError

try:
    response = client.create_account(name="Test Company")
except RaynetCrmAPIError as e:
    print(f"Raynet CRM API Error: {e}")
```

## Testing

```bash
python test_raynet_crm.py
```

**Note:** Tests require valid Raynet CRM credentials.

## Yoom Integration

This client implements the following Yoom flow bot operations:
- **Create Account** - `create_account()`
- **Delete Account** - `delete_account()`
- **Create Contact** - `create_contact()`
- **Create Product** - `create_product()`
- **Search Product** - `search_products()`
- **Get Account** - `get_account()`
- **Get Contact** - `get_contact()`
- **Get Product** - `get_product()`
- **Delete Contact** - `delete_contact()`
- **Delete Product** - `delete_product()`
- **Update Lead** - `update_lead()`
- **Search Contact** - `search_contacts()`
- **Update Account** - `update_account()`
- **Search Lead** - `search_leads()`
- **Create Lead** - `create_lead()`
- **Delete Lead** - `delete_lead()`
- **Update Contact** - `update_contact()`
- **Search Account** - `search_accounts()`
- **Get Lead** - `get_lead()`
- **Update Product** - `update_product()`

## Triggers

The following Yoom triggers are available:
- **Meeting Created**, **Task Updated**, **Lead Updated**, **Lead Deleted**, **PhoneCall Deleted**, **Account Deleted**, **Account Updated**, **Account Created**, **Task Created**, **Contact Deleted**, **Meeting Updated**, **Product Updated**, **Lead Created**, **Product Created**, **Meeting Deleted**, **Product Deleted**, **PhoneCall Created**, **PhoneCall Updated**, **Contact Updated**, **Contact Created**, **Task Deleted**

Triggers require webhook endpoint setup.