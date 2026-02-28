# Smaregi API Client

A Python client for the Smaregi POS API - comprehensive Japanese retail management system for stores, products, inventory, sales, and customers.

## Features

- **Products**: Complete product catalog management
- **Stock/Inventory**: Real-time stock tracking and adjustments
- **Sales**: Transaction and sales data management
- **Customers**: Customer database management
- **Stores**: Multi-store support
- **Categories**: Product categorization
- **Staff**: Staff management
- **Analytics**: Daily sales reports

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

### Getting API Credentials

1. Log into your [Smaregi Dashboard](https://pos.smaregi.jp/)
2. Go to **Settings → External Link → API** (外部連携 → API)
3. Enable API access
4. Note your **Contract ID** (契約ID)
5. Generate an **Access Token** (アクセストークン)

### Environment Variables

```bash
export SMAREGI_API_KEY="your_access_token"
export SMAREGI_CONTRACT_ID="your_contract_id"
export SMAREGI_BASE_URL="https://api.smaregi.jp/pos"  # Optional
```

## Usage Example

```python
from smaregi_api import SmaregiApiClient

# Initialize client
client = SmaregiApiClient(
    api_key="your_access_token",
    contract_id="12345"
)

# List stores
stores = client.list_stores()
store_id = stores[0]['storeId']

# List products
products = client.list_products(store_id=store_id, page=1)
print(f"Found products: {len(products.get('data', []))}")

# Get specific product
product = client.get_product(store_id=store_id, product_id="prod123")

# Create product
new_product = client.create_product(store_id=store_id, {
    "productId": "NEW001",
    "productName": "新しい商品",
    "categoryId": "CAT001",
    "retailPrice": 1000,  # in yen
    "costPrice": 600,
    "taxRate": 10,
    "barcode": "1234567890123"
})

# Update product
updated = client.update_product(
    store_id=store_id,
    product_id="prod123",
    {"retailPrice": 1200}
)

# Stock levels
stock_info = client.list_stock(store_id=store_id, product_id="prod123")

# Adjust stock
adjustment = client.adjust_stock([{
    "storeId": store_id,
    "productId": "prod123",
    "storageId": "STORAGE001",
    "stock": 50
}])

# List sales
sales = client.list_sales(
    store_id=store_id,
    date_from="2024-01-01",
    date_to="2024-01-31"
)

# Get specific sale
sale = client.get_sale(sale_id="SALE123")

# Create sale transaction
new_sale = client.create_sale({
    "storeId": store_id,
    "terminalId": "TERM001",
    "saleDate": "2024-01-15T10:30:00+09:00",
    "sales": [
        {
            "productId": "prod123",
            "quantity": 2,
            "retailPrice": 1000,
            "taxRate": 10
        }
    ],
    "paymentMethodId": "PAY001",
    "customerId": "CUST001"
})

# Customers
customers = client.list_customers(store_id=store_id)
customer = client.get_customer(customer_id="CUST001")

# Create customer
new_customer = client.create_customer({
    "storeId": store_id,
    "customerCode": "CUST002",
    "customerName": "山田 太郎",
    "customerNameKana": "やまだ たろう",
    "phoneNumber": "0312345678",
    "mailAddress": "customer@example.com",
    "postCode": "1000001",
    "address1": "東京都千代田区1-1",
    "address2": "",
    "birthday": "1990-01-01"
})

# Categories
categories = client.list_categories(store_id=store_id)

# Staff
staff = client.list_staff(store_id=store_id)

# Terminals
terminals = client.list_terminals(store_id=store_id)

# Payment methods
payments = client.list_payment_methods(store_id=store_id)

# Storage locations
storages = client.list_storages(store_id=store_id)

# Daily report
daily_report = client.get_daily_report(
    store_id=store_id,
    date="2024-01-15"
)

# Use context manager
with SmaregiApiClient(
    api_key="your_token",
    contract_id="12345"
) as client:
    stores = client.list_stores()
    products = client.list_products(stores[0]['storeId'])
```

## API Documentation

For complete API reference, see: https://dev.smaregi.com/ (Japanese only)

### Key Endpoints

| Resource | Methods |
|----------|---------|
| Stores | list_stores, get_store |
| Products | list_products, get_product, create_product, update_product |
| Stock | list_stock, adjust_stock |
| Sales | list_sales, get_sale, create_sale |
| Categories | list_categories, get_category |
| Customers | list_customers, get_customer, create_customer, update_customer |
| Staff | list_staff, get_staff |
| Terminals | list_terminals, get_terminal |
| Payments | list_payment_methods |
| Storage | list_storages |
| Reports | get_daily_report |

## Notes

- All currency amounts are in Japanese Yen (JPY)
- Tax rates are in percentage (e.g., 10 for 10%)
- Store ID and Contract ID are required for most operations
- Dates should be in ISO 8601 format with timezone (+09:00 for JST)
- Maximum items per page is 100

## Requirements

- Python 3.7+
- requests>=2.31.0

## License

MIT License