# Holded API Client

Python API client for Holded - CRM and ERP platform.

[Official Site](https://holded.com/) | [API Documentation](https://developers.holded.com/reference/overview)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

```python
from holded_client import HoldedClient

# Initialize client with your API key
client = HoldedClient(
    api_key="your_api_key"
)
```

Get API key from [Holded Settings](https://app.holded.com/settings/api).

## Usage

### Create Contact

```python
# Create a new contact
response = client.create_contact(
    name="John Doe",
    email="john@example.com",
    phone="+1234567890",
    mobile="+0987654321",
    address="123 Main St",
    city="New York",
    province="NY",
    postalcode="10001",
    country="US",
    type="person"
)
print(response)
```

### Update Contact

```python
# Update an existing contact
response = client.update_contact(
    contact_id="60b8d7c9e8b4d4001f7c8a7b",
    email="newemail@example.com",
    phone="+1111111111"
)
print(response)
```

### Delete Contact

```python
# Delete a contact
response = client.delete_contact("60b8d7c9e8b4d4001f7c8a7b")
print(response)
```

### Get Contact

```python
# Get contact details
response = client.get_contact("60b8d7c9e8b4d4001f7c8a7b")
print(response)
```

### Search Contacts

```python
# Search contacts
response = client.search_contacts(
    search="John",
    limit=50
)
print(response)

# List all contacts
response = client.search_contacts(limit=100)
print(response)
```

### Create Product

```python
# Create a new product
response = client.create_product(
    name="Product Name",
    description="Product description",
    sale_price=99.99,
    cost=50.00,
    tax_id="tax_123",  # Get from tax configuration
    stock=100,
    sku="SKU001"
)
print(response)
```

### Update Product

```python
# Update an existing product
response = client.update_product(
    product_id="60b8d7c9e8b4d4001f7c8a7c",
    sale_price=89.99,
    stock=50
)
print(response)
```

### Get Product

```python
# Get product details
response = client.get_product("60b8d7c9e8b4d4001f7c8a7c")
print(response)
```

### Create Payment

```python
# Create a payment
response = client.create_payment(
    invoice_id="inv_1234567890",
    amount=99.99,
    date="2026-02-28",
    notes="Payment for invoice #123",
    method="card"
)
print(response)
```

### Get Payment

```python
# Get payment details
response = client.get_payment("pay_1234567890")
print(response)
```

### Search Payments

```python
# Search payments
response = client.search_payments(
    search="invoice_123",
    limit=50
)
print(response)

# List all payments
response = client.search_payments(limit=100)
print(response)
```

## API Actions Implemented

| Action | Method | Description |
|--------|--------|-------------|
| Create Contact | `create_contact()` | Create new contact |
| Update Contact | `update_contact()` | Update existing contact |
| Delete Contact | `delete_contact()` | Delete contact |
| Get Contact | `get_contact()` | Get contact details |
| Search Contact | `search_contacts()` | Search/list contacts |
| Create Product | `create_product()` | Create new product |
| Update Product | `update_product()` | Update existing product |
| Get Product | `get_product()` | Get product details |
| Create Payment | `create_payment()` | Create new payment |
| Get Payment | `get_payment()` | Get payment details |
| Search Payment | `search_payments()` | Search/list payments |

## Response Format

```python
{
    "status": "success",
    "data": {
        "id": "60b8d7c9e8b4d4001f7c8a7b",
        "name": "John Doe",
        "email": "john@example.com",
        // ... other fields
    },
    "status_code": 200
}
```

## Error Handling

```python
from holded_client import HoldedAPIError

try:
    response = client.create_contact(
        name="Test Contact",
        email="test@example.com"
    )
except HoldedAPIError as e:
    print(f"Holded API Error: {e}")
```

## Rate Limiting

Holded API has rate limits:
- Standard tier: 100 requests/minute
- Advanced tier: 1000 requests/minute

The client does not implement rate limiting - your application should handle rate limit errors (HTTP 429) with appropriate backoff.

## Testing

```bash
python test_holded.py
```

**Note:** Tests require valid Holded credentials.

## Yoom Integration

This client implements the following Yoom flow bot operations:
- **Create Contact** - `create_contact()`
- **Create Product** - `create_product()`
- **Create Payment** - `create_payment()`
- **Get Contact** - `get_contact()`
- **Get Payment** - `get_payment()`
- **Get Product** - `get_product()`
- **Search Contact** - `search_contacts()`
- **Update Contact** - `update_contact()`
- **Update Product** - `update_product()`
- **Search Payment** - `search_payments()`

## Notes

### Contact Types
- **person**: Individual contact
- **company**: Company contact

### Payment Methods
Common payment methods:
- `cash`: Cash
- `card`: Credit/Debit card
- `transfer`: Bank transfer
- `check`: Check
- `paypal`: PayPal
- `stripe`: Stripe

## Support

For API issues, visit:
- [Holded API Documentation](https://developers.holded.com/reference/overview)
- [Holded Support](https://help.holded.com/)