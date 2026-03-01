# Cybozu

Cybozu (Kintone) is a Japanese business application platform that provides customizable database applications, workflow automation, and collaboration tools.

## API Documentation

- **Base URL:** `https://{subdomain}.cybozu.com/k/v1`
- **Authentication:** API Token (X-Cybozu-API-Token header)
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import CybozuClient

client = CybozuClient(
    subdomain="your-company",
    api_token="YOUR_API_TOKEN",
    app_id="123"
)

# Get records
records = client.get_records()
print(f"Records: {records}")

# Get specific record
record = client.get_record(record_id="1")

# Add record
record_data = {"field1": "value1", "field2": "value2"}
result = client.add_record(record_data)

# Update record
client.update_record(record_id="1", record_data={"field1": "new_value"})

# Delete records
client.delete_records(record_ids=["1", "2"])

# Get form fields
fields = client.get_form_fields()

# Get users
users = client.get_users()
```

## Error Handling

```python
from client import CybozuClient, CybozuError

try:
    client = CybozuClient(subdomain="...", api_token="...")
    records = client.get_records()
except CybozuError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.