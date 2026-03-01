# Glide API Client

A Python client for interacting with the Glide API.

## About

Glide is a no-code platform that allows you to build apps from data sources like Google Sheets, Excel, and SQL databases. This client provides access to Glide's REST API for reading, creating, updating, and deleting rows in Glide tables programmatically.

## Installation

```bash
pip install requests
```

## API Key Setup

1. Log in to your [Glide account](https://www.glideapps.com/)
2. Go to your app's settings
3. Navigate to "API" or "Integrations" section
4. Generate a new API key
5. Copy your API key and keep it secure

## Finding Your App ID

- Your app ID is available in the URL when you open your app: `https://apps.glideapps.com/{app_id}/...`
- You can also find it in your app settings under "API" section

## Usage

```python
from glide import GlideClient

# Initialize the client
client = GlideClient(api_key="your_api_key_here")

# List rows from a table
rows = client.list_rows(app_id="your_app_id", table_name="Users", limit=50)
for row in rows.get('rows', []):
    print(row)

# Get a specific row
row = client.get_row(app_id="app_id", table_name="Users", row_id="row_123")

# Create a new row
new_row = client.create_row(
    app_id="app_id",
    table_name="Users",
    row_data={
        "Name": "John Doe",
        "Email": "john@example.com",
        "Age": 30
    }
)

# Update a row
updated_row = client.update_row(
    app_id="app_id",
    table_name="Users",
    row_id="row_123",
    row_data={"Age": 31}
)

# Delete a row
client.delete_row(app_id="app_id", table_name="Users", row_id="row_123")

# Bulk operations
bulk_created = client.bulk_create_rows(
    app_id="app_id",
    table_name="Users",
    rows=[
        {"Name": "Alice", "Email": "alice@example.com"},
        {"Name": "Bob", "Email": "bob@example.com"}
    ]
)

# Query with filters
results = client.query_rows(
    app_id="app_id",
    table_name="Users",
    filters=[
        {"column": "Age", "operator": ">", "value": 25},
        {"column": "Name", "operator": "contains", "value": "John"}
    ],
    join_type="and"
)

# Get table schema
schema = client.get_table_schema(app_id="app_id", table_name="Users")

# List all tables
tables = client.list_tables(app_id="app_id")

# Close the session
client.close()
```

## API Endpoints Supported

### Table Operations
- `list_rows()` - List rows from a table with pagination
- `get_row()` - Get a specific row by ID
- `create_row()` - Create a new row
- `update_row()` - Update an existing row
- `delete_row()` - Delete a row

### Bulk Operations
- `bulk_create_rows()` - Create multiple rows at once
- `bulk_update_rows()` - Update multiple rows at once
- `bulk_delete_rows()` - Delete multiple rows at once

### Query Operations
- `query_rows()` - Query rows with filters and conditions

### File Operations
- `upload_file()` - Upload files to Glide

### App Operations
- `get_app_info()` - Get app information
- `list_tables()` - List all tables in an app
- `get_table_schema()` - Get table schema and columns

### Action Operations
- `trigger_action()` - Trigger custom app actions

## Query Operators

Supported operators for filters:
- `==` : Equals
- `!=` : Not equals
- `>` : Greater than
- `<` : Less than
- `>=` : Greater than or equal
- `<=` : Less than or equal
- `contains` : Contains string
- `startsWith` : Starts with string
- `endsWith` : Ends with string

## Rate Limits

The Glide API has rate limits. Check your specific plan for details. Implement proper error handling and exponential backoff when encountering rate limits.

## Error Handling

The client will raise `requests.exceptions.RequestException` on API errors. Always wrap API calls in try-except blocks for production code:

```python
try:
    rows = client.list_rows(app_id="app_id", table_name="Users")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

## API Documentation

Check the official Glide documentation for the most up-to-date API information and endpoint details.

## License

This client is provided as-is for integration with the Glide API.