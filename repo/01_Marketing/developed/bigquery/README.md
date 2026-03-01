# BigQuery API Integration

## Overview
BigQuery API for Google Cloud data warehouse operations. Query, search, and insert data into BigQuery tables.

## Supported Features
- ✅ Execute Query - Run SQL queries
- ✅ Search Records - Search tables with filters
- ✅ Create Record - Insert new data

## Setup

### 1. Get OAuth Access Token
1. Go to Google Cloud Console
2. Create OAuth 2.0 credentials
3. Get access token using OAuth flow or service account

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
access_token = "your_oauth_access_token"
project_id = "your_google_cloud_project_id"
```

## Usage

```python
from bigquery_client import BigQueryClient

client = BigQueryClient(
    access_token="your_access_token",
    project_id="my-project-123"
)

# Execute SQL query
result = client.execute_query(
    "SELECT COUNT(*) as count FROM `my-project.dataset.users`"
)
print(result.rows)

# Search with filters
records = client.search_records(
    table="users",
    dataset="dataset",
    filters={"status": "active", "country": "Japan"},
    limit=100
)

# Insert new record
client.create_record(
    table="users",
    dataset="dataset",
    record={
        "email": "user@example.com",
        "name": "John Doe",
        "created_at": "2024-01-01"
    },
    insert_id="user_123"
)

client.close()
```

## Integration Type
- **Type:** OAuth 2.0
- **Authentication:** Bearer token (Authorization header)
- **Protocol:** HTTPS REST API
- **Google Cloud Platform:** BigQuery v2 API

## Testability
- ✅ Query operations: Testable with valid access token
- ✅ Insert operations: Requires table write permissions
- ✅ Search operations: Requires table read permissions

## Notes
- Access tokens expire; refresh using client credentials
- Query results are paginated; handle large datasets appropriately
- Use standard SQL by default (legacy SQL available)
- Insert operations return status for each row