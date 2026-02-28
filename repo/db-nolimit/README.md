# DB-Nolimit Database Integration

DB-Nolimit is a scalable database solution with unlimited storage capacity, flexible schema, and high-performance querying capabilities.

## Installation
```bash
pip install -e .
```

## API Key Setup

1. Sign up at DB-Nolimit service
2. Create a new project/database
3. Generate API key from settings
4. Note your endpoint URL
5. Use credentials in your application

## Usage

### Initialize Client

```python
from db_nolimit import DBNolimitClient

client = DBNolimitClient(
    api_key="your-api-key",
    endpoint="https://api.db-nolimit.com"
)
```

### Databases

```python
# List databases
databases = client.list_databases()

# Create database
db = client.create_database(
    name="my_project",
    description="Project database"
)

# Get database details
db_info = client.get_database("my_project")

# Delete database
client.delete_database("my_project")

# Get statistics
stats = client.get_stats("my_project")
```

### Tables

```python
DB_NAME = "my_project"

# List tables
tables = client.list_tables(DB_NAME)

# Create table with schema
table = client.create_table(
    DB_NAME,
    "users",
    schema={
        "id": "string",
        "name": "string",
        "email": "string",
        "age": "number",
        "created_at": "datetime"
    },
    indexes=["email", "created_at"]
)

# Get table details
table_info = client.get_table(DB_NAME, "users")

# Delete table
client.delete_table(DB_NAME, "users")
```

### CRUD Operations

```python
DB_NAME = "my_project"
TABLE_NAME = "users"

# Insert record
new_user = client.insert(
    DB_NAME,
    TABLE_NAME,
    {
        "id": "user1",
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }
)

# Insert multiple records
batch = client.insert_many(
    DB_NAME,
    TABLE_NAME,
    [
        {"id": "user2", "name": "Jane", "email": "jane@example.com"},
        {"id": "user3", "name": "Bob", "email": "bob@example.com"}
    ]
)

# Find records
users = client.find(DB_NAME, TABLE_NAME, limit=10)

# Find with query
adult_users = client.find(
    DB_NAME,
    TABLE_NAME,
    query={"age": {"$gte": 18}},
    sort={"created_at": -1},
    limit=100
)

# Find one record
user = client.find_one(
    DB_NAME,
    TABLE_NAME,
    query={"email": "john@example.com"}
)

# Get record by ID
record = client.get(DB_NAME, TABLE_NAME, "user1")

# Update record
updated = client.update(
    DB_NAME,
    TABLE_NAME,
    "user1",
    {"age": 31}
)

# Update multiple records
result = client.update_many(
    DB_NAME,
    TABLE_NAME,
    query={"age": {"$lt": 18}},
    updates={"status": "minor"}
)

# Delete record
client.delete(DB_NAME, TABLE_NAME, "user1")

# Delete multiple records
result = client.delete_many(
    DB_NAME,
    TABLE_NAME,
    query={"status": "inactive"}
)
```

### Advanced Queries

```python
# Query with multiple conditions
results = client.find(
    DB_NAME,
    TABLE_NAME,
    query={
        "age": {"$gte": 18, "$lte": 65},
        "status": "active"
    }
)

# Sorting
results = client.find(
    DB_NAME,
    TABLE_NAME,
    sort={"created_at": -1, "name": 1}
)

# Pagination
page1 = client.find(DB_NAME, TABLE_NAME, limit=10, offset=0)
page2 = client.find(DB_NAME, TABLE_NAME, limit=10, offset=10)

# Count records
count = client.count(DB_NAME, TABLE_NAME)
active_count = client.count(DB_NAME, TABLE_NAME, query={"status": "active"})
```

### Aggregation

```python
# Aggregation pipeline
pipeline = [
    {
        "$match": {"age": {"$gte": 18}}
    },
    {
        "$group": {
            "_id": "$status",
            "count": {"$sum": 1},
            "avg_age": {"$avg": "$age"}
        }
    },
    {
        "$sort": {"count": -1}
    }
]

results = client.aggregate(DB_NAME, TABLE_NAME, pipeline)
```

