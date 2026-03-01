# AITable Database Integration

AITable is a modern spreadsheet-database hybrid that allows you to organize data like a spreadsheet with the power of a database, featuring AI-enhanced data analysis and real-time collaboration.

## Installation
```bash
pip install -e .
```

## API Token Setup

1. Sign up at [aitable.ai](https://aitable.ai)
2. Go to Account Settings > API Tokens
3. Generate a new API token
4. Copy the token for use in your application

## Usage

### Initialize Client

```python
from aitable import AITableClient

client = AITableClient(api_token="your-api-token")
```

### Spaces and Bases

```python
# Get all spaces
spaces = client.get_spaces()
for space in spaces:
    print(f"Space: {space['name']}")

# Get bases in a space
bases = client.get_bases(space_id="spcXXX")
for base in bases:
    print(f"Base: {base['name']} (ID: {base['id']})")

# Get base details
base = client.get_base("bseXXX")
print(f"Base: {base['name']}")
```

### Tables

```python
# Get tables in a base
tables = client.get_tables("bseXXX")
for table in tables:
    print(f"Table: {table['name']} (ID: {table['id']})")

# Get table details
table = client.get_table("bseXXX", "tblXXX")

# Get table schema
schema = client.get_schema("bseXXX", "tblXXX")
for field in schema['fields']:
    print(f"Field: {field['name']} ({field['type']})")
```

### Records CRUD

```python
BASE_ID = "bseXXX"
TABLE_ID = "tblXXX"

# Get all records
records = client.get_records(BASE_ID, TABLE_ID)

# Get with filters
records = client.get_records(
    BASE_ID,
    TABLE_ID,
    page_size=50,
    filter_by_formula="{Status} = 'Active'",
    sort=[{"field": "Created", "direction": "desc"}]
)

# Get single record
record = client.get_record(BASE_ID, TABLE_ID, "recXXX")

# Create record
new_record = client.create_record(
    BASE_ID,
    TABLE_ID,
    fields={
        "Name": "John Doe",
        "Email": "john@example.com",
        "Status": "Active"
    }
)

# Update record
updated = client.update_record(
    BASE_ID,
    TABLE_ID,
    "recXXX",
    fields={"Status": "Inactive"}
)

# Delete record
client.delete_record(BASE_ID, TABLE_ID, "recXXX")
```

### Batch Operations

```python
# Batch create
batch = client.batch_create_records(
    BASE_ID,
    TABLE_ID,
    records=[
        {"fields": {"Name": "Alice", "Email": "alice@example.com"}},
        {"fields": {"Name": "Bob", "Email": "bob@example.com"}}
    ]
)

# Batch update
batch = client.batch_update_records(
    BASE_ID,
    TABLE_ID,
    records=[
        {"id": "rec1", "fields": {"Status": "Active"}},
        {"id": "rec2", "fields": {"Status": "Active"}}
    ]
)

# Batch delete
client.batch_delete_records(
    BASE_ID,
    TABLE_ID,
    record_ids=["rec1", "rec2"]
)
```

### Fields Management

```python
# Get fields
fields = client.get_fields(BASE_ID, TABLE_ID)

# Create field
new_field = client.create_field(
    BASE_ID,
    TABLE_ID,
    name="Priority",
    type="singleSelect",
    options={"choices": ["High", "Medium", "Low"]}
)

# Update field
updated = client.update_field(
    BASE_ID,
    TABLE_ID,
    "fldXXX",
    name="Urgency"
)

# Delete field
client.delete_field(BASE_ID, TABLE_ID, "fldXXX")
```

### Views

```python
# Get views
views = client.get_views(BASE_ID, TABLE_ID)

# Get records from a specific view
records = client.get_records(
    BASE_ID,
    TABLE_ID,
    view_id="viwXXX"
)
```

### Attachments

```python
# Upload attachment
client.upload_attachment(
    BASE_ID,
    TABLE_ID,
    "recXXX",
    "fldXXX",
    "/path/to/file.pdf"
)
```

### Collaboration

```python
# Get collaborators
collaborators = client.get_collaborators(BASE_ID)

# Add collaborator
client.add_collaborator(
    BASE_ID,
    email="user@example.com",
    role="editor"  # or "viewer", "owner"
)

# Remove collaborator
client.remove_collaborator(BASE_ID, "usrXXX")
```

### Searching and Filtering

```python
# Search records
results = client.search_records(
    BASE_ID,
    TABLE_ID,
    query="john",
    fields=["Name", "Email"]
)

# Query by formula
results = client.query_by_formula(
    BASE_ID,
    TABLE_ID,
    formula="AND({Status} = 'Active', {Email} != '')"
)
```

### Webhooks

```python
# Get webhooks
webhooks = client.get_webhooks(BASE_ID)

# Create webhook
webhook = client.create_webhook(
    BASE_ID,
    TABLE_ID,
    url="https://your-server.com/webhook",
    events=["record.created", "record.updated", "record.deleted"]
)

# Delete webhook
client.delete_webhook(BASE_ID, "whkXXX")
```

### Forms

```python
# Create a form
form = client.create_form(
    BASE_ID,
    TABLE_ID,
    name="Contact Form",
    description="Submit your contact info"
)

# Get form entries
entries = client.get_form_entries("frmXXX")
```

## API Methods

### Spaces & Bases
- `get_spaces()` - List spaces
- `get_space(space_id)` - Get space details
- `get_bases(space_id)` - List bases
- `get_base(base_id)` - Get base details

### Tables & Fields
- `get_tables(base_id)` - List tables
- `get_table(base_id, table_id)` - Get table details
- `get_schema(base_id, table_id)` - Get table schema
- `get_fields(base_id, table_id)` - List fields
- `create_field(base_id, table_id, name, type, options)` - Create field
- `update_field(base_id, table_id, field_id, ...)` - Update field
- `delete_field(base_id, table_id, field_id)` - Delete field

### Records
- `get_records(base_id, table_id, ...)` - List records with filters
- `get_record(base_id, table_id, record_id)` - Get single record
- `create_record(base_id, table_id, fields)` - Create record
- `update_record(base_id, table_id, record_id, fields)` - Update record
- `delete_record(base_id, table_id, record_id)` - Delete record

### Batch Operations
- `batch_create_records(base_id, table_id, records)` - Batch create
- `batch_update_records(base_id, table_id, records)` - Batch update
- `batch_delete_records(base_id, table_id, record_ids)` - Batch delete

### Views
- `get_views(base_id, table_id)` - List views

### Collaboration
- `get_collaborators(base_id)` - List collaborators
- `add_collaborator(base_id, email, role)` - Add collaborator
- `remove_collaborator(base_id, user_id)` - Remove collaborator

### Search & Query
- `search_records(base_id, table_id, query, fields)` - Search records
- `query_by_formula(base_id, table_id, formula)` - Query with formula

### Webhooks
- `get_webhooks(base_id)` - List webhooks
- `create_webhook(base_id, table_id, url, events)` - Create webhook
- `delete_webhook(base_id, webhook_id)` - Delete webhook

### Forms
- `create_form(base_id, table_id, name, description)` - Create form
- `get_form_entries(form_id)` - Get form submissions

## Field Types

AITable supports various field types:

- `text` - Single line text
- `longText` - Multi-line text
- `number` - Numeric values
- `singleSelect` - Single choice from options
- `multiSelect` - Multiple choices
- `date` - Date and time
- `checkbox` - Boolean values
- `attachment` - File attachments
- `formula` - Computed fields
- `link` - Relationships between tables
- `lookup` - Reference related records
- `count` - Count related records
- `member` - Team member assignment
- `createdTime` - Timestamp
- `createdBy` - Creator info
- `lastModifiedTime` - Last modified timestamp
- `lastModifiedBy` - Last modifier info

## Formula Examples

```python
# Filter for active users
client.get_records(BASE_ID, TABLE_ID, filter_by_formula="{Status}='Active'")

# Query for records created in last 7 days
client.get_records(
    BASE_ID,
    TABLE_ID,
    filter_by_formula="TODAY() - DATETIME_DIFF({Created Time}, TODAY(), 'days') <= 7"
)

# Filter with multiple conditions
client.get_records(
    BASE_ID,
    TABLE_ID,
    filter_by_formula="AND({Status}='Active', {Assignee} != '', {Priority}='High')"
)

# Sorting
records = client.get_records(
    BASE_ID,
    TABLE_ID,
    sort=[
        {"field": "Priority", "direction": "desc"},
        {"field": "Created Time", "direction": "asc"}
    ]
)
```

## Rate Limits

AITable API has rate limits to ensure fair usage. If you exceed the limit, you'll receive a 429 Too Many Requests response. Implement exponential backoff when handling rate limits.

## Error Handling

```python
try:
    records = client.get_records(BASE_ID, TABLE_ID)
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Invalid API token")
    elif e.response.status_code == 404:
        print("Resource not found")
    elif e.response.status_code == 429:
        print("Rate limit exceeded")
    else:
        print(f"Error: {e}")
```

## Best Practices

1. **Batch operations**: Use batch methods for bulk operations
2. **Pagination**: Use `page_size` to optimize large result sets
3. **Field selection**: Only request needed fields
4. **Formula queries**: Use server-side filtering when possible
5. **Webhook retries**: Implement retry logic for webhook failures
6. **Error handling**: Always handle HTTP errors gracefully