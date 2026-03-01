# Callconnect API Client

Python client for Callconnect phone management API.

## Features

- Customers: Create, read, update, delete customers
- Call History: Search call records
- Webhooks: Handle webhook events

## Installation

```bash
pip install aiohttp
```

## API Actions (5)

1. 顧客を検索 (Search Customers)
2. 通話履歴を検索 (Search Call History)
3. 顧客の取得 (Get Customer)
4. 顧客を作成 (Create Customer)
5. 顧客を削除 (Delete Customer)

## Triggers (1)

- Webhookを受信したら (When webhook is received)

## Usage

```python
import asyncio
from callconnect import CallconnectClient

async def main():
    client = CallconnectClient(api_key="your_key")

    # Create customer
    customer = await client.create_customer({
        "name": "Acme Corp",
        "phone": "+81312345678",
        "email": "info@acme.com"
    })
    print(f"Customer: {customer.id}")

    # Search customers
    customers = await client.search_customers(name="Acme")
    print(f"Found {len(customers)} customers")

    # Search call history
    calls = await client.search_call_history(customer_id=customer.id)
    print(f"Found {len(calls)} calls")

asyncio.run(main())
```

## Authentication

Get API key from Callconnect dashboard.

## License

MIT