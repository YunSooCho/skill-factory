# Coda API Client

Python async client for Coda's document collaboration platform.

## Features

- ✅ Add/Update/Delete table rows
- ✅ Search table rows
- ✅ Get row details
- ✅ Create pages
- ✅ Manage permissions
- ✅ Webhook verification (Row Created, Row Updated)
- ✅ Async/await support
- ✅ Type hints and dataclasses

## Installation

```bash
pip install -r requirements.txt
```

## API Token

Get your API token from: https://coda.io/account

## Usage

### Initialize Client

```python
import asyncio
from coda_client import CodaAPIClient

async def main():
    api_token = "your-api-token-here"

    async with CodaAPIClient(api_token) as client:
        # Use the client
        pass

asyncio.run(main())
```

### Add Row

Add a new row to a Coda table.

```python
async with CodaAPIClient(api_token) as client:
    result = await client.add_row(
        doc_id="doc-abc123",
        table_id="table-xyz789",
        cells={
            "Name": "John Doe",
            "Email": "john@example.com",
            "Status": "Active",
            "Priority": "High"
        },
        key_columns=["Email"]  # Optional: for upsert
    )

    if result.success:
        print(f"Row created: {result.row.id}")
        print(f"Cells: {result.row.cells}")
```

### Get Row

Retrieve a specific row.

```python
async with CodaAPIClient(api_token) as client:
    result = await client.get_row(
        doc_id="doc-abc123",
        table_id="table-xyz789",
        row_id="row-123",
        use_column_names=True  # Use names instead of column IDs
    )

    if result.success:
        print(f"Row ID: {result.row.id}")
        print(f"Data: {result.row.cells}")
```

### Update Row

Update an existing row.

```python
async with CodaAPIClient(api_token) as client:
    result = await client.update_row(
        doc_id="doc-abc123",
        table_id="table-xyz789",
        row_id="row-123",
        cells={
            "Status": "Completed",
            "CompletedDate": "2026-02-28"
        }
    )

    if result.success:
        print(f"Row updated: {result.row.id}")
```

### Delete Row

Delete a row.

```python
async with CodaAPIClient(api_token) as client:
    result = await client.delete_row(
        doc_id="doc-abc123",
        table_id="table-xyz789",
        row_id="row-123"
    )

    if result.success:
        print("Row deleted successfully")
```

### Search Row

Search for rows matching a query.

```python
async with CodaAPIClient(api_token) as client:
    result = await client.search_row(
        doc_id="doc-abc123",
        table_id="table-xyz789",
        query="John",
        use_column_names=True,
        limit=50
    )

    print(f"Found {result.total} rows:")
    for row in result.results:
        print(f"  - {row.row.id}: {row.cells.get('Name', '')}")
```

### Create Page

Create a new page in a document.

```python
async with CodaAPIClient(api_token) as client:
    result = await client.create_page(
        doc_id="doc-abc123",
        title="New Section",
        parent_id="page-456",  # Optional: parent page
        predecessor_id="page-789"  # Optional: order position
    )

    if result.success:
        page = result.page
        print(f"Page created: {page.id}")
        print(f"Title: {page.title}")
        print(f"URL: {page.browser_link}")
```

### Add Permission

Add permissions to a document.

```python
# Add user permission
async with CodaAPIClient(api_token) as client:
    result = await client.add_permission(
        doc_id="doc-abc123",
        permission_type="user",
        access_level="edit",
        email="john@example.com"
    )

    if result.success:
        print("User permission added")

# Add group permission
result = await client.add_permission(
    doc_id="doc-abc123",
    permission_type="group",
    access_level="read",
    group_id="group-123"
)
```

### Webhook Integration

Set up webhooks for row events.

