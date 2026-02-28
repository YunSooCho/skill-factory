# Caspio Cloud Database Integration

Caspio is a low-code platform for building cloud database applications with visual app builders, DataPages, and no-code development tools.

## Installation
```bash
pip install -e .
```

## API Credentials Setup

1. Sign up at [caspio.com](https://caspio.com)
2. Go to Account Settings > API Access
3. Create a new OAuth 2.0 application:
   - **Client ID** - Your application identifier
   - **Client Secret** - Your application secret
   - **Account ID** - Found in account settings
4. Configure redirect URI (if needed)
5. Save credentials for your app

## Usage

### Initialize Client

```python
from caspio import CaspioClient

client = CaspioClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    account_id="your-account-id"
)

# Client auto-authenticates on first request
# Or manually authenticate:
token = client.authenticate()
```

### Tables

```python
ACCOUNT_ID = "your-account-id"

# List all tables
tables = client.list_tables(ACCOUNT_ID)
for table in tables:
    print(f"Table: {table['TableName']}")

# Get table details
table = client.get_table(ACCOUNT_ID, "Customers")

# Get table schema
schema = client.describe_table(ACCOUNT_ID, "Customers")
print(f"Columns: {schema['Columns']}")

# Create table
new_table = client.create_table(
    ACCOUNT_ID,
    "Products",
    columns=[
        {"Name": "ProductID", "DataType": "Number", "Unique": True},
        {"Name": "Name", "DataType": "Text"},
        {"Name": "Price", "DataType": "Number", "DecimalPlaces": 2},
        {"Name": "Description", "DataType": "Memo"}
    ],
    primary_key="ProductID"
)

# Delete table
client.delete_table(ACCOUNT_ID, "OldTable")
```

### CRUD Operations

```python
# Get rows
rows = client.get_rows(ACCOUNT_ID, "Customers")

# Get rows with parameters
rows = client.get_rows(
    ACCOUNT_ID,
    "Customers",
    params={
        'q.select': 'Name, Email, Phone',
        'q.orderBy': 'Name ASC',
        'q.limit': '50'
    }
)

# Get single row
row = client.get_row(ACCOUNT_ID, "Customers", "123")

# Insert row
new_row = client.insert_row(
    ACCOUNT_ID,
    "Customers",
    data={
        "Name": "John Doe",
        "Email": "john@example.com",
        "Phone": "555-1234",
        "Status": "Active"
    }
)

# Update row
updated = client.update_row(
    ACCOUNT_ID,
    "Customers",
    "123",
    data={"Status": "Inactive", "Email": "new@example.com"}
)

# Delete row
client.delete_row(ACCOUNT_ID, "Customers", "123")
```

### Batch Operations

```python
# Batch insert
batch = client.batch_insert(
    ACCOUNT_ID,
    "Customers",
    rows=[
        {"Name": "Alice", "Email": "alice@example.com"},
        {"Name": "Bob", "Email": "bob@example.com"},
        {"Name": "Charlie", "Email": "charlie@example.com"}
    ]
)

# Batch update
batch = client.batch_update(
    ACCOUNT_ID,
    "Customers",
    updates=[
        {"Key": "123", "Status": "Active"},
        {"Key": "124", "Status": "Active"}
    ]
)

# Batch delete
client.batch_delete(
    ACCOUNT_ID,
    "Customers",
    row_ids=["123", "124", "125"]
)
```

### Advanced Querying

```python
# Query with WHERE clause
results = client.query(
    ACCOUNT_ID,
    "Orders",
    where_clause="TotalAmount > 1000",
    select_fields="OrderID, CustomerName, TotalAmount",
    order_by="OrderDate DESC",
    limit=100
)

# Search for records
results = client.search(
    ACCOUNT_ID,
    "Customers",
    search_field="Email",
    search_value="john@example.com"
)

# Complex query with multiple conditions
results = client.query(
    ACCOUNT_ID,
    "Orders",
    where_clause="Status = 'Pending' AND OrderDate >= '2024-01-01'",
    order_by="OrderDate ASC",
    limit=50,
    offset=0
)
```

### DataPages (Forms and Views)

```python
# List DataPages
datapages = client.get_datapages(ACCOUNT_ID)

# Get DataPage details
datapage = client.get_datapage(ACCOUNT_ID, "DataPage123")

# Get DataPage data
data = client.get_datapage_data(
    ACCOUNT_ID,
    "DataPage123",
    params={'Status': 'Active'}
)

# Submit form to DataPage
result = client.submit_datapage(
    ACCOUNT_ID,
    "DataPage123",
    data={
        "Name": "Jane Doe",
        "Email": "jane@example.com",
        "Message": "Hello world"
    }
)
```

### Views

```python
# List views
views = client.list_views(ACCOUNT_ID)

# Get view data
view_data = client.get_view(ACCOUNT_ID, "ActiveCustomers")

# Create view
new_view = client.create_view(
    ACCOUNT_ID,
    "HighValueCustomers",
    source_table="Customers",
    query="SELECT * FROM Customers WHERE TotalOrders > 10"
)

# Delete view
client.delete_view(ACCOUNT_ID, "OldView")
```

### Triggers

```python
# List triggers
triggers = client.list_triggers(ACCOUNT_ID)

# Execute trigger
result = client.execute_trigger(
    ACCOUNT_ID,
    "Trigger123",
    params={"OrderID": "456"}
)
```

### Stored Procedures

```python
# List stored procedures
procedures = client.list_stored_procedures(ACCOUNT_ID)

# Execute stored procedure
result = client.execute_stored_procedure(
    ACCOUNT_ID,
    "CalculateCustomerStats",
    parameters={"CustomerID": "123"}
)
```

### Files

```python
# Get file from file field
file_content = client.get_file(
    ACCOUNT_ID,
    "Documents",
    "789",
    "Attachment"
)

# Upload file
client.upload_file(
    ACCOUNT_ID,
    "Documents",
    "789",
    "Attachment",
    "/path/to/document.pdf"
)
```

### Import/Export

```python
# Import data from file
import_result = client.import_data(
    ACCOUNT_ID,
    "Customers",
    import_file="customers.csv",
    mapping={
        "CSV_Name": "Name",
        "CSV_Email": "Email",
        "CSV_Phone": "Phone"
    }
)

# Export data to CSV
csv_data = client.export_data(
    ACCOUNT_ID,
    "Customers",
    format="csv",
    params={'q.select': 'Name, Email'}
)

# Export to JSON
json_data = client.export_data(
    ACCOUNT_ID,
    "Customers",
    format="json"
)
```

### API Usage

```python
# Get API usage statistics
usage = client.get_api_usage()
print(f"Requests: {usage['Requests']}")
print(f"Limit: {usage['Limit']}")
```

## API Methods

### Authentication
- `authenticate()` - Authenticate and get access token

### Tables
- `list_tables(account_id)` - List all tables
- `get_table(account_id, table_name)` - Get table details
- `describe_table(account_id, table_name)` - Get table schema
- `create_table(account_id, table_name, columns, primary_key)` - Create table
- `delete_table(account_id, table_name)` - Delete table

### Rows
- `get_rows(account_id, table_name, params)` - Get rows
- `get_row(account_id, table_name, row_id)` - Get single row
- `insert_row(account_id, table_name, data)` - Insert row
- `update_row(account_id, table_name, row_id, data)` - Update row
- `delete_row(account_id, table_name, row_id)` - Delete row

### Batch Operations
- `batch_insert(account_id, table_name, rows)` - Batch insert
- `batch_update(account_id, table_name, updates)` - Batch update
- `batch_delete(account_id, table_name, row_ids)` - Batch delete

### Query & Search
- `query(account_id, table_name, where_clause, ...)` - Advanced query
- `search(account_id, table_name, search_field, search_value)` - Search

### DataPages
- `get_datapages(account_id)` - List DataPages
- `get_datapage(account_id, datapage_id)` - Get DataPage details
- `get_datapage_data(account_id, datapage_id, params)` - Get DataPage data
- `submit_datapage(account_id, datapage_id, data)` - Submit form

### Views
- `list_views(account_id)` - List views
- `get_view(account_id, view_name)` - Get view data
- `create_view(account_id, view_name, source_table, query)` - Create view
- `delete_view(account_id, view_name)` - Delete view

### Triggers
- `list_triggers(account_id)` - List triggers
- `execute_trigger(account_id, trigger_id, params)` - Execute trigger

### Stored Procedures
- `list_stored_procedures(account_id)` - List procedures
- `execute_stored_procedure(account_id, procedure_name, parameters)` - Execute

### Files
- `get_file(account_id, table_name, row_id, field_name)` - Get file
- `upload_file(account_id, table_name, row_id, field_name, file_path)` - Upload file

### Import/Export
- `import_data(account_id, table_name, import_file, mapping)` - Import data
- `export_data(account_id, table_name, format, params)` - Export data

### Usage
- `get_api_usage()` - Get usage statistics

## Query Syntax

Caspio uses SQL-like query syntax:

```python
# WHERE clause examples
client.query(
    ACCOUNT_ID,
    "Customers",
    where_clause="Status = 'Active'"
)

# Multiple conditions
client.query(
    ACCOUNT_ID,
    "Orders",
    where_clause="Status = 'Pending' AND TotalAmount > 100"
)

# Date range
client.query(
    ACCOUNT_ID,
    "Orders",
    where_clause="OrderDate BETWEEN '2024-01-01' AND '2024-12-31'"
)

# LIKE pattern matching
client.query(
    ACCOUNT_ID,
    "Customers",
    where_clause="Name LIKE 'John%'"
)

# IN clause
client.query(
    ACCOUNT_ID,
    "Orders",
    where_clause="Status IN ('Pending', 'Processing')"
)

# ORDER BY
client.query(
    ACCOUNT_ID,
    "Orders",
    where_clause="TotalAmount > 0",
    order_by="OrderDate DESC, TotalAmount ASC"
)
```

## Data Types

Caspio supports these data types:
- `Text` - Short text
- `Memo` - Long text
- `Number` - Numeric values
- `Currency` - Monetary values
- `Date` - Date (no time)
- `DateTime` - Date and time
- `Yes/No` - Boolean
- `File` - File uploads
- `List` - Predefined choices
- `MultiSelectList` - Multiple choices
- `Autonumber` - Auto-increment
- `Timestamp` - Automatic timestamp
- `Formula` - Computed value

## Best Practices

1. **Use batch operations**: For bulk operations to reduce API calls
2. **Query filtering**: Use WHERE clause to limit returned data
3. **Pagination**: Use `q.limit` and `q.offset` for large datasets
4. **Error handling**: Catch and handle HTTP exceptions
5. **Token management**: Tokens auto-refresh on 401 errors
6. **Data validation**: Validate data before sending to the API
7. **File handling**: Use appropriate content types for file uploads