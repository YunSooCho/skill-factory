# AWS Athena Integration

AWS Athena is an interactive, serverless query service that makes it easy to analyze data directly in Amazon S3 using standard SQL. No infrastructure to manage.

## Installation
```bash
pip install -e .
```

## AWS Credentials Setup

1. Install AWS CLI: `pip install awscli`
2. Configure credentials: `aws configure`
3. Or set environment variables:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_DEFAULT_REGION`

Or create an IAM user with appropriate Athena permissions:
- `AmazonAthenaFullAccess` or custom policies
- S3 access for query results

## Usage

### Initialize Client

```python
from aws_athena import AthenaClient

client = AthenaClient(
    region_name="us-east-1",
    output_location="s3://my-bucket/athena-results/",
    aws_access_key_id="your-access-key",
    aws_secret_access_key="your-secret-key"
)
```

### Basic Query Execution

```python
# Execute a simple query
result = client.execute_query(
    "SELECT * FROM my_table LIMIT 10",
    database="my_database"
)

print(f"Query ID: {result['query_execution_id']}")
print(f"State: {result['execution']['Status']['State']}")

# Get results
for row in result['results']['rows'][1:]:  # Skip header row
    print(row)
```

### Using Workgroups

```python
# Initialize with workgroup
client = AthenaClient(
    region_name="us-east-1",
    output_location="s3://my-bucket/athena-results/",
    workgroup="my_workgroup"
)
```

### Database Operations

```python
# List databases
databases = client.list_databases()
for db in databases:
    print(db)

# Create database
client.create_database("new_database")

# Drop database
client.drop_database("old_database")
```

### Table Operations

```python
# List tables in a database
tables = client.list_tables("my_database")
for table in tables:
    print(f"Table: {table['Name']}")

# Get table metadata
metadata = client.get_table_metadata("my_database", "my_table")
print(f"Columns: {metadata['Columns']}")
```

### Advanced Query Execution

```python
# Query with wait for completion
result = client.execute_query(
    "SELECT count(*) as total FROM my_table WHERE date > '2024-01-01'",
    database="my_database",
    wait=True,
    timeout=120
)

# Query without waiting (async)
query_id = client.start_query_execution(
    query_string="SELECT * FROM large_table",
    database="my_database"
)

# Later, get results
execution = client.wait_for_query_completion(query_id)
if execution['Status']['State'] == 'SUCCEEDED':
    results = client.get_query_results(query_id)
```

### Pandas DataFrame Integration

```python
# Execute query and get DataFrame
df = client.query_to_dataframe(
    "SELECT * FROM sales WHERE date >= '2024-01-01'",
    database="analytics"
)

print(df.head())
print(df.describe())
```

### Batch Queries

```python
# Run multiple queries in parallel
queries = [
    "SELECT count(*) FROM table1",
    "SELECT count(*) FROM table2",
    "SELECT count(*) FROM table3"
]

results = client.batch_query(queries, database="my_db", parallel=3)
for result in results:
    if 'error' not in result:
        print(f"Query completed: {result['query_execution_id']}")
    else:
        print(f"Query failed: {result['error']}")
```

### Export Results

```python
# Execute query
result = client.execute_query("SELECT * FROM users", database="users_db")

# Export to S3 as CSV
csv_path = client.export_results_to_s3(
    result['query_execution_id'],
    bucket="results-bucket",
    key="exports/users.csv",
    format="csv"
)

# Export as JSON
json_path = client.export_results_to_s3(
    result['query_execution_id'],
    bucket="results-bucket",
    key="exports/users.json",
    format="json"
)
```

### Named Queries (Saved Queries)

```python
# List named queries
named_queries = client.list_named_queries()

# Create named query
query_id = client.create_named_query(
    name="get_daily_sales",
    database="analytics",
    query_string="SELECT * FROM sales WHERE date = CURRENT_DATE",
    description="Get today's sales"
)

# Get named query details
query_details = client.get_named_query(query_id)
print(query_details['QueryString'])

# Delete named query
client.delete_named_query(query_id)
```

### Workgroup Management

```python
# List workgroups
workgroups = client.get_workgroups()

# Create workgroup
client.create_workgroup(
    name="analytics_workgroup",
    configuration={
        'ResultConfiguration': {
            'OutputLocation': 's3://my-bucket/analytics/'
        },
        'EnforceWorkGroupConfiguration': True
    },
    description="Workgroup for analytics queries"
)