### Indexes

```python
# Create index
index = client.create_index(
    DB_NAME,
    TABLE_NAME,
    "email_index",
    fields=["email"],
    unique=True
)

# List indexes
indexes = client.list_indexes(DB_NAME, TABLE_NAME)

# Delete index
client.drop_index(DB_NAME, TABLE_NAME, "email_index")
```

### Transactions

```python
# Execute multiple operations atomically
operations = [
    {
        "type": "insert",
        "table": "users",
        "data": {"id": "user4", "name": "Alice"}
    },
    {
        "type": "update",
        "table": "logs",
        "query": {"id": "log1"},
        "updates": {"action": "user_added"}
    }
]

result = client.transaction(operations)
```

### Backup & Restore

```python
# Create backup
backup = client.backup_database("my_project")

# Restore from backup
restore = client.restore_database("my_project", backup_id="backup_123")
```

### Import/Export

```python
# Export data
json_data = client.export_data("my_project", "users", format="json")

# Import data
result = client.import_data(
    "my_project",
    "users",
    format="json",
    data=json_data
)
```

### Search

```python
# Full-text search
results = client.search(
    DB_NAME,
    TABLE_NAME,
    search_term="John Doe",
    fields=["name", "email"]
)
```

## API Methods

### Databases
- `list_databases()` - List databases
- `create_database(name, description)` - Create database
- `get_database(db_name)` - Get database details
- `delete_database(db_name)` - Delete database
- `get_stats(db_name)` - Get statistics

### Tables
- `list_tables(db_name)` - List tables
- `create_table(db_name, table_name, schema, indexes)` - Create table
- `get_table(db_name, table_name)` - Get table details
- `delete_table(db_name, table_name)` - Delete table

### Records
- `insert(db_name, table_name, record)` - Insert record
- `insert_many(db_name, table_name, records)` - Batch insert
- `find(db_name, table_name, query, limit, offset, sort)` - Find records
- `find_one(db_name, table_name, query)` - Find one record
- `get(db_name, table_name, record_id)` - Get by ID
- `update(db_name, table_name, record_id, updates)` - Update record
- `update_many(db_name, table_name, query, updates)` - Batch update
- `delete(db_name, table_name, record_id)` - Delete record
- `delete_many(db_name, table_name, query)` - Batch delete
- `count(db_name, table_name, query)` - Count records

### Advanced
- `aggregate(db_name, table_name, pipeline)` - Run aggregation
- `transaction(operations)` - Execute transaction
- `search(db_name, table_name, search_term, fields)` - Full-text search

### Indexes
- `create_index(db_name, table_name, index_name, fields, unique)` - Create index
- `list_indexes(db_name, table_name)` - List indexes
- `drop_index(db_name, table_name, index_name)` - Delete index

### Backup/Restore
- `backup_database(db_name)` - Create backup
- `restore_database(db_name, backup_id)` - Restore backup

### Import/Export
- `export_data(db_name, table_name, format)` - Export data
- `import_data(db_name, table_name, format, data)` - Import data

## Query Operators

DB-Nolimit supports these query operators:

- `$eq` - Equal to
- `$ne` - Not equal to
- `$gt` - Greater than
- `$gte` - Greater than or equal to
- `$lt` - Less than
- `$lte` - Less than or equal to
- `$in` - In array
- `$nin` - Not in array
- `$and` - AND condition
- `$or` - OR condition
- `$not` - NOT condition
- `$exists` - Field exists
- `$regex` - Regular expression match

## Aggregation Operators

- `$match` - Filter documents
- `$group` - Group documents
- `$sort` - Sort results
- `$limit` - Limit results
- `$skip` - Skip results
- `$project` - Project fields
- `$unwind` - Unwind arrays
- `$count` - Count documents
- `$sum` - Sum values
- `$avg` - Average values
- `$min` - Minimum value
- `$max` - Maximum value