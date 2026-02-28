# Coda Integration

Coda is a document-database hybrid that combines the flexibility of documents with the power of databases. Build docs, tables, apps, and automations all in one place.

## Installation
```bash
pip install -e .
```

## API Token Setup

1. Sign up at [coda.io](https://coda.io)
2. Go to Account Settings > API Tokens
3. Create a new API token
4. Save the token for your application
5. Note your document IDs for API access

## Usage

### Initialize Client

```python
from coda import CodaClient

client = CodaClient(api_token="your-api-token")
```

### Documents

```python
# List all documents
docs = client.list_docs()
for doc in docs.get('items', []):
    print(f"Doc: {doc['name']} (ID: {doc['id']})")

# Search documents
results = client.search_docs("Project Tracker")

# Get document details
doc = client.get_doc("doc-abc123")

# Create new document
new_doc = client.create_doc(
    title="New Project Tracker",
    folder_id="folder-xyz"
)

# Update document
updated = client.update_doc("doc-abc123", title="Updated Title")

# Delete document
client.delete_doc("doc-abc123")

# Publish document
client.publish_doc("doc-abc123")

# Unpublish document
client.unpublish_doc("doc-abc123")
```

### Tables

```python
DOC_ID = "doc-abc123"

# List tables
tables = client.list_tables(DOC_ID)
for table in tables:
    print(f"Table: {table['name']} (ID: {table['id']})")

# Get table details
table = client.get_table(DOC_ID, "table-xyz")

# Get table schema
schema = client.get_table_schema(DOC_ID, "table-xyz")
```

### Rows CRUD

```python
DOC_ID = "doc-abc123"
TABLE_ID = "table-xyz"

# List rows
rows = client.list_rows(DOC_ID, TABLE_ID, limit=50)

# List rows with query and sort
rows = client.list_rows(
    DOC_ID,
    TABLE_ID,
    query='Status:"Active"',
    sort_by='Created',
    limit=100
)

# Get single row
row = client.get_row(DOC_ID, TABLE_ID, "row-456")

# Create row
new_row = client.create_row(
    DOC_ID,
    TABLE_ID,
    cells=[
        {"column": "Name", "value": "John Doe"},
        {"column": "Email", "value": "john@example.com"},
        {"column": "Status", "value": "Active"}
    ]
)

# Create row with key column
new_row = client.create_row(
    DOC_ID,
    TABLE_ID,
    key_column="Email",
    rows=[
        {"cells": [
            {"column": "Name", "value": "Jane"},
            {"column": "Email", "value": "jane@example.com"}
        ]}
    ]
)

# Update row
updated = client.update_row(
    DOC_ID,
    TABLE_ID,
    "row-456",
    cells=[
        {"column": "Status", "value": "Inactive"},
        {"column": "Email", "value": "new@example.com"}
    ]
)

# Delete row
client.delete_row(DOC_ID, TABLE_ID, "row-456")

# Get all rows (handles pagination automatically)
for row in client.get_all_rows(DOC_ID, TABLE_ID):
    print(row)
```

### Batch Operations

```python
# Batch create rows
batch = client.batch_create_rows(
    DOC_ID,
    TABLE_ID,
    rows=[
        {"cells": [
            {"column": "Name", "value": "Alice"},
            {"column": "Email", "value": "alice@example.com"}
        ]},
        {"cells": [
            {"column": "Name", "value": "Bob"},
            {"column": "Email", "value": "bob@example.com"}
        ]}
    ]
)

# Batch update rows
batch = client.batch_update_rows(
    DOC_ID,
    TABLE_ID,
    updates=[
        {
            "id": "row-456",
            "cells": [{"column": "Status", "value": "Active"}]
        },
        {
            "id": "row-789",
            "cells": [{"column": "Status", "value": "Active"}]
        }
    ]
)

# Batch delete rows
client.batch_delete_rows(
    DOC_ID,
    TABLE_ID,
    row_ids=["row-456", "row-789"]
)
```

### Columns

```python
DOC_ID = "doc-abc123"
TABLE_ID = "table-xyz"

# List columns
columns = client.list_columns(DOC_ID, TABLE_ID)
for col in columns:
    print(f"Column: {col['name']} ({col['type']})")

# Get column details
column = client.get_column(DOC_ID, TABLE_ID, "col-123")

# Create text column
new_col = client.create_column(
    DOC_ID,
    TABLE_ID,
    name="Description",
    type="text"
)

# Create number column
num_col = client.create_column(
    DOC_ID,
    TABLE_ID,
    name="Price",
    type="number",
    options={"currency": "USD"}
)

# Create date column
date_col = client.create_column(
    DOC_ID,
    TABLE_ID,
    name="Due Date",
    type="date"
)

# Update column
updated = client.update_column(
    DOC_ID,
    TABLE_ID,
    "col-123",
    name="Updated Name"
)

# Delete column
client.delete_column(DOC_ID, TABLE_ID, "col-123")
```

### Special Column Types

```python
# Create formula column
formula_col = client.create_formula(
    DOC_ID,
    TABLE_ID,
    name="Total",
    formula='[Price] * [Quantity]'
)

# Create lookup column
lookup_col = client.create_lookup(
    DOC_ID,
    TABLE_ID,
    name="Contact Name",
    relationship="Contact",
    target_column="Name"
)

# Create rollup column
rollup_col = client.create_rollup(
    DOC_ID,
    TABLE_ID,
    name="Total Revenue",
    relationship="Orders",
    aggregation="sum"
)

# Create select column
select_col = client.create_column(
    DOC_ID,
    TABLE_ID,
    name="Status",
    type="checkbox",
    options={
        "color": "green",
        "label": "Active"
    }
)
```

### Buttons

```python
# List buttons
buttons = client.list_buttons(DOC_ID, TABLE_ID)

# Push a button
result = client.push_button(
    DOC_ID,
    TABLE_ID,
    "row-456",
    "btn-123"
)
```

### Views

```python
# List views
views = client.list_views(DOC_ID, TABLE_ID)

# Get view details
view = client.get_view(DOC_ID, TABLE_ID, "view-456")

# Get rows from a specific view
view_rows = client.get_view_rows(DOC_ID, TABLE_ID, "view-456")
```

### Pages

```python
# List pages in document
pages = client.list_pages(DOC_ID)
for page in pages:
    print(f"Page: {page['name']} (ID: {page['id']})")

# Get page details
page = client.get_page(DOC_ID, "page-789")
```

### Import Data

```python
# Import CSV data
csv_data = """Name,Email,Status
John,john@example.com,Active
Jane,jane@example.com,Inactive"""

result = client.import_csv(
    DOC_ID,
    TABLE_ID,
    data=csv_data,
    import_options={
        "headerCaseSensitive": False
    }
)
```

## API Methods

### Documents
- `list_docs(query, limit, page_token)` - List documents
- `get_doc(doc_id)` - Get document details
- `create_doc(title, folder_id, source_doc_id)` - Create document
- `update_doc(doc_id, title, folder_id)` - Update document
- `delete_doc(doc_id)` - Delete document
- `publish_doc(doc_id, share_link_expiration)` - Publish document
- `unpublish_doc(doc_id)` - Unpublish document
- `search_docs(query, limit)` - Search documents

### Tables
- `list_tables(doc_id)` - List tables
- `get_table(doc_id, table_id)` - Get table details
- `get_table_schema(doc_id, table_id)` - Get table schema

### Rows
- `list_rows(doc_id, table_id, ...)` - List rows
- `get_row(doc_id, table_id, row_id)` - Get single row
- `create_row(doc_id, table_id, cells, ...)` - Create row
- `update_row(doc_id, table_id, row_id, cells)` - Update row
- `delete_row(doc_id, table_id, row_id)` - Delete row
- `get_all_rows(doc_id, table_id, max_rows)` - Get all rows with pagination

### Batch Operations
- `batch_create_rows(doc_id, table_id, rows)` - Batch create
- `batch_update_rows(doc_id, table_id, updates)` - Batch update
- `batch_delete_rows(doc_id, table_id, row_ids)` - Batch delete

### Columns
- `list_columns(doc_id, table_id)` - List columns
- `get_column(doc_id, table_id, column_id)` - Get column details
- `create_column(doc_id, table_id, name, type, options)` - Create column
- `update_column(doc_id, table_id, column_id, ...)` - Update column
- `delete_column(doc_id, table_id, column_id)` - Delete column

### Special Column Types
- `create_formula(doc_id, table_id, name, formula)` - Create formula
- `create_lookup(doc_id, table_id, name, relationship, target_column)` - Create lookup
- `create_rollup(doc_id, table_id, name, relationship, aggregation)` - Create rollup

### Buttons
- `list_buttons(doc_id, table_id)` - List buttons
- `push_button(doc_id, table_id, row_id, button_id)` - Trigger button

### Views
- `list_views(doc_id, table_id)` - List views
- `get_view(doc_id, table_id, view_id)` - Get view details
- `get_view_rows(doc_id, table_id, view_id, limit)` - Get rows from view

### Pages
- `list_pages(doc_id)` - List pages
- `get_page(doc_id, page_id)` - Get page details

### Import
- `import_csv(doc_id, table_id, data, import_options)` - Import CSV data

## Cell References

Coda uses column names for cell operations:

```python
# Cell with column name
cells = [
    {"column": "Name", "value": "John"},
    {"column": "Email", "value": "john@example.com"}
]

# Cell with column ID
cells = [
    {"column": "c-abc123", "value": "John"}
]

# Multiple rows in batch
rows = [
    {
        "cells": [
            {"column": "Name", "value": "Alice"},
            {"column": "Status", "value": "Active"}
        ]
    }
]
```

## Query Syntax

Coda supports various query formats:

```python
# Simple text search
client.list_rows(DOC_ID, TABLE_ID, query="John")

# Exact match
client.list_rows(DOC_ID, TABLE_ID, query='Name:"John"')

# Status matching
client.list_rows(DOC_ID, TABLE_ID, query='Status:"Active"')

# View filtering
client.list_rows(DOC_ID, TABLE_ID, query='view:"view-456"')

# Multiple filters (use AND in Coda UI to create a view)
# Then query by that view
```

## Column Types

Coda supports these column types:

- `text` - Text
- `number` - Numbers
- `checkbox` - Boolean (yes/no)
- `date` - Date values
- `dateTime` - Date and time
- `currency` - Money values
- `formula` - Computed values
- `lookup` - Reference related data
- `rollup` - Aggregates related data
- `relation` - Links between tables
- `multiselect` - Multiple options
- `select` - Single option
- `people` - People/assignees
- `files` - File attachments
- `image` - Image files
- `button` - Interactive buttons
- `url` - Links
- `email` - Email addresses
- `progress` - Progress bars
- `slider` - Numeric sliders
- `duration` - Time durations

## Formula Examples

```python
# Create formula column
client.create_formula(
    DOC_ID,
    TABLE_ID,
    name="Total Cost",
    formula='[Price] * [Quantity]'
)

# Date formula
client.create_formula(
    DOC_ID,
    TABLE_ID,
    name="Days Since",
    formula='TODAY() - [Created Date]'
)

# Conditional formula
client.create_formula(
    DOC_ID,
    TABLE_ID,
    name="Status Badge",
    formula='IF([Status] = "Done", "✅", "❌")'
)

# Rollup
client.create_rollup(
    DOC_ID,
    TABLE_ID,
    name="Total Orders",
    relationship="Orders",
    aggregation="sum"
)

# Count related
client.create_rollup(
    DOC_ID,
    TABLE_ID,
    name="Order Count",
    relationship="Orders",
    aggregation="count"
)
```

## Best Practices

1. **Pagination**: Use `pageToken` for large datasets
2. **Column references**: Use column names for clarity
3. **Batch operations**: Use batch methods for bulk operations
4. **Error handling**: Always catch and handle HTTP exceptions
5. **View filtering**: Create views for common filters, then query by view
6. **Formula performance**: Keep formulas simple for better performance
7. **Rate limits**: Coda has rate limits - implement backoff if needed

## Common Patterns

```python
# Create table with columns
doc = client.create_doc("New Doc")
table = tables[0]  # Get default table

# Add columns
client.create_column(DOC_ID, TABLE_ID, "Name", "text")
client.create_column(DOC_ID, TABLE_ID, "Email", "email")
client.create_column(DOC_ID, TABLE_ID, "Status", "checkbox")

# Add data
client.batch_create_rows(DOC_ID, TABLE_ID, rows=[...])

# Create summary formula
client.create_formula(DOC_ID, TABLE_ID, "Summary", ...)

# Publish for sharing
client.publish_doc(DOC_ID)
```