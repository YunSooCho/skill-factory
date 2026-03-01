# confluence

Confluence Integration

> Confluence provides team collaboration and documentation.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Get your API credentials from confluence:

1. Sign up at the official confluence website
2. Navigate to API settings
3. Generate your API key or access token
4. Configure environment variables or pass credentials directly

## Usage

### Basic Setup

```python
from confluence import ConfluenceClient

# Initialize with API key
client = ConfluenceClient(
    api_key="your-api-key"
)

# Or with access token
client = ConfluenceClient(
    access_token="your-access-token"
)
```

### Example: List Resources

```python
resources = client.list_resources()
for resource in resources:
    print(resource['id'], resource['name'])
```

### Example: Create Resource

```python
data = {
    'name': 'Example Resource',
    'description': 'This is an example'
}
resource = client.create_resource(data)
print(f"Created resource: {resource['id']}")
```

### Example: Search

```python
results = client.search("keyword", limit=10)
for result in results:
    print(result['name'])
```

### Example: Webhooks

```python
# Get all webhooks
webhooks = client.get_webhooks()

# Create webhook
client.create_webhook(
    url="https://your-site.com/webhook",
    events=["created", "updated"]
)
```

## API Methods

- `get_status()` - Get API status
- `list_resources(**kwargs)` - List resources with optional filtering
- `get_resource(resource_id)` - Get specific resource by ID
- `create_resource(data)` - Create new resource
- `update_resource(resource_id, data)` - Update resource
- `delete_resource(resource_id)` - Delete resource
- `search(query, **kwargs)` - Search resources
- `batch_create(items)` - Create multiple resources
- `batch_update(updates)` - Update multiple resources
- `batch_delete(resource_ids)` - Delete multiple resources
- `get_webhooks()` - Get list of webhooks
- `create_webhook(url, events, **kwargs)` - Create webhook
- `delete_webhook(webhook_id)` - Delete webhook
- `get_account_info()` - Get account information
- `get_usage_stats(start_date, end_date)` - Get usage statistics

## Error Handling

```python
try:
    resource = client.get_resource("id")
except requests.exceptions.HTTPError as e:
    print(f"Error: {e.response.status_code}")
    print(f"Message: {e.response.json()}")
```

## Rate Limiting

The client respects rate limits automatically. Adjust the `timeout` parameter as needed.

## Support

For more information, visit the official confluence documentation.

## License

MIT License