# Delete workgroup
client.delete_workgroup("old_workgroup")
```

### Data Catalog

```python
# Get entire catalog structure
catalog = client.get_data_catalog()

# Get structure for specific database
db_catalog = client.get_data_catalog(database="my_database")
print(f"Tables in {db_catalog['database']}:")
for table in db_catalog['tables']:
    print(f"  - {table['Name']}")
```

### Cancel Query

```python
# Start a long-running query
query_id = client.start_query_execution(
    "SELECT * FROM very_large_table",
    database="my_db"
)

# Cancel if needed
client.cancel_query(query_id)
```

### Query History

```python
# Get recent query history
history = client.get_query_history(max_results=10)
for query_id in history:
    execution = client.get_query_execution(query_id)
    print(f"{query_id}: {execution['Status']['State']}")
```

## API Methods

### Query Execution
- `start_query_execution(query_string, database, ...)` - Start query
- `get_query_execution(query_id)` - Get query status
- `get_query_results(query_id, max_results, next_token)` - Get results
- `wait_for_query_completion(query_id, ...)` - Wait for completion
- `execute_query(query_string, database, wait, timeout)` - Execute and wait
- `query_to_dataframe(query_string, database, timeout)` - Return DataFrame
- `cancel_query(query_id)` - Cancel running query

### Database & Catalog
- `list_databases(max_results)` - List databases
- `create_database(database)` - Create database
- `drop_database(database)` - Drop database
- `list_tables(database, ...)` - List tables
- `get_table_metadata(database, table)` - Get table details
- `get_data_catalog(database, catalog_name)` - Get catalog structure

### Batch & Export
- `batch_query(queries, database, parallel)` - Run multiple queries
- `export_results_to_s3(query_id, bucket, key, format)` - Export to S3

### Named Queries
- `list_named_queries()` - List saved queries
- `create_named_query(name, database, query_string, ...)` - Create saved query
- `get_named_query(query_id)` - Get query details
- `delete_named_query(query_id)` - Delete saved query

### Workgroups
- `get_workgroups()` - List workgroups
- `create_workgroup(name, configuration, description)` - Create workgroup
- `delete_workgroup(name)` - Delete workgroup

### History
- `get_query_history(max_results)` - Get execution history

## Athena SQL Examples

```sql
-- Basic SELECT
SELECT * FROM cloudfront_logs LIMIT 100;

-- Filter with WHERE
SELECT * FROM sales WHERE date >= '2024-01-01';

-- Aggregations
SELECT product_id, SUM(revenue) as total_revenue
FROM sales
GROUP BY product_id
ORDER BY total_revenue DESC;

-- JOIN tables
SELECT c.name, o.order_id, o.amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01';

-- Window functions
SELECT *,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) as running_total
FROM orders;

-- Create table from query
CREATE TABLE IF NOT EXISTS daily_sales AS
SELECT date, COUNT(*) as orders, SUM(amount) as revenue
FROM sales
GROUP BY date;

-- Partitioning (recommended for large datasets)
CREATE EXTERNAL TABLE IF NOT EXISTS partitioned_logs (
    user_id STRING,
    action STRING,
    timestamp TIMESTAMP
)
PARTITIONED BY (date STRING, region STRING)
STORED AS PARQUET
LOCATION 's3://my-bucket/logs/';
```

## Best Practices

1. **Partitioning**: Use partitioned tables for better performance and cost reduction
2. **Columnar formats**: Use Parquet/ORC for storage efficiency
3. **Result caching**: Athena caches results for re-running queries
4. **Workgroups**: Use workgroups to control costs and manage permissions
5. **Query optimization**: LIMIT results during development and testing
6. **S3 bucket locations**: Use separate buckets or prefixes for different workloads
7. **Data catalog partitions**: Use MSCK REPAIR TABLE or ADD PARTITION for new partition data

## Cost Optimization

- Use columnar formats (Parquet/ORC) to scan less data
- Partition data by date, region, or other filter criteria
- Use LIMIT to reduce data scanned
- Use AWS Cost Explorer to monitor spend
- Set up budgets and alerts

## Error Handling

```python
try:
    result = client.execute_query("SELECT * FROM table", database="db")
except ClientError as e:
    if e.response['Error']['Code'] == 'InvalidRequestException':
        print("Invalid query")
    elif e.response['Error']['Code'] == 'ResourceNotFoundException':
        print("Database or table not found")
    else:
        print(f"Error: {e}")
except TimeoutError:
    print("Query timed out")
except Exception as e:
    print(f"Unexpected error: {e}")
```