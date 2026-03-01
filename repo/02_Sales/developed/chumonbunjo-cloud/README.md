# Chumonbunjo Cloud API Client

Complete API client for Chumonbunjo Cloud - a Japanese real estate sales and contract management system.

## Features

- Full API coverage for 28 endpoints
- Order/Contract management (注文住宅/分譲住宅)
- Customer data management (顧客データ)
- Quote management (見積書)
- Purchase order management (発注データ)
- Vendor management (仕入先業者)
- Partner account management (協力業者)
- CSV export functionality
- Complete error handling
- Rate limiting support

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from chumonbunjo_client import ChumonbunjoClient

async def main():
    client = ChumonbunjoClient(api_key="your_api_key")

    # Create customer
    customer = await client.create_customer({
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "090-1234-5678",
        "address": "Tokyo"
    })

    # Search contracts
    contracts = await client.search_ordered_contracts(customer_id="123")

    await client.close()

asyncio.run(main())
```

## API Endpoints

### Contracts (注文住宅/分譲住宅)
- `create_ordered_contract()`, `update_ordered_contract()`, `get_ordered_contract()`, `search_ordered_contracts()`
- `create_developed_contract()`, `update_developed_contract()`, `get_developed_contract()`, `search_developed_contracts()`

### Customers (顧客データ)
- `create_customer()`, `update_customer()`, `get_customer()`, `search_customers()`

### Quotes (見積書)
- `get_quote()`, `search_quotes()`, `create_quote_csv()`, `get_quote_csv_file()`

### Purchase Orders (発注データ)
- `get_purchase_order()`, `search_purchase_orders()`, `create_purchase_order_csv()`, `get_purchase_order_csv_file()`

### Vendors (仕入先業者)
- `create_vendor()`, `update_vendor()`, `get_vendor()`, `search_vendors()`

### Partners (協力業者)
- `create_partner()`, `update_partner()`, `get_partner()`, `search_partners()`

## Error Handling

All methods raise `ChumonbunjoAPIError` on API errors:
```python
try:
    customer = await client.create_customer(data)
except ChumonbunjoAPIError as e:
    print(f"API Error: {e}")
```

## Rate Limiting

The client includes automatic rate limiting. You can configure it:
```python
client = ChumonbunjoClient(
    api_key="your_api_key",
    max_requests_per_minute=60
)
```

## Webhook Triggers

Supports 12 webhook triggers:
- Product information updates
-土地台帳 (Land ledger) events
- Contract creation/updates
- Customer creation/updates

See the full API documentation for webhook configuration.