```python
# Verify webhook signature
def handle_webhook(payload: dict, signature: str, secret: str):
    if client.verify_webhook(payload, signature, secret):
        event = client.parse_webhook_event(payload)

        if event["event_type"] == "doc.rowCreated":
            row = event["data"].get("row", {})
            print(f"New row created: {row.get('id')}")
            # Process new row

        elif event["event_type"] == "doc.rowUpdated":
            row = event["data"].get("row", {})
            changes = event["data"].get("changes", {})
            print(f"Row updated: {row.get('id')}")
            print(f"Changes: {changes}")
            # Process updated row
    else:
        print("Invalid webhook signature")
```

## API Actions

### Add Row

Add a new row to a table.

**Parameters:**
- `doc_id` (str): Document ID
- `table_id` (str): Table ID
- `cells` (Dict[str, Any]): Column values
- `key_columns` (Optional[List[str]]): Key columns for upsert

**Returns:** `RowResponse`

### Get Row

Retrieve a specific row.

**Parameters:**
- `doc_id` (str): Document ID
- `table_id` (str): Table ID
- `row_id` (str): Row ID
- `use_column_names` (bool): Use column names (default: False)

**Returns:** `RowResponse`

### Update Row

Update an existing row.

**Parameters:**
- `doc_id` (str): Document ID
- `table_id` (str): Table ID
- `row_id` (str): Row ID
- `cells` (Dict[str, Any]): Column values to update
- `key_columns` (Optional[List[str]]): Key columns

**Returns:** `RowResponse`

### Delete Row

Delete a row.

**Parameters:**
- `doc_id` (str): Document ID
- `table_id` (str): Table ID
- `row_id` (str): Row ID

**Returns:** `RowResponse`

### Search Row

Search for rows.

**Parameters:**
- `doc_id` (str): Document ID
- `table_id` (str): Table ID
- `query` (str): Search query
- `use_column_names` (bool): Use column names (default: False)
- `limit` (int): Maximum results (default: 100)

**Returns:** `SearchResponse`

### Create Page

Create a new page.

**Parameters:**
- `doc_id` (str): Document ID
- `title` (str): Page title
- `parent_id` (Optional[str]): Parent page ID
- `predecessor_id` (Optional[str]): Predecessor page ID

**Returns:** `PageResponse`

### Add Permission

Add document permissions.

**Parameters:**
- `doc_id` (str): Document ID
- `permission_type` (str): 'user' or 'group'
- `access_level` (str): 'read', 'write', 'edit', 'admin'
- `email` (Optional[str]): User email (for user type)
- `group_id` (Optional[str]): Group ID (for group type)

**Returns:** `PermissionResponse`

## Webhook Events

### Row Created

Triggered when a new row is created.

**Event Type:** `doc.rowCreated`

**Payload:**
```json
{
  "type": "doc.rowCreated",
  "id": "evt-123",
  "timestamp": "2026-02-28T12:00:00Z",
  "data": {
    "row": {
      "id": "row-123",
      "cells": {...}
    }
  }
}
```

### Row Updated

Triggered when a row is updated.

**Event Type:** `doc.rowUpdated`

**Payload:**
```json
{
  "type": "doc.rowUpdated",
  "id": "evt-456",
  "timestamp": "2026-02-28T12:00:00Z",
  "data": {
    "row": {...},
    "changes": {...}
  }
}
```

## Getting Document/Table IDs

1. **Document ID:** Found in the document URL
   - URL: `https://coda.io/d/doc-abc123/My-Document`
   - ID: `doc-abc123`

2. **Table ID:**
   - Right-click table → Copy → Copy table ID
   - Or use the Coda API to list tables

3. **Row ID:** Returned from Add Row or Get Row operations

## Best Practices

1. **Use column names:** Set `use_column_names=True` for more readable code
2. **Batch operations:** Use efficient queries to minimize API calls
3. **Error handling:** Check `success` field before using results
4. **Webhook security:** Always verify webhook signatures
5. **Rate limits:** Coda has rate limits - implement backoff if needed

## API Reference

Official documentation: https://coda.io/developers/apis/

## Support

For issues, visit: https://help.coda.io/