# Baserow Database Integration

Baserow is an open-source no-code database that you can self-host or use in the cloud. It provides an Airtable-like experience with full API access and unlimited rows.

## Installation
```bash
pip install -e .
```

## API Token Setup

### Cloud
1. Sign up at [baserow.io](https://baserow.io)
2. Go to Settings > Account > Tokens
3. Generate a new API token
4. Copy the token

### Self-Hosted
1. Access your Baserow instance
2. Go to Settings > Profile > API Tokens
3. Create a new token
4. Use your instance's base URL

## Usage

### Initialize Client

```python
from baserow import BaserowClient

# Cloud
client = BaserowClient(
    api_token="your-api-token",
    base_url="https://api.baserow.io/api"
)

# Self-hosted
client = BaserowClient(
    api_token="your-api-token",
    base_url="https://baserow.yourdomain.com/api"
)
```

### Tables

```python
# List applications
apps = client.list_applications()

# List tables in a database
tables = client.list_tables(database_id=123)
for table in tables:
    print(f"Table: {table['name']} (ID: {table['id']})")

# Get table details
table = client.get_table(table_id=456)

# Create table
new_table = client.create_table(
    database_id=123,
    name="Customers",
    data=[
        {
            "name": "Name",
            "type": "text",
            "primary": True
        },
        {
            "name": "Email",
            "type": "text"
        },
        {
            "name": "Phone",
            "type": "phone_number"
        }
    ]
)

# Update table
updated = client.update_table(table_id=456, name="Client Database")

# Delete table
client.delete_table(table_id=456)
```

### Rows CRUD

```python
TABLE_ID = 456

# List rows
rows = client.list_rows(TABLE_ID, page=1, size=50)

# Get single row
row = client.get_row(TABLE_ID, row_id=789)

# Create row
new_row = client.create_row(
    TABLE_ID,
    data={
        "Name": "John Doe",
        "Email": "john@example.com",
        "Phone": "+1234567890"
    }
)

# Update row
updated = client.update_row(
    TABLE_ID,
    row_id=789,
    data={"Email": "newemail@example.com"}
)

# Delete row
client.delete_row(TABLE_ID, row_id=789)
```

### Batch Operations

```python
# Batch create
batch = client.batch_create_rows(
    TABLE_ID,
    rows=[
        {"Name": "Alice", "Email": "alice@example.com"},
        {"Name": "Bob", "Email": "bob@example.com"},
        {"Name": "Charlie", "Email": "charlie@example.com"}
    ]
)

# Batch update
batch = client.batch_update_rows(
    TABLE_ID,
    items=[
        {"id": 789, "Email": "updated@example.com"},
        {"id": 790, "Email": "also_updated@example.com"}
    ]
)

# Batch delete
client.batch_delete_rows(TABLE_ID, row_ids=[789, 790, 791])
```

### Fields

```python
# List fields
fields = client.list_fields(TABLE_ID)

# Get field details
field = client.get_field(field_id=100)

# Create text field
new_field = client.create_field(
    table_id=TABLE_ID,
    type="text",
    name="Description"
)

# Create number field
num_field = client.create_field(
    table_id=TABLE_ID,
    type="number",
    name="Price",
    number_decimal_places=2,
    number_negative=True
)

# Create select field
select_field = client.create_field(
    table_id=TABLE_ID,
    type="single_select",
    name="Status",
    select_options=[
        {"value": "Active", "color": "green"},
        {"value": "Inactive", "color": "red"}
    ]
)

# Create date field
date_field = client.create_field(
    table_id=TABLE_ID,
    type="date",
    name="Created",
    date_format="YYYY-MM-DD",
    date_include_time=False
)

# Update field
updated = client.update_field(field_id=100, name="Updated Description")

# Delete field
client.delete_field(field_id=100)
```

### Special Field Types

```python
# Link to another table
link_field = client.create_link_row_field(
    table_id=TABLE_ID,
    name="Orders",
    linked_table_id=200
)

# Lookup field (reference linked table)
lookup_field = client.create_lookup_field(
    table_id=TABLE_ID,
    name="Order Count",
    through_field_id=link_field['id'],
    target_field_id=300  # A field in the linked table
)

# Formula field
formula_field = client.create_formula_field(
    table_id=TABLE_ID,
    name="Total",
    formula="field('Price') * field('Quantity')"
)

# Multiple select field
multi_select = client.create_field(
    table_id=TABLE_ID,
    type="multiple_select",
    name="Tags",
    select_options=[
        {"value": "Important", "color": "red"},
        {"value": "Review", "color": "yellow"},
        {"value": "Approved", "color": "green"}
    ]
)
```

### Views

```python
# List views
views = client.list_views(TABLE_ID)

# Get view details
view = client.get_view(view_id=150)

# Create grid view
grid_view = client.create_view(
    table_id=TABLE_ID,
    type="grid",
    name="Active Customers",
    filters=[
        {"field": "Status", "value": "Active"}
    ],
    sortings=[
        {"field": "Name", "order": "ASC"}
    ]
)

# Create gallery view
gallery_view = client.create_view(
    table_id=TABLE_ID,
    type="gallery",
    name="Product Gallery"
)

# Update view
updated = client.update_view(view_id=150, name="Updated View")

# Delete view
client.delete_view(view_id=150)

# Get rows by view
results = client.get_rows_by_view(view_id=150)
```

### Special Views

```python
# Gallery view
gallery = client.get_gallery_view(view_id=150)

# Calendar view
calendar = client.get_calendar_view(
    view_id=151,
    from_date="2024-01-01",
    to_date="2024-12-31"
)

# Kanban view
kanban = client.get_kanban_view(view_id=152)

# Grid view
grid = client.get_grid_view(view_id=153)
```

### File Uploads

```python
# Upload file from URL
uploaded = client.upload_file_via_url(
    url="https://example.com/image.jpg"
)
file_url = uploaded['url']

# Upload file from local path
uploaded = client.upload_file("/path/to/file.pdf")
file_url = uploaded['url']

# Use in row creation
client.create_row(
    TABLE_ID,
    data={
        "Name": "Document",
        "File": [
            {"name": "file.pdf", "url": file_url}
        ]
    }
)
```

### Search & Filter

```python
# Search rows
results = client.search_rows(
    TABLE_ID,
    search_query="john",
    user_field_names=True
)

# Filter rows with user field names
rows = client.filter_rows(
    TABLE_ID,
    filters=[
        {"field": "Status", "value": "Active"},
        {"field": "Email", "value": "john@example.com"}
    ]
)

# Get with view filters
view_results = client.get_rows_by_view(
    view_id=150,
    page=1,
    size=100
)
```

## API Methods

### Tables
- `list_applications()` - List applications
- `list_tables(database_id)` - List tables
- `get_table(table_id)` - Get table details
- `create_table(database_id, name, data)` - Create table
- `update_table(table_id, name)` - Update table
- `delete_table(table_id)` - Delete table

### Rows
- `list_rows(table_id, page, size, search)` - List rows
- `get_row(table_id, row_id)` - Get single row
- `create_row(table_id, data, ...)` - Create row
- `update_row(table_id, row_id, data)` - Update row
- `delete_row(table_id, row_id)` - Delete row
- `batch_create_rows(table_id, rows)` - Batch create
- `batch_update_rows(table_id, items)` - Batch update
- `batch_delete_rows(table_id, row_ids)` - Batch delete

### Fields
- `list_fields(table_id)` - List fields
- `get_field(field_id)` - Get field details
- `create_field(table_id, type, name, ...)` - Create field
- `update_field(field_id, name, ...)` - Update field
- `delete_field(field_id)` - Delete field

### Views
- `list_views(table_id)` - List views
- `get_view(view_id)` - Get view details
- `create_view(table_id, type, name, ...)` - Create view
- `update_view(view_id, name, ...)` - Update view
- `delete_view(view_id)` - Delete view
- `get_rows_by_view(view_id, ...)` - Get rows by view

### Files
- `upload_file_via_url(url)` - Upload file from URL
- `upload_file(file_path)` - Upload local file

### Special Fields
- `create_link_row_field(...)` - Create link field
- `create_lookup_field(...)` - Create lookup field
- `create_formula_field(...)` - Create formula field

## Field Types

Baserow supports many field types:

- `text` - Single line text
- `long_text` - Multi-line text
- `url` - URL links
- `email` - Email addresses
- `phone_number` - Phone numbers
- `number` - Numeric values
- `rating` - Star ratings
- `boolean` - True/False
- `date` - Date and time
- `single_select` - Single choice
- `multiple_select` - Multiple choices
- `link_row` - Links to other tables
- `lookup` - Lookup from linked tables
- `formula` - Computed fields
- `count` - Count linked rows
- `rollup` - Aggregates linked rows
- `created_by` - Who created row
- `created_on` - Creation timestamp
- `last_modified_by` - Last modifier
- `last_modified_on` - Last modified timestamp
- `file` - File attachments
- `single_file` - Single file
- `password` - Encrypted password

## Best Practices

1. **Batch operations**: Use batch methods for bulk operations
2. **User field names**: Set `user_field_names=True` for readable field names
3. **Pagination**: Handle large result sets with pagination
4. **Index fields**: Use appropriate field types for performance
5. **View filters**: Use views for consistent filtering
6. **Link fields**: Use link_row for relationships instead of duplicate data