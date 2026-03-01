# Deel

Deel is a global HR and contractor management platform that helps companies hire, pay, and manage international contractors and employees compliantly.

## API Documentation

- **Base URL:** `https://api.letsdeel.com/v2`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import DeelClient

client = DeelClient(api_key="YOUR_API_KEY")

# Get contracts
contracts = client.get_contracts()
print(f"Contracts: {contracts}")

# Create contract
contract_data = {
    "contractor_id": "12345",
    "title": "Software Development",
    "scope": "..."
}
result = client.create_contract(contract_data)

# Get invoices
invoices = client.get_invoices()

# Get contractors
contractors = client.get_contractors()

# Create client
client_data = {"name": "Acme Corp", "email": "billing@acme.com"}
result = client.create_client(client_data)

# Create off-cycle payment
payment_data = {"contract_id": "123", "amount": 1000}
result = client.create_offcycle_payment(payment_data)
```

## Error Handling

```python
from client import DeelClient, DeelError

try:
    client = DeelClient(api_key="...")
    contracts = client.get_contracts()
except DeelError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.