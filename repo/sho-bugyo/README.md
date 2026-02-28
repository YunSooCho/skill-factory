# Sho Bugyo API Client

Python API client for Sho Bugyo (商簿君) - Japanese accounting and sales management system.

[Official Site](https://www.sho-bugyo.com/) | [API Documentation](https://www.sho-bugyo.com/api/)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

```python
from sho_bugyo_client import ShoBugyoClient

# Initialize client with your credentials
client = ShoBugyoClient(
    api_key="your_api_key",
    company_id="your_company_id"
)
```

Get credentials from Sho Bugyo system settings.

## Usage

### Create Estimate

```python
# Create a new estimate
items = [
    {
        "item_code": "ITEM001",
        "item_name": "商品A",
        "quantity": 10,
        "unit_price": 1000,
        "tax_type": "01"  # 01: tax included
    },
    {
        "item_code": "ITEM002",
        "item_name": "商品B",
        "quantity": 5,
        "unit_price": 2000,
        "tax_type": "01"
    }
]

response = client.create_estimate(
    customer_code="CUST001",
    issue_date="2026-02-28",
    items=items,
    expiration_date="2026-03-31",
    remarks="初回取引"
)
print(response)
```

### Create Sales Order

```python
# Create a sales order
response = client.create_sales_order(
    customer_code="CUST001",
    issue_date="2026-02-28",
    items=items,
    order_number="SO20260228001",
    delivery_date="2026-03-05"
)
print(response)
```

### Get Sales Order

```python
# Retrieve sales order details
response = client.get_sales_order("SO20260228001")
print(response)
```

### Search Sales Orders

```python
# Search sales orders
response = client.search_sales_orders(
    customer_code="CUST001",
    start_date="2026-02-01",
    end_date="2026-02-28",
    status="02",  # 02: confirmed
    limit=50
)
print(response)
```

### Create Sales Invoice

```python
# Create a sales invoice
response = client.create_sales_invoice(
    customer_code="CUST001",
    issue_date="2026-02-28",
    items=items,
    invoice_number="INV20260228001",
    due_date="2026-03-31"
)
print(response)
```

### Get Sales Invoice

```python
# Retrieve sales invoice details
response = client.get_sales_invoice("INV20260228001")
print(response)
```

### Create or Update Customer

```python
# Create a new customer
response = client.create_or_update_customer(
    customer_code="CUST001",
    customer_name="株式会社テスト",
    postal_code="100-0001",
    address="東京都千代田区1-1-1",
    phone="03-1234-5678",
    email="test@example.com",
    payment_terms="01",
    tax_type="01"
)
print(response)

# Update existing customer
response = client.create_or_update_customer(
    customer_code="CUST001",  # Same code = update
    customer_name="株式会社テスト（変更後）"
)
print(response)
```

### Search Customers

```python
# Search customers by name
response = client.search_customers(
    customer_name="株式会社",
    limit=50
)
print(response)

# Search by customer code
response = client.search_customers(
    customer_code="CUST001"
)
print(response)
```

### Create or Update Product

```python
# Create a new product
response = client.create_or_update_product(
    item_code="ITEM001",
    item_name="商品A",
    sales_price=1000,
    purchase_price=800,
    tax_type="01",
    unit="10",
    unit_name="個"
)
print(response)
```

### Search Products

```python
# Search products by name
response = client.search_products(
    item_name="商品",
    limit=50
)
print(response)

# Search by item code
response = client.search_products(
    item_code="ITEM001"
)
print(response)
```

## API Actions Implemented

| Action | Method | Description |
|--------|--------|-------------|
| 見積書情報を登録 | `create_estimate()` | Register estimate |
| 受注伝票を登録 | `create_sales_order()` | Register sales order |
| 受注伝票情報を取得 | `get_sales_order()` | Get sales order info |
| 受注伝票を検索 | `search_sales_orders()` | Search sales orders |
| 売上伝票を登録 | `create_sales_invoice()` | Register sales invoice |
| 売上伝票情報を取得 | `get_sales_invoice()` | Get sales invoice info |
| 得意先を登録・更新 | `create_or_update_customer()` | Create/update customer |
| 得意先を検索 | `search_customers()` | Search customers |
| 商品を登録・更新 | `create_or_update_product()` | Create/update product |
| 商品を検索 | `search_products()` | Search products |

## Status Codes

### Order Status
| Code | Description |
|------|-------------|
| 01 | Draft (下書き) |
| 02 | Confirmed (確定) |
| 03 | Shipped (出荷済) |
| 04 | Canceled (取消) |

### Tax Type
| Code | Description |
|------|-------------|
| 01 | Tax included (税込) |
| 02 | Tax excluded (税抜) |

## Error Handling

```python
from sho_bugyo_client import ShoBugyoAPIError

try:
    response = client.create_sales_order(
        customer_code="CUST001",
        issue_date="2026-02-28",
        items=items
    )
except ShoBugyoAPIError as e:
    print(f"Sho Bugyo API Error: {e}")
```

## Testing

```bash
python test_sho_bugyo.py
```

**Note:** Tests require valid Sho Bugyo credentials.

## Yoom Integration

This client implements the following Yoom flow bot operations:
- **受注伝票を登録** - `create_sales_order()`
- **受注伝票情報を取得** - `get_sales_order()`
- **売上伝票情報を取得** - `get_sales_invoice()`
- **受注伝票を検索** - `search_sales_orders()`
- **見積書情報を登録** - `create_estimate()`
- **商品を登録・更新** - `create_or_update_product()`
- **商品を検索** - `search_products()`
- **得意先を登録・更新** - `create_or_update_customer()`
- **売上伝票を登録** - `create_sales_invoice()`
- **得意先を検索** - `search_customers()`

## Triggers

The following Yoom triggers are available:
- **得意先が作成されたら** (When customer created)
- **商品が登録されたら** (When product registered)
- **得意先が更新されたら** (When customer updated)
- **商品が更新されたら** (When product updated)

Triggers require webhook endpoint setup in your integration.