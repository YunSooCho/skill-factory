# Nethunt API Client

Python client library for Nethunt API - CRM and database management integrated with Gmail.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

You need an API key from Nethunt. Initialize the client with your API key:

```python
from nethunt_client import NethuntClient

client = NethuntClient(api_key="your_api_key_here")
```

## Usage Examples

### Create a Record

```python
result = client.create_record(
    folder_id="folder_123",
    fields={
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "company": "Acme Corp."
    },
    tags=["client", "new"]
)
```

### Get Record Details

```python
record = client.get_record(record_id="record_123")
```

### Update a Record

```python
result = client.update_record(
    record_id="record_123",
    fields={
        "company": "Acme Corporation",
        "status": "active"
    },
    add_tags=["vip"],
    remove_tags=["new"]
)
```

### Search Records

```python
records = client.search_records(
    folder_id="folder_123",
    query="Acme",
    fields={"status": "client"},
    tags=["vip"],
    limit=50,
    sort_by="created_at",
    sort_order="desc"
)
```

### Delete a Record

```python
result = client.delete_record(record_id="record_123")
```

### Create Comment

```python
result = client.create_comment(
    record_id="record_123",
    text="Excellent client, closed the deal successfully!",
    comment_type="note"
)
```

### Get Comments for Record

```python
comments = client.get_comments(
    record_id="record_123",
    limit=50
)
```

### Update Comment

```python
result = client.update_comment(
    comment_id="comment_123",
    text="Updated comment text"
)
```

### Delete Comment

```python
result = client.delete_comment(comment_id="comment_123")
```

### Get Folders

```python
folders = client.get_folders()
```

### Get Folder Details

```python
folder = client.get_folder(folder_id="folder_123")
```

### Get Fields for Folder

```python
fields = client.get_fields(folder_id="folder_123")
```

## Webhook Handling

```python
# Verify webhook signature
is_valid = client.verify_webhook_signature(
    payload=request_body,
    signature=request.headers.get("X-Webhook-Signature"),
    webhook_secret="your_webhook_secret"
)

# Handle webhook event
data = client.handle_webhook(payload)
```

## API Actions

### Record Management
- Create Record
- Get Record
- Update Record
- Delete Record
- Search Records

### Comment Management
- Create Comment
- Get Comments
- Update Comment
- Delete Comment

### Folder & Field Management
- Get Folders
- Get Folder Details
- Get Fields for Folder

## Triggers

- New Record
- Update Record
- New Comment

## Error Handling

```python
from nethunt_client import NethuntClient, NethuntAPIError

try:
    record = client.get_record(record_id="invalid_id")
except NethuntAPIError as e:
    print(f"Error: {e}")
```

## Notes

- API uses Bearer token authentication
- Records are organized in folders with custom fields
- Tags can be added, removed, or replaced
- Search supports filtering by fields and tags
- Webhook signature verification uses HMAC-SHA256
- Sorting options available for search results