# Airtable OAuth Integration

Airtable OAuth provides secure OAuth 2.0 authentication for accessing Airtable bases without sharing API keys directly. This client enables secure, delegated access to Airtable's API.

## Installation
```bash
pip install -e .
```

## OAuth App Setup

1. Go to [Airtable's Developer Console](https://airtable.com/create/oauth)
2. Create a new OAuth application
3. Configure:
   - **Name**: Your app name
   - **Redirect URI**: Your callback URL (e.g., `http://localhost:8000/callback`)
   - **Scopes**: Choose necessary scopes (e.g., `data.records:read`, `data.records:write`)
4. Save your **Client ID** and **Client Secret**

## Usage

### OAuth Flow

```python
from airtable_oauth import AirtableOAuthClient

client = AirtableOAuthClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="http://localhost:8000/callback"
)

# Step 1: Get authorization URL
auth_url = client.get_authorization_url()
print(f"Visit: {auth_url}")

# Step 2: User authorizes and receives callback with code
# When user is redirected back, extract 'code' from URL

# Step 3: Exchange code for access token
token_data = client.exchange_code_for_token("AUTHORIZATION_CODE")
print(f"Access token: {token_data['access_token']}")

# Step 4: Use the access token for API calls
bases = client.get_bases()
```

### Using Existing Tokens

If you already have access and refresh tokens:

```python
client = AirtableOAuthClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="http://localhost:8000/callback"
)

client.set_access_token("your-access-token")
client.set_refresh_token("your-refresh-token")

# Refresh if needed
client.refresh_access_token()
```

### Working with Bases and Tables

```python
# Get all accessible bases
bases = client.get_bases()
for base in bases:
    print(f"Base: {base['name']} (ID: {base['id']})")

# Get base details
base = client.get_base("baseXXX")

# Get tables in a base
tables = client.get_tables("baseXXX")
for table in tables:
    print(f"Table: {table['name']} (ID: {table['id']})")
```

### CRUD Operations

```python
BASE_ID = "appXXX"
TABLE_ID = "tblXXX"

# Get records
records = client.get_records(BASE_ID, TABLE_ID, max_records=50)

# Get with filtering
records = client.get_records(
    BASE_ID,
    TABLE_ID,
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

# Update record (partial)
updated = client.update_record(
    BASE_ID,
    TABLE_ID,
    "recXXX",
    fields={"Status": "Inactive"}
)

# Replace record (all fields)
replaced = client.replace_record(
    BASE_ID,
    TABLE_ID,
    "recXXX",
    fields={"Name": "Jane Smith", "Email": "jane@example.com"}
)

# Delete record
client.delete_record(BASE_ID, TABLE_ID, "recXXX")
```

### Batch Operations

```python
# Create multiple records
batch = client.create_records(
    BASE_ID,
    TABLE_ID,
    records=[
        {"fields": {"Name": "Alice", "Email": "alice@example.com"}},
        {"fields": {"Name": "Bob", "Email": "bob@example.com"}},
        {"fields": {"Name": "Charlie", "Email": "charlie@example.com"}}
    ]
)

# Update multiple records
batch = client.update_records(
    BASE_ID,
    TABLE_ID,
    records=[
        {"id": "rec1", "fields": {"Status": "Active"}},
        {"id": "rec2", "fields": {"Status": "Active"}}
    ]
)

# Delete multiple records
batch = client.delete_records(
    BASE_ID,
    TABLE_ID,
    record_ids=["rec1", "rec2", "rec3"]
)
```

### Attachments

```python
# Upload attachment to a record
result = client.upload_attachment(
    BASE_ID,
    TABLE_ID,
    "recXXX",
    "Attachments",
    "/path/to/file.pdf"
)

# The attachment will be added to the specified field
```

### Advanced Querying

```python
# Query with multiple conditions
results = client.query(
    BASE_ID,
    TABLE_ID,
    max_records=100,
    fields=["Name", "Email", "Status"],
    sort=[{"field": "Name", "direction": "asc"}],
    formula="AND({Status} = 'Active', {Email} != '')"
)

# Get schema
schema = client.get_schema(BASE_ID)
for table in schema['tables']:
    print(f"Table: {table['name']}")
    for field in table['fields']:
        print(f"  Field: {field['name']} ({field['type']})")
```

### Token Management

```python
# Refresh access token
token_data = client.refresh_access_token()
print(f"New access token: {token_data['access_token']}")

# Token data includes:
# - access_token: Short-lived token for API calls
# - refresh_token: Long-lived token for refreshing
# - expires_in: Token lifetime in seconds
# - token_type: Usually "Bearer"
```

## API Methods

### OAuth
- `get_authorization_url(state, scopes)` - Generate authorization URL
- `exchange_code_for_token(code)` - Exchange code for access token
- `refresh_access_token()` - Refresh expired access token
- `set_access_token(token)` - Set pre-existing access token
- `set_refresh_token(token)` - Set pre-existing refresh token

### Bases & Tables
- `get_bases()` - List accessible bases
- `get_base(base_id)` - Get base details
- `get_tables(base_id)` - List tables in base
- `get_schema(base_id)` - Get base schema

### Records
- `get_records(base_id, table_id, ...)` - List records with filters
- `get_record(base_id, table_id, record_id)` - Get single record
- `create_record(base_id, table_id, fields)` - Create record
- `update_record(base_id, table_id, record_id, fields)` - Partial update
- `replace_record(base_id, table_id, record_id, fields)` - Full replace
- `delete_record(base_id, table_id, record_id)` - Delete record

### Batch Operations
- `create_records(base_id, table_id, records)` - Batch create
- `update_records(base_id, table_id, records)` - Batch update
- `delete_records(base_id, table_id, record_ids)` - Batch delete

### Files
- `upload_attachment(base_id, table_id, record_id, field_name, file_path)` - Upload attachment

### Advanced
- `query(base_id, table_id, ...)` - Advanced query with filtering

## OAuth Scopes

Available scopes for access control:

- `data.records:read` - Read records
- `data.records:write` - Create/update/delete records
- `data.recordComments:read` - Read record comments
- `data.recordComments:write` - Create record comments
- `schema.bases:read` - Read base schema
- `schema.bases:write` - Modify base schema
- `webhooks:manage` - Manage webhooks

## Error Handling

The client raises standard HTTP exceptions:

```python
try:
    records = client.get_records(BASE_ID, TABLE_ID)
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Token expired. Refreshing...")
        client.refresh_access_token()
    elif e.response.status_code == 404:
        print("Resource not found")
    else:
        print(f"Error: {e}")
```

## Best Practices

1. **Store refresh tokens securely**: Never expose them in client-side code
2. **Refresh tokens proactively**: Check token expiration and refresh before use
3. **Use batch operations**: For bulk operations to reduce API calls
4. **Cache schema responses**: Schema data doesn't change frequently
5. **Handle rate limits**: Airtable has rate limits (5 requests/sec per base)
6. **Use formulas wisely**: Complex formulas can slow down queries

## Webhooks

Configure webhooks in Airtable's UI to receive real-time updates:
- Record created/updated/deleted
- Field changes
- Comment additions

You can register webhooks using the OAuth token with full base access.